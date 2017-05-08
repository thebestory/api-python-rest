"""
The Bestory Project
"""

from sanic import Sanic

from tbs import config


app = Sanic()


async def invoke_listeners(app, loop, listeners):
    for listener in listeners:
        await listener(app, loop)


def add_routes(app):
    for endpoint in config.endpoints.root:
        app.add_route(
            endpoint['handler'],
            endpoint['path'],
            endpoint.get('methods', ['GET'])
        )


@app.listener('before_server_start')
async def before_start(app, loop):
    await invoke_listeners(app, loop, config.listeners.before_start)


@app.listener('after_server_start')
async def after_start(app, loop):
    await invoke_listeners(app, loop, config.listeners.after_start)


@app.listener('before_server_stop')
async def before_stop(app, loop):
    await invoke_listeners(app, loop, config.listeners.before_stop)


@app.listener('after_server_stop')
async def after_stop(app, loop):
    await invoke_listeners(app, loop, config.listeners.after_stop)


add_routes(app)
