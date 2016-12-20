"""
The Bestory Project
"""

from thebestory.lib import identifier
from . import topic


def render(story):
    return {
        "id": identifier.to36(story["id"]),
        "topic":
            topic.render(story["topic"])
            if story["topic"] is not None
            else None,
        "content": story["content"],
        "is_liked": story.get("is_liked"),
        "likes_count": story["likes_count"],
        "comments_count": story["comments_count"],
        "submitted_date":
            story["submitted_date"].isoformat()
            if story["submitted_date"]
            else None,
        "edited_date":
            story["edited_date"].isoformat()
            if story["edited_date"]
            else None,
        "published_date":
            story["published_date"].isoformat()
            if story["published_date"]
            else None
    }
