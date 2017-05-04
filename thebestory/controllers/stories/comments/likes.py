"""
The Bestory Project
"""

from sanic.response import json


def show(request, story_id, comment_id):
    return json({'hello': 'world'})


def create(request, story_id, comment_id):
    return json({'hello': 'world'})


def delete(request, story_id, comment_id):
    return json({'hello': 'world'})
