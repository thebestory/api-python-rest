"""
The Bestory Project
"""

from typing import Iterator


generator: Iterator[int]


async def before_start_listener(app, loop):
    global generator
    from tbs.lib import snowflake

    generator = snowflake.generator()


def generate() -> int:
    return next(generator)
