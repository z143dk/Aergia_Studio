#!/bin/bash
# MacOS launcher for Project Chimera
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================="
echo "Starting Project Chimera (Mac Edition)"
echo "=========================================="

PYTHON_EXEC="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

# Check for Node/NPM
if ! command -v npm &> /dev/null; then
    echo "[WARNING] npm is not installed. React frontend will NOT start."
    echo "You can only use the backend API."
else
    echo "1. Starting React Frontend..."
    cd "Project Chimera/project-chimera/studio-dashboard-react"
    # Set env vars for Mac
    export BROWSER=none
    export HOST=0.0.0.0
    npm start &
    cd "$DIR"
fi

echo "2. Starting Flask API (Port 5001)..."
cd "Project Chimera/project-chimera/backend-flask"
export PORT=5001
export WORKER_URL="http://localhost:8081"
"$PYTHON_EXEC" app.py > backend.log 2>&1 &

echo "3. Starting Background Worker (Port 8081)..."
export PORT=8081
export AI_PROVIDER=fal
"$PYTHON_EXEC" worker.py > worker.log 2>&1 &

echo "=========================================="
echo "Chimera Backend Launched."
echo "Access via Dashboard or http://localhost:5001"
echo "=========================================="
