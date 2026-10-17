#!/bin/bash
# Aergia Web Dashboard Launcher

# Ensure the terminal stays open on error
trap 'echo "Press any key to exit..."; read -n 1' EXIT

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "==========================================="
echo "   AERGIA PANTHEON LAUNCHER (MAC)"
echo "==========================================="
echo "Working Directory: $DIR"

# Open the browser (give server a second to start)
(sleep 3 && "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --profile-directory="Default" "http://localhost:5050" > /dev/null 2>&1) &

# Start the server using the specific python executable
PYTHON_EXEC="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

if [ -f "$PYTHON_EXEC" ]; then
    echo "Using Python: $PYTHON_EXEC"
    "$PYTHON_EXEC" aergia_api.py
else
    echo "ERROR: Python not found at $PYTHON_EXEC"
    echo "Falling back to 'python3'..."
    python3 aergia_api.py
fi
