"""Models that are used in the main panso.se application.

Models:
    - Eans (https://en.wikipedia.org/wiki/International_Article_Number)
        All our EANs in our database and the corresponding product name.
"""

from __future__ import annotations

from django.db import models
from simple_history.models import HistoricalRecords


class Eans(models.Model):
    """European Article Number (EAN) and the corresponding product name."""

    ean = models.TextField(primary_key=True, help_text="EAN")
    name = models.TextField(null=True, blank=True, help_text="Product name")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="eans_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Django metadata."""

        verbose_name: str = "European Article Number"
        verbose_name_plural: str = "European Article Numbers"
        db_table: str = "eans"
        db_table_comment: str = "Table storing European Article Numbers (EANs)"

    def __str__(self: Eans) -> str:
        """EAN and product name."""
        return f"{self.ean} - {self.name}"
