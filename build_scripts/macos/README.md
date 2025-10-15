# 🍎 macOS Build Guide - PaperLens Mini

This guide will help you build a standalone macOS application for PaperLens Mini.

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

1. **Open Terminal**
2. **Navigate to project directory**
   ```bash
   cd path/to/paperlens-mini
   ```
3. **Activate virtual environment** (if using one)
   ```bash
   source venv/bin/activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```
5. **Run build script**
   ```bash
   cd build_scripts/macos
   chmod +x build.sh
   ./build.sh
   ```

## 📦 What You Get

- **App Bundle**: `dist/PaperLensMini.app`
- **Size**: ~500 MB (includes Python runtime and all dependencies)
- **Standalone**: No Python installation required on target machines

## 🧪 Testing Your Build

1. **Run the application**
   ```bash
   open dist/PaperLensMini.app
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
Creates: `PaperLensMini-1.0.0-macOS.dmg`

### Option 3: ZIP Package
```bash
zip -r PaperLensMini-macOS.zip dist/PaperLensMini.app
```

## 🔧 Troubleshooting

### "App is damaged and can't be opened"
```bash
xattr -cr dist/PaperLensMini.app
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
- Add missing modules to `hiddenimports` in spec file
- Rebuild: `pyinstaller paperlens_mini_macos.spec --clean`

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
Edit `paperlens_mini_macos.spec`:
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
codesign --deep --force --sign "Developer ID Application: Your Name" dist/PaperLensMini.app

# Verify signature
codesign --verify --verbose dist/PaperLensMini.app
```

### Notarization (Optional)
For distribution outside App Store:
```bash
# Create ZIP for notarization
ditto -c -k --keepParent dist/PaperLensMini.app PaperLensMini.zip

# Submit for notarization
xcrun notarytool submit PaperLensMini.zip --wait --apple-id "your@email.com" --password "app-password" --team-id "TEAM_ID"
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
