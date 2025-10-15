"""
Configuration file for PaperLens Mini
Simple version without AI/ML models
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
CACHE_DIR = BASE_DIR / "cache"

# Configuration file
CONFIG_FILE = BASE_DIR / "config_sources.json"

# Create directories if they don't exist
for directory in [DATA_DIR, EXPORTS_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# Analysis Configuration (simplified - no AI)
MAX_RESULTS_PER_SOURCE = 300
DEFAULT_MAX_RESULTS = 300
DEFAULT_LANGUAGE = "en"

# Year settings
from datetime import datetime
CURRENT_YEAR = datetime.now().year
DEFAULT_FROM_YEAR = CURRENT_YEAR - 3  # 3 years ago

