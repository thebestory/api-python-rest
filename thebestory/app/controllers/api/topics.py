"""
The Bestory Project
"""

import json

from aiohttp import web
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

from thebestory.app.lib import identifier, listing
from thebestory.app.lib.api.response import *
from thebestory.app.models import stories, topics


class CollectionController(web.View):
    async def get(self):
        """
        Returns list of all topics.
        """
        data = []

        async with self.request.db.acquire() as conn:
            for topic in await conn.fetch(
                    select([topics]).order_by(topics.c.slug.asc())):

                # FIXME: MODEL: TOPIC
                data.append({
                    # "id": topic.id,
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


class TopicController(web.View):
    async def get(self):
        """
        Returns the topic info.
        """
        try:
            slug = self.request.match_info["slug"]
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        async with self.request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.slug == slug))

        if topic is None or not topic.is_public:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002)))

        return web.Response(
            status=200,
            content_type="application/json",

            # FIXME: MODEL: TOPIC
            text=json.dumps(ok({
                # "id": topic.id,
                "slug": topic.slug,
                "title": topic.title,
                "icon": topic.icon,
                "description": topic.description,
                "stories_count": topic.stories_count
            })))


class LatestController(web.View):
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def get(self):
        """
        Returns the list of last published stories in topic.
        Listings are supported.
        """
        try:
            slug = self.request.match_info["slug"]
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        try:
            pivot, limit, direction = self.listing.validate(
                self.request.url.query.get("before", None),
                self.request.url.query.get("after", None),
                self.request.url.query.get("limit", None))
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001)))

        async with self.request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.slug == slug))

        if topic is None or not topic.is_public and topic.slug != "all":
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002)))

        data = []

        query = select([
            stories.c.id,
            stories.c.topic_id,
            stories.c.content,
            stories.c.likes_count,
            stories.c.comments_count,
            # stories.c.edited_date,
            stories.c.published_date,
            topics.c.slug.label("topic_slug")
        ]) \
            .where(topics.c.id == stories.c.topic_id) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .order_by(stories.c.published_date.desc()) \
            .limit(limit)

        if topic.slug != "all":
            query = query.where(stories.c.topic_id == topic.id)

        # if pivot is none, fetch first page w/o any parameters
        if pivot is not None:
            if direction == listing.Direction.BEFORE:
                query = query.where(stories.c.id > pivot)
            elif direction == listing.Direction.AFTER:
                query = query.where(stories.c.id < pivot)

        async with self.request.db.acquire() as conn:
            for story in await conn.fetch(query):

                # FIXME: MODEL: STORY
                data.append({
                    "id": identifier.to36(story.id),
                    "topic": {
                        # "id": story.topic_id
                        "slug": story.topic_slug
                    },
                    "content": story.content,
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))


class HotController(web.View):
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    @staticmethod
    async def get():
        """
        Returns the list of hot stories in topic.
        Listings are supported.
        """
        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(error(4001)))


class TopController(web.View):
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def get(self):
        """
        Returns the list of top stories in topic.
        Listings are supported.
        """
        try:
            slug = self.request.match_info["slug"]
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        try:
            pivot, limit, direction = self.listing.validate(
                self.request.url.query.get("before", None),
                self.request.url.query.get("after", None),
                self.request.url.query.get("limit", None))
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001)))

        async with self.request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.slug == slug))

        if topic is None or not topic.is_public and topic.slug != "all":
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002)))

        data = []

        query = select([
            stories.c.id,
            stories.c.topic_id,
            stories.c.content,
            stories.c.likes_count,
            stories.c.comments_count,
            # stories.c.edited_date,
            stories.c.published_date,
            topics.c.slug.label("topic_slug")
        ]) \
            .where(topics.c.id == stories.c.topic_id) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .order_by(stories.c.likes_count.desc()) \
            .order_by(stories.c.published_date.desc()) \
            .limit(limit)

        if topic.slug != "all":
            query = query.where(stories.c.topic_id == topic.id)

        # if pivot is none, fetch first page w/o any parameters
        if pivot is not None:
            if direction == listing.Direction.BEFORE:
                query = query.where(stories.c.id > pivot)
            elif direction == listing.Direction.AFTER:
                query = query.where(stories.c.id < pivot)

        async with self.request.db.acquire() as conn:
            for story in await conn.fetch(query):

                # FIXME: MODEL: STORY
                data.append({
                    "id": identifier.to36(story.id),
                    "topic": {
                        # "id": story.topic_id
                        "slug": story.topic_slug
                    },
                    "content": story.content,
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))


class RandomController(web.View):
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def get(self):
        """
        Returns the list of random stories.
        """
        try:
            slug = self.request.match_info["slug"]
        except KeyError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2002)))

        try:
            limit = self.listing.validate_limit(
                self.request.url.query.get("limit", None))
        except ValueError:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001)))

        async with self.request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.slug == slug))

        if topic is None or not topic.is_public and topic.slug != "all":
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002)))

        data = []

        query = select([
            stories.c.id,
            stories.c.topic_id,
            stories.c.content,
            stories.c.likes_count,
            stories.c.comments_count,
            # stories.c.edited_date,
            stories.c.published_date,
            topics.c.slug.label("topic_slug")
        ]) \
            .where(topics.c.id == stories.c.topic_id) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .order_by(func.random()) \
            .limit(limit)

        if topic.slug != "all":
            query = query.where(stories.c.topic_id == topic.id)

        async with self.request.db.acquire() as conn:
            for story in await conn.fetch(query):

                # FIXME: MODEL: STORY
                data.append({
                    "id": identifier.to36(story.id),
                    "topic": {
                        # "id": story.topic_id
                        "slug": story.topic_slug
                    },
                    "content": story.content,
                    "likes_count": story.likes_count,
                    "comments_count": story.comments_count,
                    # "edited_date": story.edited_date.isoformat(),
                    "published_date": story.published_date.isoformat()
                })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data)))
