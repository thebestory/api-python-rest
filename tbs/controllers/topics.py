"""
The Bestory Project
"""

from sanic.response import json

from tbs import db
from tbs.lib import (
    exceptions,
    helpers,
    listing,
    response_wrapper
)
from tbs.lib.stores import topic as topic_store
from tbs.lib.stores import story as story_store
from tbs.views import topic as topic_view
from tbs.views import story as story_view


# 25 stories per page
__listing = listing.Listing(1, 100, 25)


async def list_topics(request):
    async with db.pool.acquire() as conn:
        topics = await topic_store.list(conn=conn)

        return json(response_wrapper.ok(
            topic_view.render(topic) for topic in topics
        ))


@helpers.login_required
async def create_topic(request):
    topic = request.json

    async with db.pool.acquire() as conn:
        topic = await topic_store.create(
            conn=conn,
            title=topic["title"],
            slug=topic["slug"],
            description=topic["description"],
            icon=topic["icon"],
            is_active=topic.get("is_active", False)
        )

        return json(response_wrapper.ok(topic_view.render(topic)))


async def show_topic(request, id):
    try:
        async with db.pool.acquire() as conn:
            topic = await topic_store.get(conn=conn, id=id)
            return json(response_wrapper.ok(topic_view.render(topic)))
    except exceptions.NotFoundError:
        return json(response_wrapper.error(4002), status=404)


@helpers.login_required
async def update_topic(request, id):
    new_topic = request.json

    async with db.pool.acquire() as conn:
        try:
            topic = await topic_store.get(conn=conn, id=id)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4002), status=404)

        topic = await topic_store.update(conn=conn, id=id, **new_topic)
        return json(response_wrapper.ok(topic_view.render(topic)))


@helpers.login_required
async def delete_topic(request, id):
    return json(response_wrapper.error(2003), status=403)


async def list_topic_latest_stories(request, id):
    try:
        pivot, limit, direction = __listing.validate(
            request.raw_args.get("before", None),
            request.raw_args.get("after", None),
            request.raw_args.get("limit", None)
        )
    except ValueError:
        return json(response_wrapper.error(3001), status=400)

    async with db.pool.acquire() as conn:
        if id != 0:
            try:
                await topic_store.get(conn=conn, id=id)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4002), status=404)

        topics = [] if id == 0 else [id]
        stories = None

        if pivot is not None:
            try:
                pivot = await story_store.get(conn, pivot)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4004), status=400)

            if direction == listing.Direction.BEFORE:
                stories = await story_store.list_latest(
                    conn=conn,
                    topics=topics,
                    published_date_after=pivot["published_date"],
                    limit=limit
                )
            else:
                stories = await story_store.list_latest(
                    conn=conn,
                    topics=topics,
                    published_date_before=pivot["published_date"],
                    limit=limit
                )
        else:
            stories = await story_store.list_latest(
                conn=conn,
                topics=topics,
                limit=limit
            )

        return json(response_wrapper.ok([
            story_view.render(story, story["author"], story["topic"])
            for story in stories
        ]))

async def list_topic_hot_stories(request, id):
    try:
        pivot, limit, direction = __listing.validate(
            request.raw_args.get("before", None),
            request.raw_args.get("after", None),
            request.raw_args.get("limit", None)
        )
    except ValueError:
        return json(response_wrapper.error(3001), status=400)

    async with db.pool.acquire() as conn:
        if id != 0:
            try:
                await topic_store.get(conn=conn, id=id)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4002), status=404)

        topics = [] if id == 0 else [id]
        stories = None

        if pivot is not None:
            try:
                pivot = await story_store.get(conn, pivot)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4004), status=400)

            if direction == listing.Direction.BEFORE:
                stories = await story_store.list_hot(
                    conn=conn,
                    topics=topics,
                    published_date_after=pivot["published_date"],
                    limit=limit
                )
            else:
                stories = await story_store.list_hot(
                    conn=conn,
                    topics=topics,
                    published_date_before=pivot["published_date"],
                    limit=limit
                )
        else:
            stories = await story_store.list_hot(
                conn=conn,
                topics=topics,
                limit=limit
            )

        return json(response_wrapper.ok([
            story_view.render(story, story["author"], story["topic"])
            for story in stories
        ]))


async def list_topic_top_stories(request, id):
    try:
        pivot, limit, direction = __listing.validate(
            request.raw_args.get("before", None),
            request.raw_args.get("after", None),
            request.raw_args.get("limit", None)
        )
    except ValueError:
        return json(response_wrapper.error(3001), status=400)

    async with db.pool.acquire() as conn:
        if id != 0:
            try:
                await topic_store.get(conn=conn, id=id)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4002), status=404)

        topics = [] if id == 0 else [id]
        stories = None

        if pivot is not None:
            try:
                pivot = await story_store.get(conn, pivot)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4004), status=400)

            if direction == listing.Direction.BEFORE:
                stories = await story_store.list_top(
                    conn=conn,
                    topics=topics,
                    published_date_after=pivot["published_date"],
                    limit=limit
                )
            else:
                stories = await story_store.list_top(
                    conn=conn,
                    topics=topics,
                    published_date_before=pivot["published_date"],
                    limit=limit
                )
        else:
            stories = await story_store.list_top(
                conn=conn,
                topics=topics,
                limit=limit
            )

        return json(response_wrapper.ok([
            story_view.render(story, story["author"], story["topic"])
            for story in stories
        ]))


async def list_topic_random_stories(request, id):
    try:
        pivot, limit, direction = __listing.validate(
            request.raw_args.get("before", None),
            request.raw_args.get("after", None),
            request.raw_args.get("limit", None)
        )
    except ValueError:
        return json(response_wrapper.error(3001), status=400)

    async with db.pool.acquire() as conn:
        if id != 0:
            try:
                await topic_store.get(conn=conn, id=id)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4002), status=404)

        topics = [] if id == 0 else [id]

        stories = await story_store.list_random(
            conn=conn,
            topics=topics,
            limit=limit
        )

        return json(response_wrapper.ok([
            story_view.render(story, story["author"], story["topic"])
            for story in stories
        ]))
