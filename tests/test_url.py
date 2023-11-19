import unittest

from mangas.url import URLConfig


class URLConfigTest(unittest.TestCase):
    def test_init_url(self):
        url = URLConfig(
            scheme="https",
            hostname="shonenjumpplus.com",
        )

        assert url.scheme == "https"
        assert url.hostname == "shonenjumpplus.com"

    def test_compose(self):
        url = URLConfig(
            scheme="https",
            hostname="shonenjumpplus.com",
        )

        assert url.compose() == "https://shonenjumpplus.com"
        assert url.compose("atom") == "https://shonenjumpplus.com/atom"

    def test_from_string(self):
        urls = [
            "https://shonenjumpplus.com",
            "https://shonenjumpplus.com/atom",
            "https://shonenjumpplus.com/atom/series/4856001361048451884",
            "https://shonenjumpplus.com/atom/series/4856001361048451884?free_only=1",
        ]

        for url in urls:
            print(url)
            url_config = URLConfig.from_string(url)
            print("composed", url_config.compose())
            assert url_config.compose() == url


if __name__ == "__main__":
    unittest.main()
