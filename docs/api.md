# API Documentation

## Core Modules

### GameManager (game_logic.py)

#### Classes

##### `GameManager`
Manages the core game mechanics and state.

###### Methods
- `start_game()`: Initializes a new typing test
- `check_input(text: str) -> bool`: Validates user input
- `calculate_metrics() -> Dict[str, float]`: Calculates WPM and accuracy
- `end_game() -> Dict[str, Any]`: Finalizes the game and returns results

### TypingSpeedGUI (gui.py)

#### Classes

##### `TypingSpeedGUI`
Handles the graphical user interface and user interactions.

###### Methods
- `initialize_ui()`: Sets up the GUI components
- `start_test()`: Begins a new typing test
- `update_display()`: Updates the GUI with current game state
- `show_results()`: Displays test results

### HighScores (high_scores.py)

#### Classes

##### `HighScores`
Manages high score tracking and persistence.

###### Methods
- `add_score(score: Dict[str, Any]) -> bool`: Adds a new score
- `get_scores(difficulty: str) -> List[Dict[str, Any]]`: Retrieves scores
- `save_scores() -> None`: Persists scores to storage

## Configuration

### ConfigManager (config/config_manager.py)

#### Classes

##### `ConfigManager`
Singleton class for managing application configuration.

###### Methods
- `get_instance() -> ConfigManager`: Returns singleton instance
- `get_config(key: str) -> Any`: Retrieves configuration value
- `load_config() -> None`: Loads configuration from environment

## Utility Functions (utils.py)

### Functions
- `load_word_list() -> List[str]`: Loads words for typing tests
- `calculate_wpm(text: str, time: float) -> float`: Calculates WPM
- `calculate_accuracy(original: str, typed: str) -> float`: Calculates accuracy
