"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.protocol import Record

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
    Get a single topic by it's slug.
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
                is_active=is_active
            )
        )

        await conn.execute(query, *params)
        return await get(conn=conn, id=snowflake["id"])


async def update(conn: Connection, id: int, **kwargs):
    """
    Update the topic.
    """
    query = schema.topics.update().where(schema.topics.c.id == id)

    if 'title' in kwargs:
        query = query.values(title=kwargs['title'])

    if 'slug' in kwargs:
        query = query.values(slug=kwargs['slug'])

    if 'description' in kwargs:
        query = query.values(description=kwargs['description'])

    if 'icon' in kwargs:
        query = query.values(icon=kwargs['icon'])

    if 'is_active' in kwargs:
        query = query.values(is_active=kwargs['is_active'])

    query, params = asyncpgsa.compile_query(query)

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def increment_stories_counter(conn: Connection, id: int):
    """
    Increment topic's stories counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.topics.update().where(schema.topics.c.id == id).values(
            stories_count=schema.topics.c.stories_count + 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def decrement_stories_counter(conn: Connection, id: int):
    """
    Decrement topic's stories counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.topics.update().where(schema.topics.c.id == id).values(
            stories_count=schema.topics.c.stories_count - 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)
