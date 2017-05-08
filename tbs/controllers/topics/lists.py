"""
The Bestory Project
"""

from sanic.response import json


def latest(request, slug):
    return json({'hello': 'world'})


def hot(request, slug):
    return json({'hello': 'world'})


def top(request, slug):
    return json({'hello': 'world'})


def random(request, slug):
    return json({'hello': 'world'})
