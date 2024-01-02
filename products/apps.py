"""Django application configuration for our main application."""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Django application configuration for for our main application."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "products"
