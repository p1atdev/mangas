from pathlib import Path
from PIL import Image
import numpy as np


from typing import Iterator, Literal
from pydantic import BaseModel

from ..pipeline_utils import PipelineMixin
from ...websites import GigaViewer
from ...parsers import GigaEpisodeParseOutput
from ...solvers import GigaPuzzleSolver
from ...url import URLConfig
from ...auth import AuthConfigMixin, ChromePC, SafariMobile
from ...utils import MANGAS_CACHE_DIR, ImageWrapper


class GigaEpisodeOutput(BaseModel):
    parse_output: GigaEpisodeParseOutput
    solver: GigaPuzzleSolver

    # 漫画のページを難読化解除した状態で返す
    def images(
        self, type: Literal["pil", "np", "wrap"] = "pil"
    ) -> Iterator[Image.Image | np.ndarray | ImageWrapper]:
        if self.parse_output.readable_product.page_structure is None:
            raise ValueError("page_structure is None")

        for page in self.parse_output.readable_product.page_structure.pages:
            if page.type != "main" or page.src is None:
                continue

            image = self.solver.solve_from_url(
                url=page.src,
            )

            if type == "pil":
                yield image.to_pil()
            elif type == "np":
                yield image.to_numpy()
            elif type == "wrap":
                yield image
            else:
                raise ValueError(f"invalid type: {type}")


class GigaEpisodePipeline(PipelineMixin):
    website: GigaViewer
    solver: GigaPuzzleSolver

    episode_id: str

    @classmethod
    def from_url(
        cls,
        url: str,
        auth: AuthConfigMixin = AuthConfigMixin(user_agent=ChromePC.user_agent),
        cache_dir: str = MANGAS_CACHE_DIR,
    ):
        url_config = URLConfig.from_string(url)
        website = GigaViewer(
            url=URLConfig(
                hostname=url_config.hostname,
            ),
            auth=auth,
            cache_dir=cache_dir,
        )
        episode_id = website._parse_episode_id(url=url)
        solver = GigaPuzzleSolver(
            auth=auth,
        )

        return cls(website=website, solver=solver, episode_id=episode_id)

    def __call__(
        self,
    ):
        episode = self.website.parse_episode_json(episode_id=self.episode_id)

        return GigaEpisodeOutput(
            parse_output=episode,
            solver=self.solver,
        )
