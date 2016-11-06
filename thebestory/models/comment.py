"""
The Bestory
thebestory.models.comment
"""

from sqlalchemy import *
from sqlalchemy.orm import relation

from thebestory.models.thing import (
    LikeableThing,
    CommentableThing,
)
from thebestory.models.user import User


class Comment(LikeableThing, CommentableThing):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"))

    content = Column(Text)

    submit_date = Column(DateTime)
    edit_date = Column(DateTime, nullable=True)

    author = relation(User, back_populates="comments")


class CommentableThing(Thing):
    comments_count = Column(Integer)
