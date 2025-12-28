# Development Guide

This document provides detailed development guidelines for the Calculator CLI project.

## Project Structure

```
src/
  calc/
    __init__.py
    main.py        # Core logic and CLI

tests/
  test_calc.py    # Unit tests

pyproject.toml   # Project configuration
README.md        # User documentation
```

## Development Setup

### Prerequisites

- Python 3.12 or higher
- uv (recommended) or pip
- Git

### Setup with uv (recommended)

1. Create a virtual environment:

```bash
uv venv .venv
```

2. Activate the environment:

```bash
# Windows
.venv\Scripts\activate.bat

# POSIX
source .venv/bin/activate
```

3. Install dependencies:

```bash
uv add pytest fastapi uvicorn httpx
```

4. Add project to workspace (editable mode):

```bash
uv add --dev .
```

5. Run development server:

```bash
python -m uvicorn src.calc.main:app --reload
```

### Setup with pip (alternative)

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

```bash
# Windows
.venv\Scripts\activate.bat

# POSIX
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install pytest fastapi uvicorn httpx
```

4. Install project in editable mode:

```bash
pip install -e .
```

5. Run development server:

```bash
python -m uvicorn src.calc.main:app --reload
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Building and Running

### Run as CLI

```bash
python -m src.calc.main "4 + 4"
```

Or, pass arguments separately:

```bash
python -m src.calc.main 4 + 4
```

### Run as ASGI app (development)

Use uvicorn (recommended for local development):

```bash
python -m uvicorn src.calc.main:app --reload --host 127.0.0.1 --port 8000
```

### Run with uvx

```bash
uvx --from .venv run src.calc.main:app --reload --host 127.0.0.1 --port 8000
```

Note: uvx is a wrapper around external uv tools and depends on the environment; it may require the project to be installed in the venv or be discoverable on PYTHONPATH. If you see ModuleNotFoundError for your package, perform an editable install (`pip install -e .`) inside the venv.

### Run via pipx

```bash
python -m pipx run --spec sample-uv-project serve
```

Note: This requires the package to be published to an index or be accessible by pipx --spec. Local-only projects are not directly runnable with pipx unless published or served from a local file index.

## Dependency Management

This project uses uv for dependency management. The dependency versions are specified in `pyproject.toml`.

### Adding Dependencies

```bash
uv add <package>
```

### Removing Dependencies

```bash
uv remove <package>
```

### Updating Dependencies

```bash
# Update a specific dependency
uv add <package>@<version>

# Update all dependencies to latest versions
uv update

# Check for outdated dependencies
uv outdated
```

## Recommended Workflow

1. Create and activate venv: `python -m venv .venv` -> `.venv\Scripts\activate.bat`
2. Install dev deps: `pip install -e .[dev]` or `pip install -e .` and then `pip install uvicorn fastapi httpx`.
3. Start server with uvicorn as shown above.

## Error Handling

The calculator includes basic error handling for:

- Invalid characters in expressions
- Unbalanced parentheses
- Division by zero
- Syntax errors in expressions

## Security Considerations

- The calculator uses Python's AST module for safe evaluation of expressions
- Input validation is performed before evaluation
- No arbitrary code execution is allowed

## Performance

- The calculator is optimized for simple arithmetic operations
- For complex calculations, consider using a dedicated math library

## Deployment

For production deployment, consider:

- Using a production-grade ASGI server like uvicorn with gunicorn
- Setting up proper logging and monitoring
- Implementing rate limiting and security headers
- Using environment variables for configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for your changes
5. Submit a pull request

## License

MIT