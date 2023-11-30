import requests
from bs4 import BeautifulSoup, Tag

from typing import Literal

from ..url import URLConfig
from .website_utils import WebsiteMixin
from ..auth import AuthConfigMixin
from ..parsers import (
    IchijinPlusComicsParser,
    IchijinPlusComicsSortBy,
    IchijinPlusComicsSortOrder,
    IchijinPlusSeriesParser,
    IchijinPlusEpisodeParser,
)

IchijinPlusURL = URLConfig(
    scheme="https",
    hostname="ichijin-plus.com",
)
IchijinPlusAPIURL = URLConfig(
    scheme="https",
    hostname="api.ichijin-plus.com",
)


class IchijinPlusAuthConfig(AuthConfigMixin):
    env_key: str

    _url: URLConfig = IchijinPlusURL

    def compose_headers(self) -> dict[str, str]:
        headers = super().compose_headers()
        headers["X-API-Environment-Key"] = self.env_key
        return headers

    @classmethod
    def auto_setup(cls) -> "IchijinPlusAuthConfig":
        app_js = cls._fetch_app_js()
        env = cls._fetch_env(app_js)
        return cls(env_key=env)

    # script src = /_next/static/chunks/pages/_app-[random hash].js
    @staticmethod
    def _fetch_app_js() -> str:
        index_html = requests.get(url=IchijinPlusURL.compose()).text
        index_soup = BeautifulSoup(index_html, "lxml")

        app_js_script = index_soup.find(
            "script",
            {"src": lambda x: x and x.startswith("/_next/static/chunks/pages/_app-")},
        )
        assert isinstance(app_js_script, Tag)

        app_js_url = IchijinPlusURL.compose(pathname=app_js_script["src"])
        app_js = requests.get(url=app_js_url).text

        return app_js

    # n.env.NEXT_PUBLIC_IS_TEST,o="https://api.ichijin-plus.com",s="G-3BX3CGCYSR",a="https://ichijin-plus.com",l="GGXGejnSsZw-IxHKQp8OQKHH-NDItSbEq5PU0g2w1W4="}
    @staticmethod
    def _fetch_env(app_js: str) -> str:
        env = app_js.split(',a="https://ichijin-plus.com",l="')[1].split('"}')[0]
        return env


class IchijinPlus(WebsiteMixin):
    auth: IchijinPlusAuthConfig = IchijinPlusAuthConfig.auto_setup()
    url: URLConfig = IchijinPlusURL
    api_url: URLConfig = IchijinPlusAPIURL

    comics_parser: type[IchijinPlusComicsParser] = IchijinPlusComicsParser
    series_parser: type[IchijinPlusSeriesParser] = IchijinPlusSeriesParser
    episode_parser: type[IchijinPlusEpisodeParser] = IchijinPlusEpisodeParser

    def parse_comics(
        self,
        limit: int = 100,
        nsfw: bool = True,
        order: IchijinPlusComicsSortOrder = "asc",
        sort: IchijinPlusComicsSortBy = "title_yomigana",
        after_than: str | None = None,
    ):
        parser = self.comics_parser(
            auth=self.auth,
        )
        output = parser.parse(
            self.api_url.compose(
                pathname="/comics",
                query={
                    "limit": limit,
                    "nsfw": "all" if nsfw else None,
                    "order": order,
                    "sort": sort,
                    "after_than": after_than,
                },
            ),
        )

        return output

    def parse_series(self, comic_id: str):
        parser = self.series_parser(
            auth=self.auth,
        )
        output = parser.parse(
            self.api_url.compose(
                pathname=f"/comics/{comic_id}",
            ),
        )

        return output

    def parse_episode(self, episode_id: str):
        parser = self.episode_parser(
            auth=self.auth,
        )
        output = parser.parse(
            self.api_url.compose(
                pathname=f"/episodes/{episode_id}/begin_reading",
            ),
        )

        return output
