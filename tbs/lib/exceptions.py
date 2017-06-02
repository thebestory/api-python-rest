"""
The Bestory Project
"""


class TheBestoryError(Exception):
    pass


class ValidationError(TheBestoryError, ValueError):
    pass


class NotFoundError(TheBestoryError):
    pass


class NotCreatedError(TheBestoryError):
    pass
