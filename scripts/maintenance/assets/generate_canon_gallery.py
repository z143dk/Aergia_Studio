
import os

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
    # 1. Active Canon (Root Dir)
    active_exists = [f for f in REQUIRED_ASSETS if os.path.exists(f)]
    active_exists.sort()

    # 2. Legacy/Story (assets/legacy)
    legacy_dir = os.path.join("assets", "legacy")
    legacy_files = []
    if os.path.exists(legacy_dir):
        legacy_files = [f for f in os.listdir(legacy_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        legacy_files.sort()

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Aergia Visual Canon (Blended)</title>
    <style>
        body {{ background-color: #0b1a20; color: #e0af65; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
        h1 {{ text-align: center; color: #e0af65; text-transform: uppercase; letter-spacing: 2px; }}
        h2 {{ text-align: center; color: #888; font-size: 1.2em; margin-top: -10px; margin-bottom: 30px; }}
        .section-title {{ grid-column: 1 / -1; font-size: 1.5em; border-bottom: 2px solid #e0af65; padding-top: 40px; margin-bottom: 20px; color: #00d2d3; }}
        .legacy-title {{ color: #ff6b6b; border-color: #ff6b6b; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .card {{ background: #12252e; padding: 10px; border: 1px solid #005f60; border-radius: 8px; text-align: center; transition: transform 0.2s; }}
        .card:hover {{ transform: scale(1.02); border-color: #00d2d3; box-shadow: 0 0 15px rgba(0, 210, 211, 0.3); }}
        .card.legacy {{ border-color: #552222; background: #251212; }}
        .card.legacy:hover {{ border-color: #ff6b6b; box-shadow: 0 0 15px rgba(255, 107, 107, 0.3); }}
        img {{ max-width: 100%; height: auto; border-radius: 4px; display: block; margin: 0 auto; }}
        .label {{ margin-top: 10px; font-size: 0.9em; color: #aaa; }}
    </style>
</head>
<body>
    <h1>🧿 The Aergia Visual Canon</h1>
    <h2>Restored Pantheon + User Legacy</h2>
    
    <div class="grid">
        <div class="section-title">Active Canon: Wallpapers</div>
"""
    
    # Active
    wallpapers = [f for f in active_exists if "The_" in f]
    banners = [f for f in active_exists if "_Banner" in f]
    icons = [f for f in active_exists if "_Icon" in f]

    for f in wallpapers:
        html_content += f"""<div class="card"><img src="{f}" loading="lazy"><div class="label">{f}</div></div>"""

    html_content += """<div class="section-title">Active Canon: Banners</div>"""
    for f in banners:
        html_content += f"""<div class="card"><img src="{f}" loading="lazy"><div class="label">{f}</div></div>"""

    html_content += """<div class="section-title">Active Canon: Icons</div>"""
    for f in icons:
        html_content += f"""<div class="card" style="width:150px; margin:0 auto;"><img src="{f}" loading="lazy"><div class="label">{f}</div></div>"""

    # Legacy
    if legacy_files:
        html_content += """<div class="section-title legacy-title">The Story So Far (Legacy Archives)</div>"""
        for f in legacy_files:
             # Link to assets/legacy/...
             src_path = f"assets/legacy/{f}"
             html_content += f"""
            <div class="card legacy">
                <img src="{src_path}" loading="lazy">
                <div class="label">{f}</div>
            </div>"""

    html_content += """
    </div>
</body>
</html>
"""
    
    with open("visual_canon_gallery.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Generated blended gallery with {len(active_exists)} active and {len(legacy_files)} legacy assets.")

if __name__ == "__main__":
    generate_html()
