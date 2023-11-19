import unittest

import requests
from PIL import Image
import numpy as np

from mangas.auth import DefaultAuthConfig
from mangas.utils import ImageWrapper

IMAGE_URLS = [
    "https://unsplash.com/photos/pCjw_ygKCv0/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTB8fGxlbW9ufGVufDB8fHx8MTcwMDM3OTEwN3ww&force=false&w=640",
    "https://cdn-ak-img.shonenjumpplus.com/public/page/2/14079602755456178166-580ed8f8b8a042a028524f8052aecd16",
]

auth = DefaultAuthConfig


class UtilsDataTest(unittest.TestCase):
    def test_image_wrapper_from_url(self):
        for url in IMAGE_URLS:
            res = requests.get(url, headers=auth.compose_headers(), stream=True)
            image = ImageWrapper.from_stream(res.iter_content())

            pil_image = image.to_pil()
            np_image = image.to_numpy()

            assert isinstance(pil_image, Image.Image)
            assert isinstance(np_image, np.ndarray)

            # pil_image.show()


if __name__ == "__main__":
    unittest.main()
