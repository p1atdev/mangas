from base64 import b64decode
import math

from pydantic import BaseModel

from ..solver_utils import SolverMixin
from ...utils import ImageWrapper
from ...url import URLConfig


class IchijinPlusDRMConfig(BaseModel):
    BLOCK_WIDTH_NUM: int = 4
    BLOCK_HEIGHT_NUM: int = 4

    scrambled_positions: list[int]

    @classmethod
    def from_hash(cls, hash: str):
        decoded_bytes = b64decode(hash)
        [width, height, *scrambled_positions] = decoded_bytes
        assert width * height == len(scrambled_positions), "drm hash is invalid"
        return cls(
            BLOCK_WIDTH_NUM=width,
            BLOCK_HEIGHT_NUM=height,
            scrambled_positions=scrambled_positions,
        )


class IchijinPlusPuzzleSolver(SolverMixin):
    MULTIPLE: int = 8

    @staticmethod
    def parse_drm_hash(hash: str):
        return IchijinPlusDRMConfig.from_hash(hash)

    def solve_from_image(self, image: ImageWrapper, drm: IchijinPlusDRMConfig):
        np_image = image.to_numpy()
        solved_image = np_image.copy()

        height, width = np_image.shape[:2]
        block_width = math.floor((width - width % self.MULTIPLE) / drm.BLOCK_WIDTH_NUM)
        block_height = math.floor(
            (height - height % self.MULTIPLE) / drm.BLOCK_HEIGHT_NUM
        )

        for index, position in enumerate(drm.scrambled_positions):
            source_x = position % drm.BLOCK_WIDTH_NUM
            source_y = math.floor(position / drm.BLOCK_WIDTH_NUM)
            target_x = index % drm.BLOCK_WIDTH_NUM
            target_y = math.floor(index / drm.BLOCK_WIDTH_NUM)
            solved_image[
                block_height * target_y : block_height * (target_y + 1),
                block_width * target_x : block_width * (target_x + 1),
            ] = np_image[
                block_height * source_y : block_height * (source_y + 1),
                block_width * source_x : block_width * (source_x + 1),
            ]

        return ImageWrapper.from_numpy(solved_image)

    def solve_from_url(self, url: str):
        image = self._fetch_image(url)
        url_config = URLConfig.from_string(url)
        if "drm_hash" not in url_config.query:
            raise ValueError("drm_hash query is not found in url")
        drm_hash = url_config.query["drm_hash"]
        drm_config = self.parse_drm_hash(drm_hash)

        return self.solve_from_image(image, drm_config)
