"""
The Bestory Project
"""

import sqlalchemy as sa

table = sa.Table(
    "topics",
    app.tbs.lib.db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),

    sa.Column("slug", sa.String(32), unique=True, nullable=False),
    sa.Column("title", sa.String(64), nullable=False),

    sa.Column("description", sa.Text, nullable=False),
    sa.Column("icon", sa.String(16), nullable=False),

    sa.Column("is_public", sa.Boolean, default=True, nullable=False),

    sa.Column("stories_count", sa.Integer, default=0, nullable=False),
)
