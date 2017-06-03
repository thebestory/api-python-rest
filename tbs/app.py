"""
The Bestory Project
"""

from sanic import Sanic
from sanic.response import json

from tbs.config import (
    endpoints,
    listeners,
    middleware
)
from tbs.lib import response_wrapper


instance = Sanic()


def add_listeners(type: str):
    st = "_server_".join(type.split("_"))

    for listener in listeners.all[type]:
        @instance.listener(st)
        async def listener_wrapper(app, loop):
            return await listener(app, loop)


def add_middleware(type: str):
    for mw in middleware.all[type]:
        if type == "request":
            @instance.middleware(type)
            async def middleware_wrapper(request):
                    return await mw(request)
        else:
            @instance.middleware(type)
            async def middleware_wrapper(request, response):
                    return await mw(request, response)


def add_routes(app):
    for endpoint in endpoints.root:
        app.add_route(
            endpoint["handler"],
            endpoint["path"],
            endpoint.get("methods", ["GET"])
        )


# @instance.exception(Exception)
# def server_error(request, exception):
#     return json(response_wrapper.error(1001), status=500)


add_listeners("before_start")
add_listeners("after_start")
add_listeners("before_stop")
add_listeners("after_stop")

add_middleware("request")
add_middleware("response")

add_routes(instance)
