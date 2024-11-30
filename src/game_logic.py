"""
Core game logic for the Typing Speed Test application.
"""
from typing import List, Dict, Optional, Tuple
import random
import time
from src.utils import calculate_wpm, calculate_accuracy, load_word_list
from src.settings import DIFFICULTIES

class GameManager:
    """Manages the core game logic for the typing speed test."""
    
    def __init__(self):
        self.word_list: List[str] = load_word_list()
        self.current_text: str = ""
        self.start_time: Optional[float] = None
        self.current_difficulty: str = 'medium'
        self.word_count: int = DIFFICULTIES[self.current_difficulty]['words']
        self.time_limit: Optional[int] = DIFFICULTIES[self.current_difficulty]['time_limit']
        
    def generate_text(self) -> str:
        """Generate random text for typing test based on current difficulty."""
        selected_words = random.sample(self.word_list, self.word_count)
        self.current_text = ' '.join(selected_words)
        return self.current_text
    
    def start_game(self) -> None:
        """Start a new game."""
        self.start_time = time.time()
        self.generate_text()
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set the game difficulty."""
        if difficulty in DIFFICULTIES:
            self.current_difficulty = difficulty
            self.word_count = DIFFICULTIES[difficulty]['words']
            self.time_limit = DIFFICULTIES[difficulty]['time_limit']
    
    def calculate_results(self, typed_text: str) -> Dict[str, float]:
        """Calculate typing test results."""
        if not self.start_time:
            return {'wpm': 0, 'accuracy': 0, 'time': 0}
            
        end_time = time.time()
        time_taken = end_time - self.start_time
        
        # Calculate words per minute
        word_count = len(typed_text.split())
        wpm = calculate_wpm(word_count, time_taken)
        
        # Calculate accuracy
        accuracy = calculate_accuracy(typed_text, self.current_text)
        
        return {
            'wpm': round(wpm, 2),
            'accuracy': round(accuracy, 2),
            'time': round(time_taken, 2)
        }
    
    def is_time_up(self) -> bool:
        """Check if the time limit has been reached."""
        if not self.time_limit or not self.start_time:
            return False
        return (time.time() - self.start_time) >= self.time_limit
    
    def get_remaining_time(self) -> Optional[int]:
        """Get remaining time in seconds."""
        if not self.time_limit or not self.start_time:
            return None
        remaining = self.time_limit - (time.time() - self.start_time)
        return max(0, int(remaining))
