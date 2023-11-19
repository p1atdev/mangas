from enum import Enum
from typing import Any, Literal
from datetime import datetime, date
from pydantic import BaseModel

from ..parser_utils import HTMLParserMixin
from ...url import URLConfig


class UraSundayTitlesTitle(BaseModel):
    url: str


class UraSundayTitlesParseOutput(BaseModel):
    titles: list[UraSundayTitlesTitle]


class UraSundayTitlesParser(HTMLParserMixin):
    def parse(self, url: str):
        text = self._get_soup(url)

        all_links_els = text.select(".title-all-list li a")
        all_links = [el.get("href") for el in all_links_els]
        all_links = [link for link in all_links if type(link) is str]

        config = URLConfig.from_string(url)

        titles = [
            UraSundayTitlesTitle(
                url=URLConfig(
                    scheme=config.scheme,
                    hostname=config.hostname,
                    pathname=link,
                ).compose(),
            )
            for link in all_links
        ]

        return UraSundayTitlesParseOutput(
            titles=titles,
        )
