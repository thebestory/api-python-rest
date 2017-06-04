"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib import snowflake
from tbs.lib import validators


SNOWFLAKE_TYPE = "id"


async def get(conn: Connection, id: int) -> dict:
    """Get a single Snowflake ID."""
    query, params = asyncpgsa.compile_query(
        schema.snowflakes.select().where(schema.snowflakes.c.id == id))

    try:
        row = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not row:
        raise exceptions.NotFoundError
    return schema.snowflakes.parse(row)


async def create(conn: Connection, type: str) -> dict:
    """Create a new Snowflake ID."""
    id = snowflake.generate()

    validators.snowflake.validate_id(id)
    validators.snowflake.validate_type(type)

    query, params = asyncpgsa.compile_query(
        schema.snowflakes.insert().values(id=id, type=type))

    try:
        async with conn.transaction():
            await conn.execute(query, *params)
            return await get(conn=conn, id=id)
    except (PostgresError, exceptions.NotFoundError):
        raise exceptions.NotCreatedError
