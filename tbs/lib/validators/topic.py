"""
The Bestory Project
"""

import re

from tbs.lib import exceptions


def validate_title(title: str):
    assert isinstance(title, str)

    if not 0 < len(title) <= 64:
        raise exceptions.ValidationError("Title length must be between 1 and "
                                         "64")


def validate_slug(slug: str):
    assert isinstance(slug, str)

    if re.match(r"[a-z]+[a-z0-9]*", slug) is None:
        raise exceptions.ValidationError("Slug must contains only a-z letters "
                                         "and digits, and starts with letter")

    if not 0 < len(slug) <= 32:
        raise exceptions.ValidationError("Slug length must be between 1 and "
                                         "32")


def validate_description(description: str):
    assert isinstance(description, str)


def validate_icon(icon: str):
    assert isinstance(icon, str)

    if re.match(r"[a-z0-9]+", icon) is None:
        raise exceptions.ValidationError("Icon hash must contains only a-z "
                                         "letters and digits")

    if not 0 < len(icon) <= 16:
        raise exceptions.ValidationError("Icon hash length must be between 1 "
                                         "and 32")


def validate_is_active(is_active: bool):
    assert isinstance(is_active, bool)
