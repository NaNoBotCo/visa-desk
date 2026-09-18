#!/usr/bin/env python3
"""Contrast — measure every colour pair the site actually puts together.

    python3 tools/contrast.py

Reads the tokens out of site/assets/style.css for both the light and the dark
scheme, works out the WCAG 2.1 contrast ratio for each pair that appears on
screen, and fails if any of them falls under its target.

Targets used here:
    body text          7.0   (AAA for normal text)
    secondary text     4.5   (AA)
    large text         4.5   (AA large, 24px+ or bold 19px+)
    text on a button   4.5
    non-text (borders, focus rings, icons)   3.0

Run by `make check`, so a palette change cannot quietly drop below them.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "site" / "assets" / "style.css"


# ------------------------------------------------------------------ colour

def parse_hex(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(parse_hex(a)), luminance(parse_hex(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ------------------------------------------------------------------- tokens

def tokens(css, scheme):
    """Light tokens come from bare :root; dark ones override them."""
    out = {}
    root = re.search(r":root\s*\{(.*?)\}", css, re.S)
    if root:
        for k, v in re.findall(r"--([a-z0-9-]+)\s*:\s*([^;]+);", root.group(1)):
            out[k] = v.strip()
    if scheme == "dark":
        for block in re.findall(r"@media \(prefers-color-scheme:dark\)[^{]*\{\s*:root\s*\{(.*?)\}", css, re.S):
            for k, v in re.findall(r"--([a-z0-9-]+)\s*:\s*([^;]+);", block):
                out[k] = v.strip()
    return {k: v for k, v in out.items() if v.startswith("#")}


# The pairs the page actually renders. (foreground, background, target, what)
PAIRS = [
    ("ink", "paper", 7.0, "body text on the page"),
    ("ink", "paper-2", 7.0, "body text on a banded section"),
    ("ink", "card", 7.0, "body text on a card"),
    ("ink-2", "paper", 4.5, "secondary text on the page"),
    ("ink-2", "paper-2", 4.5, "secondary text on a banded section"),
    ("ink-2", "card", 4.5, "secondary text on a card"),
    ("ink-3", "paper", 4.5, "hints and captions on the page"),
    ("ink-3", "card", 4.5, "hints and captions on a card"),
    ("marigold", "paper", 3.0, "accent against the page"),
    ("jade", "card", 4.5, "tick marks and success text"),
    ("chip-ink", "chip-bg", 4.5, "code on a referral chip"),
    ("field-line", "field-bg", 3.0, "input border, so the field is findable"),
    ("focus", "paper", 3.0, "focus ring against the page"),
    ("focus", "card", 3.0, "focus ring on a card"),
    ("line", "paper", 1.2, "hairline between sections (decorative)"),
]

# Buttons: text colour is fixed in the rule, not a token.
BUTTONS = [
    ("btn-ink", "accent", 4.5, "button label on the accent fill"),
    ("line-green-ink", "line-green", 4.5, "button label on the LINE fill"),
    ("paper", "ink", 4.5, "button label on the dark fill"),
    ("pill-ink", "pill-bg", 4.5, "tag pill text"),
]


def accent_of(t):
    """The accent fill is what .btn.accent paints."""
    return t.get("accent", t.get("marigold", "#000000"))


def main():
    css = CSS.read_text()
    fails = 0
    for scheme in ("light", "dark"):
        t = tokens(css, scheme)
        t["accent"] = accent_of(t)
        print(f"\n{scheme}\n")
        rows = [(f, b, target, what) for f, b, target, what in PAIRS]
        rows += BUTTONS
        for fg, bg, target, what in rows:
            a = t.get(fg, fg if fg.startswith("#") else None)
            b = t.get(bg, bg if bg.startswith("#") else None)
            if not a or not b:
                continue
            r = ratio(a, b)
            ok = r >= target
            fails += 0 if ok else 1
            print(f"  {'ok  ' if ok else 'FAIL'}  {r:5.2f}  (needs {target:.1f})  {what}")
    print()
    if fails:
        print(f"{fails} pair(s) under target.\n")
        return 1
    print("every pair meets its target.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
