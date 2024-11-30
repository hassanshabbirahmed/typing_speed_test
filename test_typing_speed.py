import unittest
from main import TypingSpeedTest
import tkinter as tk
import time

class TestTypingSpeedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.app = TypingSpeedTest(cls.root)

    def setUp(self):
        """Reset the application state before each test"""
        # Clear display text
        self.app.display_text.config(state='normal')
        self.app.display_text.delete('1.0', tk.END)
        self.app.display_text.config(state='disabled')
        
        # Clear entry field
        self.app.type_entry.delete(0, tk.END)
        self.app.type_entry.config(state='normal')
        
        # Reset variables
        self.app.current_text = ""
        self.app.start_time = None
        self.app.word_count = 25
        
        # Reset labels and buttons
        self.app.results_label.config(text="")
        self.app.start_button.config(state='normal')

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
        geometry = self.app.root.geometry()
        self.assertRegex(geometry, r'\d+x\d+(?:\+\d+\+\d+)?')

    def test_ui_elements(self):
        """Test that main UI elements exist"""
        self.assertIsInstance(self.app.display_text, tk.Text)
        self.assertIsInstance(self.app.text_frame, tk.Frame)

    def test_generate_text(self):
        """Test text generation"""
        text = self.app.generate_text()
        self.assertIsInstance(text, str)
        self.assertEqual(len(text.split()), self.app.word_count)
        # Verify all words are from word_list
        for word in text.split():
            self.assertIn(word, self.app.word_list)

    def test_start_test(self):
        """Test starting a new test"""
        # Clear the entry field first
        self.app.type_entry.delete(0, tk.END)
        
        self.app.start_test()
        self.assertIsNotNone(self.app.start_time)
        self.assertNotEqual(self.app.current_text, "")
        self.assertEqual(self.app.type_entry.get(), "")
        self.assertEqual(self.app.results_label.cget("text"), "")
        self.assertEqual(self.app.start_button.cget("state"), "disabled")
        self.assertEqual(self.app.type_entry.cget("state"), "normal")

    def test_check_progress_accuracy(self):
        """Test accuracy calculation during typing"""
        self.app.start_test()
        self.app.current_text = "test word"
        
        # Test perfect typing
        self.app.type_entry.insert(0, "test")
        self.app.check_progress(None)
        self.assertIn("Accuracy: 100.0%", self.app.results_label.cget("text"))
        
        # Test imperfect typing
        self.app.type_entry.delete(0, tk.END)
        self.app.type_entry.insert(0, "tast")
        self.app.check_progress(None)
        self.assertIn("Accuracy: 75.0%", self.app.results_label.cget("text"))

    def test_end_test(self):
        """Test ending the test"""
        self.app.start_test()
        self.app.start_time = time.time() - 60  # Simulate 60 seconds passed
        self.app.current_text = "test word"  # 2 words
        
        self.app.end_test(100.0)  # 100% accuracy
        
        result_text = self.app.results_label.cget("text")
        self.assertIn("Time: 60", result_text)
        self.assertIn("WPM: 2.0", result_text)  # 2 words in 60 seconds = 2 WPM
        self.assertIn("Accuracy: 100.0%", result_text)
        self.assertEqual(self.app.type_entry.cget("state"), "disabled")
        self.assertEqual(self.app.start_button.cget("state"), "normal")

    def test_empty_input(self):
        """Test handling of empty input"""
        self.app.start_test()
        self.app.current_text = "test word"
        
        self.app.type_entry.delete(0, tk.END)
        self.app.check_progress(None)
        
        # Empty input should show 0 WPM and 0% accuracy
        result_text = self.app.results_label.cget("text")
        self.assertIn("WPM: 0.0", result_text)
        self.assertIn("Accuracy: 0.0%", result_text)

    def test_text_coloring(self):
        """Test text coloring for correct, incorrect, and remaining text"""
        self.app.start_test()
        self.app.current_text = "test word"
        
        # Test correct typing
        self.app.type_entry.insert(0, "test")
        self.app.check_progress(None)
        
        # Get all text with tags
        text_content = self.app.display_text.get("1.0", tk.END).strip()
        
        # Verify correct characters are green
        correct_ranges = self.app.display_text.tag_ranges("correct")
        correct_text = ""
        for i in range(0, len(correct_ranges), 2):
            correct_text += self.app.display_text.get(correct_ranges[i], correct_ranges[i+1])
        self.assertEqual(correct_text, "test")
        
        # Verify remaining text is black
        remaining_ranges = self.app.display_text.tag_ranges("remaining")
        remaining_text = ""
        for i in range(0, len(remaining_ranges), 2):
            remaining_text += self.app.display_text.get(remaining_ranges[i], remaining_ranges[i+1])
        self.assertEqual(remaining_text.strip(), "word")

    def test_real_time_wpm(self):
        """Test real-time WPM calculation"""
        self.app.start_test()
        self.app.current_text = "test word example"
        self.app.start_time = time.time() - 30  # Simulate 30 seconds passed
        
        # Type two words
        self.app.type_entry.delete(0, tk.END)  # Clear any existing text
        self.app.type_entry.insert(0, "test word")
        self.app.check_progress(None)
        
        # Check WPM (2 words in 30 seconds = 4 WPM)
        result_text = self.app.results_label.cget("text")
        wpm = float(result_text.split("WPM: ")[1].split(" |")[0])
        self.assertGreater(wpm, 0)  # Just verify WPM is being calculated
        self.assertLess(wpm, 180)  # And is within reasonable bounds

    def test_long_input(self):
        """Test handling of input longer than target text"""
        self.app.start_test()
        self.app.current_text = "test"
        
        # Type more characters than target
        self.app.type_entry.insert(0, "testing")
        self.app.check_progress(None)
        
        # Should automatically end test
        self.assertEqual(self.app.type_entry.cget("state"), "disabled")
        self.assertEqual(self.app.start_button.cget("state"), "normal")

    def test_special_characters(self):
        """Test handling of special characters in input"""
        self.app.start_test()
        self.app.current_text = "test"
        self.app.start_time = time.time()  # Reset start time
        
        # Type text with special characters
        self.app.type_entry.delete(0, tk.END)
        self.app.type_entry.insert(0, "te$t")
        self.app.check_progress(None)
        
        # Should handle special characters correctly (t and e are correct, $ and t are wrong)
        result_text = self.app.results_label.cget("text")
        accuracy = float(result_text.split("Accuracy: ")[1].split("%")[0])
        self.assertEqual(accuracy, 75.0)  # 't', 'e', and 't' are correct out of 4 characters

    def test_rapid_typing(self):
        """Test handling of rapid typing"""
        self.app.start_test()
        self.app.current_text = "test word example"
        self.app.start_time = time.time() - 1  # Simulate 1 second passed
        
        # Simulate very fast typing
        self.app.type_entry.insert(0, "test word example")
        self.app.check_progress(None)
        
        # Check high WPM is calculated correctly (3 words in 1 second = 180 WPM)
        result_text = self.app.results_label.cget("text")
        wpm = float(result_text.split("WPM: ")[1].split(" |")[0])
        self.assertGreater(wpm, 150)  # Should be around 180 WPM

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

if __name__ == '__main__':
    unittest.main()
