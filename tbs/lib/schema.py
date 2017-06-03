"""
The Bestory Project
"""

from datetime import datetime

import pendulum
import sqlalchemy as sa


__metadata = sa.MetaData()


class DateTime(sa.TypeDecorator):
    """
    Implements a type with explicit requirement to set timezones.
    Before saving to a database, converts it to the UTC timezone.
    After retrieving from a database, has the UTC timezone.
    """
    impl = sa.DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not isinstance(value, datetime):
                raise TypeError("Expected datetime.datetime, not " +
                                repr(value))
            elif value.tzinfo is None:
                raise ValueError("Naive datetime is disallowed")
            return value.astimezone(pendulum.UTC)

    def process_result_value(self, value, dialect):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=pendulum.UTC)
        return value


snowflakes = sa.Table(
    "snowflakes",
    __metadata,

    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("type", sa.String(32), index=True, nullable=False)
)

users = sa.Table(
    "users",
    __metadata,

    sa.Column("id", sa.BigInteger, primary_key=True),

    sa.Column("username", sa.String(32), unique=True, nullable=False),
    sa.Column("email", sa.String(255), unique=True, nullable=False),
    sa.Column("password", sa.String(255), nullable=False),

    sa.Column("comments_count", sa.Integer, default=0, nullable=False),
    sa.Column("comment_reactions_count", sa.Integer, default=0,
              nullable=False),
    sa.Column("story_reactions_count", sa.Integer, default=0, nullable=False),
    sa.Column("stories_count", sa.Integer, default=0, nullable=False),

    sa.Column("registered_date", DateTime,
              default=lambda: datetime.utcnow().replace(tzinfo=pendulum.UTC),
              nullable=False)
)

topics = sa.Table(
    "topics",
    __metadata,

    sa.Column("id", sa.BigInteger, primary_key=True),

    sa.Column("title", sa.String(64), nullable=False),
    sa.Column("slug", sa.String(32), unique=True, nullable=False),

    sa.Column("description", sa.Text, nullable=False),
    sa.Column("icon", sa.String(16), nullable=False),

    sa.Column("stories_count", sa.Integer, default=0, nullable=False),

    sa.Column("is_active", sa.Boolean, default=False, nullable=False)
)

comments = sa.Table(
    "comments",
    __metadata,

    sa.Column("id", sa.BigInteger, primary_key=True),

    sa.Column("author_id", sa.BigInteger, index=True, nullable=False),
    sa.Column("story_id", sa.BigInteger, index=True, nullable=False),

    sa.Column("content", sa.Text(4096), nullable=False),

    sa.Column("reactions_count", sa.Integer, default=0, nullable=False),

    sa.Column("is_removed", sa.Boolean, default=False, nullable=False),

    sa.Column("submitted_date", DateTime,
              default=lambda: datetime.utcnow().replace(tzinfo=pendulum.UTC),
              nullable=False),
    sa.Column("edited_date", DateTime, nullable=True)
)

reactions = sa.Table(
    "reactions",
    __metadata,

    sa.Column("user_id", sa.BigInteger, index=True, nullable=False),
    sa.Column("object_id", sa.BigInteger, index=True, nullable=False),
    sa.Column("reaction_id", sa.BigInteger, index=True, nullable=False),

    sa.Column("is_removed", sa.Boolean, nullable=False),

    sa.Column("submitted_date", DateTime,
              default=lambda: datetime.utcnow().replace(tzinfo=pendulum.UTC),
              nullable=False)
)

stories = sa.Table(
    "stories",
    __metadata,

    sa.Column("id", sa.BigInteger, primary_key=True),

    sa.Column("author_id", sa.BigInteger, index=True, nullable=False),
    sa.Column("topic_id", sa.BigInteger, index=True, nullable=True),

    sa.Column("content", sa.Text(8192), nullable=False),

    sa.Column("comments_count", sa.Integer, default=0, nullable=False),
    sa.Column("reactions_count", sa.Integer, default=0, nullable=False),

    sa.Column("is_published", sa.Boolean, default=False, nullable=False),
    sa.Column("is_removed", sa.Boolean, default=False, nullable=False),

    sa.Column("submitted_date", DateTime,
              default=lambda: datetime.utcnow().replace(tzinfo=pendulum.UTC),
              nullable=False),
    sa.Column("published_date", DateTime, nullable=True),
    sa.Column("edited_date", DateTime, nullable=True)
)
