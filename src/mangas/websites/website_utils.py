from pydantic import BaseModel

from ..url import URLConfig
from ..auth import AuthConfigMixin, DefaultAuthConfig
from ..utils import MANGAS_CACHE_DIR
from ..parsers import ParserMixin


class WebsiteMixin(BaseModel):
    url: URLConfig
    auth: AuthConfigMixin = DefaultAuthConfig

    parser: type[ParserMixin] = ParserMixin

    cache_dir: str = MANGAS_CACHE_DIR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
