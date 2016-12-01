"""
The Bestory Project
"""

import json
from datetime import datetime

import pytz
from aiohttp import web
from sqlalchemy.sql import insert, select, update
from sqlalchemy.sql.expression import func

from thebestory.app.lib import identifier, listing
from thebestory.app.lib.api.response import *
from thebestory.app.models import comments, stories, topics, users

# User ID
ANONYMOUS_USER_ID = 5

# User ID
THEBESTORY_USER_ID = 2


class StoriesController:
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def details(self, request):
        """
        Returns the story info.
        """
        try:
            id = identifier.from36(request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        async with request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id))

            if story is None or story.is_removed:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            if not story.is_approved:
                return web.Response(
                    status=403,
                    content_type="application/json",
                    text=json.dumps(error(4001)))

            topic = await conn.fetchrow(
                select([topics]).where(topics.c.id == story.topic_id))

        data = {
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
        }

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(
                ok(data) if topic is not None else warning(2002, data)))

    # TODO: Auth required
    async def submit(self, request):
        """
        Sumbits a new story.
        """
        try:
            body = await request.json()
            topic_id = int(body["topic"])
            content = body["content"]
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        if len(content) <= 0:
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

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.id == topic_id))

        if topic is None:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        async with request.db.transaction() as conn:
            # TODO: Rewrite, when asyncpgsa replaces nulls with default values
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
                update(topics).values(stories_count=topics.c.stories_count + 1))

        if story_id is not None:
            async with request.db.acquire() as conn:
                story = await conn.fetchrow(
                    select([stories]).where(stories.c.id == story_id))

            if story is None:
                return web.Response(
                    status=500,
                    content_type="application/json",
                    text=json.dumps(error(1004)))

            data = {
                "id": identifier.to36(story.id),
                "content": story.content,
                "topic": None if topic is None else {
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
                "submitted_date": story.submitted_date.isoformat(),
                "published_date": None
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

    async def comments(self, request):
        """
        Returns comments for the story.
        """
        try:
            id = identifier.from36(request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        # TODO: WTF is this? Rewrite via a cte query with depth
        async with request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([
                    stories.c.is_approved,
                    stories.c.is_removed
                ]).where(stories.c.id == id))

            # Comments is not available, if story is not exists, removed or
            # not approved yet.

            if story is None or story.is_removed:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            if not story.is_approved:
                return web.Response(
                    status=403,
                    content_type="application/json",
                    text=json.dumps(error(4001)))

            comments_ = await conn.fetch(
                select([comments, users.c.username])
                    .where(users.c.id == comments.c.author_id)
                    .where(comments.c.story_id == id)
                    .order_by(comments.c.likes_count.desc()))

        data = [{
                    "id": comment.id,
                    "parent_id": comment.parent_id,
                    "author_id": comment.author_id,
                    "content": comment.content,
                    "comments": [],
                    "likes_count": comment.likes_count,
                    "comments_count": comment.comments_count,
                    "submitted_date": comment.submitted_date.isoformat(),
                    "edited_date": comment.edited_date.isoformat()
                } for comment in comments_]

        for comment in data:
            if comment["parent_id"] is not None:
                data[comment["parent_id"]]["comments"].append(comment)

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(
                ok(list(filter(lambda c: c["parent_id"] is None, data)))))

    async def latest(self, request):
        """
        Returns the list of last published stories.
        Listings are supported.
        """
        try:
            pivot, limit, direction = self.listing.validate(
                request.url.query.get("before", None),
                request.url.query.get("after", None),
                request.url.query.get("limit", None))
        except ValueError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001)))

        data = []

        query = select([
            stories.c.id,
            stories.c.topic_id,
            stories.c.content,
            stories.c.likes_count,
            stories.c.comments_count,
            # stories.c.edited_date,
            stories.c.published_date
        ]) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .order_by(stories.c.published_date.desc()) \
            .limit(limit)

        # if pivot is none, fetch first page w/o any parameters
        if pivot is not None:
            if direction == listing.Direction.BEFORE:
                query = query.where(stories.c.id > pivot)
            elif direction == listing.Direction.AFTER:
                query = query.where(stories.c.id < pivot)

        async with request.db.acquire() as conn:
            for story in await conn.fetch(query):
                data.append({
                    "id": identifier.to36(story.id),
                    "content": story.content,
                    "topic": {
                        "id": story.topic_id
                    },
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))

    async def hot(self, request):
        return web.Response(
            status=403,
            content_type="application/json",
            text=json.dumps(error(4001)))

    async def top(self, request):
        """
        Returns the list of top stories.
        Listings are supported.
        """
        try:
            pivot, limit, direction = self.listing.validate(
                request.url.query.get("before", None),
                request.url.query.get("after", None),
                request.url.query.get("limit", None))
        except ValueError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001)))

        data = []

        query = select([
            stories.c.id,
            stories.c.topic_id,
            stories.c.content,
            stories.c.likes_count,
            stories.c.comments_count,
            # stories.c.edited_date,
            stories.c.published_date
        ]) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .order_by(stories.c.likes_count.desc()) \
            .limit(limit)

        # if pivot is none, fetch first page w/o any parameters
        if pivot is not None:
            if direction == listing.Direction.BEFORE:
                query = query.where(stories.c.id > pivot)
            elif direction == listing.Direction.AFTER:
                query = query.where(stories.c.id < pivot)

        async with request.db.acquire() as conn:
            for story in await conn.fetch(query):
                data.append({
                    "id": identifier.to36(story.id),
                    "content": story.content,
                    "topic": {
                        "id": story.topic_id
                    },
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))

    async def random(self, request):
        """
        Returns the list of random stories.
        """
        try:
            limit = self.listing.validate_limit(
                request.url.query.get("limit", None))
        except ValueError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001)))

        data = []

        query = select([
            stories.c.id,
            stories.c.topic_id,
            stories.c.content,
            stories.c.likes_count,
            stories.c.comments_count,
            # stories.c.edited_date,
            stories.c.published_date
        ]) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .order_by(func.random()) \
            .limit(limit)

        async with request.db.acquire() as conn:
            for story in await conn.fetch(query):
                data.append({
                    "id": identifier.to36(story.id),
                    "content": story.content,
                    "topic": {
                        "id": story.topic_id
                    },
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(data))
