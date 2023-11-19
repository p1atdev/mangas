import requests
import numpy as np
from io import BytesIO

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
        res = requests.get(url, headers=self.auth.compose_headers())
        image = ImageWrapper.from_bytesio(BytesIO(res.content))
        return image


class SkipSolver(SolverMixin):
    def solve_from_image(self, image: ImageWrapper):
        return image

    def solve_from_url(self, url: str):
        return self._fetch_image(url)
