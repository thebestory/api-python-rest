"""
The Bestory Project
"""

import sqlalchemy as sa

from thebestory.app.lib import db

table = sa.Table(
    "topics",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),

    sa.Column("title", sa.String(64), nullable=False),
    sa.Column("slug", sa.String(32), nullable=False),

    sa.Column("description", sa.Text, nullable=False),
    sa.Column("icon", sa.String(16), nullable=False),

    sa.Column("stories_count", sa.Integer, default=0, nullable=False),
)
