"""
The Bestory Project
"""

from sanic.response import json


def list_sessions(request):
    return json({'hello': 'world'})


def create_session(request):
    return json({'hello': 'world'})


def show_session(request, id):
    return json({'hello': 'world'})


def delete_session(request):
    return json({'hello': 'world'})
