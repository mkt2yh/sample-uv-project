# Calculator CLI

A simple command-line calculator implemented in Python. Supports basic arithmetic operations with input validation and safe evaluation.

## Features

- Addition, subtraction, multiplication, division
- Parentheses and decimal support
- Input validation (invalid characters, unbalanced parentheses)
- Safe evaluation using Python AST
- Command-line interface
- Unit tests included

## Usage



## Dependency Version Management

This project uses uv for dependency management. The dependency versions are specified in `pyproject.toml`:

- `pytest>=8.0.0` - Testing framework
- `fastapi>=0.95.0` - Web framework
- `uvicorn>=0.22.0` - ASGI server
- `httpx>=0.28.1` - HTTP client for testing

To update dependencies:

```bash
# Update a specific dependency
uv add <package>@<version>

# Update all dependencies to latest versions
uv update

# Check for outdated dependencies
uv outdated
```

To add a new dependency:

```bash
uv add <package>
```

To remove a dependency:

```bash
uv remove <package>
```

```sh
# Preferred: run via installed CLI entrypoint or module path
calc "4 + 4"
# Or when running as a module (package import path 'calc')
python -m calc.main "4 + 4"
```

Or, pass arguments separately:

```sh
python -m calc.main 4 + 4  # quoting recommended
```

For detailed development and execution guidelines, see [Development Guide](doc/development.md).

Note: uvx is a wrapper around external uv tools and depends on the environment; it may require the project to be installed in the venv or be discoverable on PYTHONPATH. If you see ModuleNotFoundError for your package, perform an editable install (`pip install -e .`) inside the venv.

Important notes

- Ensure dependencies for testing FastAPI (httpx) and running (uvicorn, fastapi) are installed in the venv.
- `pyproject.toml` exposes a `serve` script (serve = "src.calc.main:app").


For detailed development guidelines, see [Development Guide](doc/development.md).

## Run from GitHub repository with uvx

You can run this project directly from a GitHub repository using uvx without installing pipx. Below are explicit steps for developers and CI.

### Run directly from GitHub (uvx)

```bash
# Run from a public GitHub repository (recommended)
uvx --from git+https://github.com/USERNAME/sample-uv-project@main serve

# Run from a specific tag or branch
uvx --from git+https://github.com/USERNAME/sample-uv-project@v1.0.0 serve

# Run from a private repository (requires SSH access)
uvx --from git+ssh://git@github.com/USERNAME/private-repo@main serve
```

Prerequisites:
- uvx must be installed on the user's machine
- The repository must contain a valid `pyproject.toml` with the `serve` script entry (it does)
- All runtime dependencies (fastapi, uvicorn) must be listed in `pyproject.toml` (they are)

Notes for developers (local development)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows (cmd.exe)
.venv\Scripts\activate.bat
# PowerShell
.venv\Scripts\Activate.ps1
# POSIX
source .venv/bin/activate
```

2. Install the project in editable mode and dev tools:

```bash
python -m pip install --upgrade pip
python -m pip install -e .[lint,security,tools]
python -m pip install pre-commit
pre-commit install
```

3. Start the server locally:

```bash
# Start uvicorn serving the FastAPI app
python -m uvicorn calc.main:app --reload
```

4. Run tests:

```bash
pytest -q
```

### Example Output

```
Parsed: 4+4
Result: 8.0
```

## Error Example

```
python -m src.calc.main "4 + a"
Error: Invalid characters in expression
```

## File Structure

- [`src/calc/main.py`](src/calc/main.py): Core logic and CLI
- [`tests/test_calc.py`](tests/test_calc.py): Unit tests

## Requirements

- Python 3.12 or higher

## License

MIT
