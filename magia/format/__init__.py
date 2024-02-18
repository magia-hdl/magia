"""
Numerical format conversions

This module provides classes for converting between different number formats,
such as fixed point and floating point numbers.

Put functions and classes here if:
- They convert Python floats to a different numerical format, or vice versa
- No operations and calculations logic is involved (e.g. addition, multiplication, etc.)
"""

from .fixed_point import FixedPoint

__all__ = [
    "FixedPoint"
]
