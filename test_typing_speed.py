import unittest
from main import TypingSpeedTest
import tkinter as tk

class TestTypingSpeedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.app = TypingSpeedTest(cls.root)

    def setUp(self):
        self.app.display_text.delete('1.0', tk.END)
        self.app.current_text = ""
        self.app.start_time = None
        self.app.word_count = 25

    def test_initial_state(self):
        """Test the initial state of the application"""
        self.assertIsNone(self.app.start_time)
        self.assertEqual(self.app.word_count, 25)
        self.assertEqual(self.app.current_text, "")

    def test_word_list(self):
        """Test that word list exists and is not empty"""
        self.assertGreater(len(self.app.word_list), 0)
        self.assertIsInstance(self.app.word_list, list)
        self.assertTrue(all(isinstance(word, str) for word in self.app.word_list))

    def test_window_properties(self):
        """Test window properties"""
        self.assertEqual(self.app.root.title(), "Typing Speed Test")
        # Check that geometry is set (format should be WxH or WxH+X+Y)
        geometry = self.app.root.geometry()
        self.assertRegex(geometry, r'\d+x\d+(?:\+\d+\+\d+)?')

    def test_ui_elements(self):
        """Test that main UI elements exist"""
        self.assertIsInstance(self.app.display_text, tk.Text)
        self.assertIsInstance(self.app.text_frame, tk.Frame)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

if __name__ == '__main__':
    unittest.main()
