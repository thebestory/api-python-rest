"""
The Bestory Project
"""

from tbs.views import user as user_view
from tbs.views import topic as topic_view


def render(story, like=None):
    _ = {
        "id": story["id"],
        "author": _render_author(story["author_id"], story.get("author")),
        "topic": _render_topic(story["topic_id"], story.get("topic")),
        "content": story["content"],
        "comments_count": story["comments_count"],
        "likes_count": story["reactions_count"],
        "is_published": story["is_published"],
        "is_removed": story["is_removed"],
        "submitted_date": story["submitted_date"].isoformat(),
        "published_date": _render_date(story["published_date"]),
        "edited_date": _render_date(story["edited_date"])
    }

    if like is not None:
        _["is_liked"] = like

    return _


def _render_author(id, author=None):
    if author is None:
        return {"id": id}
    else:
        return user_view.render(author)


def _render_topic(id, topic=None):
    if topic is None:
        return {"id": id}
    else:
        return topic_view.render(topic)


def _render_date(date):
    if date is not None:
        return date.isoformat()
    else:
        return None
