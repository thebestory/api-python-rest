"""
The Bestory Project
"""

import sqlalchemy as sa

from thebestory.app.lib import db

table = sa.Table(
    "users",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),

    sa.Column("username", sa.String(32), index=True),
)
