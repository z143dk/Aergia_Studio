import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Current Working Directory: {os.getcwd()}")

# Fix Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    print(f"Added to sys.path: {parent_dir}")

print("\n--- TESTING IMPORTS ---")

try:
    print("1. Importing midas_quant...", end=" ")
    import midas_quant
    print("✅ OK")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print("2. Importing router.registry...", end=" ")
    from router.registry import ProviderRegistry
    print("✅ OK")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print("3. Importing midas_strategist...", end=" ")
    from midas_strategist import MidasStrategist
    print("✅ OK")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print("4. Importing router.hive_mind...", end=" ")
    from router.hive_mind import HiveMind
    print("✅ OK")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print("5. Importing schwab_api...", end=" ")
    from schwab_api.client import SchwabClient
    print("✅ OK")
except Exception as e:
    print(f"❌ FAILED: {e}")

try:
    print("6. Importing mplfinance...", end=" ")
    import mplfinance as mpf
    print("✅ OK")
except Exception as e:
    print(f"❌ FAILED: {e}")
