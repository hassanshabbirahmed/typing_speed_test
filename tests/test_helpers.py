"""
Helper functions and utilities for tests.
"""
import json
from pathlib import Path
from typing import Dict, Any

def create_test_scores_file(file_path: Path, scores: Dict[str, Any]) -> None:
    """Create a test scores file with given data."""
    with open(file_path, 'w') as f:
        json.dump(scores, f)

def create_test_word_list(file_path: Path, words: list[str]) -> None:
    """Create a test word list file."""
    with open(file_path, 'w') as f:
        json.dump({'words': words}, f)

def get_sample_scores() -> Dict[str, Any]:
    """Get sample scores data for testing."""
    return {
        'easy': [
            {'wpm': 45.0, 'accuracy': 95.0, 'date': '2023-08-01T10:00:00'},
            {'wpm': 40.0, 'accuracy': 90.0, 'date': '2023-08-01T09:00:00'}
        ],
        'medium': [
            {'wpm': 55.0, 'accuracy': 92.0, 'date': '2023-08-01T11:00:00'},
            {'wpm': 50.0, 'accuracy': 88.0, 'date': '2023-08-01T08:00:00'}
        ],
        'hard': [
            {'wpm': 35.0, 'accuracy': 85.0, 'date': '2023-08-01T12:00:00'},
            {'wpm': 30.0, 'accuracy': 82.0, 'date': '2023-08-01T07:00:00'}
        ]
    }

def get_sample_words() -> list[str]:
    """Get sample word list for testing."""
    return [
        "the", "be", "to", "of", "and", 
        "test", "word", "list", "for", "typing"
    ]
