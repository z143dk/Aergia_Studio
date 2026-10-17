import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from intelligence_router import router, TaskType

class Researcher:
    def __init__(self):
        self.role = "Quantitative Researcher"

    def debate_trade(self, ticker, proposed_action):
        """
        Uses DeepSeek R1 (REASONING) to play Devil's Advocate.
        """
        system_prompt = (
            "You are a Skeptical Quantitative Researcher. "
            "Your job is to find the flaws in a proposed trade. "
            "Debate the Bull Case vs Bear Case appropriately. "
            "Conclude with a 'CONVICTION SCORE' (0-10)."
        )
        
        prompt = f"Proposed Trade: {proposed_action} on {ticker}. Why might this fail? What are the macro risks?"
        
        response = router.generate(prompt, task_type=TaskType.REASONING, system_prompt=system_prompt)
        return response

if __name__ == "__main__":
    researcher = Researcher()
    print(researcher.debate_trade("F", "Buy Call Options targeting $12"))
