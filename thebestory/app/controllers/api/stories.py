"""
The Bestory Project
"""

import json
from aiohttp import web
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

from thebestory.app.lib import identifier, listing
from thebestory.app.lib.api.response import ok, warning, error
from thebestory.app.lib.api import formatter
from thebestory.app.models import (
    comment,
    like,
    story,
    topic,
    user
)


class StoriesController:
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def details(self, request: web.Request):
        """
        Returns the story info.
        """
        try:
            id = identifier.from36(request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003))
            )

        async with request.db.acquire() as conn:
            s = await conn.fetchrow(select([story.t])
                                    .where(story.t.c.id == id))

            if s.row is None:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003))
                )

            t = await conn.fetchrow(select([topic.t])
                                    .where(topic.t.c.id == s.topic_id))

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(
                ok(formatter.story(
                    s=s,
                    extended=False,
                    t=t,
                    extended_t=True
                ))
                if t.row is not None
                else
                warning(2002, formatter.story(
                    s=s,
                    extended=False,
                    t=t,
                    extended_t=True
                ))
            )
        )

    # TODO: Submit story (auth required)
    async def submit(self, request: web.Request):
        return web.Response(
            status=403,
            content_type="application/json",
            text=json.dumps(error(4001))
        )

    async def comments(self, request: web.Request):
        """
        Returns comments for the story.
        """
        try:
            id = identifier.from36(request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003))
            )

        # TODO: WTF is this? Rewrite via a cte query with depth
        async with request.db.acquire() as conn:
            c = await conn.fetchrow(select([comment.t, user.t.username])
                                    .where(comment.t.c.story_id == id)
                                    .order_by(comment.t.c.likes_count.desc())
                                    .outerjoin(user.t))

        data = [formatter.comment(c, extended=False).update(comments=[])
                for c in c]

        for c in data:
            if c.parent_id is not None:
                data[c.parent_id].append(c)

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(filter(lambda c: c.parent_id is None, data)))
        )

    async def latest(self, request: web.Request):
        """
        Returns list of last published stories.
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
                text=json.dumps(error(2003))
            )

        data = []
        query = select([
            story.t,
            topic.t.c.slug.label("topic_slug"),
            topic.t.c.title.label("topic_title"),
            topic.t.c.icon.label("topic_icon")
        ]).order_by(story.t.c.publish_date.desc()).outerjoin(topic.t)

        async with request.db.acquire() as conn:
            query = query.limit(limit)

            # if pivot is none, fetch first page w/o any parameters
            if pivot is not None:
                if direction == listing.Direction.BEFORE:
                    query = query.where(story.t.c.id < pivot)
                elif direction == listing.Direction.AFTER:
                    query = query.where(story.t.c.id > pivot)

            for row in await conn.fetch(query):
                data.append(formatter.story(row, extended=False))

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data))
        )

    async def hot(self, request: web.Request):
        return web.Response(status=403, content_type="application/json")

    async def top(self, request: web.Request):
        return web.Response(status=403, content_type="application/json")

    async def random(self, request: web.Request):
        """
        Returns list of random stories.
        """
        try:
            # Any parameter will be regarded as an element which does not need
            # to include in response
            pivot, limit, direction = self.listing.validate(
                request.url.query.get("before", None),
                request.url.query.get("around", None),
                request.url.query.get("after", None),
                request.url.query.get("limit", None))
        except ValueError:
            return web.Response(status=400, content_type="application/json")

        data = []
        query = table.select().order_by(func.random()).limit(limit)

        if pivot is not None:
            query = query.where(table.c.id != pivot)

        async with request.db.acquire() as conn:
            for row in await conn.fetch(query):
                data.append(self._story(row))

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(data))
