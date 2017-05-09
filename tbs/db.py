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
        max_queries=db.MAX_QUERIES,
        max_inactive_connection_lifetime=db.MAX_INACTIVE_CONNECTION_LIFETIME,
        loop=loop
    )


async def after_stop_listener(app, loop):
    await pool.close()
