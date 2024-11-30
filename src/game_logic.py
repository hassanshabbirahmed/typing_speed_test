"""Game logic for the typing speed test."""
import time
import random
from pathlib import Path
from typing import Dict, List, Optional

from .utils import calculate_wpm, calculate_accuracy
from .settings import DIFFICULTIES

class GameManager:
    """Manages game state and logic."""

    def __init__(self, word_list_file: Path):
        """Initialize game manager."""
        self.word_list_file = Path(word_list_file)
        self.word_list: List[str] = []
        self.current_text = ""
        self.start_time: Optional[float] = None
        self.difficulty = 'medium'
        self.word_count = DIFFICULTIES[self.difficulty]['words']
        self.time_limit = DIFFICULTIES[self.difficulty]['time_limit']
        
        self._load_words()

    def _load_words(self) -> None:
        """Load word list from file."""
        with open(self.word_list_file, 'r') as f:
            self.word_list = [word.strip() for word in f.readlines() if word.strip()]

    def set_difficulty(self, difficulty: str) -> None:
        """Set game difficulty."""
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        
        self.difficulty = difficulty
        self.word_count = DIFFICULTIES[difficulty]['words']
        self.time_limit = DIFFICULTIES[difficulty]['time_limit']

    def generate_text(self) -> str:
        """Generate text for typing test."""
        if len(self.word_list) < self.word_count:
            # If not enough words, duplicate the list
            self.word_list = self.word_list * (self.word_count // len(self.word_list) + 1)
        
        words = random.sample(self.word_list, self.word_count)
        self.current_text = " ".join(words)
        return self.current_text

    def start_game(self, difficulty: Optional[str] = None) -> None:
        """Start a new game."""
        if difficulty:
            self.set_difficulty(difficulty)
        self.generate_text()
        self.start_time = time.time()

    def reset(self) -> None:
        """Reset game state."""
        self.current_text = ""
        self.start_time = None

    def get_elapsed_time(self) -> float:
        """Get elapsed time since game start."""
        if not self.start_time:
            return 0.0
        return time.time() - self.start_time

    def is_time_up(self) -> bool:
        """Check if time limit is reached."""
        if not self.time_limit or not self.start_time:
            return False
        return self.get_elapsed_time() >= self.time_limit

    def calculate_results(self, typed_text: str) -> Dict[str, float]:
        """Calculate typing test results."""
        elapsed_time = self.get_elapsed_time()
        wpm = calculate_wpm(typed_text, elapsed_time)
        accuracy = calculate_accuracy(typed_text, self.current_text)
        
        return {
            'wpm': wpm,
            'accuracy': accuracy,
            'time': elapsed_time
        }
