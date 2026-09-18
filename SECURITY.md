# Security

## Reporting

Open a private security advisory through GitHub's *Report a vulnerability*
button on this repository's Security tab.

## What the template stores

The site keeps the referral code in `localStorage` for 90 days. Everything a
page loads — stylesheet, script, fonts, images — comes from the site's own
origin. Cookies are not part of how the pages work.

The Worker in `worker/` writes each enquiry to D1 — the contact details the
visitor typed, the referral code, and the country Cloudflare reports for the
request. Set `SITE_ORIGIN` so the CORS header names your domain rather than `*`.

## Things a clone should not commit

- `partners-private/` — real partner names and codes. Already gitignored.
- `.names-not-on-the-site` — the guard list for unsigned sites. Committing it
  publishes the names it exists to keep off the pages. Already gitignored.
- Any Worker secret. Use `wrangler secret put`, never `vars` in `wrangler.jsonc`.
