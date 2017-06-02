"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.protocol import Record

from tbs.lib import schema


async def list_by_user(conn: Connection,
                       user_id: int,
                       removed: bool=False) -> Record:
    """
    List reactions by user.
    """
    query = schema.reactions.select() \
        .where(schema.reactions.c.user_id == user_id) \
        .order_by(schema.reactions.c.submitted_date.desc())

    if not removed:
        query = query.where(schema.reactions.c.is_removed == False)

    query, params = asyncpgsa.compile_query(query)

    return await conn.fetch(query, *params)


async def list_by_object(conn: Connection,
                         object_id: int,
                         removed: bool=False) -> Record:
    """
    List reactions by object.
    """
    query = schema.reactions.select() \
        .where(schema.reactions.c.object_id == object_id) \
        .order_by(schema.reactions.c.submitted_date.desc())

    if not removed:
        query = query.where(schema.reactions.c.is_removed == False)

    query, params = asyncpgsa.compile_query(query)

    return await conn.fetch(query, *params)


async def list_by_user_and_reaction(conn: Connection,
                                    user_id: int,
                                    reaction_id: int,
                                    removed: bool=False) -> Record:
    """
    List reactions by user and reaction.
    """
    query = schema.reactions.select() \
        .where(schema.reactions.c.user_id == user_id) \
        .where(schema.reactions.c.reaction_id == reaction_id) \
        .order_by(schema.reactions.c.submitted_date.desc())

    if not removed:
        query = query.where(schema.reactions.c.is_removed == False)

    query, params = asyncpgsa.compile_query(query)

    return await conn.fetch(query, *params)


async def list_by_user_and_object(conn: Connection,
                                  user_id: int,
                                  object_id: int,
                                  removed: bool=False) -> Record:
    """
    List reactions by user and object.
    """
    query = schema.reactions.select() \
        .where(schema.reactions.c.user_id == user_id) \
        .where(schema.reactions.c.object_id == object_id) \
        .order_by(schema.reactions.c.submitted_date.desc())

    if not removed:
        query = query.where(schema.reactions.c.is_removed == False)

    query, params = asyncpgsa.compile_query(query)

    return await conn.fetch(query, *params)


async def list_by_object_and_reaction(conn: Connection,
                                      object_id: int,
                                      reaction_id: int,
                                      removed: bool=False) -> Record:
    """
    List reactions by object and reaction.
    """
    query = schema.reactions.select() \
        .where(schema.reactions.c.object_id == object_id) \
        .where(schema.reactions.c.reaction_id == reaction_id) \
        .order_by(schema.reactions.c.submitted_date.desc())

    if not removed:
        query = query.where(schema.reactions.c.is_removed == False)

    query, params = asyncpgsa.compile_query(query)

    return await conn.fetch(query, *params)


async def list_by_user_and_object_and_reaction(conn: Connection,
                                               user_id: int,
                                               object_id: int,
                                               reaction_id: int,
                                               removed: bool=False) -> Record:
    """
    List reactions by user, object and reaction.
    """
    query = schema.reactions.select() \
        .where(schema.reactions.c.user_id == user_id) \
        .where(schema.reactions.c.object_id == object_id) \
        .where(schema.reactions.c.reaction_id == reaction_id) \
        .order_by(schema.reactions.c.submitted_date.desc())

    if not removed:
        query = query.where(schema.reactions.c.is_removed == False)

    query, params = asyncpgsa.compile_query(query)

    return await conn.fetch(query, *params)


async def create(conn: Connection,
                 user_id: int,
                 object_id: int,
                 reaction_id: int) -> Record:
    """
    Create a new reaction.
    """
    # TODO: Check for exist reaction with given parameters

    query, params = asyncpgsa.compile_query(
        schema.reactions.insert().values(
            user_id=user_id,
            object_id=object_id,
            reaction_id=reaction_id
        ).returning(
            schema.reactions.c.user_id,
            schema.reactions.c.object_id,
            schema.reactions.c.reaction_id,
            schema.reactions.c.is_removed,
            schema.reactions.c.submitted_date,
        )
    )

    return await conn.fetchrow(query, *params)
