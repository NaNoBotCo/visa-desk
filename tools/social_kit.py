#!/usr/bin/env python3
"""Social kit — the artwork for the desk's own profiles.

Renders every avatar, cover and first-post card at the size each platform
actually wants, from one set of SVG templates in the site's palette.

    python3 tools/social_kit.py            everything into brand/social/
    python3 tools/social_kit.py --list     what it would write, and why that size

Chrome is the renderer: macOS `magick` here has no rsvg delegate and drops
gradients, clip-paths and text. Nothing else is needed — no image library, no
font download beyond what macOS ships (Thonburi carries the Thai).
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "social"

INK = "#14161C"
PAPER = "#F1EEE5"
PAPER_DIM = "#A8A499"
GOLD = "#C79A3A"
INDIGO = "#24406E"

SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
SANS = "system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
THAI = "Thonburi,'Noto Sans Thai','Leelawadee UI',system-ui,sans-serif"

NAME_LIGHT = "Chiang Mai"
NAME_STRONG = "Visa Desk"
DOMAIN = "chiangmaivisadesk.com"
SERVICES_EN = "Work permits · Company registration · Retirement · 90-day · Border runs"
LEDE_TH = "เรื่องวีซ่า ให้เราจัดการ"
LEDE_EN = "Your visa, handled."
SERVICES_TH = "ใบอนุญาตทำงาน · จดทะเบียนบริษัท · ต่อวีซ่าเกษียณ · รายงานตัว 90 วัน · วิ่งชายแดน"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


# ----------------------------------------------------------------- fragments

def mark(cx, cy, size, dash=True):
    """The stamp: a dashed rounded square with a gold check through it."""
    s = size / 100.0
    x, y = cx - size / 2, cy - size / 2
    box = (f'<rect x="{x + 18 * s:.2f}" y="{y + 18 * s:.2f}" width="{64 * s:.2f}" '
           f'height="{64 * s:.2f}" rx="{16 * s:.2f}" fill="none" stroke="{PAPER}" '
           f'stroke-width="{3.2 * s:.2f}"'
           + (f' stroke-dasharray="{7 * s:.2f} {5.6 * s:.2f}"' if dash else "") + '/>')
    check = (f'<path d="M{x + 33.75 * s:.2f} {y + 52 * s:.2f} l{11.5 * s:.2f} {11.5 * s:.2f} '
             f'L{x + 67.5 * s:.2f} {y + 41.25 * s:.2f}" fill="none" stroke="{GOLD}" '
             f'stroke-width="{8 * s:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
    return box + check


def wordmark(x, y, size, anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{PAPER}">'
            f'<tspan fill="{PAPER_DIM}">{NAME_LIGHT} </tspan>'
            f'<tspan font-weight="700">{NAME_STRONG}</tspan></text>')


def rule(cx, y, w):
    return (f'<rect x="{cx - w / 2:.1f}" y="{y}" width="{w}" height="2" fill="{GOLD}" '
            f'opacity=".8"/>')


def line(x, y, text, size, font=SANS, fill=PAPER, anchor="middle", weight="400", ls="0"):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}" '
            f'fill="{fill}">{text}</text>')


def ghost(x, y, size):
    """A big faint stamp, for ground that is not empty and not busy."""
    return f'<g opacity=".07">{mark(x, y, size)}</g>'


def frame(w, h, body, ground=INK):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{ground}"/>'
            f'{body}</svg>')


# ------------------------------------------------------------------- designs

def avatar(size):
    s = size / 1024.0
    return frame(size, size, mark(size / 2, size / 2, 620 * s))


def fb_cover(w=1640, h=630):
    cx = w / 2
    return frame(w, h, "".join([
        ghost(w - 190, h / 2, 520),
        mark(cx, 168, 104),
        wordmark(cx, 320, 74),
        rule(cx, 356, 190),
        line(cx, 428, SERVICES_EN, 27, fill=PAPER_DIM),
        line(cx, 486, DOMAIN, 27, fill=GOLD, weight="600", ls="1.2"),
    ]))


def line_cover(w=1080, h=878):
    cx = w / 2
    return frame(w, h, "".join([
        ghost(cx, 300, 560),
        line(cx, 596, LEDE_TH, 62, font=THAI, weight="700"),
        line(cx, 650, LEDE_EN, 30, fill=PAPER_DIM),
        rule(cx, 690, 150),
        line(cx, 748, SERVICES_TH, 22, font=THAI, fill=PAPER_DIM),
        line(cx, 806, DOMAIN, 26, fill=GOLD, weight="600", ls="1.2"),
    ]))


def youtube_banner(w=2560, h=1440):
    cx, cy = w / 2, h / 2
    return frame(w, h, "".join([
        ghost(cx - 980, cy, 620), ghost(cx + 980, cy, 620),
        mark(cx, cy - 150, 112),
        wordmark(cx, cy + 10, 84),
        rule(cx, cy + 52, 200),
        line(cx, cy + 132, SERVICES_EN, 30, fill=PAPER_DIM),
        line(cx, cy + 196, DOMAIN, 28, fill=GOLD, weight="600", ls="1.4"),
    ]))


def post_square(n=1080):
    cx = n / 2
    return frame(n, n, "".join([
        ghost(cx, cx, 900),
        mark(cx, 250, 116),
        line(cx, 500, LEDE_TH, 84, font=THAI, weight="700"),
        line(cx, 562, LEDE_EN, 36, fill=PAPER_DIM),
        rule(cx, 610, 170),
        line(cx, 690, "ใบอนุญาตทำงาน · จดทะเบียนบริษัท", 30, font=THAI, fill=PAPER),
        line(cx, 740, "ต่อวีซ่าเกษียณ · รายงานตัว 90 วัน · วิ่งชายแดน", 30, font=THAI, fill=PAPER),
        line(cx, 880, DOMAIN, 32, fill=GOLD, weight="600", ls="1.4"),
    ]))


def post_vertical(w=1080, h=1920):
    cx = w / 2
    return frame(w, h, "".join([
        ghost(cx, 980, 980),
        mark(cx, 420, 130),
        line(cx, 760, LEDE_TH, 92, font=THAI, weight="700"),
        line(cx, 830, LEDE_EN, 38, fill=PAPER_DIM),
        rule(cx, 890, 180),
        line(cx, 980, "ใบอนุญาตทำงาน · จดทะเบียนบริษัท", 32, font=THAI),
        line(cx, 1036, "ต่อวีซ่าเกษียณ · รายงานตัว 90 วัน", 32, font=THAI),
        line(cx, 1092, "วิ่งชายแดน · แจ้งที่พัก ตม.30", 32, font=THAI),
        line(cx, 1300, DOMAIN, 34, fill=GOLD, weight="600", ls="1.4"),
    ]))


# The kit: filename, width, height, builder, what it is for.
SPECS = [
    ("avatar-1024.png", 1024, 1024, lambda: avatar(1024), "master square; keep a copy"),
    ("avatar-800-youtube.png", 800, 800, lambda: avatar(800), "YouTube channel picture"),
    ("avatar-640-line.png", 640, 640, lambda: avatar(640), "LINE OA profile image (max 3 MB)"),
    ("avatar-320-facebook-instagram.png", 320, 320, lambda: avatar(320), "Facebook Page + Instagram"),
    ("avatar-200-tiktok.png", 200, 200, lambda: avatar(200), "TikTok profile picture"),
    ("cover-facebook-1640x630.png", 1640, 630, fb_cover, "Facebook Page cover; text inside the mobile crop"),
    ("cover-line-1080x878.png", 1080, 878, line_cover, "LINE OA cover image"),
    ("banner-youtube-2560x1440.png", 2560, 1440, youtube_banner, "YouTube banner; text inside the 1546x423 safe box"),
    ("post-square-1080.png", 1080, 1080, post_square, "first post, Facebook + Instagram"),
    ("post-vertical-1080x1920.png", 1080, 1920, post_vertical, "TikTok cover / Stories / Reels"),
]


# ------------------------------------------------------------------ renderer

def find_browser():
    for path in CHROME_CANDIDATES:
        if Path(path).is_file():
            return path
    return shutil.which("chromium") or shutil.which("google-chrome")


def render(svg, out, width, height):
    browser = find_browser()
    if not browser:
        raise SystemExit("No Chrome/Chromium found; the PNGs are committed masters, so "
                         "existing files stay valid. Install Chrome to redraw them.")
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "art.html"
        page.write_text("<!doctype html><meta charset=utf-8><style>html,body{margin:0;"
                        f"padding:0;background:{INK}}}svg{{display:block}}</style>" + svg,
                        encoding="utf-8")
        # --headless=new: plain --headless hangs on current Chrome and never writes
        # the PNG. The new mode writes it in seconds but does not exit, hence the
        # poll-for-file loop.
        cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--no-sandbox", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", "--virtual-time-budget=3000",
               f"--window-size={width},{height}", f"--screenshot={out}",
               "--force-device-scale-factor=1", f"--user-data-dir={tmp}/profile",
               page.as_uri()]
        if out.exists():
            out.unlink()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for _ in range(600):
                if out.is_file() and out.stat().st_size > 0:
                    time.sleep(0.4)
                    break
                if proc.poll() is not None:
                    break
                time.sleep(0.1)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
        if not out.is_file() or out.stat().st_size == 0:
            err = (proc.stderr.read() or b"").decode(errors="replace")
            raise SystemExit(f"Chrome produced no image.\n{err[-1200:]}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="show the kit without rendering")
    args = ap.parse_args(argv)
    if args.list:
        for name, w, h, _, why in SPECS:
            print(f"{name:38} {w:>5}x{h:<5} {why}")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for name, w, h, build, why in SPECS:
        out = OUT / name
        render(build(), out, w, h)
        kb = out.stat().st_size / 1024
        print(f"{name:38} {w:>5}x{h:<5} {kb:7.0f} KB  {why}")
    print(f"\n{len(SPECS)} files in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
