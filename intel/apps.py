from django.apps import AppConfig


class IntelConfig(AppConfig):
    """Django application configuration for Intel."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "intel"
