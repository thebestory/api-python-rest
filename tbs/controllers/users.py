"""
The Bestory Project
"""

from sanic.response import json

from tbs import db
from tbs.lib import exceptions
from tbs.lib import helpers
from tbs.lib import response_wrapper
from tbs.lib.stores import user as user_store
from tbs.views import user as user_view


async def create_user(request):
    user = request.json

    async with db.pool.acquire() as conn:
        user = await user_store.create(
            conn=conn,
            username=user["username"],
            email=user["email"],
            password=user["password"])

        return json(response_wrapper.ok(user_view.render(user)))


async def show_user(request, id):
    try:
        async with db.pool.acquire() as conn:
            user = await user_store.get(conn=conn, id=id)
            return json(response_wrapper.ok(user_view.render(user)))
    except exceptions.NotFoundError:
        return json(response_wrapper.error(4001), status=404)


@helpers.login_required
async def update_user(request, id):
    new_user = request.json

    async with db.pool.acquire() as conn:
        try:
            _ = await user_store.get(conn=conn, id=id)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(4001), status=404)

        user = await user_store.update(conn=conn, id=id, **new_user)
        return json(response_wrapper.ok(user_view.render(user)))
