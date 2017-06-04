"""
The Bestory Project
"""

from tbs.views import user as user_view


def render(reaction, render_removed_status=False):
    _ = {
        "user": _render_user(reaction["user_id"], reaction.get("user")),
        "submitted_date": reaction["submitted_date"].isoformat()
    }

    if render_removed_status:
        _["is_removed"] = reaction["is_removed"]

    return _


def _render_user(id, user=None):
    if user is None:
        return {"id": id}
    else:
        return user_view.render(user)
