"""
The Bestory Project
"""

from tbs.views import user as user_view
from tbs.views import topic as topic_view


def render(story, author, topic=None):
    return {
        "id": story["id"],
        "author": user_view.render(author),
        "topic": topic_view.render(topic) if topic is not None else None,
        "content": story["content"],
        "comments_count": story["comments_count"],
        "likes_count": story["likes_count"],
        "is_liked": story.get("is_liked"),
        "is_published": story["is_published"],
        "is_removed": story["is_removed"],
        "submitted_date": story["submitted_date"].isoformat(),
        "published_date": render_date(story["published_date"]),
        "edited_date": render_date(story["edited_date"])
    }


def render_date(date):
    if date is not None:
        return date.isoformat()
    else:
        return None
