from pathlib import Path
from PIL import Image
import numpy as np


from typing import Iterator, Literal
from pydantic import BaseModel

from ..pipeline_utils import PipelineMixin
from ...websites import UraSunday
from ...parsers import UraSundayEpisodeParseOutput, UraSundayEpisodeImagePage
from ...solvers import SkipSolver
from ...url import URLConfig
from ...auth import AuthConfigMixin
from ...utils import MANGAS_CACHE_DIR, ImageWrapper


class UraSundayEpisodeOutput(BaseModel):
    parse_output: UraSundayEpisodeParseOutput
    solver: SkipSolver

    # 漫画のページを難読化解除した状態で返す
    def images(
        self, type: Literal["pil", "np", "wrap"] = "pil"
    ) -> Iterator[Image.Image | np.ndarray | ImageWrapper]:
        if self.parse_output.pages is None:
            raise ValueError("pages is None")

        for page in self.parse_output.pages:
            if not isinstance(page, UraSundayEpisodeImagePage):
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


class UraSundayEpisodePipeline(PipelineMixin):
    website: UraSunday
    solver: SkipSolver

    title_id: str
    episode_id: str | None

    @classmethod
    def from_url(
        cls,
        url: str,
        auth: AuthConfigMixin = AuthConfigMixin(),
        cache_dir: str = MANGAS_CACHE_DIR,
    ):
        url_config = URLConfig.from_string(url)
        website = UraSunday(
            url=URLConfig(
                hostname=url_config.hostname,
            ),
            auth=auth,
            cache_dir=cache_dir,
        )

        title_id = website._parse_title_id(url)
        episode_id = website._parse_episode_id(url)

        solver = SkipSolver(
            auth=auth,
        )

        return cls(
            website=website, solver=solver, title_id=title_id, episode_id=episode_id
        )

    def __call__(
        self,
    ):
        episode = self.website.parse_episode(
            title_id=self.title_id, episode_id=self.episode_id
        )

        return UraSundayEpisodeOutput(
            parse_output=episode,
            solver=self.solver,
        )
