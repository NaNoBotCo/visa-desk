#!/usr/bin/env python3
"""Render the US visa catalogue into both language pages.

    python3 tools/build_visas.py

Reads data/us-visas.json and writes site/us-visas/index.html and
site/th/us-visas/index.html. Everything else on the site is handwritten; this
one page is generated because thirty-one rows in two languages drift apart the
moment a person maintains them by hand.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = ROOT / "data" / "us-visas.json"
CONFIG = SITE / "assets" / "config.js"


def cfg(key):
    m = re.search(rf'\b{key}:\s*"([^"]*)"', CONFIG.read_text())
    return m.group(1) if m else ""


NAME = cfg("name")
DOMAIN = cfg("domain")
ORIGIN = cfg("origin")

WORDS = {
    "en": {
        "lang": "en", "dir": "ltr",
        "title": f"US visas for Thai nationals — {NAME}",
        "desc": "Document preparation for Thai nationals applying for US visas: visit, study, work, family, investment and after a refusal. Business plans, source-of-funds narratives and interview preparation, with US counsel on anything that is a filing.",
        "eyebrow": "The other direction",
        "h1": "Going to America.",
        "lede": "Thirty-one routes a Thai passport can take to the United States. We build the file; a US immigration attorney files it.",
        "cta": "Get a quote",
        "jump": "Jump to",
        "lane_h": "What we do, and what we don't",
        "lane": [
            "We assemble the file: the evidence, the civil documents, the certified translations, the timeline, the affidavits.",
            "We write the parts that are written: the business plan, the source-of-funds narrative, the job-creation and economic analysis, the personal statement.",
            "We prepare you for the interview, in Thai or in English.",
            "Legal advice and the filings themselves go through a US immigration attorney. We work alongside one; we are not one.",
        ],
        "cats": "Categories",
        "tagnote": "Two tags, and they are ours rather than anyone's ruling: <strong>Most asked for</strong> is what people walk in with. <strong>Biggest file</strong> is where the paperwork is longest and the outcome lasts longest.",
        "nav": [("../", "Thailand services"), ("./", "US visas"), ("../farang-buddy/", "Free app"), ("../partners/", "Partners")],
        "quote_h": "Tell us which one",
        "quote_p": "Or describe the situation and we name the category for you.",
        "other": ("ภาษาไทย", "../th/us-visas/"),
        "foot": "A Thai-registered company. Chiang Mai, Thailand.",
    },
    "th": {
        "lang": "th", "dir": "ltr",
        "title": f"วีซ่าอเมริกาสำหรับคนไทย — {NAME}",
        "desc": "บริการจัดเตรียมเอกสารวีซ่าสหรัฐอเมริกาสำหรับคนไทย: ท่องเที่ยว เรียน ทำงาน ครอบครัว ลงทุน และกรณีเคยถูกปฏิเสธ แผนธุรกิจ ที่มาของเงินทุน และการเตรียมสัมภาษณ์ โดยมีทนายความสหรัฐรับผิดชอบการยื่น",
        "eyebrow": "อีกทางหนึ่ง",
        "h1": "ไปอเมริกา",
        "lede": "สามสิบเอ็ดเส้นทางที่พาสปอร์ตไทยไปสหรัฐอเมริกาได้ เราจัดแฟ้มให้ ทนายความด้านตรวจคนเข้าเมืองของสหรัฐเป็นผู้ยื่น",
        "cta": "ขอใบเสนอราคา",
        "jump": "ข้ามไปที่",
        "lane_h": "เราทำอะไร และไม่ทำอะไร",
        "lane": [
            "เราจัดแฟ้ม: หลักฐาน เอกสารทะเบียนราษฎร์ คำแปลรับรอง ลำดับเหตุการณ์ และคำให้การ",
            "เราเขียนส่วนที่ต้องเขียน: แผนธุรกิจ ที่มาของเงินทุน การวิเคราะห์การจ้างงานและเศรษฐกิจ และจดหมายชี้แจงส่วนตัว",
            "เราเตรียมคุณสำหรับการสัมภาษณ์ ทั้งภาษาไทยและภาษาอังกฤษ",
            "การให้คำปรึกษาทางกฎหมายและการยื่นเรื่อง เป็นหน้าที่ของทนายความด้านตรวจคนเข้าเมืองของสหรัฐ เราทำงานร่วมกับทนาย แต่เราไม่ใช่ทนาย",
        ],
        "cats": "ประเภทวีซ่า",
        "tagnote": "ป้ายสองแบบนี้เป็นมุมมองของเราเอง ไม่ใช่คำวินิจฉัยของใคร: <strong>ถามมากที่สุด</strong> คือสิ่งที่คนเดินเข้ามาถามจริง <strong>งานเอกสารใหญ่ที่สุด</strong> คือเรื่องที่เอกสารยาวที่สุดและผลลัพธ์อยู่ยาวที่สุด",
        "nav": [("../", "บริการในไทย"), ("./", "วีซ่าอเมริกา"), ("../farang-buddy/", "แอปฟรี"), ("../partners/", "พันธมิตร")],
        "quote_h": "บอกเราว่าประเภทไหน",
        "quote_p": "หรือเล่าสถานการณ์มา แล้วเราจะบอกเองว่าเข้าข่ายประเภทใด",
        "other": ("English", "../../us-visas/"),
        "foot": "บริษัทจดทะเบียนในประเทศไทย จังหวัดเชียงใหม่",
    },
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mark_svg():
    return (
        '<svg class="stamp" viewBox="0 0 40 40" aria-hidden="true">'
        '<rect x="2" y="2" width="36" height="36" rx="9" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-dasharray="4.2 3.1"/>'
        '<path d="M12 21.5l5.4 5.4L28.6 15" fill="none" stroke="#c9761a" stroke-width="3.4" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


def wordmark(lang):
    words = NAME.split()
    light, strong = " ".join(words[:-2]), " ".join(words[-2:])
    if not light:
        return f"<span><strong>{esc(strong)}</strong></span>"
    return f"<span>{esc(light)} <strong>{esc(strong)}</strong></span>"


def render(lang, data):
    w = WORDS[lang]
    tags = data["tags"]
    url = f"{ORIGIN}/us-visas/" if lang == "en" else f"{ORIGIN}/th/us-visas/"
    alt_en = f"{ORIGIN}/us-visas/"
    alt_th = f"{ORIGIN}/th/us-visas/"
    home = "../" if lang == "en" else "../"
    assets = "../assets" if lang == "en" else "../../assets"

    jump = "\n".join(
        f'        <a href="#{g["id"]}">{esc(g[lang]["name"])}</a>'
        for g in data["groups"]
    )

    groups = []
    for g in data["groups"]:
        rows = []
        for it in g["items"]:
            pills = "".join(
                f'<span class="pill {t}">{esc(tags[t][lang])}</span>' for t in it.get("tags", [])
            )
            rows.append(
                f'''          <li class="visa">
            <span class="code">{esc(it["code"])}</span>
            <span class="body"><strong>{esc(it[lang]["name"])}</strong>
              <span class="blurb">{esc(it[lang]["blurb"])}</span></span>
            <span class="pills">{pills}</span>
          </li>'''
            )
        groups.append(
            f'''      <section class="vgroup" id="{g["id"]}">
        <h3>{esc(g[lang]["name"])}</h3>
        <p class="gblurb">{esc(g[lang]["blurb"])}</p>
        <ul class="visas">
{chr(10).join(rows)}
        </ul>
      </section>'''
        )

    lane = "\n".join(f"        <li>{esc(x)}</li>" for x in w["lane"])
    nav = "\n".join(f'      <a href="{h}">{esc(t)}</a>' for h, t in w["nav"])

    services = []
    for g in data["groups"]:
        for it in g["items"]:
            services.append(
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": f'{it["code"]} — {it["en"]["name"]}',
                        "serviceType": "US visa document preparation",
                    },
                }
            )
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": url,
        "url": url,
        "name": w["title"],
        "description": w["desc"],
        "inLanguage": lang,
        "isPartOf": {"@id": f"{ORIGIN}/#site"},
        "about": {"@id": f"{ORIGIN}/#org"},
        "mainEntity": {
            "@type": "Service",
            "name": "US visa document preparation for Thai nationals",
            "provider": {"@id": f"{ORIGIN}/#org"},
            "areaServed": {"@type": "Country", "name": "Thailand"},
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "US visa categories prepared",
                "itemListElement": services,
            },
        },
    }

    return f'''<!doctype html>
<html lang="{w["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(w["title"])}</title>
<meta name="description" content="{esc(w["desc"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="th" href="{alt_th}">
<link rel="alternate" hreflang="x-default" href="{alt_en}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(w["title"])}">
<meta property="og:description" content="{esc(w["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ORIGIN}/assets/share.png">
<meta property="og:locale" content="{"en_US" if lang == "en" else "th_TH"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fbf8f2" media="(prefers-color-scheme:light)">
<meta name="theme-color" content="#131110" media="(prefers-color-scheme:dark)">
<link rel="icon" href="{assets}/mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="{assets}/style.css">
<script src="{assets}/config.js"></script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<a class="skip" href="#cats">{esc(w["cats"])}</a>

<header class="top" id="top">
  <div class="wrap">
    <a class="mark" href="{home}">{mark_svg()}{wordmark(lang)}</a>
    <nav class="nav">
{nav}
      <a class="lang" href="{w["other"][1]}" hreflang="{"th" if lang == "en" else "en"}">{esc(w["other"][0])}</a>
      <a class="btn accent" href="#quote">{esc(w["cta"])}</a>
    </nav>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span> {esc(w["eyebrow"])}</p>
    <h1>{esc(w["h1"])}</h1>
    <p class="lede">{esc(w["lede"])}</p>
    <div class="cta-row"><a class="btn accent" href="#quote">{esc(w["cta"])}</a></div>
    <p class="chip" id="refchip">Ref <code id="refcode"></code></p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head rise"><h2>{esc(w["lane_h"])}</h2></div>
    <ul class="ticks lane">
{lane}
    </ul>
  </div>
</section>

<section id="cats">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{esc(w["cats"])}</h2>
      <p>{w["tagnote"]}</p>
    </div>
    <nav class="jump" aria-label="{esc(w["jump"])}">
{jump}
    </nav>

{chr(10).join(groups)}
  </div>
</section>

<section class="alt" id="quote">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{esc(w["quote_h"])}</h2>
      <p>{esc(w["quote_p"])}</p>
    </div>
    <p><a class="btn accent" href="{home}#quote">{esc(w["cta"])}</a></p>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div>
      <p><strong>{esc(NAME)}</strong></p>
      <p style="margin-top:.35rem">{esc(w["foot"])}</p>
      <p style="margin-top:.35rem" id="contactline"></p>
    </div>
    <nav>
{nav}
      <a href="{w["other"][1]}" hreflang="{"th" if lang == "en" else "en"}">{esc(w["other"][0])}</a>
    </nav>
  </div>
</footer>
<script src="{assets}/app.js"></script>
</body>
</html>
'''


def main():
    data = json.loads(DATA.read_text())
    for lang, out in (("en", SITE / "us-visas" / "index.html"),
                      ("th", SITE / "th" / "us-visas" / "index.html")):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(lang, data))
        n = sum(len(g["items"]) for g in data["groups"])
        print(f"   {out.relative_to(ROOT)}  ({n} categories)")


if __name__ == "__main__":
    main()
