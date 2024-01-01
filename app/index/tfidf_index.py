from __future__ import annotations
from typing import List, Dict
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

_DIR = Path("index/tfidf")
_DIR.mkdir(parents=True, exist_ok=True)
_MODEL = _DIR / "tfidf.pkl"
_META = _DIR / "metas.npy"

class TfidfIndex:
    def __init__(self):
        self.vectorizer: TfidfVectorizer | None = None
        self.doc_mat = None
        self.metas: List[Dict] = []
        if _MODEL.exists() and _META.exists():
            self.vectorizer, self.doc_mat = joblib.load(_MODEL)
            self.metas = np.load(_META, allow_pickle=True).tolist()

    def add(self, texts: List[str], metadatas: List[Dict]):
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=50000)
        self.doc_mat = self.vectorizer.fit_transform(texts)
        self.metas = metadatas
        joblib.dump((self.vectorizer, self.doc_mat), _MODEL)
        np.save(_META, np.array(self.metas, dtype=object))

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.vectorizer is None or self.doc_mat is None:
            return []
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.doc_mat)[0]
        idxs = np.argsort(-sims)[:top_k]
        hits: List[Dict] = []
        for i in idxs:
            meta = dict(self.metas[int(i)])
            meta.update({"score": float(sims[int(i)])})
            hits.append(meta)
        return hits

