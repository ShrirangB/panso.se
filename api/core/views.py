from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index_view(request: HttpRequest) -> HttpResponse:
    """Return /."""
    return render(request, "core/index.html")
