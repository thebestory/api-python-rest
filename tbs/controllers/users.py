"""
The Bestory Project
"""

from sanic.response import json


def create_user(request):
    return json({'hello': 'world'})


def show_user(request, username):
    return json({'hello': 'world'})


def update_user(request, username):
    return json({'hello': 'world'})
