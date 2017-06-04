"""
The Bestory Project
"""

from sanic.response import json

from tbs import db
from tbs.lib import exceptions
from tbs.lib import helpers
from tbs.lib import response_wrapper
from tbs.lib.stores import user as user_store
from tbs.lib.stores import topic as topic_store
from tbs.lib.stores import story as story_store
from tbs.views import story as story_view


@helpers.login_required
async def create_story(request):
    story = request.json

    if story.get("author", None) is None:
        story["author"] = request["session"]["user"]

    async with db.pool.acquire() as conn:
        try:
            author = await user_store.get(conn, story["author"]["id"])
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4001), status=400)

        try:
            topic = None
            if story.get("topic", None) is not None:
                topic = await topic_store.get(conn, story["topic"]["id"])
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4002), status=400)

        story = await story_store.create(
            conn=conn,
            author_id=author["id"],
            content=story["content"],
            topic_id=topic["id"] if topic is not None else None,
            is_published=story.get("is_published", False),
            is_removed=story.get("is_removed", False))

        return json(response_wrapper.ok(story_view.render(
            story, story["author"], story["topic"])))


async def show_story(request, id):
    async with db.pool.acquire() as conn:
        try:
            story = await story_store.get(conn=conn, id=id)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        return json(response_wrapper.ok(story_view.render(
            story, story["author"], story["topic"]
        )))


@helpers.login_required
async def update_story(request, id):
    new_story = request.json

    async with db.pool.acquire() as conn:
        try:
            _ = await story_store.get(conn=conn, id=id, preload_topic=False,
                                      preload_author=False)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        if new_story.get("topic") is not None:
            try:
                topic = await topic_store.get(conn, new_story["topic"]["id"])
                new_story["topic_id"] = topic["id"]
            except exceptions.NotFoundError:
                return json(response_wrapper.error(4002), status=400)

        story = await story_store.update(conn=conn, id=id, **new_story)

        return json(response_wrapper.ok(story_view.render(
            story, story["author"], story["topic"])))


@helpers.login_required
async def delete_story(request, id):
    return json(response_wrapper.error(2003), status=403)


async def list_story_reactions(request, story_id):
    return json({"hello": "world"})


async def create_story_reaction(request, story_id):
    return json({"hello": "world"})


async def delete_story_reaction(request, story_id):
    return json({"hello": "world"})


async def list_story_comments(request, story_id):
    return json({"hello": "world"})


async def create_story_comment(request, story_id):
    return json({"hello": "world"})


async def show_story_comment(request, story_id, id):
    return json({"hello": "world"})


async def update_story_comment(request, story_id, id):
    return json({"hello": "world"})


async def delete_story_comment(request, story_id, id):
    return json({"hello": "world"})


async def list_story_comment_reactions(request, story_id, comment_id):
    return json({"hello": "world"})


async def create_story_comment_reaction(request, story_id, comment_id):
    return json({"hello": "world"})


async def delete_story_comment_reaction(request, story_id, comment_id):
    return json({"hello": "world"})
