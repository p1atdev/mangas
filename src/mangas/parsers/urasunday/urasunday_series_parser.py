from enum import Enum
from typing import Any, Literal
from datetime import datetime, date
from pydantic import BaseModel

from ..parser_utils import HTMLParserMixin
from ...url import URLConfig


class UraSundaySeriesEpisode(BaseModel):
    url: str
    image: str


class UraSundaySeriesParseOutput(BaseModel):
    episodes: list[UraSundaySeriesEpisode]


class UraSundaySeriesParser(HTMLParserMixin):
    def parse(self, url: str):
        text = self._get_soup(url)

        links_els = text.select("div.chapter > ul > li > a")
        links = [el.get("href") for el in links_els]
        links = [link for link in links if type(link) is str]

        images_els = text.select("div.chapter > ul > li > a > img")
        images = [el.get("src") for el in images_els]
        images = [image for image in images if type(image) is str]

        assert len(links) == len(images)

        config = URLConfig.from_string(url)

        episodes = [
            UraSundaySeriesEpisode(
                url=URLConfig(
                    scheme=config.scheme,
                    hostname=config.hostname,
                    pathname=link,
                ).compose(),
                image=image,
            )
            for link, image in zip(links, images)
        ]

        return UraSundaySeriesParseOutput(
            episodes=episodes,
        )
