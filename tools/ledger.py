#!/usr/bin/env python3
"""Commission statement — what came through the site, and who it is owed to.

    python3 tools/ledger.py

Every enquiry the Worker records carries two codes:

    line     which book of business it belongs to. "th" is the shared
             Thailand-side desk; "us" is the US-outbound book; "wl" is a
             licensing enquiry. Each has its own recipients and its own code.
    licence  which copy of the site sent it. Empty for this one; set for a
             white-label deployment, and what that licence is billed from.
    origin   stamped server-side on every enquiry that came through this site.
             It does not depend on a URL parameter surviving, so it is the
             line the desk's own commission is calculated from.
    ref      an optional partner code. A partner's share comes out of the
             desk's, not instead of it.

The numbers here are what the Worker wrote to D1. Enquiries that arrived by the
email fallback are in the inbox, not in this table; the statement says so rather
than counting them as zero.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "statements"
WRANGLER_DIR = ROOT / "worker"
CONFIG = ROOT / "site" / "assets" / "config.js"


def cfg(key):
    m = re.search(rf'\b{key}:\s*"([^"]*)"', CONFIG.read_text())
    return m.group(1) if m else ""


DB = "visa-desk"


def query(sql):
    """Ask D1 for rows. Returns None when wrangler cannot answer."""
    try:
        r = subprocess.run(
            ["npx", "wrangler", "d1", "execute", DB, "--remote", "--json", "--command", sql],
            cwd=WRANGLER_DIR, capture_output=True, text=True, timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    try:
        payload = json.loads(r.stdout[r.stdout.index("["):])
        return payload[0]["results"]
    except (ValueError, KeyError, IndexError):
        return None


def load_file(path):
    try:
        d = json.loads(Path(path).expanduser().read_text())
    except (OSError, ValueError) as e:
        print(f"\n   Could not read it: {e}")
        return None
    if isinstance(d, dict):
        d = d.get("results") or d.get("rows") or []
    return d


def period():
    print("\n   1.  This month")
    print("   2.  Last month")
    print("   3.  Everything")
    c = input("\n   > ").strip()
    today = date.today()
    if c == "2":
        end = today.replace(day=1)
        start = (end - timedelta(days=1)).replace(day=1)
        return start.isoformat(), end.isoformat(), start.strftime("%B %Y")
    if c == "3":
        return "0000-01-01", "9999-12-31", "everything"
    start = today.replace(day=1)
    return start.isoformat(), "9999-12-31", start.strftime("%B %Y")


def statement(rows, start, end, label):
    rows = [r for r in rows if start <= (r.get("received_at") or "")[:10] < end]
    origin_code = cfg("originCode") or "DESK"
    origin_us = cfg("originCodeUs") or "USOUT"

    th = [r for r in rows if (r.get("line") or "th") == "th"]
    us = [r for r in rows if (r.get("line") or "th") == "us"]
    wl = [r for r in rows if (r.get("line") or "th") == "wl"]

    by_origin, by_ref = {}, {}
    for r in rows:
        by_origin[r.get("origin") or "—"] = by_origin.get(r.get("origin") or "—", 0) + 1
        k = r.get("ref") or ""
        if k:
            by_ref[k] = by_ref.get(k, 0) + 1

    L = []
    w = L.append
    w(f"COMMISSION STATEMENT — {label}")
    w(f"{cfg('name')} · {cfg('domain')}")
    w(f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    w("")
    w("=" * 62)
    w(f"  ENQUIRIES THROUGH THIS SITE                       {len(rows):>6}")
    w("=" * 62)
    w("")
    w("  EACH BOOK, COUNTED APART")
    w("  " + "-" * 58)
    w(f"    Thailand side, shared desk    {origin_code:<12} {len(th):>6}")
    w(f"    US visas, own book            {origin_us:<12} {len(us):>6}")
    w(f"    White-label enquiries         {'WLABEL':<12} {len(wl):>6}")
    w("")
    w("  Every one of these carries the origin stamp, set by the Worker")
    w("  rather than by the visitor's URL. They are the desk's line.")
    w("")
    w("  BY ORIGIN")
    w("  " + "-" * 58)
    labels = {origin_code: "  shared desk", origin_us: "  own book", "WLABEL": "  licensing"}
    for k in sorted(by_origin, key=lambda k: -by_origin[k]):
        w(f"    {k:<20} {by_origin[k]:>6}{labels.get(k, '')}")
    w("")
    if by_ref:
        w("  PARTNER CODES ALONGSIDE  (their share comes out of ours)")
        w("  " + "-" * 58)
        for k in sorted(by_ref, key=lambda k: -by_ref[k]):
            w(f"    {k:<20} {by_ref[k]:>6}")
        unattributed = len(rows) - sum(by_ref.values())
        w("")
        w(f"    {'no partner code':<20} {unattributed:>6}")
    else:
        w("  No partner codes in this period.")
    w("")
    by_lic = {}
    for r in rows:
        k = r.get("licence") or ""
        if k:
            by_lic[k] = by_lic.get(k, 0) + 1
    if by_lic:
        w("  LICENSED COPIES  (each one billable on its own licence)")
        w("  " + "-" * 58)
        for k in sorted(by_lic, key=lambda k: -by_lic[k]):
            w(f"    {k:<20} {by_lic[k]:>6}")
        w("")
        w(f"    {'this site':<20} {len(rows) - sum(by_lic.values()):>6}")
        w("")

    w("  THAILAND SIDE, BY SERVICE")
    w("  " + "-" * 58)
    need = {}
    for r in th:
        need[r.get("need") or "—"] = need.get(r.get("need") or "—", 0) + 1
    for k in sorted(need, key=lambda k: -need[k]) or ["—"]:
        w(f"    {k:<28} {need.get(k, 0):>6}")
    w("")
    w("  US VISAS, BY CATEGORY")
    w("  " + "-" * 58)
    cat = {}
    for r in us:
        cat[r.get("visa") or "not sure"] = cat.get(r.get("visa") or "not sure", 0) + 1
    if cat:
        for k in sorted(cat, key=lambda k: -cat[k]):
            w(f"    {k:<28} {cat[k]:>6}")
    else:
        w("    none in this period")
    w("")
    w("=" * 62)
    w("  What this counts: enquiries the Worker wrote to its table.")
    w("  Enquiries that arrived by the email fallback are in the inbox")
    w("  and are not in these numbers.")
    w("  What it does not count: bookings, or money. Those are settled")
    w("  against the agreed rate, from this list of enquiries.")
    w("=" * 62)
    return "\n".join(L)


def rows_from_somewhere():
    print("\n   Reading the table…")
    rows = query("SELECT id, received_at, line, origin, ref, licence, need, visa, area, page FROM enquiries")
    if rows is not None:
        print(f"   {len(rows)} row(s) from D1.")
        return rows
    print("\n   D1 did not answer. Two reasons that is normal:")
    print("     the Worker is not deployed yet, or wrangler is not logged in here.")
    path = input("\n   Path to an exported JSON file, or return to go back.\n\n   > ").strip()
    if not path:
        return None
    return load_file(path)


def main():
    while True:
        os.system("clear")
        print()
        print("━" * 62)
        print("   COMMISSION STATEMENT")
        print("━" * 62)
        print()
        print(f"   Thailand side:  {cfg('originCode') or 'DESK'}   (shared desk)")
        print(f"   US visas:       {cfg('originCodeUs') or 'USOUT'}   (own book)")
        print(f"   Site:           {cfg('domain')}")
        print()
        print("   1.   Build a statement")
        print()
        print("   0.   Quit")
        print()
        print("─" * 62)
        c = input("\n   > ").strip()
        if c != "1":
            print()
            return
        rows = rows_from_somewhere()
        if not rows:
            input("\n   Nothing to count. Press return.  ")
            continue
        start, end, label = period()
        text = statement(rows, start, end, label)
        print("\n" + text)
        OUT.mkdir(exist_ok=True)
        f = OUT / f"statement-{label.lower().replace(' ', '-')}.txt"
        f.write_text(text + "\n")
        print(f"\n   Written: {f}")
        subprocess.run(["open", "-R", str(f)])
        input("\n   Press return.  ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
