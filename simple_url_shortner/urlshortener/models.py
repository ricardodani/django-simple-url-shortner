from typing import Any

from django.conf import settings
from django.db import models
from django.urls import reverse

from .converter import num_to_base62


class Url(models.Model):
    """A stored original URL and its generated short code."""

    original_url = models.URLField()
    short_code = models.CharField(max_length=20, db_index=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.short_code:
            return f"{self.original_url} -> {self.get_absolute_url()}"
        return "Not generated URL"

    def get_absolute_url(self) -> str:
        return reverse("redirect", args=[self.short_code])

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)
        if self.pk is None:
            raise RuntimeError("The URL must be saved before generating a short code.")
        self.short_code = num_to_base62(self.pk)
        Url.objects.filter(pk=self.pk).update(short_code=self.short_code)

    class Meta:
        ordering = ["-created_at"]
