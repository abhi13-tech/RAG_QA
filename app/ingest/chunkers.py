from typing import List

def simple_chunk(text: str, max_len: int = 800) -> List[str]:
    chunks = []
    t = text.replace("\r", "\n")
    for i in range(0, len(t), max_len):
        chunks.append(t[i:i+max_len])
    return [c for c in chunks if c.strip()]

