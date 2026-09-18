(function () {
  "use strict";
  var C = window.DESK || {};
  var R = C.ref || {};
  var $ = function (s) { return document.querySelector(s); };
  var LANG = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);

  // Asset paths in config are written from the site root; pages sit at
  // different depths, so take the prefix from the stylesheet that already
  // loaded correctly on this page.
  function assetBase() {
    var link = document.querySelector('link[rel="stylesheet"]');
    var href = (link && link.getAttribute("href")) || "assets/style.css";
    return href.replace(/assets\/style\.css$/, "");
  }
  function asset(p) { return assetBase() + p; }

  var LABELS = {
    en: {
      lineAsk: "Ask on LINE", lineAdd: "Add us on LINE", lineId: "LINE",
      lineBlurb: "Add the desk on LINE and send your dates. It is the fastest way to a price.",
      shareTitle: "Share", share: "Share", copy: "Copy link", copied: "Copied",
      onLine: "LINE", onWhats: "WhatsApp", onFb: "Facebook", onTg: "Telegram",
      onX: "X", onMail: "Email", scan: "Or let them scan this",
      shareText: "Visas and border runs in Chiang Mai."
    },
    th: {
      lineAsk: "ถามทาง LINE", lineAdd: "เพิ่มเพื่อนใน LINE", lineId: "ไลน์",
      lineBlurb: "เพิ่มเราเป็นเพื่อนใน LINE แล้วส่งวันที่มา เป็นทางที่ได้ราคาเร็วที่สุด",
      shareTitle: "แชร์", share: "แชร์", copy: "คัดลอกลิงก์", copied: "คัดลอกแล้ว",
      onLine: "LINE", onWhats: "WhatsApp", onFb: "Facebook", onTg: "Telegram",
      onX: "X", onMail: "อีเมล", scan: "หรือให้เขาสแกนอันนี้",
      shareText: "บริการวีซ่าและวิ่งชายแดน เชียงใหม่"
    }
  };
  var T = LABELS[LANG] || LABELS.en;

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
  var ORIGIN = ({ us: C.originCodeUs, wl: C.originCodeWl }[LINE] || C.originCode) || "";

  var chip = $("#refchip"), code = $("#refcode");
  if (chip && code && REF) {
    code.textContent = REF;
    chip.classList.add("on");
  }
  var hidRef = $("#f-ref"); if (hidRef) hidRef.value = REF;
  var hidOrigin = $("#f-origin"); if (hidOrigin) hidOrigin.value = ORIGIN;
  var hidLine = $("#f-line"); if (hidLine) hidLine.value = LINE;
  var LICENCE = (C.licence && C.licence.id) || "";
  var hidLic = $("#f-licence"); if (hidLic) hidLic.value = LICENCE;
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

  var LINE = C.line || {};

  function shareText() { return T.shareText; }

  var TARGETS = [
    { key: "line",  label: function () { return T.onLine; },  cls: "line",
      href: function (u) { return "https://social-plugins.line.me/lineit/share?url=" + enc(u) + "&text=" + enc(shareText()); } },
    { key: "whats", label: function () { return T.onWhats; }, cls: "",
      href: function (u) { return "https://wa.me/?text=" + enc(shareText() + " " + u); } },
    { key: "fb",    label: function () { return T.onFb; },    cls: "",
      href: function (u) { return "https://www.facebook.com/sharer/sharer.php?u=" + enc(u); } },
    { key: "tg",    label: function () { return T.onTg; },    cls: "",
      href: function (u) { return "https://t.me/share/url?url=" + enc(u) + "&text=" + enc(shareText()); } },
    { key: "x",     label: function () { return T.onX; },     cls: "",
      href: function (u) { return "https://twitter.com/intent/tweet?url=" + enc(u) + "&text=" + enc(shareText()); } },
    { key: "mail",  label: function () { return T.onMail; },  cls: "",
      href: function (u) { return "mailto:?subject=" + enc(C.name || "") + "&body=" + enc(shareText() + "\n\n" + u); } }
  ];

  function enc(v) { return encodeURIComponent(v); }

  // Build the share sheet wherever the page left a .share container.
  document.querySelectorAll('[data-share="sheet"]').forEach(function (box) {
    if (box.dataset.built) return;
    box.dataset.built = "1";
    box.innerHTML = "";

    if (navigator.share) {
      box.appendChild(btn(T.share, "btn accent", function () {
        navigator.share({ title: C.name, text: shareText(), url: shareUrl() }).catch(function () {});
      }));
    }

    TARGETS.forEach(function (t) {
      var a = document.createElement("a");
      a.className = "btn ghost sbtn " + t.cls;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.href = t.href(shareUrl());
      a.appendChild(icon(t.key));
      a.appendChild(document.createTextNode(t.label()));
      box.appendChild(a);
    });

    var cb = btn(T.copy, "btn ghost", function () { copy(shareUrl(), cb, T.copy); });
    box.appendChild(cb);
  });

  function btn(text, cls, fn) {
    var b = document.createElement("button");
    b.type = "button"; b.className = cls; b.textContent = text;
    b.addEventListener("click", fn);
    return b;
  }

  function icon(key) {
    var paths = {
      line:  "M12 3C6.5 3 2 6.6 2 11c0 4 3.6 7.3 8.4 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.6 1.1-.5 6-3.5 8.2-6C21.5 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z",
      whats: "M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2z",
      fb:    "M14 8.5V7c0-.7.3-1 1-1h1.5V3.5H14c-2.2 0-3.5 1.3-3.5 3.4v1.6H8.5V11h2v9.5h3.5V11h2.2l.3-2.5H14z",
      tg:    "M21 4 2.8 11.2c-.8.3-.8 1.4 0 1.7l4.5 1.5 1.7 5.2c.2.7 1.1.9 1.6.3l2.4-2.6 4.6 3.4c.6.4 1.4.1 1.6-.6L22.5 5c.2-.8-.6-1.4-1.5-1z",
      x:     "M3 3h4.3l4.4 6 5.1-6H21l-7.2 8.3L21.6 21h-4.3l-4.8-6.5L6.8 21H3l7.6-8.8L3 3z",
      mail:  "M3 6h18v12H3z M3 6l9 6.5L21 6"
    };
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("class", "sico");
    svg.setAttribute("aria-hidden", "true");
    var pth = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pth.setAttribute("d", paths[key] || "");
    pth.setAttribute("fill", key === "mail" ? "none" : "currentColor");
    if (key === "mail") { pth.setAttribute("stroke", "currentColor"); pth.setAttribute("stroke-width", "1.7"); }
    svg.appendChild(pth);
    return svg;
  }

  // A QR of the link, for handing the phone across a counter.
  document.querySelectorAll("[data-share-qr]").forEach(function (el) {
    var img = document.createElement("img");
    img.src = asset("assets/site-qr.png");
    img.alt = "";
    img.width = 116; img.height = 116;
    var wrap = document.createElement("div");
    wrap.className = "qr";
    wrap.appendChild(img);
    var p = document.createElement("p");
    p.textContent = T.scan;
    wrap.appendChild(p);
    el.appendChild(wrap);
  });

  /* ---------------------------------------------------------------- credit */
  // One line, rendered into every footer, so a white-label copy carries it
  // without anyone remembering to paste it into eight files.
  (function () {
    var c = C.credit || {};
    if (!c.name) return;
    document.querySelectorAll("footer .wrap > div").forEach(function (box) {
      if (box.querySelector(".credit")) return;
      var p = document.createElement("p");
      p.className = "credit";
      var lic = C.licence && C.licence.holder
        ? document.createTextNode(C.licence.holder + " · ")
        : null;
      if (lic) p.appendChild(lic);
      p.appendChild(document.createTextNode((c.prefix || "Built by") + " "));
      var a = document.createElement("a");
      a.href = c.url || "#";
      a.textContent = c.name;
      a.rel = "noopener";
      p.appendChild(a);
      box.appendChild(p);
    });
  })();

  /* -------------------------------------------------------------- LINE + contact */
  function lineAddUrl() {
    // LINE wants the @ literal here, not percent-encoded.
    return LINE.id ? "https://line.me/R/ti/p/" + String(LINE.id).replace(/[^@A-Za-z0-9._-]/g, "") : "";
  }

  // A LINE button in the header of every page. Thailand answers on LINE; the
  // desk should be one tap away from wherever someone is reading.
  (function () {
    if (!LINE.id) return;
    var nav = document.querySelector(".top .nav");
    if (!nav || nav.querySelector(".linebtn")) return;
    var a = document.createElement("a");
    a.className = "btn line linebtn";
    a.href = lineAddUrl();
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.appendChild(icon("line"));
    var lbl = document.createElement("span");
    lbl.textContent = T.lineAsk;
    a.appendChild(lbl);
    var cta = nav.querySelector(".btn.accent");
    nav.insertBefore(a, cta || null);
  })();

  // A full LINE panel wherever a page asks for one.
  document.querySelectorAll("[data-line-panel]").forEach(function (el) {
    if (!LINE.id) { el.remove(); return; }
    var panel = document.createElement("div");
    panel.className = "linepanel";

    var left = document.createElement("div");
    var h = document.createElement("h3");
    h.appendChild(icon("line"));
    h.appendChild(document.createTextNode(" " + T.lineAdd));
    left.appendChild(h);
    var p = document.createElement("p");
    p.textContent = T.lineBlurb;
    left.appendChild(p);
    var a = document.createElement("a");
    a.className = "btn line";
    a.href = lineAddUrl();
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = (LINE.name || LINE.id);
    left.appendChild(a);
    panel.appendChild(left);

    if (LINE.qr) {
      var img = document.createElement("img");
      img.src = asset(LINE.qr);
      img.alt = "";
      img.width = 132; img.height = 132;
      img.className = "lineqr";
      panel.appendChild(img);
    }
    el.appendChild(panel);
  });

  var cl = $("#contactline");
  if (cl) {
    var bits = [];
    if (LINE.id) {
      bits.push('<a class="linelink" href="' + lineAddUrl() + '" target="_blank" rel="noopener noreferrer">'
                + T.lineId + " " + (LINE.name || LINE.id) + "</a>");
    }
    if (C.inbox) bits.push('<a href="mailto:' + C.inbox + '">' + C.inbox + "</a>");
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
      data.licence = LICENCE;
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
        "licence: " + (d.licence || "—"),
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
