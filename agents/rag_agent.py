# agents/rag_agent.py
from typing import List, Dict, Optional
from .base_agent import BaseAgent
from openai import AsyncOpenAI
from tools.vector_store import VectorStore
from upstash_vector import Index
import os
from dotenv import load_dotenv

load_dotenv()

class RAGAgent(BaseAgent):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        super().__init__()
        self.model = model
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Initialize Upstash Vector client and pass it to VectorStore
        self.index = Index(
            url=os.getenv("UPSTASH_VECTOR_REST_URL") or "",
            token=os.getenv("UPSTASH_VECTOR_REST_TOKEN") or ""
        )
        self.vector_store = VectorStore(index=self.index)

    async def generate_response(self, query: str, context: Optional[List[Dict]] = None) -> str:
        # 1. Get embedding for the query
        embedding = await self._get_query_embedding(query)

        # 2. Retrieve relevant context using vector similarity
        relevant_docs = await self.vector_store.query_movies(
            vector=embedding,
            top_k=5,
            include_metadata=True
        )

        # 3. Augment the prompt with context
        augmented_prompt = self._create_augmented_prompt(query, relevant_docs)

        # 4. Generate response using LLM
        response = await self._generate_completion(augmented_prompt)

        return response


    async def _get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for the query text"""
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return response.data[0].embedding

    async def _generate_completion(self, prompt: str) -> str:
        """Generate completion using OpenAI"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about movies."},
                {"role": "user", "content": prompt}
            ]
        )
        # Handle potential None case
        content = response.choices[0].message.content
        if content is None:
            return "I apologize, but I couldn't generate a response."

        return content

    def _create_augmented_prompt(self, query: str, relevant_docs: List[Dict]) -> str:
        # Format context from relevant docs, including metadata
        context_parts = []
        for doc in relevant_docs:
            metadata = doc.get('metadata', {})
            context = (
                f"Title: {metadata.get('title')}\n"
                f"Director: {metadata.get('director')}\n"
                f"Year: {metadata.get('year')}\n"
                f"Genre: {metadata.get('genre')}\n"
                f"Description: {doc.get('data', '')}\n"
            )
            context_parts.append(context)

        full_context = "\n---\n".join(context_parts)

        return f"""Context information about movies:
{full_context}

Question: {query}

Please answer the question based on the provided movie information above."""
