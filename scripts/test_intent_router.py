from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import Settings
from app.intent_router import IntentRouter
from app.rag import RAGPipeline
from app.vector_store import SearchResult


@dataclass(frozen=True)
class Message:
    role: str
    content: str


class FakeVectorStore:
    model = None

    def __init__(self) -> None:
        self.search_calls = 0

    def search(self, query: str, top_k: int | None = None) -> list[SearchResult]:
        self.search_calls += 1
        return [
            SearchResult(
                text="PostgreSQL is an OLTP database.",
                source="data/docs/postgresql.md",
                chunk_id=0,
                score=0.9,
            )
        ]


class FakeLLMClient:
    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        return "ok"


def assert_route(
    router: IntentRouter,
    question: str,
    expected_use_rag: bool,
    history: list[Message] | None = None,
) -> None:
    decision = router.route(question, history or [], "")
    if decision.use_rag != expected_use_rag:
        raise AssertionError(
            f"{question!r} routed to {decision.use_rag}, "
            f"expected {expected_use_rag}. Decision: {decision}"
        )
    print(f"{question!r} -> {decision.route}: {decision.reason}")


def assert_pipeline_search_behavior() -> None:
    config = Settings()
    vector_store = FakeVectorStore()
    llm_client = FakeLLMClient()
    router = IntentRouter(config, embedder=None, llm_client=None)
    pipeline = RAGPipeline(
        config,
        vector_store=vector_store,
        llm_client=llm_client,
        intent_router=router,
    )

    direct_answer = pipeline.answer("今天天气怎么样？")
    if direct_answer.used_rag or vector_store.search_calls != 0:
        raise AssertionError("Direct route should not call vector search.")

    rag_answer = pipeline.answer("PostgreSQL 的事务隔离怎么理解？")
    if not rag_answer.used_rag or vector_store.search_calls != 1:
        raise AssertionError("Database route should call vector search once.")

    print("Pipeline search behavior -> ok")


def main() -> None:
    router = IntentRouter(Settings(), embedder=None, llm_client=None)

    assert_route(router, "Compare PostgreSQL and MySQL for OLTP.", True)
    assert_route(router, "今天天气怎么样？", False)
    assert_route(router, "写一首关于 PostgreSQL 的诗", False)
    assert_route(
        router,
        "那它和另一个相比呢？",
        True,
        history=[Message("user", "PostgreSQL 和 MySQL 怎么选？")],
    )
    assert_route(
        router,
        "不用知识库，直接回答：PostgreSQL 是什么？",
        False,
    )
    assert_route(router, "基于文档回答：SQLite 适合什么场景？", True)
    assert_pipeline_search_behavior()


if __name__ == "__main__":
    main()
