"""
The Bestory Project
"""

import asyncpg
from asyncpg.pool import Pool

from tbs.config import db as config
from tbs.lib import seed


pool: Pool


async def connect_database(app, loop):
    global pool

    pool = await asyncpg.create_pool(
        host=config.HOST,
        port=config.PORT,
        user=config.USER,
        password=config.PASSWORD,
        database=config.DATABASE,
        min_size=config.POOL_MIN_SIZE,
        max_size=config.POOL_MAX_SIZE,
        max_queries=config.MAX_QUERIES,
        max_inactive_connection_lifetime=config.MAX_INACTIVE_CONNECTION_LIFETIME,
        loop=loop
    )


async def seed_database(app, loop):
    if config.SEED:
        async with pool.acquire() as conn:
            async with conn.transaction() as conn:
                seed.insert(conn)


async def before_start_listener(app, loop):
    await connect_database(app, loop)
    await seed_database(app, loop)


async def after_stop_listener(app, loop):
    await pool.close()
