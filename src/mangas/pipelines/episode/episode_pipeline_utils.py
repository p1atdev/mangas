from PIL import Image
import numpy as np

from typing import Iterator, Literal
from pydantic import BaseModel

from ...solvers import SolverMixin
from ...utils import MANGAS_CACHE_DIR, ImageWrapper


class EpisodePipelineOutputMixin(BaseModel):
    parse_output: BaseModel
    solver: SolverMixin

    def images(
        self, type: Literal["pil", "np", "wrap"] = "pil"
    ) -> Iterator[Image.Image | np.ndarray | ImageWrapper]:
        raise NotImplementedError()
