"""
The Bestory Project
"""

from datetime import datetime
from typing import Optional

import asyncpgsa
import pendulum
from asyncpg.connection import Connection
from asyncpg.protocol import Record

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib.stores import snowflake as snowflake_store
from tbs.lib.stores import user as user_store
from tbs.lib.stores import topic as topic_store


SNOWFLAKE_TYPE = "story"


async def get(conn: Connection, id: int) -> Record:
    """
    Get a single story.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.select().where(schema.stories.c.id == id)
    )

    story = await conn.fetchrow(query, *params)

    if not story:
        raise exceptions.NotFoundError

    return story


async def create(conn: Connection,
                 author_id: int,
                 content: str,
                 topic_id: Optional[int]=None,
                 is_published: bool=False,
                 is_removed: bool=False,
                 published_date: Optional[datetime]=None) -> Record:
    """
    Create a new story.
    """
    if is_published and published_date is None:
        published_date = datetime.utcnow().replace(tzinfo=pendulum.UTC)

    async with conn.transaction():
        snowflake = await snowflake_store.create(
            conn=conn,
            type=SNOWFLAKE_TYPE
        )

        query, params = asyncpgsa.compile_query(
            schema.stories.insert().values(
                id=snowflake["id"],
                author_id=author_id,
                topic_id=topic_id,
                content=content,
                is_published=is_published,
                is_removed=is_removed,
                published_date=published_date
            )
        )

        await conn.execute(query, *params)
        story = await get(conn=conn, id=snowflake["id"])

        await user_store.increment_stories_counter(conn=conn, id=author_id)

        if topic_id is not None:
            await topic_store.increment_stories_counter(conn=conn, id=topic_id)

        return story


async def update(conn: Connection, id: int, **kwargs):
    """
    Update the story.
    """
    query = schema.stories.update().where(schema.stories.c.id == id)

    if "topic_id" in kwargs:
        query = query.values(topic_id=kwargs["topic_id"])

    if "content" in kwargs:
        query = query.values(
            content=kwargs["content"],
            edited_date=datetime.utcnow().replace(tzinfo=pendulum.UTC)
        )

    if "is_published" in kwargs:
        query = query.values(is_published=kwargs["is_published"])

        if kwargs["is_published"]:
            query = query.values(
                published_date=datetime.utcnow().replace(tzinfo=pendulum.UTC)
            )

    if "is_removed" in kwargs:
        query = query.values(is_removed=kwargs["is_removed"])

    if "published_date" in kwargs:
        query = query.values(is_active=kwargs["published_date"])

    query, params = asyncpgsa.compile_query(query)

    async with conn.transaction():
        await conn.execute(query, *params)
        return await get(conn=conn, id=id)


async def increment_comments_counter(conn: Connection, id: int):
    """
    Increment story's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            comments_count=schema.stories.c.comments_count + 1
        )
    )

    async with conn.transaction():
        await conn.execute(query, *params)
        return await get(conn=conn, id=id)


async def increment_reactions_counter(conn: Connection, id: int):
    """
    Increment story's reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            reactions_count=schema.stories.c.reactions_count + 1
        )
    )

    async with conn.transaction():
        await conn.execute(query, *params)
        return await get(conn=conn, id=id)


async def decrement_comments_counter(conn: Connection, id: int):
    """
    Decrement story's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            comments_count=schema.stories.c.comments_count - 1
        )
    )

    async with conn.transaction():
        await conn.execute(query, *params)
        return await get(conn=conn, id=id)


async def decrement_reactions_counter(conn: Connection, id: int):
    """
    Decrement story's reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            reactions_count=schema.stories.c.reactions_count - 1
        )
    )

    async with conn.transaction():
        await conn.execute(query, *params)
        return await get(conn=conn, id=id)
