"""
The Bestory Project
"""

import sqlalchemy as sa

from thebestory.app.lib import db

users = sa.Table(
    "users",
    db.meta.DATA,

    sa.Column("id", sa.Integer, primary_key=True),

    sa.Column("username", sa.String(32), index=True),
)

# class User:
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#
#     username = Column(String)
#
#     signup_date = Column(DateTime)
#
#     stories_count = Column(Integer)
#     comments_count = Column(Integer)
#     likes_count = Column(Integer)
#
#     stories = relation(Story, back_populates="author")
#     comments = relation(Comment, back_populates="author")
#     likes = relation(Like, back_populates="user")
