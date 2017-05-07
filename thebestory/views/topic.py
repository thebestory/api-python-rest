"""
The Bestory Project
"""


def render(topic):
    return {
        "id": topic["id"],
        "slug": topic["slug"],
        "title": topic["title"],
        "description": topic["description"],
        "icon": topic["icon"],
        "stories_count": topic["stories_count"],
        "is_active": topic["is_active"]
    }
