import unittest

from PIL import Image

from mangas.pipelines import GigaEpisodePipeline

EPISODE_URLS = [
    "https://shonenjumpplus.com/episode/14079602755396027365",
    "https://shonenjumpplus.com/episode/14079602755345580881",
    "https://shonenjumpplus.com/episode/14079602755360463401",
]


class GigaEpisodePipelineTest(unittest.TestCase):
    def test_iterate_solved_images(self):
        for url in EPISODE_URLS:
            pipeline = GigaEpisodePipeline.from_url(url=url)
            output = pipeline()

            page_count = 0

            for image in output.images():
                if page_count == 3:
                    break

                assert image is not None
                assert isinstance(image, Image.Image)

                # image.show()

                page_count += 1

            assert page_count > 0


if __name__ == "__main__":
    unittest.main()
