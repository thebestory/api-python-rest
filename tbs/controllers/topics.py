"""
The Bestory Project
"""

import typing

from sanic.response import json

from tbs import db
from tbs.lib import exceptions
from tbs.lib import helpers
from tbs.lib import listing
from tbs.lib import response_wrapper
from tbs.lib.stores import topic as topic_store
from tbs.lib.stores import reaction as reaction_store
from tbs.lib.stores import story as story_store
from tbs.views import topic as topic_view
from tbs.views import story as story_view


# 25 stories per page
__listing = listing.Listing(1, 100, 25)


def __export_args_for_listing(request):
    return __listing.validate(request.raw_args.get("before", None),
                              request.raw_args.get("after", None),
                              request.raw_args.get("limit", None))


async def list_topics(request):
    async with db.pool.acquire() as conn:
        topics = await topic_store.list(conn=conn)
        return json(response_wrapper.ok(topic_view.render(topic)
                                        for topic in topics))


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
            is_active=topic.get("is_active", False))
        return json(response_wrapper.ok(topic_view.render(topic)))


async def show_topic(request, id: int):
    try:
        async with db.pool.acquire() as conn:
            topic = await topic_store.get(conn=conn, id=id)
            return json(response_wrapper.ok(topic_view.render(topic)))
    except exceptions.NotFoundError:
        return json(response_wrapper.error(4002), status=404)


@helpers.login_required
async def update_topic(request, id: int):
    new_topic = request.json

    async with db.pool.acquire() as conn:
        try:
            _ = await topic_store.get(conn=conn, id=id)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4002), status=404)

        topic = await topic_store.update(conn=conn, id=id, **new_topic)
        return json(response_wrapper.ok(topic_view.render(topic)))


@helpers.login_required
async def delete_topic(request, id: int):
    async with db.pool.acquire() as conn:
        try:
            _ = await topic_store.get(conn=conn, id=id)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4002), status=404)

        topic = await topic_store.update(conn=conn, id=id, is_active=False)
        return json(response_wrapper.ok(topic_view.render(topic)))


async def _list_topic_stories(request,
                              id: int,
                              store_func: callable,
                              listing_supported: bool=True):
    try:
        pivot, limit, direction = __export_args_for_listing(request)
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

        if listing_supported and pivot is not None:
            try:
                pivot = await story_store.get(conn, pivot)
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4004), status=400)

            if direction == listing.Direction.BEFORE:
                stories = await store_func(
                    conn=conn,
                    topics=topics,
                    published_date_after=pivot["published_date"],
                    limit=limit)
            else:
                stories = await store_func(
                    conn=conn,
                    topics=topics,
                    published_date_before=pivot["published_date"],
                    limit=limit)
        else:
            stories = await store_func(conn=conn, topics=topics, limit=limit)

        stories_ids = [story["id"] for story in stories]
        stories_likes = {id: None for id in stories_ids}

        if helpers.is_authorized(request):
            stories_likes = {id: False for id in stories_ids}

            try:
                reactions = await reaction_store.list(
                    conn=conn,
                    users=[request["session"]["user"]["id"]],
                    objects=stories_ids,
                    preload_user=False)

                for reaction in reactions:
                    stories_likes[reaction["object_id"]] = True
            except exceptions.NotFetchedError:
                pass

        return json(response_wrapper.ok([
            story_view.render(story, stories_likes[story["id"]])
            for story in stories
        ]))

async def list_topic_latest_stories(request, id: int):
    return await _list_topic_stories(request, id, story_store.list_latest)

async def list_topic_hot_stories(request, id: int):
    return await _list_topic_stories(request, id, story_store.list_hot)

async def list_topic_top_stories(request, id: int):
    return await _list_topic_stories(request, id, story_store.list_top)

async def list_topic_random_stories(request, id: int):
    return await _list_topic_stories(
        request, id, story_store.list_random, listing_supported=False)
