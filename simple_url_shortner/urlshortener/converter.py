import hashlib
import hmac
import secrets
import string
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

CHARS = string.digits + string.ascii_letters
RANDOM_CODE_LENGTH = 16
HASH_CODE_BYTES = 16
HASH_CODE_LENGTH = 22
SHORT_HASH_CODE_LENGTH = 8
DEFAULT_URL_CODE_ENCODER = "urlshortener.converter.Base62UrlCodeEncoder"


class UrlCodeEncoder(ABC):
    """Contract for converting a saved URL's integer primary key to a short code."""

    @abstractmethod
    def encode(self, value: int) -> str:
        """Return a URL-safe code for a non-negative integer."""


class Base62UrlCodeEncoder(UrlCodeEncoder):
    """Encode integer identifiers with digits, lowercase letters, then uppercase."""

    def encode(self, value: int) -> str:
        return num_to_base62(value)


class RandomUrlCodeEncoder(UrlCodeEncoder):
    """Generate an unpredictable 16-character alphanumeric short code."""

    def encode(self, value: int) -> str:
        return "".join(secrets.choice(CHARS) for _ in range(RANDOM_CODE_LENGTH))


class HmacUrlCodeEncoder(UrlCodeEncoder):
    """Encode IDs as 128-bit HMAC-SHA256 tokens using Django's SECRET_KEY."""

    code_length = HASH_CODE_LENGTH

    def __init__(self) -> None:
        self._collision_counter = 0

    def encode(self, value: int) -> str:
        if value < 0:
            raise ValueError("value must be non-negative")
        secret_key = settings.SECRET_KEY
        if not isinstance(secret_key, str) or not secret_key:
            raise ImproperlyConfigured(
                "A non-empty Django SECRET_KEY is required for HMAC URL codes."
            )

        message = f"urlshortener:{value}:{self._collision_counter}".encode("ascii")
        self._collision_counter += 1
        digest = hmac.new(
            secret_key.encode("utf-8"),
            message,
            hashlib.sha256,
        ).digest()[:HASH_CODE_BYTES]
        number = int.from_bytes(digest, byteorder="big")
        code_space = len(CHARS) ** self.code_length
        if number >= code_space:
            number %= code_space
        return num_to_base62(number).rjust(self.code_length, CHARS[0])


class ShortHmacUrlCodeEncoder(HmacUrlCodeEncoder):
    """Generate an intentionally weaker, 8-character HMAC code."""

    code_length = SHORT_HASH_CODE_LENGTH


def get_url_code_encoder() -> UrlCodeEncoder:
    """Load the configured URL code encoder, or use the base62 implementation."""
    encoder_path = getattr(
        settings,
        "URLSHORTENER_CODE_ENCODER",
        DEFAULT_URL_CODE_ENCODER,
    )
    encoder_class = import_string(encoder_path)
    if not isinstance(encoder_class, type) or not issubclass(
        encoder_class, UrlCodeEncoder
    ):
        raise ImproperlyConfigured(
            "URLSHORTENER_CODE_ENCODER must point to a UrlCodeEncoder subclass."
        )
    return encoder_class()


def num_to_base62(number: int) -> str:
    """Encode a non-negative integer as a base-62 string."""
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return CHARS[0]

    encoded: list[str] = []
    while number:
        number, remainder = divmod(number, len(CHARS))
        encoded.append(CHARS[remainder])
    return "".join(reversed(encoded))
