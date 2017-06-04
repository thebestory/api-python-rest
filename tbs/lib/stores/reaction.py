"""
The Bestory Project
"""

import typing

import asyncpgsa
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError
from sqlalchemy.sql import select

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib import validators


async def list(conn: Connection,
               users: typing.List[int]=None,
               inverse_users: bool=False,
               objects: typing.List[int]=None,
               inverse_objects: bool=False,
               reactions: typing.List[int]=None,
               inverse_reactions: bool=False,
               limit: typing.Optional[int]=None,
               include_removed: bool=False,
               only_removed: bool=False,
               preload_user: bool=True):
    """List reactions."""
    include_removed |= only_removed

    __to_select = [schema.reactions]
    __from_select = schema.reactions

    if preload_user:
        __to_select.append(schema.users)
        __from_select = __from_select.join(
            schema.users, schema.users.c.id == schema.stories.c.author_id)

    query = (select(__to_select)
             .select_from(__from_select)
             .apply_labels())

    if limit is not None:
        query = query.limit(limit)

    if users is None or len(users) == 0:
        inverse_users = True
    elif inverse_users:
        query = query.where(~schema.reactions.c.user_id.in_(users))
    else:
        query = query.where(schema.reactions.c.user_id.in_(users))

    if objects is None or len(objects) == 0:
        inverse_objects = True
    elif inverse_objects:
        query = query.where(~schema.reactions.c.object_id.in_(objects))
    else:
        query = query.where(schema.reactions.c.object_id.in_(objects))

    if reactions is None or len(reactions) == 0:
        inverse_reactions = True
    elif inverse_reactions:
        query = query.where(~schema.reactions.c.reaction_id.in_(reactions))
    else:
        query = query.where(schema.reactions.c.reaction_id.in_(reactions))

    if not include_removed:
        query = query.where(schema.reactions.c.is_removed == False)
    if only_removed:
        query = query.where(schema.reactions.c.is_removed == True)

    query, params = asyncpgsa.compile_query(query)

    try:
        rows = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    reactions = [schema.reactions.parse(row, prefix="reactions_")
                 for row in rows]

    if preload_user:
        for reaction, row in zip(reactions, rows):
            reaction["author"] = schema.users.parse(row, prefix="users_")

    return reactions


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
