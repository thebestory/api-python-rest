"""
The Bestory Project
"""

import abc
from asyncpg import pool


class Base:
    db: pool.Pool = None

    def __init__(self):
        pass

    @abc.abstractmethod
    async def commit(self):
        pass
