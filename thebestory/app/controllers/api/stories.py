"""
The Bestory Project
"""

import json
from collections import OrderedDict
from datetime import datetime

import pytz
from aiohttp import web
from sqlalchemy.sql import insert, select, update

from thebestory.app.lib import identifier
from thebestory.app.lib.api.response import *
from thebestory.app.models import comments, stories, topics, users, story_likes

# User ID
ANONYMOUS_USER_ID = 5

# User ID
THEBESTORY_USER_ID = 2


class CollectionController(web.View):
    async def post(self):  # TODO: Auth required
        """
        Submit a new story. Returns a submitted story.
        """
        # Parse the content and ID of topic
        try:
            body = await self.request.json()
            content = body["content"]
        except Exception:  # FIXME: Specify the errors can raised here
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3002)))
        try:
            slug = body["topic"]
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        # Content checks
        if len(content) <= 5:  # FIXME: Specify this value as a global setting
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5004)))
        elif len(content) > stories.c.content.type.length:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5006)))

        # TODO: Block some ascii graphics, and other unwanted symbols...

        # Get topic, where story is submitting
        async with self.request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.slug == slug))

        # Check, if topic is present and valid for submitting
        if topic is None or not topic.is_public:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        # Commit story to DB, incrementing counters for topic and user
        async with self.request.db.transaction() as conn:

            # FIXME: When asyncpgsa will replace nulls with default values
            story_id = await conn.fetchval(insert(stories).values(
                author_id=ANONYMOUS_USER_ID,
                topic_id=topic.id,
                content=content,
                likes_count=0,
                comments_count=0,
                is_approved=False,
                is_removed=False,
                submitted_date=datetime.utcnow().replace(tzinfo=pytz.utc)
            ))

            await conn.execute(
                update(topics)
                    .where(topics.c.id == topic.id)
                    .values(stories_count=topics.c.stories_count + 1))

            await conn.execute(
                update(users)
                    .where(users.c.id == ANONYMOUS_USER_ID)
                    .values(stories_count=users.c.stories_count + 1))

        # Is story committed actually?
        if story_id is not None:
            async with self.request.db.acquire() as conn:
                story = await conn.fetchrow(
                    select([stories]).where(stories.c.id == story_id))

            if story is None:
                return web.Response(
                    status=500,
                    content_type="application/json",
                    text=json.dumps(error(1004)))

            # FIXME: MODEL: STORY
            data = {
                "id": identifier.to36(story.id),
                "topic": {
                    "slug": topic.slug,
                    "title": topic.title,
                    "description": topic.description,
                    "icon": topic.icon,
                    "stories_count": topic.stories_count + 1  # obviously
                },
                "content": story.content,
                "likes_count": story.likes_count,
                "comments_count": story.comments_count,
                "submitted_date": story.submitted_date.isoformat(),
                # "edited_date": story.edited_date.isoformat(),
                "published_date": None  # obviously
            }

            return web.Response(
                status=201,
                content_type="application/json",
                text=json.dumps(ok(data)))
        else:
            return web.Response(
                status=500,
                content_type="application/json",
                text=json.dumps(error(1004)))


class StoryController(web.View):
    async def get(self):
        """
        Returns the story info.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        # TODO: Join request

        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id))

            if story is None or story.is_removed or not story.is_approved:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            topic = await conn.fetchrow(
                select([topics]).where(topics.c.id == story.topic_id))

        # Check, if topic is present
        if topic is None:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        # FIXME: MODEL: STORY
        data = {
            "id": identifier.to36(story.id),
            "topic": {
                "slug": topic.slug,
                "title": topic.title,
                "description": topic.description,
                "icon": topic.icon,
                "stories_count": topic.stories_count
            },
            "content": story.content,
            "likes_count": story.likes_count,
            "comments_count": story.comments_count,
            # "edited_date": story.edited_date.isoformat(),
            "published_date": story.published_date.isoformat()
        }

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(
                ok(data) if topic is not None else warning(2002, data)))


class LikeController(web.View):
    async def post(self):
        """
        Likes the story.
        """
        return await self._like(True)

    async def delete(self):
        """
        Unlikes the story.
        """
        return await self._like(False)

    async def _like(self, state: bool):  # TODO: Auth required
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        diff = 1 if state else -1

        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id))

            if story is None or story.is_removed or not story.is_approved:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            like = await conn.fetchrow(
                select([story_likes])
                    .where(story_likes.c.user_id == ANONYMOUS_USER_ID)
                    .where(story_likes.c.story_id == story.id)
                    .order_by(story_likes.c.timestamp.desc()))

        if like is None or like.state != state:
            async with self.request.db.transaction() as conn:
                await conn.execute(insert(story_likes).values(
                    user_id=ANONYMOUS_USER_ID,
                    story_id=story.id,
                    state=state,
                    timestamp=datetime.utcnow().replace(tzinfo=pytz.utc)
                ))

                await conn.execute(
                    update(stories)
                        .where(stories.c.id == story.id)
                        .values(likes_count=stories.c.likes_count + diff))

                await conn.execute(
                    update(users)
                        .where(users.c.id == ANONYMOUS_USER_ID)
                        .values(
                        story_likes_count=users.c.story_likes_count + diff))

            async with self.request.db.acquire() as conn:
                like = await conn.fetchrow(
                    select([story_likes])
                        .where(story_likes.c.user_id == ANONYMOUS_USER_ID)
                        .where(story_likes.c.story_id == story.id)
                        .order_by(story_likes.c.timestamp.desc()))

            if like is None:
                return web.Response(
                    status=500,
                    content_type="application/json",
                    text=json.dumps(error(1006)))

        return web.Response(
            status=201,
            content_type="application/json",

            # FIXME: MODEL: STORY LIKE
            text=json.dumps(ok({
                "user": {
                    "id": like.user_id
                },
                "story": {
                    "id": identifier.to36(like.story_id)
                },
                "state": like.state,
                "timestamp": like.timestamp.isoformat()
            })))


class CommentsController(web.View):
    async def get(self):
        """
        Returns comments for the story.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        # TODO: WTF is this? Rewrite via a cte query with depth
        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([
                    stories.c.is_approved,
                    stories.c.is_removed
                ]).where(stories.c.id == id))

            # Comments is not available, if story is not exists, removed or
            # not approved yet.

            if story is None or story.is_removed or not story.is_approved:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            comments_ = await conn.fetch(
                select(
                    [comments, users.c.username.label("author_username")])
                    .where(users.c.id == comments.c.author_id)
                    .where(comments.c.story_id == id)
                    .order_by(comments.c.likes_count.desc()))

        data = OrderedDict(
            [
                (   # FIXME: MODEL: COMMENT
                    identifier.to36(comment.id),
                    {
                        "id": identifier.to36(comment.id),
                        "parent": None if comment.parent_id is None else {
                            "id": identifier.to36(comment.parent_id),
                        },
                        "author": {
                            "id": comment.author_id,
                            "username": comment.author_username
                        },
                        "content": comment.content,
                        "comments": [],
                        "likes_count": comment.likes_count,
                        "comments_count": comment.comments_count,
                        "submitted_date": comment.submitted_date.isoformat(),
                        "edited_date": comment.edited_date.isoformat() if comment.edited_date else None
                    }
                ) for comment in comments_]
        )

        for comment in data.values():
            if comment["parent"] is not None:
                data[comment["parent"]["id"]]["comments"].append(comment)

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(
                ok(list(
                    filter(lambda c: c["parent"] is None, data.values())))))
