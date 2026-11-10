/* =========================================================
   Renie Namocot — Portfolio scripts
   All content is pre-rendered by build.py; this file only
   adds interactivity (nav, filters, modal, reveal, forms).
   ========================================================= */
(function () {
  "use strict";

  const ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg>';
  const NAMES = { nextdotjs: "Next.js", nodedotjs: "Node.js", woocommerce: "WooCommerce", wordpress: "WordPress", php: "PHP",
    javascript: "JavaScript", html5: "HTML5", bigcommerce: "BigCommerce", squarespace: "Squarespace", divi: "Divi", acf: "ACF Pro" };
  const brandName = (s) => NAMES[s] || s.charAt(0).toUpperCase() + s.slice(1);
  const LM = { divi: ["D", "#7A2EE6"], acf: ["A", "#007A65"] };
  const icon = (s) => LM[s]
    ? `<span class="lm-sm" style="background:${LM[s][1]}">${LM[s][0]}</span>`
    : `<img src="/assets/img/icons/${s}.svg" alt="" width="16" height="16" data-slug="${s}">`;
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ---------- Icon fallback ---------- */
  document.addEventListener("error", (e) => {
    const img = e.target;
    if (img.tagName !== "IMG") return;
    if (img.dataset.slug) {
      const span = document.createElement("span");
      span.className = "lm-sm";
      span.style.background = "#0B0B0C";
      span.textContent = brandName(img.dataset.slug).slice(0, 1);
      img.replaceWith(span);
    } else {
      img.classList.add("broken");
    }
  }, true);

  /* ---------- Nav ---------- */
  const nav = document.querySelector(".nav");
  const onScroll = () => nav && nav.classList.toggle("scrolled", window.scrollY > 10);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  // mobile full-screen menu
  const menuBtn = document.querySelector(".menu-btn");
  const setMenu = (open) => {
    nav.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
    menuBtn.setAttribute("aria-expanded", open);
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };
  if (menuBtn) {
    menuBtn.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
    document.querySelectorAll(".m-menu a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  }

  // services mega-menu: hover on desktop, click/keyboard everywhere
  const dd = document.querySelector(".nav-dd");
  const ddBtn = dd && dd.querySelector(".nav-dd-btn");
  const mega = document.getElementById("mega");
  let closeTimer = 0;
  const setMega = (open) => {
    if (!dd) return;
    clearTimeout(closeTimer);
    dd.classList.toggle("open", open);
    nav.classList.toggle("mega-open", open);
    ddBtn.setAttribute("aria-expanded", open);
  };
  if (dd && mega) {
    const later = () => { closeTimer = setTimeout(() => setMega(false), 180); };
    ddBtn.addEventListener("click", () => setMega(!dd.classList.contains("open")));
    if (window.matchMedia("(hover: hover)").matches) {
      [dd, mega].forEach((el) => {
        el.addEventListener("mouseenter", () => setMega(true));
        el.addEventListener("mouseleave", later);
      });
    }
    document.addEventListener("click", (e) => { if (!e.target.closest(".nav-dd, .mega")) setMega(false); });
    mega.addEventListener("focusout", (e) => { if (!mega.contains(e.relatedTarget) && e.relatedTarget !== ddBtn) setMega(false); });
  }
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (dd && dd.classList.contains("open")) { setMega(false); ddBtn.focus(); }
    if (nav.classList.contains("open")) { setMenu(false); menuBtn.focus(); }
  });

  // sliding hover highlight behind nav links
  const links = document.querySelector(".nav-links");
  const ink = links && links.querySelector(".nav-ink");
  if (ink) {
    links.querySelectorAll(":scope > a, .nav-dd-btn").forEach((el) => {
      el.addEventListener("mouseenter", () => {
        const a = el.getBoundingClientRect(), b = links.getBoundingClientRect();
        ink.style.width = a.width + "px";
        ink.style.transform = `translateX(${a.left - b.left}px)`;
      });
    });
  }

  /* ---------- Hero: rotating word, cursor spotlight, chip parallax ---------- */
  const hero = document.querySelector("[data-hero]");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (hero) {
    const rot = hero.querySelector("[data-rotator]");
    if (rot && !reduce) {
      const words = [...rot.children];
      let i = 0;
      const fit = (el) => { rot.style.width = el.getBoundingClientRect().width + "px"; };
      // wait for the intro animation + webfont, then start cycling
      (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
        fit(words[0]);
        setInterval(() => {
          const cur = words[i];
          i = (i + 1) % words.length;
          const next = words[i];
          cur.classList.remove("on"); cur.classList.add("out");
          next.classList.remove("out");
          // measure next word while it is still absolutely positioned
          rot.style.width = next.scrollWidth + "px";
          next.classList.add("on");
          setTimeout(() => cur.classList.remove("out"), 800);
        }, 2600);
        window.addEventListener("resize", () => fit(words[i]));
      });
    }
    if (!reduce && window.matchMedia("(pointer: fine)").matches) {
      let raf = 0;
      hero.addEventListener("pointermove", (e) => {
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = 0;
          const r = hero.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
          hero.style.setProperty("--sx", x * 100 + "%");
          hero.style.setProperty("--sy", y * 100 + "%");
          hero.style.setProperty("--mx", (x - 0.5).toFixed(3));
          hero.style.setProperty("--my", (y - 0.5).toFixed(3));
        });
      });
    }
  }

  /* ---------- Hero particles: drifting nodes joined by faint lines ---------- */
  const cvs = document.querySelector("[data-particles]");
  if (cvs && !reduce && cvs.getContext) {
    const ctx = cvs.getContext("2d");
    const host = cvs.closest("[data-hero]");
    const mobile = window.matchMedia("(max-width: 760px)").matches;
    let W = 0, H = 0, dpr = 1, pts = [], running = false, raf = 0;
    const mouse = { x: -9999, y: -9999 };
    const LINK = mobile ? 90 : 130;
    const size = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = host.clientWidth; H = host.clientHeight;
      cvs.width = W * dpr; cvs.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(mobile ? 34 : 90, (W * H) / (mobile ? 9000 : 14000)));
      pts = Array.from({ length: n }, () => ({
        x: Math.random() * W, y: Math.random() * H * 0.85,
        vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
        r: Math.random() * 1.4 + 0.8, hue: Math.random() < 0.7 ? "79,107,255" : "142,107,255",
      }));
    };
    const frame = () => {
      ctx.clearRect(0, 0, W, H);
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < -20) p.x = W + 20; if (p.x > W + 20) p.x = -20;
        if (p.y < -20) p.y = H + 20; if (p.y > H + 20) p.y = -20;
        const dx = mouse.x - p.x, dy = mouse.y - p.y, d2 = dx * dx + dy * dy;
        if (d2 < 160 * 160) { p.x -= dx * 0.004; p.y -= dy * 0.004; } // gentle push away from cursor
      }
      for (let i = 0; i < pts.length; i++) {
        const a = pts[i];
        for (let j = i + 1; j < pts.length; j++) {
          const b = pts[j], dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy);
          if (d < LINK) {
            ctx.strokeStyle = `rgba(${a.hue},${(1 - d / LINK) * 0.22})`;
            ctx.lineWidth = 0.8;
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
        const md = Math.hypot(mouse.x - a.x, mouse.y - a.y);
        if (md < 170) { // light up links to the cursor
          ctx.strokeStyle = `rgba(79,107,255,${(1 - md / 170) * 0.35})`;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
        }
        ctx.fillStyle = `rgba(${a.hue},0.55)`;
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill();
      }
      raf = requestAnimationFrame(frame);
    };
    const start = () => { if (!running) { running = true; raf = requestAnimationFrame(frame); } };
    const stop = () => { running = false; cancelAnimationFrame(raf); };
    size();
    cvs.classList.add("on");
    new IntersectionObserver(([e]) => (e.isIntersecting && !document.hidden ? start() : stop())).observe(host);
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    let rt = 0;
    window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(size, 200); });
    host.addEventListener("pointermove", (e) => { const r = host.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    host.addEventListener("pointerleave", () => { mouse.x = mouse.y = -9999; });
  }

  /* ---------- Mobile: "swipe" hint above horizontal carousels ---------- */
  document.querySelectorAll(".bento, .post-grid, .svc-grid, .stack-groups, .process, .offer-grid").forEach((row) => {
    if (row.children.length < 2) return;
    const hint = document.createElement("div");
    hint.className = "swipe-hint";
    hint.setAttribute("aria-hidden", "true");
    hint.innerHTML = 'Swipe to see more <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
    row.parentNode.insertBefore(hint, row);
    // keyboard users can focus and arrow-scroll the carousel on phones
    if (window.matchMedia("(max-width: 760px)").matches) {
      row.tabIndex = 0;
      row.setAttribute("role", "region");
      const sec = row.closest("section");
      const h = sec && sec.querySelector("h2");
      row.setAttribute("aria-label", (h ? h.textContent.trim() : "List") + " (scrollable)");
    }
  });

  /* ---------- Project filters ---------- */
  const filterBar = document.querySelector(".filters");
  if (filterBar) {
    const cards = document.querySelectorAll(".work-grid .project");
    const apply = (cat) => {
      filterBar.querySelectorAll(".filter").forEach((b) => {
        const on = b.dataset.cat === cat;
        b.classList.toggle("active", on);
        b.setAttribute("aria-pressed", on);
      });
      cards.forEach((c, i) => {
        const show = cat === "all" || c.dataset.cat === cat || c.dataset.cat === "*";
        c.hidden = !show;
        if (show) { c.style.animation = "none"; void c.offsetWidth; c.style.animation = ""; c.style.animationDelay = (i % 6) * 50 + "ms"; }
      });
    };
    filterBar.addEventListener("click", (e) => {
      const btn = e.target.closest(".filter");
      if (!btn) return;
      apply(btn.dataset.cat);
      history.replaceState(null, "", btn.dataset.cat === "all" ? location.pathname : "#" + btn.dataset.cat);
    });
    const hash = location.hash.slice(1);
    if (hash && filterBar.querySelector(`[data-cat="${hash}"]`)) apply(hash);
  }

  /* ---------- Modal ---------- */
  const modal = document.querySelector(".modal");
  const dataEl = document.getElementById("projects-json");
  const PROJECTS = dataEl ? JSON.parse(dataEl.textContent) : [];
  let lastFocus = null;

  function openModal(p) {
    if (!modal || !p) return;
    lastFocus = document.activeElement;
    const src = p.src;
    const host = p.url ? p.url.replace(/^https?:\/\/(www\.)?/, "") : "";
    modal.querySelector(".modal-img").innerHTML = `<img src="${esc(src)}" alt="${esc(p.title)} website">`;
    modal.querySelector(".modal-body").innerHTML = `
      <div class="kicker">${esc(p.label)}</div>
      <h3>${esc(p.title)}</h3>
      <p>${esc(p.summary)}</p>
      <h5>Built with</h5>
      <div class="modal-stack">${p.stack.map((s) => `<span>${icon(s)}${brandName(s)}</span>`).join("")}</div>
      <div class="modal-actions">
        ${p.url ? `<a class="btn btn-dark" href="${esc(p.url)}" target="_blank" rel="noopener">Visit ${esc(host)} ${ARROW_UR}</a>` : ""}
        <a class="btn btn-ghost" href="/contact/">Start a similar project</a>
      </div>`;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    modal.querySelector(".modal-close").focus();
  }
  function closeModal() {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener("click", (e) => {
    const hit = e.target.closest(".project-hit");
    if (hit) openModal(PROJECTS[+hit.closest(".project").dataset.index]);
  });
  if (modal) {
    modal.addEventListener("click", (e) => { if (e.target.closest("[data-close]")) closeModal(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && modal.classList.contains("open")) closeModal(); });
  }

  /* ---------- Reveal on scroll ---------- */
  const els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add("in"));
  }

  /* ---------- Copy email ---------- */
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const label = btn.querySelector("span") || btn;
      const original = label.textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(btn.dataset.copy) : Promise.reject())
        .then(() => { label.textContent = "Copied!"; })
        .catch(() => { label.textContent = btn.dataset.copy; })
        .finally(() => setTimeout(() => (label.textContent = original), 1800));
    });
  });

  /* ---------- Visitor counter (self-hosted PHP, see /api/visits.php) ---------- */
  const visits = document.querySelector(".visits");
  if (visits && location.protocol === "https:") {
    let counted = false;
    try { counted = sessionStorage.getItem("rn-visit") === "1"; } catch (e) {}
    fetch("/api/visits.php", { method: counted ? "GET" : "POST", cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((d) => {
        if (typeof d.total !== "number" || d.total < 1) return;
        try { sessionStorage.setItem("rn-visit", "1"); } catch (e) {}
        const el = visits.querySelector("[data-visits]");
        const end = d.total, start = Math.max(0, end - 40), t0 = performance.now();
        const step = (t) => {
          const k = Math.min(1, (t - t0) / 900);
          el.textContent = Math.round(start + (end - start) * (1 - Math.pow(1 - k, 3))).toLocaleString();
          if (k < 1) requestAnimationFrame(step);
        };
        visits.hidden = false;
        requestAnimationFrame(step);
      })
      .catch(() => {});
  }

  /* ---------- Send a message to /api/contact.php (falls back to email app) ---------- */
  const sendMessage = (data) =>
    fetch("/api/contact.php", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
      .then((r) => r.json().catch(() => ({ ok: false })).then((j) => (r.ok && j.ok ? j : Promise.reject(j.error || "failed"))));
  const mailtoFallback = (to, d) =>
    `mailto:${to}?subject=${encodeURIComponent("Project enquiry" + (d.topic ? ": " + d.topic : ""))}&body=${encodeURIComponent(d.message + "\n\n" + (d.name || ""))}`;

  /* ---------- Chat widget ---------- */
  const chat = document.querySelector("[data-chat]");
  if (chat) {
    const fab = chat.querySelector(".chat-fab");
    const panel = chat.querySelector(".chat-panel");
    const log = chat.querySelector(".chat-log");
    const form = chat.querySelector(".chat-form");
    const details = form.querySelector(".chat-details");
    const ta = form.querySelector("textarea");
    const send = form.querySelector(".chat-send");
    const TO = "rnamocotdev@gmail.com";
    const state = { step: "message", topic: "", message: "", opened: 0 };
    const add = (cls, html) => {
      const el = document.createElement("div");
      el.className = "msg " + cls;
      el.innerHTML = html;
      log.appendChild(el);
      log.scrollTop = log.scrollHeight;
      return el;
    };
    const typing = (ms) => new Promise((r) => {
      const t = add("bot typing", "<i></i><i></i><i></i>");
      setTimeout(() => { t.remove(); r(); }, ms);
    });
    const open = (yes) => {
      chat.classList.toggle("open", yes);
      fab.setAttribute("aria-expanded", yes);
      if (yes) { state.opened = state.opened || Date.now(); setTimeout(() => (state.step === "details" ? details.querySelector("input") : ta).focus(), 300); }
      else fab.focus();
    };
    fab.addEventListener("click", () => open(true));
    chat.querySelector(".chat-x").addEventListener("click", () => open(false));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && chat.classList.contains("open")) open(false); });
    ta.addEventListener("input", () => { ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight, 120) + "px"; });
    ta.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });
    log.addEventListener("click", (e) => {
      const chip = e.target.closest("[data-topic]");
      if (!chip || state.step !== "message") return;
      state.topic = chip.dataset.topic;
      chip.parentElement.remove();
      add("me", esc(state.topic));
      typing(600).then(() => { add("bot", "Great. Tell me a little about it: goals, timeline, or a link to your current site."); ta.focus(); });
    });
    const askDetails = () => {
      state.step = "details";
      typing(700).then(() => {
        add("bot", "Thanks! Where should I reply? Add your name and email below and hit send.");
        details.hidden = false;
        ta.placeholder = "Anything else? (optional)";
        details.querySelector("input").focus();
      });
    };
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const text = ta.value.trim();
      if (state.step === "message") {
        if (!text) return ta.focus();
        state.message += (state.message ? "\n" : "") + text;
        add("me", esc(text));
        ta.value = ""; ta.style.height = "auto";
        const chips = log.querySelector(".chat-chips");
        if (chips) chips.remove();
        return askDetails();
      }
      if (state.step === "details") {
        const name = form.name.value.trim(), email = form.email.value.trim();
        if (text) { state.message += "\n" + text; add("me", esc(text)); ta.value = ""; }
        if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          add("bot err", "Please add your name and a valid email so I can reply.");
          return (name ? form.email : form.name).focus();
        }
        state.step = "sending";
        send.disabled = true;
        const data = { name, email, message: state.message, topic: state.topic, page: location.href, website: form.website.value, t: state.opened };
        typing(500).then(() => sendMessage(data))
          .then(() => {
            state.step = "done";
            details.hidden = true;
            form.querySelector(".chat-compose").hidden = true;
            add("bot ok", `Thanks, ${esc(name)}! Your message is in my inbox. I’ll reply to <b>${esc(email)}</b>, usually within 24 hours.`);
          })
          .catch((err) => {
            state.step = "details";
            send.disabled = false;
            add("bot err", `${typeof err === "string" && err !== "failed" ? esc(err) + " " : "I couldn’t send that just now. "}You can also <a href="${mailtoFallback(TO, data)}">email me directly</a>.`);
          });
      }
    });
  }

  /* ---------- Contact form ---------- */
  const form = document.querySelector(".contact-form");
  if (form) {
    const params = new URLSearchParams(location.search);
    const pre = params.get("service");
    if (pre) {
      const opt = form.querySelector(`option[data-slug="${CSS.escape(pre)}"]`);
      if (opt) opt.selected = true;
    }
    const t0 = Date.now();
    const btn = form.querySelector('button[type="submit"]');
    const note = form.querySelector(".form-note");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const d = new FormData(form);
      const data = { name: d.get("name"), email: d.get("email"), topic: d.get("service"), budget: d.get("budget"),
                     message: d.get("message"), website: d.get("website") || "", page: location.href, t: t0 };
      btn.disabled = true;
      const label = btn.innerHTML;
      btn.textContent = "Sending…";
      sendMessage(data)
        .then(() => {
          form.innerHTML = `<div class="form-done"><h2>Thanks, ${esc(data.name)}!</h2><p>Your message is in my inbox. I’ll reply to <b>${esc(data.email)}</b>, usually within 24 hours.</p></div>`;
        })
        .catch((err) => {
          btn.disabled = false;
          btn.innerHTML = label;
          note.innerHTML = `${typeof err === "string" && err !== "failed" ? esc(err) + " " : "Couldn’t send right now. "}<a class="ulink" href="${mailtoFallback(form.dataset.mailto, data)}">Email me directly</a> instead.`;
          note.classList.add("err");
        });
    });
  }
})();
