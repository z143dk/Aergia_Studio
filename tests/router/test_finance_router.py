import sys
import os

# Ensure Aergia_Studio is in path
sys.path.append(os.getcwd())

from intelligence_router import router
from router.schemas import TaskRequest

def test_finance():
    print("--- Testing Financial Router ---")
    
    # Test 1: Crypto (Coinbase)
    print("\n1. Testing Crypto Routing (Should go to Coinbase)...")
    req_crypto = TaskRequest(
        prompt="What is the price of BTC?",
        task_type="financial_analysis"
    )
    res_crypto = router.orchestrate(req_crypto)
    print(f"Provider Executed: {res_crypto.provider_id}")
    print(f"Content: {res_crypto.content}")
    print(f"Routing Reasons: {res_crypto.routing.reasons}")

    # Test 2: Stocks (Schwab)
    print("\n2. Testing Stock Routing (Should go to Schwab)...")
    req_stock = TaskRequest(
        prompt="Get me the price of AAPL",
        task_type="financial_analysis"
    )
    res_stock = router.orchestrate(req_stock)
    print(f"Provider Executed: {res_stock.provider_id}")
    print(f"Content: {res_stock.content}")
    print(f"Routing Reasons: {res_stock.routing.reasons}")

if __name__ == "__main__":
    test_finance()
