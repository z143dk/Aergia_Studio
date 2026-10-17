
import os
import json

# The 27 Required Assets (The Slots)
REQUIRED_ASSETS = [
    # Wallpapers
    "The_Opening_Frame.png", "The_Journey.png", "The_Pantheon_Circle.png",
    # Banners
    "Athena_Banner.png", "Prometheus_Banner.png", "Hephaestus_Banner.png", "Aergia_Banner.png",
    "Hermes_Banner.png", "Aura_Banner.png", "Hestia_Banner.png", "Hyperion_Banner.png",
    "Midas_Banner.png", "Chimera_Banner.png", "Kairos_Banner.png", "Plutus_Banner.png",
    # Icons
    "Athena_Icon.png", "Prometheus_Icon.png", "Hephaestus_Icon.png", "Aergia_Icon.png",
    "Hermes_Icon.png", "Aura_Icon.png", "Hestia_Icon.png", "Hyperion_Icon.png",
    "Midas_Icon.png", "Chimera_Icon.png", "Kairos_Icon.png", "Plutus_Icon.png"
]

def get_legacy_files():
    legacy_dir = os.path.join("assets", "legacy")
    files = []
    if os.path.exists(legacy_dir):
        for f in os.listdir(legacy_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                files.append(f)
    files.sort()
    return files

def generate_html():
    legacy_files = get_legacy_files()
    legacy_files_json = json.dumps(legacy_files)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Aergia Canon Builder</title>
    <style>
        body {{ background-color: #0b1a20; color: #e0af65; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
        h1 {{ text-align: center; margin-bottom: 30px; }}
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        .slot-row {{ 
            display: grid; 
            grid-template-columns: 200px 300px 300px 1fr; 
            gap: 20px; 
            background: #12252e; 
            margin-bottom: 15px; 
            padding: 15px; 
            border-radius: 8px; 
            align-items: center;
            border: 1px solid #1f3a47;
        }}
        
        .slot-name {{ font-weight: bold; font-size: 1.1em; color: #00d2d3; }}
        
        img {{ max-width: 100%; max-height: 150px; border-radius: 4px; border: 2px solid #333; }}
        
        select {{ 
            width: 100%; 
            padding: 10px; 
            background: #0f1c24; 
            color: #fff; 
            border: 1px solid #005f60; 
            border-radius: 4px;
        }}
        
        .preview-box {{ text-align: center; }}
        .preview-label {{ font-size: 0.8em; color: #777; margin-bottom: 5px; }}
        
        .actions {{ position: sticky; bottom: 20px; background: #0b1a20; padding: 20px; border-top: 2px solid #00d2d3; margin-top: 40px; display: flex; gap: 20px; align-items: center; justify-content: flex-end; }}
        
        button {{ 
            padding: 12px 24px; 
            background: #00d2d3; 
            color: #000; 
            border: none; 
            border-radius: 4px; 
            font-weight: bold; 
            cursor: pointer; 
            font-size: 1em; 
        }}
        button:hover {{ background: #00a8a9; }}
        
        textarea {{ width: 100%; height: 150px; background: #080f12; color: #0f0; font-family: monospace; padding: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧿 Canon Selector</h1>
        <p>Curate your experience. Select which image to use for each official slot.</p>
        
        <div id="slots-container"></div>
        
        <div class="actions">
            <div style="flex-grow:1">
                <h3>Selection Script</h3>
                <textarea id="output-script" readonly></textarea>
            </div>
            <button onclick="generateScript()">GENERATE SCRIPT</button>
            <button onclick="copyScript()" style="background: #e0af65;">COPY TO CLIPBOARD</button>
        </div>
    </div>

    <script>
        const REQUIRED_ASSETS = {json.dumps(REQUIRED_ASSETS)};
        const LEGACY_FILES = {legacy_files_json};
        
        function init() {{
            const container = document.getElementById('slots-container');
            
            REQUIRED_ASSETS.forEach(slot => {{
                // Determine if 1:1 or 16:9 for display hints
                const isIcon = slot.includes('Icon');
                
                const row = document.createElement('div');
                row.className = 'slot-row';
                
                // Name
                const nameDiv = document.createElement('div');
                nameDiv.className = 'slot-name';
                nameDiv.innerText = slot.replace('.png', '').replace('_', ' ');
                
                // Current (Active)
                const currentDiv = document.createElement('div');
                currentDiv.className = 'preview-box';
                currentDiv.innerHTML = `<div class="preview-label">Current Active</div><img src="${{slot}}?t=${{Date.now()}}">`;
                
                // Selector
                const selectDiv = document.createElement('div');
                const select = document.createElement('select');
                select.id = `sel-${{slot}}`;
                select.onchange = (e) => updatePreview(slot, e.target.value);
                
                // Default option (Keep Current)
                const defOpt = document.createElement('option');
                defOpt.value = "CURRENT";
                defOpt.text = "Use Current (Regenerated)";
                select.appendChild(defOpt);
                
                // Legacy Options
                LEGACY_FILES.forEach(f => {{
                    const opt = document.createElement('option');
                    opt.value = f;
                    opt.text = `Legacy: ${{f}}`;
                    select.appendChild(opt);
                }});
                
                selectDiv.appendChild(select);
                
                // New Preview
                const newPreviewDiv = document.createElement('div');
                newPreviewDiv.className = 'preview-box';
                newPreviewDiv.id = `preview-${{slot}}`;
                newPreviewDiv.innerHTML = `<div class="preview-label">New Selection</div><img src="${{slot}}" style="opacity:0.5; filter:grayscale(1);">`;
                
                row.appendChild(nameDiv);
                row.appendChild(currentDiv);
                row.appendChild(selectDiv);
                row.appendChild(newPreviewDiv);
                
                container.appendChild(row);
            }});
        }}
        
        function updatePreview(slot, selectedValue) {{
            const div = document.getElementById(`preview-${{slot}}`);
            if (selectedValue === "CURRENT") {{
                div.innerHTML = `<div class="preview-label">New Selection</div><img src="${{slot}}" style="opacity:0.5; filter:grayscale(1);">`;
            }} else {{
                div.innerHTML = `<div class="preview-label">New Selection</div><img src="assets/legacy/${{selectedValue}}" style="border-color: #00d2d3;">`;
            }}
            generateScript();
        }}
        
        function generateScript() {{
            let script = "# Apply Visual Swaps\\n$root = 'C:\\\\Users\\\\z143d\\\\Aergia_Studio'\\n\\n";
            let changeCount = 0;
            
            REQUIRED_ASSETS.forEach(slot => {{
                const sel = document.getElementById(`sel-${{slot}}`);
                if (sel.value !== "CURRENT") {{
                    changeCount++;
                    script += `Write-Host "Swapping ${{slot}}..."\\n`;
                    script += `Copy-Item -Path "$root\\\\assets\\\\legacy\\\\${{sel.value}}" -Destination "$root\\\\${{slot}}" -Force\\n`;
                }}
            }});
            
            if (changeCount === 0) {{
                script = "# No changes selected.";
            }} else {{
                script += `\\nWrite-Host "Complete! ${{changeCount}} assets swapped." -ForegroundColor Green`;
            }}
            
            document.getElementById('output-script').value = script;
        }}
        
        function copyScript() {{
            const copyText = document.getElementById("output-script");
            copyText.select();
            document.execCommand("copy");
            alert("Script copied! Run this in your PowerShell terminal to apply changes.");
        }}

        init();
    </script>
</body>
</html>
"""
    
    with open("canon_selector.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Generated canon_selector.html")

if __name__ == "__main__":
    generate_html()
