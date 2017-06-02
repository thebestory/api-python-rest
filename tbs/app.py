"""
The Bestory Project
"""

from sanic import Sanic

from tbs.config import endpoints
from tbs.config import listeners


instance = Sanic()


async def invoke_listeners(app, loop, _listeners):
    for listener in _listeners:
        await listener(app, loop)


def add_routes(app):
    for endpoint in endpoints.root:
        app.add_route(
            endpoint["handler"],
            endpoint["path"],
            endpoint.get("methods", ["GET"])
        )


@instance.listener("before_server_start")
async def before_start(app, loop):
    await invoke_listeners(app, loop, listeners.before_start)


@instance.listener("after_server_start")
async def after_start(app, loop):
    await invoke_listeners(app, loop, listeners.after_start)


@instance.listener("before_server_stop")
async def before_stop(app, loop):
    await invoke_listeners(app, loop, listeners.before_stop)


@instance.listener("after_server_stop")
async def after_stop(app, loop):
    await invoke_listeners(app, loop, listeners.after_stop)


add_routes(instance)
