from pathlib import Path
from PIL import Image
import numpy as np


from typing import Iterator, Literal
from pydantic import BaseModel

from ..pipeline_utils import PipelineMixin
from ...websites import MangaCross
from ...parsers import MangaCrossEpisodeParseOutput
from ...solvers import SkipSolver
from ...url import URLConfig
from ...auth import AuthConfigMixin, ChromePC, SafariMobile
from ...utils import MANGAS_CACHE_DIR, ImageWrapper


class MangaCrossEpisodeOutput(BaseModel):
    parse_output: MangaCrossEpisodeParseOutput
    solver: SkipSolver

    # 漫画のページを難読化解除した状態で返す
    def images(
        self, type: Literal["pil", "np", "wrap"] = "pil"
    ) -> Iterator[Image.Image | np.ndarray | ImageWrapper]:
        if self.parse_output.episode_pages is None:
            raise ValueError("page_structure is None")

        for page in self.parse_output.episode_pages:
            image = self.solver.solve_from_url(
                url=page.image.pc_url,
            )

            if type == "pil":
                yield image.to_pil()
            elif type == "np":
                yield image.to_numpy()
            elif type == "wrap":
                yield image
            else:
                raise ValueError(f"invalid type: {type}")


class MangaCrossEpisodePipeline(PipelineMixin):
    website: MangaCross
    solver: SkipSolver

    comic_id: str
    episode_id: str

    @classmethod
    def from_url(
        cls,
        url: str,
        auth: AuthConfigMixin = AuthConfigMixin(user_agent=ChromePC.user_agent),
        cache_dir: str = MANGAS_CACHE_DIR,
    ):
        url_config = URLConfig.from_string(url)
        website = MangaCross(
            url=URLConfig(
                hostname=url_config.hostname,
            ),
            auth=auth,
            cache_dir=cache_dir,
        )
        comic_id = website._parse_comic_id(url)
        episode_id = website._parse_episode_id(url)
        solver = SkipSolver(
            auth=auth,
        )

        return cls(
            website=website, solver=solver, comic_id=comic_id, episode_id=episode_id
        )

    def __call__(
        self,
    ):
        episode = self.website.parse_episode(
            comic_id=self.comic_id, episode_id=self.episode_id
        )

        return MangaCrossEpisodeOutput(
            parse_output=episode,
            solver=self.solver,
        )
