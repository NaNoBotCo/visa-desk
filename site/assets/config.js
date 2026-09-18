/* Everything you might want to change lives here. */
window.DESK = {
  // Wordmark and domain. Change in one place; the whole site follows.
  name: "Chiang Mai Visa Desk",
  short: "Visa Desk",
  domain: "chiangmaivisadesk.com",
  origin: "https://chiangmaivisadesk.com",

  // Where the quote form posts. Leave empty and the form falls back to a
  // pre-filled email, so the page still works with nothing behind it.
  endpoint: "https://visa-desk-intake.nanobotco.workers.dev/quote",

  // Reply-to inbox used by the email fallback.
  inbox: "hello@chiangmaivisadesk.com",

  // LINE is how Thailand actually talks. The basic id opens an add-friend
  // screen; leave it empty and every LINE affordance on the site disappears
  // rather than half-working.
  line: {
    id: "@964yxgnk",                  // the Official Account's basic id
    name: "",                         // shown instead of the id when set
    qr: "assets/line-qr.png"          // redrawn by tools/brand.py
  },

  // Other handles shown on the contact row. Empty ones are hidden.
  whatsapp: "",
  telegram: "",

  // TWO BOOKS OF BUSINESS, ONE WEBSITE.
  //
  //   "th"  Thailand-side work — border runs, extensions, reporting. Shared
  //         with the partner agency; enquiries go to the whole desk.
  //   "us"  Thai nationals applying for US visas. A separate book. Enquiries
  //         go to its own recipients and are counted on their own line.
  //   "wl"  Someone wanting a licensed copy of this site for their own city.
  //
  // Each book has its own origin code, stamped on every enquiry that comes
  // through this site. The Worker sets it again server-side and ignores
  // whatever the page sends, so a visitor cannot strip it out of the URL.
  originCode: "CMVD",       // th — the shared desk
  originCodeUs: "USOUT",    // us — the US-outbound book
  originCodeWl: "WLABEL",   // wl — licensing this site to another city

  // WHO BUILT IT. Rendered into the footer of every page. A white-label
  // deployment keeps this line and changes the one below it.
  credit: {
    name: "hongdam.net",
    url: "https://hongdam.net",
    prefix: "Built by"
  },

  // LICENCE — filled in for a white-label deployment, blank for the original.
  // The id rides on every enquiry that deployment sends, which is how a
  // licensed site is counted and billed. Mint one with tools/licence.py.
  licence: {
    id: "",                    // e.g. "WL-UBON-01"
    holder: "",                // the business running this copy
    place: ""                  // the city or province it covers
  },

  // PARTNER CODE — optional, and it sits beside the origin rather than
  // replacing it. Empty when nobody referred the visitor.
  ref: {
    param: "ref",              // ?ref=CODE
    days: 90,                  // how long a partner code sticks to a visitor
    storageKey: "cmvd.ref"
  }
};
