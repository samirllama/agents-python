import asyncio
from agents.book_rag_agent import BookRAGAgent

async def main():
    agent = BookRAGAgent()

    # Example queries
    queries = [
        ("What does Marcus Aurelius say about personal integrity?", "integrity"),
        ("How does he define virtue?", "virtue"),
        ("What are the key principles of virtuous living?", "virtue")
    ]

    for query, concept in queries:
        print(f"\nQuery: {query}")
        response = await agent.query_philosophical_concept(query, concept)
        print(f"Response: {response}\n")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
