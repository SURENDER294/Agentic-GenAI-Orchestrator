import logging
from typing import Any, Dict, List, Optional
from src.agents.base_agent import BaseAgent
from src.memory.base_memory import BaseMemory
from src.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class Orchestrator:
    \"\"\"
    The central intelligence of the Agentic-GenAI-Orchestrator.
    Manages agent lifecycles, task delegation, and cross-agent communication.
    \"\"\"

    def __init__(self, memory: Optional[BaseMemory] = None):
        self.memory = memory
        self.agents: Dict[str, BaseAgent] = {}
        self.tools: Dict[str, BaseTool] = {}
        logger.info(\"Orchestrator initialized.\")

    def register_agent(self, agent: BaseAgent) -> None:
        \"\"\"Register a new agent in the workflow.\"\"\"
        self.agents[agent.name] = agent
        logger.debug(f\"Agent '{agent.name}' registered.\")

    def register_tool(self, tool: BaseTool) -> None:
        \"\"\"Register a tool available for agents to use.\"\"\"
        self.tools[tool.name] = tool
        logger.debug(f\"Tool '{tool.name}' registered.\")

    def run_task(self, task_description: str, target_agent_name: str) -> str:
        \"\"\"
        Assign a task to a specific agent and track the execution.
        \"\"\"
        if target_agent_name not in self.agents:
            return f\"Error: Agent '{target_agent_name}' not found.\"

        agent = self.agents[target_agent_name]
        logger.info(f\"Delegating task to {target_agent_name}: {task_description[:50]}...\")
        
        # In a real system, the orchestrator might preprocess the task
        # or provide context from memory.
        result = agent.execute(task_description)
        
        if self.memory:
            self.memory.add(
                content=f\"Task: {task_description} | Result: {result}\",
                metadata={\"agent\": target_agent_name}
            )
            
        return result

    def broadcast(self, message: str) -> None:
        \"\"\"Broadcast a message to all registered agents (e.g., status updates).\"\"\"
        for agent in self.agents.values():
            logger.debug(f\"Broadcasting to {agent.name}\")
            # Placeholder for actual broadcast logic
