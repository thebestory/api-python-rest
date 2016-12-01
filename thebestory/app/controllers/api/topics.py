"""
The Bestory Project
"""

import json
from aiohttp import web
from sqlalchemy.sql import select

from thebestory.app.lib import identifier, listing
from thebestory.app.lib.api.response import *
from thebestory.app.models import stories, topics


# TODO: In next API, upgrade to ``slug`` only public IDs (but save internal IDs)
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
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.id == id))

        if topic is None:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002)))

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok({
                "id": topic.id,
                "slug": topic.slug,
                "title": topic.title,
                "icon": topic.icon,
                "description": topic.description,
                "stories_count": topic.stories_count
            })))

    async def list(self, request):
        """
        Returns list of all topics.
        """
        data = []

        async with request.db.acquire() as conn:
            for topic in await conn.fetch(
                    select([topics]).order_by(topics.c.slug.desc())):
                data.append({
                    "id": topic.id,
                    "slug": topic.slug,
                    "title": topic.title,
                    "icon": topic.icon,
                    "description": topic.description,
                    "stories_count": topic.stories_count
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))

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
                request.url.query.get("after", None),
                request.url.query.get("limit", None)
            )
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        data = []

        async with request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.id == id))

            if topic is None:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2002)))

            query = select([
                stories.t.c.id,
                stories.t.c.content,
                stories.t.c.likes_count,
                stories.t.c.comments_count,
                # stories.t.c.edited_date,
                stories.t.c.published_date
            ]) \
                .where(topics.c.id == topic.id) \
                .where(stories.c.is_approved is True) \
                .where(stories.c.is_removed is False) \
                .order_by(stories.t.c.published_date.desc())

            # if pivot is none, fetch first page w/o any parameters
            if pivot is not None:
                if direction == listing.Direction.AFTER:
                    query = query.where(stories.c.id < pivot)
                elif direction == listing.Direction.BEFORE:
                    query = query.where(stories.c.id > pivot)

            for story in await conn.fetch(query):
                data.append({
                    "id": identifier.to36(story.id),
                    "content": story.content,
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date,
                    "published_date": story.published_date
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))
