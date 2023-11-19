import requests
import numpy as np

from pydantic import BaseModel

from ..auth import AuthConfigMixin, DefaultAuthConfig
from ..utils import MANGAS_CACHE_DIR, ImageWrapper


class SolverMixin(BaseModel):
    auth: AuthConfigMixin = DefaultAuthConfig

    cache_dir: str = MANGAS_CACHE_DIR

    def solve_from_image(self, image: ImageWrapper):
        raise NotImplementedError

    def solve_from_url(self, url: str):
        raise NotImplementedError

    def _fetch_image(self, url):
        res = requests.get(url, headers=self.auth.compose_headers(), stream=True)
        image = ImageWrapper.from_stream(res.iter_content())
        return image
