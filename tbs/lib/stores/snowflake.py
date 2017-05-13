"""
The Bestory Project
"""

from asyncpgsa.connection import SAConnection
from asyncpgsa.record import Record

from tbs import db
from tbs import snowflake
from tbs.lib import schema


SNOWFLAKE_TYPE = "id"


async def get(id_: int, conn: SAConnection=None) -> Record:
    """
    Get Snowflake ID.
    """

    if conn is None:
        conn = db.pool.acquire()

    sf = await conn.fetchrow(schema.snowflakes.select().where(
        schema.snowflakes.c.id == id_
    ))

    if sf:
        return sf
    else:
        raise ValueError


async def create(type_: str=SNOWFLAKE_TYPE, conn: SAConnection=None) -> int:
    """
    Create a new Snowflake ID.
    """

    if conn is None:
        conn = db.pool.acquire()

    sf = snowflake.generate()
    if not isinstance(sf, int):
        raise ValueError

    id_ = await conn.insert(schema.snowflakes.insert().values(
        id=sf,
        type=type_
    ))

    if id_ is None:
        raise ValueError

    return sf
