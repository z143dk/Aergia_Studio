#!/bin/bash
# Aergia Satellite Link
# Double-click to connect this Mac to your Windows PC.

echo "========================================"
echo "🏛️  Aergia Studio - Mac Satellite Link"
echo "========================================"
echo ""

# 1. Check for Exo
if ! command -v exo &> /dev/null; then
    # Try finding it via python module if binary path is missing
    RUN_CMD="python3 -m exo"
else
    RUN_CMD="exo"
fi

echo "Detected Engine: $RUN_CMD"
echo ""

# 2. Ask for Connection Info
echo "Enter the Master Node IP from your Dashboard:"
echo "(Look at the 'Hermes' panel on your Windows PC)"
read -p "IP Address: " MASTER_IP

if [ -z "$MASTER_IP" ]; then
    echo "❌ IP Required."
    exit 1
fi

# 3. Connect
echo ""
echo "🚀 Connecting to Cluster at $MASTER_IP..."
echo "Press Ctrl+C to disconnect."
echo ""

$RUN_CMD --connect-to "$MASTER_IP:52415"

# Keep window open on exit provided it wasn't a manual exit
read -p "Link Closed. Press Enter..."
