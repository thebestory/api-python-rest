"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib import validators
from tbs.lib.stores import snowflake as snowflake_store


SNOWFLAKE_TYPE = "topic"


async def list(conn: Connection,
               include_inactive: bool=False,
               only_inactive: bool=False) -> list:
    """List all topics."""
    include_inactive |= only_inactive
    query = schema.topics.select().order_by(schema.topics.c.title)

    if not include_inactive:
        query = query.where(schema.topics.c.is_active == True)
    if only_inactive:
        query = query.where(schema.topics.c.is_active == False)

    query, params = asyncpgsa.compile_query(query)

    try:
        rows = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    return [schema.topics.parse(row) for row in rows]


async def __get_execute(conn: Connection, query) -> dict:
    """Query executor."""
    query, params = asyncpgsa.compile_query(query)

    try:
        row = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not row:
        raise exceptions.NotFoundError
    return schema.topics.parse(row)

async def get(conn: Connection, id: int) -> dict:
    """Get a single topic."""
    return await __get_execute(
        conn, schema.topics.select().where(schema.topics.c.id == id))

async def get_by_slug(conn: Connection, slug: str) -> dict:
    """Get a single topic by it's slug."""
    return await __get_execute(
        conn, schema.topics.select().where(schema.topics.c.slug == slug))


async def create(conn: Connection,
                 title: str,
                 slug: str,
                 description: str,
                 icon: str,
                 is_active: bool=False) -> dict:
    """Create a new topic."""
    validators.topic.validate_title(title)
    validators.topic.validate_slug(slug)
    validators.topic.validate_description(description)
    validators.topic.validate_icon(icon)
    validators.topic.validate_is_active(is_active)

    async with conn.transaction():
        snowflake = await snowflake_store.create(conn=conn,
                                                 type=SNOWFLAKE_TYPE)

        query, params = asyncpgsa.compile_query(schema.topics.insert().values(
            id=snowflake["id"],
            title=title,
            slug=slug,
            description=description,
            icon=icon,
            is_active=is_active))

        try:
            await conn.execute(query, *params)
            return await get(conn=conn, id=snowflake["id"])
        except (PostgresError, exceptions.NotFoundError):
            raise exceptions.NotCreatedError


async def update(conn: Connection, id: int, **kwargs):
    """Update the topic."""
    query = schema.topics.update().where(schema.topics.c.id == id)

    if "title" in kwargs:
        validators.topic.validate_title(kwargs["title"])
        query = query.values(title=kwargs["title"])

    if "slug" in kwargs:
        validators.topic.validate_slug(kwargs["slug"])
        query = query.values(slug=kwargs["slug"])

    if "description" in kwargs:
        validators.topic.validate_description(kwargs["description"])
        query = query.values(description=kwargs["description"])

    if "icon" in kwargs:
        validators.topic.validate_icon(kwargs["icon"])
        query = query.values(icon=kwargs["icon"])

    if "is_active" in kwargs:
        validators.topic.validate_is_active(kwargs["is_active"])
        query = query.values(is_active=kwargs["is_active"])

    query, params = asyncpgsa.compile_query(query)

    try:
        async with conn.transaction():
            await conn.execute(query, *params)

            # If prev query executed successfully, then this query should be
            # executed successfully too
            return await get(conn=conn, id=id)
    except PostgresError:
        raise exceptions.NotUpdatedError


async def __update_counter(conn: Connection, id: int, query):
    """Change counter of the topic."""
    q, p = asyncpgsa.compile_query(query.where(schema.topics.c.id == id))

    try:
        await conn.execute(q, *p)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True

async def increment_stories_counter(conn: Connection, id: int):
    """Increment stories counter of the topic."""
    return await __update_counter(conn, id, schema.topics.update().values(
        stories_count=schema.topics.c.stories_count + 1))

async def decrement_stories_counter(conn: Connection, id: int):
    """Decrement stories counter of the topic."""
    return await __update_counter(conn, id, schema.topics.update().values(
        stories_count=schema.topics.c.stories_count - 1))
