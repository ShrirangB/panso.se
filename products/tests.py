from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import SimpleTestCase
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse


class ProductsTests(SimpleTestCase):
    """Tests for the products app."""

    def test_index_view(self: ProductsTests) -> None:
        """Test the index view."""
        url: str = reverse("products:index")
        response: HttpResponse = self.client.get(url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get("/")
        assert response2.status_code == 200

    def test_robots_txt_view(self: ProductsTests) -> None:
        """Test the robots.txt view."""
        url: str = reverse("products:robots-txt")
        response: HttpResponse = self.client.get(url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get("/robots.txt")
        assert response2.status_code == 200

    def test_favicon_view(self: ProductsTests) -> None:
        """Test the favicon.ico view."""
        response: HttpResponse = self.client.get("/favicon.ico")
        assert response.status_code == 301

    def test_icon_512_view(self: ProductsTests) -> None:
        """Test the icon-512.png view."""
        response: HttpResponse = self.client.get("/icon-512.png")
        assert response.status_code == 301

    def test_icon_192_view(self: ProductsTests) -> None:
        """Test the icon-192.png view."""
        response: HttpResponse = self.client.get("/icon-192.png")
        assert response.status_code == 301

    def test_bot_ip_list_view(self: ProductsTests) -> None:
        """Test the bot-ip-list view."""
        url: str = reverse("products:bot-ip-list")
        response: HttpResponse = self.client.get(url)
        assert response.status_code == 200
        assert response.content.decode().count(".") == 3

        response2: HttpResponse = self.client.get("/bot-ip-list.txt")
        assert response2.status_code == 200
        assert response2.content.decode().count(".") == 3
