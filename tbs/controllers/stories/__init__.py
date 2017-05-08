"""
The Bestory Project
"""

from sanic.response import json

from tbs.controllers.stories import comments, likes


def create(request):
    return json({'hello': 'world'})


def show(request, id):
    return json({'hello': 'world'})


def update(request, id):
    return json({'hello': 'world'})


def delete(request, id):
    return json({'hello': 'world'})
