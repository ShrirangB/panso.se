"""This file gets run when you run the command `python manage.py test`.

https://docs.djangoproject.com/en/5.0/topics/testing/
"""
# TODO(TheLovinator): #26 Add more tests.
# https://github.com/TheLovinator1/panso.se/issues/26

from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse


class ProductsTests(SimpleTestCase):
    """Tests for the products app."""

    def test_index_view(self: ProductsTests) -> None:
        """Test the index view."""
        url: str = reverse(viewname="products:index")
        response: HttpResponse = self.client.get(path=url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get(path="/")
        assert response2.status_code == 200

    def test_robots_txt_view(self: ProductsTests) -> None:
        """Test the robots.txt view."""
        url: str = reverse(viewname="products:robots-txt")
        response: HttpResponse = self.client.get(path=url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get(path="/robots.txt")
        assert response2.status_code == 200

    def test_favicon_view(self: ProductsTests) -> None:
        """Test the favicon.ico view."""
        response: HttpResponse = self.client.get(path="/favicon.ico")
        assert response.status_code == 301

    def test_icon_512_view(self: ProductsTests) -> None:
        """Test the icon-512.png view."""
        response: HttpResponse = self.client.get(path="/icon-512.png")
        assert response.status_code == 301

    def test_icon_192_view(self: ProductsTests) -> None:
        """Test the icon-192.png view."""
        response: HttpResponse = self.client.get(path="/icon-192.png")
        assert response.status_code == 301

    def test_bot_ip_list_view(self: ProductsTests) -> None:
        """Test the bot-ip-list view."""
        url: str = reverse(viewname="products:bot-ip-list")
        response: HttpResponse = self.client.get(path=url)
        assert response.status_code == 200
        assert response.content.decode().count(".") == 3

        response2: HttpResponse = self.client.get(path="/bot-ip-list.txt")
        assert response2.status_code == 200
        assert response2.content.decode().count(".") == 3

    def test_contact_view(self: ProductsTests) -> None:
        """Test the contact view."""
        url: str = reverse(viewname="products:contact")
        response: HttpResponse = self.client.get(path=url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get(path="/contact")
        assert response2.status_code == 200

    def test_privacy_view(self: ProductsTests) -> None:
        """Test the privacy view."""
        url: str = reverse(viewname="products:privacy")
        response: HttpResponse = self.client.get(path=url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get(path="/privacy")
        assert response2.status_code == 200

    def test_terms_view(self: ProductsTests) -> None:
        """Test the terms view."""
        url: str = reverse(viewname="products:terms")
        response: HttpResponse = self.client.get(path=url)
        assert response.status_code == 200
        response2: HttpResponse = self.client.get(path="/terms")
        assert response2.status_code == 200


class PansoAPITests(TestCase):
    """Test the Panso API."""

    def test_api_eans(self: PansoAPITests) -> None:
        """Test the API endpoint for all EANs."""
        response: HttpResponse = self.client.get("/api/v1/eans")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_api_ean(self: PansoAPITests) -> None:
        """Test the API endpoint for a single EAN."""
        response: HttpResponse = self.client.get("/api/v1/eans/1")
        assert response.status_code == 404
        assert response["Content-Type"] == "application/json"
        assert response.json() == {"error": "EAN with ID 1 not found."}

        # TODO(TheLovinator): #31 Add EANs to the test database and test the API endpoint.
        # https://github.com/TheLovinator1/panso.se/issues/31

        # response2: HttpResponse = self.client.get("/api/v1/eans/5907814951762")
        # assert response2.status_code == 200
        # assert response2["Content-Type"] == "application/json"
        # response_json = response2.json()
        # assert response_json["ean"] == "5907814951762"
        # assert response_json["name"] == "Carcassonne - Expansion 1: Inns & Cathedrals (Nordic)"

        # created: str = response_json["created"]
        # assert len(created) == 19
        # assert created[4] == "-"
        # assert created[7] == "-"
        # assert created[10] == " "
        # assert created[13] == ":"
        # assert created[16] == ":"
        # assert created[0:4].isdigit()
        # assert created[5:7].isdigit()
        # assert created[8:10].isdigit()
        # assert created[11:13].isdigit()
        # assert created[14:16].isdigit()
        # assert created[17:19].isdigit()

        # updated: str = response_json["updated"]
        # assert len(updated) == 19
        # assert updated[4] == "-"
        # assert updated[7] == "-"
        # assert updated[10] == " "
        # assert updated[13] == ":"
        # assert updated[16] == ":"
        # assert updated[0:4].isdigit()
        # assert updated[5:7].isdigit()
        # assert updated[8:10].isdigit()
        # assert updated[11:13].isdigit()
        # assert updated[14:16].isdigit()
        # assert updated[17:19].isdigit()
