"""
The Bestory Project
"""

from enum import Enum

from thebestory.app.lib import db


class User(db.model.Base):
    class Meta(Enum):
        TABLE = "users"

    class Schema(Enum):
        ID = "id"  # primary key, integer
        USERNAME = "username"  # varchar, max len: 32, not null

    def __init__(self, username: str):
        self._id = None

        self._username = username
