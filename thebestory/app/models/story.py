"""
The Bestory Project
"""

import pytz
from enum import Enum
from datetime import datetime

from thebestory.app.lib import db
from thebestory.app.models.topic import Topic
from thebestory.app.models.user import User


class Story(db.model.Base):
    class Meta(Enum):
        TABLE = "stories"

    class Schema(Enum):
        ID = "id"  # primary key, integer
        AUTHOR_ID = "author_id"  # foreign key, integer, index, not null
        TOPIC_ID = "topic_id"  # foreign key, integer, index, not null

        CONTENT = "content"  # text, max len: 8192, default: "", not null

        LIKES_COUNT = "likes_count"  # integer, default: 0, not null
        COMMENTS_COUNT = "comments_count"  # integer, default: 0, not null

        IS_APPROVED = "is_approved"  # boolean, default: False, not null
        IS_REMOVED = "is_removed"  # boolean, default: False, not null

        SUBMITTED_DATE = "submitted_date"  # datetime, default: now, not null
        EDITED_DATE = "edited_date"  # datetime, default: None, nullable
        PUBLISHED_DATE = "published_date"  # datetime, default: None, nullable

    def __init__(self, author: User, topic: Topic, content: str):
        super().__init__()

        self._id = None

        self._author = author
        self._topic = topic

        self._content = content

        self._likes_count = 0
        self._comments_count = 0

        self._is_approved = False
        self._is_removed = False

        self._submitted_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        self._edited_date = None
        self._published_date = None

