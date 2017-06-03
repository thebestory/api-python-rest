"""
The Bestory Project
"""

from datetime import datetime
from typing import Optional, List

import asyncpgsa
import pendulum
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError
from sqlalchemy.sql.expression import func

from tbs.lib import (
    data,
    exceptions,
    schema
)
from tbs.lib.stores import snowflake as snowflake_store
from tbs.lib.stores import user as user_store
from tbs.lib.stores import topic as topic_store
from tbs.lib.validators import story as validators


SNOWFLAKE_TYPE = "story"


def __list(topics: List[int]=None,
           inverse_topics: bool=False,
           authors: List[int]=None,
           inverse_authors: bool=False,
           submitted_date_before: datetime=None,
           submitted_date_after: datetime=None,
           published_date_before: datetime=None,
           published_date_after: datetime=None,
           edited_date_before: datetime=None,
           edited_date_after: datetime=None,
           limit: int=25,
           include_unpublished: bool=False,
           only_unpublished: bool=False,
           include_removed: bool=False,
           only_removed: bool=False,
           include_edited: bool=True,
           only_edited: bool=False,
           preload_user: bool=True,
           preload_topic: bool=True):
    """
    List stories.
    """
    if submitted_date_before is not None and submitted_date_after is not None:
        raise ValueError("Only one of `submitted_date_before` and "
                         "`submitted_date_after` can be specified")

    if published_date_before is not None and published_date_after is not None:
        raise ValueError("Only one of `published_date_before` and "
                         "`published_date_after` can be specified")

    if edited_date_before is not None and edited_date_after is not None:
        raise ValueError("Only one of `edited_date_before` and "
                         "`edited_date_after` can be specified")

    include_unpublished |= only_unpublished
    include_removed |= only_removed
    include_edited |= only_edited

    query = schema.stories.select().limit(limit)

    if topics is None:
        inverse_topics = True  # only for understanding
    elif inverse_topics:
        query = query.where(~schema.stories.c.topic_id.in_(topics))
    else:
        query = query.where(schema.stories.c.topic_id.in_(topics))

    if authors is None:
        inverse_authors = True  # only for understanding
    elif inverse_authors:
        query = query.where(~schema.stories.c.author_id.in_(authors))
    else:
        query = query.where(schema.stories.c.author_id.in_(authors))

    if submitted_date_before:
        query = query.where(
            schema.stories.c.submitted_date < submitted_date_before
        )
    if submitted_date_after:
        query = query.where(
            schema.stories.c.submitted_date > submitted_date_after
        )

    if published_date_before:
        query = query.where(
            schema.stories.c.published_date < published_date_before
        )
    if published_date_after:
        query = query.where(
            schema.stories.c.published_date > published_date_after
        )

    if edited_date_before:
        query = query.where(
            schema.stories.c.edited_date < edited_date_before
        )
    if edited_date_after:
        query = query.where(
            schema.stories.c.edited_date > edited_date_after
        )

    if not include_unpublished:
        query = query.where(schema.stories.c.is_published == True)
    if not include_removed:
        query = query.where(schema.stories.c.is_removed == False)
    if not include_edited:
        query = query.where(schema.stories.c.edited_date == None)

    if only_unpublished:
        query = query.where(schema.stories.c.is_published == False)
    if only_removed:
        query = query.where(schema.stories.c.is_removed == True)
    if only_edited:
        query = query.where(schema.stories.c.edited_date != None)

    return query


async def list_latest(conn: Connection,
                      topics: List[int]=None,
                      inverse_topics: bool=False,
                      authors: List[int]=None,
                      inverse_authors: bool=False,
                      submitted_date_before: datetime=None,
                      submitted_date_after: datetime=None,
                      published_date_before: datetime=None,
                      published_date_after: datetime=None,
                      edited_date_before: datetime=None,
                      edited_date_after: datetime=None,
                      limit: int=25,
                      include_unpublished: bool=False,
                      only_unpublished: bool=False,
                      include_removed: bool=False,
                      only_removed: bool=False,
                      include_edited: bool=True,
                      only_edited: bool=False,
                      preload_user: bool=True,
                      preload_topic: bool=True) -> list:
    query = __list(topics,
                   inverse_topics,
                   authors,
                   inverse_authors,
                   submitted_date_before,
                   submitted_date_after,
                   published_date_before,
                   published_date_after,
                   edited_date_before,
                   edited_date_after,
                   limit,
                   include_unpublished,
                   only_unpublished,
                   include_removed,
                   only_removed,
                   include_edited,
                   only_edited,
                   preload_user,
                   preload_topic)

    query = query.order_by(schema.stories.c.published_date.desc())

    query, params = asyncpgsa.compile_query(query)

    try:
        stories = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    return data.parse_stories(stories)


async def list_top(conn: Connection,
                   topics: List[int]=None,
                   inverse_topics: bool=False,
                   authors: List[int]=None,
                   inverse_authors: bool=False,
                   submitted_date_before: datetime=None,
                   submitted_date_after: datetime=None,
                   published_date_before: datetime=None,
                   published_date_after: datetime=None,
                   edited_date_before: datetime=None,
                   edited_date_after: datetime=None,
                   limit: int=25,
                   include_unpublished: bool=False,
                   only_unpublished: bool=False,
                   include_removed: bool=False,
                   only_removed: bool=False,
                   include_edited: bool=True,
                   only_edited: bool=False,
                   preload_user: bool=True,
                   preload_topic: bool=True) -> list:
    query = __list(topics,
                   inverse_topics,
                   authors,
                   inverse_authors,
                   submitted_date_before,
                   submitted_date_after,
                   published_date_before,
                   published_date_after,
                   edited_date_before,
                   edited_date_after,
                   limit,
                   include_unpublished,
                   only_unpublished,
                   include_removed,
                   only_removed,
                   include_edited,
                   only_edited,
                   preload_user,
                   preload_topic)

    query = query.order_by(schema.stories.c.reactions_count.desc())
    query = query.order_by(schema.stories.c.published_date.desc())

    query, params = asyncpgsa.compile_query(query)

    try:
        stories = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    return data.parse_stories(stories)


async def list_random(conn: Connection,
                      topics: List[int]=None,
                      inverse_topics: bool=False,
                      authors: List[int]=None,
                      inverse_authors: bool=False,
                      submitted_date_before: datetime=None,
                      submitted_date_after: datetime=None,
                      published_date_before: datetime=None,
                      published_date_after: datetime=None,
                      edited_date_before: datetime=None,
                      edited_date_after: datetime=None,
                      limit: int=25,
                      include_unpublished: bool=False,
                      only_unpublished: bool=False,
                      include_removed: bool=False,
                      only_removed: bool=False,
                      include_edited: bool=True,
                      only_edited: bool=False,
                      preload_user: bool=True,
                      preload_topic: bool=True) -> list:
    query = __list(topics,
                   inverse_topics,
                   authors,
                   inverse_authors,
                   submitted_date_before,
                   submitted_date_after,
                   published_date_before,
                   published_date_after,
                   edited_date_before,
                   edited_date_after,
                   limit,
                   include_unpublished,
                   only_unpublished,
                   include_removed,
                   only_removed,
                   include_edited,
                   only_edited,
                   preload_user,
                   preload_topic)

    query = query.order_by(func.random())

    query, params = asyncpgsa.compile_query(query)

    try:
        stories = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    return data.parse_stories(stories)


list_hot = list_top


async def get(conn: Connection, id: int) -> dict:
    """
    Get a single story.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.select().where(schema.stories.c.id == id)
    )

    try:
        story = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not story:
        raise exceptions.NotFoundError

    return data.parse_story(story)


async def create(conn: Connection,
                 author_id: int,
                 content: str,
                 topic_id: Optional[int]=None,
                 is_published: bool=False,
                 is_removed: bool=False,
                 published_date: Optional[datetime]=None) -> dict:
    """
    Create a new story.
    """
    validators.validate_author_id(author_id)
    validators.validate_topic_id(topic_id)
    validators.validate_content(content)
    validators.validate_is_published(is_published)
    validators.validate_is_removed(is_removed)
    validators.validate_published_date(published_date)

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

        try:
            await conn.execute(query, *params)
            await user_store.increment_stories_counter(conn=conn, id=author_id)

            if topic_id is not None:
                await topic_store.increment_stories_counter(
                    conn=conn,
                    id=topic_id
                )

            return await get(conn=conn, id=snowflake["id"])
        except (PostgresError, exceptions.DatabaseError):
            raise exceptions.NotCreatedError


async def update(conn: Connection, id: int, **kwargs):
    """
    Update the story.
    """
    query = schema.stories.update().where(schema.stories.c.id == id)

    if "topic_id" in kwargs:
        validators.validate_topic_id(kwargs["topic_id"])
        query = query.values(topic_id=kwargs["topic_id"])

    if "content" in kwargs:
        validators.validate_content(kwargs["content"])
        query = query.values(
            content=kwargs["content"],
            edited_date=datetime.utcnow().replace(tzinfo=pendulum.UTC)
        )

    if "is_published" in kwargs:
        validators.validate_is_published(kwargs["is_published"])
        query = query.values(is_published=kwargs["is_published"])

        if kwargs["is_published"]:
            query = query.values(
                published_date=datetime.utcnow().replace(tzinfo=pendulum.UTC)
            )

    if "is_removed" in kwargs:
        validators.validate_is_removed(kwargs["is_removed"])
        query = query.values(is_removed=kwargs["is_removed"])

    if "published_date" in kwargs:
        validators.validate_published_date(kwargs["published_date"])
        query = query.values(published_date=kwargs["published_date"])

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
    Increment story's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            comments_count=schema.stories.c.comments_count + 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def increment_reactions_counter(conn: Connection, id: int):
    """
    Increment story's reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            reactions_count=schema.stories.c.reactions_count + 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def decrement_comments_counter(conn: Connection, id: int):
    """
    Decrement story's comments counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            comments_count=schema.stories.c.comments_count - 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True


async def decrement_reactions_counter(conn: Connection, id: int):
    """
    Decrement story's reactions counter.
    """
    query, params = asyncpgsa.compile_query(
        schema.stories.update().where(schema.stories.c.id == id).values(
            reactions_count=schema.stories.c.reactions_count - 1
        )
    )

    try:
        await conn.execute(query, *params)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True
