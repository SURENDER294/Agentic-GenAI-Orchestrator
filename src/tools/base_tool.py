import abc
from typing import Any, Dict, Optional

class BaseTool(abc.ABC):
    \"\"\"
    Abstract base class for all tools in the Agentic-GenAI-Orchestrator.
    Tools allow agents to interact with the external world (e.g., web search, file ops).
    \"\"\"

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abc.abstractmethod
    def run(self, **kwargs: Any) -> Any:
        \"\"\"Execute the tool's core logic.\"\"\"
        pass

    def to_dict(self) -> Dict[str, str]:
        \"\"\"Return a dictionary representation for LLM tool-calling compatibility.\"\"\"
        return {
            \"name\": self.name,
            \"description\": self.description
        }
