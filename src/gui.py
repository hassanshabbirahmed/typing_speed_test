"""
GUI components for the Typing Speed Test application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
import time
from src.game_logic import GameManager
from src.settings import (
    WINDOW_SIZE, WINDOW_TITLE, WINDOW_BG,
    TITLE_FONT, TEXT_FONT, PRIMARY_COLOR
)

class TypingSpeedGUI:
    """Main GUI class for the Typing Speed Test application."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG)
        
        self.game = GameManager()
        self.timer_id: Optional[str] = None
        
        self.create_widgets()
        self.setup_bindings()
    
    def create_widgets(self) -> None:
        """Create and setup all GUI widgets."""
        # Title
        title = tk.Label(
            self.root,
            text=WINDOW_TITLE,
            font=TITLE_FONT,
            bg=WINDOW_BG,
            fg=PRIMARY_COLOR
        )
        title.pack(pady=10)
        
        # Difficulty selector
        difficulty_frame = tk.Frame(self.root, bg=WINDOW_BG)
        difficulty_frame.pack(pady=5)
        
        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=TEXT_FONT,
            bg=WINDOW_BG
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value='medium')
        for diff in ['easy', 'medium', 'hard']:
            ttk.Radiobutton(
                difficulty_frame,
                text=diff.capitalize(),
                value=diff,
                variable=self.difficulty_var,
                command=self.change_difficulty
            ).pack(side=tk.LEFT, padx=5)
        
        # Display text
        self.display_text = tk.Text(
            self.root,
            height=3,
            width=50,
            font=TEXT_FONT,
            wrap=tk.WORD,
            state='disabled'
        )
        self.display_text.pack(pady=20, padx=20)
        
        # Entry field
        self.type_entry = tk.Entry(
            self.root,
            font=TEXT_FONT,
            width=50,
            state='disabled'
        )
        self.type_entry.pack(pady=10)
        
        # Timer label
        self.timer_label = tk.Label(
            self.root,
            text="",
            font=TEXT_FONT,
            bg=WINDOW_BG
        )
        self.timer_label.pack(pady=5)
        
        # Results label
        self.results_label = tk.Label(
            self.root,
            text="",
            font=TEXT_FONT,
            bg=WINDOW_BG
        )
        self.results_label.pack(pady=5)
        
        # Start button
        self.start_button = tk.Button(
            self.root,
            text="Start Test",
            command=self.start_test,
            font=TEXT_FONT
        )
        self.start_button.pack(pady=10)
    
    def setup_bindings(self) -> None:
        """Setup keyboard and event bindings."""
        self.type_entry.bind('<Return>', lambda e: self.check_completion())
    
    def start_test(self) -> None:
        """Start a new typing test."""
        self.game.start_game()
        self.display_text.config(state='normal')
        self.display_text.delete('1.0', tk.END)
        self.display_text.insert('1.0', self.game.current_text)
        self.display_text.config(state='disabled')
        
        self.type_entry.config(state='normal')
        self.type_entry.delete(0, tk.END)
        self.type_entry.focus()
        
        self.start_button.config(state='disabled')
        self.results_label.config(text="")
        
        if self.game.time_limit:
            self.update_timer()
    
    def update_timer(self) -> None:
        """Update the timer display."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        remaining_time = self.game.get_remaining_time()
        if remaining_time is not None:
            self.timer_label.config(text=f"Time remaining: {remaining_time}s")
            if remaining_time > 0:
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.end_test()
        else:
            self.timer_label.config(text="")
    
    def end_test(self) -> None:
        """End the current typing test."""
        typed_text = self.type_entry.get()
        results = self.game.calculate_results(typed_text)
        
        result_text = (
            f"WPM: {results['wpm']}\n"
            f"Accuracy: {results['accuracy']}%\n"
            f"Time: {results['time']}s"
        )
        self.results_label.config(text=result_text)
        
        self.type_entry.config(state='disabled')
        self.start_button.config(state='normal')
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
    
    def check_completion(self) -> None:
        """Check if the typing test is complete."""
        if self.game.is_time_up():
            self.end_test()
        else:
            self.end_test()
    
    def change_difficulty(self) -> None:
        """Change the game difficulty."""
        self.game.set_difficulty(self.difficulty_var.get())
