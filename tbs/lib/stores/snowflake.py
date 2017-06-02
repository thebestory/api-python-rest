"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.protocol import Record

from tbs import snowflake_generator
from tbs.lib import exceptions
from tbs.lib import schema


SNOWFLAKE_TYPE = "id"


async def get(conn: Connection, id: int) -> Record:
    """
    Get a single Snowflake ID.
    """

    query, params = asyncpgsa.compile_query(
        schema.snowflakes.select().where(schema.snowflakes.c.id == id)
    )

    snowflake = await conn.fetchrow(query, *params)

    if not snowflake:
        raise exceptions.NotFoundError

    return snowflake


async def create(conn: Connection, type: str) -> Record:
    """
    Create a new Snowflake ID.
    """

    id = snowflake_generator.generate()
    if not isinstance(id, int):
        raise ValueError

    query, params = asyncpgsa.compile_query(
        schema.snowflakes.insert().values(id=id, type=type)
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)
