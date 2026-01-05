"""Calculator CLI core.

Provides parse_expression, evaluate_expression and CLI entrypoint.
"""

import argparse
import ast
import sys
from typing import List, Optional

from fastapi import FastAPI

# ASGI app factory for uvx: expose callable `app()` that returns ASGI app instance
_def_app = FastAPI()


def app() -> FastAPI:
    """Return ASGI application instance for uvx serve compatibility."""
    return _def_app


@_def_app.get("/")  # type: ignore[misc]
def root() -> dict[str, bool]:
    """Health-check endpoint.

    Returns a basic JSON object indicating the service is up.
    """
    return {"ok": True}


def parse_expression(expr: str) -> str:
    """Parse and sanitize arithmetic expression.

    Removes whitespace and validates allowed characters and parentheses balance.

    Args:
        expr: Raw expression string provided by the user.

    Returns:
        A sanitized expression string with whitespace removed.
    """
    cleaned = "".join(expr.split())

    # Validate allowed characters: digits, operators, parentheses and decimal point
    allowed_chars = set("0123456789+-*/().")
    if not all(c in allowed_chars for c in cleaned):
        raise ValueError("Invalid characters in expression")

    # Validate balanced parentheses
    if cleaned.count("(") != cleaned.count(")"):
        raise ValueError("Unbalanced parentheses")

    return cleaned


def _eval_ast_node(n: ast.AST) -> float:
    """Recursively evaluate an AST node containing a safe arithmetic expression.

    This function delegates binary and unary ops to small helpers to keep
    complexity low for linters.
    """
    if isinstance(n, ast.Expression):
        return _eval_ast_node(n.body)

    if isinstance(n, ast.BinOp):
        return _eval_binop(n)

    if isinstance(n, ast.UnaryOp):
        return _eval_unaryop(n)

    if isinstance(n, ast.Constant):
        if isinstance(n.value, (int, float)):
            return float(n.value)
        raise ValueError("Non-numeric constant")

    if isinstance(n, ast.Num):
        if isinstance(n.n, (int, float)):
            return float(n.n)
        raise ValueError("Non-numeric Num constant")

    raise ValueError("Unsupported expression element")


def _eval_binop(n: ast.BinOp) -> float:
    """Evaluate a binary operation AST node."""
    left: float = _eval_ast_node(n.left)
    right: float = _eval_ast_node(n.right)

    if isinstance(n.op, ast.Add):
        return left + right
    if isinstance(n.op, ast.Sub):
        return left - right
    if isinstance(n.op, ast.Mult):
        return float(left * right)
    if isinstance(n.op, ast.Div):
        return float(left / right)
    if isinstance(n.op, ast.Pow):
        return float(left ** right)
    if isinstance(n.op, ast.Mod):
        return left % right
    if isinstance(n.op, ast.FloorDiv):
        return left // right

    raise ValueError("Unsupported binary operator")


def _eval_unaryop(n: ast.UnaryOp) -> float:
    """Evaluate a unary operation AST node."""
    val: float = _eval_ast_node(n.operand)
    if isinstance(n.op, ast.UAdd):
        return +val
    if isinstance(n.op, ast.USub):
        return -val
    raise ValueError("Unsupported unary operator")


# --- Safety checking helpers moved to module scope to reduce nested complexity ---
def _is_safe(node: ast.AST) -> bool:
    """Return True if AST node only contains safe arithmetic constructs.

    Split into small checks so evaluate_expression remains simple and the
    cyclomatic complexity is distributed across helpers.
    """
    if isinstance(node, ast.Expression):
        return _is_safe(node.body)
    if isinstance(node, ast.BinOp):
        return _is_safe(node.left) and _is_safe(node.right)
    if isinstance(node, ast.UnaryOp):
        return _is_safe(node.operand)
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float))
    if isinstance(node, ast.Num):
        return isinstance(node.n, (int, float))
    return False


def evaluate_expression(expr: str) -> float:
    """Safely evaluate arithmetic expression using a custom AST evaluator.

    This avoids use of eval() and mitigates code execution risks reported by
    security scanners.
    """
    try:
        node = ast.parse(expr, mode="eval")

        # Quick structural safety check delegated to module-level helper
        if not _is_safe(node):
            raise ValueError("Invalid expression structure")

        result = _eval_ast_node(node)
        if not isinstance(result, (int, float)):
            raise ValueError("Expression did not evaluate to a number")
        # ensure float return for mypy
        res: float = float(result)
        return res

    except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as e:
        raise ValueError(f"Evaluation error: {e}") from e


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        add_help=True, description="Simple CLI calculator"
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show parsed expression",
    )
    p.add_argument("expression", nargs=argparse.REMAINDER, help="Expression to evaluate")
    return p


def _collect_expr_parts(parsed: argparse.Namespace, extras: List[str]) -> List[str]:
    """Collect expression parts from argparse Namespace and extras.

    Separated into a helper to keep main() below the complexity threshold.
    """
    parts: List[str] = []
    if hasattr(parsed, "expression") and parsed.expression:
        parts.extend(parsed.expression)
    if extras:
        parts.extend(extras)
    return parts


def _execute_and_print(parsed: argparse.Namespace, expression: str) -> int:
    """Parse, evaluate and print results; return exit code."""
    parsed_expr = parse_expression(expression)
    if parsed.verbose if isinstance(parsed, argparse.Namespace) else False:
        print(f"Parsed: {parsed_expr}")

    result = evaluate_expression(parsed_expr)
    print(f"Result: {result}")
    return 0


def _handle_value_error(e: ValueError) -> int:
    """Print user-facing message for ValueError and return exit code 1."""
    msg = str(e)
    if "Invalid characters" in msg:
        print(
            "Error: Expression contains invalid characters.", file=sys.stderr
        )
    elif "Unbalanced parentheses" in msg:
        print("Error: Unbalanced parentheses in expression.", file=sys.stderr)
    elif "Evaluation error" in msg:
        print(f"Error: {msg}", file=sys.stderr)
    else:
        print(f"Error: {msg}", file=sys.stderr)
    return 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for calculator CLI.

    Returns 0 on success, 1 on user error (invalid input), 2 on unexpected error.
    Accepts an optional argv list for testing; when argv is None, sys.argv[1:] is used.
    """
    args_list = sys.argv[1:] if argv is None else argv

    parser = _build_parser()
    try:
        # Use parse_known_args to avoid argparse exiting the process
        parsed, extras = parser.parse_known_args(args_list)
    except SystemExit:
        # argparse would print usage; mirror previous behavior
        print("Usage: calc <expression>", file=sys.stderr)
        return 1

    expr_parts = _collect_expr_parts(parsed, extras)

    if not expr_parts:
        # No expression provided
        print("Usage: calc <expression>", file=sys.stderr)
        return 1

    expression = " ".join(expr_parts)

    try:
        return _execute_and_print(parsed, expression)

    except ValueError as e:
        return _handle_value_error(e)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
