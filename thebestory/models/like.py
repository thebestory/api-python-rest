"""
The Bestory Project
"""

from enum import Enum

import pendulum
import sqlalchemy as sa

from thebestory.lib import db


class State(Enum):
    LIKE = True
    UNLIKE = False


story_table = sa.Table(
    "story_likes",
    db.meta.DATA,

    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), index=True,
              nullable=False),
    sa.Column("story_id", sa.Integer, sa.ForeignKey("stories.id"), index=True,
              nullable=False),

    sa.Column("state", sa.Boolean, nullable=False),

    sa.Column("timestamp", db.types.DateTime,
              default=pendulum.utcnow(),
              nullable=False)
)

comment_table = sa.Table(
    "comment_likes",
    db.meta.DATA,

    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), index=True,
              nullable=False),
    sa.Column("comment_id", sa.Integer,
              sa.ForeignKey("comments.id"), index=True, nullable=False),

    sa.Column("state", sa.Boolean, nullable=False),

    sa.Column("timestamp", db.types.DateTime,
              default=pendulum.utcnow(),
              nullable=False)
)
