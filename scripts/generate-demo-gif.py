#!/usr/bin/env python3
"""Generate profile GIFs (boot + cpointed CLI). GitHub blocks SMIL in SVG."""
# Made by Sn0w8ird

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

W, H = 520, 132
BG = (13, 17, 23)
FG = (88, 166, 255)
OK = (63, 185, 80)
DIM = (139, 148, 158)
MUTED = (139, 148, 158)

BOOT_LINES: list[tuple[str, tuple[int, int, int]]] = [
    ("[BOOT] Sn0w8irD operator console", MUTED),
    ("[OK]   OSCP credential loaded", OK),
    ("[OK]   ~/builds mounted (cpointed + tooling)", OK),
    ("[..]   pulse channel listening", FG),
    ("[OK]   ready_", OK),
]

CPOINTED_LINES = [
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


def _draw_terminal(
    lines: list[tuple[str, tuple[int, int, int]]],
    *,
    cursor: bool = False,
    height: int = H,
) -> Image.Image:
    img = Image.new("RGB", (W, height), BG)
    draw = ImageDraw.Draw(img)
    font = _font()
    y = 14
    for text, color in lines:
        draw.text((12, y), text, fill=color, font=font)
        y += 22
    if cursor:
        draw.text((12, min(y, height - 18)), "_", fill=OK, font=font)
    return img


def _draw_cpointed(lines: list[str], *, cursor: bool = False) -> Image.Image:
    img = Image.new("RGB", (W, 120), BG)
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
        draw.text((12, min(y, 102)), "_", fill=OK, font=font)
    return img


def _save_gif(path: Path, images: list[Image.Image], duration: int = 500) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )
    print(f"wrote {path} ({len(images)} frames)")


def gen_boot() -> None:
    images: list[Image.Image] = []
    for n in range(1, len(BOOT_LINES) + 1):
        chunk = BOOT_LINES[:n]
        images.append(_draw_terminal(chunk, cursor=False))
    images[-1] = _draw_terminal(BOOT_LINES, cursor=True)
    images.extend([images[-1]] * 12)
    _save_gif(ASSETS / "boot.gif", images, duration=450)


def gen_cpointed() -> None:
    images = [
        _draw_cpointed(CPOINTED_LINES[:n], cursor=(n == len(CPOINTED_LINES)))
        for n in range(1, len(CPOINTED_LINES) + 1)
    ]
    images.extend([images[-1]] * 10)
    _save_gif(ASSETS / "cpointed-demo.gif", images, duration=500)


def main() -> None:
    gen_boot()
    gen_cpointed()


if __name__ == "__main__":
    main()
