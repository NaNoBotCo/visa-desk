#!/usr/bin/env python3
"""Partner codes — mint a code, get a link, a QR and a sticker.

Numbered menu. Nothing here goes online; the partner list stays on this Mac.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "partners-private"
BOOK = STORE / "partners.json"
CONFIG = ROOT / "site" / "assets" / "config.js"

WORDS_OUT = 12          # longest code we mint
RESERVED = {"HOUSE", "TEST", "ADMIN", "NULL", "NONE"}


# ----------------------------------------------------------------- the book

def site_origin():
    """Read the live domain out of the site config so there is one source."""
    try:
        text = CONFIG.read_text()
        m = re.search(r'origin:\s*"([^"]+)"', text)
        if m:
            return m.group(1).rstrip("/")
    except OSError:
        pass
    return "https://chiangmaivisadesk.com"


def load():
    if BOOK.exists():
        return json.loads(BOOK.read_text())
    return {"partners": []}


def save(book):
    STORE.mkdir(exist_ok=True)
    BOOK.write_text(json.dumps(book, indent=2, ensure_ascii=False))


GENERIC = {"THE", "GUEST", "HOUSE", "HOTEL", "HOSTEL", "RESORT", "CAFE", "COFFEE",
           "COWORKING", "SPACE", "SCHOOL", "CENTRE", "CENTER", "CO", "LTD", "AND",
           "OF", "AT", "IN", "BAAN", "BAN"}


def make_code(name, taken):
    """A short, sayable code from the partner's name."""
    words = [w for w in re.findall(r"[A-Za-z0-9]+", name.upper())]
    keep = [w for w in words if w not in GENERIC] or words
    base = ""
    for w in keep:
        if base and len(base) + len(w) > WORDS_OUT:
            break
        base += w
    base = base[:WORDS_OUT]
    if not base:
        base = "PARTNER"
    code = base
    n = 2
    while code in taken or code in RESERVED:
        tail = str(n)
        code = base[: WORDS_OUT - len(tail)] + tail
        n += 1
    return code


# --------------------------------------------------------------- the artwork

def qr_data_uri(url):
    import segno
    import io
    import base64
    buf = io.BytesIO()
    segno.make(url, error="h").save(buf, kind="png", scale=12, border=2, dark="#17130f")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def sticker(code, name, url, out_png):
    """A card a guesthouse can print and put on the desk."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1400" viewBox="0 0 1000 1400">
  <rect width="1000" height="1400" fill="#fbf8f2"/>
  <rect x="34" y="34" width="932" height="1332" rx="44" fill="none"
        stroke="#e4dacb" stroke-width="4"/>
  <g transform="translate(90,110)">
    <rect x="0" y="0" width="70" height="70" rx="18" fill="#17130f"/>
    <rect x="11" y="11" width="48" height="48" rx="12" fill="none" stroke="#f3ece1"
          stroke-width="3.4" stroke-dasharray="6 4.6"/>
    <path d="M23 36l8 8 16.5-19" fill="none" stroke="#c9761a" stroke-width="5.4"
          stroke-linecap="round" stroke-linejoin="round"/>
    <text x="94" y="47" font-family="Georgia,serif" font-size="33" fill="#4a3f35">Chiang Mai <tspan font-weight="700" fill="#191410">Visa Desk</tspan></text>
  </g>
  <text x="90" y="290" font-family="Georgia,serif" font-size="60" font-weight="700" fill="#191410">Visas and border runs</text>
  <text x="90" y="356" font-family="Helvetica,Arial,sans-serif" font-size="32" fill="#4a3f35">Point your camera. Ask for a price.</text>
  <image href="{qr_data_uri(url)}" x="235" y="430" width="530" height="530"/>
  <rect x="90" y="1030" width="820" height="96" rx="48" fill="#f6e3cb"/>
  <text x="500" y="1090" text-anchor="middle" font-family="ui-monospace,Menlo,monospace"
        font-size="40" font-weight="700" fill="#6b4a2f" letter-spacing="3">{code}</text>
  <text x="500" y="1200" text-anchor="middle" font-family="Helvetica,Arial,sans-serif"
        font-size="29" fill="#7b6d5f">{esc(name)}</text>
  <text x="500" y="1290" text-anchor="middle" font-family="Helvetica,Arial,sans-serif"
        font-size="26" fill="#7b6d5f">{esc(url)}</text>
</svg>"""
    tmp = out_png.with_suffix(".svg")
    tmp.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "1000", "-h", "1400", str(tmp), "-o", str(out_png)],
                   check=True)
    tmp.unlink()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def artwork(code, name, url):
    import segno
    folder = STORE / code
    folder.mkdir(parents=True, exist_ok=True)
    segno.make(url, error="h").save(str(folder / f"{code}-qr.png"), scale=18, border=4)
    sticker(code, name, url, folder / f"{code}-card.png")
    (folder / f"{code}-link.txt").write_text(url + "\n")
    return folder


# ------------------------------------------------------------------ the menu

def line(ch="─", n=58):
    print(ch * n)


def pause():
    input("\n   Press return.  ")


def new_partner(book):
    print()
    name = input("   Who are they?  (Baan Kaew Guest House)\n\n   > ").strip()
    if not name:
        return
    taken = {p["code"] for p in book["partners"]}
    code = make_code(name, taken)

    print(f"\n   Code:  {code}")
    other = input("\n   Return to keep it, or type a different one.\n\n   > ").strip().upper()
    if other:
        other = re.sub(r"[^A-Z0-9._-]", "", other)[:40]
        if other and other not in taken:
            code = other

    url = f"{site_origin()}/?ref={code}"
    folder = artwork(code, name, url)
    book["partners"].append({
        "code": code, "name": name, "url": url,
        "added": date.today().isoformat(), "rate": "", "notes": ""
    })
    save(book)

    print()
    line()
    print(f"   {code}")
    print(f"   {url}")
    line()
    print(f"\n   Sticker and QR:  {folder}")
    print("\n   Paste this to them:\n")
    print(f"   Send anyone who asks about visas here: {url}")
    print(f"   Bookings that come through it are counted to you.")
    subprocess.run(["open", str(folder)])
    pause()


def list_partners(book):
    print()
    if not book["partners"]:
        print("   Nobody yet.")
        pause()
        return
    line()
    print(f"   {'CODE':<14} {'ADDED':<12} WHO")
    line()
    for p in book["partners"]:
        print(f"   {p['code']:<14} {p['added']:<12} {p['name']}")
    line()
    print(f"\n   {len(book['partners'])} partner(s).  {BOOK}")
    pause()


def reprint(book):
    if not book["partners"]:
        print("\n   Nobody yet.")
        pause()
        return
    print()
    for i, p in enumerate(book["partners"], 1):
        print(f"   {i}.  {p['code']:<14} {p['name']}")
    print("\n   0.  Back")
    choice = input("\n   > ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(book["partners"]):
        return
    p = book["partners"][int(choice) - 1]
    folder = artwork(p["code"], p["name"], p["url"])
    print(f"\n   Rebuilt:  {folder}")
    subprocess.run(["open", str(folder)])
    pause()


def test_link(book):
    code = input("\n   Which code?  (return for HOUSE)\n\n   > ").strip().upper() or "HOUSE"
    url = f"{site_origin()}/?ref={code}"
    print(f"\n   {url}")
    subprocess.run(["open", url])
    pause()


def main():
    book = load()
    while True:
        os.system("clear")
        print()
        line("━")
        print("   PARTNER CODES")
        line("━")
        print()
        print("   1.   New partner  →  code, link, QR, sticker")
        print()
        print("   2.   List partners")
        print()
        print("   3.   Print a sticker again")
        print()
        print("   4.   Open a referral link to test it")
        print()
        print("   0.   Quit")
        print()
        line()
        choice = input("\n   > ").strip()
        if choice == "1":
            new_partner(book)
        elif choice == "2":
            list_partners(book)
        elif choice == "3":
            reprint(book)
        elif choice == "4":
            test_link(book)
        elif choice in ("0", "q", ""):
            print()
            return
        book = load()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
