"""
The Bestory Project
"""

import json

from aiohttp import web
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

from thebestory.lib import listing
from thebestory.lib.api import renderer
from thebestory.lib.api.response import *
from thebestory.models import stories, topics, story_likes

# User ID
ANONYMOUS_USER_ID = 5

# User ID
THEBESTORY_USER_ID = 2


class CollectionController(web.View):
    async def get(self):
        """
        Returns list of all topics.
        """
        data = []

        async with self.request.db.acquire() as conn:
            for topic in await conn.fetch(
                    select([topics])
                            .where(topics.c.is_public == True)
                            .order_by(topics.c.slug.asc())
            ):
                data.append(renderer.topic({
                    "id": topic.id,
                    "slug": topic.slug,
                    "title": topic.title,
                    "icon": topic.icon,
                    "description": topic.description,
                    "stories_count": topic.stories_count
                }))

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data))
        )


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
                text=json.dumps(error(2002))
            )

        async with self.request.db.acquire() as conn:
            topic = await conn.fetchrow(
                select([topics]).where(topics.c.slug == slug)
            )

        if topic is None or not topic.is_public:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002))
            )

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(renderer.topic({
                    "id": topic.id,
                    "slug": topic.slug,
                    "title": topic.title,
                    "icon": topic.icon,
                    "description": topic.description,
                    "stories_count": topic.stories_count
            })))
        )


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
                text=json.dumps(error(2002))
            )

        try:
            pivot, limit, direction = self.listing.validate(
                self.request.url.query.get("before", None),
                self.request.url.query.get("after", None),
                self.request.url.query.get("limit", None)
            )
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001))
            )

        async with self.request.db.acquire() as conn:
            pivot_topic = None
            if slug != "all":
                pivot_topic = await conn.fetchrow(
                    select([topics]).where(topics.c.slug == slug)
                )

            pivot_story = None
            if pivot:
                pivot_story = await conn.fetchrow(
                    select([stories]).where(stories.c.id == pivot)
                )

        if slug != "all" and (pivot_topic is None or not pivot_topic.is_public):
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002))
            )

        if pivot and pivot_story is None:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001))
            )

        data = []
        ids = {}

        query = select([
            stories,
            topics
        ]) \
            .where(stories.c.topic_id != None) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .where(topics.c.is_public == True) \
            .where(topics.c.id == stories.c.topic_id) \
            .order_by(stories.c.published_date.desc()) \
            .limit(limit) \
            .apply_labels()

        if slug != "all":
            query = query.where(stories.c.topic_id == pivot_topic.id)

        # if pivot is none, fetch first page w/o any parameters
        if pivot:
            if direction == listing.Direction.BEFORE:
                query = query.where(
                    stories.c.published_date > pivot_story.published_date
                )
            elif direction == listing.Direction.AFTER:
                query = query.where(
                    stories.c.published_date < pivot_story.published_date
                )

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                r = {
                    "id": row.stories_id,
                    "topic": {
                        "id": row.topics_id,
                        "slug": row.topics_slug,
                        "title": row.topics_title,
                        "icon": row.topics_icon,
                        "description": row.topics_description,
                        "stories_count": row.topics_stories_count
                    },
                    "content": row.stories_content,
                    "is_liked": False,
                    "likes_count": row.stories_likes_count,
                    "comments_count": row.stories_comments_count,
                    "submitted_date": row.stories_submitted_date,
                    "edited_date": row.stories_edited_date,
                    "published_date": row.stories_published_date
                }

                data.append(r)
                ids[row.stories_id] = r

        query = select([story_likes]) \
            .where(story_likes.c.user_id == ANONYMOUS_USER_ID) \
            .where(story_likes.c.story_id.in_([k for k in ids.keys()])) \
            .order_by(story_likes.c.story_id) \
            .order_by(story_likes.c.timestamp.desc()) \
            .distinct(story_likes.c.story_id)

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                ids[row.story_id]["is_liked"] = row.state

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok([renderer.story(row) for row in data]))
        )


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
            text=json.dumps(error(4001))
        )


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
                text=json.dumps(error(2002))
            )

        try:
            pivot, limit, direction = self.listing.validate(
                self.request.url.query.get("before", None),
                self.request.url.query.get("after", None),
                self.request.url.query.get("limit", None)
            )
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001))
            )

        async with self.request.db.acquire() as conn:
            pivot_topic = None
            if slug != "all":
                pivot_topic = await conn.fetchrow(
                    select([topics]).where(topics.c.slug == slug)
                )

            pivot_story = None
            if pivot:
                pivot_story = await conn.fetchrow(
                    select([stories]).where(stories.c.id == pivot)
                )

        if slug != "all" and (pivot_topic is None or not pivot_topic.is_public):
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002))
            )

        if pivot and pivot_story is None:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001))
            )

        data = []
        ids = {}

        query = select([
            stories,
            topics
        ]) \
            .where(stories.c.topic_id != None) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .where(topics.c.is_public == True) \
            .where(topics.c.id == stories.c.topic_id) \
            .order_by(stories.c.likes_count.desc()) \
            .order_by(stories.c.published_date.desc()) \
            .limit(limit) \
            .apply_labels()

        if slug != "all":
            query = query.where(stories.c.topic_id == pivot_topic.id)

        # if pivot is none, fetch first page w/o any parameters
        if pivot:
            if direction == listing.Direction.BEFORE:
                query = query.where(
                    (stories.c.likes_count > pivot_story.likes_count)
                    | ((stories.c.likes_count == pivot_story.likes_count) &
                       (stories.c.published_date > pivot_story.published_date))
                )
            elif direction == listing.Direction.AFTER:
                query = query.where(
                    (stories.c.likes_count < pivot_story.likes_count)
                    | ((stories.c.likes_count == pivot_story.likes_count) &
                       (stories.c.published_date < pivot_story.published_date))
                )

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                r = {
                    "id": row.stories_id,
                    "topic": {
                        "id": row.topics_id,
                        "slug": row.topics_slug,
                        "title": row.topics_title,
                        "icon": row.topics_icon,
                        "description": row.topics_description,
                        "stories_count": row.topics_stories_count
                    },
                    "content": row.stories_content,
                    "is_liked": False,
                    "likes_count": row.stories_likes_count,
                    "comments_count": row.stories_comments_count,
                    "submitted_date": row.stories_submitted_date,
                    "edited_date": row.stories_edited_date,
                    "published_date": row.stories_published_date
                }

                data.append(r)
                ids[row.stories_id] = r

        query = select([story_likes]) \
            .where(story_likes.c.user_id == ANONYMOUS_USER_ID) \
            .where(story_likes.c.story_id.in_([k for k in ids.keys()])) \
            .order_by(story_likes.c.story_id) \
            .order_by(story_likes.c.timestamp.desc()) \
            .distinct(story_likes.c.story_id)

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                ids[row.story_id]["is_liked"] = row.state

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok([renderer.story(row) for row in data]))
        )


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
            pivot_topic = None
            if slug != "all":
                pivot_topic = await conn.fetchrow(
                    select([topics]).where(topics.c.slug == slug)
                )

        if slug != "all" and (pivot_topic is None or not pivot_topic.is_public):
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002))
            )

        data = []
        ids = {}

        query = select([
            stories,
            topics
        ]) \
            .where(stories.c.topic_id != None) \
            .where(stories.c.is_approved == True) \
            .where(stories.c.is_removed == False) \
            .where(topics.c.is_public == True) \
            .where(topics.c.id == stories.c.topic_id) \
            .order_by(func.random()) \
            .limit(limit) \
            .apply_labels()

        if slug != "all":
            query = query.where(stories.c.topic_id == pivot_topic.id)

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                r = {
                    "id": row.stories_id,
                    "topic": {
                        "id": row.topics_id,
                        "slug": row.topics_slug,
                        "title": row.topics_title,
                        "icon": row.topics_icon,
                        "description": row.topics_description,
                        "stories_count": row.topics_stories_count
                    },
                    "content": row.stories_content,
                    "is_liked": False,
                    "likes_count": row.stories_likes_count,
                    "comments_count": row.stories_comments_count,
                    "submitted_date": row.stories_submitted_date,
                    "edited_date": row.stories_edited_date,
                    "published_date": row.stories_published_date
                }

                data.append(r)
                ids[row.stories_id] = r

        query = select([story_likes]) \
            .where(story_likes.c.user_id == ANONYMOUS_USER_ID) \
            .where(story_likes.c.story_id.in_([k for k in ids.keys()])) \
            .order_by(story_likes.c.story_id) \
            .order_by(story_likes.c.timestamp.desc()) \
            .distinct(story_likes.c.story_id)

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                ids[row.story_id]["is_liked"] = row.state

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok([renderer.story(row) for row in data]))
        )


class UnapprovedController(web.View):
    # 25 stories per page
    listing = listing.Listing(1, 100, 25)

    async def get(self):
        """
        Returns the list of unapproved stories in topic.
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
            pivot_topic = None
            if slug != "all":
                pivot_topic = await conn.fetchrow(
                    select([topics]).where(topics.c.slug == slug)
                )

            pivot_story = None
            if pivot:
                pivot_story = await conn.fetchrow(
                    select([stories]).where(stories.c.id == pivot)
                )

        if slug != "all" and (pivot_topic is None or not pivot_topic.is_public):
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002))
            )

        if pivot and pivot_story is None:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3001))
            )

        data = []

        query = select([
            stories
        ]) \
            .where(stories.c.is_approved == False) \
            .where(stories.c.is_removed == False) \
            .order_by(stories.c.submitted_date.desc()) \
            .limit(limit) \
            .apply_labels()

        if slug != "all":
            query = query.where(stories.c.topic_id == pivot_topic.id)

        # if pivot is none, fetch first page w/o any parameters
        if pivot:
            if direction == listing.Direction.BEFORE:
                query = query.where(
                    stories.c.submitted_date > pivot_story.submitted_date
                )
            elif direction == listing.Direction.AFTER:
                query = query.where(
                    stories.c.submitted_date < pivot_story.submitted_date
                )

        async with self.request.db.acquire() as conn:
            for row in await conn.fetch(query):
                data.append(renderer.story({
                    "id": row.stories_id,
                    "topic": None,
                    "content": row.stories_content,
                    "is_liked": None,  # we do not provide this info for mods
                    "likes_count": row.stories_likes_count,
                    "comments_count": row.stories_comments_count,
                    "submitted_date": row.stories_submitted_date,
                    "edited_date": row.stories_edited_date,
                    "published_date": row.stories_published_date
                }))

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data))
        )
