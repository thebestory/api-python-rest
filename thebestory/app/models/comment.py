"""
The Bestory Project
"""

import pytz
from datetime import datetime
from enum import Enum

from thebestory.app.lib import db
from thebestory.app.models.user import User
from thebestory.app.models.story import Story


class Comment(db.model.Base):
    class Meta(Enum):
        TABLE = "comments"

    class Schema(Enum):
        ID = "id"  # primary key, integer
        AUTHOR_ID = "author_id"  # foreign key, integer, index, not null
        STORY_ID = "story_id"  # foreign key, integer, index, not null

        CONTENT = "content"  # text, max len: 4096, default: "", not null

        LIKES_COUNT = "likes_count"  # integer, default: 0, not null
        COMMENTS_COUNT = "comments_count"  # integer, default: 0, not null

        IS_REMOVED = "is_removed"  # boolean, default: False, not null

        SUBMITTED_DATE = "submitted_date"  # datetime, default: now, not null
        EDITED_DATE = "edited_date"  # datetime, default: None, nullable

    def __init__(self, author: User, story: Story, content: str):
        self._id = None
        self._author = author
        self._story = story

        self._content = content

        self._likes_count = 0
        self._comments_count = 0

        self._is_removed = False

        self._submitted_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        self._edited_date = None

