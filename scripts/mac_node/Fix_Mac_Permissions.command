#!/bin/bash
# Aergia Permission Fixer
# Double-click this if your dashboard won't open!

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🔧 Fixing Aergia Permissions..."
echo "Target Directory: $DIR"

# Fix permissions
chmod +x *.command *.sh
echo "✅ Made scripts executable"

# Remove quarantine (ignoring errors if not present)
xattr -d com.apple.quarantine *.command *.sh 2>/dev/null || true
echo "✅ Removed macOS quarantine restrictions"

echo "============================================"
echo "🎉 ALL FIXED! You can now launch the Dashboard."
echo "============================================"
echo "(Window will close in 5 seconds)"
sleep 5
