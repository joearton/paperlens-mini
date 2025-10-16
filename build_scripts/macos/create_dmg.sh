#!/bin/bash
# Create DMG installer for PaperLens Mini macOS Application
# This script creates a professional DMG package for distribution

set -e  # Exit on error

echo "🍎 PaperLens Mini DMG Creator"
echo "============================="
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if app exists
APP_PATH="$PROJECT_ROOT/dist/PaperLensMini.app"
if [ ! -d "$APP_PATH" ]; then
    echo -e "${RED}❌ PaperLensMini.app not found${NC}"
    echo "   Expected: $APP_PATH"
    echo "   Build the app first: ./build.sh"
    exit 1
fi

# Check if hdiutil is available (macOS only)
if ! command_exists hdiutil; then
    echo -e "${RED}❌ hdiutil not found${NC}"
    echo "   This script requires macOS"
    exit 1
fi

# Check if osascript is available
if ! command_exists osascript; then
    echo -e "${RED}❌ osascript not found${NC}"
    echo "   This script requires macOS"
    exit 1
fi

echo -e "${GREEN}✅ Found application bundle${NC}"
echo -e "${GREEN}✅ macOS tools available${NC}"

# Set version and filename
VERSION="1.0.0"
DMG_NAME="PaperLensMini-${VERSION}-macOS.dmg"
DMG_PATH="$PROJECT_ROOT/dist/$DMG_NAME"

echo "📦 Creating DMG: $DMG_NAME"
echo ""

# Clean up previous DMG and temp files
if [ -f "$DMG_PATH" ]; then
    echo -e "${BLUE}🧹 Removing previous DMG...${NC}"
    rm "$DMG_PATH"
fi

# Clean up any existing temp DMG
TEMP_DMG="$PROJECT_ROOT/dist/temp.dmg"
if [ -f "$TEMP_DMG" ]; then
    echo -e "${BLUE}🧹 Removing previous temp DMG...${NC}"
    rm "$TEMP_DMG"
fi

# Clean up any existing mount points
TEMP_MOUNT="/tmp/PaperLensMini"
if [ -d "$TEMP_MOUNT" ]; then
    echo -e "${BLUE}🧹 Cleaning previous mount point...${NC}"
    hdiutil detach "$TEMP_MOUNT" 2>/dev/null || true
    rm -rf "$TEMP_MOUNT"
fi

# Create temporary DMG
echo -e "${BLUE}🔨 Creating temporary DMG...${NC}"

# Calculate size needed (app size + overhead)
APP_SIZE=$(du -sk "$APP_PATH" | cut -f1)
DMG_SIZE=$((APP_SIZE + 10000))  # Add 10MB overhead

echo "   App size: ${APP_SIZE}KB"
echo "   DMG size: ${DMG_SIZE}KB (with overhead)"

# Create temporary DMG
if hdiutil create -srcfolder "$APP_PATH" -volname "PaperLens Mini" -fs HFS+ -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${DMG_SIZE}k "$TEMP_DMG"; then
    echo -e "${GREEN}✅ Temporary DMG created${NC}"
else
    echo -e "${RED}❌ Failed to create temporary DMG${NC}"
    exit 1
fi

# Mount the temporary DMG
echo -e "${BLUE}📁 Mounting temporary DMG...${NC}"
MOUNT_OUTPUT=$(hdiutil attach -readwrite -noverify -noautoopen "$TEMP_DMG" 2>&1)
if [ $? -eq 0 ]; then
    MOUNT_POINT=$(echo "$MOUNT_OUTPUT" | grep "Volumes" | cut -f3)
    echo -e "${GREEN}✅ DMG mounted at: $MOUNT_POINT${NC}"
else
    echo -e "${RED}❌ Failed to mount DMG${NC}"
    echo "   Error: $MOUNT_OUTPUT"
    exit 1
fi

# Create Applications symlink
echo -e "${BLUE}🔗 Creating Applications symlink...${NC}"
if ln -s /Applications "$MOUNT_POINT/Applications"; then
    echo -e "${GREEN}✅ Applications symlink created${NC}"
else
    echo -e "${RED}❌ Failed to create Applications symlink${NC}"
    exit 1
fi

# Set DMG properties
echo -e "${BLUE}🎨 Setting DMG properties...${NC}"
if osascript <<EOF
tell application "Finder"
    tell disk "PaperLens Mini"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {400, 100, 900, 400}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 128
        make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
        set position of item "PaperLensMini.app" of container window to {150, 150}
        set position of item "Applications" of container window to {350, 150}
        close
        open
        update without registering applications
        delay 2
        close
    end tell
end tell
EOF
then
    echo -e "${GREEN}✅ DMG properties set${NC}"
else
    echo -e "${YELLOW}⚠️  Could not set DMG properties, continuing anyway${NC}"
fi

# Unmount the temporary DMG
echo -e "${BLUE}📁 Unmounting temporary DMG...${NC}"
if hdiutil detach "$MOUNT_POINT"; then
    echo -e "${GREEN}✅ DMG unmounted${NC}"
else
    echo -e "${RED}❌ Failed to unmount DMG${NC}"
    exit 1
fi

# Convert to final compressed DMG
echo -e "${BLUE}🗜️  Compressing final DMG...${NC}"
if hdiutil convert "$TEMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_PATH"; then
    echo -e "${GREEN}✅ Final DMG created${NC}"
else
    echo -e "${RED}❌ Failed to create final DMG${NC}"
    exit 1
fi

# Clean up
echo -e "${BLUE}🧹 Cleaning up...${NC}"
if [ -f "$TEMP_DMG" ]; then
    rm "$TEMP_DMG"
    echo -e "${GREEN}✅ Temporary files cleaned${NC}"
fi

# Show final DMG info
echo ""
echo -e "${BLUE}🔍 Verifying final DMG...${NC}"

if [ -f "$DMG_PATH" ]; then
    echo -e "${GREEN}✅ DMG created successfully!${NC}"
    
    # Show size
    DMG_SIZE=$(du -sh "$DMG_PATH" | cut -f1)
    echo -e "${GREEN}📦 DMG size: $DMG_SIZE${NC}"
    
    # Verify DMG integrity
    echo -e "${BLUE}🔍 Verifying DMG integrity...${NC}"
    if hdiutil verify "$DMG_PATH" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ DMG integrity verified${NC}"
    else
        echo -e "${YELLOW}⚠️  DMG integrity check failed${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 DMG Creation Complete!${NC}"
    echo ""
    echo "📦 DMG created:"
    echo "   $DMG_PATH"
    echo ""
    echo "🚀 To test the DMG:"
    echo "   open '$DMG_PATH'"
    echo ""
    echo "📤 Ready for distribution!"
    echo "   Share the DMG file with users"
    echo ""
    echo "📋 DMG Features:"
    echo "   ✅ Professional layout with Applications folder"
    echo "   ✅ Proper icon positioning"
    echo "   ✅ Compressed for smaller file size"
    echo "   ✅ Ready for macOS installation"
    echo ""
    
    # Ask if user wants to open the DMG
    read -p "🧪 Test the DMG now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Opening DMG..."
        open "$DMG_PATH"
        echo -e "${GREEN}✅ DMG opened${NC}"
        echo "Check if the DMG mounts and shows the app correctly"
    fi
    
else
    echo -e "${RED}❌ DMG creation failed${NC}"
    echo "   Expected: $DMG_PATH"
    echo "   Check error messages above"
    exit 1
fi
