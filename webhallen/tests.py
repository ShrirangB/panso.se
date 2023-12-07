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
