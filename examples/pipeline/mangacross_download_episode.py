import os
from PIL import Image
from mangas import MangaCrossEpisodePipeline

pipe = MangaCrossEpisodePipeline.from_url("https://mangacross.jp/comics/kujira/1")

output = pipe()

outdir = os.path.join("output", "mangacross")
os.makedirs(outdir, exist_ok=True)


for idx, img in enumerate(output.images()):
    assert isinstance(img, Image.Image)
    img.save(os.path.join(outdir, f"{idx}.png"))
