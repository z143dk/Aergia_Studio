import json
import os
import sys
from datetime import datetime

# Path Hacking
# Path Hacking
current_dir = os.path.dirname(os.path.abspath(__file__))
midas_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(midas_dir)
sys.path.append(project_root)
sys.path.append(midas_dir)

from intelligence_router import router, TaskType

class TradingCoach:
    def __init__(self):
        # Dynamically find 'Project Midas' folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.history_path = os.path.join(base_dir, "trade_history.json")
        self.lessons_path = os.path.join(base_dir, "lessons_learned.md")

    def run_analysis(self):
        print("--- Trading Coach: Starting Post-Trade Analysis ---")
        
        # 1. Load History
        try:
            with open(self.history_path, 'r') as f:
                history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return

        # 2. Find Analyzable Trades
        # Using "PENDING" to mean "Executed but not yet critiqued"
        pending_trades = [t for t in history if t.get('outcome') == 'PENDING']
        
        if not pending_trades:
            print("No pending trades to analyze.")
            return

        print(f"Found {len(pending_trades)} trades to critique.")

        for trade in pending_trades:
            self.analyze_trade(trade)
            
            # Update status to avoid re-analysis
            trade['outcome'] = "ANALYZED"
        
        # 3. Save History Analysis Status
        with open(self.history_path, 'w') as f:
            json.dump(history, f, indent=4)
            
    def analyze_trade(self, trade):
        print(f"Analyzing Trade: {trade['id']}...")
        
        # 4. Construct Prompt
        prompt = f"""
        Analyze this recent trade decision.
        Ticker: {trade['ticker']}
        Analyst Logic: {trade.get('analyst_signal')}
        Risk Status: {trade.get('risk_evaluation')}
        Researcher Logic: {trade.get('researcher_debate')}
        
        TASK:
        You are the Head of Trading Strategy (The Coach).
        Critique this decision relative to our "100% Growth / Aggressive Swing" goal.
        Did we enter with enough conviction? Was the Risk Logic sound?
        
        OUTPUT:
        Provide a concise "Lesson Learned" (max 3 sentences) in markdown format.
        Focus on improvement.
        """
        
        # 5. Call DeepSeek R1 (Reasoning)
        lesson = router.generate(prompt, task_type=TaskType.REASONING)
        
        print("Coach's Feedback:")
        print(lesson)
        
        # 6. Append to Lessons
        self.save_lesson(trade, lesson)

    def save_lesson(self, trade, lesson):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        entry = f"\n## Trade {trade['ticker']} ({timestamp})\n**Lesson**: {lesson}\n---\n"
        
        with open(self.lessons_path, 'a') as f:
            f.write(entry)
        print("Lesson saved to 'lessons_learned.md'.")

if __name__ == "__main__":
    coach = TradingCoach()
    coach.run_analysis()
