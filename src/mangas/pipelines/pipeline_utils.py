from pydantic import BaseModel

from ..auth import AuthConfigMixin, DefaultAuthConfig
from ..utils import MANGAS_CACHE_DIR


class PipelineMixin(BaseModel):
    auth: AuthConfigMixin = DefaultAuthConfig

    cache_dir: str = MANGAS_CACHE_DIR
