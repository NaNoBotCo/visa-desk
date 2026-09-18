/* Everything you might want to change lives here. */
window.DESK = {
  // Wordmark and domain. Change in one place; the whole site follows.
  name: "Chiang Mai Visa Desk",
  short: "Visa Desk",
  domain: "chiangmaivisadesk.com",
  origin: "https://chiangmaivisadesk.com",

  // Where the quote form posts. Leave empty and the form falls back to a
  // pre-filled email, so the page still works with nothing behind it.
  endpoint: "",

  // Reply-to inbox used by the email fallback.
  inbox: "hello@chiangmaivisadesk.com",

  // Messaging handles shown on the contact row. Empty ones are hidden.
  line: "",
  whatsapp: "",
  telegram: "",

  // TWO BOOKS OF BUSINESS, ONE WEBSITE.
  //
  //   "th"  Thailand-side work — border runs, extensions, reporting. Shared
  //         with the partner agency; enquiries go to the whole desk.
  //   "us"  Thai nationals applying for US visas. A separate book. Enquiries
  //         go to its own recipients and are counted on their own line.
  //
  // Each book has its own origin code, stamped on every enquiry that comes
  // through this site. The Worker sets it again server-side and ignores
  // whatever the page sends, so a visitor cannot strip it out of the URL.
  originCode: "CMVD",       // th — the shared desk
  originCodeUs: "USOUT",    // us — the US-outbound book

  // PARTNER CODE — optional, and it sits beside the origin rather than
  // replacing it. Empty when nobody referred the visitor.
  ref: {
    param: "ref",              // ?ref=CODE
    days: 90,                  // how long a partner code sticks to a visitor
    storageKey: "cmvd.ref"
  }
};
