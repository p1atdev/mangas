from ..url import URLConfig
from .website_utils import WebsiteMixin
from ..parsers.mangacross import (
    MangaCrossComicsParser,
    MangaCrossSeriesParser,
    MangaCrossEpisodeParser,
)

MangaCrossURL = URLConfig(
    scheme="https",
    hostname="mangacross.jp",
)


class MangaCross(WebsiteMixin):
    url: URLConfig = MangaCrossURL

    # /api/comics.json
    comics_parser: type[MangaCrossComicsParser] = MangaCrossComicsParser

    # /api/comics/{comic_id}.json
    series_parser: type[MangaCrossSeriesParser] = MangaCrossSeriesParser

    # /comics/{comic_id}/{episode_id}/viewer.json
    episode_parser: type[MangaCrossEpisodeParser] = MangaCrossEpisodeParser

    def parse_comics(self):
        parser = self.comics_parser(
            auth=self.auth,
        )
        output = parser.parse(
            self.url.compose(pathname="/api/comics.json"),
        )

        return output

    def parse_series(self, comic_id: str):
        parser = self.series_parser(
            auth=self.auth,
        )
        output = parser.parse(
            self.url.compose(pathname=f"/api/comics/{comic_id}.json"),
        )

        return output

    def parse_episode(self, comic_id: str, episode_id: str | int):
        parser = self.episode_parser(
            auth=self.auth,
        )
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
