"""
The Bestory Project
"""

from collections import OrderedDict


ERROR = {
    # API errors
    1001: "Server error",
    1002: "Endpoint not found",

    # Access errors
    2001: "Too many requests",
    2002: "Unauthorized",
    2003: "Insufficient permission",

    # Listing and method limits errors
    3001: "Incorrect listing request",
    3002: "Incorrect submit request",
    3003: "Incorrect signup request",

    # Object of action errors
    4001: "Unknown user",
    4002: "Unknown topic",
    4003: "Unknown comment",
    4004: "Unknown story",
}


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
