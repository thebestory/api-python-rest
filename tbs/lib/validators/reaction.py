"""
The Bestory Project
"""

from tbs.lib import exceptions


def validate_user_id(user_id: int):
    assert isinstance(user_id, int)
    # TODO: Check in DB


def validate_object_id(object_id: int):
    assert isinstance(object_id, int)
    # TODO: Check in DB


def validate_reaction_id(reaction_id: int):
    assert isinstance(reaction_id, int)
    # TODO: Check in DB
