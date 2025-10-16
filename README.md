# Sintesa

**Simple Research Paper Analyzer**

Sintesa adalah aplikasi lightweight untuk pencarian dan visualisasi paper akademik tanpa menggunakan model AI/ML. Fokus pada fitur-fitur essential: search, visualize, dan export.

## 🌟 Fitur

### ✅ Fitur Utama Sintesa:

- **🔍 Multi-Source Paper Search**
  - CrossRef API (140M+ papers)
  - arXiv API (Physics, Math, CS, etc.)
  - Google Scholar (coming soon)
  
- **📊 Interactive Visualizations** (2 kolom layout)
  - **Keyword network** (full width) - Shows keyword relationships
  - Publications per year (bar chart)
  - Citation distribution (histogram)  
  - Timeline chart (scatter plot)
  - Source distribution (pie chart)
  
- **💾 Export Capabilities**
  - CSV export
  - Excel export (with summary statistics)
  - JSON export
  - PDF report generation

- **🎨 Modern UI**
  - Wizard-based workflow (3 steps)
  - Dark mode toggle
  - Help & About modals
  - Scroll to top button
  - Keyboard shortcuts (F1, Ctrl+D, ESC)
  - Responsive design

### ⚡ Keunggulan:
- ⚡ Ringan: ~50MB tanpa AI/ML models
- ⚡ Cepat: Startup ~2 detik
- ⚡ Simple: Fokus pada fitur essential
- ⚡ Reliable: Data langsung dari sumber akademik terpercaya

## 📋 Requirements

- Python 3.8+
- ~50MB disk space (no AI models needed)
- Internet connection for paper search

## 🚀 Quick Start

### Option 1: Using Run Script (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Installation

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py
```

### Option 3: Build Standalone Executables

Build for your platform:

**Windows:**
```cmd
build.bat
```

**macOS/Linux:**
```bash
chmod +x build.sh
./build.sh
```

**All Platforms (Python script):**
```bash
python build_all.py
```

**Build Output:**
- Windows: `dist/Sintesa.exe` (~500 MB)
- macOS: `dist/Sintesa.app` (~500 MB)  
- Linux: `dist/Sintesa/Sintesa` (~500 MB)

See [`build_scripts/README.md`](build_scripts/README.md) for detailed build instructions.

## 📖 Usage Guide

### Step 1: Search Papers 🔍
1. Enter research keywords (e.g., "machine learning healthcare")
2. Select data source:
   - **All Sources** - Search both CrossRef and arXiv (recommended)
   - **CrossRef** - Fast, reliable, DOI links
   - **arXiv** - Open-access preprints
3. Set max results: **300** (default)
4. Set from year: **Auto-set to current year - 3** (e.g., 2022 for 2025)
5. Click **"Search Papers"**
6. Wait 20-40 seconds for results

### Step 2: Visualize Data 📊
1. Click **"Next"** or wizard Step 2
2. Click **"Generate All Visualizations"**
3. View 5 interactive charts:
   - **Keyword Network** (full width) - Relationship graph of key terms
   - **Publications per Year** - Publication trends
   - **Citation Distribution** - Impact analysis
   - **Timeline** - Papers over time
   - **Source Distribution** - Papers by database
4. Charts are interactive: zoom, pan, hover for details

### Step 3: Export Results 💾
1. Click **"Next"** or wizard Step 3
2. Choose export format:
   - **CSV** - Simple data table
   - **Excel** - Multiple sheets with statistics
   - **JSON** - Complete data structure
   - **PDF** - Professional report
3. Click export button
4. Files saved in `exports/` folder

## ⌨️ Keyboard Shortcuts

- `F1` - Show Help
- `Ctrl+D` - Toggle Dark Mode
- `ESC` - Close modals
- `Enter` - Submit search

## 🏗️ Project Structure

```
sintesa/
├── app.py                      # Main application
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── run.bat / run.sh           # Launchers
│
├── modules/                    # Core modules
│   ├── base_source.py          # Base class for data sources
│   ├── crossref_source.py      # CrossRef API
│   ├── arxiv_source.py         # arXiv API
│   ├── scholar_source.py       # Google Scholar (placeholder)
│   ├── data_fetcher.py         # Multi-source search
│   ├── visualizer.py           # Plotly visualizations
│   └── exporter.py             # Export functionality
│
└── ui/                         # Frontend
    ├── index.html              # Main UI
    ├── css/style.css           # Styles
    ├── js/app.js               # JavaScript
    └── images/                 # Logo and images
        ├── logo-with-text.png
        └── favicon.png
```

## 🔧 Configuration

Default settings in `config.py`:

```python
DEFAULT_MAX_RESULTS = 300        # Papers to fetch
DEFAULT_FROM_YEAR = CURRENT_YEAR - 3  # 3 years ago
MAX_RESULTS_PER_SOURCE = 300
```

## 🎨 Features

### Dark Mode 🌙
- Click moon icon in sidebar
- Or press `Ctrl+D`
- Preference saved automatically
- Smooth transitions

### Help & About
- Click `?` icon in sidebar or press `F1` for Help
- Click `i` icon in sidebar for About
- Click outside or press `ESC` to close

### Scroll to Top ⬆️
- Appears after scrolling 300px
- Click to smooth scroll to top
- Always accessible

## 📊 Data Sources

### CrossRef
- **Coverage**: 140M+ academic papers
- **Features**: DOI links, fast search, reliable metadata
- **API Key**: Optional
- **Delay**: 1.5s between requests

### arXiv
- **Coverage**: Physics, Math, CS, Biology, etc.
- **Features**: Open-access preprints, recent research
- **API Key**: Not required
- **Delay**: 3s between requests

### Google Scholar (Coming Soon)
- Currently disabled in mini version due to rate limits
- Will be enabled in future updates

## 🐛 Troubleshooting

### Visualizations Not Showing?

1. **Check Browser Console (F12)**:
   ```
   Should see: "Plotly.js loaded successfully"
   ```

2. **Check Internet Connection**:
   - Plotly.js loads from CDN
   - Requires internet to load

3. **Verify Charts Generated**:
   ```
   Should see console logs:
   [Viz] SUCCESS: years set to container viz-years
   [Viz] SUCCESS: citations set to container viz-citations
   [Viz] SUCCESS: timeline set to container viz-timeline
   [Viz] SUCCESS: sources set to container viz-sources
   [Viz] COMPLETE: 4/4 visualizations rendered
   ```

4. **Manual Test in Console**:
   ```javascript
   typeof Plotly  // Should be "object"
   currentPapers.length  // Should be > 0
   handleVisualization()  // Retry visualization
   ```

### No Papers Found?
- Check internet connection
- Try different keywords
- Try single source (CrossRef)
- Remove year filter

### Export Errors?
- Check `exports/` folder exists
- Check write permissions
- Check disk space

## 💡 Tips

### For Better Search Results:
- Use specific keywords
- Combine terms: `"deep learning medical imaging"`
- Use year filter for recent papers
- Default: 300 papers from last 3 years

### For Better Performance:
- Search takes 20-40 seconds for 300 papers
- Single source is faster than "All Sources"
- Visualizations generate in 3-5 seconds (5 charts + keyword extraction)
- Keyword network shows top 20 terms from titles

### Using the Interface:
- **Dark Mode**: Click moon icon or press `Ctrl+D`
- **Help**: Click ? icon or press `F1`
- **About**: Click i icon in sidebar
- **Scroll to Top**: Button appears after scrolling
- **Close Modals**: Click outside or press `ESC`

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Desktop Framework | PyWebview |
| Visualizations | Plotly |
| Data Processing | Pandas |
| Data Sources | CrossRef API, arXiv API |
| Frontend | HTML5, CSS3, JavaScript |
| Build | PyInstaller |

## 🆚 Sintesa vs Publish or Perish

### Perbandingan Fitur

| Aspek | Sintesa | Publish or Perish |
|-------|---------|-------------------|
| **Platform** | Windows, macOS, Linux | Windows, macOS, Linux |
| **Size** | ~500 MB (bundled) / ~50 MB (source) | ~20 MB |
| **Data Source** | CrossRef (140M+), arXiv | Google Scholar primarily |
| **Interface** | Modern Web-based, Dark Mode | Classic Desktop UI |
| **Visualisasi** | 5+ Interactive Charts (Plotly) | Basic tables & static charts |
| **Export Format** | PDF, Excel, CSV, JSON | CSV, Excel, BibTeX, RTF |
| **Citation Metrics** | Basic (from sources) | Advanced (h-index, g-index, etc.) |
| **Open Source** | ✅ Yes (MIT License) | ❌ Freeware (closed source) |
| **Development** | Active (Python-based) | Stable (Delphi-based) |
| **Customization** | Easy to modify | Limited |
| **API Access** | Direct (CrossRef, arXiv) | Via Google Scholar |

### Kapan Menggunakan Sintesa?

✅ **Gunakan Sintesa jika:**
- Membutuhkan visualisasi interaktif yang modern
- Ingin data dari CrossRef atau arXiv langsung
- Perlu export format yang beragam (JSON, PDF report)
- Suka interface modern dengan dark mode
- Ingin modifikasi atau extend functionality
- Membutuhkan open-source solution

### Kapan Menggunakan Publish or Perish?

✅ **Gunakan Publish or Perish jika:**
- Fokus pada citation metrics (h-index, g-index)
- Primarily menggunakan Google Scholar
- Membutuhkan aplikasi yang sangat ringan (~20MB)
- Sudah terbiasa dengan workflow PoP
- Perlu analisis author impact mendalam
- Ingin BibTeX export langsung

## 📝 Development

### Technology Stack

**Backend:**
- Python 3.8+
- PyWebview (desktop framework)
- Plotly (visualizations)
- Pandas (data processing)
- Requests (HTTP)

**Frontend:**
- HTML5/CSS3
- JavaScript (ES6+)
- Plotly.js (charts)
- Font Awesome (icons)

**Data Sources:**
- CrossRef API
- arXiv API

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes with clear comments
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Credits

**Developed by ArtonLabs (Hartono)**

### Data Sources:
- **CrossRef** - Academic paper metadata
- **arXiv** - Cornell University preprint repository

### Libraries:
- [PyWebview](https://github.com/r0x0r/pywebview) - Desktop app framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation

## 📞 Support

- **Website**: [artonlabs.com](https://artonlabs.com)
- **Email**: support@artonlabs.com
- **GitHub**: [github.com/artonlabs/sintesa](https://github.com/artonlabs/sintesa)
- **Issues**: Create issue on GitHub repository

## 🚀 Roadmap

### Version 1.1.0 (Planned)
- [ ] Google Scholar integration improvements
- [ ] Additional export templates
- [ ] Custom visualization themes
- [ ] Search history export

### Version 1.2.0 (Future)
- [ ] Batch processing capabilities
- [ ] Advanced filtering options
- [ ] Citation network visualization
- [ ] Plugin system for extensibility

## 📈 Why Sintesa?

### Problem Statement
Peneliti seringkali membutuhkan tools untuk:
- Mencari paper dari multiple sources
- Visualisasi tren penelitian dengan cepat
- Export data untuk analisis lebih lanjut
- Interface modern yang mudah digunakan

Existing tools seperti Publish or Perish sangat bagus untuk citation metrics, namun:
- Terbatas pada Google Scholar
- Visualisasi yang basic
- Tidak open source (sulit dimodifikasi)
- Interface yang dated

### Our Solution
Sintesa menawarkan:
- ✅ **Multi-source**: CrossRef (140M papers) + arXiv
- ✅ **Modern UI**: Web-based interface dengan dark mode
- ✅ **Interactive**: Plotly charts yang fully interactive
- ✅ **Flexible**: Export ke 4 format berbeda
- ✅ **Open Source**: MIT license, easy to modify
- ✅ **Lightweight**: Tanpa AI/ML overhead (~50MB source)

---

## 🎯 Quick Reference

### Default Settings
- **Max Results**: 300 papers
- **From Year**: Current year - 3 (e.g., 2022 for 2025)
- **Sources**: All (CrossRef + arXiv)

### Keyboard Shortcuts
- **F1**: Help
- **Ctrl+D**: Dark Mode
- **ESC**: Close modals
- **Enter**: Search (when in search field)

### File Exports
All files saved to: `exports/` folder

### Troubleshooting
1. Check browser console (F12)
2. Verify Plotly.js loaded
3. Check internet connection
4. See logs for errors

---

**Sintesa** - Simple, fast, and lightweight research paper analyzer!

*Made with ❤️ by [ArtonLabs](https://artonlabs.com)*
