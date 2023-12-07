from __future__ import annotations

from django.db import models
from simple_history.models import HistoricalRecords


class WebhallenJSON(models.Model):
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
    history = HistoricalRecords(
        table_name="webhallen_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for Webhallen."""

        verbose_name: str = "Webhallen JSON"
        verbose_name_plural: str = "Webhallen JSON objects"
        db_table: str = "webhallen_json"

    def __str__(self: WebhallenJSON) -> str:
        """Human-readable, or informal, string representation of Webhallen.

        Returns:
            str: Product ID and created
        """
        return f"{self.product_id} - {self.created}"
