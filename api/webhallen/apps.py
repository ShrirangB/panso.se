from django.apps import AppConfig


class WebhallenConfig(AppConfig):
    """Django application configuration for Webhallen."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "webhallen"
