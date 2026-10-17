import sys
import traceback
import os

print("--- DEBUGGING DASHBOARD STARTUP ---")

try:
    print("1. Importing Flask...")
    from flask import Flask
    print("   Success.")

    print("2. Importing Router (This might fail)...")
    try:
        from intelligence_router import router, TaskType
        print("   Success.")
    except Exception as router_err:
        print(f"!!! ROUTER IMPORT ERROR: {router_err}")
        traceback.print_exc()
        # Continue without router to allow partial boot
        router = None
        TaskType = None

    print("3. Importing Aergia API...")
    import aergia_api
    print("   Success.")

    print("4. Starting Server...")
    aergia_api.main()

except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    traceback.print_exc()
    input("Press Enter to Exit...")
