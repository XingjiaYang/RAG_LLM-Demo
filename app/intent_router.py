from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Literal, Protocol, Sequence

import numpy as np

from app.config import Settings, settings
from app.llm_client import LocalLLMClient


RouteName = Literal[
    "disabled",
    "keyword_rag",
    "keyword_direct",
    "keyword_followup_rag",
    "embedding_rag",
    "embedding_direct",
    "llm_rag",
    "llm_direct",
    "fallback_direct",
]


class HistoryMessage(Protocol):
    role: str
    content: str


@dataclass(frozen=True)
class IntentDecision:
    use_rag: bool
    route: RouteName
    reason: str


class IntentRouter:
    DB_KEYWORDS = (
        "postgresql",
        "postgres",
        "mysql",
        "innodb",
        "sqlite",
        "duckdb",
        "rocksdb",
        "lmdb",
        "clickhouse",
        "druid",
        "pinot",
        "snowflake",
        "bigquery",
        "mongodb",
        "mongo",
        "cassandra",
        "scylladb",
        "redis",
        "elasticsearch",
        "opensearch",
        "neo4j",
        "timescaledb",
        "influxdb",
        "qdrant",
        "milvus",
        "weaviate",
        "pgvector",
        "chroma",
        "faiss",
        "cockroachdb",
        "yugabytedb",
        "tidb",
        "database",
        "databases",
        "data warehouse",
        "oltp",
        "olap",
        "sql",
        "nosql",
        "mvcc",
        "transaction",
        "transactions",
        "replication",
        "sharding",
        "consistency",
        "cap theorem",
        "storage engine",
        "query optimizer",
        "vector database",
        "vector db",
        "ann search",
        "数据库",
        "向量库",
        "向量数据库",
        "关系型数据库",
        "文档数据库",
        "图数据库",
        "时序数据库",
        "数据仓库",
        "湖仓",
        "事务",
        "索引",
        "查询优化",
        "存储引擎",
        "分布式数据库",
        "一致性",
        "复制",
        "分片",
        "列存",
        "行存",
    )

    FORCE_RAG_PHRASES = (
        "use rag",
        "use retrieval",
        "search the docs",
        "search docs",
        "use the docs",
        "according to the docs",
        "according to documentation",
        "based on the knowledge base",
        "based on local docs",
        "from the knowledge base",
        "with references",
        "cite sources",
        "基于文档",
        "根据文档",
        "根据知识库",
        "查知识库",
        "搜索知识库",
        "检索知识库",
        "使用检索",
        "引用资料",
        "带引用",
    )

    FORCE_DIRECT_PHRASES = (
        "do not use rag",
        "don't use rag",
        "without rag",
        "no rag",
        "do not retrieve",
        "don't retrieve",
        "without retrieval",
        "no retrieval",
        "answer directly",
        "不要用rag",
        "不用rag",
        "不要检索",
        "不用检索",
        "不要查库",
        "不要查知识库",
        "不用知识库",
        "直接回答",
        "别查",
    )

    DIRECT_TASK_KEYWORDS = (
        "write a poem",
        "poem",
        "write a joke",
        "make a joke",
        "joke",
        "write an email",
        "email",
        "cover letter",
        "resume bullet",
        "linkedin",
        "translate",
        "summarize my resume",
        "写诗",
        "诗",
        "写一首",
        "写一首诗",
        "讲个笑话",
        "笑话",
        "写邮件",
        "邮件",
        "写简历",
        "简历",
        "翻译",
    )

    CASUAL_DIRECT_PATTERNS = (
        r"^(hi|hello|hey|thanks|thank you|ok|okay)\b",
        r"^(你好|您好|谢谢|感谢|好的|收到)[。！!.\s]*$",
        r"(weather|天气|travel|旅行|recipe|菜谱|数学题|math problem)",
    )

    FOLLOWUP_MARKERS = (
        "it",
        "that",
        "those",
        "them",
        "this",
        "compare",
        "difference",
        "vs",
        "versus",
        "which one",
        "when should",
        "它",
        "这个",
        "那个",
        "上述",
        "这些",
        "对比",
        "相比",
        "区别",
        "优缺点",
        "怎么选",
        "哪个",
    )

    DB_ANCHORS = (
        "database systems, SQL, NoSQL, storage engines, transactions, indexes, query planning",
        "OLTP databases, concurrency control, MVCC, replication, sharding, consistency",
        "OLAP databases, analytics engines, data warehouses, columnar storage, ClickHouse, DuckDB",
        "vector databases, embedding indexes, ANN search, semantic search, Qdrant, Milvus, Weaviate, pgvector",
        "embedded databases, RocksDB, LMDB, SQLite, local storage engines",
        "time series databases, graph databases, document databases, distributed SQL systems",
        "数据库 系统 SQL 事务 索引 OLTP OLAP 向量数据库 分布式数据库 数据仓库",
    )

    DIRECT_ANCHORS = (
        "casual conversation, greetings, thanks, personal messages",
        "writing, translation, resume editing, emails, jokes, poetry, creative tasks",
        "general programming, Docker, GitHub, project deployment unrelated to database documentation",
        "math, travel, weather, personal advice, daily life questions",
        "general AI assistant question that does not require local database notes",
        "闲聊 翻译 写作 简历 编程 数学 天气 生活问题 不需要数据库资料",
    )

    def __init__(
        self,
        config: Settings = settings,
        embedder: object | None = None,
        llm_client: LocalLLMClient | None = None,
    ) -> None:
        self.config = config
        self.embedder = embedder
        self.llm_client = llm_client
        self._db_anchor_vectors: np.ndarray | None = None
        self._direct_anchor_vectors: np.ndarray | None = None

    def route(
        self,
        question: str,
        recent_history: Sequence[HistoryMessage],
        conversation_summary: str,
    ) -> IntentDecision:
        if not self.config.intent_router_enabled:
            return IntentDecision(True, "disabled", "Intent router disabled.")

        question = question.strip()
        keyword_decision = self._route_with_keywords(question, recent_history)
        if keyword_decision is not None:
            return keyword_decision

        embedding_decision = self._route_with_embeddings(
            question,
            recent_history,
            conversation_summary,
        )
        if embedding_decision is not None:
            return embedding_decision

        if self.config.intent_llm_fallback and self.llm_client is not None:
            llm_decision = self._route_with_llm(
                question,
                recent_history,
                conversation_summary,
            )
            if llm_decision is not None:
                return llm_decision

        return IntentDecision(
            False,
            "fallback_direct",
            "No confident database-document intent matched.",
        )

    def _route_with_keywords(
        self,
        question: str,
        recent_history: Sequence[HistoryMessage],
    ) -> IntentDecision | None:
        text = question.lower()

        if self._contains_any(text, self.FORCE_DIRECT_PHRASES):
            return IntentDecision(
                False,
                "keyword_direct",
                "User explicitly asked to avoid retrieval.",
            )

        if self._contains_any(text, self.FORCE_RAG_PHRASES):
            return IntentDecision(
                True,
                "keyword_rag",
                "User explicitly asked to use local documents.",
            )

        if self._contains_any(text, self.DIRECT_TASK_KEYWORDS):
            return IntentDecision(
                False,
                "keyword_direct",
                "Question is a writing or creative task.",
            )

        matched_db_keyword = self._first_match(text, self.DB_KEYWORDS)
        if matched_db_keyword:
            return IntentDecision(
                True,
                "keyword_rag",
                f"Matched database keyword: {matched_db_keyword}",
            )

        if any(re.search(pattern, text) for pattern in self.CASUAL_DIRECT_PATTERNS):
            return IntentDecision(
                False,
                "keyword_direct",
                "Question matched casual or off-topic wording.",
            )

        if self._looks_like_followup(text) and self._history_has_db_intent(
            recent_history,
        ):
            return IntentDecision(
                True,
                "keyword_followup_rag",
                "Short follow-up continues a database-related discussion.",
            )

        return None

    def _route_with_embeddings(
        self,
        question: str,
        recent_history: Sequence[HistoryMessage],
        conversation_summary: str,
    ) -> IntentDecision | None:
        if self.embedder is None:
            return None

        try:
            self._ensure_anchor_vectors()
            query_vector = self._embed_text(
                self._classification_text(
                    question,
                    recent_history,
                    conversation_summary,
                )
            )
        except Exception:
            return None

        if self._db_anchor_vectors is None or self._direct_anchor_vectors is None:
            return None

        db_score = float(np.max(self._db_anchor_vectors @ query_vector))
        direct_score = float(np.max(self._direct_anchor_vectors @ query_vector))
        margin = db_score - direct_score

        if (
            db_score >= self.config.intent_embedding_db_threshold
            and margin >= self.config.intent_embedding_margin
        ):
            return IntentDecision(
                True,
                "embedding_rag",
                (
                    "Embedding intent matched database topics "
                    f"(db={db_score:.3f}, direct={direct_score:.3f})."
                ),
            )

        if (
            direct_score >= self.config.intent_embedding_direct_threshold
            and -margin >= self.config.intent_embedding_margin
        ):
            return IntentDecision(
                False,
                "embedding_direct",
                (
                    "Embedding intent matched direct-chat topics "
                    f"(db={db_score:.3f}, direct={direct_score:.3f})."
                ),
            )

        return None

    def _route_with_llm(
        self,
        question: str,
        recent_history: Sequence[HistoryMessage],
        conversation_summary: str,
    ) -> IntentDecision | None:
        history_text = self._format_history(recent_history, max_chars=1800)
        summary_text = conversation_summary.strip()[-1200:] or "None"
        prompt = (
            "Local corpus scope: database systems and database selection. It "
            "covers embedded databases, OLTP, OLAP, distributed SQL, search, "
            "graph, time-series, vector databases, and related storage/retrieval "
            "concepts.\n\n"
            f"Compact memory:\n{summary_text}\n\n"
            f"Recent conversation:\n{history_text or 'None'}\n\n"
            f"Current question:\n{question}\n\n"
            "Decide whether answering should use this local database-document "
            "vector store. Return only JSON with keys use_rag and reason."
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an intent classifier. Return only compact JSON, "
                    "for example {\"use_rag\": true, \"reason\": \"...\"}."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        try:
            raw = self.llm_client.chat(
                messages,
                temperature=0.0,
                top_p=1.0,
                max_tokens=80,
            )
        except Exception:
            return None

        parsed = self._parse_llm_decision(raw)
        if parsed is None:
            return None

        use_rag, reason = parsed
        return IntentDecision(
            use_rag,
            "llm_rag" if use_rag else "llm_direct",
            reason or "LLM classifier decision.",
        )

    def _ensure_anchor_vectors(self) -> None:
        if self._db_anchor_vectors is not None and self._direct_anchor_vectors is not None:
            return
        self._db_anchor_vectors = self._embed_many(self.DB_ANCHORS)
        self._direct_anchor_vectors = self._embed_many(self.DIRECT_ANCHORS)

    def _embed_many(self, texts: Sequence[str]) -> np.ndarray:
        vectors = self.embedder.encode(texts, normalize_embeddings=True)
        return np.asarray(vectors, dtype=np.float32)

    def _embed_text(self, text: str) -> np.ndarray:
        vector = self.embedder.encode(text, normalize_embeddings=True)
        return np.asarray(vector, dtype=np.float32)

    def _classification_text(
        self,
        question: str,
        recent_history: Sequence[HistoryMessage],
        conversation_summary: str,
    ) -> str:
        recent_user_messages = [
            message.content.strip()
            for message in recent_history
            if message.role == "user" and message.content.strip()
        ][-2:]
        parts = [
            conversation_summary.strip()[-1000:],
            *recent_user_messages,
            question.strip(),
        ]
        return "\n".join(part for part in parts if part)[-2400:]

    def _format_history(
        self,
        history: Sequence[HistoryMessage],
        max_chars: int,
    ) -> str:
        text = "\n\n".join(
            f"{message.role.upper()}: {message.content.strip()}"
            for message in history
            if message.content.strip()
        )
        return text[-max_chars:]

    def _parse_llm_decision(self, raw: str) -> tuple[bool, str] | None:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        candidate = match.group(0) if match else raw.strip()

        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            lowered = raw.lower()
            if "true" in lowered and "false" not in lowered:
                return True, "LLM classifier returned true."
            if "false" in lowered and "true" not in lowered:
                return False, "LLM classifier returned false."
            return None

        if "use_rag" not in data:
            return None
        return bool(data["use_rag"]), str(data.get("reason", "")).strip()

    def _history_has_db_intent(
        self,
        recent_history: Sequence[HistoryMessage],
    ) -> bool:
        recent_text = " ".join(
            message.content.lower()
            for message in recent_history[-6:]
            if message.role == "user"
        )
        return bool(self._first_match(recent_text, self.DB_KEYWORDS))

    def _looks_like_followup(self, text: str) -> bool:
        if len(text) > 120:
            return False
        return self._contains_any(text, self.FOLLOWUP_MARKERS)

    def _first_match(self, text: str, patterns: Sequence[str]) -> str | None:
        for pattern in patterns:
            if pattern in text:
                return pattern
        return None

    def _contains_any(self, text: str, patterns: Sequence[str]) -> bool:
        return self._first_match(text, patterns) is not None
