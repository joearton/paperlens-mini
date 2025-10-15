# 🪟 Windows Build Guide - PaperLens Mini

This guide will help you build a standalone Windows executable for PaperLens Mini.

## 📋 Prerequisites

### Required Software

1. **Python 3.8-3.11** (3.9 recommended)
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Visual C++ Redistributable**
   - Usually pre-installed on Windows 10/11
   - Download from [Microsoft](https://aka.ms/vs/17/release/vc_redist.x64.exe) if needed

3. **PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

## 🚀 Quick Build

1. **Open Command Prompt** as Administrator
2. **Navigate to project directory**
   ```cmd
   cd path\to\paperlens-mini
   ```
3. **Activate virtual environment** (if using one)
   ```cmd
   .\venv\Scripts\activate
   ```
4. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```
5. **Run build script**
   ```cmd
   cd build_scripts\windows
   build.bat
   ```

## 📦 What You Get

- **Executable**: `dist\PaperLensMini.exe`
- **Size**: ~500 MB (includes Python runtime and all dependencies)
- **Standalone**: No Python installation required on target machines

## 🧪 Testing Your Build

1. **Run the executable**
   ```cmd
   dist\PaperLensMini.exe
   ```

2. **Test core features**
   - ✅ Search for papers
   - ✅ Generate visualizations
   - ✅ Export reports
   - ✅ UI interactions

## 📤 Distribution Options

### Option 1: Direct EXE
- Share the `.exe` file directly
- Users can run immediately (may trigger Windows Defender warning)

### Option 2: ZIP Package
```cmd
Compress-Archive -Path dist\PaperLensMini.exe -DestinationPath PaperLensMini-Windows.zip
```

### Option 3: Installer (Advanced)
Use tools like:
- **Inno Setup** (Free)
- **NSIS** (Free)
- **Advanced Installer** (Commercial)

## 🔧 Troubleshooting

### "Windows protected your PC"
- Click "More info"
- Click "Run anyway"
- This is normal for unsigned executables

### "PyInstaller not found"
```cmd
pip install pyinstaller
```

### "Permission denied"
- Run Command Prompt as Administrator
- Check antivirus software isn't blocking the build

### Build fails with "Module not found"
- Add missing modules to `hiddenimports` in spec file
- Rebuild: `pyinstaller paperlens_mini_windows.spec --clean`

### Large file size
- Normal for PyInstaller builds (~500 MB)
- Includes Python runtime and all dependencies
- Use `excludes` in spec file to remove unused modules

## 🎨 Customization

### Adding Icon
1. Create `.ico` file (256x256 pixels recommended)
2. Update spec file:
   ```python
   icon='path/to/your/icon.ico'
   ```

### Reducing Size
Edit `paperlens_mini_windows.spec`:
```python
excludes = [
    'matplotlib',    # Remove if not needed
    'scipy',         # Remove if not needed
    'sklearn',       # Remove if not needed
    # Add other unused modules
]
```

### Adding Version Info
Create version file and update spec:
```python
version_file='version.txt'
```

## 📊 Build Performance

| Aspect | Time | Size |
|--------|------|------|
| **Build Time** | 3-5 minutes | - |
| **Final Size** | - | ~500 MB |
| **Startup Time** | 2-3 seconds | - |

## 🆘 Getting Help

### Common Issues
1. **Check build output** for error messages
2. **Run from Command Prompt** to see detailed errors
3. **Check PyInstaller logs** in `build/` directory

### Support
- GitHub Issues: Report bugs or ask questions
- PyInstaller Docs: [pyinstaller.org](https://pyinstaller.org)

## ✅ Success Checklist

Before distributing:
- [ ] Test on Windows 10/11
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Test on fresh system (if possible)
- [ ] Create installer/package
- [ ] Write installation instructions

---

**Built with ❤️ by ArtonLabs**
