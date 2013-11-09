from django.test import TestCase
from django.conf import settings
from converter import num_to_base62
from models import Url

class URLTestCase(TestCase):

    def setUp(self):
        Url.objects.create(id=70, original_url="http://google.com")

    def test_find_url_by_shortcode(self):
        url = Url.objects.get(short_code=num_to_base62(70))
        self.assertEqual(url.id, 70)

    def test_url_have_correct_shortcode(self):
        url = Url.objects.get(id=70)
        self.assertEqual(url.short_code, num_to_base62(70))

    def test_url_is_ok(self):
        url = Url.objects.get(short_code=num_to_base62(70))
        self.assertEqual(url.original_url, "http://google.com")

    def test_creation_with_form(self):
        pass

    def test_creation_with_model(self):
        pass

class SettingsTestCase(TestCase):

    def test_if_settings_have_SITE_URL(self):
        self.assertTrue(hasattr(settings, 'SITE_URL'))
