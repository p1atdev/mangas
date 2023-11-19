from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from ..parser_util import JSONParserMixin


class MangaCrossAllComicsDisplayName(Enum):
    大人 = "大人"
    少女 = "少女"
    少年 = "少年"


class MangaCrossAllComicsName(Enum):
    BOY = "boy"
    GIRL = "girl"
    YOUTH = "youth"


class MangaCrossAllComicsComicCategory(BaseModel):
    name: MangaCrossAllComicsName
    display_name: MangaCrossAllComicsDisplayName
    color: str


class MangaCrossAllComicsComicTag(BaseModel):
    name: str


class MangaCrossAllComicsComic(BaseModel):
    dir_name: str
    title: str
    title_kana: str
    author: str
    author_kana: str
    comic_tags: list[MangaCrossAllComicsComicTag]
    image_url: str
    image_double_url: str
    list_image_url: str
    list_image_double_url: str
    caption: str
    caption_for_search: str
    restricted: bool
    comic_category: MangaCrossAllComicsComicCategory | None = None
    latest_episode_publish_start: datetime | None = None


class MangaCrossAllComicsParseOutput(BaseModel):
    comics: list[MangaCrossAllComicsComic]
    current_count: int
    current_page: int
    total_count: int
    total_pages: int


class MangaCrossAllComicsParser(JSONParserMixin):
    url: str

    def parse(self):
        output = MangaCrossAllComicsParseOutput.model_validate_json(
            self._get_text(self.url)
        )
        return output
