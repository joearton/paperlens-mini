#!/bin/bash
# Verify dependencies and build PaperLens Mini for macOS
# This script checks all required dependencies before building

set -e  # Exit on error

echo "🔍 PaperLens Mini - Dependency Verification & Build"
echo "===================================================="
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

# Check if we're in virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${RED}❌ ERROR: Not in a virtual environment${NC}"
    echo "   Please activate venv first:"
    echo "   ${BLUE}source venv/bin/activate${NC}"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ Virtual environment: $VIRTUAL_ENV${NC}"
    echo ""
fi

# Function to check if a Python package is installed
check_package() {
    package_name=$1
    import_name=$2
    
    if python -c "import $import_name" 2>/dev/null; then
        version=$(python -c "import $import_name; print(getattr($import_name, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✅ $package_name${NC} (version: $version)"
        return 0
    else
        echo -e "${RED}❌ $package_name${NC} - NOT INSTALLED"
        return 1
    fi
}

echo "🔍 Checking required dependencies..."
echo ""

# Track missing packages
missing_packages=()

# Core dependencies
echo "📦 Core Dependencies:"
check_package "pywebview" "webview" || missing_packages+=("pywebview")
check_package "requests" "requests" || missing_packages+=("requests")
check_package "beautifulsoup4" "bs4" || missing_packages+=("beautifulsoup4")
check_package "pandas" "pandas" || missing_packages+=("pandas")
check_package "numpy" "numpy" || missing_packages+=("numpy")
echo ""

# Visualization dependencies
echo "📊 Visualization Dependencies:"
check_package "plotly" "plotly" || missing_packages+=("plotly")
check_package "networkx" "networkx" || missing_packages+=("networkx")
check_package "wordcloud" "wordcloud" || missing_packages+=("wordcloud")
check_package "matplotlib" "matplotlib" || missing_packages+=("matplotlib")
echo ""

# Export dependencies
echo "💾 Export Dependencies:"
check_package "openpyxl" "openpyxl" || missing_packages+=("openpyxl")
check_package "fpdf2" "fpdf" || missing_packages+=("fpdf2")
echo ""

# Scholar dependencies
echo "🎓 Scholar Dependencies:"
check_package "scholarly" "scholarly" || missing_packages+=("scholarly")
check_package "fake-useragent" "fake_useragent" || missing_packages+=("fake-useragent")
check_package "lxml" "lxml" || missing_packages+=("lxml")
check_package "Pillow" "PIL" || missing_packages+=("Pillow")
echo ""

# Build dependencies
echo "🔨 Build Dependencies:"
check_package "PyInstaller" "PyInstaller" || missing_packages+=("pyinstaller")
echo ""

# Check if any packages are missing
if [ ${#missing_packages[@]} -ne 0 ]; then
    echo -e "${RED}❌ Missing packages detected!${NC}"
    echo ""
    echo "Missing packages:"
    for pkg in "${missing_packages[@]}"; do
        echo "  - $pkg"
    done
    echo ""
    echo -e "${YELLOW}Would you like to install missing packages?${NC}"
    read -p "Install now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "📥 Installing missing packages..."
        if [ -f "$PROJECT_ROOT/requirements-build.txt" ]; then
            pip install -r "$PROJECT_ROOT/requirements-build.txt"
        else
            pip install -r "$PROJECT_ROOT/requirements.txt"
            pip install pyinstaller
            pip install scholarly networkx wordcloud matplotlib lxml Pillow
        fi
        echo -e "${GREEN}✅ Packages installed${NC}"
        echo ""
    else
        echo ""
        echo -e "${RED}Cannot proceed without required packages.${NC}"
        echo "Install them manually:"
        echo "  ${BLUE}pip install -r requirements-build.txt${NC}"
        echo ""
        exit 1
    fi
else
    echo -e "${GREEN}✅ All dependencies are installed!${NC}"
    echo ""
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
cd "$PROJECT_ROOT"
rm -rf build dist
echo -e "${GREEN}✅ Cleaned${NC}"
echo ""

# Build confirmation
echo -e "${BLUE}Ready to build PaperLensMini.app${NC}"
echo ""
echo "Build configuration:"
echo "  • Python: $(python --version)"
echo "  • PyInstaller: $(python -c 'import PyInstaller; print(PyInstaller.__version__)')"
echo "  • Spec file: $SCRIPT_DIR/paperlens_mini_macos.spec"
echo "  • Output: $PROJECT_ROOT/dist/PaperLensMini.app"
echo ""

read -p "Proceed with build? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "🔨 Building PaperLensMini.app..."
    echo "   This may take 3-5 minutes..."
    echo ""
    
    pyinstaller "$SCRIPT_DIR/paperlens_mini_macos.spec" \
        --distpath "$PROJECT_ROOT/dist" \
        --workpath "$PROJECT_ROOT/build" \
        --clean \
        --noconfirm
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Build successful!${NC}"
        echo ""
        
        # Test if app can be opened
        if [ -d "$PROJECT_ROOT/dist/PaperLensMini.app" ]; then
            APP_SIZE=$(du -sh "$PROJECT_ROOT/dist/PaperLensMini.app" | cut -f1)
            echo "📦 Application created:"
            echo "   Path: $PROJECT_ROOT/dist/PaperLensMini.app"
            echo "   Size: $APP_SIZE"
            echo ""
            
            # Quick verification
            echo "🔍 Verifying build..."
            if [ -f "$PROJECT_ROOT/dist/PaperLensMini.app/Contents/MacOS/PaperLensMini" ]; then
                echo -e "${GREEN}✅ Executable found${NC}"
            else
                echo -e "${RED}❌ Executable not found${NC}"
            fi
            
            if [ -d "$PROJECT_ROOT/dist/PaperLensMini.app/Contents/Resources/ui" ]; then
                echo -e "${GREEN}✅ UI resources found${NC}"
            else
                echo -e "${RED}❌ UI resources not found${NC}"
            fi
            echo ""
            
            echo "🚀 Next steps:"
            echo "   1. Test the app: ${BLUE}open dist/PaperLensMini.app${NC}"
            echo "   2. Create DMG: ${BLUE}cd build_scripts/macos && ./create_dmg.sh${NC}"
            echo ""
            
            # Ask if user wants to open the app
            read -p "Open the application now? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo ""
                echo "🚀 Launching PaperLensMini.app..."
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
        echo ""
        echo "💡 Troubleshooting tips:"
        echo "   1. Make sure all dependencies are installed"
        echo "   2. Check build logs in: $PROJECT_ROOT/build/"
        echo "   3. Try manual build: ${BLUE}pyinstaller build_scripts/macos/paperlens_mini_macos.spec --clean${NC}"
        exit 1
    fi
else
    echo ""
    echo "Build cancelled."
fi

