"""
Utility functions for the typing speed test.
"""
from pathlib import Path
from typing import List

def calculate_wpm(typed_text: str, elapsed_time: float) -> int:
    """Calculate words per minute as a whole number."""
    if elapsed_time <= 0:
        return 0
    
    word_count = len(typed_text.split())
    minutes = elapsed_time / 60
    return round(word_count / minutes) if minutes > 0 else 0

def calculate_accuracy(typed_text: str, target_text: str) -> float:
    """Calculate typing accuracy as a percentage."""
    if not typed_text and not target_text:
        return 100.0
    if not typed_text or not target_text:
        return 0.0

    typed_words = typed_text.split()
    target_words = target_text.split()
    
    # Count matching words
    correct_words = sum(1 for t, r in zip(typed_words, target_words) if t == r)
    total_words = max(len(typed_words), len(target_words))
    
    return (correct_words / total_words) * 100.0

def load_word_list(word_list_file: Path) -> List[str]:
    """Load word list from file."""
    if not Path(word_list_file).exists():
        raise FileNotFoundError(f"Word list file not found: {word_list_file}")
        
    with open(word_list_file, 'r') as f:
        words = [word.strip() for word in f.readlines() if word.strip()]
    
    return words
