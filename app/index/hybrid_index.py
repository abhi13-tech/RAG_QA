from __future__ import annotations
from typing import List, Dict

def _key(h: Dict) -> str:
    return f"{h.get('source','')}|{h.get('text','')[:100]}"

class HybridIndex:
    def __init__(self, dense, bm25):
        self.dense = dense
        self.bm25 = bm25

    def add(self, texts: List[str], metadatas: List[Dict]):
        # Underlying indices manage persistence
        self.dense.add(texts, metadatas)
        self.bm25.add(texts, metadatas)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        d_hits = self.dense.search(query, top_k=top_k)
        b_hits = self.bm25.search(query, top_k=top_k)
        # Reciprocal Rank Fusion
        scores = {}
        for rank, h in enumerate(d_hits):
            k = _key(h)
            scores.setdefault(k, [h, 0.0])
            scores[k][1] += 1.0 / (60 + rank + 1)
        for rank, h in enumerate(b_hits):
            k = _key(h)
            scores.setdefault(k, [h, 0.0])
            scores[k][1] += 1.0 / (60 + rank + 1)
        merged = []
        for k, (h, s) in scores.items():
            hh = dict(h)
            hh["rrf_score"] = s
            merged.append(hh)
        merged.sort(key=lambda x: x.get("rrf_score", 0.0), reverse=True)
        return merged[:top_k]

