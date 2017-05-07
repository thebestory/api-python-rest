"""
The Bestory Project
"""

from thebestory import views


def render(comment):
    return {
        "id": comment["id"],
        "author": render_author(comment["author_id"], comment.get("author")),
        "root": render_root(comment["root_id"]),
        "parent": render_parent(comment["parent_id"]),
        "content": comment["content"],
        "comments_count": comment["comments_count"],
        "likes_count": comment["likes_count"],
        "is_liked": comment.get("is_liked"),
        "is_published": comment["is_published"],
        "is_removed": comment["is_removed"],
        "submitted_date": comment["submitted_date"].isoformat(),
        "published_date": render_date(comment["published_date"]),
        "edited_date": render_date(comment["edited_date"])
    }


def render_author(author_id, author=None):
    if author is None:
        return {"id": author_id}
    else:
        return views.user.render(author)


def render_root(root_id):
    return {"id": root_id}


def render_parent(parent_id):
    return {"id": parent_id}


def render_date(date):
    if date is not None:
        return date.isoformat()
    else:
        return None
