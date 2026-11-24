from workers import asgi

from pingri.api.app import app

Default = asgi.entrypoint(app)
