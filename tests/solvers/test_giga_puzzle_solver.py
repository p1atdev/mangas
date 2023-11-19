import unittest

from mangas.solvers import GigaPuzzleSolver

IMAGE_URLS = [
    "https://cdn-ak-img.shonenjumpplus.com/public/page/2/14079602755456178166-580ed8f8b8a042a028524f8052aecd16",
    "https://cdn-ak-img.shonenjumpplus.com/public/page/2/3269754496638383767-e4ef9b27f36b57af6def7a040a88d9fb",
    "https://cdn-img.comic-action.com/public/page/2/3270375685342463716-ae9711b20e947429c92f6cbcbecb681d",
]


class GigaPuzzleSolverTest(unittest.TestCase):
    def test_solve_images(self):
        solver = GigaPuzzleSolver()
        for url in IMAGE_URLS:
            image = solver.solve_from_url(url).to_pil()

            assert image is not None

            # image.show()


if __name__ == "__main__":
    unittest.main()
