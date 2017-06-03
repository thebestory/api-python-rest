"""
The Bestory Project
"""


class TheBestoryError(Exception):
    pass


class ValidationError(TheBestoryError, ValueError):
    pass


class DatabaseError(TheBestoryError):
    pass


class NotFetchedError(DatabaseError):
    pass


class NotFoundError(DatabaseError):
    pass


class NotCreatedError(DatabaseError):
    pass


class NotUpdatedError(DatabaseError):
    pass
