from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings
from app.vector_store import chunk_text


def main() -> None:
    total_chunks = 0

    for path in sorted(settings.docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(
            text,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )

        if not chunks:
            raise AssertionError(f"No chunks produced for {path}")

        if text.lstrip().startswith("#"):
            bad_starts = [
                chunk[:80]
                for chunk in chunks
                if not chunk.lstrip().startswith("#")
            ]
            if bad_starts:
                raise AssertionError(
                    f"Markdown heading context missing in {path}: {bad_starts}"
                )

        oversized = [
            len(chunk)
            for chunk in chunks
            if len(chunk) > settings.chunk_size
        ]
        if oversized:
            raise AssertionError(f"Oversized chunks in {path}: {oversized}")

        total_chunks += len(chunks)
        print(f"{path.name}: {len(chunks)} chunks")

    print(f"Total chunks: {total_chunks}")


if __name__ == "__main__":
    main()
