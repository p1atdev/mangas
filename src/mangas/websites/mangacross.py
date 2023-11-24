from ..url import URLConfig
from .giga_viewer import WebsiteMixin
from ..parsers.mangacross import (
    MangaCrossComicsParser,
    MangaCrossSeriesParser,
    MangaCrossEpisodeParser,
)


class MangaCross(WebsiteMixin):
    url: URLConfig = URLConfig(
        scheme="https",
        hostname="mangacross.jp",
    )

    # /api/comics.json
    comics_parser: type[MangaCrossComicsParser] = MangaCrossComicsParser

    # /api/comics/{comic_id}.json
    series_parser: type[MangaCrossSeriesParser] = MangaCrossSeriesParser

    def parse_comics(self):
        parser = MangaCrossComicsParser()
        output = parser.parse(
            self.url.compose(pathname="/api/comics.json"),
        )

        return output

    def parse_series(self, comic_id: str):
        parser = MangaCrossSeriesParser()
        output = parser.parse(
            self.url.compose(pathname=f"/api/comics/{comic_id}.json"),
        )

        return output

    def parse_episode(self, comic_id: str, episode_id: str | int):
        parser = MangaCrossEpisodeParser()
        output = parser.parse(
            self.url.compose(pathname=f"/comics/{comic_id}/{episode_id}/viewer.json")
        )

        return output

    # /comics/{comic_id}
    @staticmethod
    def _parse_comic_id(url: str) -> str:
        url_config = URLConfig.from_string(url)
        components = [c for c in url_config.pathname.split("/") if c.strip() != ""]
        assert len(components) >= 2

        comic_id = components[1]

        return comic_id

    # /comics/{comic_id}/{episode_id}
    @staticmethod
    def _parse_episode_id(url: str) -> str:
        url_config = URLConfig.from_string(url)
        components = [c for c in url_config.pathname.split("/") if c.strip() != ""]
        assert len(components) >= 3

        episode_id = components[2]

        return episode_id
