from __future__ import annotations

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from loguru import logger

load_dotenv(find_dotenv(), verbose=True)
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

logger.debug(f"BASE_DIR: {BASE_DIR}")
logger.debug(f"SECRET_KEY: {SECRET_KEY}")
logger.debug(f"DEBUG: {DEBUG}")
logger.debug(f"ADMINS: {ADMINS}")
logger.debug(f"BOT_IP_LIST: {BOT_IP_LIST}")
logger.debug(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
logger.debug(f"EMAIL_HOST_USER: {EMAIL_HOST_USER}")
logger.debug(f"EMAIL_HOST_PASSWORD: {EMAIL_HOST_PASSWORD}")
logger.debug(f"DEFAULT_FROM_EMAIL: {DEFAULT_FROM_EMAIL}")
logger.debug(f"SERVER_EMAIL: {SERVER_EMAIL}")
logger.debug(f"INTERNAL_IPS: {INTERNAL_IPS}")

INSTALLED_APPS: list[str] = [
    # First party
    "core.apps.CoreConfig",
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

DATABASE_URL: str = os.getenv(key="DATABASE_URL", default=str(Path(BASE_DIR / "db.sqlite3")))
DATABASES: dict[str, dict[str, str]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_URL,
    },
}
