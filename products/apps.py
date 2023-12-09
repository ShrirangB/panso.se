from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Django application configuration for Products."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "products"
