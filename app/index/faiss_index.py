import os
from typing import List, Dict
import numpy as np
import faiss
from pathlib import Path

from app.index.base import IndexBackend
from app.embeddings.encoder import get_encoder

_INDEX_DIR = Path("index/faiss")
_INDEX_FILE = _INDEX_DIR / "vectors.index"
_META_FILE = _INDEX_DIR / "metas.npy"

class FaissIndex(IndexBackend):
    def __init__(self):
        _INDEX_DIR.mkdir(parents=True, exist_ok=True)
        self.index = None
        self.metas: List[Dict] = []
        if _INDEX_FILE.exists() and _META_FILE.exists():
            self.index = faiss.read_index(str(_INDEX_FILE))
            self.metas = np.load(_META_FILE, allow_pickle=True).tolist()

    def add(self, texts: List[str], metadatas: List[Dict]):
        enc = get_encoder()
        vecs = enc.encode(texts).astype("float32")
        if self.index is None:
            self.index = faiss.IndexFlatIP(vecs.shape[1])
        faiss.normalize_L2(vecs)
        self.index.add(vecs)
        self.metas.extend(metadatas)
        faiss.write_index(self.index, str(_INDEX_FILE))
        np.save(_META_FILE, np.array(self.metas, dtype=object))

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index is None:
            return []
        enc = get_encoder()
        qv = enc.encode([query]).astype("float32")
        faiss.normalize_L2(qv)
        D, I = self.index.search(qv, top_k)
        hits = []
        for d, i in zip(D[0], I[0]):
            if i == -1 or i >= len(self.metas):
                continue
            meta = dict(self.metas[i])
            meta.update({"score": float(d)})
            hits.append(meta)
        return hits
