"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError

from tbs.lib import (
    data,
    exceptions,
    password,
    schema
)
from tbs.lib.stores import snowflake as snowflake_store
from tbs.lib.validators import user as validators


SNOWFLAKE_TYPE = "user"


async def get(conn: Connection, id: int) -> dict:
    """
    Get a single user.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.id == id)
    )

    try:
        user = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not user:
        raise exceptions.NotFoundError

    return data.parse_user(user)


async def get_by_username(conn: Connection, username: str) -> dict:
    """
    Get a single user by it's username.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.username == username)
    )

    try:
        user = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not user:
        raise exceptions.NotFoundError

    return data.parse_user(user)


async def get_by_email(conn: Connection, email: str) -> dict:
    """
    Get a single user by it's email.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.select().where(schema.users.c.email == email)
    )

    try:
        user = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not user:
        raise exceptions.NotFoundError

    return data.parse_user(user)


async def create(conn: Connection,
                 username: str,
                 email: str,
                 password_: str) -> dict:
    """
    Create a new user.
    """
    validators.validate_username(username)
    validators.validate_email(email)
    validators.validate_password(password_)

    password_ = password.hash(password_)

    async with conn.transaction():
        snowflake = await snowflake_store.create(
            conn=conn, type=SNOWFLAKE_TYPE
        )

        query, params = asyncpgsa.compile_query(
            schema.users.insert().values(
                id=snowflake["id"],
                username=username,
                email=email,
                password=password_
            )
        )

        try:
            await conn.execute(query, *params)
            return await get(conn=conn, id=snowflake["id"])
        except (PostgresError, exceptions.NotFoundError):
            raise exceptions.NotCreatedError


async def update(conn: Connection, id: int, **kwargs) -> dict:
    """
    Update the user.
    """
    query = schema.users.update().where(schema.users.c.id == id)

    if "username" in kwargs:
        validators.validate_username(kwargs["username"])
        query = query.values(username=kwargs["username"])

    if "email" in kwargs:
        validators.validate_email(kwargs["email"])
        query = query.values(email=kwargs["email"])

    if "password" in kwargs:
        validators.validate_password(kwargs["password"])
        query = query.values(password=password.hash(kwargs["password"]))

    query, params = asyncpgsa.compile_query(query)

    try:
        async with conn.transaction():
            await conn.execute(query, *params)

            # If prev query executed successfully, then this query should be
            # executed successfully too
            return await get(conn=conn, id=id)
    except PostgresError:
        raise exceptions.NotUpdatedError


async def increment_comments_counter(conn: Connection, id: int):
    """
    Increment user's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comments_count=schema.users.c.comments_count + 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def increment_comment_reactions_counter(conn: Connection, id: int):
    """
    Increment user's comment reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comment_reactions_count=schema.users.c.comment_reactions_count + 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def increment_story_reactions_counter(conn: Connection, id: int):
    """
    Increment user's story reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            story_reactions_count=schema.users.c.story_reactions_count + 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def increment_stories_counter(conn: Connection, id: int):
    """
    Increment user's stories counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            stories_count=schema.users.c.stories_count + 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def decrement_comments_counter(conn: Connection, id: int):
    """
    Decrement user's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comments_count=schema.users.c.comments_count - 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def decrement_comment_reactions_counter(conn: Connection, id: int):
    """
    Decrement user's comment reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            comment_reactions_count=schema.users.c.comment_reactions_count - 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def decrement_story_reactions_counter(conn: Connection, id: int):
    """
    Decrement user's story reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            story_reactions_count=schema.users.c.story_reactions_count - 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def decrement_stories_counter(conn: Connection, id: int):
    """
    Decrement user's stories counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.users.update().where(schema.users.c.id == id).values(
            stories_count=schema.users.c.stories_count - 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True
