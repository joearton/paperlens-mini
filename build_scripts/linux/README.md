# 🐧 Linux Build Guide - Sintesa

This guide will help you build a standalone Linux executable for Sintesa.

## 📋 Prerequisites

### Required Software

1. **Linux Distribution**
   - Ubuntu 20.04+ / Debian 11+
   - Fedora 34+ / RHEL 8+
   - Arch Linux / Manjaro
   - openSUSE 15+

2. **Python 3.8-3.11** (3.9 recommended)
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.9 python3.9-venv python3-pip
   
   # Fedora
   sudo dnf install python3.9 python3.9-venv python3-pip
   
   # Arch
   sudo pacman -S python python-pip
   ```

3. **System Dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev
   
   # Fedora
   sudo dnf install gtk3-devel webkit2gtk3-devel
   
   # Arch
   sudo pacman -S gtk3 webkit2gtk
   ```

4. **PyInstaller**
   ```bash
   pip install pyinstaller
   ```

## 🚀 Quick Build

1. **Open Terminal**
2. **Navigate to project directory**
   ```bash
   cd path/to/sintesa
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
   cd build_scripts/linux
   chmod +x build.sh
   ./build.sh
   ```

## 📦 What You Get

- **Executable Directory**: `dist/Sintesa/`
- **Main Executable**: `dist/Sintesa/Sintesa`
- **Size**: ~500 MB (includes Python runtime and all dependencies)
- **Standalone**: No Python installation required on target machines

## 🧪 Testing Your Build

1. **Run the application**
   ```bash
   cd dist/Sintesa
   ./Sintesa
   ```

2. **Test core features**
   - ✅ Search for papers
   - ✅ Generate visualizations
   - ✅ Export reports
   - ✅ UI interactions

## 📤 Distribution Options

### Option 1: Directory Bundle
- Share the entire `Sintesa/` directory
- Users run `./Sintesa` from the directory

### Option 2: TAR.GZ Archive
```bash
tar -czf Sintesa-Linux.tar.gz -C dist Sintesa
```

### Option 3: AppImage (Universal)
```bash
# Install AppImageKit
sudo apt install appimagetool  # Ubuntu/Debian

# Create AppImage
appimagetool dist/Sintesa Sintesa-1.0.0-x86_64.AppImage
```

### Option 4: DEB Package (Ubuntu/Debian)
```bash
# Create package structure
mkdir -p sintesa/usr/local/bin
mkdir -p sintesa/usr/share/applications
mkdir -p sintesa/usr/share/icons/hicolor/256x256/apps

# Copy files
cp -r dist/Sintesa/* sintesa/usr/local/bin/
cp Sintesa.png sintesa/usr/share/icons/hicolor/256x256/apps/

# Create desktop entry
cat > sintesa/usr/share/applications/sintesa.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Sintesa
Comment=Research Gap Analysis Tool
Exec=/usr/local/bin/Sintesa
Icon=sintesa
Terminal=false
Categories=Science;Research;
EOF

# Build DEB package
dpkg-deb --build sintesa sintesa-1.0.0-amd64.deb
```

### Option 5: RPM Package (Fedora/RHEL)
```bash
# Create spec file for RPM
# See: https://rpm-packaging-guide.github.io/
```

## 🔧 Troubleshooting

### "Permission denied"
```bash
chmod +x dist/Sintesa/Sintesa
```

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### "GTK+3 not found"
```bash
# Ubuntu/Debian
sudo apt-get install libgtk-3-dev

# Fedora
sudo dnf install gtk3-devel

# Arch
sudo pacman -S gtk3
```

### "WebKit2GTK not found"
```bash
# Ubuntu/Debian
sudo apt-get install libwebkit2gtk-4.0-dev

# Fedora
sudo dnf install webkit2gtk3-devel

# Arch
sudo pacman -S webkit2gtk
```

### Build fails with "Module not found"
- Add missing modules to `hiddenimports` in spec file
- Rebuild: `pyinstaller sintesa_linux.spec --clean`

### Large file size
- Normal for PyInstaller builds (~500 MB)
- Includes Python runtime and all dependencies
- Use `excludes` in spec file to remove unused modules

### App won't start
```bash
# Run from terminal to see error messages
cd dist/Sintesa
./Sintesa

# Check dependencies
ldd Sintesa
```

## 🎨 Customization

### Adding Icon
1. Create PNG files in multiple sizes
2. Update desktop entry file:
   ```ini
   Icon=sintesa
   ```
3. Place icons in appropriate directories

### Reducing Size
Edit `sintesa_linux.spec`:
```python
excludes = [
    'matplotlib',    # Remove if not needed
    'scipy',         # Remove if not needed
    'sklearn',       # Remove if not needed
    # Add other unused modules
]
```

### Desktop Integration
Create desktop entry file:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Sintesa
Comment=Research Gap Analysis Tool
Exec=/path/to/Sintesa
Icon=sintesa
Terminal=false
Categories=Science;Research;
```

## 📊 Build Performance

| Aspect | Time | Size |
|--------|------|------|
| **Build Time** | 2-4 minutes | - |
| **Final Size** | - | ~500 MB |
| **Startup Time** | 2-3 seconds | - |

## 🔒 Security Considerations

### AppArmor/SELinux
- May block application execution
- Users may need to create policy exceptions
- AppImage format often works better with security policies

### Permissions
- Ensure executable permissions are set
- Consider using AppImage for better portability

## 🆘 Getting Help

### Common Issues
1. **Check build output** for error messages
2. **Run from Terminal** to see detailed errors
3. **Check PyInstaller logs** in `build/` directory
4. **Verify system dependencies** are installed

### Support
- GitHub Issues: Report bugs or ask questions
- PyInstaller Docs: [pyinstaller.org](https://pyinstaller.org)

## ✅ Success Checklist

Before distributing:
- [ ] Test on target Linux distribution
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Test on fresh system (if possible)
- [ ] Create AppImage or package
- [ ] Write installation instructions
- [ ] Test desktop integration

---

**Built with ❤️ by ArtonLabs**
