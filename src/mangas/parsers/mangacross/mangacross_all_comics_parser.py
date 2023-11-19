from typing import Literal
from datetime import datetime
from pydantic import BaseModel

from ..parser_utils import JSONParserMixin


class MangaCrossAllComicsComicCategory(BaseModel):
    name: Literal["boy", "girl", "youth"]
    display_name: Literal["少年", "少女", "大人"]
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
    def parse(self, url: str):
        output = MangaCrossAllComicsParseOutput.model_validate_json(self._get_text(url))
        return output
