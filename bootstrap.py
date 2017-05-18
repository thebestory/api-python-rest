"""
The Bestory Project
"""

import os
import urllib.parse

from tbs import app
from tbs.config import app as app_config
from tbs.config import db as db_config
from tbs.config import snowflake as snowflake_config


if __name__ == '__main__':
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    db = os.environ.get("DATABASE_URL")
    machine_id = os.environ.get("MACHINE_ID")
    seed = os.environ.get("SEED")

    if host is not None:
        app_config.HOST = host

    if port is not None:
        app_config.PORT = int(port)

    if seed is not None:
        db_config.seed = False

    if db is None:
        raise ValueError("Database URL must be provided by the environment")

    if machine_id is None:
        raise ValueError("Machine ID must be provided by the environment")

    snowflake_config.MACHINE_ID = int(machine_id)

    db = urllib.parse.urlparse(db)

    db_config.HOST = db.hostname
    db_config.PORT = int(db.port)
    db_config.USER = db.username
    db_config.PASSWORD = db.password
    db_config.DATABASE = db.path[1:]

    app.instance.run(
        host=app_config.HOST,
        port=app_config.PORT,
        debug=app_config.DEBUG,
        ssl=app_config.SSL,
        sock=app_config.SOCK,
        workers=app_config.WORKERS
    )
