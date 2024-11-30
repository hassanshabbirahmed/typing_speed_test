"""
High scores management for the Typing Speed Test application.
"""
import json
from datetime import datetime
from typing import Dict, List, Any
from .settings import SCORES_FILE, MAX_HIGH_SCORES

class HighScores:
    """Manages high scores for the typing speed test."""
    
    def __init__(self):
        self.scores_file = SCORES_FILE
        self.max_scores = MAX_HIGH_SCORES
        self.scores = self._create_default_scores()
        self._load_scores()

    def _load_scores(self) -> None:
        """Load scores from file if it exists."""
        try:
            with open(self.scores_file, 'r') as f:
                loaded_scores = json.load(f)
                # Only load valid scores
                for diff in ['easy', 'medium', 'hard']:
                    if diff in loaded_scores and isinstance(loaded_scores[diff], list):
                        self.scores[diff] = loaded_scores[diff]
        except (json.JSONDecodeError, FileNotFoundError):
            pass  # Keep default scores

    def _create_default_scores(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create a new scores dictionary with empty lists."""
        return {
            'easy': [],
            'medium': [],
            'hard': []
        }

    def add_score(self, wpm: float, accuracy: float, difficulty: str) -> None:
        """Add a new score to the high scores list."""
        if difficulty not in self.scores:
            return

        score = {
            'wpm': round(wpm, 2),
            'accuracy': round(accuracy, 2),
            'date': datetime.now().isoformat()
        }

        # Add score and sort by WPM
        self.scores[difficulty].append(score)
        self.scores[difficulty].sort(key=lambda x: x['wpm'], reverse=True)

        # Keep only top scores
        self.scores[difficulty] = self.scores[difficulty][:self.max_scores]

        self._save_scores()

    def get_scores(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get all scores for a specific difficulty."""
        return self.scores.get(difficulty, [])

    def _save_scores(self) -> None:
        """Save scores to file."""
        try:
            self.scores_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.scores_file, 'w') as f:
                json.dump(self.scores, f, indent=4)
        except (OSError, IOError) as e:
            print(f"Error saving scores: {e}")  # In production, use proper logging
