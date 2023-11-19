from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .webhallen.models import Webhallen

admin.site.register(Webhallen, SimpleHistoryAdmin)
