from django.test import SimpleTestCase
from urlshortener.forms import UrlCreateForm


class UrlCreateFormTests(SimpleTestCase):
    def test_accepts_valid_url_without_exposing_owner_or_short_code(self):
        form = UrlCreateForm({"original_url": "https://example.com/python"})

        self.assertTrue(form.is_valid())
        self.assertEqual(set(form.fields), {"original_url"})

    def test_rejects_invalid_url(self):
        form = UrlCreateForm({"original_url": "not a URL"})

        self.assertFalse(form.is_valid())
