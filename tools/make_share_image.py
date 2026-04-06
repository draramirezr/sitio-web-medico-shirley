from __future__ import annotations

from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_IMAGES = PROJECT_ROOT / "static" / "images"

SRC = STATIC_IMAGES / "share-doctora-source.png"
OUT = STATIC_IMAGES / "dra-shirley-share.jpg"


def _center_crop_to_ratio(im: Image.Image, target_w: int, target_h: int) -> Image.Image:
    target_ratio = target_w / target_h
    w, h = im.size
    src_ratio = w / h

    if abs(src_ratio - target_ratio) < 1e-6:
        return im

    if src_ratio > target_ratio:
        # too wide -> crop sides
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    else:
        # too tall -> crop top/bottom (slightly higher crop to keep face)
        new_h = int(w / target_ratio)
        top = int((h - new_h) * 0.35)
        top = max(0, min(top, h - new_h))
        return im.crop((0, top, w, top + new_h))


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"Missing source image: {SRC}")

    STATIC_IMAGES.mkdir(parents=True, exist_ok=True)

    with Image.open(SRC) as im:
        im.load()
        if im.mode != "RGB":
            im = im.convert("RGB")

        im = _center_crop_to_ratio(im, 1200, 630)
        im = im.resize((1200, 630), Image.LANCZOS)
        im.save(OUT, format="JPEG", quality=86, optimize=True, progressive=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

