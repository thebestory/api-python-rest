"""
The Bestory Project
"""

from sanic.response import json


def index(request, story_id):
    return json({'hello': 'world'})


def create(request, story_id, id=None):
    return json({'hello': 'world'})


def show(request, story_id, id):
    return json({'hello': 'world'})


def update(request, story_id, id):
    return json({'hello': 'world'})


def delete(request, story_id, id):
    return json({'hello': 'world'})
