# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Sintesa - Linux Build
Build a standalone Linux executable
"""

import sys
import os
from pathlib import Path

block_cipher = None

# Get base directory (project root)
# SPECPATH is the directory containing this spec file (provided by PyInstaller)
base_dir = Path(SPECPATH).parent.parent

# Data files to include in the bundle
datas = [
    (str(base_dir / 'ui'), 'ui'),                                # UI folder (HTML, JS, CSS)
    (str(base_dir / 'config.py'), '.'),                          # Configuration file
    (str(base_dir / 'LICENSE'), '.'),                            # License file
    (str(Path(SPECPATH) / 'favicon.png'), 'ui/images'),          # Updated favicon
]

# Hidden imports - modules that PyInstaller might miss during analysis
hiddenimports = [
    # PyWebView - Linux specific
    'pywebview',
    'pywebview.platforms.gtk',
    'bottle',
    
    # GTK bindings
    'gi',
    'gi.repository',
    'gi.repository.Gtk',
    'gi.repository.WebKit2',
    'gi.repository.GLib',
    
    # Data Processing
    'pandas',
    'pandas.plotting',
    'pandas.core.groupby',
    'numpy',
    'requests',
    'beautifulsoup4',
    
    # Visualization
    'plotly',
    'plotly.graph_objects',
    'plotly.express',
    'networkx',
    
    # Export
    'openpyxl',
    'fpdf2',
    
    # Google Scholar
    'scholarly',
    'scholarly._navigator',
    
    # Standard library modules that might be missed
    'json',
    'csv',
    'datetime',
    'pathlib',
    'typing',
    'concurrent.futures',
    'threading',
    'queue',
    'urllib.parse',
    'urllib.request',
    'xml.etree.ElementTree',
    'html.parser',
    're',
    'math',
    'statistics',
    'collections',
    'itertools',
    'functools',
    'operator',
]

# Excluded modules to reduce size
excludes = [
    'tkinter',        # Not needed (GUI)
    'test',           # Test modules
    # 'unittest',     # Removed from excludes - needed by pandas and other libraries
    'doctest',        # Testing
    'IPython',        # Interactive
    'jupyter',        # Notebooks
    'pytest',         # Testing
    'sphinx',         # Documentation
    'matplotlib',     # Not used in Mini version
    'scipy',          # Not used in Mini version
    'sklearn',        # Not used in Mini version
    'tensorflow',     # Not used in Mini version
    'torch',          # Not used in Mini version
    'transformers',   # Not used in Mini version
    'spacy',          # Not used in Mini version
    'nltk',           # Not used in Mini version
    'wordcloud',      # Not used in Mini version
    'seaborn',        # Not used in Mini version
    # Note: pandas.plotting is needed internally by pandas, do not exclude
]

# Analysis configuration
a = Analysis(
    [str(base_dir / 'app.py')],
    pathex=[str(base_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries and data files
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Sintesa',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip debug symbols on Linux
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(Path(SPECPATH) / 'favicon.png'),  # Updated favicon as Linux icon
    version_file=None,
)
