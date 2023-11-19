import os
from PIL import Image
from mangas import GigaEpisodePipeline

pipe = GigaEpisodePipeline.from_url(
    "https://shonenjumpplus.com/episode/14079602755396027365"
)

output = pipe()


outdir = os.path.join("output", "giga")
os.makedirs(outdir, exist_ok=True)

for idx, img in enumerate(output.images()):
    assert isinstance(img, Image.Image)
    img.save(os.path.join(outdir, f"{idx}.png"))
