"""
Pytest configuration and fixtures.
"""
import os
import tempfile
from pathlib import Path
import pytest
import tkinter as tk
from .test_helpers import (
    create_test_scores_file,
    create_test_word_list,
    get_sample_scores,
    get_sample_words
)

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "gui: mark test as requiring GUI"
    )

@pytest.fixture(scope="session")
def xvfb():
    """Setup virtual display if running in CI."""
    if os.environ.get('CI'):
        try:
            from xvfbwrapper import Xvfb
            vdisplay = Xvfb()
            vdisplay.start()
            yield vdisplay
            vdisplay.stop()
        except ImportError:
            pytest.skip("xvfbwrapper not installed")
    else:
        yield None

@pytest.fixture
def tk_root(xvfb):
    """Create a Tkinter root window for tests."""
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def test_scores_file(temp_dir):
    """Create a temporary scores file with sample data."""
    scores_file = temp_dir / "test_scores.json"
    create_test_scores_file(scores_file, get_sample_scores())
    return scores_file

@pytest.fixture
def test_word_list_file(temp_dir):
    """Create a temporary word list file with sample words."""
    word_list_file = temp_dir / "test_words.json"
    create_test_word_list(word_list_file, get_sample_words())
    return word_list_file

@pytest.fixture
def test_env(monkeypatch):
    """Set up test environment variables."""
    env_vars = {
        'APP_ENV': 'test',
        'MAX_HIGH_SCORES': '5',
        'WINDOW_SIZE': '800x600',
        'WINDOW_TITLE': 'Typing Speed Test',
        'PRIMARY_COLOR': '#2C3E50',
        'SECONDARY_COLOR': '#ECF0F1',
        'ACCENT_COLOR': '#3498DB'
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

@pytest.fixture
def mock_config(test_env, test_scores_file, test_word_list_file):
    """Create a mock configuration for testing."""
    return {
        'env': test_env['APP_ENV'],
        'max_high_scores': int(test_env['MAX_HIGH_SCORES']),
        'window_size': test_env['WINDOW_SIZE'],
        'window_title': test_env['WINDOW_TITLE'],
        'colors': {
            'primary': test_env['PRIMARY_COLOR'],
            'secondary': test_env['SECONDARY_COLOR'],
            'accent': test_env['ACCENT_COLOR']
        },
        'files': {
            'scores': str(test_scores_file),
            'words': str(test_word_list_file)
        }
    }
