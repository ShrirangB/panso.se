from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .webhallen.models import WebhallenJSON

admin.site.register(WebhallenJSON, SimpleHistoryAdmin)
