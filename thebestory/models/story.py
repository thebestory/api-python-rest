"""
The Bestory
thebestory.models.story
"""
import datetime
from sqlalchemy import *
from sqlalchemy.orm import relation

from thebestory.models import Model
from thebestory.lib import db


class Story(Model):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    # author_id = Column(Integer, ForeignKey("author.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))

    content = Column(Text)

    submit_date = Column(db.DateTime, default=datetime.datetime.now())
    edit_date = Column(db.DateTime, nullable=True)
    publish_date = Column(db.DateTime, nullable=True)

    # author = relation("User", back_populates="stories")
    topic = relation("Topic", back_populates="stories")
