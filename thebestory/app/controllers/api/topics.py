"""
The Bestory Project
"""

import json
from aiohttp import web

from thebestory.app.models import stories, topics


class TopicsController:
    async def details(self, request):
        try:
            id = int(request.match_info["id"])
        except KeyError:
            return web.Response(status=400, content_type='application/json')

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                topics.select().where(topics.c.id == id)
            )

            if topic.row is None:
                return web.Response(status=404, content_type='application/json')

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(self._topic(topic))
        )

    async def list(self, request):
        data = []

        async with request.db.acquire() as conn:
            for row in await conn.fetch(
                    topics.select().order_by(topics.c.stories_count.desc())):
                data.append(self._topic(row))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data)
        )

    async def stories(self, request):
        try:
            id = int(request.match_info["id"])
        except KeyError:
            return web.Response(status=400, content_type='application/json')

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                topics.select().where(topics.c.id == id)
            )

            if topic.row is None:
                return web.Response(status=404, content_type='application/json')

            data = []

            for row in await conn.fetch(
                    stories.select().where(stories.c.topic_id == id).order_by(
                            stories.c.publish_date.desc()).limit(20)):
                data.append(self._story(row, topic))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data)
        )

    @staticmethod
    def _topic(topic):
        data = dict()

        data["id"] = topic.id

        data["title"] = topic.title
        data["description"] = topic.desc
        data["icon"] = topic.icon
        data["stories_count"] = topic.stories_count

        return data

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
