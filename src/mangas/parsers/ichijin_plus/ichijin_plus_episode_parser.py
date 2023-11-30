from pydantic import BaseModel, field_validator

from ..parser_utils import JSONParserMixin


class IchijinPlusEpisodePage(BaseModel):
    id: str
    episode_id: str
    drm_hash: str
    page_image_url: str


class IchijinPlusEpisodeParseOutput(BaseModel):
    comic_id: str
    comic_title: str
    comic_description: str
    comic_good_count: int
    comic_nsfw_type: str
    episode_id: str
    episode_status: str
    episode_title: str
    episode_thumbnail_image_url: str
    episode_price: int
    episode_expire_seconds: None
    episode_promotion: str
    page_direction: str
    is_first_view_spread: bool
    pages: list[IchijinPlusEpisodePage]


class IchijinPlusEpisodeParser(JSONParserMixin):
    def parse(self, url: str):
        output = IchijinPlusEpisodeParseOutput.model_validate_json(self._get_text(url))
        return output
