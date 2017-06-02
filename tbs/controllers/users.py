"""
The Bestory Project
"""

from sanic.response import json

from tbs import db
from tbs.lib import exceptions
from tbs.lib import response_wrapper
from tbs.lib.stores import user as user_store
from tbs.views import user as user_view


async def create_user(request):
    user = request.json

    with db.pool.acquire() as conn:
        user = await user_store.create(
            conn=conn,
            username=user["username"],
            email=user["email"],
            password=user["password"]
        )

        return json(response_wrapper.ok(user_view.render(user)))


async def show_user(request, id):
    try:
        with db.pool.acquire() as conn:
            user = await user_store.get(conn=conn, id=id)
            return json(response_wrapper.ok(user_view.render(user)))
    except exceptions.NotFoundError:
        return json(response_wrapper.error(4001), status=404)


async def update_user(request, id):
    user = request.json

    with db.pool.acquire() as conn:
        user = await user_store.update(conn=conn, id=id, **user)
        return json(response_wrapper.ok(user_view.render(user)))
