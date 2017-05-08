"""
The Bestory Project
"""

from sanic import Sanic

from tbs.config import endpoints
from tbs.config import listeners


app = Sanic()


async def invoke_listeners(app, loop, _listeners):
    for listener in _listeners:
        await listener(app, loop)


def add_routes(app):
    for endpoint in endpoints.root:
        app.add_route(
            endpoint['handler'],
            endpoint['path'],
            endpoint.get('methods', ['GET'])
        )


@app.listener('before_server_start')
async def before_start(app, loop):
    await invoke_listeners(app, loop, listeners.before_start)


@app.listener('after_server_start')
async def after_start(app, loop):
    await invoke_listeners(app, loop, listeners.after_start)


@app.listener('before_server_stop')
async def before_stop(app, loop):
    await invoke_listeners(app, loop, listeners.before_stop)


@app.listener('after_server_stop')
async def after_stop(app, loop):
    await invoke_listeners(app, loop, listeners.after_stop)


add_routes(app)
