from ..solver_util import SolverMixin
from ...utils import ImageWrapper


class GigaPuzzleSolver(SolverMixin):
    DIVIDE_NUM: int = 4
    MULTIPLE: int = 8

    # transforms tiles like below:
    # \ABC    \dgj
    # d\ef -> A\hk
    # gh\i    Be\l
    # jkl\    Cfi\
    #
    # ◣◹ -> ◺◥
    #
    # see /tests/assets/0-q.jpg and 0-a.jpg see actual result
    def solve_from_image(self, image: ImageWrapper):
        np_image = image.to_numpy()

        height, width = np_image.shape[:2]
        cell_width = (width // (self.DIVIDE_NUM * self.MULTIPLE)) * self.MULTIPLE
        cell_height = (height // (self.DIVIDE_NUM * self.MULTIPLE)) * self.MULTIPLE

        for i in range(self.DIVIDE_NUM):
            for j in range(i + 1):
                (
                    np_image[
                        j * cell_height : (j + 1) * cell_height,
                        i * cell_width : (i + 1) * cell_width,
                    ],
                    np_image[
                        i * cell_height : (i + 1) * cell_height,
                        j * cell_width : (j + 1) * cell_width,
                    ],
                ) = (
                    np_image[
                        i * cell_height : (i + 1) * cell_height,
                        j * cell_width : (j + 1) * cell_width,
                    ].copy(),
                    np_image[
                        j * cell_height : (j + 1) * cell_height,
                        i * cell_width : (i + 1) * cell_width,
                    ].copy(),
                )

        return ImageWrapper.from_numpy(np_image)

    def solve_from_url(self, url: str):
        image = self._fetch_image(url)
        return self.solve_from_image(image)
