"""
The Bestory
thebestory.models.thing
"""

import abc

from thebestory.models import Model
from thebestory.models.comment import CommentableThing
from thebestory.models.like import LikeableThing


class Thing(abc.ABC, Model):
    pass
