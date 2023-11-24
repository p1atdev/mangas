import re

from typing import Literal
from pydantic import BaseModel

from ..parser_utils import HTMLParserMixin
from ...utils import load_js_object


class UraSundayEpisodeHTMLPage(BaseModel):
    html: str


class UraSundayEpisodeImagePage(BaseModel):
    src: str
    spread: Literal["single"] | None = None


class UraSundayEpisodeParseOutput(BaseModel):
    pages: list[UraSundayEpisodeImagePage | UraSundayEpisodeHTMLPage]


# https://urasunday.com/title/0000/00000 や https://urasunday.com/title/0000 など
class UraSundayEpisodeParser(HTMLParserMixin):
    script_selector: str = "body > script:nth-child(7)"
    script_pattern: str = r"const\s+pages\s*=\s*\[([^\]]*)\]"

    def parse(self, url: str):
        soup = self._get_soup(url)

        target_script = soup.select_one(self.script_selector)
        assert target_script is not None

        inner_text = target_script.string
        assert inner_text is not None

        # マッチを検索
        match = re.search(self.script_pattern, inner_text)

        if match:
            pages_value = match.group(1)
            assert pages_value is not None

            pages = load_js_object(f"[{pages_value}]")

        else:
            raise ValueError("match is None")

        return UraSundayEpisodeParseOutput.model_validate({"pages": pages})
