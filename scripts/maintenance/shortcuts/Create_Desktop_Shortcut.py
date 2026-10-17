import os
import sys

def create_desktop_shortcut():
    """Creates a symbolic link on the user's desktop pointing to the dashboard launcher."""
    
    # 1. Identify paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_script = os.path.join(current_dir, "Launch_Dashboard.command")
    
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop_dir, "Aergia Dashboard.command")

    print(f"📍 Target: {target_script}")
    print(f"📍 Desktop: {desktop_dir}")

    # 2. Check if target exists
    if not os.path.exists(target_script):
        print("❌ Error: Launch_Dashboard.command not found in current directory.")
        return

    # 3. Remove existing shortcut if it exists (to prevent error)
    if os.path.exists(shortcut_path):
        try:
            os.remove(shortcut_path)
            print("🗑️  Removed existing shortcut.")
        except Exception as e:
            print(f"⚠️  Could not remove existing shortcut: {e}")

    # 4. Create Symlink
    try:
        os.symlink(target_script, shortcut_path)
        print("✅ Success! Created 'Aergia Dashboard' on your Desktop.")
        print("👉 You can now double-click it to launch Aergia.")
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")

if __name__ == "__main__":
    create_desktop_shortcut()
