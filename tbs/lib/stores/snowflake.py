"""
The Bestory Project
"""

from asyncpg import Connection
from asyncpg import Record
import asyncpgsa

from tbs import snowflake_generator
from tbs.lib import schema


SNOWFLAKE_TYPE = "id"


async def get(id: int, conn: Connection) -> Record:
    """
    Get a single Snowflake ID.
    """

    snowflake = await conn.fetchrow(asyncpgsa.compile_query(
        schema.snowflakes.select().where(schema.snowflakes.c.id == id)
    ))

    if not snowflake:
        raise ValueError

    return snowflake


async def create(type: str, conn: Connection) -> Record:
    """
    Create a new Snowflake ID.
    """

    id = snowflake_generator.generate()
    if not isinstance(id, int):
        raise ValueError

    await conn.execute(asyncpgsa.compile_query(
        schema.snowflakes.insert().values(id=id, type=type)
    ))

    return await get(id=id, conn=conn)
