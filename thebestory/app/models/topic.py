"""
The Bestory Project
"""

from enum import Enum

from thebestory.app.lib import db


class Topic(db.model.Base):
    class Meta(Enum):
        TABLE = "topics"

    class Schema(Enum):
        ID = "id"  # primary key, integer

        TITLE = "title"  # varchar, max length: 64, not null
        SLUG = "slug"  # varchar, max length: 32, index, not null

        DESCRIPTION = "description"  # text, max len: 256, default: "", nullable
        ICON = "icon"  # varchar, max len: 16, default: "", not null

        STORIES_COUNT = "stories_count"  # foreign key, integer, index, not null

    def __init__(self, title: str, slug: str, description: str = "",
                 icon: str = ""):
        self._id = None

        self._title = title
        self._slug = slug

        self._description = description
        self._icon = icon

        self._stories_count = 0
