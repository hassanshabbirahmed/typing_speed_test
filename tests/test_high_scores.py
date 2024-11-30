"""
Tests for high scores functionality.
"""
import json
import pytest
from src.high_scores import HighScores

MAX_HIGH_SCORES = 10

@pytest.fixture
def high_scores(temp_dir):
    """Fixture for HighScores instance."""
    # Initialize empty scores file
    scores_file = temp_dir / "test_scores.json"
    scores_data = {
        'easy': [],
        'medium': [],
        'hard': []
    }
    scores_file.write_text(json.dumps(scores_data))
    
    return HighScores(scores_file)

def test_initialization(high_scores):
    """Test HighScores initialization."""
    assert high_scores.scores_file
    assert isinstance(high_scores.scores, dict)
    assert all(difficulty in high_scores.scores for difficulty in ['easy', 'medium', 'hard'])

def test_add_score(high_scores):
    """Test adding and sorting scores."""
    # Add multiple scores
    high_scores.add_score(50.5, 95.0, "medium")
    high_scores.add_score(60.0, 98.0, "medium")
    high_scores.add_score(45.0, 92.0, "medium")

    scores = high_scores.get_scores("medium")
    assert len(scores) == 3
    assert scores[0]['wpm'] == 60.0  # Highest WPM first
    assert scores[-1]['wpm'] == 45.0  # Lowest WPM last

def test_max_scores_limit(high_scores):
    """Test that scores list respects max_scores limit."""
    # Add more than max scores
    for i in range(MAX_HIGH_SCORES + 5):
        high_scores.add_score(50.0 + i, 95.0, "medium")

    scores = high_scores.get_scores("medium")
    assert len(scores) == MAX_HIGH_SCORES
    assert scores[0]['wpm'] == 64.0  # Highest WPM first (50 + 14)
    assert scores[-1]['wpm'] == 55.0  # Only keeps top MAX_HIGH_SCORES (50 + 5)

def test_score_persistence(high_scores, temp_dir):
    """Test that scores are properly saved and loaded."""
    # Add some scores
    high_scores.add_score(50.5, 95.0, "medium")
    high_scores.add_score(60.0, 98.0, "medium")
    
    # Create new instance with same file
    scores_file = temp_dir / "test_scores.json"
    new_high_scores = HighScores(scores_file)
    
    # Verify scores were loaded
    scores = new_high_scores.get_scores("medium")
    assert len(scores) == 2
    assert scores[0]['wpm'] == 60.0
    assert scores[1]['wpm'] == 50.5

def test_invalid_difficulty(high_scores):
    """Test handling of invalid difficulty levels."""
    with pytest.raises(ValueError, match="Invalid difficulty"):
        high_scores.add_score(50.0, 95.0, "invalid")
        
def test_empty_scores_file(temp_dir):
    """Test initialization with empty scores file."""
    scores_file = temp_dir / "empty_scores.json"
    high_scores = HighScores(scores_file)
    assert all(difficulty in high_scores.scores for difficulty in ['easy', 'medium', 'hard'])
    assert all(len(scores) == 0 for scores in high_scores.scores.values())
    
def test_corrupted_scores_file(temp_dir):
    """Test handling of corrupted scores file."""
    scores_file = temp_dir / "corrupted_scores.json"
    scores_file.write_text("invalid json")
    
    high_scores = HighScores(scores_file)
    assert all(difficulty in high_scores.scores for difficulty in ['easy', 'medium', 'hard'])
    assert all(len(scores) == 0 for scores in high_scores.scores.values())
