# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Sintesa - macOS Build
Build a standalone macOS application bundle (.app)
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

# Add fake_useragent data files (needed by scholarly)
try:
    import fake_useragent
    import os
    fake_ua_path = os.path.dirname(fake_useragent.__file__)
    fake_ua_data = os.path.join(fake_ua_path, 'data')
    if os.path.exists(fake_ua_data):
        datas.append((fake_ua_data, 'fake_useragent/data'))
except ImportError:
    pass

# Hidden imports - modules that PyInstaller might miss during analysis
hiddenimports = [
    # PyWebView - macOS specific
    'pywebview',
    'pywebview.platforms.cocoa',
    'bottle',
    
    # Data Processing
    'pandas',
    'pandas.plotting',
    'pandas.core.groupby',
    'numpy',
    'requests',
    'beautifulsoup4',
    'lxml',
    'lxml.etree',
    'lxml._elementpath',
    
    # Visualization
    'plotly',
    'plotly.graph_objects',
    'plotly.express',
    'plotly.io',
    'plotly.io._html',
    'plotly.io._json',
    'networkx',
    'networkx.algorithms',
    'networkx.algorithms.centrality',
    'networkx.algorithms.community',
    'wordcloud',
    'PIL',
    'PIL.Image',
    
    # Export
    'openpyxl',
    'openpyxl.workbook',
    'openpyxl.styles',
    'fpdf',
    'fpdf2',
    
    # Google Scholar
    'scholarly',
    'scholarly._navigator',
    'scholarly.scholarly',
    'scholarly.publication_parser',
    'scholarly.author_parser',
    'scholarly._proxy_generator',
    'fake_useragent',
    'fake_useragent.fake',
    'fake_useragent.utils',
    'fake_useragent.errors',
    'bs4',
    'bs4.element',
    'bs4.builder',
    'bs4.builder._lxml',
    
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
    'urllib3',
    'xml.etree.ElementTree',
    'html.parser',
    're',
    'math',
    'statistics',
    'collections',
    'itertools',
    'functools',
    'operator',
    'subprocess',
    'platform',
    'tempfile',
    'shutil',
    'logging',
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
    'scipy',          # Not used in Mini version
    'sklearn',        # Not used in Mini version
    'tensorflow',     # Not used in Mini version
    'torch',          # Not used in Mini version
    'transformers',   # Not used in Mini version
    'spacy',          # Not used in Mini version
    'nltk',           # Not used in Mini version
    'seaborn',        # Not used in Mini version
    # Note: matplotlib and wordcloud ARE used, do not exclude
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
    strip=True,  # Strip debug symbols on macOS
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(Path(SPECPATH) / 'favicon.png'),  # Updated favicon as macOS executable icon
    version_file=None,
)

# Create macOS app bundle
app = BUNDLE(
    exe,
    name='Sintesa.app',
    icon=str(Path(SPECPATH) / 'favicon.png'),  # Updated favicon as macOS bundle icon
    bundle_identifier='com.artonlabs.paperlensmini',
    info_plist={
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSMinimumSystemVersion': '10.14.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleName': 'Sintesa',
        'CFBundleDisplayName': 'Sintesa',
        'CFBundleExecutable': 'Sintesa',
        'CFBundleIdentifier': 'com.artonlabs.paperlensmini',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'NSPrincipalClass': 'NSApplication',
    },
)
