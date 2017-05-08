"""
The Bestory Project
"""

from collections import OrderedDict

from tbs.lib.api.code import ERROR

__all__ = [
    "ok",
    "error"
]


def ok(data):
    return OrderedDict([
        ("status", "ok"),
        ("data", data)
    ])


def error(code):
    return OrderedDict([
        ("status", "error"),
        ("error", OrderedDict(
            code=code,
            message=ERROR[code]
        ))
    ])
