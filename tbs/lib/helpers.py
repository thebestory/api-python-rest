"""
The Bestory Project
"""

from sanic.response import json

from tbs.lib import response_wrapper


def login_required(handler):
    async def wrapper(request, **kwargs):
        if request["session"] is None:
            return json(response_wrapper.error(2002), status=401)
        else:
            return await handler(request, **kwargs)

    return wrapper
