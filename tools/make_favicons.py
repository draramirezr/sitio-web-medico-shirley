from __future__ import annotations

from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_LOGOS = PROJECT_ROOT / "static" / "logos"

# Use a high-contrast icon as source for favicons (best at 16–48px)
# Chosen: ICONO-11.jpg (white icon over brand pink background)
SRC = STATIC_LOGOS / "ICONO-11.jpg"


def _save_png(im: Image.Image, out: Path, size: int) -> None:
    img = im.resize((size, size), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"Missing source logo: {SRC}")

    STATIC_LOGOS.mkdir(parents=True, exist_ok=True)

    with Image.open(SRC) as im:
        im.load()
        if im.mode not in ("RGBA", "RGB"):
            im = im.convert("RGBA")
        elif im.mode == "RGB":
            im = im.convert("RGBA")

        # Generate modern PNG icons
        _save_png(im, STATIC_LOGOS / "favicon-32.png", 32)
        _save_png(im, STATIC_LOGOS / "favicon-48.png", 48)
        _save_png(im, STATIC_LOGOS / "apple-touch-icon.png", 180)
        _save_png(im, STATIC_LOGOS / "logo.png", 256)

        # Generate ICO (multi-size) for broad compatibility / Google
        ico = im.resize((256, 256), Image.LANCZOS)
        ico.save(
            STATIC_LOGOS / "favicon.ico",
            format="ICO",
            sizes=[(16, 16), (32, 32), (48, 48)],
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

