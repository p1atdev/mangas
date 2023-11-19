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
        parser = MangaCrossAllComicsParser(
            url=self.url.compose(pathname="/api/comics.json"),
        )
        output = parser.parse()

        return output

    def parse_comic(self, comic_id: str):
        parser = MangaCrossComicParser(
            url=self.url.compose(pathname=f"/api/comics/{comic_id}.json"),
        )
        output = parser.parse()

        return output

    def parse_episode_viewer(self, comic_id: str, episode_id: str | int):
        parser = MangaCrossEpisodeViewerParser(
            url=self.url.compose(
                pathname=f"/comics/{comic_id}/{episode_id}/viewer.json"
            ),
        )
        output = parser.parse()

        return output
