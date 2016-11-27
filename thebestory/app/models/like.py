"""
The Bestory Project
"""

import abc
import pytz
from datetime import datetime
from enum import Enum

from thebestory.app.lib import db
from thebestory.app.models.comment import Comment
from thebestory.app.models.story import Story
from thebestory.app.models.user import User


class State(Enum):
    LIKE = True
    UNLIKE = False


class Like(db.model.Base, abc.ABC):
    class Schema:
        USER_ID = "user_id"  # foreign key, integer, index, not null
        STATE = "state"  # boolean, not null

        STATE_DATE = "state_date"  # datetime, default: now, not null

    def __init__(self, user: User, state: State):
        super().__init__()

        self._user = user
        self._state = state

        self._state_date = datetime.utcnow().replace(tzinfo=pytz.utc)


class StoryLike(Like):
    class Schema(Like.Schema):
        STORY_ID = "story_id"  # foreign key, integer, index, not null

    def __init__(self, user: User, story: Story, state: State):
        super().__init__(user, state)
        self._story = story


class CommentLike(Like):
    class Schema(Like.Schema):
        COMMENT_ID = "comment_id"  # foreign key, integer, index, not null

    def __init__(self, user: User, comment: Comment, state: State):
        super().__init__(user, state)
        self._comment = comment
