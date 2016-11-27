"""
The Bestory Project
"""

from asyncpg import pool


class Base:
    db: pool.Pool = None
