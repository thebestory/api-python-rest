"""
The Bestory Project
"""

from sanic.response import json


def show(request, id):
    return json({'hello': 'world'})


def create(request, id):
    return json({'hello': 'world'})


def delete(request, id):
    return json({'hello': 'world'})
