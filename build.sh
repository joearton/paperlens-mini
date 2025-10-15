#!/bin/bash
# Quick build script for PaperLens Mini (macOS/Linux)
echo "Building PaperLens Mini..."

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 macOS detected"
    cd build_scripts/macos
    chmod +x build.sh
    ./build.sh
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Linux detected"
    cd build_scripts/linux
    chmod +x build.sh
    ./build.sh
else
    echo "❌ Unsupported platform: $OSTYPE"
    exit 1
fi
