"""
Base Agent Interface for GenAI Orchestrator
Path: src/agents/base.py

This module defines the abstract base class for all agents within the orchestrator.
It provides the core interface for execution, tool integration, and state management,
ensuring unified behavior across specialized agent personas.
"""

import logging
import time
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import asdict, dataclass, field
from typing import Any, Deque, Dict, List, Optional, Protocol, runtime_checkable


logger = logging.getLogger(__name__)


@runtime_checkable
class ToolProtocol(Protocol):
    """Minimal contract every tool should satisfy."""

    name: str

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        ...


@dataclass
class ExecutionRecord:
    timestamp: float
    input_task: str
    output_summary: str
    latency_ms: float
    status: str


@dataclass
class AgentExecutionResult:
    status: str
    agent_name: str
    task: str
    result: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base class for all GenAI agents.

    Concrete agents should implement `_execute_impl()`.
    This base class provides:
    - config validation
    - tool registration
    - standardized execution lifecycle
    - audit-friendly execution history
    """

    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str = "",
        max_history: int = 50,
    ):
        self.name = self._validate_required_text("name", name)
        self.role = self._validate_required_text("role", role)
        self.goal = self._validate_required_text("goal", goal)
        self.backstory = backstory.strip()

        if max_history <= 0:
            raise ValueError("max_history must be greater than 0")

        self.tools: List[ToolProtocol] = []
        self.execution_history: Deque[ExecutionRecord] = deque(maxlen=max_history)

    @staticmethod
    def _validate_required_text(field_name: str, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value.strip()

    def add_tool(self, tool: ToolProtocol) -> None:
        """Register a tool with the agent."""
        if not isinstance(tool, ToolProtocol):
            raise TypeError(
                "tool must implement ToolProtocol with a 'name' attribute and async 'run' method"
            )

        self.tools.append(tool)
        logger.info("Agent '%s': registered tool '%s'.", self.name, tool.name)

    @abstractmethod
    async def _execute_impl(
        self, task: str, context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Concrete agent-specific execution logic."""
        raise NotImplementedError

    async def execute(
        self, task: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Standardized execution wrapper for all agents.
        Returns a structured result dictionary for easy downstream integration.
        """
        task = self._validate_required_text("task", task)
        context = context or {}

        start_time = time.perf_counter()

        try:
            logger.info("Agent '%s': starting task execution.", self.name)
            result = await self._execute_impl(task, context)
            latency_ms = (time.perf_counter() - start_time) * 1000

            response = AgentExecutionResult(
                status="success",
                agent_name=self.name,
                task=task,
                result=result,
                latency_ms=round(latency_ms, 2),
                metadata={"tool_count": len(self.tools)},
            )

            self._log_interaction(
                input_task=task,
                output_result=self._summarize_output(result),
                latency=latency_ms,
                status="success",
            )

            logger.info(
                "Agent '%s': completed task successfully in %.2f ms.",
                self.name,
                latency_ms,
            )
            return asdict(response)

        except Exception as exc:
            latency_ms = (time.perf_counter() - start_time) * 1000

            response = AgentExecutionResult(
                status="error",
                agent_name=self.name,
                task=task,
                error=str(exc),
                latency_ms=round(latency_ms, 2),
                metadata={"tool_count": len(self.tools)},
            )

            self._log_interaction(
                input_task=task,
                output_result=str(exc),
                latency=latency_ms,
                status="error",
            )

            logger.exception(
                "Agent '%s': task execution failed after %.2f ms.",
                self.name,
                latency_ms,
            )
            return asdict(response)

    def _log_interaction(
        self,
        input_task: str,
        output_result: str,
        latency: float,
        status: str,
    ) -> None:
        """Maintain bounded execution history for observability and audit."""
        self.execution_history.append(
            ExecutionRecord(
                timestamp=time.time(),
                input_task=input_task,
                output_summary=output_result[:500],
                latency_ms=round(latency, 2),
                status=status,
            )
        )

    @staticmethod
    def _summarize_output(output: Any) -> str:
        """Create a compact string summary for execution history."""
        if output is None:
            return "None"

        if isinstance(output, (dict, list)):
            return str(output)[:500]

        return str(output)[:500]

    def build_prompt_context(self) -> str:
        """Return a formatted persona block for prompt construction."""
        return (
            f"Role: {self.role}\n"
            f"Goal: {self.goal}\n"
            f"Backstory: {self.backstory}"
        )

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Return execution history as serializable dictionaries."""
        return [asdict(record) for record in self.execution_history]
