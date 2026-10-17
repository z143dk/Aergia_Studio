import sys
import json
import requests

# Set stdout to UTF-8 to handle any special characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

def show_status():
    try:
        r = requests.get(f"{API_URL}/api/state", timeout=5)
        if r.status_code != 200:
            print(f"Error: API returned status code {r.status_code}")
            return
        
        data = r.json()
        schedule = data.get("schedule", {})
        checked = data.get("checked_logs", [])
        weight = data.get("weight", 0.0)
        last_pain = data.get("last_pain", 0)

        print("=== AERGIA HEALTH STATUS ===")
        print(f"Current Weight: {weight} lbs")
        print(f"Last Joint Pain: {last_pain}/10")
        print("\n--- Daily Checklist & Schedule ---")
        
        # Combine morning, midday, night
        for period in ["morning", "midday", "night"]:
            items = schedule.get(period, [])
            if items:
                print(f"\n[{period.upper()}]")
                for item in items:
                    status = "[x]" if item in checked else "[ ]"
                    try:
                        print(f"  {status} {item}")
                    except UnicodeEncodeError:
                        print(f"  {status} [Item contains special characters]")
        print("===============================")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Health Ops Server at {API_URL}. Is it running?")
    except Exception as e:
        print(f"Error: {e}")

def toggle_item(item, state_str):
    checked = 1 if state_str.lower() in ["true", "1", "yes"] else 0
    payload = {
        "events": [
            {
                "type": "toggle_checklist",
                "item": item,
                "checked": checked
            }
        ]
    }
    send_sync(payload, f"Toggled '{item}' to {'Completed' if checked else 'Incomplete'}")

def log_workout(w_type, duration, avg_hr, details=""):
    try:
        duration = int(duration)
        avg_hr = int(avg_hr)
    except ValueError:
        print("Error: Duration and Average HR must be integers.")
        return

    payload = {
        "events": [
            {
                "type": "log_workout",
                "workout_type": w_type,
                "duration": duration,
                "avg_hr": avg_hr,
                "details": details
            }
        ]
    }
    send_sync(payload, f"Logged {w_type} workout ({duration} mins, Avg HR: {avg_hr})")

def log_recovery(pain, soreness, sleep, weight, notes=""):
    try:
        pain = int(pain)
        soreness = int(soreness)
        sleep = int(sleep)
        weight = float(weight)
    except ValueError:
        print("Error: pain, soreness, sleep must be integers. weight must be a float.")
        return

    payload = {
        "events": [
            {
                "type": "log_recovery",
                "joint_pain": pain,
                "soreness": soreness,
                "sleep_quality": sleep,
                "weight_lbs": weight,
                "notes": notes
            }
        ]
    }
    send_sync(payload, f"Logged recovery metrics (Pain: {pain}, Soreness: {soreness}, Sleep: {sleep}, Weight: {weight} lbs)")

def send_sync(payload, success_msg):
    try:
        r = requests.post(f"{API_URL}/api/sync", json=payload, timeout=5)
        if r.status_code == 200:
            print(f"Success: {success_msg}")
        else:
            print(f"Failed to sync. Server returned {r.status_code}: {r.text}")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Health Ops Server at {API_URL}. Is it running?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_health.py status")
        print("  python manage_health.py toggle <item_text> <true/false>")
        print("  python manage_health.py log-workout <type> <duration> <avg_hr> [details]")
        print("  python manage_health.py log-recovery <pain> <soreness> <sleep> <weight> [notes]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "status":
        show_status()
    elif cmd == "toggle" and len(sys.argv) >= 4:
        toggle_item(sys.argv[2], sys.argv[3])
    elif cmd == "log-workout" and len(sys.argv) >= 5:
        details = sys.argv[5] if len(sys.argv) >= 6 else ""
        log_workout(sys.argv[2], sys.argv[3], sys.argv[4], details)
    elif cmd == "log-recovery" and len(sys.argv) >= 6:
        notes = sys.argv[6] if len(sys.argv) >= 7 else ""
        log_recovery(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], notes)
    else:
        print("Invalid arguments or command.")
        sys.exit(1)
