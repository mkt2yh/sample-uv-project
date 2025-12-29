"""Unit tests for the calc package.

These tests exercise parsing and evaluation helpers in src/calc/main.py.
"""

import pytest

from calc.main import evaluate_expression, main, parse_expression


def test_parse_expression_basic() -> None:
    """Test basic expression parsing."""
    result = parse_expression("4 + 4")
    assert result == "4+4"


def test_parse_expression_with_spaces() -> None:
    """Test expression with various spacing."""
    result = parse_expression("  4   +   4  ")
    assert result == "4+4"


def test_parse_expression_with_parentheses() -> None:
    """Test expression with parentheses."""
    result = parse_expression("(4 + 4) * 2")
    assert result == "(4+4)*2"


def test_parse_expression_invalid_chars() -> None:
    """Test expression with invalid characters."""
    with pytest.raises(ValueError, match="Invalid characters in expression"):
        parse_expression("4 + 4a")


def test_parse_expression_unbalanced_parentheses() -> None:
    """Test expression with unbalanced parentheses."""
    with pytest.raises(ValueError, match="Unbalanced parentheses"):
        parse_expression("(4 + 4")


def test_evaluate_expression_basic() -> None:
    """Test basic arithmetic evaluation."""
    result = evaluate_expression("4+4")
    assert result == 8.0


def test_evaluate_expression_complex() -> None:
    """Test complex arithmetic expression."""
    result = evaluate_expression("(4+4)*2")
    assert result == 16.0


def test_evaluate_expression_with_decimals() -> None:
    """Test expression with decimal numbers."""
    result = evaluate_expression("4.5+3.5")
    assert result == 8.0


def test_evaluate_expression_division() -> None:
    """Test division operation."""
    result = evaluate_expression("8/4")
    assert result == 2.0


def test_evaluate_expression_invalid() -> None:
    """Test invalid expression."""
    with pytest.raises(ValueError, match="Evaluation error"):
        evaluate_expression("4 + ")


def test_main_no_args() -> None:
    """Test main function with no arguments."""
    result = main([])
    assert result == 1


def test_main_valid_expression() -> None:
    """Test main function with valid expression."""
    # Mock sys.argv for testing
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["calc", "4", "+", "4"]
        result = main()
        assert result == 0
    finally:
        sys.argv = original_argv


def test_main_invalid_expression() -> None:
    """Test main function with invalid expression."""
    import sys

    original_argv = sys.argv
    try:
        sys.argv = ["calc", "4", "+", "a"]
        result = main()
        assert result == 1
    finally:
        sys.argv = original_argv
