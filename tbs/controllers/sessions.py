"""
The Bestory Project
"""

from sanic.response import json

from tbs import db
from tbs.lib import (
    exceptions,
    password,
    response_wrapper,
    session
)
from tbs.lib.stores import user as user_store
from tbs.views import session as session_view


async def list_sessions(request):
    return json(response_wrapper.error(2003), status=403)


async def create_session(request):
    credentials = request.json

    async with db.pool.acquire() as conn:
        try:
            user = await user_store.get_by_username(
                conn=conn,
                username=credentials["username"]
            )

            if password.verify(credentials["password"], user["password"]):
                return json(response_wrapper.ok(session_view.render(
                    await session.create(user)
                )))
        except exceptions.NotFoundError:
            return json(response_wrapper.error(2004), status=400)


async def show_session(request, id):
    return json(response_wrapper.error(2003), status=403)


async def delete_session(request, id=None):
    if id is not None:
        return json(response_wrapper.error(2003), status=403)

    return json(response_wrapper.ok(None), status=204)
