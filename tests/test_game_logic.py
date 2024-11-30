"""
Tests for game logic functionality.
"""
import pytest
from src.game_logic import GameManager
from src.settings import DIFFICULTIES

@pytest.fixture
def game_manager():
    """Fixture for GameManager instance."""
    return GameManager()

def test_game_manager_initialization(game_manager):
    """Test GameManager initialization."""
    assert game_manager.current_difficulty == 'medium'
    assert game_manager.word_count == DIFFICULTIES['medium']['words']
    assert game_manager.time_limit == DIFFICULTIES['medium']['time_limit']

def test_generate_text(game_manager):
    """Test text generation."""
    text = game_manager.generate_text()
    assert isinstance(text, str)
    assert len(text.split()) == game_manager.word_count

def test_difficulty_settings(game_manager):
    """Test difficulty changes."""
    # Test medium difficulty (default)
    assert game_manager.word_count == 25
    assert game_manager.time_limit == 60

    # Test easy difficulty
    game_manager.set_difficulty('easy')
    assert game_manager.word_count == 15
    assert game_manager.time_limit is None

    # Test hard difficulty
    game_manager.set_difficulty('hard')
    assert game_manager.word_count == 40
    assert game_manager.time_limit == 60

def test_calculate_results(game_manager):
    """Test results calculation."""
    game_manager.current_text = "test text"
    game_manager.start_game()
    
    # Simulate typing
    results = game_manager.calculate_results("test text")
    
    assert 'wpm' in results
    assert 'accuracy' in results
    assert 'time' in results
    assert results['accuracy'] == 100.0

def test_time_management(game_manager):
    """Test time-related functions."""
    # Test with no time limit (easy mode)
    game_manager.set_difficulty('easy')
    game_manager.start_game()
    assert not game_manager.is_time_up()
    assert game_manager.get_remaining_time() is None

    # Test with time limit (medium mode)
    game_manager.set_difficulty('medium')
    game_manager.start_game()
    assert not game_manager.is_time_up()
    remaining = game_manager.get_remaining_time()
    assert remaining is not None
    assert 0 <= remaining <= 60
