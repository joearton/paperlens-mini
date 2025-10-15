#!/usr/bin/env python3
"""
Test script for PaperLens Mini builds
Tests the built applications for basic functionality
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_windows_exe(exe_path):
    """Test Windows executable"""
    print(f"🧪 Testing Windows EXE: {exe_path}")
    
    if not exe_path.exists():
        print(f"❌ EXE not found: {exe_path}")
        return False
    
    try:
        # Start the application
        process = subprocess.Popen([str(exe_path)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Application exited immediately")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing EXE: {e}")
        return False

def test_macos_app(app_path):
    """Test macOS application bundle"""
    print(f"🧪 Testing macOS App: {app_path}")
    
    if not app_path.exists():
        print(f"❌ App bundle not found: {app_path}")
        return False
    
    try:
        # Start the application
        process = subprocess.Popen(['open', str(app_path)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process completed (open command should exit quickly)
        process.wait(timeout=10)
        
        if process.returncode == 0:
            print("✅ Application started successfully")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start application")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing App: {e}")
        return False

def test_linux_binary(binary_path):
    """Test Linux binary"""
    print(f"🧪 Testing Linux Binary: {binary_path}")
    
    if not binary_path.exists():
        print(f"❌ Binary not found: {binary_path}")
        return False
    
    # Make sure it's executable
    os.chmod(binary_path, 0o755)
    
    try:
        # Start the application
        process = subprocess.Popen([str(binary_path)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Application exited immediately")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing binary: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 PaperLens Mini - Build Test Script")
    print("=" * 40)
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist/ directory not found")
        print("   Build the application first using build scripts")
        sys.exit(1)
    
    success_count = 0
    total_count = 0
    
    # Test Windows build
    windows_exe = dist_dir / "PaperLensMini.exe"
    if windows_exe.exists():
        total_count += 1
        if test_windows_exe(windows_exe):
            success_count += 1
    
    # Test macOS build
    macos_app = dist_dir / "PaperLensMini.app"
    if macos_app.exists():
        total_count += 1
        if test_macos_app(macos_app):
            success_count += 1
    
    # Test Linux build
    linux_dir = dist_dir / "PaperLensMini"
    linux_binary = linux_dir / "PaperLensMini"
    if linux_binary.exists():
        total_count += 1
        if test_linux_binary(linux_binary):
            success_count += 1
    
    # Summary
    print("\n" + "=" * 40)
    print(f"🎯 Test Summary: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("🎉 All builds tested successfully!")
        print("\n📦 Your applications are ready for distribution!")
    elif success_count > 0:
        print("⚠️  Some builds passed, some failed")
        print("   Check the error messages above")
    else:
        print("❌ All tests failed")
        print("   Check your build configuration")
        sys.exit(1)

if __name__ == "__main__":
    main()
