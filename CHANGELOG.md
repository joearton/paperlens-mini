# Changelog

All notable changes to PaperLens Mini will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- Initial release of PaperLens Mini
- Multi-source paper search (CrossRef, arXiv)
- 5 interactive visualizations:
  - Keyword network (full width)
  - Publications per year (bar chart)
  - Citation distribution (histogram)
  - Timeline chart (scatter plot)
  - Source distribution (pie chart)
- Export capabilities (CSV, Excel, JSON, PDF)
- Modern wizard-based UI with 3-step workflow
- Dark mode toggle with persistence
- Help and About modals
- Keyboard shortcuts (F1, Ctrl+D, ESC)
- Scroll to top functionality
- Responsive design
- Standalone executables for Windows, macOS, and Linux

### Fixed
- Character encoding issues with Unicode checkmark characters
- Windows console compatibility for print statements
- Proper ASCII-safe status messages

### Technical Details
- Built with Python 3.8+ and PyWebview
- Uses Plotly.js for interactive visualizations
- Pandas for data processing
- Lightweight (~50MB vs 2GB for full version)
- No AI/ML dependencies for faster startup

### Known Limitations
- No AI/ML analysis (use full PaperLens for advanced features)
- Limited to 2 data sources (CrossRef, arXiv)
- Google Scholar integration disabled due to rate limits
- Requires internet connection for paper search and visualizations

---

## Release Notes

### Version 1.0.0 - "Mini Launch"
**Release Date:** January 15, 2025

This is the first stable release of PaperLens Mini, a simplified version of PaperLens focused on core paper search and visualization capabilities without AI/ML dependencies.

**Key Features:**
- ✅ Fast paper search across multiple academic databases
- ✅ Interactive data visualizations
- ✅ Multiple export formats
- ✅ Modern, user-friendly interface
- ✅ Cross-platform support (Windows, macOS, Linux)

**Target Users:**
- Researchers who need quick paper analysis
- Students working on literature reviews
- Anyone who wants lightweight research tools
- Users who prefer simplicity over advanced AI features

**What's Next:**
- Google Scholar integration improvements
- Additional data sources
- Performance optimizations
- User feedback integration

---

*For the full PaperLens experience with AI/ML features, visit [ArtonLabs](https://artonlabs.com)*
