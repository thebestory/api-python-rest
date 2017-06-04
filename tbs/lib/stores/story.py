"""
The Bestory Project
"""

import typing
from datetime import datetime

import asyncpgsa
import pendulum
from asyncpg.connection import Connection
from asyncpg.exceptions import PostgresError
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

from tbs.lib import exceptions
from tbs.lib import schema
from tbs.lib import validators
from tbs.lib.stores import snowflake as snowflake_store
from tbs.lib.stores import topic as topic_store
from tbs.lib.stores import user as user_store


SNOWFLAKE_TYPE = "story"


def __list_prepare(topics: typing.List[int]=None,
                   inverse_topics: bool=False,
                   authors: typing.List[int]=None,
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
                   include_inactive_topics: bool=False,  # works only when inverse_topics is True
                   only_inactive_topics: bool=False,  # works only when inverse_topics is True
                   preload_author: bool=True,
                   preload_topic: bool=True):
    """List stories query builder."""
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
    include_inactive_topics |= only_inactive_topics

    __to_select = [schema.stories]
    __from_select = schema.stories

    if preload_author:
        __to_select.append(schema.users)
        __from_select = __from_select.join(
            schema.users,
            schema.users.c.id == schema.stories.c.author_id)
    if preload_topic:
        __to_select.append(schema.topics)
        __from_select = __from_select.outerjoin(
            schema.topics,
            schema.topics.c.id == schema.stories.c.topic_id)

    query = (select(__to_select)
             .select_from(__from_select)
             .limit(limit)
             .apply_labels())

    if topics is None or len(topics) == 0:
        inverse_topics = True
    elif inverse_topics:
        query = query.where(~schema.stories.c.topic_id.in_(topics))
    else:
        query = query.where(schema.stories.c.topic_id.in_(topics))

    if authors is None:
        inverse_authors = True
    elif inverse_authors:
        query = query.where(~schema.stories.c.author_id.in_(authors))
    else:
        query = query.where(schema.stories.c.author_id.in_(authors))

    include_inactive_topics &= inverse_topics
    only_inactive_topics &= inverse_topics

    if submitted_date_before:
        query = query.where(
            schema.stories.c.submitted_date < submitted_date_before)
    if submitted_date_after:
        query = query.where(
            schema.stories.c.submitted_date > submitted_date_after)

    if published_date_before:
        query = query.where(
            schema.stories.c.published_date < published_date_before)
    if published_date_after:
        query = query.where(
            schema.stories.c.published_date > published_date_after)

    if edited_date_before:
        query = query.where(
            schema.stories.c.edited_date < edited_date_before)
    if edited_date_after:
        query = query.where(
            schema.stories.c.edited_date > edited_date_after)

    if not include_unpublished:
        query = query.where(schema.stories.c.is_published == True)
    if not include_removed:
        query = query.where(schema.stories.c.is_removed == False)
    if not include_edited:
        query = query.where(schema.stories.c.edited_date == None)
    if not include_inactive_topics:
        query = query.where(schema.topics.c.is_active == True)

    if only_unpublished:
        query = query.where(schema.stories.c.is_published == False)
    if only_removed:
        query = query.where(schema.stories.c.is_removed == True)
    if only_edited:
        query = query.where(schema.stories.c.edited_date != None)
    if only_inactive_topics:
        query = query.where(schema.topics.c.is_active == False)

    return query


async def __list_execute(conn: Connection,
                         query,
                         preload_author: bool,
                         preload_topic: bool):
    """List stories query executor."""
    query, params = asyncpgsa.compile_query(query)

    try:
        rows = await conn.fetch(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    stories = [schema.stories.parse(row, prefix="stories_") for row in rows]

    if preload_author:
        for story, row in zip(stories, rows):
            story["author"] = schema.users.parse(row, prefix="users_")
    if preload_topic:
        for story, row in zip(stories, rows):
            if story["topic_id"] is not None:
                story["topic"] = schema.topics.parse(row, prefix="topics_")
            else:
                story["topic"] = None

    return stories


async def list_latest(conn: Connection,
                      topics: typing.List[int]=None,
                      inverse_topics: bool=False,
                      authors: typing.List[int]=None,
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
                      include_inactive_topics: bool=False,
                      only_inactive_topics: bool=False,
                      preload_author: bool=True,
                      preload_topic: bool=True) -> list:
    """List latest stories."""
    query = __list_prepare(
        topics=topics,
        inverse_topics=inverse_topics,
        authors=authors,
        inverse_authors=inverse_authors,
        submitted_date_before=submitted_date_before,
        submitted_date_after=submitted_date_after,
        published_date_before=published_date_before,
        published_date_after=published_date_after,
        edited_date_before=edited_date_before,
        edited_date_after=edited_date_after,
        limit=limit,
        include_unpublished=include_unpublished,
        only_unpublished=only_unpublished,
        include_removed=include_removed,
        only_removed=only_removed,
        include_edited=include_edited,
        only_edited=only_edited,
        include_inactive_topics=include_inactive_topics,
        only_inactive_topics=only_inactive_topics,
        preload_author=preload_author,
        preload_topic=preload_topic)

    query = query.order_by(schema.stories.c.published_date.desc())
    return await __list_execute(
        conn=conn,
        query=query,
        preload_author=preload_author,
        preload_topic=preload_topic)


async def list_top(conn: Connection,
                   topics: typing.List[int]=None,
                   inverse_topics: bool=False,
                   authors: typing.List[int]=None,
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
                   include_inactive_topics: bool=False,
                   only_inactive_topics: bool=False,
                   preload_author: bool=True,
                   preload_topic: bool=True) -> list:
    """List top stories."""
    query = __list_prepare(
        topics=topics,
        inverse_topics=inverse_topics,
        authors=authors,
        inverse_authors=inverse_authors,
        submitted_date_before=submitted_date_before,
        submitted_date_after=submitted_date_after,
        published_date_before=published_date_before,
        published_date_after=published_date_after,
        edited_date_before=edited_date_before,
        edited_date_after=edited_date_after,
        limit=limit,
        include_unpublished=include_unpublished,
        only_unpublished=only_unpublished,
        include_removed=include_removed,
        only_removed=only_removed,
        include_edited=include_edited,
        only_edited=only_edited,
        include_inactive_topics=include_inactive_topics,
        only_inactive_topics=only_inactive_topics,
        preload_author=preload_author,
        preload_topic=preload_topic)

    query = query.order_by(schema.stories.c.reactions_count.desc())
    query = query.order_by(schema.stories.c.published_date.desc())
    return await __list_execute(
        conn=conn,
        query=query,
        preload_author=preload_author,
        preload_topic=preload_topic)


async def list_random(conn: Connection,
                      topics: typing.List[int]=None,
                      inverse_topics: bool=False,
                      authors: typing.List[int]=None,
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
                      include_inactive_topics: bool=False,
                      only_inactive_topics: bool=False,
                      preload_author: bool=True,
                      preload_topic: bool=True) -> list:
    """List random stories."""
    query = __list_prepare(
        topics=topics,
        inverse_topics=inverse_topics,
        authors=authors,
        inverse_authors=inverse_authors,
        submitted_date_before=submitted_date_before,
        submitted_date_after=submitted_date_after,
        published_date_before=published_date_before,
        published_date_after=published_date_after,
        edited_date_before=edited_date_before,
        edited_date_after=edited_date_after,
        limit=limit,
        include_unpublished=include_unpublished,
        only_unpublished=only_unpublished,
        include_removed=include_removed,
        only_removed=only_removed,
        include_edited=include_edited,
        only_edited=only_edited,
        include_inactive_topics=include_inactive_topics,
        only_inactive_topics=only_inactive_topics,
        preload_author=preload_author,
        preload_topic=preload_topic)

    query = query.order_by(func.random())
    return await __list_execute(
        conn=conn,
        query=query,
        preload_author=preload_author,
        preload_topic=preload_topic)


list_hot = list_top


async def get(conn: Connection,
              id: int,
              preload_author=True,
              preload_topic=True) -> dict:
    """Get a single story."""
    __to_select = [schema.stories]
    __from_select = schema.stories

    if preload_author:
        __to_select.append(schema.users)
        __from_select = __from_select.join(
            schema.users,
            schema.users.c.id == schema.stories.c.author_id)
    if preload_topic:
        __to_select.append(schema.topics)
        __from_select = __from_select.outerjoin(
            schema.topics,
            schema.topics.c.id == schema.stories.c.topic_id)

    query = (select(__to_select)
             .select_from(__from_select)
             .where(schema.stories.c.id == id)
             .apply_labels())

    query, params = asyncpgsa.compile_query(query)

    try:
        row = await conn.fetchrow(query, *params)
    except PostgresError:
        raise exceptions.NotFetchedError

    if not row:
        raise exceptions.NotFoundError

    story = schema.stories.parse(row, prefix="stories_")

    if preload_author:
        story["author"] = schema.users.parse(row, prefix="users_")
    if preload_topic:
        if story["topic_id"] is not None:
            story["topic"] = schema.topics.parse(row, prefix="topics_")
        else:
            story["topic"] = None

    return story


async def create(conn: Connection,
                 author_id: int,
                 content: str,
                 topic_id: typing.Optional[int]=None,
                 is_published: bool=False,
                 is_removed: bool=False,
                 published_date: typing.Optional[datetime]=None) -> dict:
    """Create a new story."""
    validators.story.validate_author_id(author_id)
    validators.story.validate_topic_id(topic_id)
    validators.story.validate_content(content)
    validators.story.validate_is_published(is_published)
    validators.story.validate_is_removed(is_removed)
    validators.story.validate_published_date(published_date)

    if is_published and published_date is None:
        published_date = datetime.utcnow().replace(tzinfo=pendulum.UTC)

    async with conn.transaction():
        snowflake = await snowflake_store.create(conn=conn,
                                                 type=SNOWFLAKE_TYPE)

        query, params = asyncpgsa.compile_query(schema.stories.insert().values(
            id=snowflake["id"],
            author_id=author_id,
            topic_id=topic_id,
            content=content,
            is_published=is_published,
            is_removed=is_removed,
            published_date=published_date))

        try:
            await conn.execute(query, *params)
            await user_store.increment_stories_counter(conn=conn, id=author_id)

            if topic_id is not None:
                await topic_store.increment_stories_counter(conn=conn,
                                                            id=topic_id)

            return await get(conn=conn, id=snowflake["id"])
        except (PostgresError, exceptions.DatabaseError):
            raise exceptions.NotCreatedError


async def update(conn: Connection, id: int, **kwargs):
    """Update the story."""
    query = schema.stories.update().where(schema.stories.c.id == id)

    if "topic_id" in kwargs:
        validators.story.validate_topic_id(kwargs["topic_id"])
        query = query.values(topic_id=kwargs["topic_id"])

    if "content" in kwargs:
        validators.story.validate_content(kwargs["content"])
        query = query.values(
            content=kwargs["content"],
            edited_date=datetime.utcnow().replace(tzinfo=pendulum.UTC))

    if "is_published" in kwargs:
        validators.story.validate_is_published(kwargs["is_published"])
        query = query.values(is_published=kwargs["is_published"])

        if kwargs["is_published"]:
            query = query.values(
                published_date=datetime.utcnow().replace(tzinfo=pendulum.UTC))

    if "is_removed" in kwargs:
        validators.story.validate_is_removed(kwargs["is_removed"])
        query = query.values(is_removed=kwargs["is_removed"])

    if "published_date" in kwargs:
        validators.story.validate_published_date(kwargs["published_date"])
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


async def __update_counter(conn: Connection, id: int, query):
    """Change counter of the story."""
    q, p = asyncpgsa.compile_query(query.where(schema.stories.c.id == id))

    try:
        await conn.execute(q, *p)
    except PostgresError:
        raise exceptions.NotUpdatedError

    return True

async def increment_comments_counter(conn: Connection, id: int):
    """Increment comments counter of the story."""
    return __update_counter(conn, id, schema.stories.update().values(
        comments_count=schema.topics.c.comments_count + 1))

async def increment_reactions_counter(conn: Connection, id: int):
    """Increment reactions counter of the story."""
    return __update_counter(conn, id, schema.stories.update().values(
        reactions_count=schema.topics.c.reactions_count + 1))

async def decrement_comments_counter(conn: Connection, id: int):
    """Decrement comments counter of the story."""
    return __update_counter(conn, id, schema.stories.update().values(
        comments_count=schema.topics.c.comments_count - 1))

async def decrement_reactions_counter(conn: Connection, id: int):
    """Decrement reactions counter of the story."""
    return __update_counter(conn, id, schema.stories.update().values(
        reactions_count=schema.topics.c.reactions_count - 1))
