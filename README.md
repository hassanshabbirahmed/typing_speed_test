# Typing Speed Test

[![Tests](https://github.com/hassanshabbirahmed/typing_speed_test/actions/workflows/python-test.yml/badge.svg)](https://github.com/hassanshabbirahmed/typing_speed_test/actions)
[![codecov](https://codecov.io/gh/hassanshabbirahmed/typing_speed_test/branch/main/graph/badge.svg)](https://codecov.io/gh/hassanshabbirahmed/typing_speed_test)

A Python-based application to test and improve your typing speed.

## Features

- Multiple difficulty levels (Easy, Medium, Hard)
- Real-time WPM (Words Per Minute) calculation
- Accuracy tracking
- High scores system
- Configurable word lists

## Project Structure

```
typing_speed_test/
├── src/                    # Source code
│   ├── config/            # Configuration management
│   ├── game_logic.py      # Core game mechanics
│   ├── gui.py            # User interface
│   ├── high_scores.py    # Score tracking
│   ├── settings.py       # Application settings
│   └── utils.py          # Helper functions
├── tests/                 # Test suite
│   ├── conftest.py       # Test configuration
│   ├── test_high_scores.py
│   └── test_typing_speed.py
├── assets/               # Static resources
│   ├── difficulties.json
│   └── word_lists.json
├── docs/                 # Documentation
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment template
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust settings if needed:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python -m src.main
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
