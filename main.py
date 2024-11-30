import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
from high_scores import HighScores

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x400")
        self.root.configure(bg="#f0f0f0")

        # Initialize variables
        self.current_text = ""
        self.start_time = None
        self.high_scores = HighScores()
        
        # Difficulty settings
        self.difficulties = {
            'easy': {'words': 15, 'time_limit': None},
            'medium': {'words': 25, 'time_limit': 60},
            'hard': {'words': 40, 'time_limit': 60}
        }
        self.current_difficulty = 'medium'
        self.word_count = self.difficulties[self.current_difficulty]['words']
        self.time_limit = self.difficulties[self.current_difficulty]['time_limit']
        
        # Sample words for the typing test
        self.word_list = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
            "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
            "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
            "computer", "programming", "python", "keyboard", "typing", "speed", "test",
            "practice", "software", "developer", "coding", "learning", "skills"
        ]
        
        # Create and pack widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Typing Speed Test", 
                        font=("Helvetica", 24, "bold"),
                        bg="#f0f0f0", fg="#333333")
        title.pack(pady=10)

        # Difficulty selector
        difficulty_frame = tk.Frame(self.root, bg="#f0f0f0")
        difficulty_frame.pack(pady=5)
        
        tk.Label(difficulty_frame, text="Difficulty:", 
                font=("Helvetica", 12),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        difficulty_menu = ttk.OptionMenu(
            difficulty_frame,
            self.difficulty_var,
            self.current_difficulty,
            *self.difficulties.keys(),
            command=self.change_difficulty
        )
        difficulty_menu.pack(side=tk.LEFT)

        # High score display
        self.high_score_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.high_score_label.pack(pady=5)
        self.update_high_score_display()

        # Frame for text display
        self.text_frame = tk.Frame(self.root, bg="#ffffff",
                                 padx=20, pady=20)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Text widget to display text with colors
        self.display_text = tk.Text(self.text_frame,
                                  wrap=tk.WORD,
                                  font=("Helvetica", 14),
                                  height=4,
                                  width=50,
                                  bg="#ffffff")
        self.display_text.pack(expand=True)
        self.display_text.config(state='disabled')

        # Configure text tags for coloring
        self.display_text.tag_configure("correct", foreground="green")
        self.display_text.tag_configure("incorrect", foreground="red")
        self.display_text.tag_configure("remaining", foreground="black")

        # Entry for typing
        self.type_entry = tk.Entry(self.root, 
                                 font=("Helvetica", 14),
                                 width=50)
        self.type_entry.pack(pady=20)
        self.type_entry.bind('<KeyRelease>', self.check_progress)

        # Start button
        self.start_button = tk.Button(self.root, 
                                    text="Start Test",
                                    command=self.start_test,
                                    font=("Helvetica", 12),
                                    bg="#4CAF50",
                                    fg="white",
                                    padx=20)
        self.start_button.pack(pady=10)

        # Results label
        self.results_label = tk.Label(self.root, 
                                    text="",
                                    font=("Helvetica", 12),
                                    bg="#f0f0f0")
        self.results_label.pack(pady=10)

    def generate_text(self):
        # Generate random text from our word list
        selected_words = random.sample(self.word_list, self.word_count)
        return " ".join(selected_words)

    def update_text_display(self, current_input):
        self.display_text.config(state='normal')
        self.display_text.delete(1.0, tk.END)
        
        # Compare current input with target text
        target_words = self.current_text.split()
        input_words = current_input.split()
        remaining_words = target_words[len(input_words):]
        
        # Color the fully typed words
        for i, (target_word, input_word) in enumerate(zip(target_words, input_words)):
            # Add space before word (except first word)
            if i > 0:
                self.display_text.insert(tk.END, " ")
            
            # Compare characters in the current word
            for j, (target_char, input_char) in enumerate(zip(target_word, input_word)):
                if target_char == input_char:
                    self.display_text.insert(tk.END, target_char, "correct")
                else:
                    self.display_text.insert(tk.END, target_char, "incorrect")
            
            # Handle any remaining characters in the target word
            if len(target_word) > len(input_word):
                if i > 0:
                    self.display_text.insert(tk.END, target_word[len(input_word):], "remaining")
        
        # Add any remaining words
        if remaining_words:
            if len(input_words) > 0:
                self.display_text.insert(tk.END, " ")
            self.display_text.insert(tk.END, " ".join(remaining_words), "remaining")
                
        self.display_text.config(state='disabled')

    def start_test(self):
        self.current_text = self.generate_text()
        self.display_text.config(state='normal')
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(1.0, self.current_text, "remaining")
        self.display_text.config(state='disabled')
        self.type_entry.delete(0, tk.END)
        self.type_entry.config(state='normal')
        self.start_time = time.time()
        self.start_button.config(state='disabled')
        self.results_label.config(text="")
        self.type_entry.focus()

    def change_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        self.word_count = self.difficulties[difficulty]['words']
        self.time_limit = self.difficulties[difficulty]['time_limit']
        self.update_high_score_display()
        
        # Update UI to show difficulty settings
        words = self.difficulties[difficulty]['words']
        time = self.difficulties[difficulty]['time_limit'] or "∞"
        messagebox.showinfo(
            "Difficulty Changed",
            f"Changed to {difficulty.title()}:\n"
            f"- {words} words\n"
            f"- Time limit: {time} seconds"
        )

    def update_high_score_display(self):
        best_score = self.high_scores.get_personal_best(self.current_difficulty)
        if best_score:
            self.high_score_label.config(
                text=f"Personal Best ({self.current_difficulty.title()}): "
                     f"{best_score['wpm']} WPM with {best_score['accuracy']}% accuracy"
            )
        else:
            self.high_score_label.config(
                text=f"No high score yet for {self.current_difficulty.title()}"
            )

    def check_progress(self, event):
        if not self.start_time:
            return

        current_input = self.type_entry.get()
        
        # Check time limit
        if self.time_limit:
            time_elapsed = time.time() - self.start_time
            if time_elapsed > self.time_limit:
                self.end_test(self.calculate_accuracy(current_input))
                return
        
        # Update text colors
        self.update_text_display(current_input)
        
        # Calculate accuracy and WPM
        accuracy = self.calculate_accuracy(current_input)
        if len(current_input) > 0:
            time_elapsed = time.time() - self.start_time
            words_typed = len(current_input.split())
            current_wpm = (words_typed / time_elapsed) * 60
        else:
            accuracy = 0
            current_wpm = 0

        # Check if test is complete
        if len(current_input) >= len(self.current_text):
            self.end_test(accuracy)
            return

        # Update current accuracy and WPM
        remaining = ""
        if self.time_limit:
            remaining = f" | Time: {max(0, self.time_limit - (time.time() - self.start_time)):.1f}s"
            
        self.results_label.config(
            text=f"WPM: {current_wpm:.1f} | Accuracy: {accuracy:.1f}%{remaining}")

    def calculate_accuracy(self, current_input):
        correct_chars = sum(1 for i, j in zip(current_input, self.current_text) if i == j)
        total_chars = len(current_input)
        return (correct_chars / total_chars * 100) if total_chars > 0 else 0

    def end_test(self, final_accuracy):
        end_time = time.time()
        time_taken = end_time - self.start_time
        
        # Calculate WPM
        word_count = len(self.current_text.split())
        wpm = (word_count / time_taken) * 60

        # Save score
        self.high_scores.add_score(self.current_difficulty, wpm, final_accuracy)
        self.update_high_score_display()

        # Display results
        result_text = f"Time: {time_taken:.1f}s | WPM: {wpm:.1f} | Accuracy: {final_accuracy:.1f}%"
        self.results_label.config(text=result_text)
        
        self.type_entry.config(state='disabled')
        self.start_button.config(state='normal')
        
        # Show detailed results
        best_score = self.high_scores.get_personal_best(self.current_difficulty)
        if best_score and best_score['wpm'] == round(wpm, 1):
            messagebox.showinfo(
                "Test Complete - New High Score!",
                f"{result_text}\n\nNew Personal Best for {self.current_difficulty.title()}!"
            )
        else:
            messagebox.showinfo("Test Complete", result_text)

def main():
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
