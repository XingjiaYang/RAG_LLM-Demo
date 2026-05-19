from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings
from app.vector_store import VectorStore


def main() -> None:
    query = "What is DuckDB good for?"
    store = VectorStore(settings)
    results = store.search(query, top_k=3)

    print(f"Query: {query}")
    print(f"Collection: {settings.collection_name}")
    print()

    if not results:
        print("No results found.")
        return

    for idx, result in enumerate(results, start=1):
        preview = result.text.replace("\n", " ")[:240]
        print(
            f"[{idx}] score={result.score:.4f} "
            f"source={result.source} chunk={result.chunk_id}"
        )
        print(preview)
        print()


if __name__ == "__main__":
    main()
