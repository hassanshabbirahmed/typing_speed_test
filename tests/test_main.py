"""Tests for main entry point."""
import tkinter as tk
import pytest
from unittest.mock import patch, MagicMock
from src.main import main

def test_main():
    """Test main function."""
    # Mock tkinter.Tk
    mock_root = MagicMock()
    mock_root.mainloop = MagicMock()
    
    with patch('tkinter.Tk', return_value=mock_root), \
         patch('src.main.TypingSpeedGUI') as mock_gui:
        # Run main
        main()
        
        # Verify
        mock_gui.assert_called_once_with(mock_root)
        mock_root.mainloop.assert_called_once()
