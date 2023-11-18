import unittest

from mangas.url import URLConfig


class URLConfigTest(unittest.TestCase):
    def test_init_url(self):
        url = URLConfig(
            scheme="https",
            domain="shonenjumpplus.com",
        )

        assert url.scheme == "https"
        assert url.domain == "shonenjumpplus.com"

    def test_compose(self):
        url = URLConfig(
            scheme="https",
            domain="shonenjumpplus.com",
        )

        assert url.compose() == "https://shonenjumpplus.com"
        assert url.compose("atom") == "https://shonenjumpplus.com/atom"


if __name__ == "__main__":
    unittest.main()
