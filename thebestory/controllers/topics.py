"""
The Bestory Project
"""

from sanic.response import json


def index(request):
    return json({'hello': 'world'})


def create(request):
    return json({'hello': 'world'})


def show(request, slug):
    return json({'hello': 'world'})


def update(request, slug):
    return json({'hello': 'world'})


def delete(request, slug):
    return json({'hello': 'world'})
