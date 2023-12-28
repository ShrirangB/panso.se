from django.apps import AppConfig


class AmdConfig(AppConfig):
    """Django application configuration for AMD."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "amd"
