# tools/vector_store.py
from typing import List, Dict
from upstash_vector import Index
from utils.db import MetadataDB

class VectorStore:
    def __init__(self, index: Index):
        self.index = index
        self.db = MetadataDB()

    async def query_movies(
        self,
        vector: List[float],
        top_k: int = 5,
        include_metadata: bool = True
    ) -> List[Dict]:
        # Query vector store
        results = await self.index.query(
            vector=vector,
            top_k=top_k,
            include_vectors=False
        )

        if include_metadata:
            # Enhance results with metadata from SQLite
            for result in results:
                metadata = self.db.get_metadata(result['id'])
                if metadata:
                    result['metadata'] = metadata

        return results

    def close(self):
        self.db.close()
