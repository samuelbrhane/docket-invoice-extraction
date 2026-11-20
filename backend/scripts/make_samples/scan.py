"""Turn a generated PDF into a JPG that looks like a phone photo of a paper invoice."""

from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

PAPER = (236, 230, 216)


def pdf_to_scan(pdf_path: Path, jpg_path: Path) -> None:
    page = pdfium.PdfDocument(str(pdf_path))[0]
    image = page.render(scale=150 / 72).to_pil().convert("RGB")

    # Warm, slightly faded paper
    gray = ImageOps.grayscale(image)
    image = ImageOps.colorize(gray, black=(40, 38, 36), white=PAPER)

    # Uneven lighting, darker towards the bottom
    shade = ImageOps.invert(Image.linear_gradient("L")).resize(image.size)
    image = Image.composite(image, ImageEnhance.Brightness(image).enhance(0.84), shade)

    # Grain, softness and a crooked angle
    noise = Image.effect_noise(image.size, 22).convert("RGB")
    image = Image.blend(image, noise, 0.07)
    image = image.filter(ImageFilter.GaussianBlur(0.7))
    image = image.rotate(1.6, resample=Image.BICUBIC, expand=True, fillcolor=(120, 112, 100))

    image.save(jpg_path, "JPEG", quality=66)