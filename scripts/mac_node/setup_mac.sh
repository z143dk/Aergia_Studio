#!/bin/bash
echo "Setting up Aergia Studio for macOS..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please install it (e.g. from python.org or 'brew install python3')."
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Setup complete! You can now run './launch_studio.sh'"
