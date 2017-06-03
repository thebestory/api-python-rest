"""
The Bestory Project
"""

from tbs.lib import exceptions


def validate_id(id: int):
    assert isinstance(id, int)


def validate_type(type: str):
    assert isinstance(type, str)

    if not 0 < len(type) <= 32:
        raise exceptions.ValidationError("Type length must be between 1 and "
                                         "32")
