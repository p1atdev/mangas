import unittest

from mangas.websites import IchijinPlus


class IchijinPlusTest(unittest.TestCase):
    def test_init_website(self):
        site = IchijinPlus()

        assert site.url.compose() == "https://ichijin-plus.com"
        assert site.auth.env_key is not None

        print(site.auth.env_key)

    def test_parse_comics(self):
        site = IchijinPlus()

        output = site.parse_comics()

        assert output.next_cursor is not None

        print(output.resources[0].title)

    def test_parse_comics_multi_time(self):
        site = IchijinPlus()

        first_output = site.parse_comics(
            limit=24,
            nsfw=False,
            order="asc",
            sort="title_yomigana",
            after_than=None,
        )
        assert first_output.next_cursor is not None

        cursor = first_output.next_cursor

        second_output = site.parse_comics(
            limit=24,
            nsfw=True,
            order="asc",
            sort="title_yomigana",
            after_than=cursor,
        )
        assert second_output.next_cursor is not None

        print(first_output.resources[0].title)
        print(second_output.resources[0].title)

        assert first_output.resources[0].title != second_output.resources[0].title
