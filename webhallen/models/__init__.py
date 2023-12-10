from __future__ import annotations

from webhallen.models.json import WebhallenJSON
from webhallen.models.section import WebhallenSection
from webhallen.models.sitemaps import (
    SitemapArticle,
    SitemapCampaign,
    SitemapCampaignList,
    SitemapCategory,
    SitemapHome,
    SitemapInfoPages,
    SitemapManufacturer,
    SitemapProduct,
    SitemapRoot,
    SitemapSection,
)

__all__: list[str] = [
    "WebhallenJSON",
    "WebhallenSection",
    "SitemapRoot",
    "SitemapHome",
    "SitemapSection",
    "SitemapCategory",
    "SitemapManufacturer",
    "SitemapCampaign",
    "SitemapCampaignList",
    "SitemapInfoPages",
    "SitemapArticle",
    "SitemapProduct",
]
