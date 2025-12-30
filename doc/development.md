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

1. Activate the environment:

```bash
# Windows
.venv\Scripts\activate.bat

# POSIX
source .venv/bin/activate
```

1. Install dependencies:

```bash
uv add pytest fastapi uvicorn httpx
```

1. Add project to workspace (editable mode):

```bash
uv add --dev .
```

1. Run development server:

```bash
python -m uvicorn src.calc.main:app --reload
```

### Quick Windows dev shortcut

If you use the bundled virtualenv and Windows, run:

```bat
.venv\Scripts\activate.bat && python -m uvicorn src.calc.main:app --reload
```

### Setup with pip (alternative)

1. Create a virtual environment:

```bash
python -m venv .venv
```

1. Activate the environment:

```bash
# Windows
.venv\Scripts\activate.bat

# POSIX
source .venv/bin/activate
```

1. Install dependencies:

```bash
pip install pytest fastapi uvicorn httpx
```

1. Install project in editable mode:

```bash
python -m pip install -e .[dev]
```

1. Run development server:

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
uvx --from git+https://github.com/USERNAME/sample-uv-project@main serve
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

## CI: Build wheel on tag

This repository includes a GitHub Actions workflow that builds a wheel and creates a Release when a Git tag starting with `v` (e.g. `v1.2.0`) is pushed.

To create a release that includes the built wheel from CI:

1. Create a signed tag locally (optional but recommended):

```bash
git tag -s v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

1. Alternatively, create an unsigned tag and push:

```bash
git tag v1.0.0
git push origin v1.0.0
```

1. After pushing, GitHub Actions will run the `Build Wheel on Tag` workflow and attach the generated wheel to a Release.

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

`serve = "src.calc.main:app"`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for your changes
5. Submit a pull request

## License

MIT
