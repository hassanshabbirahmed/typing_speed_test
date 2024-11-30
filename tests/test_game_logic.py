"""Tests for game logic functionality."""
import time
import pytest
from src.game_logic import GameManager

@pytest.fixture
def game_manager(test_word_list_file):
    """Fixture for GameManager instance."""
    manager = GameManager(test_word_list_file)
    manager.word_count = 3  # Use smaller word count for testing
    return manager

def test_game_manager_initialization(game_manager):
    """Test GameManager initialization."""
    assert game_manager.word_list
    assert game_manager.current_text == ""
    assert game_manager.start_time is None
    assert game_manager.difficulty == 'medium'

def test_generate_text(game_manager):
    """Test text generation."""
    text = game_manager.generate_text()
    assert isinstance(text, str)
    assert len(text.split()) == game_manager.word_count
    assert text == game_manager.current_text

def test_difficulty_settings(game_manager):
    """Test difficulty changes."""
    # Test medium difficulty (default)
    game_manager.set_difficulty('medium')
    assert game_manager.word_count == 25
    assert game_manager.time_limit == 60

    # Test easy difficulty
    game_manager.set_difficulty('easy')
    assert game_manager.word_count == 15
    assert game_manager.time_limit == 120

    # Test hard difficulty
    game_manager.set_difficulty('hard')
    assert game_manager.word_count == 40
    assert game_manager.time_limit == 45

def test_calculate_results(game_manager):
    """Test results calculation."""
    test_text = "test text"
    game_manager.start_game()
    game_manager.current_text = test_text  # Set current_text after start_game to avoid it being overwritten

    # Wait a bit to simulate typing time
    time.sleep(0.1)

    # Simulate typing with exact match
    results = game_manager.calculate_results(test_text)

    assert isinstance(results, dict)
    assert 'wpm' in results
    assert 'accuracy' in results
    assert 'time' in results
    assert results['accuracy'] == 100.0
    assert results['wpm'] > 0
    assert results['time'] > 0

def test_time_management(game_manager):
    """Test time-related functions."""
    game_manager.word_count = 3  # Use smaller word count for testing
    game_manager.start_game()
    assert game_manager.start_time is not None

    time.sleep(0.1)
    elapsed = game_manager.get_elapsed_time()
    assert elapsed > 0

    # Test time limit
    game_manager.set_difficulty('easy')  # 120 seconds
    assert not game_manager.is_time_up()

    # Reset and test with very short time
    game_manager.reset()
    game_manager.set_difficulty('hard')  # 45 seconds
    game_manager.start_game()
    assert not game_manager.is_time_up()
