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
- uv
- Git

### Setup with uv

1. Sync dependencies and create the venv from `pyproject.toml`:

```bash
uv sync
```

2. Run development server:

```bash
uv run -m uvicorn calc.main:app --reload
```

### Quick Windows dev shortcut

If you use the bundled virtualenv and Windows, run:

```bat
.venv\Scripts\activate.bat && python -m uvicorn src.calc.main:app --reload
```

### Notes

This project uses uv for all dependency management and execution.

## Running Tests

```bash
uv run -m pytest tests/ -v
```

## Building and Running

### Run as CLI

```bash
uv run calc "4 + 4"
```

Or, pass arguments separately:

```bash
uv run -m calc.main 4 + 4
```

### Run as ASGI app (development)

Use uvicorn (recommended for local development):

```bash
uv run -m uvicorn calc.main:app --reload --host 127.0.0.1 --port 8000
```

### Run with uvx

```bash
uvx --from git+https://github.com/USERNAME/sample-uv-project@main serve
```

Note: `uvx` runs tools in ephemeral environments. Prefer `uv run` when executing project code.

### Run via uvx (from repo)

```bash
uvx --from git+https://github.com/USERNAME/sample-uv-project@main serve
```

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

1. Sync dependencies: `uv sync`
2. Run checks: `uvx pre-commit run --all-files`, `uvx ruff check .`
3. Run tests: `uv run -m pytest`
4. Start server: `uv run -m uvicorn calc.main:app --reload`

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

`serve = "calc.main:app"`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for your changes
5. Submit a pull request

## License

MIT
