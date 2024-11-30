"""
Tests for high scores functionality.
"""
import pytest
import json
from pathlib import Path
from src.high_scores import HighScores
from src.settings import MAX_HIGH_SCORES

@pytest.fixture
def high_scores(test_data_dir):
    """Fixture for HighScores instance with test file."""
    scores_file = test_data_dir / "test_scores.json"
    hs = HighScores()
    hs.scores_file = scores_file
    return hs

def test_initialization(high_scores):
    """Test HighScores initialization."""
    assert isinstance(high_scores.scores, dict)
    assert all(diff in high_scores.scores for diff in ['easy', 'medium', 'hard'])
    assert all(isinstance(high_scores.scores[diff], list) for diff in ['easy', 'medium', 'hard'])

def test_add_score(high_scores):
    """Test adding and sorting scores."""
    # Add multiple scores
    high_scores.add_score(50.5, 95.0, "medium")
    high_scores.add_score(60.0, 98.0, "medium")
    high_scores.add_score(45.0, 92.0, "medium")

    scores = high_scores.get_scores("medium")
    assert len(scores) == 3
    assert scores[0]['wpm'] == 60.0
    assert scores[0]['accuracy'] == 98.0
    assert scores[-1]['wpm'] == 45.0

def test_max_scores_limit(high_scores):
    """Test that scores list respects max_scores limit."""
    # Add more than max scores
    for i in range(MAX_HIGH_SCORES + 5):
        high_scores.add_score(50.0 + i, 95.0, "medium")

    scores = high_scores.get_scores("medium")
    assert len(scores) == MAX_HIGH_SCORES
    assert scores[0]['wpm'] == 50.0 + (MAX_HIGH_SCORES + 4)  # Highest score

def test_score_persistence(high_scores):
    """Test that scores are properly saved and loaded."""
    # Add some scores
    high_scores.add_score(55.0, 96.0, "medium")
    high_scores.add_score(65.0, 98.0, "hard")

    # Create new instance with same file
    scores_file = high_scores.scores_file
    new_hs = HighScores()
    new_hs.scores_file = scores_file
    
    # Verify scores were loaded
    assert new_hs.get_scores("medium")[0]['wpm'] == 55.0
    assert new_hs.get_scores("hard")[0]['wpm'] == 65.0

def test_invalid_difficulty(high_scores):
    """Test handling of invalid difficulty levels."""
    # Adding score with invalid difficulty
    high_scores.add_score(50.0, 95.0, "invalid")
    assert "invalid" not in high_scores.scores

    # Getting scores for invalid difficulty
    assert high_scores.get_scores("invalid") == []
