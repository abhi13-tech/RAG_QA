from typing import List, Dict

class IndexBackend:
    def add(self, texts: List[str], metadatas: List[Dict]):
        raise NotImplementedError

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        raise NotImplementedError

