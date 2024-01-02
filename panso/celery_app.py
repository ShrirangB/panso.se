"""TL;DR: Celery is a distributed task queue system for handling asynchronous tasks in Python.

We use it for web scraping and other tasks that take a long time to complete and need to be run in the background.
"""

import os

from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import find_dotenv, load_dotenv

logger = get_task_logger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", value="panso.settings")

load_dotenv(dotenv_path=find_dotenv(), verbose=True)

REDIS_PASSWORD: str = os.getenv(key="REDIS_PASSWORD", default="")
REDIS_HOST: str = os.getenv(key="REDIS_HOST", default="")

if not REDIS_PASSWORD or not REDIS_PASSWORD:
    msg = "REDIS_PASSWORD environment variable is not set or empty in celery.py"
    raise ValueError(msg)

app = Celery(
    main="panso",
    broker=f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379",
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=5,
    result_backend="django-db",
    cache_backend="django-cache",
    timezone="Europe/Stockholm",
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
