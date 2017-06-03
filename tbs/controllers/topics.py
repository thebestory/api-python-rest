"""
The Bestory Project
"""

from sanic.response import json

from tbs import db
from tbs.lib import (
    exceptions,
    helpers,
    response_wrapper
)
from tbs.lib.stores import topic as topic_store
from tbs.views import topic as topic_view


async def list_topics(request):
    async with db.pool.acquire() as conn:
        topics = await topic_store.list(conn=conn)
        topics = [topic_view.render(topic) for topic in topics]
        return json(response_wrapper.ok(topics))


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
    return json({"hello": "world"})


async def list_topic_hot_stories(request, id):
    return json({"hello": "world"})


async def list_topic_top_stories(request, id):
    return json({"hello": "world"})


async def list_topic_random_stories(request, id):
    return json({"hello": "world"})
