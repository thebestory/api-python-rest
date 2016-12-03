"""
The Bestory Project
"""

import sqlalchemy as sa

from thebestory.app.lib import db

table = sa.Table(
    "users",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),

    sa.Column("username", sa.String(32), unique=True),

    sa.Column("stories_count", sa.Integer, default=0, nullable=False),
    sa.Column("comments_count", sa.Integer, default=0, nullable=False),
    sa.Column("story_likes_count", sa.Integer, default=0, nullable=False),
    sa.Column("comment_likes_count", sa.Integer, default=0, nullable=False),
)
