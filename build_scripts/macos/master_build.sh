#!/bin/bash
# Master Build Script for PaperLens Mini macOS
# This script orchestrates the complete build and packaging process

set -e  # Exit on error

echo "🚀 PaperLens Mini Master Build Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 Script directory: $SCRIPT_DIR"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print section header
print_section() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}════════════════════════════════════════${NC}"
    echo ""
}

# Function to run script with error handling
run_script() {
    local script_name="$1"
    local script_path="$2"
    local description="$3"
    
    echo -e "${BLUE}🔄 Running: $description${NC}"
    echo "   Script: $script_name"
    echo ""
    
    if [ -f "$script_path" ]; then
        chmod +x "$script_path"
        if "$script_path"; then
            echo -e "${GREEN}✅ $description completed successfully${NC}"
        else
            echo -e "${RED}❌ $description failed${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Script not found: $script_path${NC}"
        exit 1
    fi
}

# Check prerequisites
print_section "🔍 PREREQUISITES CHECK"

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

# Check macOS tools
echo ""
echo -e "${BLUE}🔍 Checking macOS tools...${NC}"

if command_exists hdiutil; then
    echo -e "${GREEN}✅ hdiutil found${NC}"
else
    echo -e "${RED}❌ hdiutil not found${NC}"
    echo "   This script requires macOS"
    exit 1
fi

if command_exists osascript; then
    echo -e "${GREEN}✅ osascript found${NC}"
else
    echo -e "${RED}❌ osascript not found${NC}"
    echo "   This script requires macOS"
    exit 1
fi

# Check if verify_and_build.sh exists
if [ -f "$SCRIPT_DIR/verify_and_build.sh" ]; then
    echo -e "${GREEN}✅ verify_and_build.sh found${NC}"
else
    echo -e "${RED}❌ verify_and_build.sh not found${NC}"
    echo "   Please ensure all build scripts are present"
    exit 1
fi

echo ""

# Main menu
print_section "📋 BUILD OPTIONS"

echo "Choose build option:"
echo ""
echo "1) 🔍 Verify dependencies and build app only"
echo "2) 🔨 Build app and create DMG installer"
echo "3) 📦 Create DMG from existing app"
echo "4) 🧪 Test existing app"
echo "5) 🧹 Clean everything and start fresh"
echo "6) ❌ Exit"
echo ""

read -p "Enter your choice (1-6): " -n 1 -r
echo
echo ""

case $REPLY in
    1)
        print_section "🔍 VERIFY AND BUILD APP"
        run_script "verify_and_build.sh" "$SCRIPT_DIR/verify_and_build.sh" "Dependency verification and app build"
        ;;
    2)
        print_section "🔍 VERIFY AND BUILD APP"
        run_script "verify_and_build.sh" "$SCRIPT_DIR/verify_and_build.sh" "Dependency verification and app build"
        
        print_section "📦 CREATE DMG INSTALLER"
        run_script "create_dmg.sh" "$SCRIPT_DIR/create_dmg.sh" "DMG installer creation"
        ;;
    3)
        APP_PATH="$PROJECT_ROOT/dist/PaperLensMini.app"
        if [ ! -d "$APP_PATH" ]; then
            echo -e "${RED}❌ PaperLensMini.app not found${NC}"
            echo "   Expected: $APP_PATH"
            echo "   Build the app first or choose option 1 or 2"
            exit 1
        fi
        
        print_section "📦 CREATE DMG INSTALLER"
        run_script "create_dmg.sh" "$SCRIPT_DIR/create_dmg.sh" "DMG installer creation"
        ;;
    4)
        APP_PATH="$PROJECT_ROOT/dist/PaperLensMini.app"
        if [ ! -d "$APP_PATH" ]; then
            echo -e "${RED}❌ PaperLensMini.app not found${NC}"
            echo "   Expected: $APP_PATH"
            echo "   Build the app first or choose option 1 or 2"
            exit 1
        fi
        
        print_section "🧪 TESTING APP"
        echo -e "${BLUE}🧪 Testing PaperLensMini.app...${NC}"
        echo "Opening application..."
        open "$APP_PATH"
        echo -e "${GREEN}✅ Application launched${NC}"
        echo "Check if the app starts without errors"
        ;;
    5)
        print_section "🧹 CLEANING"
        echo -e "${BLUE}🧹 Cleaning all build artifacts...${NC}"
        
        cd "$PROJECT_ROOT"
        
        if [ -d "build" ]; then
            rm -rf build
            echo -e "${GREEN}✅ Removed build directory${NC}"
        fi
        
        if [ -d "dist" ]; then
            rm -rf dist
            echo -e "${GREEN}✅ Removed dist directory${NC}"
        fi
        
        if [ -d "__pycache__" ]; then
            rm -rf __pycache__
            echo -e "${GREEN}✅ Removed __pycache__ directory${NC}"
        fi
        
        # Clean Python cache files
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        
        echo -e "${GREEN}✅ Clean completed${NC}"
        echo ""
        echo "Ready for fresh build. Run this script again and choose option 1 or 2."
        ;;
    6)
        echo -e "${GREEN}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac

# Final summary
print_section "🎉 BUILD COMPLETE"

echo -e "${GREEN}🎉 Build process completed successfully!${NC}"
echo ""

# Show what was created
if [ -d "$PROJECT_ROOT/dist/PaperLensMini.app" ]; then
    APP_SIZE=$(du -sh "$PROJECT_ROOT/dist/PaperLensMini.app" | cut -f1)
    echo -e "${GREEN}📱 Application:${NC}"
    echo "   $PROJECT_ROOT/dist/PaperLensMini.app ($APP_SIZE)"
fi

DMG_FILES=$(find "$PROJECT_ROOT/dist" -name "*.dmg" 2>/dev/null | wc -l)
if [ $DMG_FILES -gt 0 ]; then
    echo -e "${GREEN}📦 DMG Installer:${NC}"
    for dmg in "$PROJECT_ROOT/dist"/*.dmg; do
        if [ -f "$dmg" ]; then
            DMG_SIZE=$(du -sh "$dmg" | cut -f1)
            echo "   $dmg ($DMG_SIZE)"
        fi
    done
fi

echo ""
echo "🚀 Next steps:"
echo "   1. Test the application thoroughly"
echo "   2. Verify all features work correctly"
echo "   3. Share the DMG with users"
echo ""
echo -e "${GREEN}✨ Happy building!${NC}"
