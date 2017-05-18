"""
The Bestory Project
"""

from asyncpg.connection import Connection
from asyncpg.protocol import Record
import asyncpgsa

from tbs.lib import schema
from tbs.lib.stores import snowflake as snowflake_store


SNOWFLAKE_TYPE = "user"


async def get(id: int, conn: Connection) -> Record:
    """
    Get a single user.
    """

    user = await conn.fetchrow(asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.id == id)
    ))

    if not user:
        raise ValueError

    return user


async def create(username: str,
                 email: str,
                 password: str,
                 conn: Connection) -> Record:
    """
    Create a new user.
    """

    with conn.transaction() as conn:
        snowflake = await snowflake_store.create(type=SNOWFLAKE_TYPE, conn=conn)

        await conn.execute(asyncpgsa.compile_query(
            schema.users.insert().values(
                id=snowflake["id"],
                username=username,
                email=email,
                password=password
            )
        ))

        return await get(id=snowflake["id"], conn=conn)
