"""
The Bestory Project
"""

from asyncpg.connection import Connection
from asyncpg.protocol import Record
import asyncpgsa

from tbs.lib import schema
from tbs.lib.stores import snowflake as snowflake_store


SNOWFLAKE_TYPE = "topic"


async def get(conn: Connection, id: int) -> Record:
    """
    Get a single topic.
    """

    query, params = asyncpgsa.compile_query(
        schema.topics.select().where(schema.topics.c.id == id)
    )

    topic = await conn.fetchrow(query, *params)

    if not topic:
        raise ValueError

    return topic


async def get_by_slug(conn: Connection, slug: str) -> Record:
    """
    Get a single topic.
    """

    query, params = asyncpgsa.compile_query(
        schema.topics.select().where(schema.topics.c.slug == slug)
    )

    topic = await conn.fetchrow(query, *params)

    if not topic:
        raise ValueError

    return topic


async def create(conn: Connection,
                 title: str,
                 slug: str,
                 description: str,
                 icon: str,
                 stories_count: int=0,
                 is_active: bool=False) -> Record:
    """
    Create a new topic.
    """

    async with conn.transaction():
        snowflake = await snowflake_store.create(conn=conn, type=SNOWFLAKE_TYPE)

        query, params = asyncpgsa.compile_query(
            schema.topics.insert().values(
                id=snowflake["id"],
                title=title,
                slug=slug,
                description=description,
                icon=icon,
                stories_count=stories_count,
                is_active=is_active
            )
        )

        await conn.execute(query, *params)
        return await get(conn=conn, id=snowflake["id"])
