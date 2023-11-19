from ..solver_utils import SolverMixin
from ...utils import ImageWrapper
from ...auth import FirefoxMobile


# パズルを解かない
class GigaPuzzleSkipSolver(SolverMixin):
    def solve_from_image(self, image: ImageWrapper):
        return image

    def solve_from_url(self, url: str):
        image = self._fetch_image(url)
        return self.solve_from_image(image)
