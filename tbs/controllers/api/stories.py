"""
The Bestory Project
"""

import datetime
import json
from collections import OrderedDict

import pendulum
from aiohttp import web
from sqlalchemy.sql import insert, select, update

from tbs.lib import identifier
from tbs.lib.api import renderer
from tbs.lib.api.response import *
from tbs.models import comments, stories, story_likes, topics, users

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
                text=json.dumps(error(3002))
            )

        # Content checks
        if len(content) <= 5:  # FIXME: Specify this value as a global setting
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5004))
            )
        elif len(content) > stories.c.content.type.length:
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(5006))
            )

        # TODO: Block some ascii graphics, and other unwanted symbols...

        row = None

        try:
            # Commit story to DB, incrementing counters for topic and user
            async with self.request.db.acquire() as conn:

                # FIXME: When asyncpgsa will replace nulls with default values
                story_id = await conn.fetchval(insert(stories).values(
                    author_id=ANONYMOUS_USER_ID,
                    content=content,
                    likes_count=0,
                    comments_count=0,
                    is_approved=False,
                    is_removed=False,
                    submitted_date=datetime.datetime.utcnow().replace(tzinfo=pendulum.UTC)
                ))

            if story_id is None:
                raise ValueError

            async with self.request.db.acquire() as conn:
                row = await conn.fetchrow(
                    select([
                        stories
                    ])
                        .where(stories.c.id == story_id)
                        .order_by(stories.c.submitted_date.desc())
                        .apply_labels()
                )

            if row is None:
                raise ValueError
        except ValueError:
            return web.Response(
                status=500,
                content_type="application/json",
                text=json.dumps(error(1004))
            )

        # POST
        # row is not None (successfully committed)

        data = renderer.story({
            "id": row.stories_id,
            "topic": None,
            "content": row.stories_content,
            "is_liked": False,  # trivia
            "likes_count": row.stories_likes_count,
            "comments_count": row.stories_comments_count,
            "submitted_date": row.stories_submitted_date,
            "edited_date": row.stories_edited_date,
            "published_date": row.stories_published_date
        })

        return web.Response(
            status=201,
            content_type="application/json",
            text=json.dumps(ok(data))
        )


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
                text=json.dumps(error(2003))
            )

        async with self.request.db.acquire() as conn:
            row = await conn.fetchrow(
                select([
                    stories,
                    topics
                ])
                    .where(stories.c.id == id)
                    .where(stories.c.topic_id != None)
                    .where(topics.c.id == stories.c.topic_id)
                    .apply_labels()
            )

            like = await conn.fetchrow(
                select([story_likes])
                    .where(story_likes.c.user_id == ANONYMOUS_USER_ID)
                    .where(story_likes.c.story_id == id)
                    .order_by(story_likes.c.story_id)
                    .order_by(story_likes.c.timestamp.desc())
                    .distinct(story_likes.c.story_id)
            )

        if row is None or row.stories_is_removed or not row.stories_is_approved:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2003))
            )

        data = renderer.story({
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
            "is_liked": False if like is None else like.state,
            "likes_count": row.stories_likes_count,
            "comments_count": row.stories_comments_count,
            "submitted_date": row.stories_submitted_date,
            "edited_date": row.stories_edited_date,
            "published_date": row.stories_published_date
        })

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(data))
        )

    async def patch(self):
        """
        Edit the story.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003))
            )

        try:
            body = await self.request.json()
            content = body.get("content")
            slug = body.get("topic")
            is_approved = body.get("is_approved")

            if is_approved is not None:
                if not isinstance(is_approved, bool):
                    raise ValueError("Property ``is_approved`` must be boolean")
        except Exception:  # FIXME: Specify the errors can raised here
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3002))
            )

        if content is not None:
            # Content checks
            if len(content) <= 5:  # FIXME: Specify this value as a global setting
                return web.Response(
                    status=400,
                    content_type="application/json",
                    text=json.dumps(error(5004))
                )
            elif len(content) > stories.c.content.type.length:
                return web.Response(
                    status=400,
                    content_type="application/json",
                    text=json.dumps(error(5006))
                )

        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id)
            )

            if slug is not None:
                topic = await conn.fetchrow(
                    select([topics]).where(topics.c.slug == slug)
                )
            else:
                topic = None

            like = await conn.fetchrow(
                select([story_likes])
                    .where(story_likes.c.user_id == ANONYMOUS_USER_ID)
                    .where(story_likes.c.story_id == id)
                    .order_by(story_likes.c.story_id)
                    .order_by(story_likes.c.timestamp.desc())
                    .distinct(story_likes.c.story_id)
            )

        if story is None or story.is_removed:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2003))
            )

        if slug is not None and (topic is None or not topic.is_public):
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2002))
            )

        # We cannot publish story, if topic is not specified
        if is_approved is not None \
                and is_approved \
                and (topic is None and story.topic_id is None):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(3002))
            )

        # PRE:
        # is_approved = True

        # POST:
        # topic is not None OR story.topic_id is not None

        if content is not None or slug is not None or is_approved is not None:
            query = update(stories)\
                .where(stories.c.id == id)\
                .values(edited_date=datetime.datetime.utcnow().replace(tzinfo=pendulum.UTC))

            if content is not None:
                query = query.values(content=content)

            if slug is not None:
                query = query.values(topic_id=topic.id)

            if is_approved is not None:
                if is_approved:
                    query = query.values(
                        is_approved=True,
                        published_date=datetime.datetime.utcnow().replace(tzinfo=pendulum.UTC)
                    )
                else:
                    query = query.values(
                        is_approved=False,
                    )

            async with self.request.db.transaction() as conn:
                await conn.execute(query)

                if is_approved is not None:
                    d = 1 if is_approved else -1

                    tq = update(topics)\
                        .values(stories_count=topics.c.stories_count + d)

                    if topic is not None:
                        tq.where(topics.c.id == topic.id)
                    else:
                        tq.where(topics.c.id == story.topic_id)

                    await conn.execute(tq)
                    await conn.execute(
                        update(users)
                            .where(users.c.id == story.author_id)
                            .values(stories_count=users.c.stories_count + d)
                    )

                story = await conn.fetchrow(
                    select([stories]).where(stories.c.id == id)
                )

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(ok(renderer.story({
                "id": story.id,
                "topic": None,
                "content": story.content,
                "is_liked": False if like is None else like.state,
                "likes_count": story.likes_count,
                "comments_count": story.comments_count,
                "submitted_date": story.submitted_date,
                "edited_date": story.edited_date,
                "published_date": story.published_date
            })))
        )

    async def delete(self):
        """
        Delete a story.
        """
        try:
            id = identifier.from36(self.request.match_info["id"])
        except (KeyError, ValueError):
            return web.Response(
                status=400,
                content_type="application/json",
                text=json.dumps(error(2003)))

        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id))

        if story is None or story.is_removed:
            return web.Response(
                status=404,
                content_type="application/json",
                text=json.dumps(error(2003))
            )

        async with self.request.db.acquire() as conn:
            await conn.execute(
                update(stories)
                    .where(stories.c.id == id)
                    .values(is_removed=True)
            )

            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id)
            )

        if story.is_removed:
            return web.Response(
                status=204,
                content_type="application/json"
            )
        else:
            return web.Response(
                status=500,
                content_type="application/json",
                text=json.dumps(error(1004))
            )


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
                text=json.dumps(error(2003))
            )

        diff = 1 if state else -1

        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([stories]).where(stories.c.id == id)
            )

            if story is None or story.is_removed or not story.is_approved:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003))
                )

            like = await conn.fetchrow(
                select([story_likes])
                    .where(story_likes.c.user_id == ANONYMOUS_USER_ID)
                    .where(story_likes.c.story_id == story.id)
                    .order_by(story_likes.c.timestamp.desc())
            )

        if like is None or like.state != state:
            async with self.request.db.transaction() as conn:
                await conn.execute(insert(story_likes).values(
                    user_id=ANONYMOUS_USER_ID,
                    story_id=story.id,
                    state=state,
                    timestamp=datetime.datetime.utcnow().replace(tzinfo=pendulum.UTC)
                ))

                await conn.execute(
                    update(stories)
                        .where(stories.c.id == story.id)
                        .values(likes_count=stories.c.likes_count + diff)
                )

                await conn.execute(
                    update(users)
                        .where(users.c.id == ANONYMOUS_USER_ID)
                        .values(
                        story_likes_count=users.c.story_likes_count + diff)
                )

            async with self.request.db.acquire() as conn:
                like = await conn.fetchrow(
                    select([story_likes])
                        .where(story_likes.c.user_id == ANONYMOUS_USER_ID)
                        .where(story_likes.c.story_id == story.id)
                        .order_by(story_likes.c.timestamp.desc())
                )

            if like is None:
                return web.Response(
                    status=500,
                    content_type="application/json",
                    text=json.dumps(error(1006))
                )

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
            }))
        )


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
                text=json.dumps(error(2003))
            )

        # TODO: WTF is this? Rewrite via a cte query with depth
        async with self.request.db.acquire() as conn:
            story = await conn.fetchrow(
                select([
                    stories.c.is_approved,
                    stories.c.is_removed
                ]).where(stories.c.id == id)
            )

            # Comments is not available, if story is not exists, removed or
            # not approved yet.

            if story is None or story.is_removed or not story.is_approved:
                return web.Response(
                    status=404,
                    content_type="application/json",
                    text=json.dumps(error(2003)))

            comments_ = await conn.fetch(
                select([
                    comments,
                    users.c.username.label("author_username")
                ])
                    .where(users.c.id == comments.c.author_id)
                    .where(comments.c.story_id == id)
                    .order_by(comments.c.submitted_date.desc())
            )

        data = OrderedDict(
            [
                (
                    comment.id,
                    {
                        "id": comment.id,
                        "parent": {
                            "id": comment.parent_id,
                        },
                        "author": {
                            "id": comment.author_id,
                            "username": comment.author_username
                        },
                        "content": comment.content,
                        "comments": [],
                        "likes_count": comment.likes_count,
                        "comments_count": comment.comments_count,
                        "submitted_date": comment.submitted_date,
                        "edited_date": comment.edited_date
                    }
                ) for comment in comments_]
        )

        for comment in data.values():
            if comment["parent"]["id"] is not None:
                data[comment["parent"]["id"]]["comments"].append(comment)

        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps(
                ok([renderer.comment(c)
                    for c in filter(
                        lambda c: c["parent"]["id"] is None, data.values()
                    )])
            )
        )
