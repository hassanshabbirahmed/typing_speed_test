"""Tests for utility functions."""
import os
import pytest
from src.utils import calculate_wpm, calculate_accuracy, load_word_list

def test_calculate_wpm():
    """Test WPM calculation."""
    # Test normal case
    assert calculate_wpm("word1 word2 word3", 60) == 3.0  # 3 words in 1 minute = 3 WPM
    assert calculate_wpm("word1 word2", 30) == 4.0  # 2 words in 0.5 minutes = 4 WPM
    
    # Test edge cases
    assert calculate_wpm("", 60) == 0.0  # Empty text
    assert calculate_wpm("word", 0) == 0.0  # Zero time
    assert calculate_wpm("word", -1) == 0.0  # Negative time

def test_calculate_accuracy():
    """Test accuracy calculation."""
    # Test perfect match
    assert calculate_accuracy("test text", "test text") == 100.0
    
    # Test partial match
    assert calculate_accuracy("test text", "test") == 50.0
    assert calculate_accuracy("test text", "test texting") == 50.0
    
    # Test no match
    assert calculate_accuracy("test text", "wrong words") == 0.0
    
    # Test empty strings
    assert calculate_accuracy("", "") == 100.0
    assert calculate_accuracy("test", "") == 0.0
    assert calculate_accuracy("", "test") == 0.0

def test_load_word_list(test_word_list_file):
    """Test word list loading."""
    # Test loading from file
    words = load_word_list(test_word_list_file)
    assert isinstance(words, list)
    assert len(words) > 0
    assert all(isinstance(word, str) for word in words)
    
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        load_word_list("nonexistent.txt")
    
    # Test with empty file
    empty_file = os.path.join(os.path.dirname(test_word_list_file), "empty.txt")
    with open(empty_file, "w") as f:
        pass
    words = load_word_list(empty_file)
    assert len(words) == 0
