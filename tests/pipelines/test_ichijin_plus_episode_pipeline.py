import unittest

from PIL import Image

from mangas.pipelines import IchijinPlusEpisodePipeline

EPISODE_URLS = [
    "https://ichijin-plus.com/episodes/49869036978995",
    "https://ichijin-plus.com/episodes/3160680153227",
    "https://ichijin-plus.com/episodes/84387818308868",
]


class IchijinPlusEpisodePipelineTest(unittest.TestCase):
    def test_iterate_solved_images(self):
        for url in EPISODE_URLS:
            pipeline = IchijinPlusEpisodePipeline.from_url(url=url)
            output = pipeline()

            print(output.parse_output.comic_title, output.parse_output.episode_title)

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
