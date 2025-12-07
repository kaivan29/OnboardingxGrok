"""Utility functions for the calculator."""
from typing import List


def format_number(num: float, decimals: int = 2) -> str:
    """Format a number with specified decimal places."""
    return f"{num:.{decimals}f}"


def validate_positive(value: float) -> bool:
    """Validate that a value is positive."""
    return value > 0


def sum_list(numbers: List[float]) -> float:
    """Sum a list of numbers."""
    return sum(numbers)


def average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

