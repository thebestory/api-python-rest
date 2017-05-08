"""
The Bestory Project
"""

from .comment import table as comments
from .like import (
    comment_table as comment_likes,
    story_table as story_likes
)
from .story import table as stories
from .topic import table as topics
from .user import table as users
