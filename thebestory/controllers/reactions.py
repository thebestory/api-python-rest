"""
The Bestory Project
"""

from sanic.response import json


def show(request):
    return json({'hello': 'world'})


def create(request):
    return json({'hello': 'world'})


def delete(request):
    return json({'hello': 'world'})
