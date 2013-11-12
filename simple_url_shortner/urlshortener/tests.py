from django.test import TestCase, client
from django.contrib.auth.models import User

from .converter import num_to_base62
from .models import Url
from .forms import UrlCreateForm

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
        _original_url = u'http://google.com/'
        form = UrlCreateForm({'original_url': _original_url})
        instance = form.save()
        self.assertEqual(instance.original_url, _original_url)
        self.assertTrue(isinstance(instance.id, int))
        self.assertTrue(len(instance.short_code) > 0)

class ClientTestCase(TestCase):

    def setUp(self):
        self.credentials = {'username': 'teste', 'password': 'teste'}
        User.objects.create(**self.credentials)
        self.client = client.Client()

    def test_index_returns_status_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
