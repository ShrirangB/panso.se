# Create your tests here.
from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase

if TYPE_CHECKING:
    from django.http import HttpResponse


class IntelTests(TestCase):
    """Tests things for the Intel app."""

    # TODO: Test that we get the correct data from the API.
    def test_get_filter_data(self: IntelTests) -> None:
        """Test that the filter data is available."""
        response: HttpResponse = self.client.get("/api/intel/filter")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []
