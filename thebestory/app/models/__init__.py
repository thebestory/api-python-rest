"""
The Bestory Project
"""

from thebestory.app.lib.db import meta

from thebestory.app.models.comment import table as comments
from thebestory.app.models.story import table as stories
from thebestory.app.models.topic import table as topics
from thebestory.app.models.user import table as users

from thebestory.app.models.like import (
    story_table as story_likes,
    comment_table as comment_likes
)
