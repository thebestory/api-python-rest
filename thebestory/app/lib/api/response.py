"""
The Bestory Project
"""

from thebestory.app.lib.api.code import WARNING, ERROR

__all__ = [
    "ok",
    "warning",
    "error"
]


def ok(data):
    return {
        "status": "ok",
        "data": data
    }


def warning(code, data):
    return {
        "status": "warning",
        "warning": {
            "code": code,
            "message": WARNING[code]
        },
        "data": data
    }


def error(code):
    return {
        "status": "error",
        "error": {
            "code": code,
            "message": ERROR[code]
        }
    }
