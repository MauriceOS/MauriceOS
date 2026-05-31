#!/usr/bin/env python3
"""Generate assets/cpointed-demo.gif — terminal-style CLI preview for profile README."""
# Made by Sn0w8ird

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cpointed-demo.gif"

W, H = 120, 120
W, H = 520, 120
BG = (13, 17, 23)
FG = (88, 166, 255)
OK = (63, 185, 80)
DIM = (139, 148, 158)

LINES = [
    "operator@sn0w8ird:~$ cpointed scan --host lab --fingerprint",
    "[*] loading module surface ...",
    "[*] fingerprint: panel surface detected",
    "[OK] report ready — authorized use only",
]


def _font(size: int = 12):
    for name in ("cour.ttf", "Consolas.ttf", "DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _frame(lines: list[str], cursor: bool = False) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = _font()
    y = 14
    for i, line in enumerate(lines):
        if i == 0:
            color = FG
        elif line.startswith("[OK]"):
            color = OK
        else:
            color = DIM
        draw.text((12, y), line, fill=color, font=font)
        y += 22
    if cursor:
        draw.text((12, min(y, H - 18)), "_", fill=OK, font=font)
    return img


def main() -> None:
    images = [_frame(LINES[:n], cursor=(n == len(LINES))) for n in range(1, len(LINES) + 1)]
    images.extend([images[-1]] * 10)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        OUT,
        save_all=True,
        append_images=images[1:],
        duration=500,
        loop=0,
        optimize=True,
    )
    print(f"wrote {OUT} ({len(images)} frames)")


if __name__ == "__main__":
    main()
