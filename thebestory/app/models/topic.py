"""
The Bestory Project
"""

import sqlalchemy as sa

from thebestory.app.lib import db

topics = sa.Table(
    "topics",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),

    sa.Column("title", sa.String(64), nullable=False),
    sa.Column("desc", sa.Text, default="", nullable=False),
    sa.Column("icon", sa.String(16), default="", nullable=False),

    sa.Column("stories_count", sa.Integer, default=0, nullable=False),
)
