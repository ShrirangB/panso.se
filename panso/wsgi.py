"""WSGI is a how our web server communicates with Django.

We are using Gunicorn (https://gunicorn.org/) as our HTTP server.

In front of Gunicorn we have Nginx (https://www.nginx.com/) as a reverse proxy.
And in front of Nginx we have Cloudflare (https://www.cloudflare.com/).


https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="panso.settings")

application: WSGIHandler = get_wsgi_application()
