# PaperLens Mini - Build Notes

## 🔧 Known Issues and Fixes

### Issue: "No module named 'pandas.plotting'"

**Problem:**
When running the built executable, you get:
```
ModuleNotFoundError: No module named 'pandas.plotting'
```

**Root Cause:**
Pandas internally requires `pandas.plotting` module even if we don't use it directly. Excluding it from the build causes runtime errors.

**Solution Applied:**
1. ✅ Removed `pandas.plotting` from `excludes` list in all spec files
2. ✅ Added `pandas.plotting` and `pandas.core.groupby` to `hiddenimports`
3. ✅ Updated all platform spec files (Windows, macOS, Linux)

**Files Modified:**
- `build_scripts/windows/paperlens_mini_windows.spec`
- `build_scripts/macos/paperlens_mini_macos.spec`
- `build_scripts/linux/paperlens_mini_linux.spec`

### How to Rebuild After Fix

**Windows:**
```cmd
cd build_scripts\windows
pyinstaller paperlens_mini_windows.spec --clean --noconfirm
```

**macOS:**
```bash
cd build_scripts/macos
pyinstaller paperlens_mini_macos.spec --clean --noconfirm
```

**Linux:**
```bash
cd build_scripts/linux
pyinstaller paperlens_mini_linux.spec --clean --noconfirm
```

## 📋 Important Notes

### Pandas Dependencies
The following pandas modules **must NOT be excluded**:
- `pandas.plotting` - Required internally by pandas
- `pandas.core.groupby` - Required for aggregation operations

These are automatically included in the `hiddenimports` list.

### Safe to Exclude
These modules are confirmed safe to exclude:
- `matplotlib` - Not used in Mini version
- `scipy` - Not used in Mini version
- `sklearn` - Not used in Mini version
- `tensorflow`, `torch`, `transformers` - No AI/ML in Mini
- `nltk`, `spacy` - No NLP in Mini
- `wordcloud`, `seaborn` - Not used for visualizations

### Testing Your Build

After building, test the executable:

**Windows:**
```cmd
dist\PaperLensMini.exe
```

**macOS:**
```bash
open dist/PaperLensMini.app
```

**Linux:**
```bash
cd dist/PaperLensMini
./PaperLensMini
```

### Expected Behavior
The application should:
1. ✅ Start without errors
2. ✅ Show the main UI window
3. ✅ Allow paper search
4. ✅ Generate visualizations
5. ✅ Export data

### Troubleshooting

**If the app still won't start:**
1. Run from terminal to see error messages
2. Check if all dependencies are in `hiddenimports`
3. Try clean rebuild: `--clean --noconfirm`
4. Check PyInstaller build warnings

**If visualizations don't work:**
1. Verify `plotly` is in `hiddenimports`
2. Check that Plotly.js CDN is accessible (requires internet)
3. Check browser console in UI (if available)

## 🚀 Build Performance

### Expected Times
- **Windows**: 3-5 minutes
- **macOS**: 2-4 minutes
- **Linux**: 2-4 minutes

### Expected Sizes
- **Windows**: ~500 MB
- **macOS**: ~500 MB
- **Linux**: ~500 MB

### Size Breakdown
- Python runtime: ~50 MB
- Pandas + NumPy: ~150 MB
- Plotly: ~50 MB
- PyWebView + dependencies: ~100 MB
- Other libraries: ~50 MB
- Application code: ~10 MB
- UI files: ~5 MB
- Overhead: ~85 MB

## 📚 Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [Build Scripts README](build_scripts/README.md)
- [Platform-Specific Guides](build_scripts/)
  - [Windows](build_scripts/windows/README.md)
  - [macOS](build_scripts/macos/README.md)
  - [Linux](build_scripts/linux/README.md)

---

**Last Updated:** 2024-10-15
**Issue:** Fixed pandas.plotting import error
**Status:** ✅ Resolved
