"""
The Bestory Project
"""

import os
import urllib.parse

from tbs import config
from tbs.application import app


if __name__ == '__main__':
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    db = os.environ.get("DATABASE_URL")
    machine_id = os.environ.get("MACHINE_ID")

    if host is not None:
        config.app.HOST = host

    if port is not None:
        config.app.PORT = port

    if db is None:
        raise ValueError("Database URL must be provided by the environment")

    if machine_id is None:
        raise ValueError("Machine ID must be provided by the environment")

    config.snowflake.MACHINE_ID = machine_id

    db = urllib.parse.urlparse(db)

    config.db.HOST = db.hostname
    config.db.PORT = db.port
    config.db.USER = db.username
    config.db.PASSWORD = db.password
    config.db.DATABASE = db.path[1:]

    app.run(
        host=config.app.HOST,
        port=config.app.PORT,
        debug=config.app.DEBUG,
        ssl=config.app.SSL,
        sock=config.app.SOCK,
        workers=config.app.WORKERS,
        loop=config.app.LOOP
    )
