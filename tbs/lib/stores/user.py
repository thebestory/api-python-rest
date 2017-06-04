"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError

from tbs.lib import exceptions
from tbs.lib import password as passutils
from tbs.lib import schema
from tbs.lib import validators
from tbs.lib.stores import snowflake as snowflake_store


SNOWFLAKE_TYPE = "user"


async def __get_execute(conn: Connection, query) -> dict:
    """Query executor."""
    query, params = asyncpgsa.compile_query(query)

    try:
        row = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not row:
        raise exceptions.NotFoundError
    return schema.users.parse(row)

async def get(conn: Connection, id: int) -> dict:
    """Get a single user."""
    return await __get_execute(
        conn, schema.users.select().where(schema.users.c.id == id))

async def get_by_username(conn: Connection, username: str) -> dict:
    """Get a single user by it's username."""
    return await __get_execute(
        conn, schema.users.select().where(schema.users.c.username == username))

async def get_by_email(conn: Connection, email: str) -> dict:
    """Get a single user by it's email."""
    return await __get_execute(
        conn, schema.users.select().where(schema.users.c.email == email))


async def create(conn: Connection,
                 username: str,
                 email: str,
                 password: str) -> dict:
    """Create a new user."""
    validators.user.validate_username(username)
    validators.user.validate_email(email)
    validators.user.validate_password(password)

    password = passutils.hash(password)

    async with conn.transaction():
        snowflake = await snowflake_store.create(conn=conn,
                                                 type=SNOWFLAKE_TYPE)

        query, params = asyncpgsa.compile_query(schema.users.insert().values(
            id=snowflake["id"],
            username=username,
            email=email,
            password=password))

        try:
            await conn.execute(query, *params)
            return await get(conn=conn, id=snowflake["id"])
        except (PostgresError, exceptions.NotFoundError):
            raise exceptions.NotCreatedError


async def update(conn: Connection, id: int, **kwargs) -> dict:
    """Update the user."""
    query = schema.users.update().where(schema.users.c.id == id)

    if "username" in kwargs:
        validators.user.validate_username(kwargs["username"])
        query = query.values(username=kwargs["username"])

    if "email" in kwargs:
        validators.user.validate_email(kwargs["email"])
        query = query.values(email=kwargs["email"])

    if "password" in kwargs:
        validators.user.validate_password(kwargs["password"])
        query = query.values(password=passutils.hash(kwargs["password"]))

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
    """Change counter of the user."""
    q, p = asyncpgsa.compile_query(query.where(schema.users.c.id == id))

    try:
        await conn.execute(q, *p)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True

async def increment_stories_counter(conn: Connection, id: int):
    """Increment stories counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        stories_count=schema.users.c.stories_count + 1))

async def increment_comments_counter(conn: Connection, id: int):
    """Increment comments counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        comments_count=schema.users.c.comments_count + 1))

async def increment_story_reactions_counter(conn: Connection, id: int):
    """Increment story reactions counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        story_reactions_count=schema.users.c.story_reactions_count + 1))

async def increment_comment_reactions_counter(conn: Connection, id: int):
    """Increment comment reactions counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        comment_reactions_count=schema.users.c.comment_reactions_count + 1))

async def decrement_stories_counter(conn: Connection, id: int):
    """Decrement stories counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        stories_count=schema.users.c.stories_count - 1))

async def decrement_comments_counter(conn: Connection, id: int):
    """Decrement comments counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        comments_count=schema.users.c.comments_count - 1))

async def decrement_story_reactions_counter(conn: Connection, id: int):
    """Decrement story reactions counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        story_reactions_count=schema.users.c.story_reactions_count - 1))

async def decrement_comment_reactions_counter(conn: Connection, id: int):
    """Decrement comment reactions counter of the user."""
    return __update_counter(conn, id, schema.users.update().values(
        comment_reactions_count=schema.users.c.comment_reactions_count - 1))
