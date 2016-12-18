"""
The Bestory Project
"""


def render(topic):
    return {
        "id": topic["id"],
        "slug": topic["slug"],
        "title": topic["title"],
        "icon": topic["icon"],
        "description": topic["description"],
        "stories_count": topic["stories_count"]
    }
