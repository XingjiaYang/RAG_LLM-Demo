from dataclasses import dataclass
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    return float(value)


@dataclass(frozen=True)
class Settings:
    docs_dir: Path = PROJECT_ROOT / "data" / "docs"
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection_name: str = os.getenv("QDRANT_COLLECTION", "tech_docs")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    chunk_size: int = _env_int("CHUNK_SIZE", 800)
    chunk_overlap: int = _env_int("CHUNK_OVERLAP", 120)
    retrieve_top_k: int = _env_int("RETRIEVE_TOP_K", 4)

    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:8000/v1")
    llm_api_key: str = os.getenv("LLM_API_KEY", "token")
    llm_model: str = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    llm_temperature: float = _env_float("LLM_TEMPERATURE", 0.2)
    llm_top_p: float = _env_float("LLM_TOP_P", 0.9)
    llm_max_tokens: int = _env_int("LLM_MAX_TOKENS", 2048)
    llm_timeout_seconds: float = _env_float("LLM_TIMEOUT_SECONDS", 300.0)

    history_recent_turns: int = _env_int("HISTORY_RECENT_TURNS", 6)
    history_max_messages: int = _env_int("HISTORY_MAX_MESSAGES", 80)
    conversation_summary_max_chars: int = _env_int(
        "CONVERSATION_SUMMARY_MAX_CHARS",
        2200,
    )


settings = Settings()
