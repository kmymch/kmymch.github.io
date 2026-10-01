# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Shrink images for the web and strip their metadata (EXIF, including GPS).

Files that are already small and metadata-free are left untouched, so running this
repeatedly does not keep re-compressing them.

Usage:
  uv run tools/optimize_images.py FILE...    # specific files (used by the pre-commit hook)
  uv run tools/optimize_images.py --all      # every image under assets/
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
MAX_SIDE = 1600           # longest side in px
JPEG_QUALITY = 82
JPEG_MAX_BYTES = 500_000  # re-encode JPEGs above this even if not resized
PNG_WARN_BYTES = 1_000_000
EXTS = {".jpg", ".jpeg", ".png"}


def optimize(path: Path) -> None:
    before = path.stat().st_size
    with Image.open(path) as im:
        im.load()
        fmt = im.format
        has_exif = bool(im.getexif())
        too_big = max(im.size) > MAX_SIDE
        heavy_jpeg = fmt == "JPEG" and before > JPEG_MAX_BYTES
        if not (has_exif or too_big or heavy_jpeg):
            return
        icc = im.info.get("icc_profile")
        out = ImageOps.exif_transpose(im)  # apply the rotation before dropping EXIF
        if too_big:
            out.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)

    if fmt == "JPEG":
        if out.mode not in ("RGB", "L"):
            out = out.convert("RGB")
        out.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True, icc_profile=icc)
    else:
        out.save(path, "PNG", optimize=True, icc_profile=icc)

    after = path.stat().st_size
    print(f"optimize_images: {path.relative_to(ROOT)}  {before // 1024} KB -> {after // 1024} KB")
    if fmt == "PNG" and after > PNG_WARN_BYTES:
        print(f"  warning: still {after // 1024} KB; if this is a photo, save it as .jpg instead")


def main(args):
    if args == ["--all"]:
        files = [p for p in (ROOT / "assets").rglob("*") if p.suffix.lower() in EXTS]
    else:
        files = [Path(a).resolve() for a in args]
    for f in files:
        if f.suffix.lower() in EXTS and f.exists():
            optimize(f)


if __name__ == "__main__":
    main(sys.argv[1:])
