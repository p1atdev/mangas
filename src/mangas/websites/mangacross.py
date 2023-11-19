from ..url import URLConfig
from .giga_viewer import WebsiteMixin
from ..parsers.mangacross import (
    MangaCrossAllComicsParser,
    MangaCrossComicParser,
    MangaCrossEpisodeViewerParser,
)


class MangaCross(WebsiteMixin):
    url: URLConfig = URLConfig(
        scheme="https",
        hostname="mangacross.jp",
    )

    # /api/comics.json
    all_comics_parser: type[MangaCrossAllComicsParser] = MangaCrossAllComicsParser

    # /api/comics/{comic_id}.json
    comic_parser: type[MangaCrossComicParser] = MangaCrossComicParser

    def parse_all_comics(self):
        parser = MangaCrossAllComicsParser()
        output = parser.parse(
            self.url.compose(pathname="/api/comics.json"),
        )

        return output

    def parse_comic(self, comic_id: str):
        parser = MangaCrossComicParser()
        output = parser.parse(
            self.url.compose(pathname=f"/api/comics/{comic_id}.json"),
        )

        return output

    def parse_episode_viewer(self, comic_id: str, episode_id: str | int):
        parser = MangaCrossEpisodeViewerParser()
        output = parser.parse(
            self.url.compose(pathname=f"/comics/{comic_id}/{episode_id}/viewer.json")
        )

        return output

    # /comics/{comic_id}
    def _parse_comic_id(self, url: str) -> str:
        url_config = URLConfig.from_string(url)
        components = [c for c in url_config.pathname.split("/") if c.strip() != ""]
        assert len(components) >= 2

        comic_id = components[1]

        return comic_id

    # /comics/{comic_id}/{episode_id}
    def _parse_episode_id(self, url: str) -> str:
        url_config = URLConfig.from_string(url)
        components = [c for c in url_config.pathname.split("/") if c.strip() != ""]
        assert len(components) >= 3

        episode_id = components[2]

        return episode_id
