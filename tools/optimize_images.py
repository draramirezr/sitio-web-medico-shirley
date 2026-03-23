from __future__ import annotations

import io
import os
import sys
import urllib.request
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_IMAGES = PROJECT_ROOT / "static" / "images"


EXTERNAL_IMAGES: dict[str, str] = {
    # Home/Servicios cards (previously hosted externally)
    "servicios-tratamientos-esteticos.png": "https://mgx-backend-cdn.metadl.com/generate/images/1040625/2026-03-18/3472b72c-6479-4947-b622-60178c365205.png",
}


def _download(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; draramirez-site-optimizer/1.0)",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def _save_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _optimize_to_webp(src_path: Path, dst_path: Path, max_width: int = 900, quality: int = 82) -> None:
    with Image.open(src_path) as im:
        im.load()
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        elif im.mode == "RGBA":
            # Keep alpha when present
            pass

        w, h = im.size
        if w > max_width:
            new_h = max(1, round(h * (max_width / w)))
            im = im.resize((max_width, new_h), Image.LANCZOS)

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst_path, format="WEBP", quality=quality, method=6)


def main() -> int:
    STATIC_IMAGES.mkdir(parents=True, exist_ok=True)

    # 1) Download externals to /static/images (PNG originals kept as fallback)
    for filename, url in EXTERNAL_IMAGES.items():
        out_path = STATIC_IMAGES / filename
        if out_path.exists():
            continue
        data = _download(url)
        _save_bytes(out_path, data)

    # 2) Convert key PNG/JPG images to WEBP (smaller transfer)
    candidates = [
        STATIC_IMAGES / "servicios-ginecologia-general.png",
        STATIC_IMAGES / "servicios-obstetricia-embarazo.png",
        STATIC_IMAGES / "servicios-tratamientos-esteticos.png",
    ]

    for src in candidates:
        if not src.exists():
            print(f"[skip] missing: {src.relative_to(PROJECT_ROOT)}")
            continue
        dst = src.with_suffix(".webp")
        _optimize_to_webp(src, dst)
        print(
            f"[ok] {src.name} -> {dst.name} "
            f"({src.stat().st_size/1024:.1f} KiB -> {dst.stat().st_size/1024:.1f} KiB)"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

