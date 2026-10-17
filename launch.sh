#!/usr/bin/env bash
cd "$(dirname "$0")"
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi
"$PYTHON_CMD" "scripts/launch.py" "$@"
