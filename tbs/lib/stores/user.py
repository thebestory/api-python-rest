"""
The Bestory Project
"""

from datetime import datetime
from typing import Optional

from asyncpg.connection import Connection
from asyncpg.protocol import Record
import asyncpgsa

import pendulum

from tbs.lib import schema
from tbs.lib.stores import snowflake as snowflake_store


SNOWFLAKE_TYPE = "user"


async def get(id: int, conn: Connection) -> Record:
    """
    Get a single user.
    """

    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.id == id)
    )

    user = await conn.fetchrow(query, *params)

    if not user:
        raise ValueError

    return user


async def create(conn: Connection,
                 username: str,
                 email: str,
                 password: str,
                 comments_count: int=0,
                 comment_reactions_count: int=0,
                 story_reactions_count: int=0,
                 stories_count: int=0,
                 registered_date: Optional[datetime]=None) -> Record:
    """
    Create a new user.
    """
    if registered_date is None:
        registered_date = datetime.utcnow().replace(tzinfo=pendulum.UTC)

    async with conn.transaction():
        snowflake = await snowflake_store.create(type=SNOWFLAKE_TYPE, conn=conn)

        query, params = asyncpgsa.compile_query(
            schema.users.insert().values(
                id=snowflake["id"],
                username=username,
                email=email,
                password=password,
                comments_count=comments_count,
                comment_reactions_count=comment_reactions_count,
                story_reactions_count=story_reactions_count,
                stories_count=stories_count,
                registered_date=registered_date
            )
        )

        await conn.execute(query, *params)
        return await get(id=snowflake["id"], conn=conn)
