"""
The Bestory Project
"""

from tbs.views import user as user_view


def render(session):
    return {
        "jwt": session["jwt"],
        "user": user_view.render(session["user"])
    }
