"""
The Bestory Project
"""

import json
from aiohttp import web
from sqlalchemy.sql.expression import func

from thebestory.app.models import stories, topics


class StoriesController:
    async def details(self, request: web.Request):
        try:
            id = int(request.match_info["id"])
        except KeyError:
            return web.Response(status=400, content_type='application/json')

        async with request.db.acquire() as conn:
            story = await conn.fetchrow(
                stories.select().where(stories.c.id == id))

            if story.row is None:
                return web.Response(status=404, content_type='application/json')

            topic = await conn.fetchrow(
                topics.select().where(topics.c.id == story.topic_id)
            )

            if topic.row is None:
                return web.Response(status=500, content_type='application/json')

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(self._story(story, topic))
        )

    async def submit(self, request: web.Request):
        pass

    async def comments(self, request: web.Request):
        pass

    async def latest(self, request: web.Request):
        data = []

        async with request.db.acquire() as conn:
            for row in await conn.fetch(
                    stories.select().order_by(
                        stories.c.publish_date.desc()).limit(20)):
                data.append(self._story(row))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data)
        )

    async def hot(self, request: web.Request):
        pass

    async def top(self, request: web.Request):
        pass

    async def random(self, request: web.Request):
        data = []

        async with request.db.acquire() as conn:
            for row in await conn.fetch(
                    stories.select().order_by(func.random()).limit(20)):
                data.append(self._story(row))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data)
        )

    @staticmethod
    def _story(story, topic=None):
        data = dict()

        data["id"] = story.id

        data["topic"] = dict()
        data["topic"]["id"] = story.topic_id

        if topic is not None:
            data["topic"]["title"] = topic.title

        data["content"] = story.content
        data["likes_count"] = 0
        data["comments_count"] = 0
        data["submitted_date"] = story.submit_date.isoformat()

        if story.publish_date is not None:
            data["published_date"] = story.publish_date.isoformat()
        else:
            data["published_date"] = None

        return data
