"""
The Bestory Project
"""

import json
from datetime import datetime

import pytz
from aiohttp import web
from sqlalchemy.sql import insert, select, update

from thebestory.app.lib import identifier
from thebestory.app.lib.api.response import *
from thebestory.app.models import comments, stories, topics, users

# User ID
ANONYMOUS_USER_ID = 5

# User ID
THEBESTORY_USER_ID = 2


class CommentsController:
    async def details(self, request):
        """
        Returns the comment info.
        """
        try:
            id = identifier.from36(request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2004)))

        async with request.db.acquire() as conn:
            comment = await conn.fetchrow(
                select([comments, users.c.username])
                    .where(users.c.id == comments.c.author_id)
                    .where(comments.c.id == id))

            if comment is None or comment.is_removed:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2004)))

            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == comment.story_id))

            if story is None or story.is_removed or not story.is_approved:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            topic = await conn.fetchrow(
                select([topics]).where(topics.c.id == story.topic_id))

        data = {
            "id": identifier.to36(comment.id),
            "content": comment.content,
            "story": {"id": comment.story_id} if story is None else {
                "id": identifier.to36(story.id),
                "content": story.content,
                "topic": {"id": story.topic_id} if topic is None else {
                    "id": topic.id,
                    "slug": topic.slug,
                    "title": topic.title,
                    "description": topic.description,
                    "icon": topic.icon,
                    "stories_count": topic.stories_count
                },
                "likes_count": story.likes_count,
                "comments_count": story.comments_count,
                # "edited_date": story.edited_date.isoformat(),
                "published_date": story.published_date.isoformat()
            },
            "likes_count": comment.likes_count,
            "comments_count": comment.comments_count,
            "submitted_date": comment.submitted_date.isoformat(),
            "edited_date": comment.edited_date.isoformat() if comment.edited_date else None
        }

        if story is None:
            data = warning(2003, data)
        elif topic is None:
            data = warning(2002, data)
        else:
            data = ok(data)

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(data))

    async def submit(self, request):
        """
        Sumbits a new comment.
        """
        # Parses the content and IDs and checks, if only one of IDs is present
        try:
            body = await request.json()

            story_id = body.get("story")
            parent_id = body.get("parent")

            content = body["content"]

            if not story_id and not parent_id or story_id and parent_id:
                raise ValueError("No one or both IDs is provided")
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3003)))

        # Check if given story ID is correct
        try:
            if story_id is not None:
                story_id = identifier.from36(story_id)
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        # Check if given parent comment ID is correct
        try:
            if parent_id is not None:
                parent_id = identifier.from36(parent_id)
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2004)))

        # Content checks
        if len(content) <= 0:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5005)))
        elif len(content) > comments.c.content.type.length:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5007)))

        # TODO: Block some ascii graphics, and other unwanted symbols...

        # Getting story, where comment is submitting
        async with request.db.acquire() as conn:
            parent = None

            if parent_id:
                parent = await conn.fetchrow(
                    select([comments]).where(comments.c.id == parent_id))

                # XXX: Is user can comment a other's removed comment?
                if parent is None or parent.is_removed:
                    return web.Response(
                        status=404,
                        content_type="application/json",
                        text=json.dumps(error(2004)))

                story_id = parent.story_id

            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == story_id))

        # Checks, if story is present and valid for comment submitting
        if story is None or story.is_removed or not story.is_approved:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2003)))

        # Committing comment to DB, incrementing counters for story and user
        async with request.db.transaction() as conn:
            # TODO: Rewrite, when asyncpgsa replaces nulls with default values

            comment_id = await conn.fetchval(insert(comments).values(
                parent_id=parent.id if parent is not None else None,
                author_id=ANONYMOUS_USER_ID,
                story_id=story.id,
                content=content,
                likes_count=0,
                comments_count=0,
                is_removed=False,
                submitted_date=datetime.utcnow().replace(tzinfo=pytz.utc)
            ))

            await conn.execute(
                update(stories)
                    .where(stories.c.id == story.id)
                    .values(comments_count=stories.c.comments_count + 1))

            await conn.execute(
                update(users)
                    .where(users.c.id == ANONYMOUS_USER_ID)
                    .values(comments_count=users.c.comments_count + 1))

        # Is comment committed actually?
        if comment_id is not None:
            async with request.db.acquire() as conn:
                comment = await conn.fetchrow(
                    select([comments, users.c.username])
                        .where(users.c.id == comments.c.author_id)
                        .where(comments.c.id == comment_id))

                topic = await conn.fetchrow(
                    select([topics]).where(topics.c.id == story.topic_id))

            if comment is None:
                return web.Response(
                    status=500,
                    content_type="application/json",
                    text=json.dumps(error(1005)))

            # TODO: extend with parent comment
            data = {
                "id": identifier.to36(comment.id),
                "parent_id": comment.parent_id,
                "content": comment.content,
                "story": {"id": comment.story_id} if story is None else {
                    "id": identifier.to36(story.id),
                    "content": story.content,
                    "topic": {"id": story.topic_id} if topic is None else {
                        "id": topic.id,
                        "slug": topic.slug,
                        "title": topic.title,
                        "description": topic.description,
                        "icon": topic.icon,
                        "stories_count": topic.stories_count
                    },
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count + 1,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                },
                "likes_count": comment.likes_count,
                "comments_count": comment.comments_count,
                "submitted_date": comment.submitted_date.isoformat(),
                "edited_date": comment.edited_date.isoformat() if comment.edited_date else None
            }

            if story is None:
                data = warning(2003, data)
            elif topic is None:
                data = warning(2002, data)
            else:
                data = ok(data)

            return web.Response(
                status=201,
                content_type="application/json",
                text=json.dumps(data))
        else:
            return web.Response(
                status=500,
                content_type="application/json",
                text=json.dumps(error(1005)))
