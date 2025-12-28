"""Calculator CLI core.

Provides parse_expression, evaluate_expression and CLI entrypoint.
"""

import sys
import ast
import argparse
from typing import List, Optional
from fastapi import FastAPI


# ASGI app for uvx
app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}


def parse_expression(expr: str) -> str:
    """Parse and sanitize arithmetic expression.

    Removes whitespace and validates allowed characters and parentheses balance.
    """
    cleaned = ''.join(expr.split())

    # Validate allowed characters: digits, operators, parentheses and decimal point
    allowed_chars = set('0123456789+-*/().')
    if not all(c in allowed_chars for c in cleaned):
        raise ValueError("Invalid characters in expression")

    # Validate balanced parentheses
    if cleaned.count('(') != cleaned.count(')'):
        raise ValueError("Unbalanced parentheses")

    return cleaned


def _eval_ast_node(n: ast.AST) -> float:
    """Recursively evaluate an AST node containing a safe arithmetic expression.

    Supported nodes: Expression, BinOp (+, -, *, /, **, %, //), UnaryOp (+, -), Constant/Num.
    """
    # Expression wrapper
    if isinstance(n, ast.Expression):
        return _eval_ast_node(n.body)

    # Binary operations
    if isinstance(n, ast.BinOp):
        left = _eval_ast_node(n.left)
        right = _eval_ast_node(n.right)
        if isinstance(n.op, ast.Add):
            return left + right
        if isinstance(n.op, ast.Sub):
            return left - right
        if isinstance(n.op, ast.Mult):
            return left * right
        if isinstance(n.op, ast.Div):
            return left / right
        if isinstance(n.op, ast.Pow):
            return left ** right
        if isinstance(n.op, ast.Mod):
            return left % right
        if isinstance(n.op, ast.FloorDiv):
            return left // right
        raise ValueError("Unsupported binary operator")

    # Unary operations
    if isinstance(n, ast.UnaryOp):
        val = _eval_ast_node(n.operand)
        if isinstance(n.op, ast.UAdd):
            return +val
        if isinstance(n.op, ast.USub):
            return -val
        raise ValueError("Unsupported unary operator")

    # Numeric literal
    if isinstance(n, ast.Constant):
        if isinstance(n.value, (int, float)):
            return float(n.value)
        raise ValueError("Non-numeric constant")

    # Backwards-compat
    if isinstance(n, ast.Num):
        return float(n.n)

    raise ValueError("Unsupported expression element")


def evaluate_expression(expr: str) -> float:
    """Safely evaluate arithmetic expression using a custom AST evaluator.

    This avoids use of eval() and mitigates code execution risks reported by
    security scanners.
    """
    try:
        node = ast.parse(expr, mode='eval')

        # Quick structural safety check
        def _is_safe(n: ast.AST) -> bool:
            if isinstance(n, ast.Expression):
                return _is_safe(n.body)
            if isinstance(n, ast.BinOp):
                return _is_safe(n.left) and _is_safe(n.right)
            if isinstance(n, ast.UnaryOp):
                return _is_safe(n.operand)
            if isinstance(n, ast.Constant):
                return isinstance(n.value, (int, float))
            if isinstance(n, ast.Num):
                return isinstance(n.n, (int, float))
            return False

        if not _is_safe(node):
            raise ValueError("Invalid expression structure")

        result = _eval_ast_node(node)
        if not isinstance(result, (int, float)):
            raise ValueError("Expression did not evaluate to a number")
        return float(result)

    except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as e:
        raise ValueError(f"Evaluation error: {e}")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(add_help=True, description="Simple CLI calculator")
    p.add_argument('-v', '--verbose', action='store_true', help='Show parsed expression')
    p.add_argument('expression', nargs=argparse.REMAINDER, help='Expression to evaluate (e.g. 4 + 4)')
    return p


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
        print('Usage: calc <expression>', file=sys.stderr)
        return 1

    # expression may be in parsed.expression (REMAINDER) or extras; combine both
    expr_parts: List[str] = []
    if hasattr(parsed, 'expression') and parsed.expression:
        expr_parts.extend(parsed.expression)
    if extras:
        expr_parts.extend(extras)

    if not expr_parts:
        # No expression provided
        print('Usage: calc <expression)', file=sys.stderr)
        return 1

    expression = ' '.join(expr_parts)

    try:
        parsed_expr = parse_expression(expression)
        if parsed.verbose if isinstance(parsed, argparse.Namespace) else False:
            print(f"Parsed: {parsed_expr}")

        result = evaluate_expression(parsed_expr)
        print(f"Result: {result}")

        return 0

    except ValueError as e:
        # Provide clearer error messages for common cases
        msg = str(e)
        if 'Invalid characters' in msg:
            print('Error: Expression contains invalid characters. Use only digits, operators and parentheses.', file=sys.stderr)
        elif 'Unbalanced parentheses' in msg:
            print('Error: Unbalanced parentheses in expression.', file=sys.stderr)
        elif 'Evaluation error' in msg:
            print(f'Error: {msg}', file=sys.stderr)
        else:
            print(f'Error: {msg}', file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
