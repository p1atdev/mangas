from pathlib import Path
from PIL import Image
from mangas import GigaEpisodePipeline

pipe = GigaEpisodePipeline.from_url(
    "https://shonenjumpplus.com/episode/14079602755396027365"
)

output = pipe()

outdir = Path("output")
outdir.mkdir(exist_ok=True)

for idx, img in enumerate(output.images()):
    assert isinstance(img, Image.Image)
    img.save(outdir / f"{idx}.png")
