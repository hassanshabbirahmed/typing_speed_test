"""
Settings module that imports configuration from config manager.
"""
from .config import get_config

# Get configuration
config = get_config()

# Import all settings from config
DIFFICULTIES = config.difficulties
WINDOW_SIZE = config.window_size
WINDOW_TITLE = config.window_title
WINDOW_BG = config.window_bg
PRIMARY_COLOR = config.primary_color
SECONDARY_COLOR = config.secondary_color
TITLE_FONT = config.title_font
TEXT_FONT = config.text_font

# File paths
SCORES_FILE = config.scores_file
WORD_LISTS_FILE = config.word_lists_file

# Game settings
MAX_HIGH_SCORES = config.max_high_scores
