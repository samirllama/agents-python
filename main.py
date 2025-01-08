import asyncio
from agents.rag_agent import RAGAgent

async def main():
    # Initialize the RAG agent
    agent = RAGAgent()

    # Example query
    query = "What are some highly rated action movies?"

    # Get response
    response = await agent.generate_response(query)
    print(f"Query: {query}")
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
