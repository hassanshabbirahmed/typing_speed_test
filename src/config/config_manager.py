"""
Configuration management for the Typing Speed Test application.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import json
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Config:
    """Configuration data class."""
    env: str
    debug: bool
    data_dir: Path
    scores_file: Path
    word_lists_file: Path
    max_high_scores: int
    window_size: str
    window_title: str
    window_bg: str
    primary_color: str
    secondary_color: str
    title_font: tuple
    text_font: tuple
    difficulties: Dict[str, Dict[str, Any]]

class ConfigManager:
    """Manages application configuration."""
    
    _instance: Optional['ConfigManager'] = None
    _config: Optional[Config] = None
    
    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration based on environment."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Determine environment
        env = os.getenv('APP_ENV', 'development')
        
        # Set base paths
        base_dir = Path(__file__).parent.parent.parent
        data_dir = base_dir / 'data'
        assets_dir = base_dir / 'assets'
        
        # Create directories if they don't exist
        data_dir.mkdir(exist_ok=True)
        assets_dir.mkdir(exist_ok=True)
        
        # Load difficulties from file
        difficulties_file = assets_dir / 'difficulties.json'
        if not difficulties_file.exists():
            difficulties = {
                'easy': {'words': 15, 'time_limit': 120},
                'medium': {'words': 25, 'time_limit': 60},
                'hard': {'words': 40, 'time_limit': 45}
            }
            difficulties_file.write_text(json.dumps(difficulties, indent=4))
        else:
            difficulties = json.loads(difficulties_file.read_text())
        
        # Create configuration
        self._config = Config(
            env=env,
            debug=env == 'development',
            data_dir=data_dir,
            scores_file=data_dir / 'typing_scores.json',
            word_lists_file=assets_dir / 'word_lists.json',
            max_high_scores=int(os.getenv('MAX_HIGH_SCORES', '10')),
            window_size=os.getenv('WINDOW_SIZE', '800x400'),
            window_title=os.getenv('WINDOW_TITLE', 'Typing Speed Test'),
            window_bg=os.getenv('WINDOW_BG', '#f0f0f0'),
            primary_color=os.getenv('PRIMARY_COLOR', '#333333'),
            secondary_color=os.getenv('SECONDARY_COLOR', '#f0f0f0'),
            title_font=('Helvetica', 24, 'bold'),
            text_font=('Helvetica', 12),
            difficulties=difficulties
        )
    
    @property
    def config(self) -> Config:
        """Get the current configuration."""
        return self._config

def get_config() -> Config:
    """Get the current configuration singleton."""
    return ConfigManager().config
