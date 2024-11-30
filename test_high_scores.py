import unittest
import os
import json
from high_scores import HighScores

class TestHighScores(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_scores.json"
        # Remove the test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.high_scores = HighScores()
        self.high_scores.scores_file = self.test_file
        self.high_scores.reset()  # Start with clean state

    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_score(self):
        """Test adding and sorting scores"""
        # Add multiple scores
        self.high_scores.add_score("medium", 50.5, 95.0)
        self.high_scores.add_score("medium", 60.0, 98.0)
        self.high_scores.add_score("medium", 45.0, 92.0)

        # Check scores are sorted by WPM
        scores = self.high_scores.get_high_scores("medium")
        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0]["wpm"], 60.0)
        self.assertEqual(scores[1]["wpm"], 50.5)
        self.assertEqual(scores[2]["wpm"], 45.0)

    def test_personal_best(self):
        """Test getting personal best score"""
        self.high_scores.add_score("easy", 40.0, 90.0)
        self.high_scores.add_score("easy", 45.0, 85.0)
        
        best = self.high_scores.get_personal_best("easy")
        self.assertIsNotNone(best)
        self.assertEqual(best["wpm"], 45.0)
        self.assertEqual(best["accuracy"], 85.0)

    def test_different_difficulties(self):
        """Test scores for different difficulties are separate"""
        self.high_scores.add_score("easy", 40.0, 90.0)
        self.high_scores.add_score("medium", 50.0, 85.0)
        self.high_scores.add_score("hard", 30.0, 80.0)

        easy_scores = self.high_scores.get_high_scores("easy")
        medium_scores = self.high_scores.get_high_scores("medium")
        hard_scores = self.high_scores.get_high_scores("hard")

        self.assertEqual(len(easy_scores), 1)
        self.assertEqual(len(medium_scores), 1)
        self.assertEqual(len(hard_scores), 1)

    def test_top_10_limit(self):
        """Test only top 10 scores are kept"""
        # Add 15 scores
        for i in range(15):
            self.high_scores.add_score("medium", float(i), 90.0)

        scores = self.high_scores.get_high_scores("medium")
        self.assertEqual(len(scores), 10)
        self.assertEqual(scores[0]["wpm"], 14.0)  # Highest score should be kept

    def test_file_persistence(self):
        """Test scores are saved to and loaded from file"""
        # Add a score and verify it's saved
        self.high_scores.add_score("medium", 50.0, 95.0)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Create new instance and verify score is loaded
        new_scores = HighScores()
        new_scores.scores_file = self.test_file
        new_scores.reset()  # Start with clean state
        new_scores._load_scores()  # Load scores from file
        scores = new_scores.get_high_scores("medium")
        
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0]["wpm"], 50.0)
        self.assertEqual(scores[0]["accuracy"], 95.0)

if __name__ == '__main__':
    unittest.main()
