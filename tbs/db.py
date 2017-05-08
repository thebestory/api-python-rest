"""
The Bestory Project
"""

import asyncpg


pool: asyncpg.pool.Pool


async def before_start_listener(app, loop):
    global pool
    from tbs import config

    pool = await asyncpg.create_pool(
        host=config.db.HOST,
        port=config.db.PORT,
        user=config.db.USER,
        password=config.db.PASSWORD,
        database=config.db.DATABASE,
        min_size=config.db.POOL_MIN_SIZE,
        max_size=config.db.POOL_MAX_SIZE,
        loop=loop
    )


async def after_stop_listener(app, loop):
    pool.close()
