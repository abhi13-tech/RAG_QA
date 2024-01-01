from pathlib import Path
from typing import List, Tuple
import re

def load_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text

def load_generic(path: Path) -> str:
    if path.suffix.lower() in {".txt", ".md"}:
        return load_text(path)
    # naive binary-to-text fallback for PDFs/HTML
    try:
        return path.read_bytes().decode("utf-8", errors="ignore")
    except Exception:
        return ""

def discover(paths: List[str] | None) -> List[Path]:
    if paths:
        items = [Path(p) for p in paths]
    else:
        items = list(Path("data/raw").glob("**/*"))
    return [p for p in items if p.is_file()]

