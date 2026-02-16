import abc
from typing import Any, Dict, List, Optional
from datetime import datetime

class BaseMemory(abc.ABC):
    \"\"\"
    Abstract base class for all memory implementations in the Agentic-GenAI-Orchestrator.
    Provides a standardized interface for long-term and short-term agent memory.
    \"\"\"

    @abc.abstractmethod
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        \"\"\"Add a new memory entry.\"\"\"
        pass

    @abc.abstractmethod
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        \"\"\"Search for relevant memories based on a query.\"\"\"
        pass

    @abc.abstractmethod
    def clear(self) -> None:
        \"\"\"Clear all stored memories.\"\"\"
        pass

    @abc.abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        \"\"\"Retrieve all stored memories.\"\"\"
        pass

    def _format_timestamp(self) -> str:
        \"\"\"Utility to generate ISO format timestamps for memory entries.\"\"\"
        return datetime.utcnow().isoformat()
