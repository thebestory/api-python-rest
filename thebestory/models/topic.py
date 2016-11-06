"""
The Bestory
thebestory.models.topic
"""

from sqlalchemy import *
from sqlalchemy.orm import relation

from thebestory.models import Model


class Topic(Model):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    description = Column(Text)
    icon = Column(String)  # Icon hash

    stories_count = Column(Integer)

    stories = relation("Story", back_populates="topic")
