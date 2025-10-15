# PaperLens Mini

**Simple Research Paper Analyzer - Without AI/ML**

PaperLens Mini adalah versi sederhana dari PaperLens yang fokus pada pencarian dan visualisasi paper akademik tanpa menggunakan model AI/ML dan fitur translation. Cocok untuk penggunaan yang lebih ringan dan cepat.

## 🌟 Fitur

### ✅ Yang Ada di PaperLens Mini:

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

### ❌ Yang Tidak Ada (dibanding PaperLens Full):
- ❌ AI/ML Models (Google Flan-T5, spaCy, Sentence Transformers)
- ❌ NLP Analysis (topic modeling, keyword extraction)
- ❌ RAG System (Q&A with AI)
- ❌ Deep Translator (Indonesian translation)
- ❌ Advanced research gap detection
- ❌ 16+ data sources (hanya 2-3 sources)

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
- Windows: `dist/PaperLensMini.exe` (~500 MB)
- macOS: `dist/PaperLensMini.app` (~500 MB)  
- Linux: `dist/PaperLensMini/PaperLensMini` (~500 MB)

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
paperlens-mini/
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

## 🆚 PaperLens vs PaperLens Mini

| Feature | PaperLens | PaperLens Mini |
|---------|-----------|----------------|
| Paper Search | ✅ (16+ sources) | ✅ (2 sources) |
| Visualizations | ✅ Advanced | ✅ Basic (4 charts) |
| Export | ✅ | ✅ |
| AI/ML Analysis | ✅ | ❌ |
| Topic Modeling | ✅ | ❌ |
| Gap Detection | ✅ | ❌ |
| RAG Q&A | ✅ | ❌ |
| Translation | ✅ | ❌ |
| Disk Space | ~2GB | ~50MB |
| Startup Time | ~10s | ~2s |
| UI Features | Full | Simplified |
| Dark Mode | ✅ | ✅ |
| Help/About | ✅ | ✅ |

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

- Email: support@artonlabs.com
- Issues: Create issue on repository

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

**PaperLens Mini** - Simple, fast, and lightweight research paper analyzer!

*For AI-powered features, use the full PaperLens version*

*Made with ❤️ by [ArtonLabs](https://artonlabs.com)*
