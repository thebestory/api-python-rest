"""
The Bestory Project
"""

from typing import Iterator

from tbs.lib import snowflake


generator: Iterator[int]


async def before_start_listener(app, loop):
    global generator
    generator = snowflake.generator()


def generate() -> int:
    return next(generator)
