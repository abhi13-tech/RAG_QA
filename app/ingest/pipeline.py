from pathlib import Path
import json
from typing import List
from app.ingest.loaders import discover, load_generic
from app.ingest.chunkers import simple_chunk

_OUT_DIR = Path("data/processed")

def run_ingest(paths: List[str] | None = None) -> int:
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = discover(paths)
    out_file = _OUT_DIR / "chunks.jsonl"
    n = 0
    with out_file.open("w", encoding="utf-8") as f:
        for p in files:
            text = load_generic(p)
            for ch in simple_chunk(text):
                rec = {"text": ch, "source": str(p)}
                f.write(json.dumps(rec) + "\n")
                n += 1
    return n

if __name__ == "__main__":
    print({"processed": run_ingest()})

