import logging
import sys
import os

# Add parent directory to path to find intelligence_router
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intelligence_router import router, TaskType

class DeepSeekBrain:
    def __init__(self):
        self.router = router
        logging.info("DeepSeekBrain initialized via IntelligenceRouter.")
    
    def reason(self, context, prompt):
        """
        Uses IntelligenceRouter (DeepSeek Priority) to reason through a trading problem.
        Args:
            context (str): Market data, news summary, etc.
            prompt (str): The specific question (e.g., "Is this a Bull Flag?")
        Returns:
            str: The reasoning output.
        """
        full_system_prompt = "You are a specialized Quant Trader AI. You analyze market data logically and conservatively. You protect capital above all else."
        full_user_prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{prompt}"
        
        # Use the Router to generate the response
        # TaskType.CODING is used for logic/reasoning tasks
        return self.router.generate(full_user_prompt, task_type=TaskType.CODING, system_prompt=full_system_prompt)

if __name__ == "__main__":
    # Test
    brain = DeepSeekBrain()
    print("Brain Initialized. Tests require API Keys in .env")
