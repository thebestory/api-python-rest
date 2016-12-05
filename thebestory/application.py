"""
The Bestory Project
"""

import asyncio
import asyncpgsa
from aiohttp import web
from asyncpg.pool import Pool

from thebestory import config


class Application:
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._app = web.Application(loop=self._loop)

        self._db = None

        self._controllers = {}

        self._config()

    async def _on_startup(self):
        self._db = await asyncpgsa.create_pool(
            host=config.db.HOST,
            port=config.db.PORT,
            user=config.db.USER,
            password=config.db.PASSWORD,
            database=config.db.DATABASE,
            loop=self._loop,
            min_size=config.db.POOL_MIN_SIZE,
            max_size=config.db.POOL_MAX_SIZE,
        )

    async def _on_shutdown(self):
        pass

    async def _on_cleanup(self):
        pass

    def _config(self):
        self._config_mw()
        self._config_routes()

        from thebestory.app.lib import patch
        from asyncpgsa.connection import SAConnection
        SAConnection.fetchrow = patch.asyncpgsa.fetchrow

    def _config_mw(self):
        """Adds middlewares to the application instance"""

        async def middleware_db(app, handler):
            async def bind_db(request: web.Request):
                request.db = self.db
                return await handler(request)

            return bind_db

        self._app.middlewares.extend(config.MW)
        self._app.middlewares.append(middleware_db)

    def _config_routes(self):
        """Adds routes to the application instance"""

        for route in config.ROUTES:
            if route.get("method"):
                if route["controller"] not in self._controllers:
                    self._controllers[route["controller"]] = route["controller"]()

                action = getattr(
                    self._controllers[route["controller"]],
                    route["action"],
                )

                self._app.router.add_route(
                    route["method"],
                    route["path"],
                    action,
                )
            else:
                self._app.router.add_route(
                    "*",
                    route["path"],
                    route["controller"]
                )

    @property
    def db(self) -> asyncpgsa.pool.SAPool:
        return self._db

    def run(self):
        """Runs the server"""

        handler = self._app.make_handler()
        server = self._loop.run_until_complete(
            self._loop.create_server(
                handler,
                config.app.HOST,
                config.app.PORT,
                ssl=config.app.SSL
            )
        )

        self._loop.run_until_complete(self._on_startup())

        print("Serving on", server.sockets[0].getsockname(), "...")

        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            print("Stopping server", "...")
        finally:
            server.close()
            self._loop.run_until_complete(server.wait_closed())
            self._loop.run_until_complete(self._on_shutdown())
            self._loop.run_until_complete(
                handler.finish_connections(config.app.FINISH_TIMEOUT))
            self._loop.run_until_complete(self._on_cleanup())
            self._loop.close()


app = Application()
