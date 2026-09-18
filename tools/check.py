#!/usr/bin/env python3
"""Checks that run before the site goes out, and in CI on every push.

    python3 tools/check.py

Fails loudly on the things that are easy to break in a clone: a half-swapped
domain, JSON-LD that no longer parses, a local path left in a page, a missing
robots or sitemap, a page that names a person.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CONFIG = SITE / "assets" / "config.js"

# Hosts the site may LINK to. Everything a page LOADS still has to be
# same-origin; these are destinations a person taps, not resources fetched.
SHARE_HOSTS = {
    "line.me", "social-plugins.line.me", "wa.me", "t.me",
    "twitter.com", "x.com", "www.facebook.com",
}
VOCAB_HOSTS = {
    "schema.org", "creativecommons.org", "api.resend.com",
    "sitemaps.org", "www.sitemaps.org", "www.w3.org",
}

PAGES = ["index.html", "us-visas/index.html", "farang-buddy/index.html", "partners/index.html",
         "white-label/index.html",
         "th/index.html", "th/us-visas/index.html", "th/farang-buddy/index.html",
         "th/partners/index.html", "th/white-label/index.html"]
PAIRS = [("index.html", "th/index.html"),
         ("us-visas/index.html", "th/us-visas/index.html"),
         ("farang-buddy/index.html", "th/farang-buddy/index.html"),
         ("partners/index.html", "th/partners/index.html"),
         ("white-label/index.html", "th/white-label/index.html")]
REQUIRED = ["robots.txt", "sitemap.xml", "llms.txt", "assets/style.css",
            "assets/app.js", "assets/config.js", "assets/share.png", "assets/mark.svg",
            "assets/farang-buddy-qr.png",
            "assets/line-qr.png", "assets/site-qr.png"]

fails = []

# Built, not written, so this file does not match its own check.
HOME_MARK = "/" + "Users" + "/"


def fail(msg):
    fails.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg):
    print(f"  ok    {msg}")


def config_value(key):
    m = re.search(rf'\b{key}:\s*"([^"]*)"', CONFIG.read_text())
    return m.group(1) if m else ""


def text_files():
    for p in SITE.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".html", ".txt", ".xml", ".js", ".json"}:
            yield p


def main():
    print("\nsite\n")

    for rel in REQUIRED:
        if (SITE / rel).exists():
            ok(rel)
        else:
            fail(f"missing {rel}")

    domain = config_value("domain")
    origin = config_value("origin")
    if not domain:
        fail("config.js has no domain")
    if origin != f"https://{domain}":
        fail(f"config origin {origin!r} does not match domain {domain!r}")
    else:
        ok(f"domain {domain}")

    print("\njson-ld\n")
    for rel in PAGES:
        s = (SITE / rel).read_text()
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        if not blocks:
            fail(f"{rel} has no JSON-LD")
        for b in blocks:
            try:
                json.loads(b)
            except json.JSONDecodeError as e:
                fail(f"{rel} JSON-LD: {e}")
        else:
            ok(f"{rel} ({len(blocks)} block(s))")

    print("\nlanguages\n")

    for en, th in PAIRS:
        for rel in (en, th):
            if not (SITE / rel).exists():
                fail(f"missing {rel}")
                continue
            s = (SITE / rel).read_text()
            for tag in ('hreflang="en"', 'hreflang="th"', 'hreflang="x-default"'):
                if tag not in s:
                    fail(f"{rel} has no {tag}")
        if (SITE / th).exists() and 'lang="th"' not in (SITE / th).read_text()[:400]:
            fail(f"{th} is not marked lang=\"th\"")
    if not fails:
        ok(f"{len(PAIRS)} page(s), both languages, linked both ways")

    built = ROOT / "tools" / "build_visas.py"
    if built.exists():
        import subprocess
        before = [(SITE / r).read_text() for r in ("us-visas/index.html", "th/us-visas/index.html")]
        subprocess.run([sys.executable, str(built)], capture_output=True, check=True)
        after = [(SITE / r).read_text() for r in ("us-visas/index.html", "th/us-visas/index.html")]
        if before != after:
            fail("the US visa pages are out of date — run tools/build_visas.py and commit")
        else:
            ok("US visa pages match data/us-visas.json")

    bad_links = []
    for rel in PAGES:
        f = SITE / rel
        if not f.exists():
            continue
        for m in re.findall(r'href="([^"]*index\.html[^"]*)"', f.read_text()):
            bad_links.append(f"{rel} -> {m}")
    if bad_links:
        for b in bad_links:
            fail(f"link to index.html, which the host redirects: {b}")
    else:
        ok("internal links use the directory form the canonical tags declare")

    print("\ncontrast\n")
    import subprocess as _sp
    r = _sp.run([sys.executable, str(ROOT / "tools" / "contrast.py")], capture_output=True, text=True)
    if r.returncode == 0:
        ok("every colour pair on the page meets its target")
    else:
        for ln in r.stdout.splitlines():
            if "FAIL" in ln:
                fail(ln.strip())

    print("\nhygiene\n")

    # Hosts the site is allowed to point at: the configured backend, and the
    # free app it gives away.
    endpoint = config_value("endpoint")
    extra = {"farangbuddy.netlify.app"}          # the free app the site gives away
    credit = config_value("url")                  # whoever built it
    for candidate in (endpoint, credit):
        if candidate:
            m = re.match(r"https?://([^/]+)", candidate)
            if m:
                extra.add(m.group(1))

    stale = []
    for p in text_files():
        s = p.read_text()
        for m in re.findall(r'https?://([a-z0-9.-]+\.[a-z]{2,})', s):
            if m in VOCAB_HOSTS or m in SHARE_HOSTS or m in extra:
                continue
            if m != domain:
                stale.append(f"{p.relative_to(SITE)} -> {m}")
    if stale:
        for s in sorted(set(stale)):
            fail(f"link to another host: {s}")
    else:
        ok("every absolute link points at the configured domain")

    leaks = [str(p.relative_to(SITE)) for p in text_files() if HOME_MARK in p.read_text()]
    if leaks:
        for l in leaks:
            fail(f"local path in {l}")
    else:
        ok("no local paths")

    todo = [str(p.relative_to(SITE)) for p in text_files()
            if re.search(r"\b(TODO|FIXME|XXX|PUT-THE-)", p.read_text())]
    if todo:
        for t in todo:
            fail(f"placeholder left in {t}")
    else:
        ok("no placeholders")

    import subprocess
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                                 text=True, check=True).stdout.split()
    except Exception:
        tracked = []
    repo_leaks = []
    for rel in tracked:
        f = ROOT / rel
        if not f.is_file() or f.suffix.lower() in {".png", ".jpg", ".ico", ".woff2"}:
            continue
        try:
            if HOME_MARK in f.read_text():
                repo_leaks.append(rel)
        except (UnicodeDecodeError, OSError):
            continue
    if repo_leaks:
        for r in repo_leaks:
            fail(f"home-directory path in a tracked file: {r}")
    elif tracked:
        ok(f"no home-directory paths in {len(tracked)} tracked file(s)")

    names = ROOT / ".names-not-on-the-site"
    if names.exists():
        banned = [w.strip() for w in names.read_text().splitlines()
                  if w.strip() and not w.startswith("#")]
        hits = []
        candidates = [ROOT / r for r in tracked] if tracked else list(text_files())
        for p in candidates:
            if not p.is_file() or p.suffix.lower() in {".png", ".jpg", ".ico", ".woff2"}:
                continue
            try:
                body = p.read_text().lower()
            except (UnicodeDecodeError, OSError):
                continue
            for w in banned:
                if w.lower() in body:
                    hits.append(f"{p.relative_to(ROOT)} -> {w}")
        if hits:
            for h in hits:
                fail(f"name on the site: {h}")
        else:
            ok(f"none of the {len(banned)} withheld name(s) appear in tracked files")

    print()
    if fails:
        print(f"{len(fails)} problem(s).\n")
        return 1
    print("clean.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
