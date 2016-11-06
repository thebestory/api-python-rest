"""
The Bestory
thebestory.application
"""

from aiohttp import web
from thebestory import config


class Application:
    def __init__(self):
        self._controllers = {}
        self._websockets = []
        self._app = web.Application()

        self._config_app()
        self._config_routes()

    async def on_startup(self, app):
        pass

    async def on_shutdown(self, app):
        pass

    async def on_cleanup(self, app):
        pass

    def _config_app(self):
        """Adds handlers on the main events of application"""

        self._app.on_startup.append(self.on_startup)
        self._app.on_shutdown.append(self.on_shutdown)
        self._app.on_cleanup.append(self.on_cleanup)

    def _config_routes(self):
        """Adds routes to the application instance"""

        for route in config.routes.ROUTES:
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

    def run(self):
        web.run_app(self._app)


Application().run()
