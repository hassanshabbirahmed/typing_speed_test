"""High scores management."""
import json
from pathlib import Path
from typing import Dict, List

from .settings import MAX_HIGH_SCORES

class HighScores:
    """Manages high scores."""

    def __init__(self, scores_file: Path):
        """Initialize high scores manager."""
        self.scores_file = Path(scores_file)
        self.scores: Dict[str, List[Dict[str, float]]] = {
            'easy': [],
            'medium': [],
            'hard': []
        }
        self._load_scores()

    def _load_scores(self) -> None:
        """Load scores from file."""
        if self.scores_file.exists():
            try:
                with open(self.scores_file, 'r') as f:
                    loaded_scores = json.load(f)
                    # Validate loaded scores format
                    if isinstance(loaded_scores, dict) and all(
                        difficulty in loaded_scores for difficulty in ['easy', 'medium', 'hard']
                    ):
                        self.scores = loaded_scores
            except (json.JSONDecodeError, KeyError):
                # Reset scores if file is corrupted
                self._save_scores()

    def _save_scores(self) -> None:
        """Save scores to file."""
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, wpm: float, accuracy: float, difficulty: str) -> None:
        """Add a new score."""
        if difficulty not in self.scores:
            raise ValueError(f"Invalid difficulty: {difficulty}")

        score = {
            'wpm': wpm,
            'accuracy': accuracy,
            'timestamp': None  # Could add timestamp if needed
        }

        # Add score and sort by WPM
        self.scores[difficulty].append(score)
        self.scores[difficulty].sort(key=lambda x: x['wpm'], reverse=True)

        # Keep only top scores
        if len(self.scores[difficulty]) > MAX_HIGH_SCORES:
            self.scores[difficulty] = self.scores[difficulty][:MAX_HIGH_SCORES]

        self._save_scores()

    def get_scores(self, difficulty: str) -> List[Dict[str, float]]:
        """Get scores for a difficulty level."""
        if difficulty not in self.scores:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        return self.scores[difficulty]
