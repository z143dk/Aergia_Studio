#!/bin/bash
# Midas Launcher (Debug Mode)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Launching Midas..." > midas_debug.log

PYTHON_EXEC="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
SCRIPT="Project Midas/midas_home.py"

echo "Python: $PYTHON_EXEC" >> midas_debug.log
echo "Script: $SCRIPT" >> midas_debug.log

# Check if script exists
if [ ! -f "$SCRIPT" ]; then
    echo "ERROR: Script not found!" >> midas_debug.log
    exit 1
fi

# Execute with logging
"$PYTHON_EXEC" "$SCRIPT" >> midas_debug.log 2>&1 &
echo "Process launched." >> midas_debug.log
