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


class FakeClassifierLLM:
    def __init__(self, response: str) -> None:
        self.response = response

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        return self.response


class FakeIntentEmbedder:
    def encode(
        self,
        texts: str | list[str] | tuple[str, ...],
        normalize_embeddings: bool = True,
    ) -> list[float] | list[list[float]]:
        if isinstance(texts, str):
            return self._encode_one(texts)
        return [self._encode_one(text) for text in texts]

    def _encode_one(self, text: str) -> list[float]:
        lowered = text.lower()
        direct_markers = (
            "casual conversation",
            "writing, translation",
            "unrelated to database documentation",
            "math, travel",
            "general ai assistant",
            "闲聊",
            "周末旅行",
            "天气",
        )
        if any(marker in lowered for marker in direct_markers):
            return [0.0, 1.0]

        db_markers = (
            "database",
            "databases",
            "postgresql",
            "mysql",
            "oltp",
            "olap",
            "storage",
            "数据库",
            "事务",
        )
        if any(marker in lowered for marker in db_markers):
            return [1.0, 0.0]

        return [0.5, 0.5]


def assert_route(
    router: IntentRouter,
    question: str,
    expected_use_rag: bool,
    history: list[Message] | None = None,
    expected_route: str | None = None,
    conversation_summary: str = "",
) -> None:
    decision = router.route(question, history or [], conversation_summary)
    if decision.use_rag != expected_use_rag:
        raise AssertionError(
            f"{question!r} routed to {decision.use_rag}, "
            f"expected {expected_use_rag}. Decision: {decision}"
        )
    if expected_route is not None and decision.route != expected_route:
        raise AssertionError(
            f"{question!r} used route {decision.route}, "
            f"expected {expected_route}. Decision: {decision}"
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


def assert_embedding_context_behavior() -> None:
    router = IntentRouter(Settings(), embedder=FakeIntentEmbedder(), llm_client=None)
    history = [
        Message("user", "PostgreSQL 和 MySQL 怎么选？"),
        Message("assistant", "PostgreSQL 更适合需要复杂 SQL 和扩展的 OLTP。"),
    ]

    classification_text = router._classification_text(
        "那它和另一个相比呢？",
        history,
        "User is comparing transactional databases.",
    )
    if "USER: PostgreSQL 和 MySQL 怎么选？" not in classification_text:
        raise AssertionError("Embedding classification text should include user turns.")
    if "ASSISTANT: PostgreSQL 更适合" not in classification_text:
        raise AssertionError(
            "Embedding classification text should include assistant turns."
        )

    assert_route(
        router,
        "那它和另一个相比呢？",
        True,
        history=history,
        expected_route="embedding_rag",
        conversation_summary="User is comparing transactional databases.",
    )
    assert_route(
        router,
        "周末旅行怎么规划？",
        False,
        expected_route="embedding_direct",
    )


def assert_llm_fallback_behavior() -> None:
    rag_router = IntentRouter(
        Settings(),
        embedder=None,
        llm_client=FakeClassifierLLM(
            '{"use_rag": "true", "reason": "DB follow-up"}'
        ),
    )
    assert_route(
        rag_router,
        "那长期维护成本呢？",
        True,
        history=[Message("assistant", "We compared PostgreSQL and MySQL.")],
        expected_route="llm_rag",
    )

    direct_router = IntentRouter(
        Settings(),
        embedder=None,
        llm_client=FakeClassifierLLM(
            '{"use_rag": "false", "reason": "general chat"}'
        ),
    )
    assert_route(
        direct_router,
        "推荐一份晚餐菜单",
        False,
        expected_route="llm_direct",
    )


def main() -> None:
    router = IntentRouter(Settings(), embedder=None, llm_client=None)

    assert_route(
        router,
        "Compare PostgreSQL and MySQL for OLTP.",
        True,
        expected_route="keyword_rag",
    )
    assert_route(
        router,
        "Hi, what is PostgreSQL?",
        True,
        expected_route="keyword_rag",
    )
    assert_route(
        router,
        "今天天气怎么样？",
        False,
        expected_route="fallback_direct",
    )
    assert_route(
        router,
        "写一首关于 PostgreSQL 的诗",
        False,
        expected_route="keyword_direct",
    )
    assert_route(
        router,
        "PostgreSQL email notification pattern 怎么设计？",
        True,
        expected_route="keyword_rag",
    )
    assert_route(
        router,
        "不用知识库，直接回答：PostgreSQL 是什么？",
        False,
        expected_route="keyword_direct",
    )
    assert_route(
        router,
        "基于文档回答：SQLite 适合什么场景？",
        True,
        expected_route="keyword_rag",
    )
    assert_embedding_context_behavior()
    assert_llm_fallback_behavior()
    assert_pipeline_search_behavior()


if __name__ == "__main__":
    main()
