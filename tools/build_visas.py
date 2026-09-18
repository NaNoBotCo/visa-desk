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
INBOX = cfg("inbox")

WORDS = {
    "en": {
        "lang": "en", "dir": "ltr",
        "title": f"US visas for Thai nationals — {NAME}",
        "desc": "Document preparation for Thai nationals applying for US visas: visit, study, work, family, investment and after a refusal. Business plans, source-of-funds narratives and interview preparation, with US counsel on anything that is a filing.",
        "eyebrow": "The other direction",
        "h1": "Going to America.",
        "lede": "Thirty-one kinds of US visa a Thai passport holder can apply for. We prepare your file. A US immigration attorney files it.",
        "cta": "Get a quote",
        "jump": "Jump to",
        "lane_h": "What we do, and what we don't",
        "lane": [
            "We put the file together: the evidence, the official documents, the certified translations, the timeline and the sworn statements.",
            "We write the parts that must be written: the business plan, where the money came from, the job and economic analysis, and your personal statement.",
            "We prepare you for the interview, in Thai or in English.",
            "Legal advice and the filing itself are done by a US immigration attorney. We work with one. We are not one.",
        ],
        "cats": "Categories",
        "tagnote": "These two labels are our own opinion, not an official decision. <strong>Most asked for</strong> means people ask us for it often. <strong>Biggest file</strong> means the paperwork is long and the result lasts a long time.",
        "nav": [("../", "Thailand services"), ("./", "US visas"), ("../farang-buddy/", "Free app"), ("../partners/", "Partners")],
        "quote_h": "Start a case",
        "quote_p": "If you are not sure which one, describe your situation and we tell you.",
        "other": ("ภาษาไทย", "../th/us-visas/"),
        "wl": ("Licensing", "../white-label/"),
        "foot": "US visa document preparation. Chiang Mai, Thailand.",
        "run_h": "How a case runs",
        "run_p": "",
        "run": [
            ("Intake", "What you want, who is helping you in the United States, and what you have already tried. About one hour, in Thai or English."),
            ("The category", "We tell you which visa fits you, and say clearly if a different one would be better."),
            ("The evidence plan", "A list, in order, of every document you need and who issues it. Many refusals happen because one document was asked for too late."),
            ("The written work", "The parts somebody has to write, not collect. This is the part that decides most cases."),
            ("Attorney review", "A US immigration attorney checks the file and submits it. We hand over a file that is ordered and easy to read."),
            ("Interview preparation", "We practise the questions, in the order they are asked, in the language you will answer in."),
            ("After", "Approved, refused, or asked for more evidence. Each one has a next step, and we tell you what it is."),
        ],
        "write_h": "The written work",
        "write_p": "Collecting documents is only half the work. These are the parts somebody has to write, and the officer reads them closely.",
        "write": [
            ("Business plan", "Written to the standard these cases are judged by: the market, the company structure, the money, and a hiring plan the numbers support."),
            ("Source-of-funds narrative", "Where every baht came from, traced back to a source someone else can check, with a document for each step."),
            ("Job-creation and economic analysis", "What the investment does in the local economy, in the form the adjudicator expects to see it."),
            ("Personal statement and timeline", "The story of your relationship, career or work, told once and the same way throughout, with the evidence matched to it."),
            ("Certified translation", "Thai official documents into English, certified, with names spelled the same way as in your passport."),
            ("Response to a request for evidence", "We answer exactly what was asked, in the order it was asked."),
        ],
        "sep": "This is a separate business from the Thailand services on this site. Messages sent from this page go only to the US team.",
        "faq_h": "Questions",
        "faq": [
            ("Are you attorneys?", "No, and we say so on every page. The desk assembles the file and writes the written pieces. A US immigration attorney gives the legal advice and does the filing. If someone tells you a non-attorney can do that part, walk away from them."),
            ("I was refused before. Is that the end of it?", "No. What matters is what has changed since then, written down with evidence, before you pay the fee again. That is a separate piece of work and we price it separately."),
            ("Do you guarantee an outcome?", "Nobody can, and anyone who does is selling you something. The consulate decides. What we control is whether the file makes the case it should."),
            ("How long does it take?", "It depends on the visa type and on how busy the consulate is. We do not publish times on this page, because a published time is out of date very quickly. Your written price tells you the current situation for your case."),
            ("Can you work from Chiang Mai if I am somewhere else?", "Yes. Most of the work is documents and phone calls. Only the interview needs you there in person, and we prepare you for it before that."),
            ("What does it cost?", "We give a written price for each case before any work starts. The writing is priced separately from collecting the documents, because they are different amounts of work."),
        ],
        "f_name": "Name", "f_contact": "Email, LINE or WhatsApp",
        "f_cat": "Which category", "f_cat_unsure": "Not sure — tell me",
        "f_before": "Have you applied before?",
        "f_before_opts": ["No, this is the first time", "Yes, and it was approved", "Yes, and it was refused", "Yes, and it is still pending"],
        "f_who": "Who is on the US side", "f_who_ph": "An employer, a spouse, a school, a business of your own, nobody yet",
        "f_where": "Where you are", "f_where_ph": "Chiang Mai, Bangkok, Isaan, abroad…",
        "f_notes": "The situation, in your own words",
        "f_notes_ph": "Dates that matter, a refusal, a deadline, a business you already run.",
        "f_send": "Send it", "f_status": "This goes to the US desk.",
        "f_noscript_a": "Your browser is not running scripts. Email the same details to ",
        "f_noscript_b": " and a price comes back.",
    },
    "th": {
        "lang": "th", "dir": "ltr",
        "title": f"วีซ่าอเมริกาสำหรับคนไทย — {NAME}",
        "desc": "บริการจัดเตรียมเอกสารวีซ่าสหรัฐอเมริกาสำหรับคนไทย: ท่องเที่ยว เรียน ทำงาน ครอบครัว ลงทุน และกรณีเคยถูกปฏิเสธ แผนธุรกิจ ที่มาของเงินทุน และการเตรียมสัมภาษณ์ โดยมีทนายความสหรัฐรับผิดชอบการยื่น",
        "eyebrow": "อีกทางหนึ่ง",
        "h1": "ไปอเมริกา",
        "lede": "วีซ่าสหรัฐ 31 ประเภทที่คนถือพาสปอร์ตไทยยื่นได้ เราเตรียมแฟ้มให้คุณ ทนายความด้านตรวจคนเข้าเมืองของสหรัฐเป็นผู้ยื่น",
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
        "tagnote": "ป้ายสองแบบนี้เป็นความเห็นของเราเอง ไม่ใช่คำวินิจฉัยทางการ <strong>ถามมากที่สุด</strong> หมายถึงมีคนถามเราบ่อย <strong>งานเอกสารใหญ่ที่สุด</strong> หมายถึงเอกสารเยอะ และผลลัพธ์อยู่ได้นาน",
        "nav": [("../", "บริการในไทย"), ("./", "วีซ่าอเมริกา"), ("../farang-buddy/", "แอปฟรี"), ("../partners/", "พันธมิตร")],
        "quote_h": "เริ่มเรื่องของคุณ",
        "quote_p": "ถ้าไม่แน่ใจว่าประเภทไหน เล่าสถานการณ์มา แล้วเราจะบอกให้",
        "other": ("English", "../../us-visas/"),
        "wl": ("สิทธิ์ใช้งาน", "../white-label/"),
        "foot": "บริการจัดเตรียมเอกสารวีซ่าสหรัฐ จังหวัดเชียงใหม่",
        "run_h": "เรื่องหนึ่งเดินอย่างไร",
        "run_p": "",
        "run": [
            ("รับเรื่อง", "คุณต้องการอะไร ใครอยู่ฝั่งสหรัฐให้คุณ และเคยลองอะไรมาแล้ว ใช้เวลาราวหนึ่งชั่วโมง ภาษาไทยหรืออังกฤษก็ได้"),
            ("เลือกประเภท", "เราบอกว่าประเภทไหนตรงกับคุณ และบอกตรง ๆ ถ้าอีกประเภทหนึ่งน่าจะดีกว่า"),
            ("แผนหลักฐาน", "รายการเอกสารเรียงลำดับ พร้อมบอกว่าใครเป็นผู้ออกให้ เรื่องที่ถูกปฏิเสธส่วนใหญ่คือเอกสารที่ไม่มีใครขอไว้ทัน"),
            ("งานเขียน", "ส่วนที่ต้องเขียน ไม่ใช่แค่รวบรวม ตรงนี้คือจุดที่แฟ้มหนึ่งชนะ"),
            ("ทนายความตรวจ", "ทนายความด้านตรวจคนเข้าเมืองของสหรัฐตรวจและยื่น เราส่งมอบแฟ้มที่จัดมาเพื่อให้อ่าน ไม่ใช่กล่องเอกสาร"),
            ("เตรียมสัมภาษณ์", "คำถามตามลำดับที่มันจะมาจริง ในภาษาที่คุณจะใช้ตอบ"),
            ("หลังจากนั้น", "อนุมัติ ปฏิเสธ หรือขอหลักฐานเพิ่ม แต่ละทางมีหมากถัดไป และเราบอกว่าเป็นหมากไหน"),
        ],
        "write_h": "งานเขียน",
        "write_p": "การรวบรวมเอกสารเป็นแค่ครึ่งเดียวของงาน ส่วนด้านล่างนี้คือสิ่งที่ต้องมีคนเขียน และเจ้าหน้าที่อ่านอย่างละเอียด",
        "write": [
            ("แผนธุรกิจ", "เขียนตามมาตรฐานที่ใช้พิจารณาจริง ทั้งตลาด โครงสร้าง เงินทุน และแผนการจ้างงานที่ตัวเลขรองรับได้"),
            ("ที่มาของเงินทุน", "ทุกบาทมาจากไหน สาวถึงต้นทางที่คนนอกตรวจสอบได้ พร้อมเอกสารทุกทอด"),
            ("การวิเคราะห์การจ้างงานและเศรษฐกิจ", "เงินลงทุนก้อนนี้ทำอะไรกับเศรษฐกิจในพื้นที่ เขียนในรูปแบบที่เจ้าหน้าที่คาดว่าจะได้เห็น"),
            ("คำชี้แจงส่วนตัวและลำดับเหตุการณ์", "เรื่องความสัมพันธ์ อาชีพ หรือผลงาน เล่าครั้งเดียว ให้ตรงกันทั้งหมด และผูกกับหลักฐานทีละจุด"),
            ("คำแปลรับรอง", "เอกสารราชการไทยเป็นภาษาอังกฤษ พร้อมรับรอง และสะกดชื่อให้ตรงกับพาสปอร์ต"),
            ("การตอบหนังสือขอหลักฐานเพิ่ม", "ตอบสิ่งที่เขาถามจริง ตามลำดับที่เขาถาม"),
        ],
        "sep": "ส่วนนี้เป็นคนละธุรกิจกับบริการฝั่งประเทศไทยในเว็บเดียวกัน ข้อความที่ส่งจากหน้านี้ไปถึงทีมวีซ่าอเมริกาเท่านั้น",
        "faq_h": "คำถามที่พบบ่อย",
        "faq": [
            ("คุณเป็นทนายความหรือเปล่า", "ไม่ใช่ และเราบอกไว้ทุกหน้า เราจัดแฟ้มและเขียนส่วนที่ต้องเขียน ส่วนคำปรึกษาทางกฎหมายและการยื่นเป็นของทนายความสหรัฐ ถ้าใครบอกคุณว่าคนที่ไม่ใช่ทนายทำส่วนนั้นได้ ให้เดินออกมา"),
            ("เคยถูกปฏิเสธมาก่อน จบแล้วใช่ไหม", "ไม่ใช่ เป็นแค่จุดตั้งต้น สิ่งที่สำคัญคืออะไรเปลี่ยนไปตั้งแต่ตอนนั้น เขียนไว้และมีหลักฐาน ก่อนจะจ่ายค่าธรรมเนียมอีกครั้ง งานส่วนนี้เราเสนอราคาแยก"),
            ("รับประกันผลได้ไหม", "ไม่มีใครรับประกันได้ และใครที่รับประกันคือกำลังขายของ สถานทูตเป็นผู้ตัดสิน สิ่งที่เราคุมได้คือแฟ้มนั้นพูดในสิ่งที่ควรพูดหรือเปล่า"),
            ("ใช้เวลานานแค่ไหน", "ขึ้นกับประเภทและช่วงเวลา เราไม่ประกาศระยะเวลาไว้ในเว็บ เพราะพอเขียนเสร็จก็เก่าแล้ว ใบเสนอราคาจะบอกภาพปัจจุบันของเรื่องคุณ"),
            ("อยู่จังหวัดอื่น ทำงานกับเชียงใหม่ได้ไหม", "ได้ งานส่วนใหญ่คือเอกสารและการคุยกัน ส่วนที่ต้องไปด้วยตัวเองคือวันสัมภาษณ์ และการเตรียมตัวเกิดขึ้นก่อนหน้านั้น"),
            ("ราคาเท่าไร", "เสนอราคาเป็นลายลักษณ์อักษรต่อหนึ่งเรื่อง ก่อนเริ่มงาน งานเขียนคิดแยกจากงานจัดแฟ้ม เพราะเป็นงานคนละปริมาณ"),
        ],
        "f_name": "ชื่อ", "f_contact": "อีเมล LINE หรือ WhatsApp",
        "f_cat": "ประเภทไหน", "f_cat_unsure": "ไม่แน่ใจ — ช่วยดูให้หน่อย",
        "f_before": "เคยยื่นมาก่อนไหม",
        "f_before_opts": ["ยังไม่เคย นี่เป็นครั้งแรก", "เคย และได้รับอนุมัติ", "เคย และถูกปฏิเสธ", "เคย และยังรออยู่"],
        "f_who": "ฝั่งสหรัฐมีใคร", "f_who_ph": "นายจ้าง คู่สมรส สถานศึกษา ธุรกิจของคุณเอง หรือยังไม่มี",
        "f_where": "คุณอยู่ที่ไหน", "f_where_ph": "เชียงใหม่ กรุงเทพ อีสาน ต่างประเทศ…",
        "f_notes": "เล่าสถานการณ์ด้วยคำของคุณเอง",
        "f_notes_ph": "วันที่สำคัญ การถูกปฏิเสธ กำหนดเส้นตาย ธุรกิจที่คุณทำอยู่แล้ว",
        "f_send": "ส่ง", "f_status": "ข้อมูลนี้ไปที่ทีมวีซ่าอเมริกา",
        "f_noscript_a": "เบราว์เซอร์ของคุณปิดสคริปต์อยู่ ส่งรายละเอียดเดียวกันมาที่ ",
        "f_noscript_b": " แล้วราคาจะกลับไป",
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
    home = "../"
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
                '          <li class="visa">\n'
                f'            <span class="code">{esc(it["code"])}</span>\n'
                f'            <span class="body"><strong>{esc(it[lang]["name"])}</strong>\n'
                f'              <span class="blurb">{esc(it[lang]["blurb"])}</span></span>\n'
                f'            <span class="pills">{pills}</span>\n'
                "          </li>"
            )
        groups.append(
            f'      <section class="vgroup" id="{g["id"]}">\n'
            f'        <h3>{esc(g[lang]["name"])}</h3>\n'
            f'        <p class="gblurb">{esc(g[lang]["blurb"])}</p>\n'
            '        <ul class="visas">\n'
            + "\n".join(rows)
            + "\n        </ul>\n      </section>"
        )

    lane = "\n".join(f"        <li>{esc(x)}</li>" for x in w["lane"])
    nav = "\n".join(f'      <a href="{h}">{esc(t)}</a>' for h, t in w["nav"])

    run = "\n".join(
        '      <div class="step rise">\n'
        f"        <h3>{esc(t)}</h3>\n"
        f"        <p>{esc(b)}</p>\n"
        "      </div>"
        for t, b in w["run"]
    )

    write = "\n".join(
        '      <article class="card rise">\n'
        f"        <h3>{esc(t)}</h3>\n"
        f"        <p>{esc(b)}</p>\n"
        "      </article>"
        for t, b in w["write"]
    )

    faq = "\n".join(
        f"      <details><summary>{esc(q)}</summary>\n        <p>{esc(a)}</p></details>"
        for q, a in w["faq"]
    )

    # category picker, grouped exactly like the catalogue above it
    opts = [f'            <option value="">{esc(w["f_cat_unsure"])}</option>']
    for g in data["groups"]:
        opts.append(f'            <optgroup label="{esc(g[lang]["name"])}">')
        for it in g["items"]:
            label = f'{it["code"]} — {it[lang]["name"]}'
            opts.append(f"              <option>{esc(label)}</option>")
        opts.append("            </optgroup>")
    cat_options = "\n".join(opts)

    before = "\n".join(f"            <option>{esc(o)}</option>" for o in w["f_before_opts"])

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
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url,
                "url": url,
                "name": w["title"],
                "description": w["desc"],
                "inLanguage": lang,
                "isPartOf": {"@id": f"{ORIGIN}/#site"},
                "mainEntity": {"@id": f"{url}#service"},
            },
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": "US visa document preparation for Thai nationals",
                "serviceType": "Visa document preparation",
                "areaServed": {"@type": "Country", "name": "Thailand"},
                "availableLanguage": ["en", "th"],
                "description": (
                    "Assembly of the evidence file, certified translation, the written "
                    "pieces (business plan, source-of-funds narrative, job-creation and "
                    "economic analysis, personal statement) and interview preparation. "
                    "Legal advice and filings go through a US immigration attorney."
                ),
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": "US visa categories prepared",
                    "itemListElement": services,
                },
            },
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "inLanguage": lang,
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in w["faq"]
                ],
            },
        ],
    }

    other_lang = "th" if lang == "en" else "en"
    locale = "en_US" if lang == "en" else "th_TH"

    return f"""<!doctype html>
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
<meta property="og:locale" content="{locale}">
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
<a class="skip" href="#quote">{esc(w["quote_h"])}</a>

<header class="top" id="top">
  <div class="wrap">
    <a class="mark" href="{home}">{mark_svg()}{wordmark(lang)}</a>
    <nav class="nav">
{nav}
      <a class="lang" href="{w["other"][1]}" hreflang="{other_lang}">{esc(w["other"][0])}</a>
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
    <div class="cta-row"><a class="btn accent" href="#quote">{esc(w["cta"])}</a>
      <a class="btn ghost" href="#cats">{esc(w["cats"])}</a></div>
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

<section id="run">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{esc(w["run_h"])}</h2>
      {'<p>' + esc(w["run_p"]) + '</p>' if w["run_p"] else ''}
    </div>
    <div class="steps">
{run}
    </div>
  </div>
</section>

<section class="alt" id="written">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{esc(w["write_h"])}</h2>
      <p>{esc(w["write_p"])}</p>
    </div>
    <div class="grid">
{write}
    </div>
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

<section class="alt" id="faq">
  <div class="wrap">
    <div class="section-head rise"><h2>{esc(w["faq_h"])}</h2></div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>

<section id="quote">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{esc(w["quote_h"])}</h2>
      <p>{esc(w["quote_p"])}</p>
    </div>

    <form class="panel" id="quoteform" data-line="us" novalidate>
      <div class="fields">
        <div class="field">
          <label for="f-name">{esc(w["f_name"])}</label>
          <input id="f-name" name="name" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="f-contact">{esc(w["f_contact"])}</label>
          <input id="f-contact" name="contact" autocomplete="email" required>
        </div>
        <div class="field wide">
          <label for="f-visa">{esc(w["f_cat"])}</label>
          <select id="f-visa" name="visa">
{cat_options}
          </select>
        </div>
        <div class="field">
          <label for="f-need">{esc(w["f_before"])}</label>
          <select id="f-need" name="need">
{before}
          </select>
        </div>
        <div class="field">
          <label for="f-who">{esc(w["f_who"])}</label>
          <input id="f-who" name="who" placeholder="{esc(w["f_who_ph"])}">
        </div>
        <div class="field">
          <label for="f-where">{esc(w["f_where"])}</label>
          <input id="f-where" name="where" placeholder="{esc(w["f_where_ph"])}">
        </div>
        <div class="field wide">
          <label for="f-notes">{esc(w["f_notes"])}</label>
          <textarea id="f-notes" name="notes" placeholder="{esc(w["f_notes_ph"])}"></textarea>
        </div>
        <div class="field hp" aria-hidden="true">
          <label for="f-company">Company</label>
          <input id="f-company" name="company" tabindex="-1" autocomplete="off">
        </div>
      </div>

      <input type="hidden" name="origin" id="f-origin">
      <input type="hidden" name="line" id="f-line">
      <input type="hidden" name="licence" id="f-licence">
      <input type="hidden" name="ref" id="f-ref">
      <input type="hidden" name="page" id="f-page">
      <input type="hidden" name="landing" id="f-landing">

      <div class="form-foot">
        <button class="btn accent" type="submit" id="f-submit">{esc(w["f_send"])}</button>
        <p class="status" id="f-status" role="status" aria-live="polite">{esc(w["f_status"])}</p>
      </div>
      <noscript><p class="hint" style="margin-top:1rem">{esc(w["f_noscript_a"])}<a href="mailto:{INBOX}">{INBOX}</a>{esc(w["f_noscript_b"])}</p></noscript>
    </form>

    <div data-line-panel style="margin-top:1.8rem"></div>

    <p class="hint" style="margin-top:1.4rem;max-width:62ch">{esc(w["sep"])}</p>
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
      <a href="{w["wl"][1]}">{esc(w["wl"][0])}</a>
      <a href="{w["other"][1]}" hreflang="{other_lang}">{esc(w["other"][0])}</a>
    </nav>
  </div>
</footer>
<script src="{assets}/app.js"></script>
</body>
</html>
"""


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
