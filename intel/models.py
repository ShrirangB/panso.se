from __future__ import annotations

from django.db import models
from simple_history.models import HistoricalRecords


class ArkFilterData(models.Model):
    """The data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""

    json_data = models.JSONField(verbose_name="Intel ARK Filter Data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        table_name="ark_filter_data_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Django metadata."""

        verbose_name: str = "Intel ARK Filter Data"
        verbose_name_plural: str = "Intel ARK Filter Data"
        db_table: str = "ark_filter_data"
        db_table_comment: str = "Table storing Intel ARK Filter Data"

    def __str__(self: ArkFilterData) -> str:
        """Return the string representation of the model."""
        return f"Intel ARK Filter Data ({self.created_at})"
