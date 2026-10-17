
import requests
try:
    r = requests.get("http://127.0.0.1:5000/")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("Success: Dashboard is reachable")
    else:
        print("Failure: Non-200 status")
except Exception as e:
    print(f"Error: {e}")
