from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm
import numpy as np
from app.core.config import settings
from app.embeddings.encoder import get_encoder

class QdrantIndex:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection = settings.COLLECTION
        enc = get_encoder()
        # Create collection if missing (non-destructive)
        try:
            self.client.get_collection(self.collection)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=qm.VectorParams(size=enc.dim, distance=qm.Distance.COSINE),
            )

    def add(self, texts: List[str], metadatas: List[Dict]):
        enc = get_encoder()
        vecs = enc.encode(texts)
        self.client.upsert(
            collection_name=self.collection,
            points=[
                qm.PointStruct(id=i, vector=vecs[i].tolist(), payload=metadatas[i])
                for i in range(len(texts))
            ],
        )

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        enc = get_encoder()
        qv = enc.encode([query])[0].tolist()
        res = self.client.search(
            collection_name=self.collection,
            query_vector=qv,
            limit=top_k,
            with_payload=True,
        )
        hits = []
        for r in res:
            meta = dict(r.payload)
            meta.update({"score": float(r.score)})
            hits.append(meta)
        return hits
