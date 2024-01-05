from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from intel.models import Processor

if TYPE_CHECKING:
    import datetime


class LatestProcessorsFeed(Feed):
    """RSS 2.0 feed for the latest processors.

    URL:
        /intel/.rss
    """

    title: str = "Panso - Latest Intel processors"
    link: str = "/intel/"
    description: str = "The latest Intel processors on Panso."
    language: str = "en"

    def author_name(self: LatestProcessorsFeed) -> str:  # noqa: PLR6301
        """Get author name."""
        return "Panso.se"

    def author_email(self: LatestProcessorsFeed) -> str:  # noqa: PLR6301
        """Get author email."""
        return "rss@panso.se"

    def author_link(self: LatestProcessorsFeed) -> str:  # noqa: PLR6301
        """Get author link."""
        return "https://panso.se/"

    def categories(self: LatestProcessorsFeed) -> list[str]:  # noqa: PLR6301
        """Get categories."""
        return ["Panso", "Hardware", "Intel", "CPU"]

    def feed_copyright(self: LatestProcessorsFeed) -> str:  # noqa: PLR6301
        """Get feed copyright."""
        return "CC BY-SA 4.0"

    def items(self: LatestProcessorsFeed):  # noqa: ANN201, PLR6301
        """Get the latest processors."""
        return Processor.objects.order_by("-created")[:300]

    def item_title(self: LatestProcessorsFeed, item: Processor) -> str:  # noqa: PLR6301
        """Get CPU name."""
        return item.name or "Unknown processor"

    def item_description(self: LatestProcessorsFeed, item: Processor) -> str:  # noqa: PLR6301
        """Get CPU description."""
        # TODO(TheLovinator): #56 Improve Intel processor RSS feed description
        # https://github.com/TheLovinator1/panso.se/issues/56
        return f"Found new Intel CPU: {item.name} - {item.total_cores} cores ({item.total_threads} threads)"

    def item_link(self: LatestProcessorsFeed, item: Processor) -> str:  # noqa: PLR6301
        """Get CPU link."""
        return item.get_absolute_url()

    def item_updateddate(self: LatestProcessorsFeed, item: Processor) -> datetime.datetime:  # noqa: PLR6301
        """Get CPU updated date."""
        return item.updated


class AtomLatestProcessorsFeed(LatestProcessorsFeed):
    """Same as LatestProcessorsFeed but in Atom format.

    URL:
        /intel/.atom
    """

    feed_type = Atom1Feed
    subtitle: str = LatestProcessorsFeed.description
