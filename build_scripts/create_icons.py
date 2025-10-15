#!/usr/bin/env python3
"""
Icon creation script for PaperLens Mini
Creates platform-specific icons from a base PNG image
"""

import os
import sys
from pathlib import Path
from PIL import Image

def create_ico(input_path, output_path, sizes=[16, 32, 48, 64, 128, 256]):
    """Create ICO file for Windows"""
    try:
        # Load the base image
        img = Image.open(input_path)
        
        # Create list of images in different sizes
        images = []
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Save as ICO
        images[0].save(output_path, format='ICO', sizes=[(img.width, img.height) for img in images])
        print(f"[OK] Created ICO: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create ICO: {e}")
        return False

def create_icns(input_path, output_path):
    """Create ICNS file for macOS"""
    try:
        # Load the base image
        img = Image.open(input_path)
        
        # Create iconset directory
        iconset_dir = output_path.with_suffix('.iconset')
        iconset_dir.mkdir(exist_ok=True)
        
        # Create different sizes for ICNS
        sizes = [
            (16, 'icon_16x16.png'),
            (32, 'icon_16x16@2x.png'),
            (32, 'icon_32x32.png'),
            (64, 'icon_32x32@2x.png'),
            (128, 'icon_128x128.png'),
            (256, 'icon_128x128@2x.png'),
            (256, 'icon_256x256.png'),
            (512, 'icon_256x256@2x.png'),
            (512, 'icon_512x512.png'),
            (1024, 'icon_512x512@2x.png'),
        ]
        
        for size, filename in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(iconset_dir / filename)
        
        # Convert to ICNS using iconutil (macOS only)
        if sys.platform == 'darwin':
            import subprocess
            result = subprocess.run(['iconutil', '-c', 'icns', str(iconset_dir)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Move the created ICNS file
                icns_file = iconset_dir.with_suffix('.icns')
                if icns_file.exists():
                    icns_file.rename(output_path)
                    # Clean up iconset directory
                    import shutil
                    shutil.rmtree(iconset_dir)
                    print(f"[OK] Created ICNS: {output_path}")
                    return True
                else:
                    print(f"[ERROR] ICNS file not created")
                    return False
            else:
                print(f"[ERROR] iconutil failed: {result.stderr}")
                return False
        else:
            print(f"[WARNING] ICNS creation requires macOS. Created iconset at: {iconset_dir}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Failed to create ICNS: {e}")
        return False

def create_linux_icons(input_path, output_dir):
    """Create PNG icons for Linux"""
    try:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Load the base image
        img = Image.open(input_path)
        
        # Create different sizes for Linux
        sizes = [16, 24, 32, 48, 64, 96, 128, 192, 256, 512]
        
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(output_dir / f"paperlens_mini_{size}x{size}.png")
        
        print(f"[OK] Created Linux icons in: {output_dir}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create Linux icons: {e}")
        return False

def main():
    """Main function"""
    print("PaperLens Mini - Icon Creation Script")
    print("=" * 40)
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("[ERROR] PIL (Pillow) not found")
        print("   Install with: pip install Pillow")
        sys.exit(1)
    
    # Look for base icon
    base_icon_paths = [
        Path("images/logo-with-text.png"),
        Path("images/logo.png"),
        Path("ui/images/logo-with-text.png"),
        Path("ui/images/logo.png"),
        Path("logo.png"),
    ]
    
    base_icon = None
    for path in base_icon_paths:
        if path.exists():
            base_icon = path
            break
    
    if not base_icon:
        print("[ERROR] No base icon found. Please provide a PNG image.")
        print("   Place your icon as one of:")
        for path in base_icon_paths:
            print(f"   - {path}")
        sys.exit(1)
    
    print(f"Using base icon: {base_icon}")
    
    # Create output directories
    windows_dir = Path("build_scripts/windows")
    macos_dir = Path("build_scripts/macos")
    linux_dir = Path("build_scripts/linux")
    
    success_count = 0
    total_count = 0
    
    # Create Windows ICO
    total_count += 1
    windows_ico = windows_dir / "PaperLensMini.ico"
    if create_ico(base_icon, windows_ico):
        success_count += 1
    
    # Create macOS ICNS
    total_count += 1
    macos_icns = macos_dir / "PaperLensMini.icns"
    if create_icns(base_icon, macos_icns):
        success_count += 1
    
    # Create Linux PNGs
    total_count += 1
    linux_icons_dir = linux_dir / "icons"
    if create_linux_icons(base_icon, linux_icons_dir):
        success_count += 1
    
    # Summary
    print("\n" + "=" * 40)
    print(f"Icon Creation Summary: {success_count}/{total_count} successful")
    
    if success_count > 0:
        print("\nCreated files:")
        if windows_ico.exists():
            print(f"   Windows: {windows_ico}")
        if macos_icns.exists():
            print(f"   macOS: {macos_icns}")
        if linux_icons_dir.exists():
            print(f"   Linux: {linux_icons_dir}/")
        
        print("\nNext steps:")
        print("   1. Update spec files to use the new icons")
        print("   2. Rebuild your applications")
        print("   3. Test the icons in your built apps")
    else:
        print("[ERROR] No icons were created successfully")

if __name__ == "__main__":
    main()
