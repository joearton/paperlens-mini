# 📦 PaperLens Mini - Build & Distribution Guide

Welcome to the PaperLens Mini build system! This directory contains everything you need to create standalone executables for **macOS**, **Windows**, and **Linux**.

## 🎯 Quick Start

### Choose Your Platform

| Platform | Directory | Output | Size |
|----------|-----------|--------|------|
| 🍎 **macOS** | [`macos/`](macos/) | `.app` bundle | ~500 MB |
| 🪟 **Windows** | [`windows/`](windows/) | `.exe` file | ~500 MB |
| 🐧 **Linux** | [`linux/`](linux/) | Binary + libs | ~500 MB |

### One-Step Build

```bash
# macOS
cd macos && ./build.sh

# Windows
cd windows && build.bat

# Linux
cd linux && ./build.sh
```

## 📋 What You'll Get

Each platform build includes:

✅ **Self-contained executable**
- Python runtime (no installation required)
- All dependencies bundled
- UI files (HTML, CSS, JavaScript)

✅ **Professional packaging**
- macOS: `.app` bundle + optional `.dmg`
- Windows: `.exe` + optional installer
- Linux: Binary + AppImage/DEB/RPM

✅ **No internet required** for local analysis
- Works offline (except for paper search)

## 🔧 Prerequisites

### All Platforms

1. **Python 3.8 - 3.11** (3.9 recommended)
2. **PyInstaller**: `pip install pyinstaller`
3. **Project dependencies**: `pip install -r requirements.txt`
4. **~2 GB disk space** for build process

### Platform-Specific

#### macOS
- macOS 10.14+ (Mojave or later)
- Xcode Command Line Tools: `xcode-select --install`

#### Windows
- Windows 10/11 (64-bit)
- Visual C++ Redistributable (usually pre-installed)

#### Linux
- Ubuntu 20.04+ / Fedora 34+ / equivalent
- GTK3 and WebKit2GTK libraries
  ```bash
  # Ubuntu/Debian
  sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev
  
  # Fedora
  sudo dnf install gtk3-devel webkit2gtk3-devel
  ```

## 📂 Directory Structure

```
build_scripts/
├── README.md                    # This file
│
├── macos/                       # macOS build files
│   ├── README.md               # Detailed macOS instructions
│   ├── paperlens_mini_macos.spec    # PyInstaller configuration
│   ├── build.sh                # Automated build script
│   └── create_dmg.sh           # DMG creation script
│
├── windows/                     # Windows build files
│   ├── README.md               # Detailed Windows instructions
│   ├── paperlens_mini_windows.spec  # PyInstaller configuration
│   └── build.bat               # Automated build script
│
└── linux/                       # Linux build files
    ├── README.md               # Detailed Linux instructions
    ├── paperlens_mini_linux.spec    # PyInstaller configuration
    └── build.sh                # Automated build script
```

## 🚀 Build Process

### Step-by-Step

1. **Prepare Environment**
   ```bash
   # Create/activate virtual environment
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Navigate to Platform Directory**
   ```bash
   cd build_scripts/macos     # or windows, or linux
   ```

3. **Run Build Script**
   ```bash
   ./build.sh    # macOS/Linux
   build.bat     # Windows
   ```

4. **Find Your Build**
   - Output location: `dist/` in project root
   - Build time: 3-5 minutes
   - Size: ~500 MB (simplified version)

## 📤 Distribution Formats

### macOS

**App Bundle** (Built automatically)
```bash
open dist/PaperLensMini.app
```

**DMG Installer** (Optional)
```bash
cd macos
./create_dmg.sh
# Creates: PaperLensMini-1.0.0-macOS.dmg
```

### Windows

**Standalone EXE** (Built automatically)
```bash
dist\PaperLensMini.exe
```

### Linux

**Directory Bundle** (Built automatically)
```bash
./dist/PaperLensMini/PaperLensMini
```

**AppImage** (Recommended - Universal)
```bash
# See linux/README.md for AppImage creation
# Creates: PaperLensMini-1.0.0-x86_64.AppImage
```

## 🔍 What Gets Bundled

### Included ✅

| Component | Purpose | Size |
|-----------|---------|------|
| Python Runtime | Execute Python code | ~50 MB |
| Dependencies | NumPy, Pandas, Plotly, etc. | ~200 MB |
| UI Files | HTML, CSS, JS | ~5 MB |
| Application Code | Core functionality | ~10 MB |

### Excluded ❌

- AI/ML models (not used in Mini version)
- Deep translation libraries
- Heavy NLP dependencies

## 📊 Build Comparison

| Aspect | macOS | Windows | Linux |
|--------|-------|---------|-------|
| **Output** | `.app` bundle | Single `.exe` | Directory |
| **Size** | ~500 MB | ~500 MB | ~500 MB |
| **Build Time** | 2-4 min | 3-5 min | 2-4 min |
| **Distribution** | `.dmg` | `.exe` | AppImage |
| **Portability** | High | High | Highest |

## 🐛 Common Issues & Solutions

### PyInstaller Not Found
```bash
pip install pyinstaller
```

### Build Fails - Missing Modules
```bash
# Add to hiddenimports in spec file
# Then rebuild with --clean flag
pyinstaller paperlens_mini_windows.spec --clean
```

### "No module named 'pandas.plotting'"
This is fixed in the spec files. If you still see this error:
1. Make sure you're using the latest spec files
2. Clean rebuild: `pyinstaller spec_file.spec --clean --noconfirm`
3. Check that `pandas.plotting` is NOT in the `excludes` list

### Large File Size
This is normal. The bundle includes:
- Python interpreter (~50 MB)
- All libraries (~200 MB)
- UI files (~5 MB)

### App Won't Open

**macOS**: "App is damaged"
```bash
xattr -cr dist/PaperLensMini.app
```

**Windows**: "Windows protected your PC"
```
Click "More info" → "Run anyway"
```

**Linux**: Permission denied
```bash
chmod +x dist/PaperLensMini/PaperLensMini
```

## 🎨 Customization

### Adding Custom Icon

Each platform has specific icon requirements:

**macOS** (`.icns`)
```bash
# Update spec: icon='path/to/icon.icns'
```

**Windows** (`.ico`)
```bash
# Update spec: icon='path/to/icon.ico'
```

**Linux** (`.png`)
```bash
# Used in desktop entry file
```

### Modifying Build Settings

Edit the `.spec` file for your platform:
- `hiddenimports`: Add missing modules
- `excludes`: Remove unused modules
- `datas`: Include additional files
- `upx`: Enable/disable compression

## 🧪 Testing Your Build

### Functional Testing

1. **Launch Application**
   - macOS: `open dist/PaperLensMini.app`
   - Windows: `dist\PaperLensMini.exe`
   - Linux: `dist/PaperLensMini/PaperLensMini`

2. **Test Core Features**
   - ✅ Search for papers
   - ✅ Generate visualizations
   - ✅ Export reports
   - ✅ UI interactions

## 🎯 Production Checklist

Before distributing your build:

- [ ] Test on target platform
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Test on fresh system (if possible)
- [ ] Create installer/package
- [ ] Write installation instructions
- [ ] Include license and credits
- [ ] Create release notes
- [ ] Test distribution format

## 📝 Version Management

When releasing updates:

1. **Update version number** in spec files
2. **Update version** in `app.py`
3. **Rebuild** for all platforms
4. **Test** each build
5. **Create** release packages
6. **Tag** release in git: `git tag v1.0.0`

## 🌟 Success!

You've successfully built PaperLens Mini for distribution! 🎉

Your users can now:
- Install without Python
- Use without internet (for local analysis)
- Run on any supported platform
- Access all features offline

**Next Steps:**
- Share your build with users
- Gather feedback
- Iterate and improve

---

**Built with ❤️ by ArtonLabs**

*"Find the gap, Lead the science"*
