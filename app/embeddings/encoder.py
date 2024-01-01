from __future__ import annotations
from typing import List
import numpy as np
from functools import lru_cache

from app.core.config import settings

def _hash_embed(texts: List[str], dim: int = 512) -> np.ndarray:
    vecs = []
    for t in texts:
        h = np.zeros(dim, dtype=np.float32)
        for i, ch in enumerate(t.encode("utf-8")[:4096]):
            h[i % dim] += (ch % 13) / 255.0
        vecs.append(h)
    return np.vstack(vecs)

class Encoder:
    def __init__(self):
        self._mode = "hash"
        self._dim = 512
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            # Encode a tiny sample to discover dim without network
            test = self.model.encode(["test"], normalize_embeddings=False)
            self._dim = int(test.shape[1])
            self._mode = "st"
        except Exception:
            self.model = None

    @property
    def dim(self) -> int:
        return self._dim

    def encode(self, texts: List[str]) -> np.ndarray:
        if self._mode == "st" and self.model is not None:
            import numpy as np
            vecs = self.model.encode(texts, normalize_embeddings=False)
            return np.asarray(vecs, dtype=np.float32)
        return _hash_embed(texts, dim=self._dim)


@lru_cache(maxsize=1)
def get_encoder() -> Encoder:
    return Encoder()

