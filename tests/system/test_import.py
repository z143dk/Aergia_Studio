import sys
import os

print("Testing imports...")
try:
    from intelligence_router import router
    print("✅ intelligence_router imported successfully.")
except Exception as e:
    print(f"❌ intelligence_router failed: {e}")
    sys.exit(1)

try:
    from aergia_api import app
    print("✅ aergia_api imported successfully.")
except Exception as e:
    print(f"❌ aergia_api failed: {e}")
    sys.exit(1)

print("All systems go.")
