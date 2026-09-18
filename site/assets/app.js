(function () {
  "use strict";
  var C = window.DESK || {};
  var R = C.ref || {};
  var $ = function (s) { return document.querySelector(s); };

  /* ---------------------------------------------------------- referral code */
  function readStored() {
    try {
      var raw = localStorage.getItem(R.storageKey);
      if (!raw) return null;
      var o = JSON.parse(raw);
      if (!o || !o.v || (o.exp && Date.now() > o.exp)) return null;
      return o.v;
    } catch (e) { return null; }
  }
  function store(v) {
    try {
      localStorage.setItem(R.storageKey, JSON.stringify({
        v: v, exp: Date.now() + (R.days || 90) * 864e5
      }));
    } catch (e) {}
  }
  function clean(v) { return String(v || "").trim().slice(0, 40).replace(/[^A-Za-z0-9._-]/g, ""); }

  var fromUrl = clean(new URLSearchParams(location.search).get(R.param || "ref"));
  if (fromUrl) store(fromUrl);
  var REF = fromUrl || readStored() || "";        // partner code, may be empty

  // Which book of business this page's form belongs to. A form marked
  // data-line="us" is the US-outbound book and is stamped, routed and counted
  // separately from the shared Thailand-side desk.
  var formEl = document.getElementById("quoteform");
  var LINE = (formEl && formEl.getAttribute("data-line")) || "th";
  var ORIGIN = (LINE === "us" ? C.originCodeUs : C.originCode) || "";

  var chip = $("#refchip"), code = $("#refcode");
  if (chip && code && REF) {
    code.textContent = REF;
    chip.classList.add("on");
  }
  var hidRef = $("#f-ref"); if (hidRef) hidRef.value = REF;
  var hidOrigin = $("#f-origin"); if (hidOrigin) hidOrigin.value = ORIGIN;
  var hidLine = $("#f-line"); if (hidLine) hidLine.value = LINE;
  var hidPage = $("#f-page"); if (hidPage) hidPage.value = location.pathname;
  var hidLanding = $("#f-landing"); if (hidLanding) hidLanding.value = location.href.slice(0, 500);

  /* ------------------------------------------------------------- share link */
  function shareUrl() {
    var u = new URL(C.origin || location.origin);
    u.pathname = "/";
    if (REF) u.searchParams.set(R.param || "ref", REF);
    return u.toString();
  }
  var box = $("#sharelink"); if (box) box.textContent = shareUrl();

  var sb = $("#sharebtn");
  if (sb) sb.addEventListener("click", function () {
    var d = { title: C.name, text: "Visa paperwork and border runs in Chiang Mai.", url: shareUrl() };
    if (navigator.share) { navigator.share(d).catch(function () {}); }
    else { copy(shareUrl(), sb, "Share this page"); }
  });
  var cb = $("#copybtn");
  if (cb) cb.addEventListener("click", function () { copy(shareUrl(), cb, "Copy link"); });

  function copy(text, btn, label) {
    var done = function () { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = label; }, 1800); };
    if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, fallback); } else { fallback(); }
    function fallback() {
      var t = document.createElement("textarea");
      t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); done(); } catch (e) {}
      document.body.removeChild(t);
    }
  }

  /* ------------------------------------------------------------ contact row */
  var cl = $("#contactline");
  if (cl) {
    var bits = [];
    if (C.inbox) bits.push('<a href="mailto:' + C.inbox + '">' + C.inbox + "</a>");
    if (C.line) bits.push("LINE " + C.line);
    if (C.whatsapp) bits.push("WhatsApp " + C.whatsapp);
    if (C.telegram) bits.push("Telegram " + C.telegram);
    cl.innerHTML = bits.join(" · ");
  }

  /* ------------------------------------------------------------------- form */
  var form = $("#quoteform");
  if (form) {
    var status = $("#f-status"), submit = $("#f-submit");
    var idem = "q_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 8);
    var sending = false;

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (sending) return;

      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      if (data.company) return;                       // bait field
      delete data.company;

      if (!data.name || !data.contact) {
        say("Name and one way to reach you, then it can go.", "err");
        (data.name ? $("#f-contact") : $("#f-name")).focus();
        return;
      }

      data.ref = REF;
      data.origin = ORIGIN;
      data.line = LINE;
      data.landing = location.href.slice(0, 500);
      data.idempotencyKey = idem;
      data.submittedAt = new Date().toISOString();

      if (!C.endpoint) { mailto(data); return; }

      sending = true;
      submit.textContent = "Sending…";
      say("Sending.");
      post(C.endpoint, data, 2)
        .then(function () {
          form.reset();
          submit.textContent = "Sent";
          say("In. A price comes back to " + data.contact + ".", "ok");
        })
        .catch(function () {
          sending = false;
          submit.textContent = "Send it";
          say("That did not go through. Opening an email with the same details.", "err");
          mailto(data);
        });
    });

    function post(url, body, tries) {
      return fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Idempotency-Key": body.idempotencyKey },
        body: JSON.stringify(body)
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r;
      }).catch(function (e) {
        if (tries > 0) return new Promise(function (res) { setTimeout(res, 1200); }).then(function () { return post(url, body, tries - 1); });
        throw e;
      });
    }

    function mailto(d) {
      var lines = [
        "Name: " + (d.name || ""),
        "Contact: " + (d.contact || ""),
        "Visa: " + (d.visa || "not sure"),
        "Needs: " + (d.need || ""),
        "Date: " + (d.date || ""),
        "Where: " + (d.where || ""),
        "",
        (d.notes || ""),
        "",
        "line: " + (d.line || "th"),
        "origin: " + (d.origin || ""),
        "ref: " + (d.ref || "—")
      ].join("\n");
      var href = "mailto:" + (C.inbox || "") +
        "?subject=" + encodeURIComponent("Quote — " + (d.need || "enquiry")) +
        "&body=" + encodeURIComponent(lines);
      say("Opening your email with everything filled in.", "ok");
      location.href = href;
    }

    function say(msg, kind) {
      status.textContent = msg;
      status.className = "status" + (kind ? " " + kind : "");
    }
  }

  /* -------------------------------------------------------------- chrome fx */
  var top = $("#top");
  if (top) {
    var onScroll = function () { top.classList.toggle("stuck", window.scrollY > 8); };
    addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  if (window.IntersectionObserver && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".rise").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".rise").forEach(function (el) { el.classList.add("in"); });
  }
})();
