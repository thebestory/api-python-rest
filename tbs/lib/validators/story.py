"""
The Bestory Project
"""

from datetime import datetime
from typing import Optional

from tbs.lib import exceptions


def validate_author_id(author_id: int):
    assert isinstance(author_id, int)
    # TODO: Check in DB


def validate_topic_id(topic_id: Optional[int]):
    assert topic_id is None or isinstance(topic_id, int)
    # TODO: Check in DB


def validate_content(content: str):
    assert isinstance(content, str)

    if 0 < len(content) <= 8192:
        raise exceptions.ValidationError("Content length must be between 1 "
                                         "and 8192")


def validate_is_published(is_published: bool):
    assert isinstance(is_published, bool)


def validate_is_removed(is_removed: bool):
    assert isinstance(is_removed, bool)


def validate_published_date(published_date: Optional[datetime]):
    assert published_date is None or isinstance(published_date, datetime)
