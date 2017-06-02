"""
The Bestory Project
"""

from sanic.response import json


async def create_story(request):
    return json({"hello": "world"})


async def show_story(request, id):
    return json({"hello": "world"})


async def update_story(request, id):
    return json({"hello": "world"})


async def delete_story(request, id):
    return json({"hello": "world"})


async def list_story_reactions(request, story_id):
    return json({"hello": "world"})


async def create_story_reaction(request, story_id):
    return json({"hello": "world"})


async def delete_story_reaction(request, story_id):
    return json({"hello": "world"})


async def list_story_comments(request, story_id):
    return json({"hello": "world"})


async def create_story_comment(request, story_id):
    return json({"hello": "world"})


async def show_story_comment(request, story_id, id):
    return json({"hello": "world"})


async def update_story_comment(request, story_id, id):
    return json({"hello": "world"})


async def delete_story_comment(request, story_id, id):
    return json({"hello": "world"})


async def list_story_comment_reactions(request, story_id, comment_id):
    return json({"hello": "world"})


async def create_story_comment_reaction(request, story_id, comment_id):
    return json({"hello": "world"})


async def delete_story_comment_reaction(request, story_id, comment_id):
    return json({"hello": "world"})
