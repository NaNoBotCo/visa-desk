#!/usr/bin/env python3
"""Brand — set the name and the domain, then redraw the artwork.

This is the file a cloner runs first. It rewrites site/assets/config.js, swaps
the domain everywhere it appears as literal text (titles, canonical links,
JSON-LD, llms.txt, sitemap, robots), and redraws the share card and the icon.

    python3 tools/brand.py                       numbered menu
    python3 tools/brand.py --show
    python3 tools/brand.py --name "Phuket Visa Desk" --domain phuketvisadesk.com
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CONFIG = SITE / "assets" / "config.js"

TEXT_SUFFIXES = {".html", ".txt", ".xml", ".js", ".json", ".jsonc", ".md"}


# ------------------------------------------------------------------- reading

def read_config():
    text = CONFIG.read_text()
    out = {}
    for key in ("name", "short", "domain", "origin", "inbox"):
        m = re.search(rf'\b{key}:\s*"([^"]*)"', text)
        out[key] = m.group(1) if m else ""
    return out


def split_name(name):
    """'Chiang Mai Visa Desk' -> ('Chiang Mai', 'Visa Desk') for the two-weight wordmark."""
    words = name.split()
    if len(words) <= 2:
        return "", name
    return " ".join(words[:-2]), " ".join(words[-2:])


# ------------------------------------------------------------------- writing

def set_config(name=None, domain=None, inbox=None):
    text = CONFIG.read_text()
    if name:
        light, strong = split_name(name)
        text = re.sub(r'(\bname:\s*")[^"]*(")', lambda m: m.group(1) + name + m.group(2), text, count=1)
        text = re.sub(r'(\bshort:\s*")[^"]*(")', lambda m: m.group(1) + strong + m.group(2), text, count=1)
    if domain:
        text = re.sub(r'(\bdomain:\s*")[^"]*(")', lambda m: m.group(1) + domain + m.group(2), text, count=1)
        text = re.sub(r'(\borigin:\s*")[^"]*(")', lambda m: m.group(1) + "https://" + domain + m.group(2), text, count=1)
    if inbox:
        text = re.sub(r'(\binbox:\s*")[^"]*(")', lambda m: m.group(1) + inbox + m.group(2), text, count=1)
    CONFIG.write_text(text)


def swap_everywhere(old, new, label):
    """Replace a literal string across every text file under site/ (and the worker)."""
    if not old or old == new:
        return 0
    hits = 0
    for base in (SITE, ROOT / "worker"):
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            s = p.read_text()
            if old in s:
                p.write_text(s.replace(old, new))
                hits += 1
    print(f"   {label}: {old} -> {new}  ({hits} file(s))")
    return hits


REGION_WORDS = ["northern Thailand", "Northern Thailand", "Thailand", "Thai",
                "Lanna", "Nimman", "Santitham", "Hang Dong", "Old City",
                "TM30", "90-day", "DTV"]


def region_words():
    """Words a cloner in another country has to change by hand."""
    found = []
    for w in REGION_WORDS:
        n = 0
        for p in SITE.rglob("*"):
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES:
                n += p.read_text().count(w)
        if n:
            found.append((w, n))
    return found


def set_cname(domain):
    (SITE / "CNAME").write_text(domain + "\n")


# ------------------------------------------------------------------- artwork

def wordmark_svg(name, x, y, size, light_fill="#454C59", strong_fill="#14161C"):
    light, strong = split_name(name)
    if light:
        return (f'<text x="{x}" y="{y}" font-family="Georgia,\'Times New Roman\',serif" '
                f'font-size="{size}" fill="{light_fill}">{esc(light)} '
                f'<tspan font-weight="700" fill="{strong_fill}">{esc(strong)}</tspan></text>')
    return (f'<text x="{x}" y="{y}" font-family="Georgia,\'Times New Roman\',serif" '
            f'font-size="{size}" font-weight="700" fill="{strong_fill}">{esc(strong)}</text>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def draw_share(cfg, out):
    headline = "Your visa, handled."
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F7F4EC"/><stop offset="1" stop-color="#EFE1C8"/>
    </linearGradient>
    <radialGradient id="g1" cx="0.18" cy="0.2" r="0.7">
      <stop offset="0" stop-color="#C79A3A" stop-opacity="0.26"/><stop offset="1" stop-color="#C79A3A" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="0.92" cy="0.08" r="0.6">
      <stop offset="0" stop-color="#3B7361" stop-opacity="0.20"/><stop offset="1" stop-color="#3B7361" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#g1)"/>
  <rect width="1200" height="630" fill="url(#g2)"/>
  <g transform="translate(88,84)">
    <rect x="0" y="0" width="64" height="64" rx="16" fill="#14161C"/>
    <rect x="10" y="10" width="44" height="44" rx="11" fill="none" stroke="#F1EEE5" stroke-width="3" stroke-dasharray="5.6 4.4"/>
    <path d="M21 33l7.4 7.4L43.5 26" fill="none" stroke="#C79A3A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    {wordmark_svg(cfg['name'], 86, 43, 30)}
  </g>
  <text x="88" y="316" font-family="Georgia,'Times New Roman',serif" font-size="98" font-weight="700" fill="#14161C" letter-spacing="-2">{esc(headline)}</text>
  <text x="88" y="392" font-family="Helvetica,Arial,sans-serif" font-size="35" fill="#454C59">Extensions · reporting · re-entry permits · border runs</text>
  <text x="88" y="446" font-family="Helvetica,Arial,sans-serif" font-size="35" fill="#454C59">Chiang Mai, northern Thailand</text>
  <rect x="88" y="506" width="336" height="66" rx="33" fill="#C79A3A"/>
  <text x="256" y="548" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="27" font-weight="700" fill="#ffffff">Get a quote</text>
  <text x="452" y="548" font-family="Helvetica,Arial,sans-serif" font-size="26" fill="#5F6775">{esc(cfg['domain'])}</text>
  <g opacity="0.16" transform="translate(880,300) rotate(-14)">
    <rect x="0" y="0" width="250" height="250" rx="34" fill="none" stroke="#14161C" stroke-width="9" stroke-dasharray="20 15"/>
    <path d="M66 132l44 44 82-94" fill="none" stroke="#14161C" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</svg>"""
    tmp = out.with_suffix(".tmp.svg")
    tmp.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "1200", "-h", "630", str(tmp), "-o", str(out)], check=True)
    tmp.unlink()
    print(f"   share card: {out}")


# --------------------------------------------------------------------- menus

def show(cfg):
    print()
    print("   name    ", cfg["name"])
    print("   domain  ", cfg["domain"])
    print("   inbox   ", cfg["inbox"])
    print()


def menu():
    while True:
        os.system("clear")
        cfg = read_config()
        print()
        print("━" * 58)
        print("   BRAND")
        print("━" * 58)
        show(cfg)
        print("   1.   Change the name")
        print()
        print("   2.   Change the domain")
        print()
        print("   3.   Change the inbox")
        print()
        print("   4.   Redraw the share card")
        print()
        print("   0.   Quit")
        print()
        print("─" * 58)
        c = input("\n   > ").strip()
        if c == "1":
            new = input("\n   New name\n\n   > ").strip()
            if new:
                swap_everywhere(cfg["name"], new, "name")
                set_config(name=new)
                draw_share(read_config(), SITE / "assets" / "share.png")
                input("\n   Press return.  ")
        elif c == "2":
            new = input("\n   New domain  (no https://)\n\n   > ").strip().lower().lstrip("htps:/")
            if new:
                swap_everywhere(cfg["domain"], new, "domain")
                set_config(domain=new)
                set_cname(new)
                draw_share(read_config(), SITE / "assets" / "share.png")
                input("\n   Press return.  ")
        elif c == "3":
            new = input("\n   New inbox\n\n   > ").strip()
            if new:
                swap_everywhere(cfg["inbox"], new, "inbox")
                set_config(inbox=new)
                input("\n   Press return.  ")
        elif c == "4":
            draw_share(read_config(), SITE / "assets" / "share.png")
            input("\n   Press return.  ")
        elif c in ("0", "q", ""):
            print()
            return


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name")
    ap.add_argument("--domain")
    ap.add_argument("--inbox")
    ap.add_argument("--city", nargs=2, metavar=("OLD", "NEW"),
                    help='swap a city name in the copy, e.g. --city "Chiang Mai" Phuket')
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--draw", action="store_true", help="redraw the share card only")
    a = ap.parse_args()

    if not any([a.name, a.domain, a.inbox, a.show, a.draw]):
        return menu()

    cfg = read_config()
    if a.show:
        return show(cfg)
    if a.name:
        swap_everywhere(cfg["name"], a.name, "name")
        set_config(name=a.name)
    if a.domain:
        d = a.domain.replace("https://", "").replace("http://", "").strip("/")
        swap_everywhere(cfg["domain"], d, "domain")
        set_config(domain=d)
        set_cname(d)
    if a.inbox:
        swap_everywhere(cfg["inbox"], a.inbox, "inbox")
        set_config(inbox=a.inbox)
    if a.city:
        swap_everywhere(a.city[0], a.city[1], "city")
        leftovers = region_words()
        if leftovers:
            print("\n   Still naming the old region by hand:")
            for w, n in leftovers:
                print(f"     {w}  ({n} place(s))")
    draw_share(read_config(), SITE / "assets" / "share.png")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
