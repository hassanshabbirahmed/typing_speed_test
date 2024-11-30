"""
GUI components for the Typing Speed Test application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from pathlib import Path
from .game_logic import GameManager
from .high_scores import HighScores
from .settings import (
    WINDOW_SIZE, WINDOW_TITLE, WINDOW_BG,
    TITLE_FONT, TEXT_FONT, PRIMARY_COLOR
)
import time

class TypingSpeedGUI:
    """Main GUI class for the Typing Speed Test application."""
    
    def __init__(self, root: tk.Tk, word_list_file: Optional[Path] = None, scores_file: Optional[Path] = None):
        """Initialize the GUI."""
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG)
        
        word_list_path = word_list_file or Path("assets/wordlist.txt")
        scores_path = scores_file or Path("data/scores.json")
        
        self.game = GameManager(word_list_path)
        self.high_scores = HighScores(scores_path)
        self.current_text = ""
        self.typed_chars = 0
        self.timer_id = None
        
        # Initialize difficulty variable
        self.difficulty_var = tk.StringVar(value='medium')
        self.difficulty_var.trace_add('write', self._on_difficulty_change)
        
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self) -> None:
        """Create GUI widgets."""
        # Title
        self.title_label = ttk.Label(
            self.root,
            text="Typing Speed Test",
            font=TITLE_FONT,
            background=WINDOW_BG,
            foreground=PRIMARY_COLOR
        )
        self.title_label.pack(pady=20)
        
        # Difficulty selection
        difficulty_frame = ttk.Frame(self.root)
        difficulty_frame.pack(pady=10)
        
        ttk.Label(difficulty_frame, text="Difficulty:").pack(side=tk.LEFT, padx=5)
        for diff in ['easy', 'medium', 'hard']:
            ttk.Radiobutton(
                difficulty_frame,
                text=diff.capitalize(),
                variable=self.difficulty_var,
                value=diff
            ).pack(side=tk.LEFT, padx=5)
        
        # Text display
        self.text_display = tk.Text(
            self.root,
            height=3,
            width=50,
            font=TEXT_FONT,
            wrap=tk.WORD,
            state='disabled'
        )
        self.text_display.pack(pady=20)
        
        # Input field
        self.input_field = ttk.Entry(
            self.root,
            width=50,
            font=TEXT_FONT,
            state='disabled'
        )
        self.input_field.pack(pady=10)
        
        # Timer label
        self.timer_label = ttk.Label(
            self.root,
            text="Time: 0",
            font=TEXT_FONT
        )
        self.timer_label.pack(pady=10)
        
        # Control buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Start button
        self.start_button = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_game
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop_game,
            state='disabled'
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_game,
            state='disabled'
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Stats frame
        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(pady=10)
        
        self.wpm_label = ttk.Label(
            stats_frame,
            text="0 WPM",
            font=TEXT_FONT
        )
        self.wpm_label.pack(side=tk.LEFT, padx=10)
        
        self.accuracy_label = ttk.Label(
            stats_frame,
            text="100%",
            font=TEXT_FONT
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=10)
    
    def _setup_bindings(self) -> None:
        """Setup keyboard bindings."""
        self.input_field.bind('<KeyRelease>', self.check_progress)
    
    def start_game(self) -> None:
        """Start a new typing test."""
        self.game.start_game(self.difficulty_var.get())
        self.current_text = self.game.current_text
        self.text_display.configure(state='normal')
        self.text_display.delete('1.0', tk.END)
        self.text_display.insert('1.0', self.current_text)
        self.text_display.configure(state='disabled')
        self.input_field.configure(state='normal')
        self.input_field.delete(0, tk.END)
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.reset_button.configure(state='normal')
        self._update_timer()
        
    def stop_game(self) -> None:
        """Stop the current typing test."""
        if not self.game.start_time:
            return
            
        if messagebox.askyesno("Confirm Stop", "Are you sure you want to stop the test?"):
            self.end_test()
            
    def end_test(self) -> None:
        """End the typing test."""
        if not self.game.start_time:
            return
            
        results = self.game.calculate_results(self.input_field.get())
        self.high_scores.add_score(
            results['wpm'],
            results['accuracy'],
            self.game.difficulty
        )
        
        self.input_field.configure(state='disabled')
        self.start_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.reset_button.configure(state='disabled')
        
        messagebox.showinfo(
            "Test Complete",
            f"WPM: {results['wpm']}\n"
            f"Accuracy: {results['accuracy']}%\n"
            f"Time: {results['time']} seconds"
        )

    def reset_game(self) -> None:
        """Reset the game state."""
        self.game.reset()
        self.current_text = ""
        self.typed_chars = 0
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.text_display.configure(state='normal')
        self.text_display.delete('1.0', tk.END)
        self.text_display.configure(state='disabled')
        self.input_field.configure(state='disabled')
        self.input_field.delete(0, tk.END)
        self.start_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.reset_button.configure(state='disabled')
        self.timer_label.configure(text="Time: 0")
        self.wpm_label.configure(text="0 WPM")
        self.accuracy_label.configure(text="100%")
    
    def check_progress(self, event: Optional[tk.Event] = None) -> None:
        """Check typing progress."""
        if not self.game.start_time:
            return
            
        typed_text = self.input_field.get()
        self.typed_chars = len(typed_text)
        
        # Update text display colors
        self.text_display.configure(state='normal')
        self.text_display.delete('1.0', tk.END)
        self.text_display.insert('1.0', self.current_text)
        
        # Color the text based on correctness
        for i, (typed_char, correct_char) in enumerate(
            zip(typed_text, self.current_text[:len(typed_text)])
        ):
            tag = 'correct' if typed_char == correct_char else 'incorrect'
            self.text_display.tag_add(tag, f'1.{i}', f'1.{i+1}')
        
        self.text_display.configure(state='disabled')
        
        # Update stats
        results = self.game.calculate_results(typed_text)
        self.wpm_label.configure(text=f"{results['wpm']} WPM")
        self.accuracy_label.configure(text=f"{results['accuracy']}%")
        
        # Check if test is complete
        if len(typed_text) >= len(self.current_text) or self.game.is_time_up():
            self.end_test()
    
    def _on_difficulty_change(self, *args) -> None:
        """Handle difficulty change."""
        difficulty = self.difficulty_var.get()
        self.game.set_difficulty(difficulty)
    
    def _update_timer(self) -> None:
        """Update the timer display."""
        if not self.game.start_time:
            return
            
        elapsed = int(time.time() - self.game.start_time)
        self.timer_label.configure(text=f"Time: {elapsed}")
        
        if not self.game.is_time_up():
            self.timer_id = self.root.after(100, self._update_timer)
        else:
            self.end_test()
            
    def destroy(self) -> None:
        """Clean up resources."""
        if hasattr(self, 'root'):
            self.root.destroy()
