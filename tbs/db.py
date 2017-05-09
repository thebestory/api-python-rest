"""
The Bestory Project
"""

import asyncpgsa

from tbs.config import db


pool: asyncpgsa.pool.SAPool


async def before_start_listener(app, loop):
    global pool

    pool = await asyncpgsa.create_pool(
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
