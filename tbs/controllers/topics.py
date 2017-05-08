"""
The Bestory Project
"""

from sanic.response import json


def list_topics(request):
    return json({'hello': 'world'})


def create_topic(request):
    return json({'hello': 'world'})


def show_topic(request, slug):
    return json({'hello': 'world'})


def update_topic(request, slug):
    return json({'hello': 'world'})


def delete_topic(request, slug):
    return json({'hello': 'world'})


def list_topic_latest_stories(request, slug):
    return json({'hello': 'world'})


def list_topic_hot_stories(request, slug):
    return json({'hello': 'world'})


def list_topic_top_stories(request, slug):
    return json({'hello': 'world'})


def list_topic_random_stories(request, slug):
    return json({'hello': 'world'})
