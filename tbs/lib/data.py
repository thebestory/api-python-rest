"""
The Bestory Project
"""

from typing import List

import sqlalchemy as sa
from asyncpg.protocol import Record

from tbs.lib import schema


def parse(table: sa.Table, record: Record):
    """
    Parses an object into dict from asyncpg.Record.
    """
    object = {column.key: None for column in table.columns}

    for key in object:
        if key in record:
            object[key] = record[key]

    return object


def parse_snowflake(record: Record):
    """
    Parses a Snowflake ID into dict from asyncpg.Record.
    """
    return parse(schema.snowflakes, record)


def parse_snowflakes(records: List[Record]):
    """
    Parses a Snowflake IDs into dict from asyncpg.Record.
    """
    return [parse_snowflake(record) for record in records]


def parse_user(record: Record):
    """
    Parses a user into dict from asyncpg.Record.
    """
    return parse(schema.users, record)


def parse_users(records: List[Record]):
    """
    Parses a users into dict from asyncpg.Record.
    """
    return [parse_user(record) for record in records]


def parse_topic(record: Record):
    """
    Parses a topic into dict from asyncpg.Record.
    """
    return parse(schema.topics, record)


def parse_topics(records: List[Record]):
    """
    Parses a topics into dict from asyncpg.Record.
    """
    return [parse_topic(record) for record in records]


def parse_comment(record: Record):
    """
    Parses a comment into dict from asyncpg.Record.
    """
    return parse(schema.comments, record)


def parse_comments(records: List[Record]):
    """
    Parses a comments into dict from asyncpg.Record.
    """
    return [parse_comment(record) for record in records]


def parse_reaction(record: Record):
    """
    Parses a reaction into dict from asyncpg.Record.
    """
    return parse(schema.reactions, record)


def parse_reactions(records: List[Record]):
    """
    Parses a reactions into dict from asyncpg.Record.
    """
    return [parse_reaction(record) for record in records]


def parse_story(record: Record):
    """
    Parses a story into dict from asyncpg.Record.
    """
    return parse(schema.stories, record)


def parse_stories(records: List[Record]):
    """
    Parses a stories into dict from asyncpg.Record.
    """
    return [parse_story(record) for record in records]
