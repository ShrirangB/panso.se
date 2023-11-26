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

        verbose_name: str = "Webhallen"
        verbose_name_plural: str = "Webhallen"
        db_table: str = "webhallen_json"

    def __str__(self: WebhallenJSON) -> str:
        """Human-readable, or informal, string representation of Webhallen.

        Returns:
            str: Product ID and created
        """
        return f"{self.product_id} - {self.created}"


class WebhallenProduct(models.Model):
    """Model definition for a Webhallen product. Used for generating HUGO pages."""

    product_id = models.IntegerField(primary_key=True, help_text="Product ID")
    created = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated")
    history = HistoricalRecords(
        table_name="webhallen_product_history",
        excluded_fields=["created", "updated"],
    )

    minimum_rank_level = models.IntegerField(null=True, blank=True, help_text="Minimum rank level")
    images_zoom = models.TextField(null=True, blank=True, help_text="Comma separated list of zoom images")
    images_large = models.TextField(null=True, blank=True, help_text="Comma separated list of large images")
    images_thumb = models.TextField(null=True, blank=True, help_text="Comma separated list of thumbnail images")
    name = models.TextField(null=True, blank=True, help_text="Product name")

    price = models.TextField(null=True, blank=True, help_text="Product price")
    vat = models.TextField(null=True, blank=True, help_text="Product VAT")
    price_end_at = models.DateTimeField(null=True, blank=True, help_text="Price end at")
    price_nearly_over = models.BooleanField(null=True, help_text="Price nearly over")
    price_flash_sale = models.BooleanField(null=True, help_text="Price flash sale")
    price_type = models.TextField(null=True, blank=True, help_text="Price type")

    regular_price = models.TextField(null=True, blank=True, help_text="Regular price")
    regular_price_type = models.TextField(null=True, blank=True, help_text="Regular price type")
    regular_price_end_at = models.DateTimeField(null=True, blank=True, help_text="Regular price end at")
    regular_price_nearly_over = models.BooleanField(null=True, help_text="Regular price nearly over")
    regular_price_flash_sale = models.BooleanField(null=True, help_text="Regular price flash sale")

    lowest_price = models.TextField(null=True, blank=True, help_text="Lowest price")
    lowest_price_type = models.TextField(null=True, blank=True, help_text="Lowest price type")
    lowest_price_end_at = models.DateTimeField(null=True, blank=True, help_text="Lowest price end at")
    lowest_price_nearly_over = models.BooleanField(null=True, help_text="Lowest price nearly over")
    lowest_price_flash_sale = models.BooleanField(null=True, help_text="Lowest price flash sale")

    level_one_price = models.TextField(null=True, blank=True, help_text="Level one price")
    level_one_price_type = models.TextField(null=True, blank=True, help_text="Level one price type")
    level_one_price_end_at = models.DateTimeField(null=True, blank=True, help_text="Level one price end at")
    level_one_price_nearly_over = models.BooleanField(null=True, help_text="Level one price nearly over")
    level_one_price_flash_sale = models.BooleanField(null=True, help_text="Level one price flash sale")

    description = models.TextField(null=True, blank=True, help_text="Product description")
    meta_title = models.TextField(null=True, blank=True, help_text="Product meta title")
    meta_description = models.TextField(null=True, blank=True, help_text="Product meta description")

    canonical_url = models.TextField(null=True, blank=True, help_text="Product canonical URL")
    release_date = models.TextField(null=True, blank=True, help_text="Product release date")

    section_id = models.IntegerField(null=True, blank=True, help_text="Section ID")
    is_digital = models.BooleanField(null=True, help_text="Is digital")
    discontinued = models.BooleanField(null=True, help_text="Discontinued")
    category_tree = models.TextField(null=True, blank=True, help_text="Category tree")

    main_category_path = models.TextField(null=True, blank=True, help_text="Comma separated main category path")
    manufacturer = models.IntegerField(null=True, blank=True, help_text="Manufacturer")
    part_numbers = models.TextField(null=True, blank=True, help_text="Comma separated list of part numbers")
    eans = models.TextField(null=True, blank=True, help_text="Comma separated list of EANs")
    thumbnail = models.TextField(null=True, blank=True, help_text="Thumbnail URL")

    average_rating = models.FloatField(null=True, blank=True, help_text="Average rating")
    average_rating_type = models.TextField(null=True, blank=True, help_text="Average rating type")

    energy_marking_rating = models.TextField(null=True, blank=True, help_text="Energy marking rating (F to A)")
    energy_marking_label = models.TextField(null=True, blank=True, help_text="Energy rating label link")

    package_size_id = models.IntegerField(null=True, blank=True, help_text="Package size ID")
    status_codes = models.TextField(null=True, blank=True, help_text="Comma separated list of status codes")
    long_delivery_notice = models.TextField(null=True, blank=True, help_text="Long delivery notice")
    categories = models.TextField(null=True, blank=True, help_text="Comma separated list of categories")
    phone_subscription = models.BooleanField(null=True, help_text="Phone subscription")

    highlighted_review_id = models.IntegerField(null=True, blank=True, help_text="Highlighted review ID")
    highlighted_review_text = models.TextField(null=True, blank=True, help_text="Highlighted review text")
    highlighted_review_rating = models.IntegerField(null=True, blank=True, help_text="Highlighted review rating")
    highlighted_review_upvotes = models.IntegerField(null=True, blank=True, help_text="Highlighted review upvotes")
    highlighted_review_downvotes = models.IntegerField(null=True, blank=True, help_text="Highlighted review downvotes")
    highlighted_review_verified = models.BooleanField(null=True, help_text="Highlighted review verified")
    highlighted_review_created = models.DateTimeField(null=True, blank=True, help_text="Highlighted review created")
    highlighted_review_is_anonymous = models.BooleanField(null=True, help_text="Highlighted review is anonymous")
    highlighted_review_is_employee = models.BooleanField(null=True, help_text="Highlighted review is employee")
    highlighted_review_product_id = models.IntegerField(null=True, blank=True, help_text="Highlighted product ID")
    highlighted_review_user_id = models.TextField(
        null=True,
        blank=True,
        help_text="Highlighted review user ID - Anonymous if anonymous",
    )
    highlighted_review_is_hype = models.BooleanField(null=True, help_text="Highlighted review is hype")

    is_fyndware = models.BooleanField(null=True, help_text="Is Fyndware")
    fyndware_of = models.IntegerField(null=True, blank=True, help_text="The product ID of the real product")
    fyndware_of_description = models.TextField(null=True, blank=True, help_text="Fyndware of description")
    fyndware_class = models.IntegerField(null=True, blank=True, help_text="Fyndware class")

    main_title = models.TextField(null=True, blank=True, help_text="Main title")
    sub_title = models.TextField(null=True, blank=True, help_text="Sub title")
    is_shippable = models.BooleanField(null=True, help_text="Is shippable")
    is_collectable = models.BooleanField(null=True, help_text="Is collectable")
    excluded_shipping_methods = models.TextField(null=True, blank=True, help_text="Excluded shipping methods")
    insurance_id = models.IntegerField(null=True, blank=True, help_text="Insurance ID")

    possible_delivery_methods = models.TextField(null=True, blank=True, help_text="Possible delivery methods")

    class Meta:
        """Meta definition for WebhallenProduct."""

        verbose_name: str = "Webhallen product"
        verbose_name_plural: str = "Webhallen products"
        db_table: str = "webhallen_product"

    def __str__(self: WebhallenProduct) -> str:
        """Human-readable, or informal, string representation of a Webhallen product.

        Returns:
            str: Product name and price
        """
        return f"{self.name} - {self.price} kr"


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

        verbose_name: str = "Webhallen section"
        verbose_name_plural: str = "Webhallen sections"
        db_table: str = "webhallen_section"

    def __str__(self: WebhallenSection) -> str:
        """Human-readable, or informal, string representation of a Webhallen section.

        Returns:
            str: Section ID and name
        """
        return f"{self.section_id} - {self.name}"


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
