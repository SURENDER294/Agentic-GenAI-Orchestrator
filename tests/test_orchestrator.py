import unittest
from src.orchestrator import Orchestrator

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()

    def test_orchestrator_initialization(self):
        self.assertIsNotNone(self.orchestrator)
        self.assertEqual(len(self.orchestrator.agents), 0)
        self.assertEqual(len(self.orchestrator.tools), 0)

    def test_agent_registration(self):
        # Mock agent for testing
        class MockAgent:
            def __init__(self):
                self.name = "TestAgent"
        
        agent = MockAgent()
        self.orchestrator.register_agent(agent)
        self.assertIn("TestAgent", self.orchestrator.agents)

if __name__ == "__main__":
    unittest.main()
