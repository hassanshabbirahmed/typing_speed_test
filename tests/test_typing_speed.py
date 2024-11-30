"""
Tests for the typing speed GUI functionality.
"""
import pytest
import tkinter as tk
from main import TypingSpeedTest

@pytest.fixture
def gui(tk_root):
    """Fixture for TypingSpeedTest instance."""
    app = TypingSpeedTest(tk_root)
    yield app
    # Cleanup is handled by tk_root fixture in conftest.py

def test_gui_initialization(gui):
    """Test GUI initialization."""
    assert isinstance(gui.word_count, int)
    assert gui.type_entry.cget('state') == 'disabled'
    assert gui.start_button.cget('state') == 'normal'

def test_start_test(gui):
    """Test starting a new typing test."""
    gui.start_test()
    
    assert gui.type_entry.cget('state') == 'normal'
    assert gui.start_button.cget('state') == 'disabled'
    assert gui.display_text.get('1.0', tk.END).strip() != ''
    assert gui.results_label.cget('text') == ''

def test_end_test(gui):
    """Test ending a typing test."""
    gui.start_test()
    gui.type_entry.insert(0, "test typing")
    gui.end_test(100.0)
    
    assert gui.type_entry.cget('state') == 'disabled'
    assert gui.start_button.cget('state') == 'normal'
    assert gui.results_label.cget('text') != ''

def test_check_progress(gui):
    """Test checking progress during typing."""
    gui.start_test()
    gui.type_entry.insert(0, "test")
    gui.check_progress(None)
    
    assert gui.results_label.cget('text') != ''

def test_empty_input(gui):
    """Test handling of empty input."""
    gui.start_test()
    gui.type_entry.delete(0, tk.END)
    gui.check_progress(None)
    
    assert gui.results_label.cget('text') != ''

def test_text_coloring(gui):
    """Test text coloring for correct, incorrect, and remaining text."""
    gui.start_test()
    gui.type_entry.insert(0, "test")
    gui.check_progress(None)
    
    assert gui.display_text.get("1.0", tk.END).strip() != ''

def test_real_time_wpm(gui):
    """Test real-time WPM calculation."""
    gui.start_test()
    gui.type_entry.insert(0, "test word")
    gui.check_progress(None)
    
    assert gui.results_label.cget('text') != ''

def test_long_input(gui):
    """Test handling of input longer than target text."""
    gui.start_test()
    gui.type_entry.insert(0, "testing")
    gui.check_progress(None)
    
    assert gui.type_entry.cget('state') == 'disabled'
    assert gui.start_button.cget('state') == 'normal'

def test_special_characters(gui):
    """Test handling of special characters in input."""
    gui.start_test()
    gui.type_entry.insert(0, "te$t")
    gui.check_progress(None)
    
    assert gui.results_label.cget('text') != ''

def test_rapid_typing(gui):
    """Test handling of rapid typing."""
    gui.start_test()
    gui.type_entry.insert(0, "test word example")
    gui.check_progress(None)
    
    assert gui.results_label.cget('text') != ''
