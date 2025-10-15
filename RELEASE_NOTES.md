# PaperLens Mini v1.0.0 - Release Notes

## 🎉 First Stable Release!

**Release Date:** January 15, 2025  
**Version:** 1.0.0  
**Codename:** "Mini Launch"

---

## 📋 What's New

### ✨ Core Features
- **Multi-Source Paper Search**: Search across CrossRef (140M+ papers) and arXiv databases
- **Interactive Visualizations**: 5 beautiful charts including keyword networks and citation analysis
- **Export Capabilities**: Save results in CSV, Excel, JSON, or PDF formats
- **Modern UI**: Clean, wizard-based interface with dark mode support

### 🚀 Performance
- **Lightweight**: Only ~50MB vs 2GB for full PaperLens
- **Fast Startup**: ~2 seconds vs ~10 seconds for full version
- **No AI Dependencies**: Runs without heavy ML models

### 🎨 User Experience
- **3-Step Wizard**: Search → Visualize → Export
- **Dark Mode**: Toggle with moon icon or Ctrl+D
- **Keyboard Shortcuts**: F1 (Help), Ctrl+D (Dark Mode), ESC (Close)
- **Responsive Design**: Works on different screen sizes

---

## 📦 Downloads

### Windows
- **File**: `PaperLensMini.exe`
- **Size**: ~500 MB
- **Requirements**: Windows 10/11 (64-bit)
- **Installation**: Download and run directly

### macOS
- **File**: `PaperLensMini.app`
- **Size**: ~500 MB
- **Requirements**: macOS 10.14+ (64-bit)
- **Installation**: Download, open, and drag to Applications folder

### Linux
- **File**: `PaperLensMini` (executable)
- **Size**: ~500 MB
- **Requirements**: Ubuntu 18.04+ or equivalent
- **Installation**: Download, make executable (`chmod +x`), and run

---

## 🔧 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Ubuntu 18.04
- **RAM**: 4 GB
- **Storage**: 1 GB free space
- **Internet**: Required for paper search and visualizations

### Recommended
- **RAM**: 8 GB or more
- **Storage**: 2 GB free space
- **Internet**: Stable broadband connection

---

## 🚀 Quick Start Guide

### 1. Download & Install
1. Download the executable for your platform
2. Run the application
3. No additional installation required!

### 2. Search Papers
1. Enter your research keywords (e.g., "machine learning healthcare")
2. Select data sources (recommended: "All Sources")
3. Set max results (default: 300)
4. Click "Search Papers"
5. Wait 20-40 seconds for results

### 3. Visualize Data
1. Click "Generate All Visualizations"
2. Explore 5 interactive charts:
   - **Keyword Network**: See relationships between key terms
   - **Publications per Year**: Track research trends
   - **Citation Distribution**: Analyze paper impact
   - **Timeline**: View papers over time
   - **Source Distribution**: See database breakdown

### 4. Export Results
1. Choose your preferred format (CSV, Excel, JSON, PDF)
2. Click the export button
3. Files are saved in the `exports/` folder

---

## 🆚 PaperLens vs PaperLens Mini

| Feature | PaperLens Full | PaperLens Mini |
|---------|----------------|----------------|
| **Paper Search** | ✅ 16+ sources | ✅ 2 sources |
| **Visualizations** | ✅ Advanced | ✅ Basic (5 charts) |
| **Export** | ✅ | ✅ |
| **AI/ML Analysis** | ✅ | ❌ |
| **Topic Modeling** | ✅ | ❌ |
| **Gap Detection** | ✅ | ❌ |
| **RAG Q&A** | ✅ | ❌ |
| **Translation** | ✅ | ❌ |
| **Disk Space** | ~2GB | ~50MB |
| **Startup Time** | ~10s | ~2s |

---

## 🐛 Known Issues & Limitations

### Current Limitations
- **Google Scholar**: Temporarily disabled due to rate limits
- **AI Features**: Not available in Mini version
- **Offline Mode**: Requires internet for search and visualizations
- **Large Datasets**: Performance may vary with 500+ papers

### Fixed in This Release
- ✅ Character encoding issues on Windows
- ✅ Unicode compatibility problems
- ✅ Console output formatting

---

## 🔮 What's Coming Next

### Version 1.1.0 (Planned)
- Google Scholar integration improvements
- Additional data sources
- Performance optimizations
- Better error handling

### Version 1.2.0 (Future)
- Batch processing capabilities
- Advanced filtering options
- Custom visualization themes
- Plugin system

---

## 📞 Support & Feedback

### Getting Help
- **Documentation**: Check the README.md file
- **Issues**: Report bugs on GitHub Issues
- **Email**: support@artonlabs.com
- **Website**: [artonlabs.com](https://artonlabs.com)

### Contributing
We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 🙏 Acknowledgments

### Data Sources
- **CrossRef**: Academic paper metadata (140M+ papers)
- **arXiv**: Cornell University preprint repository

### Libraries & Frameworks
- [PyWebview](https://github.com/r0x0r/pywebview) - Desktop app framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation

### Development
- **Developer**: Hartono (ArtonLabs)
- **License**: MIT License
- **Repository**: [GitHub](https://github.com/your-username/paperlens-mini)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [ArtonLabs](https://artonlabs.com)**

*"Find the gap, Lead the innovation"*
