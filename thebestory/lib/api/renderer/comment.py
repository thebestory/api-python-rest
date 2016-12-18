"""
The Bestory Project
"""

from thebestory.lib import identifier


def render(comment):
    return {
        "id": identifier.to36(comment["id"]),
        "parent": {
            "id":
                identifier.to36(comment["parent"]["id"])
                if comment["parent"]["id"] is not None
                else None,
        },
        "author": {
            "id": comment["author"]["id"],
            "username": comment["author"]["username"]
        },
        "content": comment["content"],
        "comments": [render(c) for c in comment["comments"]],
        "likes_count": comment["likes_count"],
        "comments_count": comment["comments_count"],
        "submitted_date":
            comment["submitted_date"].isoformat()
            if comment["submitted_date"]
            else None,
        "edited_date":
            comment["edited_date"].isoformat()
            if comment["edited_date"]
            else None,
    }
