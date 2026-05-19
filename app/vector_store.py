from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
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


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


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
