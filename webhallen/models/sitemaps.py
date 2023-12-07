from __future__ import annotations

from django.db import models
from simple_history.models import HistoricalRecords


class SitemapRoot(models.Model):
    """Model for https://www.webhallen.com/sitemap.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_root_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapRoot."""

        verbose_name: str = "Sitemap root"
        verbose_name_plural: str = "Sitemap roots"
        db_table: str = "webhallen_sitemap_root"

    def __str__(self: SitemapRoot) -> str:
        """Human-readable, or informal, string representation of a Sitemap root.

        Returns:
            str: URL
        """
        return self.loc


class SitemapHome(models.Model):
    """Model for https://www.webhallen.com/sitemap.home.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_home_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapHome."""

        verbose_name: str = "Sitemap home"
        verbose_name_plural: str = "Sitemap homes"
        db_table: str = "webhallen_sitemap_home"

    def __str__(self: SitemapHome) -> str:
        """Human-readable, or informal, string representation of a Sitemap home.

        Returns:
            str: URL
        """
        return self.loc


class SitemapSection(models.Model):
    """Model for https://www.webhallen.com/sitemap.section.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_section_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapSection."""

        verbose_name: str = "Sitemap section"
        verbose_name_plural: str = "Sitemap sections"
        db_table: str = "webhallen_sitemap_section"

    def __str__(self: SitemapSection) -> str:
        """Human-readable, or informal, string representation of a Sitemap section.

        Returns:
            str: URL
        """
        return self.loc


class SitemapCategory(models.Model):
    """Model for https://www.webhallen.com/sitemap.category.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_category_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapCategory."""

        verbose_name: str = "Sitemap category"
        verbose_name_plural: str = "Sitemap categories"
        db_table: str = "webhallen_sitemap_category"

    def __str__(self: SitemapCategory) -> str:
        """Human-readable, or informal, string representation of a Sitemap category.

        Returns:
            str: URL
        """
        return self.loc


class SitemapCampaign(models.Model):
    """Model for https://www.webhallen.com/sitemap.campaign.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_campaign_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapCampaign."""

        verbose_name: str = "Sitemap campaign"
        verbose_name_plural: str = "Sitemap campaigns"
        db_table: str = "webhallen_sitemap_campaign"

    def __str__(self: SitemapCampaign) -> str:
        """Human-readable, or informal, string representation of a Sitemap campaign.

        Returns:
            str: URL
        """
        return self.loc


class SitemapCampaignList(models.Model):
    """Model for https://www.webhallen.com/sitemap.campaignList.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_campaign_list_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapCampaignList."""

        verbose_name: str = "Sitemap campaign list"
        verbose_name_plural: str = "Sitemap campaign lists"
        db_table: str = "webhallen_sitemap_campaign_list"

    def __str__(self: SitemapCampaignList) -> str:
        """Human-readable, or informal, string representation of a Sitemap campaign list.

        Returns:
            str: URL
        """
        return self.loc


class SitemapInfoPages(models.Model):
    """Model for https://www.webhallen.com/sitemap.infoPages.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_info_pages_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapInfoPages."""

        verbose_name: str = "Sitemap info page"
        verbose_name_plural: str = "Sitemap info pages"
        db_table: str = "webhallen_sitemap_info_pages"

    def __str__(self: SitemapInfoPages) -> str:
        """Human-readable, or informal, string representation of a Sitemap info pages.

        Returns:
            str: URL
        """
        return self.loc


class SitemapProduct(models.Model):
    """Model for https://www.webhallen.com/sitemap.product.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_product_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapProduct."""

        verbose_name: str = "Sitemap product"
        verbose_name_plural: str = "Sitemap products"
        db_table: str = "webhallen_sitemap_product"

    def __str__(self: SitemapProduct) -> str:
        """Human-readable, or informal, string representation of a Sitemap product.

        Returns:
            str: URL
        """
        return self.loc


class SitemapManufacturer(models.Model):
    """Model for https://www.webhallen.com/sitemap.manufacturer.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_manufacturer_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapManufacturer."""

        verbose_name: str = "Sitemap manufacturer"
        verbose_name_plural: str = "Sitemap manufacturers"
        db_table: str = "webhallen_sitemap_manufacturer"

    def __str__(self: SitemapManufacturer) -> str:
        """Human-readable, or informal, string representation of a Sitemap manufacturer.

        Returns:
            str: URL
        """
        return self.loc


class SitemapArticle(models.Model):
    """Model for https://www.webhallen.com/sitemap.article.xml."""

    loc = models.URLField(primary_key=True, help_text="URL")
    priority = models.FloatField(null=True, help_text="Priority")
    active = models.BooleanField(null=True, help_text="If the URL is still in the sitemap")

    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_sitemap_article_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Meta definition for SitemapArticle."""

        verbose_name: str = "Sitemap article"
        verbose_name_plural: str = "Sitemap articles"
        db_table: str = "webhallen_sitemap_article"

    def __str__(self: SitemapArticle) -> str:
        """Human-readable, or informal, string representation of a Sitemap article.

        Returns:
            str: URL
        """
        return self.loc
