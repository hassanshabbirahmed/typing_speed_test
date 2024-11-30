# Development Guide

## Project Structure

```
typing_speed_test/
├── src/               # Source code
│   ├── gui.py        # GUI components
│   ├── game_logic.py # Core game logic
│   ├── settings.py   # Configuration
│   └── utils.py      # Helper functions
├── tests/            # Test suite
├── assets/           # Static resources
└── docs/             # Documentation
```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development tools
   ```

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Code Style

This project follows PEP 8 guidelines. Use pylint for code style checking:
```bash
pylint src/ tests/
```
