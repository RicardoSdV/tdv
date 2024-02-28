import falcon


class PingResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = "Pong"


# Create the Falcon application
app = falcon.App()

# Instantiate the PingResource class
ping_resource = PingResource()

# Add the ping route to the application
app.add_route('/ping', ping_resource)


# Optional: Add a default route to handle undefined routes
class DefaultResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_404  # Not Found
        resp.body = "Not Found"


# Instantiate the DefaultResource class
default_resource = DefaultResource()

# Add the default route to the application
app.add_route('/', default_resource)


# Entry point for Gunicorn to serve the Falcon app
def create_app():
    return app


# For running with Gunicorn
if __name__ == '__main__':
    import os

    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 8000))
    workers = 1

    bind_address = f'{host}:{port}'
    print(f'Starting server on {bind_address} with {workers} workers.')

    # Use Gunicorn to serve the Falcon app
    from gunicorn.app.base import BaseApplication


    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application


    options = {
        'bind': bind_address,
        'workers': workers,
        'accesslog': '-',
        'errorlog': '-',
        'worker_class': 'gevent'
    }

    StandaloneApplication(app, options).run()
