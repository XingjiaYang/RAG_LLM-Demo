from __future__ import annotations

from dataclasses import dataclass

from app.config import Settings, settings
from app.llm_client import LocalLLMClient
from app.vector_store import SearchResult, VectorStore


@dataclass(frozen=True)
class RAGAnswer:
    answer: str
    contexts: list[SearchResult]


class RAGPipeline:
    def __init__(
        self,
        config: Settings = settings,
        vector_store: VectorStore | None = None,
        llm_client: LocalLLMClient | None = None,
    ) -> None:
        self.config = config
        self.vector_store = vector_store or VectorStore(config)
        self.llm_client = llm_client or LocalLLMClient(config)

    def answer(self, question: str, top_k: int | None = None) -> RAGAnswer:
        contexts = self.vector_store.search(question, top_k=top_k)
        messages = self._build_messages(question, contexts)
        answer = self.llm_client.chat(messages)
        return RAGAnswer(answer=answer, contexts=contexts)

    def _build_messages(
        self,
        question: str,
        contexts: list[SearchResult],
    ) -> list[dict[str, str]]:
        context_text = "\n\n".join(
            (
                f"[{idx}] source={item.source} chunk={item.chunk_id} "
                f"score={item.score:.4f}\n{item.text}"
            )
            for idx, item in enumerate(contexts, start=1)
        )
        if not context_text:
            context_text = "No retrieved context."

        system_prompt = (
            "You are a concise technical assistant. Answer using the retrieved "
            "context when it is relevant. If the context is insufficient, say so "
            "and avoid inventing details."
        )
        user_prompt = (
            "Retrieved context:\n"
            f"{context_text}\n\n"
            "Question:\n"
            f"{question}\n\n"
            "Answer in the same language as the question when possible."
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
