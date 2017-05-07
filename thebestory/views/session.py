"""
The Bestory Project
"""

from thebestory import views


def render(session):
    return {
        "jwt": session["jwt"],
        "user": render_user(session["user_id"], session["user"]),
        "created_date": session["created_date"].isoformat(),
        "expired_date": session["expired_date"].isoformat()
    }


def render_user(user_id, user=None):
    if user is None:
        return {"id": user_id}
    else:
        return views.user.render(user)
