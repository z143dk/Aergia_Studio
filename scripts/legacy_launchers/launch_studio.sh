#!/bin/bash

# Get the directory where the script is located to ensure we run from the correct path
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Launching Aergia Studio..."
python3 aergia_dashboard.py
