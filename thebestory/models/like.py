"""
The Bestory
thebestory.models.like
"""

import enum

from sqlalchemy import *
from sqlalchemy.orm import relation

from thebestory.models.user import User
from thebestory.models.thing import Thing


class Like:
    class State(enum.IntEnum):
        LIKED = 1
        UNLIKED = 0

    def __init__(self, user: User, thing: Thing, state: State):
        pass


class LikeableThing(Thing):
    likes_count = Column(Integer)

