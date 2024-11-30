"""
Utility functions for the Typing Speed Test application.
"""
import json
from typing import List
from .settings import WORD_LISTS_FILE

def load_word_list() -> List[str]:
    """Load the word list from the assets directory."""
    try:
        with open(WORD_LISTS_FILE, 'r') as f:
            return json.load(f)['words']
    except FileNotFoundError:
        # Fallback to default word list if file doesn't exist
        return ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I"]

def calculate_wpm(total_words: int, time_taken: float) -> float:
    """Calculate words per minute."""
    if time_taken == 0:
        return 0
    return (total_words / time_taken) * 60

def calculate_accuracy(typed_text: str, target_text: str) -> float:
    """Calculate typing accuracy percentage."""
    if not target_text:
        return 0
    correct_chars = sum(1 for t, r in zip(typed_text, target_text) if t == r)
    return (correct_chars / len(target_text)) * 100
