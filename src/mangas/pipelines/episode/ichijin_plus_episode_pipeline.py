from PIL import Image
import numpy as np

from typing import Iterator, Literal

from ..pipeline_utils import PipelineMixin
from ...websites import IchijinPlus, IchijinPlusAuthConfig
from ...parsers import IchijinPlusEpisodeParseOutput
from ...solvers import IchijinPlusPuzzleSolver
from ...url import URLConfig
from ...utils import MANGAS_CACHE_DIR, ImageWrapper
from .episode_pipeline_utils import EpisodePipelineOutputMixin


class IchijinPlusEpisodeOutput(EpisodePipelineOutputMixin):
    parse_output: IchijinPlusEpisodeParseOutput
    solver: IchijinPlusPuzzleSolver

    # 漫画のページを難読化解除した状態で返す
    def images(
        self, type: Literal["pil", "np", "wrap"] = "pil"
    ) -> Iterator[Image.Image | np.ndarray | ImageWrapper]:
        if self.parse_output.pages is None:
            raise ValueError("pages is None")

        for page in self.parse_output.pages:
            image = self.solver.solve_from_url(
                url=page.page_image_url,
            )

            if type == "pil":
                yield image.to_pil()
            elif type == "np":
                yield image.to_numpy()
            elif type == "wrap":
                yield image
            else:
                raise ValueError(f"invalid type: {type}")


class IchijinPlusEpisodePipeline(PipelineMixin):
    website: IchijinPlus
    solver: IchijinPlusPuzzleSolver

    episode_id: str

    @classmethod
    def from_url(
        cls,
        url: str,
        auth: IchijinPlusAuthConfig = IchijinPlusAuthConfig.auto_setup(),
        cache_dir: str = MANGAS_CACHE_DIR,
    ):
        url_config = URLConfig.from_string(url)
        website = IchijinPlus(
            url=URLConfig(
                hostname=url_config.hostname,
            ),
            auth=auth,
            cache_dir=cache_dir,
        )
        episode_id = website._parse_episode_id(url)
        solver = IchijinPlusPuzzleSolver(
            auth=auth,
        )

        return cls(website=website, solver=solver, episode_id=episode_id)

    def __call__(
        self,
    ):
        episode = self.website.parse_episode(episode_id=self.episode_id)

        return IchijinPlusEpisodeOutput(
            parse_output=episode,
            solver=self.solver,
        )
