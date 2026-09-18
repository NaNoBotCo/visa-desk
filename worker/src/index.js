/**
 * Quote + partner intake for the site.
 *
 * POST /quote   { name, contact, visa, need, date, where, notes, ref, idempotencyKey }
 * GET  /health
 *
 * Writes the enquiry to D1 with its referral token, then emails everyone on
 * the desk. The token is what the commission is calculated from, so it is
 * stored even when the email step fails.
 *
 * Recipients come from the DESK_RECIPIENTS secret — a comma-separated list —
 * so the addresses are not in this repository:
 *
 *     wrangler secret put DESK_RECIPIENTS
 *
 * ATTRIBUTION HAS TWO LAYERS.
 *   origin  — set here from ORIGIN_CODE, never from the request body. Every
 *             enquiry that comes through this site carries it, so the desk's
 *             commission does not depend on a URL parameter surviving.
 *   ref     — an optional partner code carried in from ?ref=. It sits beside
 *             the origin and is paid out of the desk's share, not instead of it.
 */

const CORS = (origin) => ({
  "Access-Control-Allow-Origin": origin,
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Idempotency-Key",
  "Access-Control-Max-Age": "86400"
});

// Fields the page is allowed to set. "origin" is deliberately not among them:
// it is stamped here, from the Worker's own config, so an enquiry that came
// through this site carries the desk's attribution whatever the URL said.
const FIELDS = ["name", "contact", "visa", "need", "date", "where", "notes", "ref", "page", "landing"];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = env.SITE_ORIGIN || "*";

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS(origin) });
    if (url.pathname === "/health") return json({ ok: true }, 200, origin);
    if (url.pathname !== "/quote" || request.method !== "POST") return json({ error: "not found" }, 404, origin);

    let body;
    try { body = await request.json(); } catch (e) { return json({ error: "bad json" }, 400, origin); }

    if (body.company) return json({ ok: true }, 202, origin);          // bait field filled: drop quietly
    const name = str(body.name), contact = str(body.contact);
    if (!name || !contact) return json({ error: "name and contact required" }, 422, origin);

    const key = str(body.idempotencyKey) || request.headers.get("Idempotency-Key") || crypto.randomUUID();
    const row = {};
    for (const f of FIELDS) row[f] = str(body[f]);
    row.ref = row.ref.slice(0, 40);                       // partner code, may be empty
    row.origin = (env.ORIGIN_CODE || "DESK").slice(0, 40); // ours, always, not the page's

    const seen = await env.DB.prepare("SELECT id FROM enquiries WHERE idem = ?").bind(key).first();
    if (seen) return json({ ok: true, id: seen.id, duplicate: true }, 200, origin);

    const res = await env.DB.prepare(
      `INSERT INTO enquiries (idem, name, contact, visa, need, travel_date, area, notes,
                              origin, ref, page, landing, referer, received_at, ip_country)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    ).bind(
      key, row.name, row.contact, row.visa, row.need, row.date, row.where, row.notes,
      row.origin, row.ref, row.page, row.landing,
      str(request.headers.get("referer")).slice(0, 500),
      new Date().toISOString(), request.headers.get("cf-ipcountry") || ""
    ).run();

    const id = res.meta.last_row_id;

    const to = recipients(env);
    if (env.RESEND_KEY && to.length) {
      try {
        await fetch("https://api.resend.com/emails", {
          method: "POST",
          headers: { Authorization: `Bearer ${env.RESEND_KEY}`, "Content-Type": "application/json" },
          body: JSON.stringify({
            from: env.MAIL_FROM || "desk@chiangmaivisadesk.com",
            to,
            reply_to: contact.includes("@") ? contact : undefined,
            subject: `#${id} ${row.need || "enquiry"} — ${row.name} [${row.origin}${row.ref ? "/" + row.ref : ""}]`,
            text:
              `origin: ${row.origin}   (commission: the desk)\n` +
              `ref:    ${row.ref || "—"}${row.ref ? "   (partner share out of the desk's)" : ""}\n\n` +
              FIELDS.map((f) => `${f}: ${row[f]}`).join("\n") +
              `\n\nid: ${id}\nidem: ${key}`
          })
        });
      } catch (e) { /* the row is already saved; the desk can read the table */ }
    }

    return json({ ok: true, id }, 200, origin);
  }
};

function recipients(env) {
  return String(env.DESK_RECIPIENTS || env.DESK_INBOX || "")
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.includes("@"));
}

function str(v) { return typeof v === "string" ? v.trim().slice(0, 2000) : ""; }
function json(o, status, origin) {
  return new Response(JSON.stringify(o), {
    status, headers: { "Content-Type": "application/json", ...CORS(origin) }
  });
}
