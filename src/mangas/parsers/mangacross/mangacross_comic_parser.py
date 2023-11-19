from enum import Enum
from typing import Any
from datetime import datetime, date
from pydantic import BaseModel

from ..parser_util import JSONParserMixin


class MangaCrossComicPurchaseURL(BaseModel):
    amazon: str
    rakuten: str


class MangaCrossComicBook(BaseModel):
    id: int
    isbn: str
    title: str
    author: str
    cover_url: str
    release_date: date
    purchase_url: MangaCrossComicPurchaseURL


class MangaCrossComicComicCategory(BaseModel):
    name: str
    display_name: str
    color: str


class MangaCrossComicComicTag(BaseModel):
    name: str


class MangaCrossComicOgpURL(Enum):
    EPISODE_OGPS_ORIGINAL_MISSING_PNG = "/episode_ogps/original/missing.png"


class MangaCrossComicStatus(Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class MangaCrossComicEpisode(BaseModel):
    id: int
    volume: str
    sort_volume: int
    page_count: int
    title: str
    publish_start: datetime
    member_publish_start: datetime
    status: MangaCrossComicStatus
    page_url: str
    ogp_url: MangaCrossComicOgpURL
    list_image_url: str
    list_image_double_url: str
    episode_next_date: datetime | None
    next_date_customize_text: str
    is_unlimited_comic: bool
    publish_end: datetime | None = None
    member_publish_end: datetime | None = None


class MangaCrossComicPromotion(BaseModel):
    title: None
    content: None


class MangaCrossComicRelatedComic(BaseModel):
    dir_name: str
    title: str
    title_kana: str
    author: str
    author_kana: str
    comic_category: MangaCrossComicComicCategory
    comic_tags: list[MangaCrossComicComicTag]
    image_url: str
    image_double_url: str
    list_image_url: str
    list_image_double_url: str
    caption: str
    caption_for_search: str
    latest_episode_publish_start: datetime | None
    restricted: bool


class MangaCrossComic(BaseModel):
    dir_name: str
    title: str
    title_kana: str
    author: str
    author_kana: str
    comic_category: MangaCrossComicComicCategory
    comic_tags: list[MangaCrossComicComicTag]
    image_url: str
    image_double_url: str
    list_image_url: str
    list_image_double_url: str
    caption: str
    caption_for_search: str
    latest_episode_publish_start: datetime | None
    restricted: bool
    series: bool
    seo_word_common: str
    seo_word_comic: str
    seo_word_episode: str
    seo_outline: str
    ad_lating: int
    outline: str
    comic_url: str
    large_image_url: str
    image_sp_url: str
    logo_url: str
    background_url: str
    ogp_url: str
    icon_url: str
    tw_hashtag: str
    tw_screen_name: str
    next_publish_at: datetime
    next_date_customize_text: str
    promotion: MangaCrossComicPromotion
    is_unlimited_comic: bool
    unlimited_event_singles: list[Any]
    episodes: list[MangaCrossComicEpisode]
    books: list[MangaCrossComicBook]
    related_comics: list[MangaCrossComicRelatedComic]


class MangaCrossComicParseOutput(BaseModel):
    comic: MangaCrossComic


class MangaCrossComicParser(JSONParserMixin):
    url: str

    def parse(self):
        output = MangaCrossComicParseOutput.model_validate_json(
            self._get_text(self.url)
        )
        return output
