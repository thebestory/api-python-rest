"""
The Bestory Project
"""

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib import validators


async def __list_executor(conn: Connection,
                          query,
                          include_removed: bool,
                          only_removed: bool) -> list:
    """List reactions query executor."""
    include_removed |= only_removed

    if not include_removed:
        query = query.where(schema.reactions.c.is_removed == False)
    if only_removed:
        query = query.where(schema.reactions.c.is_removed == True)

    query, params = asyncpgsa.compile_query(query)

    try:
        rows = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    return [schema.reactions.parse(row) for row in rows]

async def list_by_user(conn: Connection,
                       user_id: int,
                       include_removed: bool=False,
                       only_removed: bool=False) -> list:
    """List reactions by user."""
    return await __list_executor(
        conn=conn,
        query=(schema.reactions.select()
               .where(schema.reactions.c.user_id == user_id)
               .order_by(schema.reactions.c.submitted_date.desc())),
        include_removed=include_removed,
        only_removed=only_removed)

async def list_by_object(conn: Connection,
                         object_id: int,
                         include_removed: bool=False,
                         only_removed: bool=False) -> list:
    """List reactions by object."""
    return await __list_executor(
        conn=conn,
        query=(schema.reactions.select()
               .where(schema.reactions.c.object_id == object_id)
               .order_by(schema.reactions.c.submitted_date.desc())),
        include_removed=include_removed,
        only_removed=only_removed)

async def list_by_user_and_object(conn: Connection,
                                  user_id: int,
                                  object_id: int,
                                  include_removed: bool=False,
                                  only_removed: bool=False) -> list:
    """List reactions by user and object."""
    return await __list_executor(
        conn=conn,
        query=(schema.reactions.select()
               .where(schema.reactions.c.user_id == user_id)
               .where(schema.reactions.c.object_id == object_id)
               .order_by(schema.reactions.c.submitted_date.desc())),
        include_removed=include_removed,
        only_removed=only_removed)

async def list_by_user_and_reaction(conn: Connection,
                                    user_id: int,
                                    reaction_id: int,
                                    include_removed: bool=False,
                                    only_removed: bool=False) -> list:
    """List reactions by user and reaction."""
    return await __list_executor(
        conn=conn,
        query=(schema.reactions.select()
               .where(schema.reactions.c.user_id == user_id)
               .where(schema.reactions.c.reaction_id == reaction_id)
               .order_by(schema.reactions.c.submitted_date.desc())),
        include_removed=include_removed,
        only_removed=only_removed)

async def list_by_object_and_reaction(conn: Connection,
                                      object_id: int,
                                      reaction_id: int,
                                      include_removed: bool=False,
                                      only_removed: bool=False) -> list:
    """List reactions by object and reaction."""
    return await __list_executor(
        conn=conn,
        query=(schema.reactions.select()
               .where(schema.reactions.c.object_id == object_id)
               .where(schema.reactions.c.reaction_id == reaction_id)
               .order_by(schema.reactions.c.submitted_date.desc())),
        include_removed=include_removed,
        only_removed=only_removed)

async def list_by_user_and_object_and_reaction(conn: Connection,
                                               user_id: int,
                                               object_id: int,
                                               reaction_id: int,
                                               include_removed: bool=False,
                                               only_removed: bool=False
                                               ) -> list:
    """List reactions by user, object and reaction."""
    return await __list_executor(
        conn=conn,
        query=(schema.reactions.select()
               .where(schema.reactions.c.user_id == user_id)
               .where(schema.reactions.c.object_id == object_id)
               .where(schema.reactions.c.reaction_id == reaction_id)
               .order_by(schema.reactions.c.submitted_date.desc())),
        include_removed=include_removed,
        only_removed=only_removed)


async def create(conn: Connection,
                 user_id: int,
                 object_id: int,
                 reaction_id: int) -> dict:
    """Create a new reaction."""
    validators.reaction.validate_user_id(user_id)
    validators.reaction.validate_object_id(object_id)
    validators.reaction.validate_reaction_id(reaction_id)

    query, params = asyncpgsa.compile_query(schema.reactions.insert().values(
        user_id=user_id,
        object_id=object_id,
        reaction_id=reaction_id
    ).returning(
        schema.reactions.c.user_id,
        schema.reactions.c.object_id,
        schema.reactions.c.reaction_id,
        schema.reactions.c.is_removed,
        schema.reactions.c.submitted_date))

    try:
        return schema.reactions.parse(await conn.fetchrow(query, *params))
    except PostgresError:
        raise exceptions.NotCreatedError
