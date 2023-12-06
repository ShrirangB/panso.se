from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Django application configuration for HTML pages that are not tied to a specific store."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "pages"
