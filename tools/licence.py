#!/usr/bin/env python3
"""Licences — mint one for a white-label copy of this site.

    python3 tools/licence.py

A licensed copy is a copy of this repository with three things changed: its
name and domain (tools/brand.py), its recipient list (a Worker secret), and the
licence block this tool writes. The licence id then rides on every enquiry that
copy sends, which is what it is billed from — whether or not anyone remembers
to raise the invoice.

The register stays on this machine. It is real customers.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "licences-private"
BOOK = STORE / "licences.json"
CONFIG = ROOT / "site" / "assets" / "config.js"

TIERS = [
    ("flat", "Flat licence — they run their own backend"),
    ("carried", "Carried — we host the enquiries and the statements"),
    ("carried+us", "Carried, plus the US visa pages"),
]


def cfg(key):
    m = re.search(rf'\b{key}:\s*"([^"]*)"', CONFIG.read_text())
    return m.group(1) if m else ""


def load():
    return json.loads(BOOK.read_text()) if BOOK.exists() else {"licences": []}


def save(b):
    STORE.mkdir(exist_ok=True)
    BOOK.write_text(json.dumps(b, indent=2, ensure_ascii=False))


def make_id(place, taken):
    base = re.sub(r"[^A-Za-z0-9]+", "", place).upper()[:8] or "SITE"
    n = 1
    while f"WL-{base}-{n:02d}" in taken:
        n += 1
    return f"WL-{base}-{n:02d}"


def block(lic):
    """The config the licensed copy pastes in."""
    return (
        "  licence: {\n"
        f'    id: "{lic["id"]}",\n'
        f'    holder: "{lic["holder"]}",\n'
        f'    place: "{lic["place"]}"\n'
        "  },"
    )


def new(book):
    print()
    holder = input("   Whose copy is it?  (the business name)\n\n   > ").strip()
    if not holder:
        return
    place = input("\n   Which province or city?\n\n   > ").strip()
    domain = input("\n   Their domain, if they have one yet.\n\n   > ").strip().lower()

    print()
    for i, (_, label) in enumerate(TIERS, 1):
        print(f"   {i}.  {label}")
    c = input("\n   > ").strip()
    tier = TIERS[int(c) - 1][0] if c.isdigit() and 1 <= int(c) <= len(TIERS) else TIERS[0][0]

    taken = {x["id"] for x in book["licences"]}
    lic = {
        "id": make_id(place or holder, taken),
        "holder": holder,
        "place": place,
        "domain": domain,
        "tier": tier,
        "issued": date.today().isoformat(),
        "rate": "",
        "notes": "",
    }
    book["licences"].append(lic)
    save(book)

    folder = STORE / lic["id"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "config-block.txt").write_text(block(lic) + "\n")
    (folder / "setup.txt").write_text(setup_notes(lic))

    print()
    print("═" * 62)
    print(f"   {lic['id']}")
    print("═" * 62)
    print()
    print(block(lic))
    print()
    print(f"   Written to: {folder}")
    subprocess.run(["open", str(folder)])
    input("\n   Press return.  ")


def setup_notes(lic):
    return f"""SETTING UP {lic['id']} — {lic['holder']}
{lic['place'] or '(no place given)'} · {lic['domain'] or '(no domain yet)'} · {lic['tier']}
Issued {lic['issued']}

1.  Clone the repository into its own folder.

2.  Brand it:

        python3 tools/brand.py --name "{lic['holder']}" --domain {lic['domain'] or 'their-domain.com'}
        python3 tools/brand.py --city "Chiang Mai" "{lic['place'] or 'THEIR CITY'}"

    The second command lists the region words still to change by hand.

3.  Paste this into site/assets/config.js, replacing the empty licence block:

{block(lic)}

4.  Set their LINE Official Account id in the same file, or clear it. An
    empty id removes every LINE button rather than leaving one that fails.

5.  Their backend:

    flat        they deploy worker/ themselves and set their own secrets.
    carried     deploy a Worker for them; set DESK_RECIPIENTS to their
                addresses and ORIGIN_CODE to {lic['id']}.

6.  Check before it goes out:

        make check

7.  Their enquiries then carry licence={lic['id']}, and Statement.command
    totals them on their own line.
"""


def listing(book):
    print()
    if not book["licences"]:
        print("   None yet.")
        input("\n   Press return.  ")
        return
    print("─" * 62)
    print(f"   {'ID':<16} {'ISSUED':<12} {'TIER':<11} WHO")
    print("─" * 62)
    for x in book["licences"]:
        print(f"   {x['id']:<16} {x['issued']:<12} {x['tier']:<11} {x['holder']}")
    print("─" * 62)
    print(f"\n   {len(book['licences'])} licence(s).  {BOOK}")
    input("\n   Press return.  ")


def main():
    while True:
        os.system("clear")
        book = load()
        print()
        print("━" * 62)
        print("   LICENCES")
        print("━" * 62)
        print()
        print(f"   This copy:  {cfg('name')}  ({cfg('originCode') or 'DESK'})")
        print(f"   Credit:     {cfg('name') and cfg('url') or 'hongdam.net'}")
        print()
        print("   1.   Mint a licence for a new copy")
        print()
        print("   2.   List licences")
        print()
        print("   0.   Quit")
        print()
        print("─" * 62)
        c = input("\n   > ").strip()
        if c == "1":
            new(book)
        elif c == "2":
            listing(book)
        else:
            print()
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
