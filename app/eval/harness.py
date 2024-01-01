from pathlib import Path
import json
from typing import List, Dict, Tuple
import re

from app.index.build import get_dense_index, get_bm25_index
from app.index.hybrid_index import HybridIndex
from app.retrieval.reranker import rerank_hits
from app.llm.generator import answer_question

SETS_DIR = Path("eval/sets")

def _load_set(path: Path) -> List[Dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def _normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def _em(pred: str, gold: str) -> float:
    return 1.0 if _normalize(pred) == _normalize(gold) else 0.0

def _f1(pred: str, gold: str) -> float:
    p_tokens = _normalize(pred).split()
    g_tokens = _normalize(gold).split()
    if not p_tokens and not g_tokens:
        return 1.0
    if not p_tokens or not g_tokens:
        return 0.0
    common = 0
    g_counts = {}
    for t in g_tokens:
        g_counts[t] = g_counts.get(t, 0) + 1
    for t in p_tokens:
        if g_counts.get(t, 0) > 0:
            common += 1
            g_counts[t] -= 1
    if common == 0:
        return 0.0
    precision = common / len(p_tokens)
    recall = common / len(g_tokens)
    return 2 * precision * recall / (precision + recall)

def _faithfulness(pred: str, contexts: List[Dict]) -> float:
    # Fraction of answer tokens grounded in contexts
    ctxt = " ".join([c.get("text", "") for c in contexts])
    c_tokens = set(_normalize(ctxt).split())
    a_tokens = _normalize(pred).split()
    if not a_tokens:
        return 0.0
    grounded = sum(1 for t in a_tokens if t in c_tokens)
    return grounded / len(a_tokens)

def _evaluate_variant(name: str, hits_fn, data: List[Dict], top_k: int) -> Dict:
    ems: List[float] = []
    f1s: List[float] = []
    faiths: List[float] = []
    recalls: List[float] = []
    for ex in data:
        hits = hits_fn(ex["question"], top_k)
        txt = "\n".join([h.get("text", "") for h in hits])
        recall = 1.0 if ex.get("must_contain", "") and ex["must_contain"] in txt else 0.0
        recalls.append(recall)
        pred = answer_question(ex["question"], hits)
        ems.append(_em(pred, ex.get("answer", "")))
        f1s.append(_f1(pred, ex.get("answer", "")))
        faiths.append(_faithfulness(pred, hits))
    def avg(xs):
        return round(sum(xs) / len(xs), 3) if xs else 0.0
    return {
        "variant": name,
        "n": len(data),
        "em": avg(ems),
        "f1": avg(f1s),
        "faithfulness": avg(faiths),
        "retrieval_recall": avg(recalls),
    }

def run_eval(top_k: int = 5) -> Dict:
    path = SETS_DIR / "sample.jsonl"
    data = _load_set(path)
    dense = get_dense_index()
    bm25 = get_bm25_index()
    hybrid = HybridIndex(dense, bm25)

    variants = [
        ("dense", lambda q, k: dense.search(q, top_k=k)),
        ("dense+rerank", lambda q, k: rerank_hits(q, dense.search(q, top_k=k), enabled=True)),
        ("hybrid", lambda q, k: hybrid.search(q, top_k=k)),
        ("hybrid+rerank", lambda q, k: rerank_hits(q, hybrid.search(q, top_k=k), enabled=True)),
    ]
    results = {v[0]: _evaluate_variant(v[0], v[1], data, top_k) for v in variants}
    return results

if __name__ == "__main__":
    print(run_eval())
