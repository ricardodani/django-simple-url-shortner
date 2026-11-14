from django.test import SimpleTestCase
from urlshortener.converter import num_to_base62


class Base62Tests(SimpleTestCase):
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
