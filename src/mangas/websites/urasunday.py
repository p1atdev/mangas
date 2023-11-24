import re

from ..url import URLConfig
from .website_utils import WebsiteMixin
from ..parsers import UraSundayEpisodeParser, UraSundayTitlesParser


# https://urasunday.com
class UraSunday(WebsiteMixin):
    url: URLConfig = URLConfig(
        scheme="https",
        hostname="urasunday.com",
    )

    titles_parser: type[UraSundayTitlesParser] = UraSundayTitlesParser

    episode_parser: type[UraSundayEpisodeParser] = UraSundayEpisodeParser

    def parse_titles(self, pathname: str):
        parser = self.titles_parser(
            auth=self.auth,
        )
        output = parser.parse(
            self.url.compose(
                pathname=pathname,
            ),
        )

        return output

    def parse_serial_titles(self):
        return self.parse_titles(pathname="/serial_title")

    def parse_complete_titles(self):
        return self.parse_titles(pathname="/complete_title")

    def parse_episode(self, title_id: str, episode_id: str | None = None):
        parser = self.episode_parser(
            auth=self.auth,
        )
        episode_id = episode_id or ""
        output = parser.parse(
            self.url.compose(
                pathname=f"/title/{title_id}/{episode_id}",
            ),
        )

        return output

    @staticmethod
    def _parse_title_id(url: str) -> str:
        # /title/1234
        path = URLConfig.from_string(url).pathname
        match = re.search(r"/title/(\d+)", path)
        assert match is not None
        return match.group(1)

    @staticmethod
    def _parse_episode_id(url: str) -> str | None:
        # /title/1234/5678 or /title/1234
        path = URLConfig.from_string(url).pathname
        match = re.search(r"/title/\d+/(\d+)", path)
        if match is None:
            return None

        return match.group(1)
