import unittest

from mangas.websites import MangaCross
from mangas.parsers import (
    MangaCrossComicsParser,
    MangaCrossSeriesParser,
    MangaCrossEpisodeViewerParser,
)
from mangas.auth import FirefoxPC, AuthConfigMixin
from mangas.url import URLConfig


COMIC_IDS = [
    "fairway",
    "watamaho",
    "kimigaro",
    "okaeri",
]

EPISODE_IDS = range(1, 3)


site = MangaCross()


class MangaCrossComicsParserTest(unittest.TestCase):
    def test_parse_all_comics(self):
        parser = MangaCrossComicsParser()
        output = parser.parse(
            url=site.url.compose(pathname="/api/comics.json"),
        )

        assert output is not None

    def test_parse_comic(self):
        for comic_id in COMIC_IDS:
            parser = MangaCrossSeriesParser()
            output = parser.parse(
                url=site.url.compose(pathname=f"/api/comics/{comic_id}.json"),
            )

            print(output.comic.title)

            assert output is not None

    def test_parse_episode_viewr(self):
        for comic_id in COMIC_IDS:
            for episode_id in EPISODE_IDS:
                parser = MangaCrossEpisodeViewerParser()
                output = parser.parse(
                    site.url.compose(
                        pathname=f"/comics/{comic_id}/{episode_id}/viewer.json"
                    )
                )

                print(output.comic.title, output.page_count)

                assert output is not None
                assert output.page_count == len(output.episode_pages)


if __name__ == "__main__":
    unittest.main()
