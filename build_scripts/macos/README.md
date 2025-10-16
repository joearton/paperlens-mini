# 🍎 macOS Build Guide - Sintesa

This guide will help you build a standalone macOS application for Sintesa.

## 📋 Prerequisites

### Required Software

1. **macOS 10.14+** (Mojave or later)
2. **Python 3.8-3.11** (3.9 recommended)
   ```bash
   # Using Homebrew (recommended)
   brew install python@3.9
   
   # Or download from python.org
   ```

3. **Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```

4. **PyInstaller**
   ```bash
   pip install pyinstaller
   ```

## 🚀 Quick Build

### Option 1: Master Script (Recommended)
```bash
# 1. Navigate to project directory
cd path/to/sintesa

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run master build script
cd build_scripts/macos
./master_build.sh
```

### Option 2: Automated Build
```bash
# 1. Navigate to project directory
cd path/to/sintesa

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run verification and build script
cd build_scripts/macos
./verify_and_build.sh
```

### Option 3: Manual Build
```bash
# 1. Navigate to project directory
cd path/to/sintesa

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements-build.txt

# 4. Run build script
cd build_scripts/macos
./build.sh
```

## 🛠️ Available Scripts

### Master Scripts
- **`master_build.sh`** - Main orchestration script with menu options
- **`verify_and_build.sh`** - Automated dependency verification and build

### Individual Scripts
- **`build.sh`** - Basic app build (requires dependencies pre-installed)
- **`create_dmg.sh`** - Create DMG installer from existing app

### Script Features
- ✅ **Error handling** - Comprehensive error checking and reporting
- ✅ **Dependency verification** - Automatic package checking and installation
- ✅ **Progress feedback** - Clear status updates and emoji indicators
- ✅ **Interactive prompts** - User-friendly confirmation dialogs
- ✅ **Post-build verification** - Automatic testing and validation
- ✅ **Cleanup** - Automatic temporary file cleanup

## 📦 What You Get

- **App Bundle**: `dist/Sintesa.app`
- **Size**: ~500 MB (includes Python runtime and all dependencies)
- **Standalone**: No Python installation required on target machines

## 🧪 Testing Your Build

1. **Run the application**
   ```bash
   open dist/Sintesa.app
   ```

2. **Test core features**
   - ✅ Search for papers
   - ✅ Generate visualizations
   - ✅ Export reports
   - ✅ UI interactions

## 📤 Distribution Options

### Option 1: App Bundle
- Share the `.app` folder directly
- Users can drag to Applications folder

### Option 2: DMG Installer
```bash
cd build_scripts/macos
chmod +x create_dmg.sh
./create_dmg.sh
```
Creates: `Sintesa-1.0.0-macOS.dmg`

### Option 3: ZIP Package
```bash
zip -r Sintesa-macOS.zip dist/Sintesa.app
```

## 🔧 Troubleshooting

### "App is damaged and can't be opened"
```bash
xattr -cr dist/Sintesa.app
```

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### "Permission denied"
```bash
chmod +x build.sh
chmod +x create_dmg.sh
```

### Build fails with "Module not found"

**Common missing modules:**
- `ModuleNotFoundError: No module named 'fpdf'`
  - Make sure `fpdf2` is installed: `pip install fpdf2`
  - Already added to hiddenimports in spec file

- `scholarly library not installed`
  - Install: `pip install scholarly`
  - Already added to hiddenimports in spec file

- `NetworkX not available`
  - Install: `pip install networkx`
  - Already added to hiddenimports in spec file

- `WordCloud not available`
  - Install: `pip install wordcloud`
  - Already added to hiddenimports in spec file

**Solution:**
1. Install all build dependencies:
   ```bash
   pip install -r requirements-build.txt
   ```
2. Clean rebuild:
   ```bash
   pyinstaller sintesa_macos.spec --clean --noconfirm
   ```
3. If still failing, add missing modules to `hiddenimports` in spec file

### Large file size
- Normal for PyInstaller builds (~500 MB)
- Includes Python runtime and all dependencies
- Use `excludes` in spec file to remove unused modules

## 🎨 Customization

### Adding Icon
1. Create `.icns` file (512x512 pixels recommended)
   ```bash
   # Convert PNG to ICNS
   iconutil -c icns icon.iconset
   ```
2. Update spec file:
   ```python
   icon='path/to/your/icon.icns'
   ```

### Reducing Size
Edit `sintesa_macos.spec`:
```python
excludes = [
    'matplotlib',    # Remove if not needed
    'scipy',         # Remove if not needed
    'sklearn',       # Remove if not needed
    # Add other unused modules
]
```

### Code Signing (Optional)
```bash
# Sign the app
codesign --deep --force --sign "Developer ID Application: Your Name" dist/Sintesa.app

# Verify signature
codesign --verify --verbose dist/Sintesa.app
```

### Notarization (Optional)
For distribution outside App Store:
```bash
# Create ZIP for notarization
ditto -c -k --keepParent dist/Sintesa.app Sintesa.zip

# Submit for notarization
xcrun notarytool submit Sintesa.zip --wait --apple-id "your@email.com" --password "app-password" --team-id "TEAM_ID"
```

## 📊 Build Performance

| Aspect | Time | Size |
|--------|------|------|
| **Build Time** | 2-4 minutes | - |
| **Final Size** | - | ~500 MB |
| **Startup Time** | 2-3 seconds | - |

## 🔒 Security Considerations

### Gatekeeper
- Unsigned apps will show security warning
- Users need to right-click → Open (first time)
- Code signing eliminates this warning

### Notarization
- Required for macOS 10.15+ distribution
- Prevents "app is damaged" errors
- Requires Apple Developer Account ($99/year)

## 🆘 Getting Help

### Common Issues
1. **Check build output** for error messages
2. **Run from Terminal** to see detailed errors
3. **Check PyInstaller logs** in `build/` directory

### Support
- GitHub Issues: Report bugs or ask questions
- PyInstaller Docs: [pyinstaller.org](https://pyinstaller.org)

## ✅ Success Checklist

Before distributing:
- [ ] Test on macOS 10.14+
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Test on fresh system (if possible)
- [ ] Create DMG installer
- [ ] Consider code signing
- [ ] Write installation instructions

---

**Built with ❤️ by ArtonLabs**
