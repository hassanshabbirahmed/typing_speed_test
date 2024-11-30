"""
Main entry point for the Typing Speed Test application.
"""
import tkinter as tk
from gui import TypingSpeedGUI

def main():
    root = tk.Tk()
    app = TypingSpeedGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
