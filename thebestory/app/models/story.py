"""
The Bestory Project
"""

import datetime

import pytz
import sqlalchemy as sa

from thebestory.app.lib import db

stories = sa.Table(
    "stories",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),
    # sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id"), index=True),
    sa.Column("topic_id", sa.Integer, sa.ForeignKey("topics.id"), index=True,
              nullable=False),

    sa.Column("content", sa.Text, nullable=False),

    sa.Column("submit_date", db.types.DateTime,
              default=datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
              nullable=False),
    sa.Column("edit_date", db.types.DateTime, nullable=True),
    sa.Column("publish_date", db.types.DateTime, nullable=True),
)
