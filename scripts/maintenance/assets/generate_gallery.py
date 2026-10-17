import os

# The 27 Required Assets
REQUIRED_ASSETS = [
    # Banners
    "Athena_Banner.png", "Prometheus_Banner.png", "Hephaestus_Banner.png", "Aergia_Banner.png",
    "Hermes_Banner.png", "Aura_Banner.png", "Hestia_Banner.png", "Hyperion_Banner.png",
    "Midas_Banner.png", "Chimera_Banner.png", "Kairos_Banner.png", "Plutus_Banner.png",
    # Icons
    "Athena_Icon.png", "Prometheus_Icon.png", "Hephaestus_Icon.png", "Aergia_Icon.png",
    "Hermes_Icon.png", "Aura_Icon.png", "Hestia_Icon.png", "Hyperion_Icon.png",
    "Midas_Icon.png", "Chimera_Icon.png", "Kairos_Icon.png", "Plutus_Icon.png",
    # Wallpapers
    "The_Journey.png", "The_Pantheon_Circle.png", "The_Opening_Frame.png"
]

def generate_html():
    # Find images
    files = [f for f in os.listdir('.') if f.startswith('generated_image') and f.endswith('.png')]
    files.sort()

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Aergia Visual Sorter</title>
    <style>
        body {{ background-color: #1a1a1a; color: #ddd; font-family: sans-serif; padding: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }}
        .card {{ background: #2a2a2a; padding: 10px; border-radius: 8px; text-align: center; }}
        img {{ max-width: 100%; height: auto; border-radius: 4px; border: 2px solid #444; }}
        select {{ width: 100%; padding: 8px; margin-top: 10px; background: #333; color: white; border: 1px solid #555; }}
        .filename {{ font-size: 0.8em; color: #888; margin-bottom: 5px; word-break: break-all; }}
        #output-area {{ margin-top: 30px; padding: 20px; background: #000; border: 1px solid #444; }}
        button {{ padding: 10px 20px; background: #007acc; color: white; border: none; cursor: pointer; font-size: 1.1em; }}
        button:hover {{ background: #005f9e; }}
    </style>
</head>
<body>
    <h1>🧿 Aergia Visual Sorter</h1>
    <p>Match the generated images to their Canon names. When done, click "Generate Rename Script" and run it in PowerShell.</p>
    
    <div class="grid">
"""

    options = '<option value="">-- Select Role --</option>'
    for asset in REQUIRED_ASSETS:
        options += f'<option value="{asset}">{asset}</option>'

    for f in files:
        html_content += f"""
        <div class="card">
            <img src="{f}" loading="lazy">
            <div class="filename">{f}</div>
            <select id="sel_{f}" onchange="updateScript()">
                {options}
            </select>
        </div>
"""

    html_content += """
    </div>

    <div id="output-area">
        <h3>PowerShell Rename Script</h3>
        <textarea id="script-box" rows="15" style="width:100%; background:#111; color:#0f0; font-family:monospace;"></textarea>
        <br><br>
        <button onclick="copyScript()">Copy to Clipboard</button>
    </div>

    <script>
        function updateScript() {
            let script = "# Rename Assets Script\\n";
            script += "$root = 'C:\\\\Users\\\\z143d\\\\Aergia_Studio'\\n\\n";
            
            const selects = document.querySelectorAll('select');
            selects.forEach(sel => {
                if (sel.value) {
                    const original = sel.id.replace('sel_', '');
                    const target = sel.value;
                    script += `Rename-Item -Path "$root\\\\${original}" -NewName "${target}" -Force\\n`;
                    script += `Write-Host "Renamed ${original} -> ${target}"\\n`;
                }
            });
            
            document.getElementById('script-box').value = script;
        }

        function copyScript() {
            const copyText = document.getElementById("script-box");
            copyText.select();
            document.execCommand("copy");
            alert("Script copied! Paste into PowerShell.");
        }
    </script>
</body>
</html>
"""
    
    with open("visual_sorter.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Generated visual_sorter.html with {len(files)} candidates.")

if __name__ == "__main__":
    generate_html()
