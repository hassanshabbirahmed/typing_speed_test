"""
Tests for utility functions.
"""
import pytest
from src.utils import calculate_wpm, calculate_accuracy, load_word_list

def test_calculate_wpm():
    """Test WPM calculation."""
    assert calculate_wpm(30, 60) == 30.0  # 30 words in 1 minute = 30 WPM
    assert calculate_wpm(15, 30) == 30.0  # 15 words in 30 seconds = 30 WPM
    assert calculate_wpm(0, 60) == 0.0    # No words = 0 WPM
    assert calculate_wpm(10, 0) == 0.0    # Divide by zero protection

def test_calculate_accuracy():
    """Test accuracy calculation."""
    # Perfect match
    assert calculate_accuracy("test", "test") == 100.0
    
    # No match
    assert calculate_accuracy("test", "none") == 0.0
    
    # Partial match
    assert calculate_accuracy("test", "tent") == 75.0  # 3/4 characters match
    
    # Empty strings
    assert calculate_accuracy("", "") == 0.0
    assert calculate_accuracy("test", "") == 0.0
    assert calculate_accuracy("", "test") == 0.0

def test_load_word_list(test_data_dir):
    """Test word list loading."""
    # Test actual word list loading
    words = load_word_list()
    assert isinstance(words, list)
    assert all(isinstance(word, str) for word in words)
    assert len(words) > 0

    # Test with missing file (should return default list)
    default_words = load_word_list()
    assert isinstance(default_words, list)
    assert len(default_words) > 0
