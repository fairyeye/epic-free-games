# AGENTS.md - Guidelines for AI Coding Agents

This document provides guidelines for AI agents working on this Epic Games Free Games notification project.

## Project Overview

A Python-based GitHub Actions application that automatically fetches Epic Games' weekly free games and sends notifications via Feishu (飞书). The project consists of:

- `epic_games.py` - Fetches free game data from Epic Games API
- `send_feishu.py` - Formats and outputs notification messages
- `.github/workflows/epic-weekly.yml` - GitHub Actions workflow for scheduling and execution

## Build, Lint, and Test Commands

### Running Scripts Locally

```bash
# Fetch and display free games JSON
python3 epic_games.py

# Format and display Feishu message
python3 epic_games.py | python3 send_feishu.py

# Test with specific output file
python3 epic_games.py > games.json
python3 send_feishu.py < games.json
```

### Python Quality Tools

```bash
# Syntax check
python3 -m py_compile epic_games.py send_feishu.py

# Check code style with black
pip install black
black --check epic_games.py send_feishu.py

# Sort imports
pip install isort
isort --check-only epic_games.py send_feishu.py

# Run all checks
black --check epic_games.py send_feishu.py && isort --check-only epic_games.py send_feishu.py
```

### Type Checking

```bash
# Install mypy
pip install mypy

# Type check Python files
mypy epic_games.py send_feishu.py
```

### Testing

```bash
# Run pytest if tests exist
python3 -m pytest

# Run a specific test file
python3 -m pytest tests/

# Run a specific test
python3 -m pytest tests/test_epic_games.py::test_is_currently_free
```

## Code Style Guidelines

### General Principles

- Write clear, self-documenting code
- Use Chinese comments and output messages (as this is a Chinese-focused project)
- Keep functions focused and single-purpose
- Handle errors gracefully with informative messages

### Python Style

- **Python Version**: Python 3.x (shebang: `#!/usr/bin/env python3`)
- **Line Length**: 120 characters max
- **Indentation**: 4 spaces (no tabs)
- **Encoding**: UTF-8 with `from __future__` imports not required for Python 3

### Imports

```python
# Standard library imports first, alphabetically
import json
import sys
from datetime import datetime
from urllib.error import URLError
from urllib.request import urlopen

# No third-party imports currently used
```

- Group imports: standard library, third-party, local modules
- Sort imports alphabetically within each group
- Use isort to enforce import ordering

### Naming Conventions

```python
# Functions: snake_case, descriptive with verbs
def fetch_free_games():
def is_currently_free(game):
def format_free_promotion(game):

# Variables: snake_case
current_free = []
games_data = {}

# Constants: UPPER_SNAKE_CASE (if any)
# API_URL = "https://..."

# Classes: PascalCase (if added later)
# class GameNotification:
```

- Use descriptive names that indicate purpose
- Avoid single-letter variables except in loops (`game` in `for game in games`)
- Prefix private functions with underscore if needed (`_helper_function()`)

### Functions

```python
def fetch_free_games():
    """Get Epic Games free game information"""
    # Single responsibility: one function does one thing
    # Keep functions under 50 lines when possible
    pass
```

- Include docstrings for all public functions
- Keep functions short and focused
- Use type hints where beneficial (Python 3.5+)

### Type Hints (Recommended)

```python
from typing import Optional, Dict, List, Any

def fetch_free_games() -> Optional[Any]:
    """Fetch free games data from Epic Games API"""
    # ...

def format_free_promotion(game: Dict[str, Any]) -> Dict[str, str]:
    """Format current free game information"""
    # ...
```

### Error Handling

```python
def fetch_free_games():
    """Get Epic Games free game information"""
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except URLError as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None
```

- Use try/except for I/O operations (network, file)
- Write errors to stderr: `print(..., file=sys.stderr)`
- Return `None` or use `sys.exit(1)` for fatal errors in main flow
- Avoid bare `except:` clauses - catch specific exceptions

### JSON Handling

```python
# Use ensure_ascii=False for Chinese content
print(json.dumps(result, ensure_ascii=False, indent=2))

# Handle JSON errors gracefully
try:
    games_data = json.loads(input_data)
except json.JSONDecodeError:
    print("Error: Invalid JSON input", file=sys.stderr)
    sys.exit(1)
```

### Data Processing

```python
# Use .get() for safe dictionary access
title = game.get("title", "Unknown")

# Handle nested dicts with multiple .get() calls
data = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
```

### File Structure

```
epic-free-games/
├── epic_games.py       # Main data fetching script
├── send_feishu.py      # Message formatting script
├── .github/workflows/
│   └── epic-weekly.yml # GitHub Actions workflow
├── README.md           # Project documentation
├── QUICKSTART.md       # Quick start guide
├── LICENSE
└── .gitignore
```

### GitHub Actions Workflow

- Use latest stable action versions (`actions/checkout@v4`, `actions/setup-python@v5`)
- Use `continue-on-error: true` for non-critical steps
- Check for configuration secrets before using them
- Output status messages clearly

## Workflow for Changes

1. Make changes to Python scripts
2. Run syntax check: `python3 -m py_compile epic_games.py send_feishu.py`
3. Test locally: `python3 epic_games.py | python3 send_feishu.py`
4. Verify no lint errors: `black --check` and `isort --check-only`
5. Commit changes with clear message

## Notes

- No build step required (pure Python scripts)
- No dependencies beyond Python standard library
- Scripts are executable (`chmod +x *.py`)
- Workflow uses `python3` command (not specific version)
