# Aergia Unified Dashboard - Deployment Guide

## What This Is
The Aergia Unified Dashboard is a Flask-based web interface that serves as the "Pantheon Launcher" for your Agentic OS. It combines the beautiful Visual Canon with functional module launching.

## File Structure
```
C:\Users\z143d\Aergia_Studio\
├── aergia_api.py                # Main Flask app (Backend)
├── Aergia_Web/
│   ├── templates/
│   │   └── dashboard.html       # HTML template
│   └── static/
│       ├── style.css            # Cinematic styling
│       ├── script.js            # Interactive logic
│       └── assets/              # Visual Canon
│           ├── banners/
│           ├── icons/
│           └── wallpapers/
```

## Installation Steps

### 1. Copy Files
The system has automatically generated the required files in `Aergia_Studio/Aergia_Web`.

### 2. Copy Assets
Assets have been moved to `Aergia_Web/static/assets/` to ensure they load correctly.

### 3. Install Flask (if not already installed)
```bash
pip install flask
```

### 4. Launch the Dashboard
You can use the provided batch scripts:
*   **Start Server**: `Launch_Aergia_API.bat`
*   **Open Interface**: `Launch_Web_Dashboard.bat`

### 5. Open in Browser
Navigate to: http://localhost:5000

## Features

### Interactive Pantheon Grid
- Click any god icon to launch their module
- Hover over icons to see their banner as the background
- Smooth cinematic transitions

### Keyboard Shortcuts
- Press `R` → Launch Aergia (Rest Mode)
- Press `H` → Launch Hephaestus (Code)

### Status Bar
Real-time feedback on module launches at the bottom of the screen

## Module Actions
The dashboard currently supports:
- **Athena** → intelligence_router.py
- **Prometheus** → intelligence_router.py (reasoning mode)
- **Hephaestus** → antigravity.abacus.ai (URL)
- **Hyperion** → Project Hyperion/hyperion_gui.py
- **Midas** → Project Midas/midas_home.py
- **Chimera** → start_chimera.bat
- **Aergia** → Rest Mode (dims screen)

## Customization

### Change Background
Edit `static/style.css` line 18 to use a different default background:
```css
background-image: url('/static/assets/wallpapers/The_Pantheon_Circle.png');
```

### Add New Gods
Edit the `PANTHEON` dictionary in `aergia_api.py` to add new modules.

### Modify Colors
The teal-amber palette is defined in `style.css`:
- Primary Teal: `#00d2d3`
- Gold/Amber: `#e0af65`
- Dark Background: `#0b1a20`

## Troubleshooting

### "Module not found" errors
Verify the paths in the `launch_module()` function in `aergia_api.py` match your actual file locations.

### Assets not loading
Ensure all images are in the `Aergia_Web/static/assets` folder.

### Port already in use
Change the port in `aergia_api.py` line 147:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Next Steps
1. Test each module launch
2. Add the theme song player for Aergia rest mode
3. Implement the Planner Layer integration
4. Create desktop shortcut to launch dashboard on boot

---
Built with the Lazy Genius approach 🧿
