import unittest

from mangas.auth import SafariMobile, AuthConfigMixin
from mangas.parsers import GigaEpisodeParser
from mangas.solvers import GigaPuzzleSolver, GigaPuzzleSkipSolver

IMAGE_URLS = [
    "https://cdn-ak-img.shonenjumpplus.com/public/page/2/14079602755456178166-580ed8f8b8a042a028524f8052aecd16",
    "https://cdn-ak-img.shonenjumpplus.com/public/page/2/3269754496638383767-e4ef9b27f36b57af6def7a040a88d9fb",
    "https://cdn-img.comic-action.com/public/page/2/3270375685342463716-ae9711b20e947429c92f6cbcbecb681d",
]

EPISODE_URLS = ["https://comic-action.com/episode/14079602755395095361.json"]


class GigaPuzzleSolverTest(unittest.TestCase):
    def test_solve_images(self):
        solver = GigaPuzzleSolver()
        for url in IMAGE_URLS:
            image = solver.solve_from_url(url).to_pil()

            assert image is not None

            # image.show()

    def test_skip_solve_images(self):
        solver = GigaPuzzleSkipSolver()
        for url in EPISODE_URLS:
            episode = GigaEpisodeParser(
                auth=AuthConfigMixin(
                    user_agent=SafariMobile.user_agent,
                ),
                url=url,
            ).parse()

            assert episode.readable_product.page_structure is not None

            for page in episode.readable_product.page_structure.pages:
                if page.type != "main" or page.src is None:
                    continue

                image = solver.solve_from_url(page.src).to_pil()

                assert image is not None

                # image.show()

                break


if __name__ == "__main__":
    unittest.main()
