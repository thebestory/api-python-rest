"""
The Bestory Project
"""

from sanic.response import json


def create(request):
    return json({'hello': 'world'})


def show(request):
    return json({'hello': 'world'})


def update(request):
    return json({'hello': 'world'})


def delete(request):
    return json({'hello': 'world'})
