from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable
from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from app.config import Settings, settings


@dataclass(frozen=True)
class SearchResult:
    text: str
    source: str
    chunk_id: int
    score: float


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    sections = _markdown_sections(text)
    if not sections:
        return []

    chunks: list[str] = []
    current_parts: list[str] = []

    for section in sections:
        for part in _split_oversized_section(section, chunk_size):
            if not current_parts:
                current_parts.append(part)
                continue

            candidate = _join_chunk_parts([*current_parts, part])
            if len(candidate) <= chunk_size:
                current_parts.append(part)
                continue

            chunks.append(_join_chunk_parts(current_parts))
            current_parts = _overlap_parts(current_parts, overlap)

            if (
                current_parts
                and len(_join_chunk_parts([*current_parts, part])) > chunk_size
            ):
                current_parts = []

            current_parts.append(part)

    if current_parts:
        chunks.append(_join_chunk_parts(current_parts))

    return chunks


def _markdown_sections(text: str) -> list[str]:
    heading_stack: list[tuple[int, str]] = []
    body_lines: list[str] = []
    sections: list[str] = []
    in_fence = False

    def flush_body() -> None:
        body = "\n".join(body_lines).strip()
        body_lines.clear()
        if not body:
            return

        heading_context = "\n".join(heading for _, heading in heading_stack)
        section = "\n\n".join(part for part in [heading_context, body] if part)
        if section:
            sections.append(section)

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        if _FENCE_RE.match(line):
            body_lines.append(line)
            in_fence = not in_fence
            continue

        heading_match = _HEADING_RE.match(line) if not in_fence else None
        if heading_match:
            flush_body()
            level = len(heading_match.group(1))
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, line.strip()))
            continue

        body_lines.append(line)

    flush_body()
    return sections


def _split_oversized_section(section: str, chunk_size: int) -> list[str]:
    section = section.strip()
    if len(section) <= chunk_size:
        return [section]

    heading_prefix, body = _split_heading_prefix(section)
    if not body:
        return _word_boundary_chunks(section, chunk_size)

    body_limit = (
        chunk_size - len(heading_prefix) - 2
        if heading_prefix
        else chunk_size
    )
    body_limit = max(120, body_limit)
    parts: list[str] = []

    for body_part in _word_boundary_chunks(body, body_limit):
        chunk = "\n\n".join(
            part for part in [heading_prefix, body_part] if part
        ).strip()
        parts.append(chunk)

    return parts


def _split_heading_prefix(section: str) -> tuple[str, str]:
    lines = section.splitlines()
    prefix_lines: list[str] = []
    body_start = 0
    seen_heading = False

    for idx, line in enumerate(lines):
        if _HEADING_RE.match(line):
            prefix_lines.append(line.strip())
            seen_heading = True
            body_start = idx + 1
            continue

        if seen_heading and not line.strip():
            body_start = idx + 1
            continue

        break

    prefix = "\n".join(prefix_lines).strip()
    body = "\n".join(lines[body_start:]).strip()
    return prefix, body


def _word_boundary_chunks(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text.strip()] if text.strip() else []

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for token in re.findall(r"\S+\s*", text):
        if current and current_len + len(token) > max_chars:
            chunks.append("".join(current).strip())
            current = []
            current_len = 0

        while len(token) > max_chars:
            if current:
                chunks.append("".join(current).strip())
                current = []
                current_len = 0
            chunks.append(token[:max_chars].strip())
            token = token[max_chars:]

        current.append(token)
        current_len += len(token)

    if current:
        chunks.append("".join(current).strip())

    return [chunk for chunk in chunks if chunk]


def _join_chunk_parts(parts: list[str]) -> str:
    return "\n\n".join(part.strip() for part in parts if part.strip()).strip()


def _overlap_parts(parts: list[str], max_chars: int) -> list[str]:
    if max_chars <= 0:
        return []

    overlap: list[str] = []
    total_len = 0

    for part in reversed(parts):
        part_len = len(part)
        separator_len = 2 if overlap else 0
        if total_len + separator_len + part_len > max_chars:
            break
        overlap.insert(0, part)
        total_len += separator_len + part_len

    return overlap


class VectorStore:
    def __init__(
        self,
        config: Settings = settings,
        client: QdrantClient | None = None,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.config = config
        self.client = client or QdrantClient(url=config.qdrant_url)
        self.model = model or SentenceTransformer(config.embedding_model)

    @property
    def vector_size(self) -> int:
        if hasattr(self.model, "get_embedding_dimension"):
            size = self.model.get_embedding_dimension()
        else:
            size = self.model.get_sentence_embedding_dimension()
        if size is None:
            raise RuntimeError("Embedding model did not report a vector dimension")
        return int(size)

    def ensure_collection(self, recreate: bool = False) -> None:
        collection_names = {c.name for c in self.client.get_collections().collections}

        if recreate and self.config.collection_name in collection_names:
            self.client.delete_collection(collection_name=self.config.collection_name)
            collection_names.remove(self.config.collection_name)

        if self.config.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def ingest_markdown_dir(
        self,
        docs_dir: Path | None = None,
        recreate: bool = False,
    ) -> int:
        docs_path = docs_dir or self.config.docs_dir
        self.ensure_collection(recreate=recreate)

        points: list[PointStruct] = []
        for file_path in sorted(docs_path.glob("*.md")):
            points.extend(self._points_for_file(file_path))

        if not points:
            return 0

        self.client.upsert(
            collection_name=self.config.collection_name,
            points=points,
        )
        return len(points)

    def search(self, query: str, top_k: int | None = None) -> list[SearchResult]:
        limit = top_k or self.config.retrieve_top_k
        query_vector = self._embed_one(query)

        if hasattr(self.client, "query_points"):
            response = self.client.query_points(
                collection_name=self.config.collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True,
            )
            hits = response.points
        else:
            hits = self.client.search(
                collection_name=self.config.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
            )

        results: list[SearchResult] = []
        for hit in hits:
            payload = hit.payload or {}
            results.append(
                SearchResult(
                    text=str(payload.get("text", "")),
                    source=str(payload.get("source", "")),
                    chunk_id=int(payload.get("chunk_id", -1)),
                    score=float(hit.score),
                )
            )
        return results

    def _points_for_file(self, file_path: Path) -> Iterable[PointStruct]:
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(
            text,
            chunk_size=self.config.chunk_size,
            overlap=self.config.chunk_overlap,
        )
        if not chunks:
            return []

        embeddings = self.model.encode(chunks, normalize_embeddings=True)
        points: list[PointStruct] = []
        for idx, embedding in enumerate(embeddings):
            point_id = str(uuid5(NAMESPACE_URL, f"{file_path}:{idx}:{chunks[idx]}"))
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload={
                        "source": str(file_path),
                        "chunk_id": idx,
                        "text": chunks[idx],
                    },
                )
            )
        return points

    def _embed_one(self, text: str) -> list[float]:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
