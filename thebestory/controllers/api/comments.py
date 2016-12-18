"""
The Bestory Project
"""

import json
from datetime import datetime

import pendulum
from aiohttp import web
from sqlalchemy.sql import insert, select, update

from thebestory.lib import identifier
from thebestory.lib.api.response import *
from thebestory.models import (
    comment_likes,
    comments,
    stories,
    topics,
    users,
)

# User ID
ANONYMOUS_USER_ID = 5

# User ID
THEBESTORY_USER_ID = 2


class CollectionController(web.View):
    async def post(self):
        """
        Sumbit a new comment. Returns a submitted comment.
        """
        # Parse the content and IDs and check, if only one of IDs is present
        try:
            body = await self.request.json()

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
        if len(content) <= 0:  # FIXME: Specify this value as a global setting
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

        # Get story, where comment is submitting
        async with self.request.db.acquire() as conn:
            parent = None

            if parent_id:
                parent = await conn.fetchrow(
                    select([comments]).where(comments.c.id == parent_id))

                if parent is None or parent.is_removed:
                    return web.Response(
                        status=404,
                        content_type="application/json",
                        text=json.dumps(error(2004)))

                story_id = parent.story_id

            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == story_id))

        # Check, if story is present and valid for comment submitting
        if story is None or story.is_removed or not story.is_approved:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2003)))

        # Commit comment to DB, incrementing counters for story and user
        async with self.request.db.transaction() as conn:

            # FIXME: When asyncpgsa will replace nulls with default values
            comment_id = await conn.fetchval(insert(comments).values(
                parent_id=parent.id if parent is not None else None,
                author_id=ANONYMOUS_USER_ID,
                story_id=story.id,
                content=content,
                likes_count=0,
                comments_count=0,
                is_removed=False,
                submitted_date=pendulum.utcnow()
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
            async with self.request.db.acquire() as conn:
                comment = await conn.fetchrow(
                    select(
                        [comments, users.c.username.label("author_username")])
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
            # FIXME: MODEL: COMMENT
            data = {
                "id": identifier.to36(comment.id),
                "parent": None if comment.parent_id is None else {
                    "id": identifier.to36(comment.parent_id),
                },
                "author": {
                    "id": comment.author_id,
                    "username": comment.author_username
                },
                "content": comment.content,
                "story": {
                    "id": identifier.to36(comment.story_id)
                } if story is None else {
                    "id": identifier.to36(story.id),
                    "content": story.content,
                    "topic": None if topic is None else {
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
                "edited_date": None  # obviously / trivial case
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


class CommentController(web.View):
    async def get(self):
        """
        Returns the comment.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2004)))

        async with self.request.db.acquire() as conn:
            comment = await conn.fetchrow(
                select([comments, users.c.username.label("author_username")])
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

        # TODO: extend with parent comment
        # FIXME: MODEL: COMMENT
        data = {
            "id": identifier.to36(comment.id),
            "parent": None if comment.parent_id is None else {
                "id": identifier.to36(comment.parent_id),
            },
            "author": {
                "id": comment.author_id,
                "username": comment.author_username
            },
            "content": comment.content,
            "story": {
                "id": identifier.to36(comment.story_id)
            } if story is None else {
                "id": identifier.to36(story.id),
                "content": story.content,
                "topic": None if topic is None else {
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

    async def patch(self):
        """
        Edit the comment.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2004)))

        try:
            body = await self.request.json()
            content = body.get("content")
        except Exception:  # FIXME: Specify the errors can raised here
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3003)))

        # Content checks
        if len(content) <= 0:  # FIXME: Specify this value as a global setting
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5005)))
        elif len(content) > comments.c.content.type.length:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5007)))

        async with self.request.db.acquire() as conn:
            comment = await conn.fetchrow(
                select([comments, users.c.username.label("author_username")])
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

        if content is not None:
            query = update(comments).where(comments.c.id == id)

            if content is not None:
                query = query.values(
                    content=content,
                    edited_date=pendulum.utcnow()
                )

            async with self.request.db.acquire() as conn:
                await conn.execute(query)

                comment = await conn.fetchrow(
                    select(
                        [comments, users.c.username.label("author_username")])
                        .where(users.c.id == comments.c.author_id)
                        .where(comments.c.id == id))

        # FIXME: MODEL: COMMENT
        data = {
            "id": identifier.to36(comment.id),
            "parent": None if comment.parent_id is None else {
                "id": identifier.to36(comment.parent_id),
            },
            "author": {
                "id": comment.author_id,
                "username": comment.author_username
            },
            "content": comment.content,
            "story": {
                "id": identifier.to36(comment.story_id)
            } if story is None else {
                "id": identifier.to36(story.id),
                "content": story.content,
                "topic": None if topic is None else {
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
            text=json.dumps(data)
        )

    async def delete(self):
        """
        Delete the comment.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2004)))

        async with self.request.db.acquire() as conn:
            comment = await conn.fetchrow(
                select([comments, users.c.username.label("author_username")])
                    .where(users.c.id == comments.c.author_id)
                    .where(comments.c.id == id))

            if comment is None or comment.is_removed:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2004)))

        query = update(comments)\
            .where(comments.c.id == id)\
            .values(is_removed=True)

        async with self.request.db.acquire() as conn:
            await conn.execute(query)
            comment = await conn.fetchrow(
                select([comments]).where(comments.c.id == id))

        if comment.is_removed:
            return web.Response(
                status=204,
                content_type="application/json"
            )
        else:
            return web.Response(
                status=500,
                content_type="application/json",
                text=json.dumps(error(1005))
            )


class LikeController(web.View):
    async def post(self):
        """
        Likes the comment.
        """
        return await self._like(self.request, True)

    async def delete(self):
        """
        Unlikes the comment.
        """
        return await self._like(self.request, False)

    @staticmethod
    async def _like(request, state: bool):
        try:
            id = identifier.from36(request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2004)))

        diff = 1 if state else -1

        async with request.db.acquire() as conn:
            comment = await conn.fetchrow(
                select([comments]).where(comments.c.id == id))

            if comment is None or comment.is_removed:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2004)))

            like = await conn.fetchrow(
                select([comment_likes])
                    .where(comment_likes.c.user_id == ANONYMOUS_USER_ID)
                    .where(comment_likes.c.comment_id == comment.id))

        if like is None or like.state != state:
            async with request.db.transaction() as conn:
                await conn.execute(insert(comment_likes).values(
                    user_id=ANONYMOUS_USER_ID,
                    comment_id=comment.id,
                    state=state,
                    timestamp=pendulum.utcnow()
                ))

                await conn.execute(
                    update(comments)
                        .where(comments.c.id == comment.id)
                        .values(likes_count=comments.c.likes_count + diff))

                await conn.execute(
                    update(users)
                        .where(users.c.id == ANONYMOUS_USER_ID)
                        .values(
                        comment_likes_count=users.c.comment_likes_count + diff))

            async with request.db.acquire() as conn:
                like = await conn.fetchrow(
                    select([comment_likes])
                        .where(comment_likes.c.user_id == ANONYMOUS_USER_ID)
                        .where(comment_likes.c.comment_id == comment.id)
                        .order_by(comment_likes.c.timestamp.desc()))

            if like is None:
                return web.Response(
                    status=500,
                    content_type="application/json",
                    text=json.dumps(error(1006)))

        return web.Response(
            status=201,
            content_type="application/json",

            # FIXME: MODEL: COMMENT LIKE
            text=json.dumps(ok({
                "user": {
                    "id": like.user_id
                },
                "comment": {
                    "id": identifier.to36(like.comment_id)
                },
                "state": like.state,
                "timestamp": like.timestamp.isoformat()
            })))
