"""
The Bestory Project
"""

from tbs.views import story as story_view
from tbs.views import user as user_view


def render(comment, like=None):
    _ = {
        "id": comment["id"],
        "author": _render_author(comment["author_id"], comment.get("author")),
        "story": _render_story(comment["story_id"], comment.get("story")),
        "content": comment["content"],
        "likes_count": comment["reactions_count"],
        "is_removed": comment["is_removed"],
        "submitted_date": comment["submitted_date"].isoformat(),
        "edited_date": _render_date(comment["edited_date"])
    }

    if like is not None:
        _["is_liked"] = like

    return _


def _render_author(id, author=None):
    if author is None:
        return {"id": id}
    else:
        return user_view.render(author)


def _render_story(id, story=None):
    if story is None:
        return {"id": id}
    else:
        return story_view.render(story)


def _render_date(date):
    if date is not None:
        return date.isoformat()
    else:
        return None
