"""This module contains the model for the scraped Webhallen sections.

Section examples:
    https://www.webhallen.com/se/section/18-Fyndvaror
    https://www.webhallen.com/se/section/3-Datorer-Tillbehor
    https://www.webhallen.com/se/section/8-Datorkomponenter
"""

from __future__ import annotations

import typing

from django.db import models
from simple_history.models import HistoricalRecords


class WebhallenSection(models.Model):
    """Model definition for WebhallenSection.

    Icon URL example:
        #1A1A1D is the icon color
        - https://cdn.webhallen.com/api/dynimg/category/datorkomponenter/1A1A1D
        - https://cdn.webhallen.com/api/dynimg/category/datorer_tillbehor/1A1A1D


    Example:
        - id: 8
        - metaTitle: "Datorkomponenter - datordelar och uppgraderingspaket"
        - active: true
        - icon: "datorkomponenter"
        - name: "Datorkomponenter"

    Args:
        models: Django model
    """

    section_id = models.IntegerField(primary_key=True, help_text="Section ID")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_section_history",
        excluded_fields=["created", "updated"],
    )

    meta_title = models.TextField(null=True, blank=True, help_text="Meta title")
    active = models.BooleanField(null=True, help_text="Active")
    icon = models.TextField(null=True, blank=True, help_text="Icon")
    icon_url = models.URLField(null=True, blank=True, help_text="Icon URL")
    name = models.TextField(null=True, blank=True, help_text="Name")
    url = models.URLField(null=True, blank=True, help_text="URL")

    class Meta:
        """Meta definition for WebhallenSection."""

        ordering: typing.ClassVar[list] = ["-section_id"]
        verbose_name: str = "Webhallen section"
        verbose_name_plural: str = "Webhallen sections"
        db_table: str = "webhallen_section"
        db_table_comment: str = "Table storing Webhallen sections"

    def __str__(self: WebhallenSection) -> str:
        """Human-readable, or informal, string representation of a Webhallen section.

        Returns:
            str: Section ID and name
        """
        return f"{self.section_id} - {self.name}"
