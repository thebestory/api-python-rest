"""
The Bestory Project
"""

from sanic.response import json


def create(request):
    return json({'hello': 'world'})


def show(request, username):
    return json({'hello': 'world'})


def update(request, username):
    return json({'hello': 'world'})
