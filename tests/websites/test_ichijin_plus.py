import unittest

from mangas.websites import IchijinPlus

COMIC_IDS = ["49461344665806", "2406857801750", "67585341292776"]

EPISODE_IDS = ["67705093080099", "49869036978995", "2886942130261", "7129295356145"]


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

    def test_parse_series(self):
        site = IchijinPlus()

        for comic_id in COMIC_IDS:
            output = site.parse_series(comic_id=comic_id)

            assert output.id == comic_id

            print(output.title)

    def test_parse_episode(self):
        site = IchijinPlus()

        for episode_id in EPISODE_IDS:
            output = site.parse_episode(episode_id=episode_id)

            assert output.episode_id == episode_id

            print(output.comic_title, output.episode_title)
