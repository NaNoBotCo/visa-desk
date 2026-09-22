#!/usr/bin/env python3
"""Social copy — the profile text for the desk's own accounts, with the counts.

Every field each platform asks for, in English and Thai, written to fit the
field. The lengths printed beside each block are counted here, not guessed, so
an edit that overruns a limit shows up the moment this runs.

    python3 tools/social_copy.py            write notes/social-profiles.txt
    python3 tools/social_copy.py --check    counts only; non-zero if one overruns
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "notes" / "social-profiles.txt"

DOMAIN = "chiangmaivisadesk.com"
SITE = f"https://{DOMAIN}/"
INBOX = "hello@chiangmaivisadesk.com"
HANDLE = "chiangmaivisadesk"

# (platform, field, limit or None, text)
BLOCKS = [
    ("LINE OA", "display name", 20, "Chiang Mai Visa Desk"),
    ("LINE OA", "status message — EN", 20, "Your visa, handled."),
    ("LINE OA", "status message — TH", 20, "วีซ่า เราจัดการให้"),
    ("LINE OA", "greeting message — TH then EN", 500,
     "สวัสดีค่ะ ที่นี่ Chiang Mai Visa Desk\n"
     "ใบอนุญาตทำงาน จดทะเบียนบริษัทไทย ต่อวีซ่าเกษียณ รายงานตัว 90 วัน แจ้งที่พัก ตม.30 "
     "และวิ่งชายแดน\n"
     "เล่าสถานการณ์ของคุณมาในแชทนี้ แล้วเราจะส่งใบเสนอราคาที่ระบุขั้นตอน เอกสาร และราคาให้\n\n"
     "Chiang Mai Visa Desk — work permits, Thai company registration, retirement "
     "extensions, 90-day reporting, TM30 and border runs.\n"
     "Tell us your situation in this chat and we send back a quote that names the "
     "steps, the papers and the price.\n"
     f"{SITE}"),
    ("LINE OA", "description / about", 500,
     "Visa and immigration paperwork for long-stay residents of Chiang Mai and "
     "northern Thailand: work permits and the Non-B that carries them, Thai company "
     "registration with tax ID and VAT, retirement extensions, 90-day reports, TM30, "
     "re-entry permits and escorted border runs. Quotes by chat or email. "
     f"English-first, Thai spoken. {SITE}"),

    ("Facebook Page", "page name", 75, "Chiang Mai Visa Desk"),
    ("Facebook Page", "username", 50, HANDLE),
    ("Facebook Page", "short description", 255,
     "Work permits, Thai company registration, retirement extensions, 90-day "
     "reporting, TM30 and escorted border runs from Chiang Mai. Tell us your "
     "situation; we quote the job, prepare the papers and file them."),
    ("Facebook Page", "about / long", 1000,
     "Chiang Mai Visa Desk prepares and files the paperwork that keeps long-stay "
     "residents of northern Thailand in status.\n\n"
     "· Work permits — the Non-B, the permit, the tax ID and social security "
     "registration prepared as one file. New permits, renewals and a change of "
     "employer.\n"
     "· Thai company registration — registration, shareholder and director paperwork, "
     "tax ID and VAT, the corporate bank account, and the work permit the company "
     "then issues.\n"
     "· Retirement — Non-O and Non-OA, the annual extension, bank letters and account "
     "paperwork, insurance documents, and the 90-day reports that follow.\n"
     "· Border runs — door pickup in Chiang Mai, papers prepared in advance, staff at "
     "both counters, return the same trip.\n"
     "· Extensions, 90-day reporting, TM30 address notification, re-entry permits.\n\n"
     "There is a second book of work: Thai nationals applying for US visas — B1/B2, "
     "F-1, K-1 and the document file each one needs.\n\n"
     f"Quotes by message or email: {INBOX}\n{SITE}"),

    ("Instagram", "name field", 30, "Chiang Mai Visa Desk"),
    ("Instagram", "bio — EN", 150,
     "Work permits · Thai company setup · Retirement extensions · 90-day · TM30 · "
     "Border runs\nChiang Mai. Message for a quote."),
    ("Instagram", "bio — TH", 150,
     "ใบอนุญาตทำงาน · จดทะเบียนบริษัท · ต่อวีซ่าเกษียณ · รายงานตัว 90 วัน · วิ่งชายแดน\n"
     "เชียงใหม่ · ทักมาขอใบเสนอราคาได้"),

    ("TikTok", "name", 30, "Chiang Mai Visa Desk"),
    ("TikTok", "bio — TH (for the US-visa book)", 80,
     "วีซ่าอเมริกาสำหรับคนไทย B1/B2 F-1 K-1\nเตรียมเอกสารครบ · เชียงใหม่"),
    ("TikTok", "bio — EN (for the Thailand book)", 80,
     "Work permits · company setup · retirement visas · border runs · Chiang Mai"),

    ("YouTube", "channel name", 50, "Chiang Mai Visa Desk"),
    ("YouTube", "handle", 30, f"@{HANDLE}"),
    ("YouTube", "channel description", 1000,
     "How Thai visa and immigration paperwork actually works, filmed in Chiang Mai.\n\n"
     "Work permits and the Non-B. Thai company registration with tax ID and VAT. "
     "Retirement extensions, Non-O and Non-OA. 90-day reporting, TM30 address "
     "notification, re-entry permits, and escorted border runs.\n\n"
     "A second series covers Thai nationals applying for US visas — B1/B2, F-1 and "
     "K-1, and the document file each one needs.\n\n"
     "Each video says which office, which form, and what the counter asks for. "
     "Rules and fees change; every video carries the date it was filmed.\n\n"
     f"{SITE}\n{INBOX}"),
]

UPLOADS = [
    ("LINE OA", "profile image", "brand/social/avatar-640-line.png"),
    ("LINE OA", "cover image", "brand/social/cover-line-1080x878.png"),
    ("Facebook Page", "profile picture", "brand/social/avatar-320-facebook-instagram.png"),
    ("Facebook Page", "cover photo", "brand/social/cover-facebook-1640x630.png"),
    ("Facebook Page", "first post", "brand/social/post-square-1080.png"),
    ("Instagram", "profile picture", "brand/social/avatar-320-facebook-instagram.png"),
    ("Instagram", "first post", "brand/social/post-square-1080.png"),
    ("TikTok", "profile picture", "brand/social/avatar-200-tiktok.png"),
    ("TikTok", "video cover / first post", "brand/social/post-vertical-1080x1920.png"),
    ("YouTube", "channel picture", "brand/social/avatar-800-youtube.png"),
    ("YouTube", "banner", "brand/social/banner-youtube-2560x1440.png"),
]

SETUP = """\
ORDER OF WORK

1  LINE OA          manager.line.biz  ->  Create an account.  Sign in with a LINE
                    Business ID made from {inbox}, not with the personal
                    account that already runs @964yxgnk.  The basic id it issues is
                    random (@xxx1234); a chosen id is a paid yearly extra.
                    Then: Settings -> Messaging API -> Enable, and copy the channel
                    access token and the channel secret.
2  Facebook Page    business.facebook.com  ->  new business portfolio  ->  create the
                    Page.  Category: Consulting Agency, second category Legal Service.
                    Do not add a street address; set it as a business without a
                    storefront.  Page roles: you, plus Beer.
3  Instagram        Sign up fresh, switch to a Professional account (Business), then
                    link it to the Page from the Page's Linked Accounts.  The API can
                    only publish to an IG account linked this way.
4  TikTok           Sign up with {inbox}, then Settings -> Account -> Switch to
                    Business Account.  Category: Professional Services.
5  YouTube          A new Google account for the desk, then create the channel and
                    claim the handle.

WHAT COMES BACK TO ME

  LINE channel access token + channel secret
  Facebook Page id, and a system-user token from the business portfolio
  Instagram business account id
  TikTok: nothing yet - the posting API needs an app audit first
  YouTube: the channel id, and an OAuth client for the desk's Google account

  Tokens go into ~/.config/nanobotco/keys.json under a visa_desk block.

WHAT EACH SIGN-UP WILL ASK FOR THAT ONLY YOU HAVE

  A phone number for TikTok and for the new Google account.
  An email: {inbox} reaches you at 530kings@proton.me already.
""".format(inbox=INBOX)


def counted():
    rows = []
    for platform, field, limit, text in BLOCKS:
        n = len(text)
        over = limit is not None and n > limit
        rows.append((platform, field, limit, n, over, text))
    return rows


def write():
    rows = counted()
    out = []
    out.append("CHIANG MAI VISA DESK — PROFILE TEXT AND ARTWORK")
    out.append("Generated by tools/social_copy.py. Each block is the whole field: paste it as it is.\nCharacter counts are measured here; the limits are what the copy was written to fit,\nand each form shows its own.")
    out.append("")
    current = None
    for platform, field, limit, n, over, text in rows:
        if platform != current:
            out.append("")
            out.append("=" * 72)
            out.append(platform.upper())
            out.append("=" * 72)
            current = platform
        cap = f"limit {limit}" if limit else "no stated limit"
        flag = "  ** OVER **" if over else ""
        out.append("")
        out.append(f"--- {field}   [{n} characters, {cap}]{flag}")
        out.append("")
        out.append(text)
        out.append("")
    out.append("")
    out.append("=" * 72)
    out.append("ARTWORK — WHICH FILE GOES WHERE")
    out.append("=" * 72)
    out.append("")
    for platform, slot, path in UPLOADS:
        out.append(f"{platform:16} {slot:26} {path}")
    out.append("")
    out.append("Redraw any of them with: python3 tools/social_kit.py")
    out.append("")
    out.append("=" * 72)
    out.append(SETUP)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="print the counts, write nothing")
    args = ap.parse_args(argv)
    rows = counted() if args.check else write()
    bad = 0
    for platform, field, limit, n, over, _ in rows:
        mark = "OVER" if over else "ok"
        bad += 1 if over else 0
        print(f"{mark:4} {platform:15} {field:34} {n:>5} / {limit if limit else '-'}")
    if not args.check:
        print(f"\n{OUT}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
