"""
The Bestory Project
"""


class TheBestoryError(Exception):
    pass


class ValidationError(TheBestoryError, ValueError):
    pass
