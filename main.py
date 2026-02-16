import os
from dotenv import load_dotenv
from src.orchestrator import Orchestrator
from src.utils import setup_logging

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize logging
    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
    
    # Create the GenAI Orchestrator
    orchestrator = Orchestrator()
    
    # Example task
    task = "Analyze the current trends in Generative AI for 2024."
    print(f"Executing task: {task}")
    
    # Note: In a real scenario, we would register agents and tools here.
    # result = orchestrator.execute(task)
    # print(f"Result: {result}")

if __name__ == "__main__":
    main()
