"""
The Bestory Project
"""

import os
import urllib.parse

from sanic import Sanic

from thebestory import config


app = Sanic()


async def invoke_listeners(app, loop, listeners):
    for listener in listeners:
        await listener(app, loop)


def setup_env(app):
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    db = os.environ.get("DATABASE_URL")

    if host is not None:
        config.app.HOST = host

    if port is not None:
        config.app.PORT = port

    if db is None:
        raise ValueError("Database URL must be provided by the environment")

    db = urllib.parse.urlparse(db)

    config.db.HOST = db.hostname
    config.db.PORT = db.port
    config.db.USER = db.username
    config.db.PASSWORD = db.password
    config.db.DATABASE = db.path[1:]


def add_routes(app):
    for endpoint in config.endpoints.root:
        app.add_route(
            endpoint['handler'],
            endpoint['path'],
            endpoint.get('methods', ['GET'])
        )


@app.listener('before_server_start')
async def before_start(app, loop):
    invoke_listeners(app, loop, config.listeners.before_start)


@app.listener('after_server_start')
async def after_start(app, loop):
    invoke_listeners(app, loop, config.listeners.after_start)


@app.listener('before_server_stop')
async def before_stop(app, loop):
    invoke_listeners(app, loop, config.listeners.before_stop)


@app.listener('after_server_stop')
async def after_stop(app, loop):
    invoke_listeners(app, loop, config.listeners.after_stop)


def main(app):
    setup_env(app)
    add_routes(app)


main(app)


if __name__ == '__main__':
    app.run(
        host=config.app.HOST,
        port=config.app.PORT,
        debug=config.app.DEBUG,
        ssl=config.app.SSL,
        sock=config.app.SOCK,
        workers=config.app.WORKERS,
        loop=config.app.LOOP
    )
