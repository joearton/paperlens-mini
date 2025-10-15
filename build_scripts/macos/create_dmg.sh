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

# Check if app exists
APP_PATH="$PROJECT_ROOT/dist/PaperLensMini.app"
if [ ! -d "$APP_PATH" ]; then
    echo -e "${RED}❌ PaperLensMini.app not found${NC}"
    echo "   Build the app first: ./build.sh"
    exit 1
fi

# Set version and filename
VERSION="1.0.0"
DMG_NAME="PaperLensMini-${VERSION}-macOS.dmg"
DMG_PATH="$PROJECT_ROOT/dist/$DMG_NAME"

echo "📦 Creating DMG: $DMG_NAME"
echo ""

# Clean up previous DMG
if [ -f "$DMG_PATH" ]; then
    echo "🧹 Removing previous DMG..."
    rm "$DMG_PATH"
fi

# Create temporary DMG
echo "🔨 Creating temporary DMG..."
TEMP_DMG="$PROJECT_ROOT/dist/temp.dmg"
TEMP_MOUNT="/tmp/PaperLensMini"

# Calculate size needed (app size + overhead)
APP_SIZE=$(du -sk "$APP_PATH" | cut -f1)
DMG_SIZE=$((APP_SIZE + 10000))  # Add 10MB overhead

# Create temporary DMG
hdiutil create -srcfolder "$APP_PATH" -volname "PaperLens Mini" -fs HFS+ -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${DMG_SIZE}k "$TEMP_DMG"

# Mount the temporary DMG
echo "📁 Mounting temporary DMG..."
MOUNT_POINT=$(hdiutil attach -readwrite -noverify -noautoopen "$TEMP_DMG" | grep "Volumes" | cut -f3)

# Create Applications symlink
echo "🔗 Creating Applications symlink..."
ln -s /Applications "$MOUNT_POINT/Applications"

# Set DMG properties
echo "🎨 Setting DMG properties..."
osascript <<EOF
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
        set background picture of theViewOptions to file "System:Library:PrivateFrameworks:LoginUIKit.framework:Versions:A:Frameworks:LoginUICore.framework:Resources:apple_logo_black.png"
        make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
        set position of item "PaperLensMini.app" of container window to {150, 150}
        set position of item "Applications" of container window to {350, 150}
        close
        open
        update without registering applications
        delay 5
        close
    end tell
end tell
EOF

# Unmount the temporary DMG
echo "📁 Unmounting temporary DMG..."
hdiutil detach "$MOUNT_POINT"

# Convert to final compressed DMG
echo "🗜️  Compressing final DMG..."
hdiutil convert "$TEMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_PATH"

# Clean up
echo "🧹 Cleaning up..."
rm "$TEMP_DMG"

# Show final DMG info
if [ -f "$DMG_PATH" ]; then
    echo ""
    echo -e "${GREEN}✅ DMG created successfully!${NC}"
    echo ""
    echo "📦 DMG created:"
    echo "   $DMG_PATH"
    echo ""
    
    # Show size
    DMG_SIZE=$(du -sh "$DMG_PATH" | cut -f1)
    echo "💾 DMG size: $DMG_SIZE"
    echo ""
    
    echo "🚀 To test the DMG:"
    echo "   open '$DMG_PATH'"
    echo ""
    echo "📤 Ready for distribution!"
    echo "   Share the DMG file with users"
    echo ""
    
    # Ask if user wants to open the DMG
    read -p "Open the DMG now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "$DMG_PATH"
    fi
else
    echo -e "${RED}❌ DMG creation failed${NC}"
    exit 1
fi
