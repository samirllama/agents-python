from typing import List, Dict, Optional
from .base_agent import BaseAgent
from tools.book_vectorizer import BookVectorizer
from tools.vector_store import VectorStore
from openai import AsyncOpenAI
from upstash_vector import Index
import os
from dotenv import load_dotenv

load_dotenv()

class BookRAGAgent(BaseAgent):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        super().__init__()
        self.model = model
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorizer = BookVectorizer()
        # Initialize Upstash Vector client and pass it to VectorStore
        self.index = Index(
            url=os.getenv("UPSTASH_VECTOR_REST_URL") or "",
            token=os.getenv("UPSTASH_VECTOR_REST_TOKEN") or ""
        )
        self.vector_store = VectorStore(index=self.index)

    async def generate_response(
        self,
        query: str,
        context: Optional[List[Dict]] = None
    ) -> str:
        """Implement the abstract method from BaseAgent"""
        # If context is provided, use it; otherwise, fetch context through vector search
        if context is None:
            # Default to treating the query as a virtue-related query
            return await self.query_philosophical_concept(query, concept="virtue")
        else:
            # Use provided context to generate response
            prompt = self._create_philosophical_prompt(
                query=query,
                contexts=context,
                concept="general"  # or detect concept from query
            )
            return await self.generate_completion(prompt)

    async def get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for the query text"""
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return response.data[0].embedding

    async def generate_completion(self, prompt: str) -> str:
        """Generate completion using OpenAI"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a philosophical assistant specializing in ancient wisdom and practical philosophy."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        if content is None:
            return "I apologize, but I couldn't generate a response."
        return content

    async def query_philosophical_concept(
        self,
        query: str,
        concept: str,
        top_k: int = 3
    ) -> str:
        # Get embedding for the query
        embedding = await self.get_query_embedding(
            f"Find text about {concept}: {query}"
        )

        # Get relevant passages using existing query_movies method
        # Note: We're using query_movies as it's our existing vector query method
        results = await self.vector_store.query_movies(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Create prompt with context
        prompt = self._create_philosophical_prompt(query, results, concept)

        # Generate response
        return await self.generate_completion(prompt)

    def _create_philosophical_prompt(
        self,
        query: str,
        contexts: List[Dict],
        concept: str
    ) -> str:
        # Extract text from results
        context_text = "\n\n".join([
            f"Passage: {ctx.get('metadata', {}).get('text', '')}"
            for ctx in contexts if ctx.get('metadata')
        ])

        return f"""
        Using the following passages from Marcus Aurelius' Meditations,
        answer the question about {concept}.

        {context_text}

        Question: {query}

        Please provide a thoughtful answer that:
        1. Directly references the relevant passages
        2. Explains the philosophical concept
        3. Relates it to practical application

        Answer:
        """
