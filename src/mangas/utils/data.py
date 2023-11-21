from PIL import Image
import numpy as np
from io import BytesIO

import chompjs
from typing import Iterator, Any
import humps
from pydantic import BaseModel, ConfigDict


# JSON のキーをすべてキャメルケースにキャストするモデル
class ForceCamelCaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(alias_generator=humps.camelize)


# 画像のラッパーモデル
class ImageWrapper(BaseModel):
    bytes: bytes

    @classmethod
    def from_file(cls, image_path: str):
        with open(image_path, "rb") as f:
            return cls(bytes=f.read())

    @classmethod
    def from_pil(cls, image: Image.Image):
        with BytesIO() as f:
            image.save(f, format="png")
            return cls(bytes=f.getvalue())

    @classmethod
    def from_numpy(cls, image: np.ndarray):
        return cls.from_pil(Image.fromarray(image))

    @classmethod
    def from_stream(cls, stream: Iterator[bytearray]):
        return cls(bytes=b"".join(stream))

    @classmethod
    def from_bytesio(cls, bytesio: BytesIO):
        return cls(bytes=bytesio.getvalue())

    def to_pil(self):
        return Image.open(BytesIO(self.bytes))

    def to_numpy(self):
        return np.array(self.to_pil())


def load_js_object(js_object: str) -> Any:
    return chompjs.parse_js_object(js_object)
