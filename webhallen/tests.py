"""This file gets run when you run the command `python manage.py test`.

https://docs.djangoproject.com/en/5.0/topics/testing/
"""
# TODO(TheLovinator): #26 Add more tests.
# https://github.com/TheLovinator1/panso.se/issues/26

from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse


class WebhallenTests(TestCase):
    """Tests for the webhallen app."""

    def test_index_view(self: WebhallenTests) -> None:
        """Test the index view."""
        url: str = reverse("webhallen:index")
        response: HttpResponse = self.client.get(url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get("/webhallen/")
        assert response2.status_code == 200


class WebhallenAPITests(TestCase):
    """Tests for the webhallen API."""

    # TODO(TheLovinator): #31 Add product data to the test database and test the API endpoint.
    # https://github.com/TheLovinator1/panso.se/issues/31
    def test_api_products(self: WebhallenAPITests) -> None:
        """Test the API endpoint for all products."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/products")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_product(self: WebhallenAPITests) -> None:
        """Test the API endpoint for a single product."""
        # TODO(TheLovinator): #31 Add product data to the test database and test the API endpoint.
        # https://github.com/TheLovinator1/panso.se/issues/31

    def test_api_sitemaps_root(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the root sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/root")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_home(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the home sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/home")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_info_pages(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the info pages sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/info-pages")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_categories(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the categories sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/categories")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_products(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the products sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/products")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_campaigns(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the campaigns sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/campaigns")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_campaign_lists(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the campaign lists sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/campaign-lists")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_sections(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the sections sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/sections")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_manufacturers(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the manufacturers sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/manufacturers")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_sitemaps_articles(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the articles sitemap."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sitemaps/articles")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_list_sections(self: WebhallenAPITests) -> None:
        """Test the API endpoint for the sections list."""
        response: HttpResponse = self.client.get("/api/v1/webhallen/sections")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []
