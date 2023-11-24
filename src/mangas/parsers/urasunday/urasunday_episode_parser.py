import re

from typing import Literal
from pydantic import BaseModel

from bs4 import BeautifulSoup

from ..parser_utils import HTMLParserMixin
from ...utils import load_js_object


class UraSundayEpisodeHTMLPage(BaseModel):
    html: str


class UraSundayEpisodeImagePage(BaseModel):
    src: str
    spread: Literal["single"] | None = None


class UraSundayEpisodeParseOutput(BaseModel):
    title_name: str
    episode_name: str
    description: str

    pages: list[UraSundayEpisodeImagePage | UraSundayEpisodeHTMLPage]


# https://urasunday.com/title/0000/00000 や https://urasunday.com/title/0000 など
class UraSundayEpisodeParser(HTMLParserMixin):
    script_selector: str = "body > script:nth-child(7)"
    script_pattern: str = r"const\s+pages\s*=\s*\[([^\]]*)\]"

    def parse(self, url: str):
        soup = self._get_soup(url)

        pages = self._parse_pages(soup)
        title_name = self._parse_title_name(soup)
        episode_name = self._parse_episode_name(soup)
        description = self._parse_description(soup)

        return UraSundayEpisodeParseOutput.model_validate(
            {
                "title_name": title_name,
                "episode_name": episode_name,
                "description": description,
                "pages": pages,
            }
        )

    def _parse_pages(self, soup: BeautifulSoup):
        target_script = soup.select_one(self.script_selector)
        assert target_script is not None

        inner_text = target_script.string
        assert inner_text is not None

        match = re.search(self.script_pattern, inner_text)

        if match:
            pages_value = match.group(1)
            assert pages_value is not None

            pages = load_js_object(f"[{pages_value}]")

        else:
            raise ValueError("match is None")

        return pages

    def _parse_title_name(self, soup: BeautifulSoup):
        title_el = soup.select_one("div.info > h1")
        assert title_el is not None
        title_name = title_el.string
        assert isinstance(title_name, str)

        return title_name.strip()

    def _parse_episode_name(self, soup: BeautifulSoup):
        episode_name_el = soup.select_one(
            ".title > div:nth-child(1) > div:nth-child(1)"
        )
        assert episode_name_el is not None
        episode_name = episode_name_el.string
        assert isinstance(episode_name, str)

        return episode_name.strip()

    def _parse_description(self, soup: BeautifulSoup):
        description_el = soup.select_one('meta[name="description"]')
        assert description_el is not None

        description = description_el["content"]
        assert isinstance(description, str)

        return description.strip()
