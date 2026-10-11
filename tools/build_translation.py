#!/usr/bin/env python3
"""Render the translation service page in English, Thai and Burmese.

    python3 tools/build_translation.py

Writes site/translation/index.html, site/th/translation/index.html and
site/my/translation/index.html from the table below, so the three languages
carry the same papers, steps and questions.
"""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ORIGIN = "https://chiangmaivisadesk.com"
PATHS = {"en": "translation/", "th": "th/translation/", "my": "my/translation/"}

W = {
    "en": {
        "title": "Translation: Thai, English, Burmese — Chiang Mai Visa Desk",
        "desc": "Translation between Thai, English and Burmese for visa, work-permit and migrant-worker files in Chiang Mai: bank letters, certificates, house registration, contracts, pink card and CI papers, and an interpreter at Immigration and the employment office.",
        "skip": "Skip to the quote form",
        "nav": ["Thailand services", "Migrant workers", "Translation", "US visas", "Partners"],
        "quote": "Get a quote",
        "eyebrow": "Chiang Mai · Thai · English · Burmese",
        "h1": "Translation for visa and work-permit files.",
        "lede": "Thai, English and Burmese. The papers Chiang Mai Immigration and the employment office ask for, translated and stamped, and an interpreter at the counter.",
        "jump": "Papers",
        "papers_h": "Papers",
        "papers": [
            ("Retirement and marriage files", "Bank letters and statements, marriage and birth certificates, house registration."),
            ("Work permits", "Employment contracts, payslips, degree certificates and transcripts, company papers."),
            ("Migrant workers", "Pink card, Certificate of Identity (CI) and passport pages, and contracts in Thai and Burmese side by side."),
            ("Study and family", "School letters and transcripts, birth certificates, consent letters for children."),
            ("Police and medical", "Police clearance, medical certificates and hospital records."),
            ("US visa files", "The Thai papers a US file needs, in English."),
        ],
        "talk_h": "Interpreting",
        "talk": "At Chiang Mai Immigration, the Chiang Mai Provincial Employment Office, hospitals and police stations, in Thai, English and Burmese. By phone or video for an appointment anywhere else.",
        "stamp_h": "The stamp",
        "stamp": "A translated page carries the translator's name, the date and the desk's stamp. We don't notarize. Burmese comes back in Unicode Myanmar script; a Zawgyi copy is there on request.",
        "how_h": "How it works",
        "how": [
            ("The papers", "A photo or scan of each page, the languages, and the office the papers go to."),
            ("The price", "In writing, by the pages, the words or the hours."),
            ("Delivery", "A PDF on LINE or by email, and stamped paper copies in Chiang Mai."),
        ],
        "form_h": "Get a quote",
        "f_name": "Name", "f_name_ph": "Your name, or the business name",
        "f_contact": "Email, LINE or WhatsApp", "f_contact_ph": "Where we should reply",
        "f_who": "You are", "f_whos": ["Applying for myself", "An employer", "A worker", "Helping someone else"],
        "f_langs": "Languages", "f_langs_o": ["Thai → English", "English → Thai", "Burmese → Thai", "Thai → Burmese", "Burmese → English", "English → Burmese"],
        "f_need": "What it is", "f_needs": ["Bank letter or statement", "Birth, marriage or divorce certificate", "House registration", "Contract or payslips", "School papers", "Pink card, CI or passport", "Police or medical papers", "Interpreter at an office", "Something else"],
        "f_date": "Needed by", "f_date_hint": "An approximate date is fine.",
        "f_where": "Office", "f_where_ph": "For example: Chiang Mai Immigration",
        "f_notes": "Anything else", "f_notes_ph": "For example: how many pages, or the visa the papers are for.",
        "send": "Send it", "status": "This goes to the desk inbox.",
        "noscript": "Your browser is not running scripts. Email the same details to <a href=\"mailto:hello@chiangmaivisadesk.com\">hello@chiangmaivisadesk.com</a> and a price comes back.",
        "faq_h": "Questions",
        "faq": [
            ("Which languages?", "Thai, English and Burmese, in any direction between them."),
            ("Is a phone photo enough to price it?", "Yes, when every line can be read."),
            ("Do you notarize?", "No. A translated page carries the translator's name, the date and the desk's stamp."),
            ("What does it cost?", "Each job is priced in writing, by the pages, the words or the hours."),
        ],
        "foot_tag": "A Thai-registered company. Chiang Mai, Thailand.",
        "foot": ["Thailand services", "Migrant workers", "Translation", "US visas", "Free app", "Partners", "Licensing"],
        "locale": "en_US",
    },
    "th": {
        "title": "แปลเอกสาร ไทย อังกฤษ พม่า — Chiang Mai Visa Desk",
        "desc": "แปลเอกสารภาษาไทย อังกฤษ และพม่า สำหรับแฟ้มวีซ่า ใบอนุญาตทำงาน และแรงงานต่างด้าวในเชียงใหม่ หนังสือรับรองธนาคาร ทะเบียนสมรส สูติบัตร ทะเบียนบ้าน สัญญาจ้าง บัตรชมพู เอกสาร CI และล่ามที่ตรวจคนเข้าเมืองและสำนักงานจัดหางาน",
        "skip": "ข้ามไปที่แบบฟอร์มขอราคา",
        "nav": ["บริการในไทย", "แรงงานต่างด้าว", "แปลเอกสาร", "วีซ่าอเมริกา", "พันธมิตร"],
        "quote": "ขอใบเสนอราคา",
        "eyebrow": "เชียงใหม่ · ไทย · อังกฤษ · พม่า",
        "h1": "แปลเอกสารสำหรับแฟ้มวีซ่าและใบอนุญาตทำงาน",
        "lede": "ไทย อังกฤษ และพม่า เอกสารที่ตรวจคนเข้าเมืองเชียงใหม่และสำนักงานจัดหางานขอ แปลและประทับตรา และล่ามที่เคาน์เตอร์",
        "jump": "เอกสาร",
        "papers_h": "เอกสาร",
        "papers": [
            ("แฟ้มเกษียณและแต่งงาน", "หนังสือรับรองและรายการเดินบัญชีธนาคาร ทะเบียนสมรส สูติบัตร ทะเบียนบ้าน"),
            ("ใบอนุญาตทำงาน", "สัญญาจ้าง สลิปเงินเดือน ปริญญาบัตรและใบแสดงผลการเรียน เอกสารบริษัท"),
            ("แรงงานต่างด้าว", "บัตรชมพู เอกสาร CI และหน้าหนังสือเดินทาง สัญญาภาษาไทยและพม่าเทียบกันในหน้าเดียว"),
            ("การเรียนและครอบครัว", "หนังสือจากโรงเรียนและใบแสดงผลการเรียน สูติบัตร หนังสือยินยอมสำหรับเด็ก"),
            ("ตำรวจและการแพทย์", "หนังสือรับรองความประพฤติ ใบรับรองแพทย์ และประวัติการรักษา"),
            ("แฟ้มวีซ่าอเมริกา", "เอกสารไทยที่แฟ้มวีซ่าอเมริกาต้องใช้ แปลเป็นภาษาอังกฤษ"),
        ],
        "talk_h": "ล่าม",
        "talk": "ที่ตรวจคนเข้าเมืองเชียงใหม่ สำนักงานจัดหางานจังหวัดเชียงใหม่ โรงพยาบาล และสถานีตำรวจ ภาษาไทย อังกฤษ และพม่า นัดที่อื่นใช้โทรศัพท์หรือวิดีโอ",
        "stamp_h": "ตราประทับ",
        "stamp": "หน้าที่แปลแล้วมีชื่อผู้แปล วันที่ และตราของเดสก์ เราไม่รับรองโนตารี ภาษาพม่าส่งเป็นอักษรยูนิโค้ด ขอฉบับ Zawgyi ได้",
        "how_h": "ขั้นตอน",
        "how": [
            ("เอกสาร", "รูปถ่ายหรือสแกนทุกหน้า ภาษาที่ต้องการ และหน่วยงานที่จะยื่น"),
            ("ราคา", "เป็นลายลักษณ์อักษร ตามจำนวนหน้า คำ หรือชั่วโมง"),
            ("ส่งคืน", "PDF ทาง LINE หรืออีเมล และฉบับกระดาษประทับตราในเชียงใหม่"),
        ],
        "form_h": "ขอใบเสนอราคา",
        "f_name": "ชื่อ", "f_name_ph": "ชื่อของคุณ หรือชื่อกิจการ",
        "f_contact": "อีเมล ไลน์ หรือ WhatsApp", "f_contact_ph": "ช่องทางที่ให้เราตอบกลับ",
        "f_who": "คุณคือ", "f_whos": ["ยื่นเอง", "นายจ้าง", "แรงงาน", "ช่วยคนอื่น"],
        "f_langs": "ภาษา", "f_langs_o": ["ไทย → อังกฤษ", "อังกฤษ → ไทย", "พม่า → ไทย", "ไทย → พม่า", "พม่า → อังกฤษ", "อังกฤษ → พม่า"],
        "f_need": "เอกสารอะไร", "f_needs": ["หนังสือรับรองหรือรายการเดินบัญชีธนาคาร", "สูติบัตร ทะเบียนสมรส หรือทะเบียนหย่า", "ทะเบียนบ้าน", "สัญญาจ้างหรือสลิปเงินเดือน", "เอกสารโรงเรียน", "บัตรชมพู CI หรือหนังสือเดินทาง", "เอกสารตำรวจหรือแพทย์", "ล่ามที่หน่วยงาน", "เรื่องอื่น"],
        "f_date": "ต้องการภายใน", "f_date_hint": "วันที่โดยประมาณก็ได้",
        "f_where": "หน่วยงาน", "f_where_ph": "เช่น ตรวจคนเข้าเมืองเชียงใหม่",
        "f_notes": "อื่น ๆ", "f_notes_ph": "เช่น จำนวนหน้า หรือวีซ่าที่ใช้เอกสารนี้",
        "send": "ส่ง", "status": "ส่งเข้ากล่องจดหมายของเดสก์",
        "noscript": "เบราว์เซอร์ของคุณปิดสคริปต์อยู่ ส่งรายละเอียดเดียวกันมาที่ <a href=\"mailto:hello@chiangmaivisadesk.com\">hello@chiangmaivisadesk.com</a> แล้วราคาจะกลับไป",
        "faq_h": "คำถาม",
        "faq": [
            ("แปลภาษาอะไรบ้าง", "ไทย อังกฤษ และพม่า ทุกทิศทาง"),
            ("รูปจากโทรศัพท์พอสำหรับประเมินราคาไหม", "พอ ถ้าอ่านออกทุกบรรทัด"),
            ("รับรองโนตารีไหม", "ไม่ หน้าที่แปลแล้วมีชื่อผู้แปล วันที่ และตราของเดสก์"),
            ("ราคาเท่าไร", "ทุกงานมีใบเสนอราคาเป็นลายลักษณ์อักษร ตามจำนวนหน้า คำ หรือชั่วโมง"),
        ],
        "foot_tag": "บริษัทจดทะเบียนในประเทศไทย เชียงใหม่",
        "foot": ["บริการในไทย", "แรงงานต่างด้าว", "แปลเอกสาร", "วีซ่าอเมริกา", "แอปฟรี", "พันธมิตร", "สิทธิ์ใช้งาน"],
        "locale": "th_TH",
    },
    "my": {
        "title": "ဘာသာပြန် - ထိုင်း၊ အင်္ဂလိပ်၊ မြန်မာ — Chiang Mai Visa Desk",
        "desc": "ချင်းမိုင်ရှိ ဗီဇာ၊ အလုပ်ပါမစ်နှင့် ရွှေ့ပြောင်းအလုပ်သမား ဖိုင်များအတွက် ထိုင်း၊ အင်္ဂလိပ်နှင့် မြန်မာ ဘာသာပြန်။ ဘဏ်ထောက်ခံစာ၊ မွေးစာရင်း၊ လက်ထပ်စာချုပ်၊ အိမ်ထောင်စုစာရင်း၊ အလုပ်ခန့်စာချုပ်၊ ပန်းရောင်ကတ်နှင့် CI စာရွက်များ၊ လူဝင်မှုကြီးကြပ်ရေးရုံးနှင့် အလုပ်အကိုင်ရုံးတွင် စကားပြန်။",
        "skip": "စျေးနှုန်းပုံစံသို့",
        "nav": ["ထိုင်းဝန်ဆောင်မှု", "ရွှေ့ပြောင်းအလုပ်သမား", "ဘာသာပြန်", "အမေရိကန်ဗီဇာ", "မိတ်ဖက်"],
        "quote": "စျေးနှုန်း",
        "eyebrow": "ချင်းမိုင် · ထိုင်း · အင်္ဂလိပ် · မြန်မာ",
        "h1": "ဗီဇာနှင့် အလုပ်ပါမစ် ဖိုင်များအတွက် ဘာသာပြန်။",
        "lede": "ထိုင်း၊ အင်္ဂလိပ်နှင့် မြန်မာ။ ချင်းမိုင် လူဝင်မှုကြီးကြပ်ရေးရုံးနှင့် အလုပ်အကိုင်ရုံးက တောင်းသော စာရွက်များကို ဘာသာပြန်ပြီး တံဆိပ်တုံးပေးပါသည်။ ကောင်တာတွင် စကားပြန်လည်း ရှိပါသည်။",
        "jump": "စာရွက်စာတမ်း",
        "papers_h": "စာရွက်စာတမ်း",
        "papers": [
            ("အငြိမ်းစားနှင့် လက်ထပ် ဖိုင်", "ဘဏ်ထောက်ခံစာနှင့် ဘဏ်စာရင်းရှင်းတမ်း၊ လက်ထပ်စာချုပ်၊ မွေးစာရင်း၊ အိမ်ထောင်စုစာရင်း။"),
            ("အလုပ်ပါမစ်", "အလုပ်ခန့်စာချုပ်၊ လစာစလစ်၊ ဘွဲ့လက်မှတ်နှင့် အမှတ်စာရင်း၊ ကုမ္ပဏီစာရွက်များ။"),
            ("ရွှေ့ပြောင်းအလုပ်သမား", "ပန်းရောင်ကတ်၊ CI (Certificate of Identity) နှင့် နိုင်ငံကူးလက်မှတ် စာမျက်နှာများ၊ ထိုင်း-မြန်မာ ယှဉ်တွဲ စာချုပ်များ။"),
            ("ပညာရေးနှင့် မိသားစု", "ကျောင်းစာနှင့် အမှတ်စာရင်း၊ မွေးစာရင်း၊ ကလေးများအတွက် ခွင့်ပြုစာ။"),
            ("ရဲနှင့် ဆေး", "ပြစ်မှုကင်းရှင်းကြောင်း ထောက်ခံစာ၊ ဆေးထောက်ခံစာနှင့် ဆေးရုံမှတ်တမ်း။"),
            ("အမေရိကန်ဗီဇာ ဖိုင်", "အမေရိကန်ဖိုင်အတွက် လိုအပ်သော ထိုင်းစာရွက်များကို အင်္ဂလိပ်ဘာသာဖြင့်။"),
        ],
        "talk_h": "စကားပြန်",
        "talk": "ချင်းမိုင် လူဝင်မှုကြီးကြပ်ရေးရုံး၊ ချင်းမိုင် ခရိုင် အလုပ်အကိုင်ရုံး၊ ဆေးရုံများနှင့် ရဲစခန်းများတွင် ထိုင်း၊ အင်္ဂလိပ်နှင့် မြန်မာ ဘာသာဖြင့်။ အခြားနေရာရှိ ချိန်းဆိုမှုအတွက် ဖုန်း သို့မဟုတ် ဗီဒီယိုဖြင့်။",
        "stamp_h": "တံဆိပ်",
        "stamp": "ဘာသာပြန်ထားသော စာမျက်နှာတွင် ဘာသာပြန်သူ၏အမည်၊ ရက်စွဲနှင့် ဒက်စ်၏ တံဆိပ် ပါပါသည်။ ကျွန်ုပ်တို့ နိုတာရီ အတည်ပြုချက် မလုပ်ပါ။ မြန်မာစာကို ယူနီကုဒ်ဖြင့် ပြန်ပို့ပါသည်။ ဇော်ဂျီမူကို တောင်းနိုင်ပါသည်။",
        "how_h": "လုပ်ပုံ",
        "how": [
            ("စာရွက်များ", "စာမျက်နှာတိုင်း၏ ဓာတ်ပုံ သို့မဟုတ် စကင်ဖိုင်၊ ဘာသာစကားနှင့် တင်မည့်ရုံး။"),
            ("စျေးနှုန်း", "စာဖြင့်၊ စာမျက်နှာ၊ စာလုံး သို့မဟုတ် နာရီအလိုက်။"),
            ("ပြန်ပို့ခြင်း", "LINE သို့မဟုတ် အီးမေးလ်ဖြင့် PDF၊ ချင်းမိုင်တွင် တံဆိပ်တုံးထားသော စာရွက်မူ။"),
        ],
        "form_h": "စျေးနှုန်း",
        "f_name": "အမည်", "f_name_ph": "သင့်အမည် သို့မဟုတ် လုပ်ငန်းအမည်",
        "f_contact": "အီးမေးလ်၊ LINE သို့မဟုတ် WhatsApp", "f_contact_ph": "ပြန်ကြားရမည့်နေရာ",
        "f_who": "သင်သည်", "f_whos": ["ကိုယ်တိုင် လျှောက်သူ", "အလုပ်ရှင်", "အလုပ်သမား", "အခြားသူကို ကူညီသူ"],
        "f_langs": "ဘာသာစကား", "f_langs_o": ["မြန်မာ → ထိုင်း", "ထိုင်း → မြန်မာ", "မြန်မာ → အင်္ဂလိပ်", "အင်္ဂလိပ် → မြန်မာ", "ထိုင်း → အင်္ဂလိပ်", "အင်္ဂလိပ် → ထိုင်း"],
        "f_need": "ဘာစာရွက်လဲ", "f_needs": ["ဘဏ်ထောက်ခံစာ သို့မဟုတ် စာရင်းရှင်းတမ်း", "မွေးစာရင်း၊ လက်ထပ် သို့မဟုတ် ကွာရှင်း စာချုပ်", "အိမ်ထောင်စုစာရင်း", "အလုပ်ခန့်စာချုပ် သို့မဟုတ် လစာစလစ်", "ကျောင်းစာရွက်", "ပန်းရောင်ကတ်၊ CI သို့မဟုတ် နိုင်ငံကူးလက်မှတ်", "ရဲ သို့မဟုတ် ဆေး စာရွက်", "ရုံးတွင် စကားပြန်", "အခြား"],
        "f_date": "လိုအပ်သည့်ရက်", "f_date_hint": "ခန့်မှန်းရက်ဖြင့် ရပါသည်။",
        "f_where": "ရုံး", "f_where_ph": "ဥပမာ - ချင်းမိုင် လူဝင်မှုကြီးကြပ်ရေးရုံး",
        "f_notes": "အခြားအချက်များ", "f_notes_ph": "ဥပမာ - စာမျက်နှာ အရေအတွက်၊ သို့မဟုတ် စာရွက်များ သုံးမည့် ဗီဇာ။",
        "send": "ပို့မည်", "status": "ဒက်စ်၏ အီးမေးလ်သို့ ရောက်ပါမည်။",
        "noscript": "သင့်ဘရောက်ဆာတွင် script မဖွင့်ထားပါ။ အချက်အလက်များကို <a href=\"mailto:hello@chiangmaivisadesk.com\">hello@chiangmaivisadesk.com</a> သို့ အီးမေးလ်ပို့ပါက စျေးနှုန်း ပြန်ရပါမည်။",
        "faq_h": "မေးခွန်းများ",
        "faq": [
            ("ဘယ်ဘာသာတွေလဲ။", "ထိုင်း၊ အင်္ဂလိပ်နှင့် မြန်မာ၊ မည်သည့်ဘက်သို့မဆို။"),
            ("စျေးနှုန်းအတွက် ဖုန်းဓာတ်ပုံ လုံလောက်သလား။", "စာကြောင်းတိုင်း ဖတ်၍ရလျှင် လုံလောက်ပါသည်။"),
            ("နိုတာရီ လုပ်ပေးသလား။", "မလုပ်ပါ။ ဘာသာပြန်ထားသော စာမျက်နှာတွင် ဘာသာပြန်သူ၏အမည်၊ ရက်စွဲနှင့် ဒက်စ်၏ တံဆိပ် ပါပါသည်။"),
            ("ဘယ်လောက်ကျသလဲ။", "အလုပ်တိုင်းကို စာမျက်နှာ၊ စာလုံး သို့မဟုတ် နာရီအလိုက် စာဖြင့် စျေးနှုန်းပေးပါသည်။"),
        ],
        "foot_tag": "ထိုင်းနိုင်ငံတွင် မှတ်ပုံတင်ထားသော ကုမ္ပဏီ။ ချင်းမိုင်။",
        "foot": ["ထိုင်းဝန်ဆောင်မှု", "ရွှေ့ပြောင်းအလုပ်သမား", "ဘာသာပြန်", "အမေရိကန်ဗီဇာ", "အခမဲ့အက်ပ်", "မိတ်ဖက်", "လိုင်စင်"],
        "locale": "my_MM",
    },
}

LANG_LINKS = [("en", "English"), ("th", "ภาษาไทย"), ("my", "မြန်မာ")]


def e(s):
    return escape(s, quote=True)


def page(lang):
    t = W[lang]
    up = "../" if lang == "en" else "../../"
    home = up if lang == "en" else (up + "th/" if lang == "th" else up)
    # Section links: a Thai page links Thai sections; Burmese has only this page.
    sec = (lambda p: up + ("th/" if lang == "th" else "") + p)
    url = f"{ORIGIN}/{PATHS[lang]}"
    alts = "\n".join(f'<link rel="alternate" hreflang="{k}" href="{ORIGIN}/{v}">' for k, v in PATHS.items())
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{ORIGIN}/{PATHS["en"]}">'
    langs = "".join(f'\n      <a class="lang" href="{up}{PATHS[k]}" hreflang="{k}">{n}</a>' for k, n in LANG_LINKS if k != lang)
    n = t["nav"]
    nav = (f'<a href="{home}">{e(n[0])}</a>\n      <a href="{sec("migrant-workers/")}">{e(n[1])}</a>\n'
           f'      <a href="./" aria-current="page">{e(n[2])}</a>\n      <a href="{sec("us-visas/")}">{e(n[3])}</a>\n'
           f'      <a href="{sec("partners/")}">{e(n[4])}</a>')
    f = t["foot"]
    foot = (f'<a href="{home}">{e(f[0])}</a>\n      <a href="{sec("migrant-workers/")}">{e(f[1])}</a>\n'
            f'      <a href="./">{e(f[2])}</a>\n      <a href="{sec("us-visas/")}">{e(f[3])}</a>\n'
            f'      <a href="{sec("farang-buddy/")}">{e(f[4])}</a>\n      <a href="{sec("partners/")}">{e(f[5])}</a>\n'
            f'      <a href="{sec("white-label/")}">{e(f[6])}</a>'
            + "".join(f'\n      <a href="{up}{PATHS[k]}" hreflang="{k}">{nm}</a>' for k, nm in LANG_LINKS if k != lang)
            + '\n      <a href="https://motdang.net/cm/p/chiang-mai-visa-desk-cmcuratedchiangmaivisadesk.html">Mot Dang</a>')
    cards = "".join(f'\n      <article class="card rise">\n        <h3>{e(h)}</h3>\n        <p>{e(p)}</p>\n      </article>' for h, p in t["papers"])
    steps = "".join(f'\n      <div class="step rise">\n        <h3>{e(h)}</h3>\n        <p>{e(p)}</p>\n      </div>' for h, p in t["how"])
    opts = lambda xs: "".join(f"\n            <option>{e(x)}</option>" for x in xs)
    faq = "".join(f"\n      <details><summary>{e(q)}</summary>\n        <p>{e(a)}</p></details>" for q, a in t["faq"])
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#page", "url": url, "name": t["title"], "inLanguage": lang,
             "dateModified": "2026-10-11", "isPartOf": {"@id": ORIGIN + "/#site"}, "about": {"@id": url + "#service"}},
            {"@type": "Service", "@id": url + "#service", "name": t["h1"], "serviceType": "Translation and interpreting",
             "provider": {"@id": ORIGIN + "/#org"}, "availableLanguage": ["th", "en", "my"],
             "areaServed": [{"@type": "AdministrativeArea", "name": "Chiang Mai Province"},
                            {"@type": "AdministrativeArea", "name": "Northern Thailand"}]},
            {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        ],
    }
    return f"""<!doctype html>
<html lang="{lang}" translate="no" class="notranslate">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="canonical" href="{url}">
{alts}
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Chiang Mai Visa Desk">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ORIGIN}/assets/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F7F4EC" media="(prefers-color-scheme:light)">
<meta name="theme-color" content="#111319" media="(prefers-color-scheme:dark)">
<link rel="icon" href="{up}assets/mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}assets/style.css">
<script src="{up}assets/config.js"></script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<meta name="google" content="notranslate">
<meta name="robots" content="notranslate">
<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"+location.hostname.slice(0,-15).replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1").replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>
</head>
<body>
<a class="skip" href="#quote">{e(t["skip"])}</a>

<header class="top" id="top">
  <div class="wrap">
    <a class="mark" href="{home}"><svg class="stamp" viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="9" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="4.2 3.1"/><path d="M12 21.5l5.4 5.4L28.6 15" fill="none" stroke="#C79A3A" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Chiang Mai <strong>Visa Desk</strong></span></a>
    <nav class="nav">
      {nav}{langs}
      <a class="btn accent" href="#quote">{e(t["quote"])}</a>
    </nav>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span> {e(t["eyebrow"])}</p>
    <h1>{e(t["h1"])}</h1>
    <p class="lede">{e(t["lede"])}</p>
    <div class="cta-row"><a class="btn accent" href="#quote">{e(t["quote"])}</a>
      <a class="btn ghost" href="#papers">{e(t["jump"])}</a></div>
    <p class="chip" id="refchip">Referred by <code id="refcode"></code></p>
  </div>
</section>

<section class="alt" id="papers">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{e(t["papers_h"])}</h2>
    </div>
    <div class="grid">{cards}
    </div>
  </div>
</section>

<section id="interpreting">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{e(t["talk_h"])}</h2>
      <p>{e(t["talk"])}</p>
    </div>
  </div>
</section>

<section class="alt" id="stamp">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{e(t["stamp_h"])}</h2>
      <p>{e(t["stamp"])}</p>
    </div>
  </div>
</section>

<section id="how">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{e(t["how_h"])}</h2>
    </div>
    <div class="steps">{steps}
    </div>
  </div>
</section>

<section class="alt" id="quote">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{e(t["form_h"])}</h2>
    </div>

    <form class="panel" id="quoteform" novalidate>
      <div class="fields">
        <div class="field">
          <label for="f-name">{e(t["f_name"])}</label>
          <input id="f-name" name="name" autocomplete="name" required placeholder="{e(t["f_name_ph"])}">
        </div>
        <div class="field">
          <label for="f-contact">{e(t["f_contact"])}</label>
          <input id="f-contact" name="contact" autocomplete="email" required placeholder="{e(t["f_contact_ph"])}">
        </div>
        <div class="field">
          <label for="f-who">{e(t["f_who"])}</label>
          <select id="f-who" name="who">{opts(t["f_whos"])}
          </select>
        </div>
        <div class="field">
          <label for="f-visa">{e(t["f_langs"])}</label>
          <select id="f-visa" name="visa">{opts(t["f_langs_o"])}
          </select>
        </div>
        <div class="field">
          <label for="f-need">{e(t["f_need"])}</label>
          <select id="f-need" name="need">{opts(t["f_needs"])}
          </select>
        </div>
        <div class="field">
          <label for="f-date">{e(t["f_date"])}</label>
          <input id="f-date" name="date" type="date">
          <span class="hint">{e(t["f_date_hint"])}</span>
        </div>
        <div class="field">
          <label for="f-where">{e(t["f_where"])}</label>
          <input id="f-where" name="where" placeholder="{e(t["f_where_ph"])}">
        </div>
        <div class="field wide">
          <label for="f-notes">{e(t["f_notes"])}</label>
          <textarea id="f-notes" name="notes" placeholder="{e(t["f_notes_ph"])}"></textarea>
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
        <button class="btn accent" type="submit" id="f-submit">{e(t["send"])}</button>
        <p class="status" id="f-status" role="status" aria-live="polite">{e(t["status"])}</p>
      </div>
      <noscript><p class="hint" style="margin-top:1rem">{t["noscript"]}</p></noscript>
    </form>
    <div data-line-panel style="margin-top:1.6rem"></div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <div class="section-head rise">
      <h2>{e(t["faq_h"])}</h2>
    </div>
    <div class="faq">{faq}
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div>
      <p><strong>Chiang Mai Visa Desk</strong></p>
      <p style="margin-top:.35rem">{e(t["foot_tag"])}</p>
      <p style="margin-top:.35rem" id="contactline"></p>
    </div>
    <nav>
      {foot}
    </nav>
  </div>
</footer>
<script src="{up}assets/app.js"></script>
</body>
</html>
"""


def main():
    for lang, rel in PATHS.items():
        out = SITE / rel / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang))
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
