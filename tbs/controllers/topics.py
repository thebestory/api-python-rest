"""
The Bestory Project
"""

from sanic.response import json


async def list_topics(request):
    return json({"hello": "world"})


async def create_topic(request):
    return json({"hello": "world"})


async def show_topic(request, id):
    return json({"hello": "world"})


async def update_topic(request, id):
    return json({"hello": "world"})


async def delete_topic(request, id):
    return json({"hello": "world"})


async def list_topic_latest_stories(request, id):
    return json({"hello": "world"})


async def list_topic_hot_stories(request, id):
    return json({"hello": "world"})


async def list_topic_top_stories(request, id):
    return json({"hello": "world"})


async def list_topic_random_stories(request, id):
    return json({"hello": "world"})
