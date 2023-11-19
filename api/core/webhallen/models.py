from __future__ import annotations

from django.db import models
from simple_history.models import HistoricalRecords


class Webhallen(models.Model):
    """Model definition for Webhallen.

    This is scraped from the Webhallen API.

    Args:
        models: Django model

    Returns:
        Webhallen model
    """

    product_id = models.IntegerField(primary_key=True, help_text="Product ID")
    product_json = models.JSONField(help_text="Product JSON")
    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords()

    class Meta:
        """Meta definition for Webhallen."""

        verbose_name: str = "Webhallen"
        verbose_name_plural: str = "Webhallen"

    def __str__(self: Webhallen) -> str:
        """Unicode representation of Webhallen.

        Returns:
            str: Product ID and created
        """
        return f"{self.product_id} - {self.created}"

    def __repr__(self: Webhallen) -> str:
        """Unicode representation of Webhallen.

        Returns:
            str: Product ID and created
        """
        return f"{self.product_id} - {self.created}"
