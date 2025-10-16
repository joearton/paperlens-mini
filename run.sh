#!/bin/bash

echo "===================================="
echo "PaperLens Mini Launcher"
echo "===================================="
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo

# Run application
echo "Starting PaperLens Mini..."
echo
python app.py

