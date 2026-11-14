from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError, models, transaction
from django.urls import reverse

from .converter import get_url_code_encoder

MAX_SHORT_CODE_LENGTH = 22
MAX_CODE_GENERATION_ATTEMPTS = 5


class Url(models.Model):
    """A stored original URL and its generated short code."""

    original_url = models.URLField()
    short_code = models.CharField(
        max_length=MAX_SHORT_CODE_LENGTH,
        blank=True,
        null=True,
        unique=True,
    )
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
        should_generate_code = self._state.adding or not self.short_code
        with transaction.atomic():
            if should_generate_code:
                self.short_code = None
            super().save(*args, **kwargs)
            if not should_generate_code:
                return
            if self.pk is None:
                raise RuntimeError(
                    "The URL must be saved before generating a short code."
                )

            encoder = get_url_code_encoder()
            for _ in range(MAX_CODE_GENERATION_ATTEMPTS):
                short_code = encoder.encode(self.pk)
                if (
                    not isinstance(short_code, str)
                    or not short_code
                    or not short_code.isascii()
                    or not short_code.isalnum()
                    or len(short_code) > MAX_SHORT_CODE_LENGTH
                ):
                    raise ImproperlyConfigured(
                        "URLSHORTENER_CODE_ENCODER.encode() must return a non-empty "
                        "ASCII alphanumeric string of at most "
                        f"{MAX_SHORT_CODE_LENGTH} characters."
                    )
                try:
                    with transaction.atomic():
                        Url.objects.filter(pk=self.pk).update(short_code=short_code)
                except IntegrityError:
                    if (
                        Url.objects.filter(short_code=short_code)
                        .exclude(pk=self.pk)
                        .exists()
                    ):
                        continue
                    raise
                self.short_code = short_code
                return

            raise RuntimeError(
                "The URL code encoder repeatedly generated codes already in use."
            )

    class Meta:
        ordering = ["-created_at"]
