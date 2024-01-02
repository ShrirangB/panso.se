"""This file contains our Django settings that configuration our Django installation.

https://docs.djangoproject.com/en/5.0/topics/settings/
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(dotenv_path=find_dotenv(), verbose=True)

# Run Django in debug mode
DEBUG: bool = os.getenv(key="DEBUG", default="True").lower() == "true"

BASE_DIR: Path = Path(__file__).resolve().parent.parent

# The secret key is used for cryptographic signing, and should be set to a unique, unpredictable value.
SECRET_KEY: str = os.getenv("SECRET_KEY", default="")

# A list of all the people who get code error notifications. When DEBUG=False and a view raises an exception, Django
ADMINS: list[tuple[str, str]] = [("Joakim Hellsén", "django@panso.se")]

# A list of strings representing the host/domain names that this Django site can serve.
# .panso.se will match *.panso.se and panso.se
ALLOWED_HOSTS: list[str] = [".panso.se", ".localhost", "127.0.0.1"]

# The time zone that Django will use to display datetimes in templates and to interpret datetimes entered in forms
TIME_ZONE = "Europe/Stockholm"

# If datetimes will be timezone-aware by default. If True, Django will use timezone-aware datetimes internally.
USE_TZ = True

# Don't use Django's translation system
# TODO(TheLovinator): #20 We should probably make the site available in Swedish at some point.
# https://github.com/TheLovinator1/panso.se/issues/20
USE_I18N = False

# Decides which translation is served to all users.
LANGUAGE_CODE = "en-us"

# Default decimal separator used when formatting decimal numbers.
DECIMAL_SEPARATOR = ","

# Use a space as the thousand separator instead of a comma
THOUSAND_SEPARATOR = " "

# Use gmail for sending emails
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

# Use the X-Forwarded-Host header
USE_X_FORWARDED_HOST = True

# Set the Referrer Policy HTTP header on all responses that do not already have one.
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Full Python import path to our main URL configuration.
ROOT_URLCONF = "panso.urls"

# URL to use when referring to static files located in STATIC_ROOT.
# https://panso.se/static/...
STATIC_URL = "static/"

# Use a 64-bit integer as a primary key for models that don't have a field with primary_key=True.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Remove revert button from the admin
SIMPLE_HISTORY_REVERT_DISABLED = True

# A string representing the full Python import path to our WSGI application object
WSGI_APPLICATION = "panso.wsgi.application"

# Internal IPs that are allowed to see debug views
INTERNAL_IPS: list[str] = ["127.0.0.1", "localhost"]

# Applications include some combination of models, views, templates, template tags, static files, URLs, middleware, etc
INSTALLED_APPS: list[str] = [
    # First party
    "amd.apps.AmdConfig",
    "intel.apps.IntelConfig",
    "products.apps.ProductsConfig",
    "webhallen.apps.WebhallenConfig",
    # Third party
    "cacheops",  # https://github.com/Suor/django-cacheops
    "debug_toolbar",  # https://github.com/jazzband/django-debug-toolbar/
    "django_celery_results",  # https://github.com/celery/django-celery-results
    "django_filters",  # https://github.com/carltongibson/django-filter
    "simple_history",  # https://github.com/jazzband/django-simple-history
    "whitenoise.runserver_nostatic",  # https://whitenoise.readthedocs.io/en/latest/index.html
    # Django
    "django.contrib.admin",
    "django.contrib.sitemaps",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Middleware is a framework of hooks into Django's request/response processing.
MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# A dictionary containing the settings for how we should connect to our PostgreSQL database.
DATABASES: dict[str, dict[str, str]] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "panso",
        "USER": os.getenv(key="POSTGRES_USER", default=""),
        "PASSWORD": os.getenv(key="POSTGRES_PASSWORD", default=""),
        "HOST": os.getenv(key="POSTGRES_HOST", default=""),
        "PORT": os.getenv(key="POSTGRES_PORT", default="5432"),
    },
}

# A list containing the settings for all template engines to be used with Django.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

# Use Redis for caching
# TODO(TheLovinator): #21 Use a Unix socket instead of TCP/IP for Redis.  # noqa: TD003
# TODO(TheLovinator): #21 Disallow specific commands. See https://redis.io/docs/management/security/#disallowing-specific-commands
# https://github.com/TheLovinator1/panso.se/issues/21
REDIS_PASSWORD: str = os.getenv(key="REDIS_PASSWORD", default="")
REDIS_HOST: str = os.getenv(key="REDIS_HOST", default="")
CACHES: dict[str, dict[str, str]] = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379",
    },
}

# The absolute path to the directory where 'python manage.py collectstatic' will copy static files for deployment
# TODO(TheLovinator): #22 Should we store these on Cloudflare? Or at least in RAM to avoid disk I/O?
# https://github.com/TheLovinator1/panso.se/issues/22
STATIC_ROOT: Path = BASE_DIR / "staticfiles"
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"]

# Use WhiteNoise to serve static files. https://whitenoise.readthedocs.io/en/latest/django.html
STORAGES: dict[str, dict[str, str]] = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# TODO(TheLovinator): #21 Use a separate Redis database for cache and Celery?  # noqa: TD003
# TODO(TheLovinator): #21 Cacheops has support for Sentinel, should we use it?
# https://github.com/TheLovinator1/panso.se/issues/21
CACHEOPS_REDIS: dict[str, str | int] = {
    "host": REDIS_HOST,
    "port": 6379,
    "db": 1,
    "socket_timeout": 3,
    "password": REDIS_PASSWORD,
}

# Cache everything for a year by default
CACHEOPS_DEFAULTS: dict[str, int] = {"timeout": 60 * 60 * 24 * 365}

# Tell cacheops to degrade gracefully on redis fail
CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS: dict[str, dict[str, str]] = {
    "products.*": {"ops": "all"},
    "webhallen.*": {"ops": "all"},
    "intel.*": {"ops": "all"},
    "amd.*": {"ops": "all"},
}
