"""
Test configuration and fixtures.
"""
import os
import json
import pytest
import tkinter as tk
from pathlib import Path
from xvfbwrapper import Xvfb
from .test_helpers import (
    get_sample_scores,
    get_sample_words
)

# Constants
MAX_HIGH_SCORES = 10

@pytest.fixture(scope="session")
def xvfb():
    """Start virtual display for GUI tests."""
    try:
        vdisplay = Xvfb(width=1280, height=720, colordepth=24)
        vdisplay.start()
        yield vdisplay
        vdisplay.stop()
    except (EnvironmentError, OSError) as e:
        pytest.skip(f"Xvfb not available: {e}")

@pytest.fixture
def tk_root(xvfb):
    """Create Tkinter root window."""
    root = None
    try:
        root = tk.Tk()
        root.geometry("800x600")  # Set a fixed size for consistency
        yield root
    except tk.TclError as e:
        pytest.skip(f"Could not create Tkinter window: {e}")
    finally:
        if root:
            try:
                root.destroy()
            except tk.TclError:
                pass  # Window might already be destroyed

@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary directory for test files."""
    return tmp_path

@pytest.fixture
def test_word_list_file(temp_dir):
    """Create test word list file."""
    word_list = get_sample_words()
    word_list_file = temp_dir / "test_words.txt"
    word_list_file.write_text("\n".join(word_list))
    return word_list_file

@pytest.fixture
def test_scores_file(temp_dir):
    """Create test scores file."""
    scores = get_sample_scores()
    scores_file = temp_dir / "test_scores.json"
    scores_file.write_text(json.dumps(scores))
    return scores_file

@pytest.fixture
def test_env():
    """Set up test environment variables."""
    os.environ['APP_ENV'] = 'test'
    os.environ['MAX_HIGH_SCORES'] = str(MAX_HIGH_SCORES)
    return {
        'APP_ENV': 'test',
        'MAX_HIGH_SCORES': MAX_HIGH_SCORES
    }

@pytest.fixture
def mock_config(test_env, test_scores_file, test_word_list_file):
    """Create a mock configuration for testing."""
    return {
        'env': test_env['APP_ENV'],
        'max_high_scores': int(test_env['MAX_HIGH_SCORES']),
        'files': {
            'scores': str(test_scores_file),
            'words': str(test_word_list_file)
        }
    }
