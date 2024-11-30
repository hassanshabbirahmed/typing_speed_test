# Contributing Guidelines

Thank you for considering contributing to the Typing Speed Test project! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information

### Suggesting Enhancements

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear title and description
   - Detailed explanation of the feature
   - Use cases and benefits
   - Potential implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes following our coding standards
4. Write or update tests
5. Run the test suite:
   ```bash
   pytest
   ```
6. Commit your changes:
   ```bash
   git commit -m "feat: add your feature description"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/typing_speed_test.git
   cd typing_speed_test
   ```

2. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for classes and functions

### Example

```python
from typing import List, Optional

def calculate_average(numbers: List[float]) -> Optional[float]:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: List of numbers to average

    Returns:
        Average value or None if list is empty
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
```

### Testing

- Write tests for new features
- Maintain or improve code coverage
- Use pytest fixtures appropriately
- Mock external dependencies

### Documentation

- Update API documentation for new features
- Include docstrings for public methods
- Update README.md if necessary
- Add comments for complex logic

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test updates
- chore: Maintenance tasks

Example:
```
feat(high-scores): add difficulty-based filtering

Add ability to filter high scores by difficulty level.
This change includes:
- New filtering method in HighScores class
- Updated GUI to show filtered scores
- Tests for new functionality
```

## Review Process

1. All code changes require review
2. Address review comments promptly
3. Keep pull requests focused and small
4. Ensure CI checks pass
5. Update documentation as needed

## Questions?

Feel free to create an issue for any questions about contributing. We're here to help!
