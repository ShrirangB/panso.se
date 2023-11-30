from __future__ import annotations

import os
from pathlib import Path

import sentry_sdk
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), verbose=True)

sentry_dsn: str = os.getenv(key="SENTRY_DSN", default="")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


BASE_DIR: Path = Path(__file__).resolve().parent.parent
SECRET_KEY: str = os.getenv("SECRET_KEY", default="")
DEBUG: bool = os.getenv(key="DEBUG", default="True").lower() == "true"
ADMINS: list[tuple[str, str]] = [("Joakim Hellsén", "django@panso.se")]
BOT_IP_LIST: list[str] = [os.getenv(key="BOT_IP", default="")]
ALLOWED_HOSTS: list[str] = [".panso.se", ".localhost", "127.0.0.1", "::1"]

TIME_ZONE = "Europe/Stockholm"
USE_TZ = True
USE_I18N = False
LANGUAGE_CODE = "en-us"
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = " "
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER: str = os.getenv(key="EMAIL_HOST_USER", default="webmaster@localhost")
EMAIL_HOST_PASSWORD: str = os.getenv(key="EMAIL_HOST_PASSWORD", default="")
EMAIL_SUBJECT_PREFIX = "[Panso] "
EMAIL_USE_LOCALTIME = True
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL: str = os.getenv(key="EMAIL_HOST_USER", default="webmaster@localhost")
SERVER_EMAIL: str = os.getenv(key="EMAIL_HOST_USER", default="webmaster@localhost")
USE_X_FORWARDED_HOST = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
ROOT_URLCONF = "api.urls"
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SIMPLE_HISTORY_REVERT_DISABLED = True
WSGI_APPLICATION = "api.wsgi.application"
INTERNAL_IPS: list[str] = ["127.0.0.1", "localhost"]
if BOT_IP_LIST:
    INTERNAL_IPS.extend(BOT_IP_LIST)

INSTALLED_APPS: list[str] = [
    # First party
    "webhallen.apps.WebhallenConfig",
    # Third party
    "simple_history",  # https://github.com/jazzband/django-simple-history
    # Django
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

DATABASE_URL: str = os.getenv(key="DATABASE_URL", default=str(Path(BASE_DIR / "db.sqlite3")))
DATABASES: dict[str, dict[str, str]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_URL,
    },
}
