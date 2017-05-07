"""
The Bestory Project
"""

from thebestory import views


def render(story):
    return {
        "id": story["id"],
        "author": render_author(story["author_id"], story.get("author")),
        "topic": render_topic(story["topic"], story.get("topic")),
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


def render_author(author_id, author=None):
    if author is None:
        return {"id": author_id}
    else:
        return views.user.render(author)


def render_topic(topic_id, topic=None):
    if topic is None:
        return {"id": topic_id}
    else:
        return views.topic.render(topic)


def render_date(date):
    if date is not None:
        return date.isoformat()
    else:
        return None
