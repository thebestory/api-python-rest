"""
The Bestory Project
"""

import json
from aiohttp import web

from thebestory.app.lib import identifier, listing
from thebestory.app.models import stories, topics


class TopicsController:
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def details(self, request):
        """
        Returns the topic info.
        """
        try:
            id = int(request.match_info["id"])
        except KeyError:
            return web.Response(status=400, content_type='application/json')

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                topics.select().where(topics.c.id == id))

            if topic.row is None:
                return web.Response(status=404, content_type='application/json')

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(self._topic(topic)))

    async def list(self, request):
        """
        Returns list of all topics.
        """
        data = []

        async with request.db.acquire() as conn:
            for row in await conn.fetch(
                    topics.select().order_by(topics.c.slug.desc())):
                data.append(self._topic(row))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data))

    # TODO: Before and After with publish dates, not IDs
    async def stories(self, request):
        """
        Returns list of stories in the topic.
        Listings are supported.
        """
        try:
            id = int(request.match_info["id"])
            pivot, limit, direction = self.listing.validate(
                request.url.query.get("before", None),
                request.url.query.get("around", None),
                request.url.query.get("after", None),
                request.url.query.get("limit", None))
        except (KeyError, ValueError):
            return web.Response(status=400, content_type='application/json')

        data = []
        query = stories.select().where(stories.c.topic_id == id).order_by(
            stories.c.publish_date.desc())

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                topics.select().where(topics.c.id == id))

            if topic.row is None:
                return web.Response(status=404, content_type='application/json')

            if direction != listing.Direction.AROUND:
                query = query.limit(limit)

                # if pivot is none, fetch first page w/o any parameters
                if pivot is not None:
                    if direction == listing.Direction.BEFORE:
                        query = query.where(stories.c.id < pivot)
                    elif direction == listing.Direction.AFTER:
                        query = query.where(stories.c.id > pivot)

                for row in await conn.fetch(query):
                    data.append(self._story(row, topic))
            else:
                # TODO: check if only part data was fetched
                query_before = query.where(stories.c.id <= pivot).limit(
                    sum(divmod(limit, 2)))
                query_after = query.where(stories.c.id > pivot).limit(
                    limit // 2)

                query = query_before.union(query_after)

                for row in await conn.fetch(query):
                    data.append(self._story(row, topic))

        return web.Response(
            status=200,
            content_type='application/json',
            text=json.dumps(data))

    @staticmethod
    def _topic(topic):
        data = dict()

        data["id"] = topic.id
        data["slug"] = topic.slug
        data["title"] = topic.title
        data["description"] = topic.desc
        data["icon"] = topic.icon
        data["stories_count"] = topic.stories_count

        return data

    @staticmethod
    def _story(story, topic):
        data = dict()

        data["id"] = identifier.to36(story.id)

        data["topic"] = dict()
        data["topic"]["id"] = topic.id
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
