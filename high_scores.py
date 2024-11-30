import json
import os
from datetime import datetime

class HighScores:
    def __init__(self):
        self.scores_file = "typing_scores.json"
        self.scores = self._create_default_scores()
        self._load_scores()

    def _load_scores(self):
        """Load scores from file if it exists"""
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r') as f:
                    loaded_scores = json.load(f)
                    # Only load valid scores
                    for diff in ['easy', 'medium', 'hard']:
                        if diff in loaded_scores and isinstance(loaded_scores[diff], list):
                            self.scores[diff] = loaded_scores[diff]
            except (json.JSONDecodeError, FileNotFoundError):
                pass  # Keep default scores

    def _create_default_scores(self):
        """Create a new scores dictionary with empty lists"""
        return {
            'easy': [],
            'medium': [],
            'hard': []
        }

    def add_score(self, difficulty, wpm, accuracy):
        """Add a new score for the given difficulty"""
        if difficulty not in self.scores:
            self.scores[difficulty] = []
            
        score = {
            'wpm': float(round(wpm, 1)),
            'accuracy': float(round(accuracy, 1)),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.scores[difficulty].append(score)
        self.scores[difficulty].sort(key=lambda x: (-x['wpm'], -x['accuracy']))
        self.scores[difficulty] = self.scores[difficulty][:10]
        
        self._save_scores()
        return score

    def get_high_scores(self, difficulty):
        """Get high scores for the given difficulty"""
        if difficulty not in self.scores:
            self.scores[difficulty] = []
        return self.scores[difficulty].copy()  # Return a copy to prevent modification

    def _save_scores(self):
        """Save scores to file"""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")

    def get_personal_best(self, difficulty):
        """Get the personal best score for the given difficulty"""
        scores = self.get_high_scores(difficulty)
        return scores[0] if scores else None

    def clear_scores(self):
        """Clear all scores (used for testing)"""
        self.scores = self._create_default_scores()
        if os.path.exists(self.scores_file):
            os.remove(self.scores_file)

    def reset(self):
        """Reset scores to default state (used for testing)"""
        self.scores = self._create_default_scores()
