from typing import Literal
from datetime import datetime
from pydantic import BaseModel

from ..parser_utils import JSONParserMixin


class MangaCrossComicsComicCategory(BaseModel):
    name: Literal["boy", "girl", "youth"]
    display_name: Literal["少年", "少女", "大人"]
    color: str


class MangaCrossComicsComicTag(BaseModel):
    name: str


class MangaCrossComicsComic(BaseModel):
    dir_name: str
    title: str
    title_kana: str
    author: str
    author_kana: str
    comic_tags: list[MangaCrossComicsComicTag]
    image_url: str
    image_double_url: str
    list_image_url: str
    list_image_double_url: str
    caption: str
    caption_for_search: str
    restricted: bool
    comic_category: MangaCrossComicsComicCategory | None = None
    latest_episode_publish_start: datetime | None = None


class MangaCrossComicsParseOutput(BaseModel):
    comics: list[MangaCrossComicsComic]
    current_count: int
    current_page: int
    total_count: int
    total_pages: int


class MangaCrossComicsParser(JSONParserMixin):
    def parse(self, url: str):
        output = MangaCrossComicsParseOutput.model_validate_json(self._get_text(url))
        return output
