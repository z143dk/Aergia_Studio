import time
import sys
import os

# Imports (Relative to protect against path shifts)
from .technical_analyst import TechnicalAnalyst
from .risk_manager import RiskManager
from .researcher import Researcher
from .news_analyst import NewsAnalyst
from .execution_agent import ExecutionAgent
from .trade_logger import TradeLogger
from .data_ingestion import DataIngestionAgent
from .ml_analyst import MLAnalyst

# Midas Strategies (Assumes 'strategies' package is in sys.path or root)
# Since midas_home runs from Project Midas, 'strategies' is at root level relative to execution
from strategies.momentum_breakout import MomentumBreakout

class StrategyCoordinator:
    def __init__(self):
        self.analyst = TechnicalAnalyst()
        self.risk = RiskManager()
        self.researcher = Researcher()
        self.news = NewsAnalyst()
        self.executor = ExecutionAgent()
        self.logger = TradeLogger()
        
        # Phase 3 & 4 Components
        self.data_feed = DataIngestionAgent()
        self.strategy = MomentumBreakout()
        self.ml = MLAnalyst()
        
    def run_daily_cycle(self):
        print("--- Strategy Coordinator: Market Cycle Start ---")
        
        # 1. Analyst Scan
        tickers = ["F", "PLTR", "TSLA", "BTC", "ETH"] # Added Crypto Support
        for ticker in tickers:
            print(f"\n--- Processing {ticker} ---")
            
            # Phase 3: Data Ingestion
            snapshot = self.data_feed.get_market_snapshot(ticker)
            
            # Phase 4: ML Oracle (Probabilistic Logic)
            ml_prediction = self.ml.generate_probability(snapshot)
            print(f"ML Oracle: {ml_prediction['direction']} ({ml_prediction['probability']}%)")
            
            # Phase 3: Strategy Logic (The "Sniper")
            strat_decision = self.strategy.evaluate(snapshot)
            print(f"Strategy Output: {strat_decision}")
            
            if strat_decision['action'] == "WAIT":
                print(f"Strategy Wait: {strat_decision['reason']}")
                # Log the 'Miss' for coaching too? Maybe later.
                continue
            
            print(f">>> MOMENTUM SIGNAL DECTECTED: {strat_decision['action']} <<<")
            
            # 1.5 Analyst "Gut Check" (AI Verification)
            # We pass the same data to the Analyst for a second opinion
            # For now, keeping the original analyze_ticker flow which refetches data
            # Optimization: Pass snapshot to analyst later
            analysis = self.analyst.analyze_ticker(ticker)
            print(f"AI Analyst Opinion: {analysis}")
            
            # 1.75 News Check
            print("Checking Sentiment...")
            sentiment = self.news.analyze_sentiment(ticker)
            print(f"News Analyst: {sentiment}")
            
            if "NEGATIVE" in sentiment:
                print("TRADE ABORTED: Negative News Sentiment.")
                continue

            # 2. Risk Check
            # Use Strategy Target or Default
            contract_price = 0.50 # Placeholder for Option Premium
            approved, risk_msg = self.risk.evaluate_trade(ticker, 10.00, contract_price)
            print(f"Risk Manager: {risk_msg}")
            
            if approved:
                # 3. Researcher Debate
                print("Requesting Deep Reasoner opinion...")
                debate = self.researcher.debate_trade(ticker, "BUY CALL")
                print(f"Researcher Logic:\n{debate}")
                
                # 4. Execution (LIVE)
                print(">>> SENDING ORDER TO EXECUTION AGENT <<<")
                
                # Determine Parameters
                quantity = 1
                price = snapshot.get('price', 0)
                option_sym = None
                
                # Basic Crypto Sizing
                if ticker in ["BTC", "ETH", "SOL", "DOGE"]:
                    quantity = 0.00001 if ticker == "BTC" else 0.001
                    action = "BUY" # Auto-Pilot strictly Buys for momentum for now
                    
                # Basic Stock Sizing
                else:
                    action = "BUY"
                    # We need an option picker here. For now, skipping real stock exec
                    print("Auto-Pilot: Stock execution requires Option Selection (Not implemented in Cycle yet).")
                    continue

                # Execute
                order_status = self.executor.execute_order(
                    ticker=ticker,
                    action=action,
                    quantity=quantity,
                    price=price,
                    option_symbol=option_sym
                )
                print(f"Order Result: {order_status}")
                
                self.logger.log_trade_attempt(
                    ticker=ticker,
                    signal_data=analysis,
                    risk_data=risk_msg,
                    researcher_data=debate,
                    execution_status=order_status
                )
            
            else:
                self.logger.log_trade_attempt(
                    ticker=ticker,
                    signal_data=analysis,
                    risk_data=risk_msg,
                    researcher_data="N/A",
                    execution_status="BLOCKED_BY_RISK"
                )

if __name__ == "__main__":
    coord = StrategyCoordinator()
    coord.run_daily_cycle()
