"""
The Bestory Project
"""

import asyncpg

from tbs.config import db


pool: asyncpg.pool.Pool


async def before_start_listener(app, loop):
    global pool

    pool = await asyncpg.create_pool(
        host=db.HOST,
        port=db.PORT,
        user=db.USER,
        password=db.PASSWORD,
        database=db.DATABASE,
        min_size=db.POOL_MIN_SIZE,
        max_size=db.POOL_MAX_SIZE,
        loop=loop
    )


async def after_stop_listener(app, loop):
    await pool.close()