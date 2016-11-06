"""
The Bestory
thebestory.models.user
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relation

from thebestory.models.comment import Comment
from thebestory.models.like import Like
from thebestory.models.story import Story


class User:
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String)

    signup_date = Column(DateTime)

    stories_count = Column(Integer)
    comments_count = Column(Integer)
    likes_count = Column(Integer)

    stories = relation(Story, back_populates="author")
    comments = relation(Comment, back_populates="author")
    likes = relation(Like, back_populates="user")
