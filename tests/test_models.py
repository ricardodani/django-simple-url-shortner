from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django.urls import reverse
from urlshortener.converter import UrlCodeEncoder, num_to_base62
from urlshortener.models import Url


class HexUrlCodeEncoder(UrlCodeEncoder):
    def encode(self, value: int) -> str:
        return f"x{value:x}"


class InvalidUrlCodeEncoder(UrlCodeEncoder):
    def encode(self, value: int) -> str:
        return "invalid-code"


class UrlModelTests(TestCase):
    def test_save_generates_a_stable_short_code(self):
        url = Url.objects.create(original_url="https://example.com/python")

        self.assertEqual(url.short_code, num_to_base62(url.pk))

        url.original_url = "https://example.org/updated"
        url.save()

        self.assertEqual(url.short_code, num_to_base62(url.pk))

    def test_configured_encoder_is_used_for_new_urls_and_redirects(self):
        encoder_path = f"{__name__}.HexUrlCodeEncoder"
        with override_settings(URLSHORTENER_CODE_ENCODER=encoder_path):
            url = Url.objects.create(original_url="https://example.com/custom")

        self.assertEqual(url.short_code, f"x{url.pk:x}")
        response = self.client.get(url.get_absolute_url())
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers["Location"], url.original_url)

    def test_random_encoder_creates_distinct_codes_for_saved_urls(self):
        with override_settings(
            URLSHORTENER_CODE_ENCODER="urlshortener.converter.RandomUrlCodeEncoder"
        ):
            first = Url.objects.create(original_url="https://example.com/first")
            second = Url.objects.create(original_url="https://example.com/second")

        self.assertEqual(len(first.short_code), 16)
        self.assertEqual(len(second.short_code), 16)
        self.assertNotEqual(first.short_code, second.short_code)

    def test_hmac_encoder_persists_22_character_codes(self):
        with override_settings(
            URLSHORTENER_CODE_ENCODER="urlshortener.converter.HmacUrlCodeEncoder"
        ):
            url = Url.objects.create(original_url="https://example.com/hmac")

        self.assertEqual(len(url.short_code), 22)
        self.assertTrue(url.short_code.isalnum())

    def test_short_code_collision_is_retried(self):
        first = Url.objects.create(original_url="https://example.com/first")
        with patch("urlshortener.models.get_url_code_encoder") as get_encoder:
            get_encoder.return_value.encode.side_effect = [
                first.short_code,
                "uniqueCode",
            ]
            second = Url.objects.create(original_url="https://example.com/second")

        self.assertEqual(second.short_code, "uniqueCode")
        self.assertEqual(Url.objects.count(), 2)

    def test_invalid_encoder_output_rolls_back_new_url(self):
        encoder_path = f"{__name__}.InvalidUrlCodeEncoder"
        with (
            override_settings(URLSHORTENER_CODE_ENCODER=encoder_path),
            self.assertRaisesRegex(ImproperlyConfigured, "ASCII alphanumeric"),
        ):
            Url.objects.create(original_url="https://example.com/invalid")

        self.assertFalse(Url.objects.exists())

    def test_string_representation_and_absolute_url(self):
        url = Url.objects.create(original_url="https://example.com/")

        self.assertEqual(str(url), f"{url.original_url} -> {url.get_absolute_url()}")
        self.assertEqual(
            url.get_absolute_url(),
            reverse("redirect", args=[num_to_base62(url.pk)]),
        )

    def test_user_relation_uses_the_configured_user_model(self):
        user = get_user_model().objects.create_user(username="url-owner")
        url = Url.objects.create(
            original_url="https://example.com/",
            user=user,
        )

        self.assertEqual(url.user, user)
