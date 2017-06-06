"""
The Bestory Project
"""

from asyncpg.connection import Connection
from sanic.response import text, json

from tbs import db
from tbs.lib import exceptions
from tbs.lib import helpers
from tbs.lib import response_wrapper
from tbs.lib.stores import user as user_store
from tbs.lib.stores import topic as topic_store
from tbs.lib.stores import reaction as reaction_store
from tbs.lib.stores import story as story_store
from tbs.views import reaction as reaction_view
from tbs.views import story as story_view


async def _get_user_like_status(request, conn: Connection, story_id: int):
    like = None

    if helpers.is_authorized(request):
        like = False

        try:
            reactions = await reaction_store.list(
                conn=conn,
                users=[request["session"]["user"]["id"]],
                objects=[story_id],
                preload_user=False)

            if len(reactions) > 0:
                like = True
        except exceptions.NotFetchedError:
            pass

    return like


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

        like = await _get_user_like_status(request, conn, story["id"])
        return json(response_wrapper.ok(story_view.render(story, like)),
                    status=201)


async def show_story(request, id: int):
    async with db.pool.acquire() as conn:
        try:
            story = await story_store.get(conn=conn, id=id)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        like = await _get_user_like_status(request, conn, story["id"])
        return json(response_wrapper.ok(story_view.render(story, like)))


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
        like = await _get_user_like_status(request, conn, story["id"])
        return json(response_wrapper.ok(story_view.render(story, like)))


@helpers.login_required
async def delete_story(request, id):
    async with db.pool.acquire() as conn:
        try:
            _ = await story_store.get(conn=conn, id=id, preload_topic=False,
                                      preload_author=False)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        _ = await story_store.update(conn=conn, id=id, is_removed=True)
        return text("", status=204)


async def list_story_reactions(request, story_id):
    async with db.pool.acquire() as conn:
        try:
            _ = await story_store.get(conn=conn, id=story_id, preload_topic=False,
                                      preload_author=False)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        reactions = await reaction_store.list(conn=conn, objects=[story_id])
        return json(response_wrapper.ok([
            reaction_view.render(reaction) for reaction in reactions
        ]))


@helpers.login_required
async def create_story_reaction(request, story_id):
    async with db.pool.acquire() as conn:
        try:
            _ = await story_store.get(conn=conn, id=story_id, preload_topic=False,
                                      preload_author=False)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        reactions = await reaction_store.list(
            conn=conn,
            users=[request["session"]["user"]["id"]],
            objects=[story_id],
            preload_user=False)

        reaction = None

        if len(reactions) > 0:
            reaction = reactions[0]
        else:
            async with conn.transaction():
                reaction = await reaction_store.create(
                    conn=conn,
                    user_id=request["session"]["user"]["id"],
                    object_id=story_id,
                    reaction_id=0)

                await user_store.increment_story_reactions_counter(
                    conn=conn, id=request["session"]["user"]["id"])
                await story_store.increment_reactions_counter(
                    conn=conn, id=story_id)

        return json(response_wrapper.ok(reaction_view.render(reaction)),
                    status=201)


@helpers.login_required
async def delete_story_reaction(request, story_id):
    async with db.pool.acquire() as conn:
        try:
            _ = await story_store.get(conn=conn, id=story_id, preload_topic=False,
                                      preload_author=False)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4004), status=404)

        async with conn.transaction():
            await reaction_store.delete(
                conn=conn,
                user_id=request["session"]["user"]["id"],
                object_id=story_id,
                reaction_id=0)

            await user_store.decrement_story_reactions_counter(
                conn=conn, id=request["session"]["user"]["id"])
            await story_store.decrement_reactions_counter(
                conn=conn, id=story_id)

        return text("", status=204)


async def list_story_comments(request, story_id):
    return json(response_wrapper.error(2003), status=403)


async def create_story_comment(request, story_id):
    return json(response_wrapper.error(2003), status=403)


async def show_story_comment(request, story_id, id):
    return json(response_wrapper.error(2003), status=403)


async def update_story_comment(request, story_id, id):
    return json(response_wrapper.error(2003), status=403)


async def delete_story_comment(request, story_id, id):
    return json(response_wrapper.error(2003), status=403)


async def list_story_comment_reactions(request, story_id, comment_id):
    return json(response_wrapper.error(2003), status=403)


async def create_story_comment_reaction(request, story_id, comment_id):
    return json(response_wrapper.error(2003), status=403)


async def delete_story_comment_reaction(request, story_id, comment_id):
    return json(response_wrapper.error(2003), status=403)
