from __future__ import annotations

import os
from pathlib import Path

import sentry_sdk
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), verbose=True)

DEBUG: bool = os.getenv(key="DEBUG", default="True").lower() == "true"
sentry_sdk.init(
    dsn="https://9b2528b38dbd535184b0b2420c80aea4@o4505228040339456.ingest.sentry.io/4506312539439104",
    debug=DEBUG,
    environment="Development" if DEBUG else "Production",
    send_default_pii=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
SECRET_KEY: str = os.getenv("SECRET_KEY", default="")
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
ROOT_URLCONF = "core.urls"
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SIMPLE_HISTORY_REVERT_DISABLED = True
WSGI_APPLICATION = "core.wsgi.application"
INTERNAL_IPS: list[str] = ["127.0.0.1", "localhost"]
if BOT_IP_LIST:
    INTERNAL_IPS.extend(BOT_IP_LIST)

INSTALLED_APPS: list[str] = [
    # First party
    "webhallen.apps.WebhallenConfig",
    # Third party
    "simple_history",  # https://github.com/jazzband/django-simple-history
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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


TEMPLATES: list[dict[str, str | list[str] | bool | dict[str, list[str]]]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


REDIS_PASSWORD: str = os.getenv(key="REDIS_PASSWORD", default="")
REDIS_HOST: str = os.getenv(key="REDIS_HOST", default="")
CACHES: dict[str, dict[str, str]] = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379",
    },
}
