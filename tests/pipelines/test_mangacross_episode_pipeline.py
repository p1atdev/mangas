import unittest

from PIL import Image

from mangas.pipelines import MangaCrossEpisodePipeline

EPISODE_URLS = [
    "https://mangacross.jp/comics/fairway/1",
    "https://mangacross.jp/comics/watamaho/1",
    "https://mangacross.jp/comics/cosmicstar/2",
]


class MangaCrossEpisodePipelineTest(unittest.TestCase):
    def test_iterate_solved_images(self):
        for url in EPISODE_URLS:
            pipeline = MangaCrossEpisodePipeline.from_url(url)
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
