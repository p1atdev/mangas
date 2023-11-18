import unittest

from mangas.url import URLConfig


class URLConfigTest(unittest.TestCase):
    def test_init_url(self):
        url = URLConfig(
            scheme="https",
            domain="shonenjumpplus.com",
        )

        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.domain, "shonenjumpplus.com")

    def test_compose(self):
        url = URLConfig(
            scheme="https",
            domain="shonenjumpplus.com",
        )

        self.assertEqual(url.compose(), "https://shonenjumpplus.com")
        self.assertEqual(url.compose("atom"), "https://shonenjumpplus.com/atom")
