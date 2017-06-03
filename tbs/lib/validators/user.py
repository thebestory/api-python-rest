"""
The Bestory Project
"""

import re

from tbs.lib import exceptions


def validate_username(username: str):
    assert isinstance(username, str)

    if 0 < len(username) <= 32:
        raise exceptions.ValidationError("Username length must be between 1 "
                                         "and 32")


def validate_email(email: str):
    assert isinstance(email, str)

    if re.match(r".+@.+", email) is None:
        raise exceptions.ValidationError("It's a not valid email string")

    if 0 < len(email) <= 255:
        raise exceptions.ValidationError("Email length must be between 1 "
                                         "and 255")


def validate_password(password: str):
    assert isinstance(password, str)

    if 0 < len(password) <= 255:
        raise exceptions.ValidationError("Password length must be between 1 "
                                         "and 32")
