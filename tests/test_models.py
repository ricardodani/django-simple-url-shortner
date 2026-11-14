from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from urlshortener.converter import num_to_base62
from urlshortener.models import Url


class UrlModelTests(TestCase):
    def test_save_generates_a_stable_short_code(self):
        url = Url.objects.create(original_url="https://example.com/python")

        self.assertEqual(url.short_code, num_to_base62(url.pk))

        url.original_url = "https://example.org/updated"
        url.save()

        self.assertEqual(url.short_code, num_to_base62(url.pk))

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
