"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.protocol import Record

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib.stores import snowflake as snowflake_store


SNOWFLAKE_TYPE = "user"


async def get(conn: Connection, id: int) -> Record:
    """
    Get a single user.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.id == id)
    )

    user = await conn.fetchrow(query, *params)

    if not user:
        raise exceptions.NotFoundError

    return user


async def get_by_username(conn: Connection, username: str) -> Record:
    """
    Get a single user by it's username.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.username == username)
    )

    user = await conn.fetchrow(query, *params)

    if not user:
        raise exceptions.NotFoundError

    return user


async def get_by_email(conn: Connection, email: str) -> Record:
    """
    Get a single user by it's email.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.email == email)
    )

    user = await conn.fetchrow(query, *params)

    if not user:
        raise exceptions.NotFoundError

    return user


async def create(conn: Connection,
                 username: str,
                 email: str,
                 password: str) -> Record:
    """
    Create a new user.
    """
    async with conn.transaction():
        snowflake = await snowflake_store.create(conn=conn, type=SNOWFLAKE_TYPE)

        query, params = asyncpgsa.compile_query(
            schema.users.insert().values(
                id=snowflake["id"],
                username=username,
                email=email,
                password=password
            )
        )

        try:
            await conn.execute(query, *params)
            return await get(conn=conn, id=snowflake["id"])
        except:
            raise exceptions.NotCreatedError


async def update(conn: Connection, id: int, **kwargs) -> Record:
    """
    Update the user.
    """
    query = schema.users.update().where(schema.users.c.id == id)

    if "username" in kwargs:
        query = query.values(username=kwargs["username"])

    if "email" in kwargs:
        query = query.values(email=kwargs["email"])

    if "password" in kwargs:
        query = query.values(password=kwargs["password"])

    query, params = asyncpgsa.compile_query(query)

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def increment_comments_counter(conn: Connection, id: int):
    """
    Increment user's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comments_count=schema.users.c.comments_count + 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def increment_comment_reactions_counter(conn: Connection, id: int):
    """
    Increment user's comment reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comment_reactions_count=schema.users.c.comment_reactions_count + 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def increment_story_reactions_counter(conn: Connection, id: int):
    """
    Increment user's story reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            story_reactions_count=schema.users.c.story_reactions_count + 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def increment_stories_counter(conn: Connection, id: int):
    """
    Increment user's stories counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            stories_count=schema.users.c.stories_count + 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def decrement_comments_counter(conn: Connection, id: int):
    """
    Decrement user's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comments_count=schema.users.c.comments_count - 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def decrement_comment_reactions_counter(conn: Connection, id: int):
    """
    Decrement user's comment reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comment_reactions_count=schema.users.c.comment_reactions_count - 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def decrement_story_reactions_counter(conn: Connection, id: int):
    """
    Decrement user's story reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            story_reactions_count=schema.users.c.story_reactions_count - 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)


async def decrement_stories_counter(conn: Connection, id: int):
    """
    Decrement user's stories counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            stories_count=schema.users.c.stories_count - 1
        )
    )

    await conn.execute(query, *params)
    return await get(conn=conn, id=id)
