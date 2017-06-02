"""
The Bestory Project
"""

from sanic.response import json


async def list_sessions(request):
    return json({"hello": "world"})


async def create_session(request):
    return json({"hello": "world"})


async def show_session(request, id):
    return json({"hello": "world"})


async def delete_session(request, id=None):
    return json({"hello": "world"})
