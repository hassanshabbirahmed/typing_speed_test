"""
Tests for GUI functionality.
"""
import time
import pytest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch, MagicMock
from src.gui import TypingSpeedGUI

@pytest.fixture
def typing_gui(tk_root, test_word_list_file, test_scores_file):
    """Fixture for TypingSpeedGUI instance."""
    gui = None
    try:
        gui = TypingSpeedGUI(tk_root, test_word_list_file, test_scores_file)
        yield gui
    finally:
        if gui:
            try:
                gui.destroy()
            except tk.TclError:
                pass

def test_gui_initialization(typing_gui):
    """Test GUI initialization."""
    assert isinstance(typing_gui.root, tk.Tk)
    assert isinstance(typing_gui.text_display, tk.Text)
    assert isinstance(typing_gui.input_field, ttk.Entry)
    assert isinstance(typing_gui.timer_label, ttk.Label)
    assert isinstance(typing_gui.start_button, ttk.Button)
    assert typing_gui.difficulty_var.get() == 'medium'

def test_difficulty_change(typing_gui):
    """Test difficulty selection."""
    typing_gui.difficulty_var.set('easy')
    typing_gui.root.update()  # Process events
    assert typing_gui.game.difficulty == 'easy'
    assert typing_gui.game.word_count == 15

    typing_gui.difficulty_var.set('hard')
    typing_gui.root.update()  # Process events
    assert typing_gui.game.difficulty == 'hard'
    assert typing_gui.game.word_count == 40

def test_start_game(typing_gui):
    """Test game start functionality."""
    typing_gui.start_game()
    typing_gui.root.update()  # Process events
    
    assert typing_gui.game.current_text
    assert typing_gui.text_display.get("1.0", tk.END).strip()
    assert str(typing_gui.input_field.cget('state')) == 'normal'
    assert str(typing_gui.start_button.cget('state')) == 'disabled'

def test_reset_game(typing_gui):
    """Test game reset functionality."""
    typing_gui.start_game()
    typing_gui.root.update()  # Process events
    
    typing_gui.reset_game()
    typing_gui.root.update()  # Process events
    
    assert not typing_gui.game.current_text
    assert not typing_gui.text_display.get("1.0", tk.END).strip()
    assert str(typing_gui.input_field.cget('state')) == 'disabled'
    assert str(typing_gui.start_button.cget('state')) == 'normal'
    assert typing_gui.timer_label.cget('text') == "Time: 0"

def test_input_validation(typing_gui):
    """Test input field validation."""
    typing_gui.start_game()
    typing_gui.root.update()  # Process events
    
    # Simulate correct input
    typing_gui.input_field.insert(tk.END, "test")
    typing_gui.root.update()  # Process events
    assert typing_gui.input_field.get().strip() == "test"
    
    # Clear input
    typing_gui.input_field.delete(0, tk.END)
    typing_gui.root.update()  # Process events
    assert not typing_gui.input_field.get().strip()

def test_timer_update(typing_gui):
    """Test timer updates."""
    # Set up initial game state
    typing_gui.game.start_time = time.time() - 5  # Started 5 seconds ago
    
    # Update timer display
    typing_gui._update_timer()
    typing_gui.root.update()  # Process events
    
    # Verify timer display
    timer_text = typing_gui.timer_label.cget('text')
    assert timer_text == "Time: 5", f"Expected 'Time: 5' but got '{timer_text}'"
    
    # Verify timer is scheduled
    assert typing_gui.timer_id is not None
