import os
from intelligence_router import router, TaskType

class MidasAdvisor:
    def __init__(self):
        self.name = "Midas Intelligence Engine"

    def generate_morning_briefing(self, portfolio_data, market_news):
        """
        Uses DeepSeek R1 (Reasoning) to analyze your specific 
        financial situation and give a strategic briefing.
        """
        prompt = f"""
        Analyze the following portfolio and market data for Project Midas.
        
        PORTFOLIO DATA:
        {portfolio_data}
        
        MARKET NEWS:
        {market_news}
        
        Provide a concise, high-level strategic briefing. 
        Focus on: 
        1. Risk levels (Medicaid safety limits).
        2. Top 3 actionable swing trade opportunities.
        3. A 'Coach's Note' on emotional discipline for today's volatility.
        """
        
        # Route to REASONING lane (DeepSeek R1)
        briefing = router.generate(
            prompt=prompt,
            task_type=TaskType.REASONING,
            system_prompt="You are the Midas Trading Coach, a world-class financial strategist."
        )
        return briefing

# Example usage for testing
if __name__ == "__main__":
    advisor = MidasAdvisor()
    # Mock data for test
    print("--- Midas Intelligence Test ---")
    print(advisor.generate_morning_briefing("Balance: $50k, Positions: TSLA, NVDA", "Market is bullish on AI.")) 
