from django.test import TestCase
from converter import num_to_base62
from models import Url

class ConverterTestCase(TestCase):

    def setUp(self):
        Url.objects.create(id=70, url="http://google.com")

    def test_find_url_by_shortcode(self):
        url = Url.objects.get(short_code=num_to_base62(70))
        self.assertEqual(url.id, 70)

    def test_url_have_correct_shortcode(self):
        url = Url.objects.get(id=70)
        self.assertEqual(url.short_code, num_to_base62(70))
