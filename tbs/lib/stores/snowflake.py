"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError

from tbs.lib import (
    data,
    exceptions,
    schema,
)
from tbs.lib.validators import snowflake as validators
from tbs.lib.snowflake import next_snowflake


SNOWFLAKE_TYPE = "id"


async def get(conn: Connection, id: int) -> dict:
    """
    Get a single Snowflake ID.
    """
    query, params = asyncpgsa.compile_query(
        schema.snowflakes.select().where(schema.snowflakes.c.id == id)
    )

    try:
        snowflake = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not snowflake:
        raise exceptions.NotFoundError

    return data.parse_snowflake(snowflake)


async def create(conn: Connection, type: str) -> dict:
    """
    Create a new Snowflake ID.
    """
    id = next_snowflake()

    validators.validate_id(id)
    validators.validate_type(type)

    query, params = asyncpgsa.compile_query(
        schema.snowflakes.insert().values(id=id, type=type)
    )

    try:
        async with conn.transaction():
            await conn.execute(query, *params)
            return await get(conn=conn, id=id)
    except (PostgresError, exceptions.NotFoundError):
        raise exceptions.NotCreatedError
