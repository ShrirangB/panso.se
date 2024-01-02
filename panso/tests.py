"""This file gets run when you run the command `python manage.py test`.

https://docs.djangoproject.com/en/5.0/topics/testing/
"""
# TODO(TheLovinator): #26 Add more tests.
# https://github.com/TheLovinator1/panso.se/issues/26

from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase

if TYPE_CHECKING:
    from django.http import HttpResponse


class PansoTests(TestCase):
    """Tests things that are not in any app."""

    def test_api_docs(self: PansoTests) -> None:
        """Test that the api docs are available."""
        response: HttpResponse = self.client.get(path="/api/v1/docs/redoc")
        assert response.status_code == 200
        response2: HttpResponse = self.client.get(path="/api/v1/docs/swagger")
        assert response2.status_code == 200

    # TODO(TheLovinator): #32 Re-add admin page.
    # https://github.com/TheLovinator1/panso.se/issues/32

    # def test_admin(self: PansoTests) -> None:
    #     """Test that the admin is available."""
    #     url: str = reverse("admin:index")
    #     response: HttpResponse = self.client.get(url)
    #     assert response.status_code == 302
    #     response2: HttpResponse = self.client.get("/admin/")
    #     assert response2.status_code == 302

    #     url: str = reverse("admin:login")
    #     response3: HttpResponse = self.client.get(url)
    #     assert response3.status_code == 200
    #     response4: HttpResponse = self.client.get("/admin/login/")
    #     assert response4.status_code == 200
