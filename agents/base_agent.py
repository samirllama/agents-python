# agents/base_agent.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseAgent(ABC):
    def __init__(self):
        self.memory = []

    @abstractmethod
    async def generate_response(self, query: str, context: Optional[List[Dict]] = None) -> str:
        pass

    async def generate(self, prompt: str) -> str | None:
        # Implementation for LLM generation
        pass
