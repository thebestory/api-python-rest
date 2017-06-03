"""
The Bestory Project
"""

from typing import List

import sqlalchemy as sa
from asyncpg.protocol import Record

from tbs.lib import schema


def parse(table: sa.Table, record: Record, prefix=""):
    """
    Parses an object into dict from asyncpg.Record.
    """
    object = {column.key: None for column in table.columns}

    for key in object:
        if key in record:
            object[key] = record[prefix + key]

    return object


def parse_snowflake(record: Record, prefix=""):
    """
    Parses a Snowflake ID into dict from asyncpg.Record.
    """
    return parse(schema.snowflakes, record, prefix)


def parse_snowflakes(records: List[Record], prefix=""):
    """
    Parses a Snowflake IDs into dict from asyncpg.Record.
    """
    return [parse_snowflake(record, prefix) for record in records]


def parse_user(record: Record, prefix=""):
    """
    Parses a user into dict from asyncpg.Record.
    """
    return parse(schema.users, record, prefix)


def parse_users(records: List[Record], prefix=""):
    """
    Parses a users into dict from asyncpg.Record.
    """
    return [parse_user(record, prefix) for record in records]


def parse_topic(record: Record, prefix=""):
    """
    Parses a topic into dict from asyncpg.Record.
    """
    return parse(schema.topics, record, prefix)


def parse_topics(records: List[Record], prefix=""):
    """
    Parses a topics into dict from asyncpg.Record.
    """
    return [parse_topic(record, prefix) for record in records]


def parse_comment(record: Record, prefix=""):
    """
    Parses a comment into dict from asyncpg.Record.
    """
    return parse(schema.comments, record, prefix)


def parse_comments(records: List[Record], prefix=""):
    """
    Parses a comments into dict from asyncpg.Record.
    """
    return [parse_comment(record, prefix) for record in records]


def parse_reaction(record: Record, prefix=""):
    """
    Parses a reaction into dict from asyncpg.Record.
    """
    return parse(schema.reactions, record, prefix)


def parse_reactions(records: List[Record], prefix=""):
    """
    Parses a reactions into dict from asyncpg.Record.
    """
    return [parse_reaction(record, prefix) for record in records]


def parse_story(record: Record, prefix=""):
    """
    Parses a story into dict from asyncpg.Record.
    """
    return parse(schema.stories, record, prefix)


def parse_stories(records: List[Record], prefix=""):
    """
    Parses a stories into dict from asyncpg.Record.
    """
    return [parse_story(record, prefix) for record in records]
