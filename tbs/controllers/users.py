"""
The Bestory Project
"""

from sanic.response import json


async def create_user(request):
    return json({'hello': 'world'})


async def show_user(request, id):
    return json({'hello': 'world'})


async def update_user(request, id):
    return json({'hello': 'world'})
