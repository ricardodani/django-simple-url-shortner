from django.test import SimpleTestCase, override_settings
from urlshortener.converter import (
    Base62UrlCodeEncoder,
    HmacUrlCodeEncoder,
    RandomUrlCodeEncoder,
    ShortHmacUrlCodeEncoder,
    num_to_base62,
)


class Base62Tests(SimpleTestCase):
    def test_base62_encoder_implements_the_url_code_contract(self):
        self.assertEqual(Base62UrlCodeEncoder().encode(62), "10")

    def test_random_encoder_generates_unpredictable_alphanumeric_codes(self):
        encoder = RandomUrlCodeEncoder()

        first_code = encoder.encode(1)
        second_code = encoder.encode(2)

        self.assertEqual(len(first_code), 16)
        self.assertTrue(first_code.isascii())
        self.assertTrue(first_code.isalnum())
        self.assertNotEqual(first_code, second_code)

    def test_hmac_encoder_returns_stable_128_bit_codes(self):
        encoder = HmacUrlCodeEncoder()

        first_code = encoder.encode(123)
        repeated_code = HmacUrlCodeEncoder().encode(123)

        self.assertEqual(len(first_code), 22)
        self.assertTrue(first_code.isascii())
        self.assertTrue(first_code.isalnum())
        self.assertEqual(first_code, repeated_code)

    def test_hmac_encoder_uses_django_secret_key(self):
        with override_settings(SECRET_KEY="first-secret"):
            first_code = HmacUrlCodeEncoder().encode(123)
        with override_settings(SECRET_KEY="second-secret"):
            second_code = HmacUrlCodeEncoder().encode(123)

        self.assertNotEqual(first_code, second_code)

    def test_short_hmac_encoder_returns_eight_characters(self):
        code = ShortHmacUrlCodeEncoder().encode(123)

        self.assertEqual(len(code), 8)
        self.assertTrue(code.isalnum())

    def test_encodes_zero(self):
        self.assertEqual(num_to_base62(0), "0")

    def test_encodes_base62_boundaries(self):
        self.assertEqual(num_to_base62(61), "Z")
        self.assertEqual(num_to_base62(62), "10")
        self.assertEqual(num_to_base62(3843), "ZZ")

    def test_preserves_existing_lowercase_then_uppercase_alphabet(self):
        self.assertEqual(num_to_base62(10), "a")
        self.assertEqual(num_to_base62(35), "z")
        self.assertEqual(num_to_base62(61), "Z")

    def test_encodes_large_integers_without_float_conversion(self):
        self.assertEqual(num_to_base62(62**30), "1" + ("0" * 30))

    def test_rejects_negative_numbers(self):
        with self.assertRaisesRegex(ValueError, "non-negative"):
            num_to_base62(-1)
