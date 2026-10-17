#!/bin/bash
cd "$(dirname "$0")" || exit
echo "========================================"
echo "   AERGIA EXO CLUSTER LAUNCHER"
echo "========================================"

# Set Dashboard Directory to the local build
export DASHBOARD_DIR="$(pwd)/exo_dashboard_build"
echo "Dashboard Assets: $DASHBOARD_DIR"

# Check Python environment
if ! python3 -c "import exo" &> /dev/null; then
    echo "ERROR: 'exo' package is not found in python3."
    echo "Please ensure you have installed it (pip install . in source)."
    read -p "Press enter to exit..."
    exit 1
fi

echo "Starting Exo Node..."
echo "This node is patched to automatically discover:"
echo " - Ryzen Laptop (100.111.220.42)"
echo " - Ryzen Desktop (100.88.136.43)"
echo ""
echo "Press CTRL+C to stop."
echo "========================================"

python3 -m exo
