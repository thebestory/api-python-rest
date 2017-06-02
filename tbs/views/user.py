"""
The Bestory Project
"""


def render(user):
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "comments_count": user["comments_count"],
        "comment_likes_count": user["comment_reactions_count"],
        "story_likes_count": user["story_reactions_count"],
        "stories_count": user["stories_count"],
        "registered_date": user["registered_date"].isoformat()
    }
