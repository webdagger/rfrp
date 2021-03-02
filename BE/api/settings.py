from starlette.config import Config
import sentry_sdk

config = Config('.env')

DEBUG = config("DEBUG", cast=bool, default=False)
HTTPS_ONLY = config("HTTPS_ONLY", cast=bool, default=False)
SECRET = config("SECRET_KEY", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default="mongodb://mongodb0.example.com:27017",
)



# The Sentry DSN is a unique identifier for our app when connecting to Sentry
# See https://docs.sentry.io/platforms/python/#connecting-the-sdk-to-sentry
SENTRY_DSN = config("SENTRY_DSN", cast=str, default="")



RELEASE_VERSION = config("RELEASE_VERSION", cast=str, default="<local dev>")


if SENTRY_DSN:  # pragma: nocover
    sentry_sdk.init(dsn=SENTRY_DSN, release=RELEASE_VERSION, traces_sample_rate=1.0)