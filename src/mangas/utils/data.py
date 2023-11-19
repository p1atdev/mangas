from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import requests

from typing import Iterator
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
    def from_cv2(cls, image: np.ndarray):
        return cls.from_numpy(image)

    @classmethod
    def from_stream(cls, stream: Iterator[bytearray]):
        return cls(bytes=b"".join(stream))

    def to_pil(self):
        return Image.open(BytesIO(self.bytes))

    def to_numpy(self):
        return np.array(self.to_pil())

    def to_cv2(self):
        return self.to_numpy()
