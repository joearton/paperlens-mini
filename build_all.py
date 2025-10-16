#!/usr/bin/env python3
"""
Master build script for Sintesa
Builds for all platforms (Windows, macOS, Linux)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_platform():
    """Get current platform"""
    return platform.system().lower()

def run_command(command, cwd=None):
    """Run command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            return True
        else:
            print(f"❌ {command}")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {command}")
        print(f"   Exception: {e}")
        return False

def check_requirements():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("[OK] PyInstaller is installed")
        return True
    except ImportError:
        print("[ERROR] PyInstaller not found")
        print("   Install with: pip install pyinstaller")
        return False

def build_windows():
    """Build for Windows"""
    print("\nBuilding for Windows...")
    script_path = Path("build_scripts/windows/build.bat")
    if script_path.exists():
        return run_command(str(script_path))
    else:
        print(f"[ERROR] Build script not found: {script_path}")
        return False

def build_macos():
    """Build for macOS"""
    print("\nBuilding for macOS...")
    script_path = Path("build_scripts/macos/build.sh")
    if script_path.exists():
        # Make script executable
        os.chmod(script_path, 0o755)
        return run_command(f"./{script_path}")
    else:
        print(f"[ERROR] Build script not found: {script_path}")
        return False

def build_linux():
    """Build for Linux"""
    print("\nBuilding for Linux...")
    script_path = Path("build_scripts/linux/build.sh")
    if script_path.exists():
        # Make script executable
        os.chmod(script_path, 0o755)
        return run_command(f"./{script_path}")
    else:
        print(f"[ERROR] Build script not found: {script_path}")
        return False

def main():
    """Main build function"""
    print("Sintesa - Multi-Platform Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("[ERROR] app.py not found. Run this script from the project root.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    current_platform = get_platform()
    print(f"Current platform: {current_platform}")
    
    # Ask user which platforms to build
    print("\nWhich platforms would you like to build?")
    print("1. Current platform only")
    print("2. All platforms")
    print("3. Windows only")
    print("4. macOS only")
    print("5. Linux only")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    success_count = 0
    total_count = 0
    
    if choice in ["1", "2"] or (choice == "3" and current_platform == "windows") or (choice == "4" and current_platform == "darwin") or (choice == "5" and current_platform == "linux"):
        if current_platform == "windows":
            total_count += 1
            if build_windows():
                success_count += 1
        elif current_platform == "darwin":
            total_count += 1
            if build_macos():
                success_count += 1
        elif current_platform == "linux":
            total_count += 1
            if build_linux():
                success_count += 1
    
    if choice == "2":
        # Build all platforms (if possible)
        if current_platform != "windows":
            total_count += 1
            if build_windows():
                success_count += 1
        
        if current_platform != "darwin":
            total_count += 1
            if build_macos():
                success_count += 1
        
        if current_platform != "linux":
            total_count += 1
            if build_linux():
                success_count += 1
    
    if choice == "3":
        total_count += 1
        if build_windows():
            success_count += 1
    
    if choice == "4":
        total_count += 1
        if build_macos():
            success_count += 1
    
    if choice == "5":
        total_count += 1
        if build_linux():
            success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Build Summary: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("[SUCCESS] All builds completed successfully!")
        print("\nBuilt applications:")
        
        # List built applications
        dist_dir = Path("dist")
        if dist_dir.exists():
            for item in dist_dir.iterdir():
                if item.is_file() and item.suffix in [".exe", ".dmg", ".AppImage"]:
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"   {item.name} ({size_mb:.1f} MB)")
                elif item.is_dir() and item.name.startswith("Sintesa"):
                    print(f"   {item.name}/")
    else:
        print("[WARNING] Some builds failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
