"""
Aergia Unified Dashboard
The Pantheon Launcher - Cinematic Agentic OS Interface
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import os
import os
import sys

# Import Intelligence Router for Swarm
from intelligence_router import router, TaskType

# Configure Flask to use Aergia_Web folders
app = Flask(__name__, 
            template_folder=r'Aergia_Web/templates',
            static_folder=r'Aergia_Web/static')
CORS(app)

# Root directory
ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve files from the root assets directory"""
    return send_from_directory(os.path.join(ROOT, 'assets'), filename)

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio files from the assets/audio directory"""
    return send_from_directory(os.path.join(ROOT, 'assets', 'audio'), filename)

# Pantheon Registry - Maps gods to their modules
# ADAPTED: Using Restored Canon filenames
PANTHEON = {
    'athena': {
        'name': 'Athena',
        'title': 'Wisdom & General Chat',
        'icon': 'assets/icons/Athena_Icon.png',
        'banner': 'assets/banners/Athena_Banner.png',
        'action': 'intelligence_router',
        'description': 'General purpose AI assistant powered by ChatLLM'
    },
    'prometheus': {
        'name': 'Prometheus',
        'title': 'Deep Reasoning & Research',
        'icon': 'assets/icons/Prometheus_Icon.png',
        'banner': 'assets/banners/Prometheus_Banner.png',
        'action': 'intelligence_router',
        'description': 'Advanced reasoning using Gemini for complex analysis'
    },
    'hephaestus': {
        'name': 'Hephaestus',
        'title': 'Code Creation & Building',
        'icon': 'assets/icons/Hephaestus_Icon.png',
        'banner': 'assets/banners/Hephaestus_Banner.png',
        'action': 'antigravity',
        'description': 'Code generation and project building with Antigravity'
    },
    'aergia': {
        'name': 'Aergia',
        'title': 'Rest & Healing',
        'icon': 'assets/icons/Aergia_Icon.png',
        'banner': 'assets/banners/Aergia_Banner.png',
        'action': 'rest_mode',
        'description': 'The lazy genius - rest, reflection, and restoration'
    },
    'hermes': {
        'name': 'Hermes',
        'title': 'Travel & Connection',
        'icon': 'assets/icons/Hermes_Icon.png',
        'banner': 'assets/banners/Hermes_Banner.png',
        'action': 'hermes_connector',
        'description': 'Connect to Tailscale Network (Satellite Mode)'
    },
    'aura': {
        'name': 'Aura',
        'title': 'Energy & Wind',
        'icon': 'assets/icons/Aura_Icon.png',
        'banner': 'assets/banners/Aura_Banner.png',
        'action': 'coming_soon',
        'description': 'System monitoring and energy management'
    },
    'hestia': {
        'name': 'Hestia',
        'title': 'Health & Bioregulation',
        'icon': 'assets/icons/Hestia_Icon.png',
        'banner': 'assets/banners/Hestia_Banner.png',
        'action': 'hestia_health',
        'description': 'Daily checklist, peptide schedules, and biomarker tracking'
    },
    'hyperion': {
        'name': 'Hyperion',
        'title': 'AI Director & Oversight',
        'icon': 'assets/icons/Hyperion_Icon.png',
        'banner': 'assets/banners/Hyperion_Banner.png',
        'action': 'hyperion_director',
        'description': 'AI video director and creative orchestration'
    },
    'midas': {
        'name': 'Midas',
        'title': 'Financial Engine',
        'icon': 'assets/icons/Midas_Icon.png',
        'banner': 'assets/banners/Midas_Banner.png',
        'action': 'midas_home',
        'description': 'Financial tracking and value optimization'
    },
    'chimera': {
        'name': 'Chimera',
        'title': 'Video & Media Engine',
        'icon': 'assets/icons/Chimera_Icon.png',
        'banner': 'assets/banners/Chimera_Banner.png',
        'action': 'chimera_studio',
        'description': 'AI video generation powered by FAL.ai'
    },
    'morai': {
        'name': 'Morai',
        'title': 'The Fates & Destiny',
        'icon': 'assets/icons/Morai_Icon.png',
        'banner': 'assets/banners/Morai_Banner.png',
        'action': 'morai_engine',
        'description': 'Weaving the threads of destiny and execution'
    },
    'kairos': {
        'name': 'Kairos',
        'title': 'Time & Scheduling',
        'icon': 'assets/icons/Kairos_Icon.png',
        'banner': 'assets/banners/Kairos_Banner.png',
        'action': 'coming_soon',
        'description': 'Task scheduling and temporal orchestration'
    },
    'plutus': {
        'name': 'Plutus',
        'title': 'Legacy & Final Output',
        'icon': 'assets/icons/Plutus_Icon.png',
        'banner': 'assets/banners/Plutus_Banner.png',
        'action': 'plutus_treasury',
        'description': 'Final output generation and legacy archiving'
    },
    'ares': {
        'name': 'Ares',
        'title': 'Cyber Defense',
        'icon': 'assets/icons/Ares_Icon.png',
        'banner': 'assets/banners/Ares_Banner.png',
        'action': 'coming_soon',
        'description': 'Find Evil! - Protocol SIFT / Nemo Claw'
    },
    'edge': {
        'name': 'Edge AI',
        'title': 'Local Offline Intelligence',
        'icon': 'assets/icons/Prometheus_Icon.png',
        'banner': 'assets/banners/Prometheus_Banner.png',
        'action': 'intelligence_router',
        'description': 'Run open-weights models (Gemma/Hermes) locally for free via Ollama'
    }
}


@app.route('/')
def index():
    """Main dashboard view"""
    return render_template('dashboard.html', pantheon=PANTHEON)

@app.route('/api/launch/<god_id>')
def launch_module(god_id):
    """Launch a specific module"""
    if god_id not in PANTHEON:
        return jsonify({'error': 'Unknown god'}), 404

    god = PANTHEON[god_id]
    action = god['action']

    try:
        if action == 'intelligence_router':
            # Launch the intelligence router
            # Launch the intelligence router
            subprocess.Popen([sys.executable, os.path.join(ROOT, 'intelligence_router.py')], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'antigravity':
            # Launch Antigravity (Hephaestus)
            # Adapting to open URL as requested in previous logic (no local launcher found yet)
            import webbrowser
            webbrowser.open("https://antigravity.abacus.ai/")
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'hyperion_director':
            # Launch Hyperion
            script_path = os.path.join(ROOT, 'Project Hyperion', 'hyperion_gui.py')
            # Launch Hyperion
            script_path = os.path.join(ROOT, 'Project Hyperion', 'hyperion_gui.py')
            subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path), creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'midas_home':
            # Launch Midas Pro Terminal
            script_path = os.path.join(ROOT, 'Project Midas', 'midas_terminal.py') # [UPDATE] Point to new terminal
            subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path), creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'chimera_studio':
            # Launch Chimera
            # Launch Chimera
            script_path = os.path.join(ROOT, 'start_chimera.sh') # Using sh for mac
            subprocess.Popen(['bash', script_path], cwd=ROOT)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'hermes_connector':
            # Launch Hermes (Satellite Connector)
            script_path = os.path.join(ROOT, 'Connect_Mac_Node.command')
            # Use 'open' on Mac to launch in a new Terminal window
            subprocess.Popen(['open', script_path], cwd=ROOT)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'morai_engine':
            # Launch Morai
            script_path = os.path.join(ROOT, 'Project Morai', 'morai_engine.py')
            # Launch Morai
            script_path = os.path.join(ROOT, 'Project Morai', 'morai_engine.py')
            subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path), creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'plutus_treasury':
            # Launch Plutus (Treasury)
            script_path = os.path.join(ROOT, 'Project Plutus', 'plutus_treasury.py')
            subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path), creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return jsonify({'status': 'launched', 'module': god['name']})

        elif action == 'rest_mode':
            # Aergia rest mode - play theme song, dim screen, etc.
            return jsonify({'status': 'rest_mode_activated', 'module': god['name']})

        elif action == 'hestia_health':
            # Launch Hestia Health Server (health_ops_server.py)
            script_path = os.path.join(ROOT, 'health_ops_server.py')
            subprocess.Popen([sys.executable, script_path], cwd=ROOT, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            # Open browser to local health center
            import webbrowser
            webbrowser.open("http://localhost:5000")
            return jsonify({'status': 'launched', 'module': god['name']})

        elif god_id == 'ares':
            # Launch the Ares REST API backend
            script_path = os.path.join(ROOT, "..", "Project-Ares-SANS", "src", "ares_api.py")
            subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path), creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            # Automatically open the browser to the web view
            import webbrowser
            webbrowser.open("http://localhost:5555" if os.getenv("ARES_PORT") else "http://localhost:5051")
            return jsonify({'status': 'launched', 'module': god['name']})

        else:
            return jsonify({'status': 'coming_soon', 'module': god['name']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/git_sync', methods=['POST'])
def git_sync():
    """
    Perform a Git Sync:
    1. Git Pull (Unattended)
    2. Git Add .
    3. Git Commit
    4. Git Push
    """
    try:
        log = []
        
        def run_git(args):
            # Run git command in ROOT
            result = subprocess.run(['git'] + args, cwd=ROOT, capture_output=True, text=True)
            output = result.stdout + result.stderr
            log.append(f"> git {' '.join(args)}\n{output}")
            return result.returncode == 0

        # 1. Pull
        log.append("--- PULLING CHANGES ---")
        if run_git(['pull', '--rebase', '--autostash']):
             log.append("Pull Successful.")
        else:
             log.append("Pull Failed (Likely Conflict or Network). Continuing to Push...")

        # 2. Add
        log.append("\n--- STAGING CHANGES ---")
        run_git(['add', '.'])

        # 3. Commit
        log.append("\n--- COMMITTING ---")
        # Check if there are changes first
        status = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout
        if status.strip():
            msg = f"Auto-Sync: {os.environ.get('USER', 'Aergia User')}"
            run_git(['commit', '-m', msg])
        else:
            log.append("No local changes to commit.")

        # 4. Push
        log.append("\n--- PUSHING TO CLOUD ---")
        if run_git(['push']):
             log.append("Push Successful.")
        else:
             log.append("Push Failed. Check Authentication.")

        return jsonify({'status': 'completed', 'log': '\n'.join(log)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/taildrop', methods=['POST'])
def taildrop_sync():
    """
    Direct Sync via Tailscale (Taildrop).
    Automatically detects OS and sends to the partner device.
    
    Mac -> Sends to 'dansasusvivo' (Windows)
    Windows -> Sends to 'daniels-macbook-pro' (Mac)
    
    Modes:
    - 'project': Syncs code (ignores venv, __pycache__, etc.)
    - 'secrets': Syncs .env and token files (Sensitive!)
    """
    try:
        data = request.json
        mode = data.get('mode', 'project')
        
        import platform
        import shutil
        import datetime
        import zipfile
        
        current_os = platform.system()
        
        # Configuration based on OS
        if current_os == "Darwin": # Mac
            target_device = "dansasusvivo" 
            tailscale_cli = "/Applications/Tailscale.app/Contents/MacOS/Tailscale"
             # Fallback if cli not found (user might have brew install)
            if not os.path.exists(tailscale_cli):
                tailscale_cli = "tailscale"
        elif current_os == "Windows":
            target_device = "daniels-macbook-pro"
            tailscale_cli = "tailscale" # Usually in PATH on Windows
        else:
             # Linux / Other
            target_device = "dansasusvivo" # Default to Windows machine if running on Linux server?
            tailscale_cli = "tailscale"

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if mode == 'secrets':
            # 1. Zip Secrets
            zip_name = f"Aergia_Secrets_{timestamp}.zip"
            zip_path = os.path.join(ROOT, zip_name)
            
            files_to_send = [
                ".env",
                "Project Midas/schwab_tokens.json",
                "Project Midas/chimera-credentials.json"
            ]
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                found_any = False
                for f in files_to_send:
                    full_p = os.path.join(ROOT, f)
                    if os.path.exists(full_p):
                        zipf.write(full_p, arcname=os.path.basename(f))
                        found_any = True
                    else:
                        print(f"Skipping missing secret: {f}")
                
                if not found_any:
                    return jsonify({'error': "No secrets found to send."}), 404
                        
        else:
            # 2. Zip Project (Code + Configs only)
            zip_name = f"Aergia_Project_{timestamp}.zip" 
            if not os.path.exists(os.path.join(ROOT, "tmp")):
                os.makedirs(os.path.join(ROOT, "tmp"))
            zip_path = os.path.join(ROOT, "tmp", zip_name)
            
            # Whitelist approach is much faster and safer for massive project folders
            allowed_exts = {'.py', '.html', '.css', '.js', '.json', '.md', '.png', '.jpg', '.bat', '.sh', '.command', '.txt'}
            ignore_dirs = {'.git', '.venv', 'venv', '__pycache__', 'tmp', 'node_modules', '.idea', '.vscode', '.gemini'}
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root_dir, dirs, files in os.walk(ROOT):
                    # Modify dirs in-place to skip heavy ignored directories entirely
                    dirs[:] = [d for d in dirs if d not in ignore_dirs]
                    
                    for f in files:
                        if any(f.lower().endswith(ext) for ext in allowed_exts):
                            full_path = os.path.join(root_dir, f)
                            rel_path = os.path.relpath(full_path, ROOT)
                            zipf.write(full_path, arcname=rel_path)

        # 3. Execute Taildrop
        cmd = [tailscale_cli, "file", "cp", zip_path, f"{target_device}:"]
        
        print(f"[TAILDROP] Sending {zip_path} to {target_device} via {tailscale_cli}...")
        
        # Cross-platform subprocess handling
        if current_os == "Windows":
             result = subprocess.run(cmd, capture_output=True, text=True, shell=True) # Shell needed for PATH resol sometimes
        else:
             result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Cleanup Zip
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': f"Sent to {target_device}. Check 'Received Files'."})
        else:
            return jsonify({'error': f"Taildrop Failed: {result.stderr}"}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

import io

@app.route('/api/system/sync_state', methods=['GET'])
def sync_state():
    """
    Returns a dictionary of all relevant files and their last modification timestamps.
    Used by the requesting node to compute a diff.
    """
    try:
        import platform
        import stat
        state = {}
        
        allowed_exts = {'.py', '.html', '.css', '.js', '.json', '.md', '.png', '.jpg', '.bat', '.sh', '.command', '.txt'}
        ignore_dirs = {'.git', '.venv', 'venv', '__pycache__', 'tmp', 'node_modules', '.idea', '.vscode', '.gemini'}
        
        for root_dir, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for f in files:
                if any(f.lower().endswith(ext) for ext in allowed_exts):
                    full_path = os.path.join(root_dir, f)
                    rel_path = os.path.relpath(full_path, ROOT)
                    # Use os.stat to get modification time
                    mtime = os.stat(full_path)[stat.ST_MTIME]
                    state[rel_path] = mtime
                    
        return jsonify({'status': 'success', 'os': platform.system(), 'state': state})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/sync_receive', methods=['POST'])
def sync_receive():
    """
    Receives a packaged ZIP of changed files and extracts them directly
    over the local Aergia_Studio directory.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request.'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading.'}), 400

        # Save the incoming zip to tmp
        if not os.path.exists(os.path.join(ROOT, "tmp")):
            os.makedirs(os.path.join(ROOT, "tmp"))
            
        zip_path = os.path.join(ROOT, "tmp", "incoming_delta.zip")
        file.save(zip_path)
        
        print(f"[SYNC_RECEIVE] Received {file.filename}. Extracting...")
        
        # Extract directly over the ROOT directory
        import zipfile
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extracted_files = zip_ref.namelist()
            zip_ref.extractall(ROOT)
            
        # Cleanup
        os.remove(zip_path)
        
        print(f"[SYNC_RECEIVE] Successfully updated {len(extracted_files)} files.")
        
        return jsonify({
            'status': 'success', 
            'message': f'Seamlessly updated {len(extracted_files)} files in place.',
            'files': extracted_files
        })
        
    except Exception as e:
        print(f"[SYNC_RECEIVE ERROR] {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/deep_sync', methods=['POST'])
def deep_sync():
    """
    The brain of the Delta Sync.
    1. Fetches the target node's sync_state.
    2. Compares local files against the target's state.
    3. Zips ONLY new or modified files.
    4. POSTs the zip to the target's sync_receive endpoint.
    """
    try:
        import requests
        import platform
        import stat
        import zipfile
        
        current_os = platform.system()
        target_ip = "100.111.220.42" if current_os == "Darwin" else "100.75.65.95" # Windows IP or Mac IP
        base_url = f"http://{target_ip}:5050"
        
        print(f"[DEEP_SYNC] Fetching state from {base_url}/api/system/sync_state...")
        
        # 1. Fetch Remote State
        try:
            response = requests.get(f"{base_url}/api/system/sync_state", timeout=5)
            response.raise_for_status()
            remote_data = response.json()
            remote_state = remote_data.get('state', {})
        except requests.exceptions.RequestException as e:
             return jsonify({'error': f'Could not connect to target node ({target_ip}). Is aergia_api.py running?'}), 503

        print(f"[DEEP_SYNC] Target has {len(remote_state)} files. Computing diff...")

        # 2. Compute Diff & Zip
        if not os.path.exists(os.path.join(ROOT, "tmp")):
            os.makedirs(os.path.join(ROOT, "tmp"))
            
        zip_path = os.path.join(ROOT, "tmp", "outgoing_delta.zip")
        files_to_send = []
        
        allowed_exts = {'.py', '.html', '.css', '.js', '.json', '.md', '.png', '.jpg', '.bat', '.sh', '.command', '.txt'}
        ignore_dirs = {'.git', '.venv', 'venv', '__pycache__', 'tmp', 'node_modules', '.idea', '.vscode', '.gemini'}
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, dirs, files in os.walk(ROOT):
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                for f in files:
                    if any(f.lower().endswith(ext) for ext in allowed_exts):
                        full_path = os.path.join(root_dir, f)
                        rel_path = os.path.relpath(full_path, ROOT)
                        
                        # Use normpath to ensure cross-platform path matching
                        normalized_rel_path = rel_path.replace('\\', '/')
                        
                        mtime = os.stat(full_path)[stat.ST_MTIME]
                        remote_mtime = remote_state.get(normalized_rel_path, 0)
                        
                        # If file is newer locally (by > 2 seconds to account for clock skew) or doesn't exist remotely
                        if mtime > (remote_mtime + 2):
                            zipf.write(full_path, arcname=rel_path)
                            files_to_send.append(rel_path)

        # 3. Send Payload
        if not files_to_send:
             if os.path.exists(zip_path): os.remove(zip_path)
             return jsonify({'status': 'success', 'message': 'Systems are already perfectly synced. 0 bytes transferred.'})

        print(f"[DEEP_SYNC] Zipped {len(files_to_send)} changed files. Transmitting payload...")
        
        try:
             with open(zip_path, 'rb') as f:
                 files = {'file': ('outgoing_delta.zip', f, 'application/zip')}
                 post_response = requests.post(f"{base_url}/api/system/sync_receive", files=files, timeout=30)
                 post_response.raise_for_status()
                 result_data = post_response.json()
                 
                 # Cleanup
                 os.remove(zip_path)
                 
                 return jsonify({
                     'status': 'success', 
                     'message': f"Sent {len(files_to_send)} modified files. Target extracted successfully.",
                     'log': "\n".join(files_to_send)
                 })
                 
        except requests.exceptions.RequestException as e:
             if os.path.exists(zip_path): os.remove(zip_path)
             # Try to get backend error message if it returned JSON
             err_msg = str(e)
             if hasattr(e, 'response') and e.response is not None:
                 try:
                     err_msg = e.response.json().get('error', err_msg)
                 except: pass
             return jsonify({'error': f'Failed to send payload: {err_msg}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/network_status', methods=['GET'])
def network_status():
    """Check if the Ryzen Windows User (dansasusvivo) is accessible via Tailscale."""
    try:
        import platform
        # Target the Ryzen laptop specifically via its static Tailscale IP
        target_ip = "100.111.220.42"
        
        # Determine the correct ping command based on OS (Mac uses -c, Windows uses -n)
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "1", "-w", "2000", target_ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "2000", target_ip]
        
        # Execute the ping. A return code of 0 means the Ryzen laptop answered the ping.
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({'status': 'online', 'details': f'Connected to Ryzen node at {target_ip}'})
        else:
            return jsonify({'status': 'offline', 'error': 'Ryzen node unreachable or Tailscale offline on remote'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})

@app.route('/api/system/network_launch', methods=['POST'])
def network_launch():
    """Launch the Tailscale Application."""
    try:
        import platform
        sys_os = platform.system()
        
        if sys_os == "Darwin":
            subprocess.Popen(["open", "-a", "Tailscale"])
            return jsonify({'status': 'launching', 'message': 'Opening Tailscale on Mac...'})
            
        elif sys_os == "Windows":
            # Try generic start first
            subprocess.Popen("start tailscale-ipn", shell=True) 
            # Fallback to common path if needed (though start usually works if registered)
            return jsonify({'status': 'launching', 'message': 'Opening Tailscale on Windows...'})
            
        else:
            return jsonify({'error': 'Unsupported OS for auto-launch'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ask_hive', methods=['POST'])
def ask_hive():
    """
    Send a prompt to the Hive Mind (Swarm).
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        print(f"🐝 Hive Request: {prompt}")
        
        # Execute Swarm Logic
        response = router.generate(prompt, task_type=TaskType.SWARM)
        
        return jsonify({'status': 'success', 'response': response})

    except Exception as e:
        print(f"Hive Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/worker/execute', methods=['POST'])
def execute_task():
    """
    Endpoint to receive tasks from other Pantheon nodes (e.g. Mac -> Windows).
    Expected JSON:
    {
        "module": "midas",
        "script": "crunch_numbers.py", 
        "args": ["--mode", "heavy"],
        "cwd": "optional/path" 
    }
    """
    try:
        data = request.json
        full_command = []
        
        # Determine the python executable (using system python)
        full_command.append(sys.executable)
        
        # Resolve script path
        # Assume scripts are relative to Aergia Root if not absolute
        script = data.get('script')
        if not script:
            return jsonify({'error': 'No script specified'}), 400
            
        script_path = script if os.path.isabs(script) else os.path.join(ROOT, script)
        
        if not os.path.exists(script_path):
             # Try looking in project folders
             possible_paths = [
                 os.path.join(ROOT, "Project Midas", script),
                 os.path.join(ROOT, "Project Chimera", script),
                 os.path.join(ROOT, "Project Hyperion", script)
             ]
             found = False
             for p in possible_paths:
                 if os.path.exists(p):
                     script_path = p
                     found = True
                     break
             if not found:
                 return jsonify({'error': f'Script not found: {script}'}), 404

        full_command.append(script_path)
        
        # Add args
        if 'args' in data:
            full_command.extend(data['args'])
            
        # Determine CWD
        cwd = data.get('cwd') or os.path.dirname(script_path)
        
        print(f"[WORKER] Executing: {full_command} in {cwd}")
        
        # Run in background (fire and forget)
        subprocess.Popen(full_command, cwd=cwd, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        
        return jsonify({'status': 'task_started', 'command': str(full_command), 'node': os.environ.get('COMPUTERNAME', 'Unknown')})
        
    except Exception as e:
        print(f"[WORKER ERROR] {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/pantheon')
def get_pantheon():
    """Return the full pantheon registry"""
    return jsonify(PANTHEON)

if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    print("[SYSTEM] Aergia Unified Dashboard Starting...")
    print(f"Root: {ROOT}")
    print(f"Pantheon: {len(PANTHEON)} gods registered")
    app.run(debug=True, host='0.0.0.0', port=5050)
