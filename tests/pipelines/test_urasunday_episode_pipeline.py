import unittest

from PIL import Image

from mangas.pipelines import UraSundayEpisodePipeline

EPISODE_URLS = [
    "https://urasunday.com/title/1301/123482",
    "https://urasunday.com/title/1301/",
    "https://urasunday.com/title/1301",
    "https://urasunday.com/title/2060/188243",
]


class UraSundayEpisodePipelineTest(unittest.TestCase):
    def test_iterate_solved_images(self):
        for url in EPISODE_URLS:
            pipeline = UraSundayEpisodePipeline.from_url(url)
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
