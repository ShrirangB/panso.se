from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Class representing a Django application and its configuration."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core"
