"""
The Bestory Project
"""

import json
from aiohttp import web
from sqlalchemy.sql.expression import func

from thebestory.app.lib import identifier, listing
from thebestory.app.models import stories, topics


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
            return web.Response(status=400, content_type='application/json')

        async with request.db.acquire() as conn:
            story = await conn.fetchrow(
                stories.select().where(stories.c.id == id))

            if story.row is None:
                return web.Response(status=404, content_type='application/json')

            topic = await conn.fetchrow(
                topics.select().where(topics.c.id == story.topic_id))

            if topic.row is None:
                return web.Response(status=500, content_type='application/json')

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(self._story(story, topic)))

    async def submit(self, request: web.Request):
        return web.Response(status=403, content_type='application/json')

    async def comments(self, request: web.Request):
        return web.Response(status=403, content_type='application/json')

    async def latest(self, request: web.Request):
        """
        Returns list of last published stories.
        Listings are supported.
        """
        try:
            pivot, limit, direction = self.listing.validate(
                request.url.query.get("before", None),
                request.url.query.get("around", None),
                request.url.query.get("after", None),
                request.url.query.get("limit", None))
        except ValueError:
            return web.Response(status=400, content_type='application/json')

        data = []
        query = stories.select().order_by(stories.c.publish_date.desc())

        async with request.db.acquire() as conn:
            if direction != listing.Direction.AROUND:
                query = query.limit(limit)

                # if pivot is none, fetch first page w/o any parameters
                if pivot is not None:
                    if direction == listing.Direction.BEFORE:
                        query = query.where(stories.c.id < pivot)
                    elif direction == listing.Direction.AFTER:
                        query = query.where(stories.c.id > pivot)

                for row in await conn.fetch(query):
                    data.append(self._story(row))
            else:
                # TODO: check if only part data was fetched
                query_before = query.where(stories.c.id <= pivot).limit(
                    sum(divmod(limit, 2)))
                query_after = query.where(stories.c.id > pivot).limit(
                    limit // 2)

                query = query_before.union(query_after)

                for row in await conn.fetch(query):
                    data.append(self._story(row))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data))

    async def hot(self, request: web.Request):
        return web.Response(status=403, content_type='application/json')

    async def top(self, request: web.Request):
        return web.Response(status=403, content_type='application/json')

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
            return web.Response(status=400, content_type='application/json')

        data = []
        query = stories.select().order_by(func.random()).limit(limit)

        if pivot is not None:
            query = query.where(stories.c.id != pivot)

        async with request.db.acquire() as conn:
            for row in await conn.fetch(query):
                data.append(self._story(row))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data))

    @staticmethod
    def _story(story, topic=None):
        data = dict()

        data["id"] = identifier.to36(story.id)

        data["topic"] = dict()
        data["topic"]["id"] = story.topic_id

        if topic is not None:
            data["topic"]["slug"] = topic.slug
            data["topic"]["title"] = topic.title

        data["content"] = story.content

        data["likes_count"] = 0
        data["comments_count"] = 0

        data["submit_date"] = story.submit_date.isoformat()

        if story.publish_date is not None:
            data["publish_date"] = story.publish_date.isoformat()
        else:
            data["publish_date"] = None

        return data
