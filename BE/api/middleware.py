from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import settings
import ssl
from mongoengine import connect


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.db = connect('rfrp', host=settings.DATABASE_URL)
        response = await call_next(request)
        return response



middleware = []

if settings.SENTRY_DSN:  # pragma: nocover
    middleware += [Middleware(SentryAsgiMiddleware)]

if settings.HTTPS_ONLY:  # pragma: nocover
    middleware += [Middleware(HTTPSRedirectMiddleware)]

middleware += [
    Middleware(SessionMiddleware, secret_key=settings.SECRET, https_only=settings.HTTPS_ONLY)
]

middleware += [
  Middleware(DatabaseMiddleware)
]