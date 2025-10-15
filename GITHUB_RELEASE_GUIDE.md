# 🚀 Panduan Membuat Release di GitHub - PaperLens Mini

## 📋 Persiapan Sebelum Release

### 1. Pastikan Semua File Siap
```bash
# Cek status git
git status

# Pastikan semua perubahan sudah di-commit
git add .
git commit -m "Fix character encoding issues for v1.0.0 release"
```

### 2. Build Executables untuk Semua Platform
```bash
# Windows
cd build_scripts\windows
pyinstaller paperlens_mini_windows.spec --clean --noconfirm

# macOS (jika ada Mac)
cd build_scripts/macos
pyinstaller paperlens_mini_macos.spec --clean --noconfirm

# Linux
cd build_scripts/linux
pyinstaller paperlens_mini_linux.spec --clean --noconfirm
```

### 3. Test Executables
```bash
# Test Windows
dist\PaperLensMini.exe

# Test macOS
open dist/PaperLensMini.app

# Test Linux
cd dist/PaperLensMini
./PaperLensMini
```

---

## 🏷️ Langkah-langkah Membuat Release

### Step 1: Buat Git Tag
```bash
# Buat tag untuk versi 1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0 - First stable release"

# Push tag ke GitHub
git push origin v1.0.0
```

### Step 2: Buat Release di GitHub

#### Via GitHub Web Interface:

1. **Buka Repository di GitHub**
   - Pergi ke: `https://github.com/your-username/paperlens-mini`

2. **Klik "Releases"**
   - Di sidebar kanan, klik "Releases"
   - Atau langsung ke: `https://github.com/your-username/paperlens-mini/releases`

3. **Klik "Create a new release"**

4. **Isi Form Release:**
   ```
   Tag version: v1.0.0
   Release title: PaperLens Mini v1.0.0 - First Stable Release
   
   Description:
   ## 🎉 First Stable Release!
   
   PaperLens Mini v1.0.0 is now available! This lightweight research paper analyzer provides fast search and visualization capabilities without AI/ML dependencies.
   
   ### ✨ What's New
   - Multi-source paper search (CrossRef, arXiv)
   - 5 interactive visualizations
   - Export to CSV, Excel, JSON, PDF
   - Modern UI with dark mode
   - Cross-platform executables
   
   ### 📦 Downloads
   - **Windows**: PaperLensMini.exe (~500MB)
   - **macOS**: PaperLensMini.app (~500MB) 
   - **Linux**: PaperLensMini executable (~500MB)
   
   ### 🔧 Fixed Issues
   - Character encoding issues on Windows
   - Unicode compatibility problems
   - Console output formatting
   
   See [RELEASE_NOTES.md](RELEASE_NOTES.md) for complete details.
   ```

5. **Upload Assets:**
   - Drag & drop `PaperLensMini.exe` (Windows)
   - Drag & drop `PaperLensMini.app` (macOS, jika ada)
   - Drag & drop `PaperLensMini` folder (Linux)

6. **Publish Release:**
   - Klik "Publish release"

#### Via GitHub CLI (Alternatif):
```bash
# Install GitHub CLI terlebih dahulu
# https://cli.github.com/

# Login ke GitHub
gh auth login

# Buat release
gh release create v1.0.0 \
  --title "PaperLens Mini v1.0.0 - First Stable Release" \
  --notes-file RELEASE_NOTES.md \
  dist/PaperLensMini.exe \
  dist/PaperLensMini.app \
  dist/PaperLensMini/
```

---

## 📝 Template Release Notes

### Untuk Release v1.0.0:
```markdown
## 🎉 First Stable Release!

**PaperLens Mini v1.0.0** is now available! This lightweight research paper analyzer provides fast search and visualization capabilities without AI/ML dependencies.

### ✨ Key Features
- **Multi-Source Search**: CrossRef (140M+ papers) + arXiv
- **Interactive Visualizations**: 5 beautiful charts
- **Export Capabilities**: CSV, Excel, JSON, PDF
- **Modern UI**: Dark mode, keyboard shortcuts, responsive design
- **Cross-Platform**: Windows, macOS, Linux executables

### 🚀 Performance
- **Lightweight**: ~50MB vs 2GB for full PaperLens
- **Fast Startup**: ~2 seconds
- **No AI Dependencies**: Runs without heavy ML models

### 🔧 Fixed Issues
- ✅ Character encoding issues on Windows
- ✅ Unicode compatibility problems  
- ✅ Console output formatting

### 📦 Downloads
- **Windows**: `PaperLensMini.exe` (~500MB)
- **macOS**: `PaperLensMini.app` (~500MB)
- **Linux**: `PaperLensMini` executable (~500MB)

### 🆚 PaperLens vs PaperLens Mini
| Feature | PaperLens Full | PaperLens Mini |
|---------|----------------|----------------|
| Paper Search | ✅ 16+ sources | ✅ 2 sources |
| Visualizations | ✅ Advanced | ✅ Basic (5 charts) |
| AI/ML Analysis | ✅ | ❌ |
| Disk Space | ~2GB | ~50MB |
| Startup Time | ~10s | ~2s |

### 📖 Documentation
- [README.md](README.md) - Complete usage guide
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Detailed release notes
- [CHANGELOG.md](CHANGELOG.md) - Version history

### 🐛 Known Limitations
- Google Scholar temporarily disabled due to rate limits
- Requires internet connection for search and visualizations
- No AI/ML features (use full PaperLens for advanced analysis)

### 🔮 What's Next
- Google Scholar integration improvements
- Additional data sources
- Performance optimizations

---

**Made with ❤️ by [ArtonLabs](https://artonlabs.com)**

*For AI-powered features, use the full PaperLens version*
```

---

## 🎯 Best Practices untuk Release

### 1. Version Numbering
- Gunakan [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`
- v1.0.0 = First stable release
- v1.1.0 = New features
- v1.0.1 = Bug fixes

### 2. Release Notes
- **Jelas dan Informatif**: Jelaskan apa yang baru dan apa yang diperbaiki
- **Include Screenshots**: Jika memungkinkan, tambahkan screenshot UI
- **Link ke Dokumentasi**: Sertakan link ke README dan dokumentasi lain
- **Known Issues**: Sebutkan batasan dan masalah yang diketahui

### 3. Assets
- **Naming Convention**: Gunakan nama yang konsisten
  - `PaperLensMini-v1.0.0-Windows.exe`
  - `PaperLensMini-v1.0.0-macOS.app`
  - `PaperLensMini-v1.0.0-Linux.tar.gz`
- **File Size**: GitHub limit 2GB per file
- **Compression**: Gunakan ZIP untuk mengurangi ukuran

### 4. Testing
- **Test di Platform Target**: Pastikan executable berjalan di OS yang berbeda
- **Test Fitur Utama**: Search, visualize, export
- **Test Error Handling**: Coba dengan input yang tidak valid

---

## 🔄 Workflow untuk Release Berikutnya

### Untuk Patch Release (v1.0.1):
```bash
# 1. Fix bugs
git checkout -b fix/bug-description
# ... make changes ...
git commit -m "Fix: description of bug fix"

# 2. Update version
# Update version in ui/index.html (line 354-355)
# Update CHANGELOG.md

# 3. Create release
git tag -a v1.0.1 -m "Release version 1.0.1 - Bug fixes"
git push origin v1.0.1
```

### Untuk Feature Release (v1.1.0):
```bash
# 1. Develop features
git checkout -b feature/new-feature
# ... implement features ...
git commit -m "Feat: add new feature description"

# 2. Update documentation
# Update README.md, CHANGELOG.md, RELEASE_NOTES.md

# 3. Create release
git tag -a v1.1.0 -m "Release version 1.1.0 - New features"
git push origin v1.1.0
```

---

## 📊 Monitoring Release

### 1. GitHub Insights
- Monitor download statistics
- Check issue reports
- Review user feedback

### 2. Analytics
- Track usage patterns
- Monitor error rates
- Collect user feedback

### 3. Follow-up
- Respond to issues quickly
- Plan next release based on feedback
- Update documentation as needed

---

## 🆘 Troubleshooting

### Common Issues:

#### 1. Tag Already Exists
```bash
# Delete existing tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Create new tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

#### 2. Large File Upload
```bash
# Use Git LFS for large files
git lfs track "*.exe"
git lfs track "*.app"
git add .gitattributes
git commit -m "Add LFS tracking for executables"
```

#### 3. Build Failures
```bash
# Clean build
pyinstaller --clean --noconfirm paperlens_mini_windows.spec

# Check dependencies
pip list
pip install -r requirements.txt
```

---

## 🎉 Congratulations!

Setelah mengikuti panduan ini, Anda akan memiliki:

✅ **Professional GitHub Release**  
✅ **Cross-platform Executables**  
✅ **Complete Documentation**  
✅ **Version History**  
✅ **User-friendly Downloads**

**Next Steps:**
1. Share release di social media
2. Update website/documentation
3. Monitor user feedback
4. Plan next release

---

**Happy Releasing! 🚀**

*Made with ❤️ by [ArtonLabs](https://artonlabs.com)*
