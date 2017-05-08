"""
The Bestory Project
"""

from sanic.response import json


def create_story(request):
    return json({'hello': 'world'})


def show_story(request, id):
    return json({'hello': 'world'})


def update_story(request, id):
    return json({'hello': 'world'})


def delete_story(request, id):
    return json({'hello': 'world'})


def list_story_likes(request, story_id):
    return json({'hello': 'world'})


def create_story_like(request, story_id):
    return json({'hello': 'world'})


def delete_story_like(request, story_id):
    return json({'hello': 'world'})


def list_story_comments(request, story_id):
    return json({'hello': 'world'})


def create_story_comment(request, story_id, id=None):
    return json({'hello': 'world'})


def show_story_comment(request, story_id, id):
    return json({'hello': 'world'})


def update_story_comment(request, story_id, id):
    return json({'hello': 'world'})


def delete_story_comment(request, story_id, id):
    return json({'hello': 'world'})


def list_story_comment_likes(request, story_id, comment_id):
    return json({'hello': 'world'})


def create_story_comment_like(request, story_id, comment_id):
    return json({'hello': 'world'})


def delete_story_comment_like(request, story_id, comment_id):
    return json({'hello': 'world'})
