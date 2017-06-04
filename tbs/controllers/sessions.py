"""
The Bestory Project
"""

from sanic.response import text, json

from tbs import db
from tbs.lib import exceptions
from tbs.lib import helpers
from tbs.lib import password
from tbs.lib import response_wrapper
from tbs.lib import session
from tbs.lib.stores import user as user_store
from tbs.views import session as session_view


@helpers.login_required
async def list_sessions(request):
    return json(response_wrapper.error(2003), status=403)


async def create_session(request):
    credentials = request.json

    async with db.pool.acquire() as conn:
        try:
            user = await user_store.get_by_username(
                conn=conn, username=credentials["username"])

            if password.verify(credentials["password"], user["password"]):
                return json(response_wrapper.ok(session_view.render(
                    await session.create(user))), status=201)
            else:
                return json(response_wrapper.error(2004), status=400)
        except exceptions.NotFoundError:
            return json(response_wrapper.error(2004), status=400)


@helpers.login_required
async def show_session(request, id):
    return json(response_wrapper.error(2003), status=403)


@helpers.login_required
async def delete_session(request, id=None):
    if id is not None:
        return json(response_wrapper.error(2003), status=403)

    return text("", status=204)
