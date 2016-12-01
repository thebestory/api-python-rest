"""
The Bestory Project
"""

from datetime import datetime
import pytz
import sqlalchemy as sa

from thebestory.app.lib import db

table = sa.Table(
    "stories",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id"), index=True,
              nullable=False),
    sa.Column("topic_id", sa.Integer, sa.ForeignKey("topics.id"), index=True,
              nullable=False),

    sa.Column("content", sa.Text(8192), nullable=False),

    sa.Column("likes_count", sa.Integer, default=0, nullable=False),
    sa.Column("comments_count", sa.Integer, default=0, nullable=False),

    sa.Column("is_approved", sa.Boolean, default=False, nullable=False),
    sa.Column("is_removed", sa.Boolean, default=False, nullable=False),

    sa.Column("submitted_date", db.types.DateTime,
              default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc),
              nullable=False),
    sa.Column("edited_date", db.types.DateTime, nullable=True),
    sa.Column("published_date", db.types.DateTime, nullable=True),
)
