from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from urlshortener.models import Url


class UrlViewIntegrationTests(TestCase):
    def test_homepage_renders_for_anonymous_users(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shorten URL")

    def test_anonymous_user_can_create_and_follow_a_short_url(self):
        response = self.client.post(
            reverse("index"),
            {"original_url": "https://example.com/python"},
        )
        url = Url.objects.get()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, url.short_code)
        self.assertIsNone(url.user)

        redirect_response = self.client.get(url.get_absolute_url())

        self.assertEqual(redirect_response.status_code, 301)
        self.assertEqual(
            redirect_response.headers["Location"],
            "https://example.com/python",
        )

    def test_authenticated_user_owns_created_url(self):
        user = get_user_model().objects.create_user(username="ricardo")
        self.client.force_login(user)

        response = self.client.post(
            reverse("index"),
            {"original_url": "https://example.com/private"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Url.objects.get().user, user)

    def test_invalid_url_does_not_create_a_record(self):
        response = self.client.post(
            reverse("index"),
            {"original_url": "not a URL"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "URL not valid.")
        self.assertFalse(Url.objects.exists())

    def test_missing_short_code_returns_404(self):
        response = self.client.get("/not-a-stored-code")

        self.assertEqual(response.status_code, 404)

    def test_registration_logs_the_new_user_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-user",
                "password1": "A-strong-password-123!",
                "password2": "A-strong-password-123!",
            },
        )

        self.assertRedirects(response, reverse("index"))
        self.assertTrue(
            self.client.session.get("_auth_user_id"),
        )

    def test_logout_requires_post_and_logs_the_user_out(self):
        user = get_user_model().objects.create_user(username="url-owner")
        self.client.force_login(user)

        get_response = self.client.get(reverse("logout"))
        post_response = self.client.post(reverse("logout"))

        self.assertEqual(get_response.status_code, 405)
        self.assertRedirects(post_response, "/")
        self.assertNotIn("_auth_user_id", self.client.session)
