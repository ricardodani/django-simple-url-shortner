"""
Request Context processors.
"""

from django.http import HttpRequest


def site_context(request: HttpRequest) -> dict[str, object]:
    return {}
