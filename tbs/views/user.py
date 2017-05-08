"""
The Bestory Project
"""


def render(user):
    return {
        "id": user["id"],
        "username": user["username"],
        "comments_count": user["comments_count"],
        "likes_count": user["likes_count"],
        "stories_count": user["stories_count"],
        "registered_date": user["registered_date"].isoformat()
    }
