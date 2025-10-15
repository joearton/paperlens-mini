#!/bin/bash
# Build script for PaperLens Mini macOS Application
# This script automates the build process using PyInstaller

set -e  # Exit on error

echo "🍎 PaperLens Mini macOS Build Script"
echo "====================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."

echo "📁 Project root: $PROJECT_ROOT"
echo ""

# Check if we're in virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Not in a virtual environment${NC}"
    echo "   It's recommended to activate venv first:"
    echo "   source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check PyInstaller
echo "🔍 Checking PyInstaller..."
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${RED}❌ PyInstaller not found${NC}"
    echo "   Install with: pip install pyinstaller"
    exit 1
fi
echo -e "${GREEN}✅ PyInstaller found${NC}"
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
cd "$PROJECT_ROOT"
rm -rf build dist
echo -e "${GREEN}✅ Cleaned${NC}"
echo ""

# Build the application
echo "🔨 Building PaperLensMini.app..."
echo "   This may take 3-5 minutes..."
echo ""

pyinstaller "$SCRIPT_DIR/paperlens_mini_macos.spec" \
    --clean \
    --noconfirm

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo ""
    echo "📦 Application created:"
    echo "   $PROJECT_ROOT/dist/PaperLensMini.app"
    echo ""
    
    # Show size
    APP_SIZE=$(du -sh "$PROJECT_ROOT/dist/PaperLensMini.app" | cut -f1)
    echo "💾 Application size: $APP_SIZE"
    echo ""
    
    # Test if app can be opened
    echo "🧪 Testing application..."
    if [ -d "$PROJECT_ROOT/dist/PaperLensMini.app" ]; then
        echo -e "${GREEN}✅ Application bundle created successfully${NC}"
        echo ""
        echo "🚀 To run the application:"
        echo "   open dist/PaperLensMini.app"
        echo ""
        echo "📤 To create DMG for distribution:"
        echo "   cd build_scripts/macos"
        echo "   ./create_dmg.sh"
        echo ""
        
        # Ask if user wants to open the app
        read -p "Open the application now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "$PROJECT_ROOT/dist/PaperLensMini.app"
        fi
    else
        echo -e "${RED}❌ Application bundle not found${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${RED}❌ Build failed${NC}"
    echo "   Check the error messages above"
    exit 1
fi
