"""
Base Agent Interface for GenAI Orchestrator
Path: src/agents/base.py

This module defines the abstract base class for all agents within the orchestrator.
It provides the core interface for execution, tool integration, and state management,
ensuring a unified behavior across different agentic specialized personas.

Author: AI Engineer (FAANG Grade)
Language: Python 3.8+
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract Base Class representing a GenAI Agent.
    All specialized agents (Researcher, Coder, Reviewer) must inherit from this.
    """

    def __init__(self, name: str, role: str, goal: str, backstory: str = ""):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools: List[Any] = []
        self.execution_history: List[Dict[str, Any]] = []

    def add_tool(self, tool: Any) -> None:
        """Registers a functional tool with the agent."""
        self.tools.append(tool)
        logger.info(f"Agent {self.name}: Tool {type(tool).__name__} registered.")

    @abstractmethod
    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main execution logic for the agent.
        Must be implemented by concrete subclasses.
        """
        pass

    def _log_interaction(self, input_task: str, output_result: str, latency: float):
        """Internal helper to maintain execution history for audit and memory."""
        self.execution_history.append({
            "timestamp": time.time(),
            "input": input_task,
            "output": output_result,
            "latency_ms": latency * 1000
        })

    def get_agent_profile(self) -> str:
        """Returns a formatted string representing the agent's persona for prompt injection."""
        profile = (
            f"Role: {self.role}
"
            f"Goal: {self.goal}
"
            f"Backstory: {self.backstory}"
        )
        return profile
