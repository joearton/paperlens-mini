#!/bin/bash
# Build script for PaperLens Mini Linux Executable
# This script automates the build process using PyInstaller

set -e  # Exit on error

echo "PaperLens Mini Linux Build Script"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."

echo "Project root: $PROJECT_ROOT"
echo ""

# Check if we're in virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}WARNING: Not in a virtual environment${NC}"
    echo "   It's recommended to activate venv first:"
    echo "   source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check system dependencies
echo "Checking system dependencies..."

# Check GTK
if ! pkg-config --exists gtk+-3.0; then
    echo -e "${RED}ERROR: GTK+3 not found${NC}"
    echo "   Install with:"
    echo "   Ubuntu/Debian: sudo apt-get install libgtk-3-dev"
    echo "   Fedora: sudo dnf install gtk3-devel"
    echo "   Arch: sudo pacman -S gtk3"
    exit 1
fi
echo -e "${GREEN}OK: GTK+3 found${NC}"

# Check WebKit2GTK
if ! pkg-config --exists webkit2gtk-4.0; then
    echo -e "${RED}ERROR: WebKit2GTK not found${NC}"
    echo "   Install with:"
    echo "   Ubuntu/Debian: sudo apt-get install libwebkit2gtk-4.0-dev"
    echo "   Fedora: sudo dnf install webkit2gtk3-devel"
    echo "   Arch: sudo pacman -S webkit2gtk"
    exit 1
fi
echo -e "${GREEN}OK: WebKit2GTK found${NC}"

# Check PyInstaller
echo ""
echo "Checking PyInstaller..."
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${RED}ERROR: PyInstaller not found${NC}"
    echo "   Install with: pip install pyinstaller"
    exit 1
fi
echo -e "${GREEN}OK: PyInstaller found${NC}"
echo ""

# Clean previous builds
echo "Cleaning previous builds..."
cd "$PROJECT_ROOT"
rm -rf build dist
echo -e "${GREEN}OK: Cleaned${NC}"
echo ""

# Build the application
echo "Building PaperLensMini..."
echo "   This may take 3-5 minutes..."
echo ""

pyinstaller "$SCRIPT_DIR/paperlens_mini_linux.spec" \
    --distpath "$PROJECT_ROOT/dist" \
    --workpath "$PROJECT_ROOT/build" \
    --clean \
    --noconfirm

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}OK: Build successful!${NC}"
    echo ""
    echo "Application created:"
    echo "   $PROJECT_ROOT/dist/PaperLensMini/"
    echo ""
    
    # Show size
    APP_SIZE=$(du -sh "$PROJECT_ROOT/dist/PaperLensMini" | cut -f1)
    echo "Application size: $APP_SIZE"
    echo ""
    
    # Test if executable exists
    echo "Testing application..."
    if [ -x "$PROJECT_ROOT/dist/PaperLensMini/PaperLensMini" ]; then
        echo -e "${GREEN}OK: Executable created successfully${NC}"
        echo ""
        echo "To run the application:"
        echo "   cd dist/PaperLensMini"
        echo "   ./PaperLensMini"
        echo ""
        echo "To create distributable package:"
        echo "   AppImage: See README.md (Universal)"
        echo "   TAR.GZ:   tar -czf PaperLensMini.tar.gz -C dist PaperLensMini"
        echo "   DEB:      See README.md (Ubuntu/Debian)"
        echo "   RPM:      See README.md (Fedora/RHEL)"
        echo ""
        
        # Ask if user wants to run the app
        read -p "Run the application now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$PROJECT_ROOT/dist/PaperLensMini"
            ./PaperLensMini
        fi
    else
        echo -e "${RED}ERROR: Executable not found or not executable${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${RED}ERROR: Build failed${NC}"
    echo "   Check the error messages above"
    exit 1
fi
