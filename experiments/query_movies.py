# experiments/query_movies.py
import asyncio
from tools.vector_store import VectorStore

async def main():
    vector_store = VectorStore()

    results = await vector_store.query_movies(
        query="Show me action movies with high ratings",
        filters={
            "genre": "Action",
            "rating": "8.0"
        },
        top_k=5
    )

    for result in results:
        print(f"\nTitle: {result['metadata']['title']}")
        print(f"Score: {result['score']}")
        print(f"Metadata: {result['metadata']}")

if __name__ == "__main__":
    asyncio.run(main())
