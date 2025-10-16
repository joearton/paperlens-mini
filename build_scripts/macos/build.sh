#!/bin/bash
# Build script for PaperLens Mini macOS Application
# This script automates the build process using PyInstaller

set -e  # Exit on error

echo "🔨 PaperLens Mini macOS Build Script"
echo "====================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."

echo "📁 Project root: $PROJECT_ROOT"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if package is installed
package_installed() {
    python -c "import $1" 2>/dev/null
}

# Check if we're in virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠️  WARNING: Not in a virtual environment${NC}"
    echo "   It's recommended to activate venv first:"
    echo "   source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Aborted. Please activate venv and try again.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Virtual environment active: ${VIRTUAL_ENV}${NC}"
fi
echo ""

# Check critical dependencies
echo -e "${BLUE}🔍 Checking dependencies...${NC}"

# Check PyInstaller
if ! command_exists pyinstaller; then
    echo -e "${RED}❌ PyInstaller not found${NC}"
    echo "   Install with: pip install pyinstaller"
    exit 1
fi
echo -e "${GREEN}✅ PyInstaller found${NC}"

# Check critical Python packages
critical_packages=("pywebview" "pandas" "numpy" "requests" "plotly")
missing_packages=()

for package in "${critical_packages[@]}"; do
    if package_installed "$package"; then
        echo -e "${GREEN}✅ $package installed${NC}"
    else
        echo -e "${RED}❌ $package missing${NC}"
        missing_packages+=("$package")
    fi
done

# Check if requirements-build.txt exists
if [ -f "$PROJECT_ROOT/requirements-build.txt" ]; then
    echo -e "${GREEN}✅ requirements-build.txt found${NC}"
else
    echo -e "${YELLOW}⚠️  requirements-build.txt not found${NC}"
    echo "   Some dependencies might be missing"
fi

# Handle missing packages
if [ ${#missing_packages[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Missing critical packages: ${missing_packages[*]}${NC}"
    echo ""
    echo "To install missing dependencies:"
    echo "   pip install -r requirements-build.txt"
    echo ""
    read -p "Install missing packages now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing dependencies..."
        pip install -r "$PROJECT_ROOT/requirements-build.txt"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
        else
            echo -e "${RED}❌ Failed to install dependencies${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Cannot continue without required packages${NC}"
        exit 1
    fi
fi

echo ""

# Clean previous builds
echo -e "${BLUE}🧹 Cleaning previous builds...${NC}"
cd "$PROJECT_ROOT"

if [ -d "build" ] || [ -d "dist" ]; then
    rm -rf build dist
    echo -e "${GREEN}✅ Cleaned previous builds${NC}"
else
    echo -e "${GREEN}✅ No previous builds to clean${NC}"
fi
echo ""

# Verify spec file exists
if [ ! -f "$SCRIPT_DIR/paperlens_mini_macos.spec" ]; then
    echo -e "${RED}❌ Spec file not found: $SCRIPT_DIR/paperlens_mini_macos.spec${NC}"
    exit 1
fi

# Build the application
echo -e "${BLUE}🔨 Building PaperLensMini.app...${NC}"
echo "   This may take 3-5 minutes..."
echo "   Using spec file: $SCRIPT_DIR/paperlens_mini_macos.spec"
echo ""

# Build with error handling
if pyinstaller "$SCRIPT_DIR/paperlens_mini_macos.spec" \
    --distpath "$PROJECT_ROOT/dist" \
    --workpath "$PROJECT_ROOT/build" \
    --clean \
    --noconfirm; then
    echo -e "${GREEN}✅ Build command completed${NC}"
else
    echo -e "${RED}❌ Build command failed${NC}"
    echo "Check the error messages above"
    exit 1
fi

# Post-build verification
echo ""
echo -e "${BLUE}🔍 Verifying build...${NC}"

APP_PATH="$PROJECT_ROOT/dist/PaperLensMini.app"

if [ -d "$APP_PATH" ]; then
    echo -e "${GREEN}✅ Application bundle created successfully${NC}"
    
    # Show size
    APP_SIZE=$(du -sh "$APP_PATH" | cut -f1)
    echo -e "${GREEN}📦 Application size: $APP_SIZE${NC}"
    
    # Check if executable exists
    EXECUTABLE_PATH="$APP_PATH/Contents/MacOS/PaperLensMini"
    if [ -f "$EXECUTABLE_PATH" ]; then
        echo -e "${GREEN}✅ Executable found${NC}"
        
        # Check executable permissions
        if [ -x "$EXECUTABLE_PATH" ]; then
            echo -e "${GREEN}✅ Executable has correct permissions${NC}"
        else
            echo -e "${YELLOW}⚠️  Executable permissions may need fixing${NC}"
            chmod +x "$EXECUTABLE_PATH"
        fi
    else
        echo -e "${RED}❌ Executable not found${NC}"
        exit 1
    fi
    
    # Check if Info.plist exists
    INFO_PLIST="$APP_PATH/Contents/Info.plist"
    if [ -f "$INFO_PLIST" ]; then
        echo -e "${GREEN}✅ Info.plist found${NC}"
    else
        echo -e "${RED}❌ Info.plist not found${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Build successful!${NC}"
    echo ""
    echo "📱 Application created:"
    echo "   $APP_PATH"
    echo ""
    echo "🚀 To run the application:"
    echo "   open dist/PaperLensMini.app"
    echo ""
    echo "📦 To create DMG for distribution:"
    echo "   cd build_scripts/macos"
    echo "   ./create_dmg.sh"
    echo ""
    
    # Ask if user wants to open the app
    read -p "🧪 Test the application now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Opening application..."
        open "$APP_PATH"
        echo -e "${GREEN}✅ Application launched${NC}"
        echo "Check if the app starts without errors"
    fi
    
    # Ask if user wants to create DMG
    echo ""
    read -p "📦 Create DMG installer now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating DMG installer..."
        cd "$SCRIPT_DIR"
        ./create_dmg.sh
    fi
    
else
    echo -e "${RED}❌ Application bundle not found${NC}"
    echo "   Expected: $APP_PATH"
    echo "   Check build logs for errors"
    exit 1
fi
