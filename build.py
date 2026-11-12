#!/usr/bin/env python3
"""
Static site builder for Renie Namocot's portfolio.

    python build.py            -> builds the site into ./public
    python build.py --serve    -> builds, then serves ./public on http://localhost:5173

Edit content in:
    src/content/services.py   service landing pages
    src/content/blog.py       blog posts
    src/content/plugins.py    plugin store
    src/data/projects.json    portfolio projects
    src/pages/home.html       homepage sections
"""
import html
import json
import math
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "public"
sys.path.insert(0, str(SRC / "content"))

from services import SERVICES  # noqa: E402
from blog import POSTS  # noqa: E402
from plugins import PLUGINS as ALL_PLUGINS  # noqa: E402
from legal import PRIVACY, TERMS  # noqa: E402

# Only plugins marked "published": True appear on the site. With none published,
# the whole plugin store (pages, nav, sitemap, homepage section) is hidden.
PLUGINS = [p for p in ALL_PLUGINS if p.get("published")]
HAS_PLUGINS = bool(PLUGINS)
# Always show the /plugins/ store page and its nav/footer links, even before any
# plugin is published (it shows a "coming soon" state). Set to False to hide it.
SHOW_PLUGIN_STORE = True
STORE_ON = SHOW_PLUGIN_STORE or HAS_PLUGINS

# ------------------------------------------------------------------ CONFIG
SITE_URL = "https://rnamocotdev.com"        # <-- CHANGE to your real domain (no trailing slash)
NAME = "Renie Namocot"
JOB = "Full-Stack Web Developer"
TAGLINE = "WordPress & Shopify Developer"
EMAIL = "rnamocotdev@gmail.com"
LOCATION = "Philippines"
COUNTRIES = ["Australia", "United States", "United Kingdom", "Germany", "New Zealand", "Singapore"]
SAME_AS = [
    # Add your profiles, they strengthen your entity for Google & AI search:
    # "https://www.linkedin.com/in/your-handle",
    # "https://github.com/your-handle",
    # "https://www.upwork.com/freelancers/your-id",
]
OG_IMAGE = "/assets/img/profile.webp"
SITES_BUILT = "1,000+"   # total websites built (most under NDA)
CREDIT_URL = "https://renienamocot.com/"   # footer "Designed & developed by RN" link
# Search engine verification. Paste ONLY the content="..." value from each tool (leave "" to skip):
GOOGLE_SITE_VERIFICATION = "-qCzvDETRABgZTAZikY0MfzuzwIbW0UPn7OZMZOH4lA"   # Google Search Console -> Settings -> Ownership verification -> HTML tag
BING_SITE_VERIFICATION = ""     # Bing Webmaster Tools -> Add site -> HTML Meta Tag
# IndexNow key (Bing, Yandex, Seznam, Naver...). Any 8-128 hex chars; a file with this name is published at the site root.
INDEXNOW_KEY = "7f3c9a1e5b2d4f8a9c0e6b1d3a5f7c9e"
# Google Analytics 4 Measurement ID, e.g. "G-ABC123XYZ". Leave "" for no analytics.
# When set, a cookie consent banner appears and GA only loads after the visitor clicks "Accept"
# (Google Consent Mode v2), and the privacy policy is updated automatically.
GA4_ID = ""
LEGAL_UPDATED = "2026-11-10"   # "Last updated" date on /privacy/ and /terms/. Change it when you edit src/content/legal.py
BUILD_DATE = date.today().isoformat()

DATA = json.loads((SRC / "data" / "projects.json").read_text(encoding="utf-8"))
PROJECTS, CATEGORIES = DATA["projects"], DATA["categories"]
SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}
SITEMAP = []

# ------------------------------------------------------------------ HELPERS
esc = html.escape
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg>'

LETTERMARKS = {"divi": ("D", "#7A2EE6"), "acf": ("ACF", "#007A65")}
BRAND_NAMES = {
    "nextdotjs": "Next.js", "nodedotjs": "Node.js", "woocommerce": "WooCommerce", "wordpress": "WordPress",
    "graphql": "GraphQL", "php": "PHP", "acf": "ACF Pro", "googleanalytics": "Google Analytics",
    "googlecalendar": "Google Calendar", "tailwindcss": "Tailwind CSS", "paypal": "PayPal", "hubspot": "HubSpot",
    "javascript": "JavaScript", "n8n": "n8n", "mysql": "MySQL", "html5": "HTML5",
    "googlesearchconsole": "Google Search Console", "googletagmanager": "Google Tag Manager", "googleads": "Google Ads",
}


def brand(slug):
    return BRAND_NAMES.get(slug, slug[:1].upper() + slug[1:])


# ------------------------------------------------------------------ LOCAL ASSETS
# Every image is self-hosted. External sources are downloaded ONCE into assets/
# (cached; delete a file to re-download it), then served from your own domain.
ASSETS = ROOT / "assets"
UA = {"User-Agent": "Mozilla/5.0 (portfolio build script)"}
_failed = set()


def _fetch(url):
    import urllib.request
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


# ------------------------------------------------------------------ IMAGE PIPELINE
# High-quality originals live in src/media/<kind>/ (NOT deployed). The build makes
# resized, cropped WebP variants in assets/img/<kind>/<name>-<width>.webp and every
# <img> gets srcset/sizes/width/height automatically (see `responsive`).
MEDIA = SRC / "media"
IMG_KINDS = {
    # kind:  (widths, aspect w/h, webp quality, default `sizes`)
    "stock": ((480, 800, 1200, 1800), 3 / 2, 72, "(max-width: 960px) 92vw, 50vw"),
    "work": ((480, 800, 1200), 16 / 10, 74, "(max-width: 640px) 68vw, (max-width: 1100px) 46vw, 30vw"),
}
_variants = {}


def ensure_variants(kind, name):
    """Create (once) the WebP variants for a master image; returns {width: (w, h)}."""
    key = (kind, name)
    if key in _variants:
        return _variants[key]
    widths, aspect, quality, _ = IMG_KINDS[kind]
    master = MEDIA / kind / f"{name}.jpg"
    if not master.exists():
        if kind != "stock":
            raise FileNotFoundError(master)
        master.parent.mkdir(parents=True, exist_ok=True)
        print(f"  downloading photo {name}")
        master.write_bytes(_fetch(f"https://images.unsplash.com/{name}?auto=format&fit=crop&w=2400&q=90&fm=jpg"))
    out_dir = ASSETS / "img" / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    dims = {w: (w, round(w / aspect)) for w in widths}
    todo = [w for w in widths if not (out_dir / f"{name}-{w}.webp").exists()
            or (out_dir / f"{name}-{w}.webp").stat().st_mtime < master.stat().st_mtime]
    if todo:
        from PIL import Image, ImageOps
        src = Image.open(master).convert("RGB")
        # crop to the target aspect (top-anchored for screenshots, centred for photos)
        centering = (0.5, 0.0) if kind == "work" else (0.5, 0.5)
        for w in todo:
            im = ImageOps.fit(src, dims[w], Image.LANCZOS, centering=centering)
            q = quality if w <= 800 else quality - 8  # big variants are viewed at high DPR: artefacts invisible
            im.save(out_dir / f"{name}-{w}.webp", "WEBP", quality=q, method=6)
    _variants[key] = dims
    return dims


def _pick(widths, w):
    return next((x for x in widths if x >= w), widths[-1])


def local_photo(pid, w=1200):
    dims = ensure_variants("stock", pid)
    return f"/assets/img/stock/{pid}-{_pick(sorted(dims), w)}.webp"


VARIANT_RX = re.compile(r"/assets/img/(stock|work)/([\w-]+?)-(\d+)\.webp")


def srcset_for(src):
    m = VARIANT_RX.fullmatch(src)
    if not m:
        return None
    kind, name, w = m.group(1), m.group(2), int(m.group(3))
    dims = ensure_variants(kind, name)
    srcset = ", ".join(f"/assets/img/{kind}/{name}-{x}.webp {x}w" for x in sorted(dims))
    return srcset, IMG_KINDS[kind][3], dims[w]


def responsive(markup):
    """Add srcset, sizes and the true width/height to every pipeline <img>."""
    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        info = srcset_for(src)
        if not info or "srcset=" in tag:
            return tag
        srcset, sizes, (w, h) = info
        custom = re.search(r'data-sizes="([^"]+)"', tag)
        if custom:
            sizes = custom.group(1)
            tag = tag.replace(custom.group(0), "")
        tag = re.sub(r'\s(width|height)="\d+"', "", tag)
        return tag.replace(f'src="{src}"', f'src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}"', 1)
    return re.sub(r"<img\s[^>]*>", rep, markup)


# ------------------------------------------------------------------ SOCIAL SHARE IMAGES (og:image)
# Facebook/LinkedIn/X need JPG/PNG, ideally 1200x630.
def og_image(src=None):
    from PIL import Image, ImageOps
    out_dir = ASSETS / "img" / "og"
    out_dir.mkdir(parents=True, exist_ok=True)
    m = VARIANT_RX.fullmatch(src or "")
    if m:
        kind, name = m.group(1), m.group(2)
        dest = out_dir / f"{name}.jpg"
        if not dest.exists():
            centering = (0.5, 0.0) if kind == "work" else (0.5, 0.5)
            im = ImageOps.fit(Image.open(MEDIA / kind / f"{name}.jpg").convert("RGB"), (1200, 630), Image.LANCZOS, centering=centering)
            im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
        return f"/assets/img/og/{dest.name}"
    dest = out_dir / "default.jpg"
    if not dest.exists():
        make_default_og(dest)
    return "/assets/img/og/default.jpg"


def make_default_og(dest):
    """Branded 1200x630 share card: RN mark, name, role and profile photo."""
    from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps

    def font(names, size):
        for n in names:
            for d in ("C:/Windows/Fonts/", "/Library/Fonts/", "/usr/share/fonts/truetype/dejavu/"):
                try:
                    return ImageFont.truetype(d + n, size)
                except OSError:
                    pass
        return ImageFont.load_default(size)
    bold = ["segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
    reg = ["segoeui.ttf", "arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#F6F6F3")
    d = ImageDraw.Draw(im)
    # photo panel (white background multiplied onto a soft blue tint, like the site)
    panel = Image.new("RGB", (470, 550), "#DCE1F4")
    photo = ImageOps.fit(Image.open(ASSETS / "img" / "profile.webp").convert("RGB"), (470, 550), Image.LANCZOS, centering=(0.5, 0.25))
    panel = ImageChops.multiply(panel, photo)
    mask = Image.new("L", panel.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *panel.size), 36, fill=255)
    im.paste(panel, (W - 470 - 40, 40), mask)
    # RN mark, drawn 8x larger then downscaled for smooth anti-aliased edges
    k, size = 8, 88
    mk = Image.new("RGBA", (40 * k, 40 * k), (0, 0, 0, 0))
    md = ImageDraw.Draw(mk)
    sw = int(3.4 * k)
    P = lambda x, y: (x * k, y * k)
    md.rounded_rectangle((0, 0, 40 * k - 1, 40 * k - 1), 11 * k, fill="#0B0B0C")
    for seg in ([(8.5, 31), (8.5, 9), (15, 9)], [(15, 19), (11.5, 19), (26, 31), (26, 9)]):
        md.line([P(*pt) for pt in seg], fill="white", width=sw, joint="curve")
        for pt in (seg[0], seg[-1]):  # round caps
            x, y = P(*pt); md.ellipse((x - sw / 2, y - sw / 2, x + sw / 2, y + sw / 2), fill="white")
    md.arc((10 * k - sw / 2, 9 * k - sw / 2, 20 * k + sw / 2, 19 * k + sw / 2), -90, 90, fill="white", width=sw)
    md.ellipse(((31 - 2.3) * k, (30.6 - 2.3) * k, (31 + 2.3) * k, (30.6 + 2.3) * k), fill="#4F6BFF")
    mk = mk.resize((size, size), Image.LANCZOS)
    im.paste(mk, (72, 70), mk)
    # text
    d.text((72, 210), NAME, font=font(bold, 64), fill="#0B0B0C")
    d.text((72, 292), TAGLINE, font=font(reg, 36), fill="#2A2A2E")
    y = 372
    for line in ("1,000+ websites built", "Custom themes · Plugins · WooCommerce · Shopify"):
        d.text((72, y), line, font=font(reg, 26), fill="#6B6B73")
        y += 40
    d.rounded_rectangle((72, 500, 72 + 330, 556), 28, fill="#0B0B0C")
    d.text((100, 513), EMAIL, font=font(reg, 24), fill="white")
    im.save(dest, "JPEG", quality=86, optimize=True, progressive=True)


def local_icon(slug, color=None):
    """Simple Icons slug -> self-hosted SVG (brand colour, or e.g. color='white')."""
    name = f"{slug}-{color}.svg" if color else f"{slug}.svg"
    dest = ASSETS / "img" / "icons" / name
    if not dest.exists():
        if name in _failed:
            return None
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            print(f"  downloading icon {name}")
            dest.write_bytes(_fetch(f"https://cdn.simpleicons.org/{slug}" + (f"/{color}" if color else "")))
        except Exception as e:
            print(f"  ! icon {name} unavailable ({e}); using lettermark")
            _failed.add(name)
            return None
    return f"/assets/img/icons/{name}"


def local_flag(code):
    dest = ASSETS / "img" / "flags" / f"{code}.svg"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"  downloading flag {code}")
        dest.write_bytes(_fetch(f"https://flagcdn.com/{code}.svg"))
    return f"/assets/img/flags/{code}.svg"


def localize(markup):
    """Rewrite any remaining external image URLs in hand-written HTML to self-hosted copies."""
    markup = re.sub(r"https://images\.unsplash\.com/(photo-[0-9a-f-]+)\?[^\"'\s)]*?w=(\d+)[^\"'\s)]*",
                    lambda m: local_photo(m.group(1), int(m.group(2))), markup)
    markup = re.sub(r"https://flagcdn\.com/w\d+/([a-z]{2})\.png", lambda m: local_flag(m.group(1)), markup)
    return markup


def icon(slug, small=False, color=None, label=False):
    src = None if slug in LETTERMARKS else local_icon(slug, color)
    if src is None:
        t, bg = LETTERMARKS.get(slug, (brand(slug)[:2], "#0B0B0C"))
        if small and len(t) > 1:
            t = t[0]
        cls = "lm-sm" if small else "lm"
        if label:
            return f'<span class="{cls}" style="background:{bg}" role="img" aria-label="{brand(slug)}">{t}</span>'
        return f'<span class="{cls}" style="background:{bg}" aria-hidden="true">{t}</span>'
    size = 16 if small else 22
    return (f'<img src="{src}" alt="{brand(slug) if label else ""}" width="{size}" height="{size}" '
            f'loading="lazy" decoding="async" data-slug="{slug}">')


def hydrate(markup):
    """Turn <i data-icon="slug" [data-color="x"]></i> into real icons at build time."""
    def rep(m):
        attrs = dict(re.findall(r'data-(\w+)="([^"]*)"', m.group(0)))
        return icon(attrs.get("icon"), small="data-small" in m.group(0), color=attrs.get("color"))
    return re.sub(r'<i data-icon="[^"]+"[^>]*></i>', rep, markup)


def photo(pid, w=1200, q=80):
    if pid.startswith("/") or pid.startswith("http"):
        return pid
    return local_photo(pid, w)


def pimg(p, w=1200):
    src = p.get("src")
    if not src:
        return photo(p["img"], w)
    m = VARIANT_RX.fullmatch(src)
    if m:
        dims = ensure_variants(m.group(1), m.group(2))
        return f"/assets/img/{m.group(1)}/{m.group(2)}-{_pick(sorted(dims), w)}.webp"
    return src


def asset_version(rel):
    """Short content hash for cache-busting (?v=...) so browsers fetch updated CSS/JS immediately."""
    import hashlib
    return hashlib.md5((ASSETS / rel).read_bytes()).hexdigest()[:8]


def abs_url(path):
    return SITE_URL + path


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")


def fmt_date(d):
    return date.fromisoformat(d).strftime("%b %d, %Y").replace(" 0", " ")


def read_time(body):
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return max(1, math.ceil(words / 220))


LOGO_SVG = ('<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11"/>'
            '<path d="M8.5 31V9H15a5 5 0 0 1 0 10h-3.5L26 31V9" fill="none" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="31" cy="30.6" r="2.3"/></svg>')

# ------------------------------------------------------------------ SCHEMA
PERSON_ID = SITE_URL + "/#person"
BUSINESS_ID = SITE_URL + "/#business"
WEBSITE_ID = SITE_URL + "/#website"

PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": NAME, "jobTitle": JOB, "email": f"mailto:{EMAIL}",
    "description": f"Full-stack WordPress & Shopify developer based in the Philippines who has built {SITES_BUILT} websites for clients worldwide.",
    "url": SITE_URL + "/", "image": abs_url(OG_IMAGE),
    "address": {"@type": "PostalAddress", "addressCountry": "PH"},
    "knowsAbout": ["WordPress development", "Custom WordPress themes", "WordPress plugin development",
                   "Headless WordPress", "Next.js", "Elementor", "Divi", "Advanced Custom Fields",
                   "WooCommerce", "Shopify theme development", "Shopify API", "Stripe", "PayPal",
                   "Online booking systems", "Business automation", "Figma to WordPress",
                   "Responsive web design", "Laravel", "React", "REST APIs", "GraphQL", "SEO", "Technical SEO",
                   "Google Search Console", "Google Analytics 4", "Google Tag Manager", "Conversion tracking",
                   "E-commerce tracking", "Core Web Vitals"],
    "sameAs": SAME_AS,
}
BUSINESS = {
    "@type": "ProfessionalService", "@id": BUSINESS_ID, "name": f"{NAME}: {TAGLINE}",
    "url": SITE_URL + "/", "image": abs_url(OG_IMAGE), "email": EMAIL, "founder": {"@id": PERSON_ID},
    "logo": {"@type": "ImageObject", "url": abs_url("/assets/img/icons-app/icon-512.png"), "width": 512, "height": 512},
    "address": {"@type": "PostalAddress", "addressCountry": "PH"},
    "areaServed": [{"@type": "Country", "name": c} for c in COUNTRIES] + [{"@type": "Place", "name": "Worldwide"}],
    "priceRange": "$$",
    "hasOfferCatalog": {
        "@type": "OfferCatalog", "name": "Web development services",
        "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                             "url": abs_url(f"/services/{s['slug']}/")}} for s in SERVICES],
    },
}
WEBSITE = {"@type": "WebSite", "@id": WEBSITE_ID, "url": SITE_URL + "/", "name": NAME,
           "publisher": {"@id": PERSON_ID}, "inLanguage": "en"}


def breadcrumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(u)} for i, (n, u) in enumerate(trail)]}


def breadcrumbs_html(trail):
    items = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{esc(n)}</li>')
        else:
            items.append(f'<li><a href="{u}">{esc(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


# ------------------------------------------------------------------ LAYOUT
NAV_ITEMS = [("About", "/about/"), ("Services", "/services/"), ("Work", "/projects/"),
             ("Plugins", "/plugins/"), ("Blog", "/blog/"), ("Contact", "/contact/")]
if not STORE_ON:
    NAV_ITEMS = [n for n in NAV_ITEMS if n[1] != "/plugins/"]


SERVICE_SHORT = {
    "wordpress-development": "Fast, secure, custom WordPress sites",
    "custom-wordpress-theme-development": "Hand-coded block & classic themes",
    "wordpress-plugin-development": "Bespoke features & API integrations",
    "headless-wordpress-development": "WordPress + Next.js front ends",
    "elementor-development": "Pixel-perfect, editable Elementor Pro",
    "divi-development": "Custom Divi builds & child themes",
    "acf-development": "Structured content with ACF Pro",
    "woocommerce-development": "Custom stores that sell",
    "shopify-development": "OS 2.0 themes, apps & APIs",
    "stripe-paypal-payment-integration": "Checkout, subscriptions, deposits",
    "online-booking-system-development": "Appointments, classes, reservations",
    "wordpress-automation": "Zapier, Make, n8n & webhooks",
    "figma-to-wordpress": "Designs converted pixel-perfect",
    "web-design": "Clean, responsive, conversion-led UI",
    "technical-seo-analytics": "GSC, GA4, events & conversions",
    "custom-web-development": "Dashboards, SaaS & web apps",
}
CHEVRON = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>'


TAB_ICONS = {
    "/": '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "/services/": '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="2"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
    "/projects/": '<rect x="3" y="4" width="18" height="14" rx="2.5"/><path d="M3 8.5h18M8 21h8"/>',
    "/blog/": '<path d="M5 4h11l3 3v13H5z"/><path d="M9 10h6M9 14h6M9 18h4"/>',
    "/contact/": '<path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-5 4V6a1 1 0 0 1 1-1z"/>',
}


def tabbar(active):
    tabs = [("Home", "/"), ("Services", "/services/"), ("Work", "/projects/"), ("Blog", "/blog/"), ("Contact", "/contact/")]
    out = []
    for n, u in tabs:
        on = active == u
        out.append(f'<a href="{u}" class="tab{" on" if on else ""}"{" aria-current=\"page\"" if on else ""}>'
                   f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{TAB_ICONS[u]}</svg>'
                   f'<span>{n}</span></a>')
    return "".join(out)


def nav(active):
    def link(n, u):
        cur = ' class="active" aria-current="page"' if active == u else ""
        return f'<a href="{u}"{cur}>{n}</a>'

    items = []
    for n, u in NAV_ITEMS:
        if u == "/services/":
            cur = " active" if active == u else ""
            items.append(f'<div class="nav-dd"><button class="nav-dd-btn{cur}" aria-expanded="false" aria-controls="mega">'
                         f'Services {CHEVRON}</button></div>')
        elif u != "/contact/":
            items.append(link(n, u))
    mega_items = "".join(
        f'<a class="mega-item" href="/services/{x["slug"]}/"><span class="mega-ico">{icon(x["icons"][0])}</span>'
        f'<span><strong>{esc(x["name"])}</strong><small>{esc(SERVICE_SHORT.get(x["slug"], ""))}</small></span></a>'
        for x in SERVICES)
    m_services = "".join(f'<a href="/services/{x["slug"]}/">{icon(x["icons"][0], small=True)}{esc(x["name"])}</a>' for x in SERVICES)
    m_main = "".join(f'<a class="m-big{" active" if active == u else ""}" href="{u}">{n}</a>' for n, u in NAV_ITEMS)
    return f"""<header class="nav">
  <div class="nav-bar">
    <a href="/" class="logo" aria-label="{NAME}, home">{LOGO_SVG}<span class="logo-text">{NAME}<small>{TAGLINE}</small></span></a>
    <nav class="nav-links" aria-label="Primary">{"".join(items)}<span class="nav-ink" aria-hidden="true"></span></nav>
    <div class="nav-cta">
      <a href="/contact/" class="nav-contact{" active" if active == "/contact/" else ""}">Contact</a>
      <a href="/contact/" class="btn btn-dark btn-sm nav-btn">Let’s talk {ARROW}</a>
      <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="m-menu"><span></span><span></span></button>
    </div>
  </div>
  <div class="mega" id="mega" role="region" aria-label="Services">
    <div class="mega-inner">
      <div class="mega-grid">{mega_items}</div>
      <div class="mega-side">
        <span class="kicker">Not sure what you need?</span>
        <p>Tell me about your project and I’ll recommend the right platform and approach, with no obligation.</p>
        <a href="/contact/" class="btn btn-dark btn-sm">Get a free recommendation {ARROW}</a>
        <a href="/services/" class="link-arrow">See all services →</a>
      </div>
    </div>
  </div>
  <nav class="tabbar" aria-label="Quick navigation">{tabbar(active)}</nav>
  <div class="m-menu" id="m-menu" aria-label="Mobile menu">
    <nav class="m-main" aria-label="Mobile primary">{m_main}</nav>
    <div class="m-sub"><span class="kicker">Services</span><div class="m-services">{m_services}</div></div>
    <div class="m-foot"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="/contact/" class="btn btn-dark">Start a project {ARROW}</a></div>
  </div>
</header>"""


def cta(title='Have a project <span class="serif">in mind?</span>',
        text="Whether it’s a WordPress rebuild, a new Shopify theme or a custom web app, I’d like to hear about it. I usually reply within 24 hours."):
    return f"""<section class="cta dark" id="contact">
  <div class="cta-bg"><img src="{photo('photo-1497366216548-37526070297c', 1800)}" data-sizes="(max-width: 640px) 100vw, 60vw" alt="" loading="lazy" decoding="async"></div>
  <div class="wrap">
    <div class="kicker reveal">Contact</div>
    <h2 class="reveal d1">{title}</h2>
    <p class="reveal d2">{text}</p>
    <a href="mailto:{EMAIL}" class="email-link reveal d2">{EMAIL}</a>
    <div class="cta-actions reveal d3">
      <a href="/contact/" class="btn btn-light">Start a project {ARROW}</a>
      <button class="btn btn-ghost" data-copy="{EMAIL}"><span>Copy email</span></button>
    </div>
  </div>
</section>"""


def footer():
    svc = "".join(f'<a href="/services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES[:8])
    svc2 = "".join(f'<a href="/services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES[8:])
    return f"""<footer>
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="/" class="logo" aria-label="{NAME}, home">{LOGO_SVG}<span class="logo-text">{NAME}<small>Remote · Worldwide</small></span></a>
        <p>Full-stack web developer specialising in WordPress, Shopify and custom web applications. Based in the {LOCATION}, working with clients worldwide.</p>
        <a href="mailto:{EMAIL}" class="footer-email">{EMAIL}</a>
      </div>
      <div class="footer-cols">
        <div><h2 class="fh">Services</h2>{svc}</div>
        <div><h2 class="fh">More services</h2>{svc2}</div>
        <div><h2 class="fh">Explore</h2><a href="/about/">About</a><a href="/projects/">Projects</a>{'<a href="/plugins/">Plugins</a>' if STORE_ON else ''}<a href="/blog/">Blog</a><a href="/contact/">Contact</a><a href="/sitemap/">Sitemap</a></div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {date.today().year} {NAME}. All rights reserved.</span>
      <span class="legal-links"><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a>{'<button type="button" data-consent-open>Cookie settings</button>' if GA4_ID else ''}</span>
      <span class="visits" hidden><b data-visits>0</b> visitors</span>
      <span class="credit">Designed & developed by <a href="{CREDIT_URL}" target="_blank" rel="noopener" title="Renie Namocot: Full-Stack Web Developer">{LOGO_SVG.replace('class="logo-mark"', 'class="logo-mark credit-mark"')}<span>RN</span></a></span>
    </div>
  </div>
</footer>"""


MODAL = """<div class="modal" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Project details">
  <div class="modal-backdrop" data-close></div>
  <div class="modal-panel">
    <button class="modal-close" data-close aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    <div class="modal-img"></div>
    <div class="modal-body"></div>
  </div>
</div>"""


CHAT_WIDGET = f"""<div class="chat" data-chat>
  <button class="chat-fab" type="button" aria-label="Chat with Renie" aria-expanded="false" aria-controls="chat-panel">
    <span class="chat-av"><img src="/assets/img/profile.webp" alt="" width="40" height="40"></span>
    <span class="chat-fab-text"><strong>Chat with Renie</strong><small>Usually replies within 24h</small></span>
    <svg class="chat-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-5 4V6a1 1 0 0 1 1-1z"/></svg>
  </button>
  <section class="chat-panel" id="chat-panel" role="dialog" aria-label="Chat with Renie" aria-modal="false">
    <header class="chat-head">
      <span class="chat-av"><img src="/assets/img/profile.webp" alt="" width="40" height="40"></span>
      <div><strong>Renie Namocot</strong><small>WordPress &amp; Shopify developer · replies by email</small></div>
      <button class="chat-x" type="button" aria-label="Close chat"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    </header>
    <div class="chat-log" aria-live="polite">
      <div class="msg bot">Hi, I’m Renie. What are you working on? Pick one below or type your message.</div>
      <div class="chat-chips">
        <button type="button" data-topic="New WordPress website">New WordPress site</button>
        <button type="button" data-topic="Shopify store or theme">Shopify store</button>
        <button type="button" data-topic="WooCommerce / payments">WooCommerce / payments</button>
        <button type="button" data-topic="Fix or speed up my site">Fix or speed up a site</button>
        <button type="button" data-topic="Custom web app / SaaS">Custom app / SaaS</button>
      </div>
    </div>
    <form class="chat-form" novalidate>
      <div class="chat-details" hidden>
        <input name="name" placeholder="Your name" autocomplete="name" aria-label="Your name" maxlength="80">
        <input name="email" type="email" placeholder="Your email" autocomplete="email" aria-label="Your email" maxlength="120">
      </div>
      <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="chat-compose">
        <textarea name="message" rows="1" placeholder="Type your message…" aria-label="Message" maxlength="5000"></textarea>
        <button class="chat-send" type="submit" aria-label="Send"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
      </div>
      <p class="chat-note">Messages go straight to {EMAIL}</p>
    </form>
  </section>
</div>"""


def render(path, title, desc, body, schema=None, active=None, og_type="website", image=None,
           with_cta=True, with_modal=False, priority="0.7", lastmod=None, noindex=False, preload_img=None,
           preload_sizes=None):
    canonical = abs_url(path)
    og_img = abs_url(og_image(image))
    graph = [WEBSITE, PERSON] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    ld = ld.replace('"/assets/', f'"{SITE_URL}/assets/')  # schema needs absolute image URLs
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    projects_json = ""
    if with_modal:
        projects_json = ('<script type="application/json" id="projects-json">'
                         + json.dumps(PROJECTS, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    verification = ""
    if GOOGLE_SITE_VERIFICATION:
        verification += f'<meta name="google-site-verification" content="{esc(GOOGLE_SITE_VERIFICATION)}">\n'
    if BING_SITE_VERIFICATION:
        verification += f'<meta name="msvalidate.01" content="{esc(BING_SITE_VERIFICATION)}">\n'
    preload = ""
    if preload_img:
        info = srcset_for(preload_img)
        if info:
            preload = (f'<link rel="preload" as="image" imagesrcset="{info[0]}" '
                       f'imagesizes="{preload_sizes or info[1]}" fetchpriority="high">')
        else:
            preload = f'<link rel="preload" as="image" href="{preload_img}" fetchpriority="high">'

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Renie N.">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="{NAME}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#F6F6F3">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{verification}
<link rel="alternate" type="application/rss+xml" title="{NAME}: Blog" href="/blog/rss.xml">
<link rel="preload" href="/assets/fonts/inter-tight-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="/assets/css/fonts.css?v={asset_version('css/fonts.css')}">
<link rel="stylesheet" href="/assets/css/style.css?v={asset_version('css/style.css')}">
<script type="application/ld+json">
{ld}
</script>
{ANALYTICS_HEAD}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav(active)}
<main id="main">
{body}
{cta() if with_cta is True else (with_cta or "")}
</main>
{footer()}
{MODAL if with_modal else ""}
{CHAT_WIDGET}
{CONSENT_BANNER}
{projects_json}
<script src="/assets/js/main.js?v={asset_version('js/main.js')}" defer></script>
</body>
</html>
"""
    doc = responsive(localize(hydrate(doc)))
    target = OUT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    if not noindex:
        images = []
        for src in re.findall(r'<img [^>]*?src="(/assets/img/(?:stock|work)/[^"]+|/assets/img/profile\.webp)"', doc):
            m = VARIANT_RX.fullmatch(src)
            if m:  # point the sitemap at the largest variant
                src = f"/assets/img/{m.group(1)}/{m.group(2)}-{max(ensure_variants(m.group(1), m.group(2)))}.webp"
            if src not in images:
                images.append(src)
        SITEMAP.append((canonical, lastmod or BUILD_DATE, priority, images[:30], title))


# ------------------------------------------------------------------ COMPONENTS
def cat_icon(key):
    c = next((c for c in CATEGORIES if c["key"] == key), None)
    return icon(c["icon"], small=True) if c and c.get("icon") else ""


NDA_TILE = """<article class="project nda-tile" data-cat="*">
  <div class="project-media nda-media">
    <div class="nda-inner">
      <span class="nda-num">1,000+</span>
      <span class="nda-label">websites built</span>
      <p>Most of my work is under NDA for agencies and brands, so only a small selection is public. I’m happy to share relevant examples privately.</p>
      <a href="/contact/" class="btn btn-light btn-sm">Request private examples</a>
    </div>
  </div>
</article>"""


def project_card(p, idx, heading="h3", sizes=None):
    stack = "".join(f"<span>{icon(s, small=True, label=True)}</span>" for s in p["stack"][:3])
    visit = (f'<a class="visit" href="{esc(p["url"])}" target="_blank" rel="noopener">'
             f'{esc(re.sub(r"^https?://(www\.)?", "", p["url"]))} {ARROW_UR}</a>') if p.get("url") else ""
    return f"""<article class="project" data-index="{idx}" data-cat="{p['category']}">
  <button class="project-hit" aria-label="View details: {esc(p['title'])}"></button>
  <div class="project-media">
    <img class="cover" src="{pimg(p, 1100)}"{f' data-sizes="{sizes}"' if sizes else ""} alt="{esc(p['title'])} website homepage ({esc(p['label'])})" loading="lazy" decoding="async">
    <div class="overlay"></div>
    <span class="label">{cat_icon(p['category'])}{esc(p['label'])}</span>
    <span class="view">{ARROW_UR}</span>
  </div>
  <div class="project-meta">
    <div><{heading}>{esc(p['title'])}</{heading}><p>{esc(p['summary'])}</p></div>
    <div class="stack">{stack}</div>
  </div>
  {visit}
</article>"""


def showcase(items, eager=0):
    cards = "".join(
        f'<div class="shot"><img src="{pimg(p, 800)}" data-sizes="(max-width: 640px) 240px, 340px" alt="" '
        f'loading="{"eager" if i < eager else "lazy"}" decoding="async">'
        f'<span class="tag">{icon(p["stack"][0], small=True)}{esc(p["label"].split("·")[0].strip())}</span></div>'
        for i, p in enumerate(items))
    return cards + cards.replace('<div class="shot">', '<div class="shot" aria-hidden="true">').replace('loading="eager"', 'loading="lazy"')


def service_card(s, i):
    icons = "".join(f'<span class="ico">{icon(x)}</span>' for x in s["icons"][:3])
    return f"""<article class="card svc-card reveal">
  <span class="num">{i:02d}</span>
  <div class="icons">{icons}</div>
  <h3><a class="stretched" href="/services/{s['slug']}/">{esc(s['name'])}</a></h3>
  <p>{esc(s['desc'])}</p>
  <span class="more">Learn more {ARROW}</span>
</article>"""


def post_card(p, heading="h3"):
    return f"""<article class="post-card reveal">
  <a href="/blog/{p['slug']}/" class="post-media" tabindex="-1" aria-hidden="true"><img src="{photo(p['img'], 800)}" data-sizes="(max-width: 640px) 68vw, (max-width: 1100px) 46vw, 30vw" alt="" loading="lazy" decoding="async"></a>
  <div class="post-meta"><span class="pill">{esc(p['category'])}</span><time datetime="{p['date']}">{fmt_date(p['date'])}</time><span>· {read_time(p['body'])} min read</span></div>
  <{heading}><a class="stretched" href="/blog/{p['slug']}/">{esc(p['title'])}</a></{heading}>
  <p>{esc(p['desc'])}</p>
</article>"""


def plugin_card(p):
    status = '<span class="pill pill-soon">Coming soon</span>' if p["status"] != "available" else f'<span class="pill pill-live">${esc(p["price"])}</span>'
    works = "".join(f"<span>{icon(w, small=True)}</span>" for w in p["works_with"][:4])
    return f"""<article class="plugin-card reveal">
  <div class="plugin-top"><span class="plugin-icon">{icon(p['icon'])}</span>{status}</div>
  <h3><a class="stretched" href="/plugins/{p['slug']}/">{esc(p['name'])}</a></h3>
  <p>{esc(p['tagline'])}</p>
  <div class="plugin-foot"><div class="stack">{works}</div><span class="more">Details {ARROW}</span></div>
</article>"""


def faq_html(faqs):
    return "".join(f'<details class="faq reveal"><summary><h3>{esc(q)}</h3><span class="plus" aria-hidden="true"></span></summary><div class="faq-a"><p>{esc(a)}</p></div></details>' for q, a in faqs)


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ------------------------------------------------------------------ PAGES
def products_section():
    items = [p for p in PROJECTS if p["category"] == "saas"]
    if not items:
        return ""
    cards = []
    for i, p in enumerate(items):
        stack = "".join(f'<span class="chip-ico">{icon(s, small=True)}{brand(s)}</span>' for s in p["stack"])
        host = re.sub(r"^https?://(www\.)?", "", p["url"]).rstrip("/")
        cards.append(f"""<article class="product reveal{' d1' if i else ''}">
  <a class="product-shot" href="{esc(p['url'])}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
    <span class="browser"><i></i><i></i><i></i><b>{esc(host)}</b></span>
    <img src="{pimg(p, 1200)}" data-sizes="(max-width: 960px) 92vw, 46vw" alt="" loading="lazy" decoding="async">
  </a>
  <div class="product-body">
    <span class="product-kind">{esc(p.get('tagline', ''))}</span>
    <h3>{esc(p['title'])}</h3>
    <p>{esc(p['summary'])}</p>
    {f'<p class="product-stat">{esc(p["stat"])}</p>' if p.get('stat') else ''}
    <div class="works">{stack}</div>
    <a class="btn btn-dark btn-sm" href="{esc(p['url'])}" target="_blank" rel="noopener">Visit {esc(host)} {ARROW_UR}</a>
  </div>
</article>""")
    return f"""<section class="section products" id="products">
  <div class="wrap">
    <div class="section-head">
      <div><div class="kicker reveal">My own products</div><h2 class="h2 reveal d1">SaaS I’ve built <span class="serif">and run.</span></h2></div>
      <p class="reveal d2">Beyond client work, I design, build, launch and grow my own software. It’s hands-on experience with product decisions, UX, SEO, security, billing and support.</p>
    </div>
    <div class="product-grid">{"".join(cards)}</div>
  </div>
</section>"""


def software_schema():
    return [{"@type": "SoftwareApplication", "name": p["title"], "url": p["url"], "description": p["summary"],
             "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
             "image": abs_url(pimg(p)), "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID}}
            for p in PROJECTS if p["category"] == "saas"]


def build_home():
    body = (SRC / "pages" / "home.html").read_text(encoding="utf-8")
    featured = [(i, p) for i, p in enumerate(PROJECTS) if p.get("featured")][:6]
    body = body.replace("{{SHOWCASE_1}}", showcase(PROJECTS[0::3], eager=4))
    body = body.replace("{{SHOWCASE_2}}", showcase(PROJECTS[1::3], eager=4))
    body = body.replace("{{SHOWCASE_3}}", showcase(PROJECTS[2::3], eager=4))
    body = body.replace("{{PRODUCTS}}", products_section())
    body = body.replace("{{FEATURED_WORK}}", "".join(project_card(p, i, sizes="(max-width: 640px) 68vw, 46vw") for i, p in featured))
    plugins = "".join(plugin_card(p) for p in PLUGINS[:3])
    body = body.replace("{{PLUGINS_TEASER}}", "" if not HAS_PLUGINS else f"""<section class="section" id="plugins" style="padding-top:0">
  <div class="wrap">
    <div class="section-head">
      <div><div class="kicker reveal">Plugins</div><h2 class="h2 reveal d1">Premium WordPress <span class="serif">plugins.</span></h2></div>
      <div class="reveal d2"><p style="margin-bottom:18px">Lightweight, developer-friendly plugins built from real client work.</p><a href="/plugins/" class="link-arrow">Browse plugins →</a></div>
    </div>
    <div class="plugin-grid">{plugins}</div>
  </div>
</section>""")
    posts = "".join(post_card(p) for p in sorted(POSTS, key=lambda x: x["date"], reverse=True)[:3])
    body = body.replace("{{BLOG_TEASER}}", f"""<section class="section" id="blog" style="padding-top:0">
  <div class="wrap">
    <div class="section-head">
      <div><div class="kicker reveal">Insights</div><h2 class="h2 reveal d1">From the <span class="serif">blog.</span></h2></div>
      <div class="reveal d2"><p style="margin-bottom:18px">Practical notes on WordPress, Shopify, headless builds and SEO.</p><a href="/blog/" class="link-arrow">All articles →</a></div>
    </div>
    <div class="post-grid">{posts}</div>
  </div>
</section>""")
    home_page = {"@type": ["WebPage", "ProfilePage"], "@id": SITE_URL + "/#webpage", "url": SITE_URL + "/",
                 "name": f"{NAME} | WordPress & Shopify Developer", "isPartOf": {"@id": WEBSITE_ID},
                 "about": {"@id": PERSON_ID}, "mainEntity": {"@id": PERSON_ID}}
    render("/", f"{NAME} | WordPress & Shopify Developer for Hire",
           "WordPress & Shopify developer with 1,000+ websites built: custom themes, plugins, headless, WooCommerce, Stripe/PayPal payments and booking systems.",
           body, schema=[BUSINESS, home_page] + software_schema(), active="/", with_modal=True, priority="1.0")


def build_about():
    countries = "".join(
        f'<span><img src="https://flagcdn.com/w40/{c}.png" width="20" height="14" alt="">{n}</span>'
        for c, n in [("au", "Australia"), ("us", "United States"), ("gb", "United Kingdom"), ("de", "Germany"),
                     ("nz", "New Zealand"), ("sg", "Singapore")])
    trail = [("Home", "/"), ("About", "/about/")]
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="about-grid" style="margin-top:28px">
      <div class="portrait reveal">
        <img src="/assets/img/profile.webp" alt="Portrait of {NAME}, {JOB}" width="640" height="680">
        <span class="badge-float b1"><i data-icon="wordpress"></i>WordPress expert</span>
        <span class="badge-float b2"><i data-icon="shopify"></i>Shopify developer</span>
        <div class="name-card"><div><strong>{NAME}</strong><span>{JOB}</span></div><span class="flag"><img src="https://flagcdn.com/w40/ph.png" width="20" height="14" alt="">{LOCATION}</span></div>
      </div>
      <div class="about-text">
        <div class="kicker reveal">About me</div>
        <h1 class="h2 reveal d1">Hi, I’m Renie, <span class="serif">a full-stack web developer.</span></h1>
        <p class="reveal d2">I’m a full-stack web developer based in the {LOCATION}. I build reliable, practical and user-friendly digital products.</p>
        <p class="reveal d2">My experience covers traditional CMS-based websites as well as custom web applications. I’ve worked with businesses, teams and on personal projects, building everything from corporate websites and e-commerce platforms to custom dashboards, management systems and SaaS-style applications.</p>
        <p class="reveal d2">I’ve worked with clients in Australia, the United States, the United Kingdom, Germany, New Zealand and Singapore, collaborating remotely across time zones.</p>
        <p class="reveal d3">I especially like building products from the ground up: taking an idea, designing the system behind it, developing the application, deploying it and continuing to improve it.</p>
        <p class="reveal d3">So far I’ve built <strong>more than 1,000 websites</strong>. Most were for agencies and brands under NDA, so only a small selection appears in my portfolio.</p>
        <p class="reveal d3">I’m also hands-on with <strong>technical SEO and analytics</strong>: Google Search Console, GA4, Google Tag Manager, and event and conversion tracking, so the sites I build can be found and measured.</p>
        <p class="muted reveal d3">I also build and run my own SaaS products, <a class="ulink" href="https://tarsiflow.com/" target="_blank" rel="noopener">tarsiflow</a> (client management for freelancers and agencies) and <a class="ulink" href="https://mytindahan.store/" target="_blank" rel="noopener">MyTindahan</a> (a store app used by 1,500+ sari-sari and grocery store owners). That gives me hands-on experience beyond development, including product decisions, user experience, SEO, security, deployment and marketing.</p>
        <div class="countries reveal d3">{countries}</div>
        <div class="hero-actions" style="justify-content:flex-start"><a href="/services/" class="btn btn-dark">What I do {ARROW}</a><a href="/projects/" class="btn btn-ghost">See my work</a></div>
      </div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Specialities</div><h2 class="h2 reveal d1">What I’m <span class="serif">known for.</span></h2></div></div>
    <div class="svc-grid">{"".join(service_card(s, i + 1) for i, s in enumerate(SERVICES[:6]))}</div>
  </div>
</section>"""
    about = {"@type": "AboutPage", "url": abs_url("/about/"), "name": f"About {NAME}", "mainEntity": {"@id": PERSON_ID}}
    render("/about/", f"About {NAME}: Full-Stack WordPress & Shopify Developer",
           f"{NAME} is a full-stack developer from the {LOCATION} building WordPress, Shopify and custom web apps for clients in AU, US, UK, DE, NZ and SG.",
           body, schema=[about, breadcrumbs_schema(trail)], active="/about/", priority="0.8",
           preload_img="/assets/img/profile.webp")


def build_services_hub():
    trail = [("Home", "/"), ("Services", "/services/")]
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="kicker reveal">Services</div>
    <h1 class="reveal d1">Web development <span class="serif">services.</span></h1>
    <div class="page-hero-row"><p class="reveal d2">WordPress, Shopify and custom development, from custom themes and plugins to headless builds, payments, booking systems and automation. Pick a service to see what’s included, how I work and common questions.</p></div>
  </div>
</section>
<section style="padding-bottom:clamp(80px,10vw,140px)">
  <div class="wrap"><h2 class="sr-only">All services</h2><div class="svc-grid">{"".join(service_card(s, i + 1) for i, s in enumerate(SERVICES))}</div></div>
</section>"""
    lst = {"@type": "CollectionPage", "url": abs_url("/services/"), "name": "Web development services",
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": abs_url(f"/services/{s['slug']}/"), "name": s["name"]}
               for i, s in enumerate(SERVICES)]}}
    render("/services/", "WordPress, Shopify & Web Development Services | Renie Namocot",
           "Custom WordPress themes & plugins, headless, Elementor, Divi, ACF, WooCommerce, Shopify, Stripe & PayPal, booking systems, automation and web apps.",
           body, schema=[lst, BUSINESS, breadcrumbs_schema(trail)], active="/services/", priority="0.9")


def build_service(s):
    path = f"/services/{s['slug']}/"
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
    icons = "".join(f'<span class="ico">{icon(x)}</span>' for x in s["icons"])
    offers = "".join(f'<div class="offer reveal"><span class="check" aria-hidden="true"></span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in s["offers"])
    related = "".join(service_card(SERVICE_BY_SLUG[r], i + 1) for i, r in enumerate(s["related"]) if r in SERVICE_BY_SLUG)
    work = [(i, p) for i, p in enumerate(PROJECTS) if p["category"] in s["projects"]][:3]
    work_html = ""
    if work:
        work_html = f"""<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Related work</div><h2 class="h2 reveal d1">Recent <span class="serif">projects.</span></h2></div><a href="/projects/" class="link-arrow reveal">All projects →</a></div>
    <div class="work-grid" data-work>{"".join(project_card(p, i) for i, p in work)}</div>
  </div>
</section>"""
    posts = [p for p in POSTS if s["slug"] in p["services"]][:3]
    posts_html = ""
    if posts:
        posts_html = f"""<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Reading</div><h2 class="h2 reveal d1">Related <span class="serif">articles.</span></h2></div></div>
    <div class="post-grid">{"".join(post_card(p) for p in posts)}</div>
  </div>
</section>"""
    body = f"""<section class="page-hero svc-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="svc-hero-grid">
      <div>
        <div class="icons reveal">{icons}</div>
        <h1 class="reveal d1">{esc(s['h1'])}</h1>
        <p class="lead-answer reveal d2">{esc(s['lead'])}</p>
        <div class="hero-actions reveal d3" style="justify-content:flex-start"><a href="/contact/?service={s['slug']}" class="btn btn-dark">Get a quote {ARROW}</a><a href="#faq" class="btn btn-ghost">FAQs</a></div>
      </div>
      <div class="svc-hero-img reveal d2"><img src="{photo(s['img'], 1200)}" data-sizes="(max-width: 960px) 92vw, 46vw" alt="{esc(s['name'])}" fetchpriority="high"></div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">What’s included</div><h2 class="h2 reveal d1">{esc(s['name'])} <span class="serif">services.</span></h2></div></div>
    <div class="offer-grid">{offers}</div>
    <div class="prose svc-prose reveal">{s['body']}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Process</div><h2 class="h2 reveal d1">How we’ll <span class="serif">work together.</span></h2></div></div>
    <div class="process">
      <div class="step reveal"><h3>Discover</h3><p>A short call to understand your goals, users, scope and timeline. Then a fixed quote.</p></div>
      <div class="step reveal d1"><h3>Plan & design</h3><p>Architecture, content model and design, signed off before development starts.</p></div>
      <div class="step reveal d2"><h3>Build</h3><p>Development on a staging site with regular progress updates you can review.</p></div>
      <div class="step reveal d3"><h3>Launch & support</h3><p>Launch, SEO checks, training and optional ongoing maintenance.</p></div>
    </div>
  </div>
</section>
{work_html}
<section class="section" id="faq" style="padding-top:0">
  <div class="wrap faq-wrap">
    <div><div class="kicker reveal">FAQ</div><h2 class="h2 reveal d1">Common <span class="serif">questions.</span></h2><p class="reveal d2" style="color:var(--muted);margin-top:20px">Have another question? <a class="ulink" href="mailto:{EMAIL}">Email me</a>.</p></div>
    <div class="faq-list">{faq_html(s['faqs'])}</div>
  </div>
</section>
{posts_html}
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Related services</div><h2 class="h2 reveal d1">You might <span class="serif">also need.</span></h2></div></div>
    <div class="svc-grid">{related}</div>
  </div>
</section>"""
    service = {"@type": "Service", "@id": abs_url(path) + "#service", "name": s["name"], "description": s["desc"],
               "url": abs_url(path), "image": photo(s["img"], 1200), "serviceType": s["name"],
               "provider": {"@id": PERSON_ID},
               "areaServed": [{"@type": "Country", "name": c} for c in COUNTRIES] + [{"@type": "Place", "name": "Worldwide"}],
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["name"], "itemListElement": [
                   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in s["offers"]]}}
    render(path, s["title"], s["desc"], body, schema=[service, faq_schema(s["faqs"]), breadcrumbs_schema(trail)],
           active="/services/", with_modal=bool(work), priority="0.9", image=photo(s["img"], 1200),
           preload_img=photo(s["img"], 1200), preload_sizes="(max-width: 960px) 92vw, 46vw")


def build_projects():
    trail = [("Home", "/"), ("Projects", "/projects/")]
    filters = []
    for c in CATEGORIES:
        n = len(PROJECTS) if c["key"] == "all" else sum(p["category"] == c["key"] for p in PROJECTS)
        if not n:
            continue
        ic = icon(c["icon"], small=True) if c.get("icon") else ""
        active = " active" if c["key"] == "all" else ""
        filters.append(f'<button class="filter{active}" data-cat="{c["key"]}" aria-pressed="{str(c["key"] == "all").lower()}">{ic}{c["name"]}<span class="count">{n}</span></button>')
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="kicker reveal">Portfolio</div>
    <h1 class="reveal d1">Selected <span class="serif">projects.</span></h1>
    <div class="page-hero-row">
      <p class="reveal d2">I’ve built more than 1,000 websites, and most of them are under NDA. These are public builds on WordPress, Elementor, Divi, WooCommerce, Shopify, Wix, Squarespace, BigCommerce and custom code. Open any project for details, or visit the live site.</p>
      <div class="cms-stats reveal d3">
        <div><i data-icon="wordpress"></i><span><strong>WordPress</strong>Themes, plugins, builders</span></div>
        <div><i data-icon="shopify"></i><span><strong>Shopify</strong>Themes, apps, APIs</span></div>
      </div>
    </div>
  </div>
</section>
<section style="padding-bottom:clamp(80px,10vw,140px)">
  <div class="wrap">
    <div class="filters" role="toolbar" aria-label="Filter projects">{"".join(filters)}</div>
    <div class="work-grid" data-work>{"".join(project_card(p, i, "h2") for i, p in enumerate(PROJECTS))}{NDA_TILE}</div>
  </div>
</section>"""
    lst = {"@type": "CollectionPage", "url": abs_url("/projects/"), "name": "Projects",
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "item": {"@type": "CreativeWork", "name": p["title"],
                "description": p["summary"], "image": abs_url(pimg(p)) if pimg(p).startswith("/") else pimg(p), "url": p.get("url"), "creator": {"@id": PERSON_ID}}}
               for i, p in enumerate(PROJECTS)]}}
    render("/projects/", "Projects: Elementor, Shopify & WordPress | Renie Namocot",
           "Portfolio of websites built on Elementor, Divi, custom WordPress themes, WooCommerce, Shopify, headless WordPress (Next.js) and other CMS platforms.",
           body, schema=[lst, breadcrumbs_schema(trail)], active="/projects/", with_modal=True, priority="0.8")


PLUGIN_CATEGORIES = [
    ("woocommerce", "WooCommerce extensions", "Checkout, product and order tools that make WooCommerce stores sell more."),
    ("wordpress", "Contact Form 7 add-ons", "Extra fields, integrations and spam protection for Contact Form 7."),
    ("php", "Shortcodes", "Drop-in shortcodes for layouts, content blocks and dynamic data."),
    ("javascript", "Sliders", "Fast, accessible sliders and carousels for any theme or builder."),
]


def category_card(ico, title, text):
    return f"""<article class="plugin-card reveal">
  <div class="plugin-top"><span class="plugin-icon">{icon(ico)}</span></div>
  <h3>{esc(title)}</h3>
  <p>{esc(text)}</p>
  <div class="plugin-foot"><span></span><a class="more" href="mailto:{EMAIL}?subject={esc(title).replace(' ', '%20')}%20waitlist">Join waitlist {ARROW}</a></div>
</article>"""


def build_plugins():
    trail = [("Home", "/"), ("Plugins", "/plugins/")]
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="kicker reveal">Plugin store</div>
    <h1 class="reveal d1">WordPress <span class="serif">plugins.</span></h1>
    <div class="page-hero-row"><p class="reveal d2">Premium WordPress plugins built from real client work: WooCommerce extensions, Contact Form 7 add-ons, shortcodes and sliders. They’re lightweight, secure and developer-friendly. Join the waitlist to get launch pricing.</p>
      <a href="mailto:{EMAIL}?subject=Plugin%20waitlist" class="btn btn-dark reveal d3">Join the waitlist {ARROW}</a></div>
  </div>
</section>
<section style="padding-bottom:clamp(80px,10vw,140px)">
  <div class="wrap"><div class="plugin-grid{"" if HAS_PLUGINS else " plugin-grid-2"}">{"".join(plugin_card(p) for p in PLUGINS) if HAS_PLUGINS else "".join(category_card(*c) for c in PLUGIN_CATEGORIES)}</div></div>
</section>"""
    lst = {"@type": "CollectionPage", "url": abs_url("/plugins/"), "name": "WordPress plugins",
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": abs_url(f"/plugins/{p['slug']}/"), "name": p["name"]}
               for i, p in enumerate(PLUGINS)]}}
    render("/plugins/", "Premium WordPress Plugins | Renie Namocot",
           "Lightweight, developer-friendly premium WordPress plugins: WooCommerce extensions, Contact Form 7 add-ons, shortcodes and sliders, by WordPress developer Renie Namocot.",
           body, schema=[lst, breadcrumbs_schema(trail)], active="/plugins/", priority="0.8")


def build_plugin(p):
    path = f"/plugins/{p['slug']}/"
    trail = [("Home", "/"), ("Plugins", "/plugins/"), (p["name"], path)]
    available = p["status"] == "available" and p.get("buy_url")
    if available:
        buy = f'<a href="{esc(p["buy_url"])}" class="btn btn-dark" rel="nofollow">Buy now · ${esc(p["price"])} {ARROW}</a>'
    else:
        buy = f'<a href="mailto:{EMAIL}?subject={esc(p["name"])}%20waitlist" class="btn btn-dark">Join the waitlist {ARROW}</a>'
    extra = ""
    if p.get("demo_url"):
        extra += f'<a href="{esc(p["demo_url"])}" class="btn btn-ghost" rel="nofollow">Live demo</a>'
    if p.get("docs_url"):
        extra += f'<a href="{esc(p["docs_url"])}" class="btn btn-ghost">Documentation</a>'
    feats = "".join(f'<div class="offer reveal"><span class="check" aria-hidden="true"></span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in p["features"])
    works = "".join(f'<span class="chip-ico">{icon(w, small=True)}{brand(w)}</span>' for w in p["works_with"])
    status = '<span class="pill pill-soon">Coming soon</span>' if not available else f'<span class="pill pill-live">${esc(p["price"])} / year</span>'
    others = "".join(plugin_card(o) for o in PLUGINS if o["slug"] != p["slug"])
    body = f"""<section class="page-hero svc-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="svc-hero-grid">
      <div>
        <div class="plugin-top reveal" style="justify-content:flex-start;gap:14px"><span class="plugin-icon">{icon(p['icon'])}</span>{status}</div>
        <h1 class="reveal d1">{esc(p['name'])}</h1>
        <p class="lead-answer reveal d2"><strong>{esc(p['tagline'])}</strong> {esc(p['desc'])}</p>
        <div class="works reveal d2"><span>Works with</span>{works}</div>
        <div class="hero-actions reveal d3" style="justify-content:flex-start">{buy}{extra}</div>
      </div>
      <div class="svc-hero-img reveal d2"><img src="{photo(p['img'], 1200)}" data-sizes="(max-width: 960px) 92vw, 46vw" alt="{esc(p['name'])}" fetchpriority="high"></div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Features</div><h2 class="h2 reveal d1">What’s <span class="serif">inside.</span></h2></div></div>
    <div class="offer-grid">{feats}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">More plugins</div><h2 class="h2 reveal d1">Explore <span class="serif">the store.</span></h2></div></div>
    <div class="plugin-grid">{others}</div>
  </div>
</section>"""
    app = {"@type": "SoftwareApplication", "name": p["name"], "description": p["desc"],
           "applicationCategory": "BusinessApplication", "operatingSystem": "WordPress",
           "url": abs_url(path), "image": photo(p["img"], 1200), "author": {"@id": PERSON_ID}}
    if available:
        app["offers"] = {"@type": "Offer", "price": p["price"], "priceCurrency": "USD",
                         "availability": "https://schema.org/InStock", "url": p["buy_url"]}
    render(path, f"{p['name']}: WordPress Plugin | {NAME}", p["desc"], body,
           schema=[app, breadcrumbs_schema(trail)], active="/plugins/", priority="0.7", image=photo(p["img"], 1200))


def build_blog_index():
    trail = [("Home", "/"), ("Blog", "/blog/")]
    posts = sorted(POSTS, key=lambda x: x["date"], reverse=True)
    lead, rest = posts[0], posts[1:]
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="kicker reveal">Blog</div>
    <h1 class="reveal d1">Notes on building <span class="serif">for the web.</span></h1>
    <div class="page-hero-row"><p class="reveal d2">Practical articles on WordPress, Shopify, headless development, e-commerce and SEO in the age of AI search.</p></div>
  </div>
</section>
<section style="padding-bottom:clamp(80px,10vw,140px)">
  <div class="wrap">
    <article class="post-lead reveal">
      <a href="/blog/{lead['slug']}/" class="post-media" tabindex="-1" aria-hidden="true"><img src="{photo(lead['img'], 1200)}" data-sizes="(max-width: 960px) 92vw, 56vw" alt="" fetchpriority="high"></a>
      <div>
        <div class="post-meta"><span class="pill">{esc(lead['category'])}</span><time datetime="{lead['date']}">{fmt_date(lead['date'])}</time><span>· {read_time(lead['body'])} min read</span></div>
        <h2><a class="stretched" href="/blog/{lead['slug']}/">{esc(lead['title'])}</a></h2>
        <p>{esc(lead['desc'])}</p>
        <span class="more">Read article {ARROW}</span>
      </div>
    </article>
    <div class="post-grid" style="margin-top:clamp(40px,5vw,64px)">{"".join(post_card(p, "h2") for p in rest)}</div>
  </div>
</section>"""
    blog = {"@type": "Blog", "url": abs_url("/blog/"), "name": f"{NAME}: Blog", "publisher": {"@id": PERSON_ID},
            "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": abs_url(f"/blog/{p['slug']}/"),
                          "datePublished": p["date"]} for p in posts]}
    render("/blog/", "Blog: WordPress, Shopify & SEO Insights | Renie Namocot",
           "Practical articles on WordPress development, Shopify, headless WordPress, WooCommerce, page builders and SEO for AI search in 2026.",
           body, schema=[blog, breadcrumbs_schema(trail)], active="/blog/", priority="0.8",
           lastmod=max(p.get("updated", p["date"]) for p in POSTS))


def build_post(p):
    path = f"/blog/{p['slug']}/"
    trail = [("Home", "/"), ("Blog", "/blog/"), (p["title"], path)]
    toc, n = [], [0]

    def add_id(m):
        text = m.group(1)
        sid = slugify(text)
        toc.append((sid, re.sub(r"<[^>]+>", "", text)))
        return f'<h2 id="{sid}">{text}</h2>'
    content = re.sub(r"<h2>(.*?)</h2>", add_id, p["body"])
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    updated = p.get("updated")
    upd = f' · Updated <time datetime="{updated}">{fmt_date(updated)}</time>' if updated and updated != p["date"] else ""
    services = "".join(
        f'<a class="side-link" href="/services/{s}/">{icon(SERVICE_BY_SLUG[s]["icons"][0], small=True)}{SERVICE_BY_SLUG[s]["name"]}</a>'
        for s in p["services"] if s in SERVICE_BY_SLUG)
    more = [x for x in sorted(POSTS, key=lambda x: x["date"], reverse=True) if x["slug"] != p["slug"]][:3]
    body = f"""<article class="article">
  <header class="article-head">
    <div class="wrap narrow">
      {breadcrumbs_html(trail)}
      <div class="post-meta"><span class="pill">{esc(p['category'])}</span><span>{read_time(p['body'])} min read</span></div>
      <h1>{esc(p['title'])}</h1>
      <p class="article-desc">{esc(p['desc'])}</p>
      <div class="byline">
        <img src="/assets/img/profile.webp" alt="{NAME}" width="44" height="44">
        <div><a href="/about/" rel="author"><strong>{NAME}</strong></a><span>{JOB} · <time datetime="{p['date']}">{fmt_date(p['date'])}</time>{upd}</span></div>
      </div>
    </div>
  </header>
  <div class="wrap">
    <figure class="article-hero"><img src="{photo(p['img'], 1800)}" data-sizes="(max-width: 1440px) 92vw, 1330px" alt="" fetchpriority="high"></figure>
    <div class="article-grid">
      <div class="article-side">
        <nav class="toc" aria-label="Table of contents"><h2 class="fh">On this page</h2><ol>{toc_html}</ol></nav>
        <div class="side-box"><h2 class="fh">Related services</h2>{services}</div>
      </div>
      <div class="prose">{content}
        <div class="author-box">
          <img src="/assets/img/profile.webp" alt="{NAME}" width="72" height="72" loading="lazy">
          <div><h2 class="fh">About the author</h2><p><strong>{NAME}</strong> is a full-stack web developer from the {LOCATION} who specialises in WordPress, Shopify and custom web applications. Renie has built sites and apps for clients across Australia, the US, UK, Germany, New Zealand and Singapore. <a href="/about/">More about Renie →</a></p></div>
        </div>
      </div>
    </div>
  </div>
</article>
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><div class="kicker reveal">Keep reading</div><h2 class="h2 reveal d1">More <span class="serif">articles.</span></h2></div><a href="/blog/" class="link-arrow reveal">All articles →</a></div>
    <div class="post-grid">{"".join(post_card(x) for x in more)}</div>
  </div>
</section>"""
    posting = {"@type": "BlogPosting", "@id": abs_url(path) + "#article", "headline": p["title"],
               "description": p["desc"], "image": photo(p["img"], 1800), "datePublished": p["date"],
               "dateModified": p.get("updated", p["date"]), "author": {"@id": PERSON_ID},
               "publisher": {"@id": PERSON_ID}, "mainEntityOfPage": abs_url(path),
               "articleSection": p["category"], "wordCount": len(re.sub(r"<[^>]+>", " ", p["body"]).split()),
               "inLanguage": "en"}
    seo_title = p.get("seo_title") or p["title"]
    if len(seo_title) + len(NAME) + 3 <= 65:
        seo_title = f"{seo_title} | {NAME}"
    render(path, seo_title, p["desc"], body, schema=[posting, breadcrumbs_schema(trail)],
           active="/blog/", og_type="article", image=photo(p["img"], 1200), priority="0.7",
           lastmod=p.get("updated", p["date"]))


# ------------------------------------------------------------------ CONSENT + ANALYTICS
# Analytics only loads after the visitor accepts (the choice is remembered in localStorage as "rn-consent").
ANALYTICS_HEAD = "" if not GA4_ID else """<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
(function () {
  var c = null;
  try { c = localStorage.getItem("rn-consent"); } catch (e) {}
  gtag("consent", "default", {analytics_storage: c === "granted" ? "granted" : "denied",
    ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied"});
  window.rnLoadAnalytics = function () {
    if (window.rnAnalyticsLoaded) return;
    window.rnAnalyticsLoaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=__GA__";
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", "__GA__");
  };
  if (c === "granted") window.rnLoadAnalytics();
})();
</script>""".replace("__GA__", GA4_ID)

CONSENT_BANNER = "" if not GA4_ID else """<div class="consent" data-consent hidden role="region" aria-label="Cookie consent">
  <p><strong>Cookies?</strong> I’d like to use Google Analytics cookies to see which pages are useful. They’re only set if you accept. <a href="/privacy/#cookies-and-similar-technologies">Privacy policy</a></p>
  <div class="consent-actions">
    <button type="button" class="btn btn-ghost" data-consent-choice="denied">Reject</button>
    <button type="button" class="btn btn-dark" data-consent-choice="granted">Accept</button>
  </div>
</div>"""


def legal_text(html):
    if GA4_ID:
        analytics = ("<h2>Analytics (only with your consent)</h2>\n"
                     "<p>If you click <strong>Accept</strong> on the cookie banner, this site uses <strong>Google Analytics 4</strong> "
                     "to understand which pages are visited, how people find the site and roughly where visitors come from. "
                     "Google Analytics sets cookies and collects data such as pages viewed, device and browser type, and approximate location. "
                     "Google Analytics 4 doesn’t log or store IP addresses. If you click <strong>Reject</strong>, or don’t choose, Google Analytics "
                     "isn’t loaded at all. You can change your choice any time using <strong>Cookie settings</strong> at the bottom of every page.</p>\n"
                     "<p><strong>Legal basis:</strong> your consent.</p>")
        short = "Google Analytics is only used if you accept cookies."
        cookies = ("<p>This site only sets cookies if you accept analytics:</p>\n<table>\n"
                   "<thead><tr><th>Name</th><th>Provider</th><th>Purpose</th><th>Expires</th></tr></thead>\n<tbody>\n"
                   "<tr><td><code>_ga</code></td><td>Google Analytics</td><td>Distinguishes visitors</td><td>2 years</td></tr>\n"
                   "<tr><td><code>_ga_*</code></td><td>Google Analytics</td><td>Keeps track of a visit</td><td>2 years</td></tr>\n"
                   "</tbody>\n</table>\n"
                   "<p>Your choice is saved in your browser’s local storage as <code>rn-consent</code> so the banner doesn’t appear on every page. "
                   "The visitor counter uses session storage, which is cleared when you close the tab. "
                   "To change your choice, use <strong>Cookie settings</strong> in the footer, or clear this site’s data in your browser.</p>")
        processor = "<li><strong>Google (Google Analytics)</strong>, only if you accept analytics cookies.</li>"
    else:
        analytics = ("<h2>Analytics</h2>\n<p>This website doesn’t use Google Analytics or any other third-party analytics or "
                     "advertising trackers. The only statistic collected is the visitor counter described above.</p>")
        short = "This site doesn’t use cookies or third-party analytics."
        cookies = ("<p><strong>This website doesn’t use cookies.</strong> That’s why you don’t see a cookie banner. "
                   "The visitor counter uses your browser’s session storage, which never leaves your device "
                   "and is cleared when you close the tab. If analytics is added in the future, it will only run after you "
                   "agree to it, and this policy will be updated.</p>")
        processor = ""
    for k, v in {"[[ANALYTICS_SHORT]]": short, "[[ANALYTICS_PROCESSOR]]": processor, "[[ANALYTICS]]": analytics,
                 "[[COOKIES]]": cookies, "[[NAME]]": NAME, "[[EMAIL]]": EMAIL,
                 "[[SITE]]": SITE_URL.split("//", 1)[-1], "[[LOCATION]]": LOCATION}.items():
        html = html.replace(k, v)
    # give each h2 an id so sections can be linked (e.g. /privacy/#cookies-and-similar-technologies)
    return re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h2 id="{slugify(m.group(1))}">{m.group(1)}</h2>', html)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")


def build_legal(path, kicker, h1, title, desc, html):
    trail = [("Home", "/"), (kicker, path)]
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="kicker reveal">{kicker}</div>
    <h1 class="reveal d1">{h1}</h1>
    <div class="page-hero-row"><p class="reveal d2">Last updated <time datetime="{LEGAL_UPDATED}">{fmt_date(LEGAL_UPDATED)}</time></p></div>
  </div>
</section>
<section style="padding-bottom:clamp(80px,10vw,140px)">
  <div class="wrap"><div class="prose legal-prose">{legal_text(html)}</div></div>
</section>"""
    page = {"@type": "WebPage", "url": abs_url(path), "name": title, "dateModified": LEGAL_UPDATED}
    render(path, title, desc, body, schema=[page, breadcrumbs_schema(trail)], with_cta=False,
           priority="0.3", lastmod=LEGAL_UPDATED)


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact/")]
    options = "".join(f'<option value="{esc(s["name"])}" data-slug="{s["slug"]}">{esc(s["name"])}</option>' for s in SERVICES)
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="contact-grid">
      <div>
        <div class="kicker reveal">Contact</div>
        <h1 class="reveal d1">Let’s build <span class="serif">something good.</span></h1>
        <p class="reveal d2" style="color:var(--muted);font-size:18px;max-width:480px">Tell me a little about your project and I’ll reply within 24 hours with next steps. I work remotely with clients worldwide.</p>
        <a href="mailto:{EMAIL}" class="contact-email reveal d2">{EMAIL}</a>
        <ul class="contact-points reveal d3">
          <li><strong>Based in</strong><span>{LOCATION} · remote, worldwide</span></li>
          <li><strong>Clients in</strong><span>{", ".join(COUNTRIES)}</span></li>
          <li><strong>Experience</strong><span>1,000+ websites built (most under NDA)</span></li>
          <li><strong>Response time</strong><span>Usually within 24 hours</span></li>
        </ul>
      </div>
      <form class="contact-form reveal d2" data-mailto="{EMAIL}">
        <div class="field-row">
          <label>Name<input name="name" required autocomplete="name"></label>
          <label>Email<input name="email" type="email" required autocomplete="email"></label>
        </div>
        <label>Service<select name="service"><option value="">Choose a service…</option>{options}{'<option>Plugin purchase / licence</option>' if HAS_PLUGINS else ''}<option>Something else</option></select></label>
        <label>Budget<select name="budget"><option value="">Select a range…</option><option>Under $1,000</option><option>$1,000 – $3,000</option><option>$3,000 – $7,500</option><option>$7,500+</option><option>Not sure yet</option></select></label>
        <label>Project details<textarea name="message" rows="6" required placeholder="Goals, timeline, links to your current site or designs…"></textarea></label>
        <button class="btn btn-dark" type="submit">Send message {ARROW}</button>
        <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <p class="form-note">Your message goes straight to my inbox. I reply within 24 hours. See the <a class="ulink" href="/privacy/">privacy policy</a> for how your details are handled.</p>
      </form>
    </div>
  </div>
</section>"""
    contact = {"@type": "ContactPage", "url": abs_url("/contact/"), "name": f"Contact {NAME}", "about": {"@id": PERSON_ID}}
    render("/contact/", f"Contact {NAME}: Hire a WordPress & Shopify Developer",
           f"Get in touch with {NAME} about WordPress, Shopify, WooCommerce, headless or custom web development projects. Replies within 24 hours.",
           body, schema=[contact, BUSINESS, breadcrumbs_schema(trail)], active="/contact/", with_cta=False, priority="0.8")


def build_404():
    popular = "".join(
        f'<a class="nf-link" href="/services/{x["slug"]}/">{icon(x["icons"][0], small=True)}<span>{esc(x["name"])}</span>{ARROW}</a>'
        for x in SERVICES[:8])
    latest = "".join(
        f'<a class="nf-link" href="/blog/{x["slug"]}/"><span>{esc(x["title"])}</span>{ARROW}</a>'
        for x in sorted(POSTS, key=lambda x: x["date"], reverse=True)[:4])
    body = f"""<section class="page-hero nf">
  <div class="wrap">
    <div class="nf-grid">
      <div>
        <div class="nf-code" aria-hidden="true">4<span>0</span>4</div>
        <h1>This page took a <span class="serif">wrong turn.</span></h1>
        <p class="nf-lead">The page you’re looking for may have moved, been renamed, or never existed. Here are some good places to go instead.</p>
        <div class="hero-actions" style="justify-content:flex-start">
          <a href="/" class="btn btn-dark">Back to home {ARROW}</a>
          <a href="/projects/" class="btn btn-ghost">See my work</a>
          <a href="/contact/" class="btn btn-ghost">Contact me</a>
        </div>
      </div>
      <div class="nf-cols">
        <div class="nf-box"><h2 class="fh">Popular services</h2>{popular}<a class="link-arrow" href="/services/" style="margin-top:14px;display:inline-block">All services →</a></div>
        <div class="nf-box"><h2 class="fh">Latest articles</h2>{latest}<a class="link-arrow" href="/sitemap/" style="margin-top:14px;display:inline-block">Full sitemap →</a></div>
      </div>
    </div>
  </div>
</section>"""
    render("/404.html", f"Page not found (404) | {NAME}", "Sorry, this page could not be found.", body, noindex=True, with_cta=False)


def build_html_sitemap():
    trail = [("Home", "/"), ("Sitemap", "/sitemap/")]
    group = lambda title, links: (f'<div class="sm-group reveal"><h2>{title}</h2><ul>'
                                  + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in links) + "</ul></div>")
    body = f"""<section class="page-hero">
  <div class="wrap">
    {breadcrumbs_html(trail)}
    <div class="kicker reveal">Sitemap</div>
    <h1 class="reveal d1">Every page, <span class="serif">in one place.</span></h1>
    <div class="sm-grid">
      {group("Main pages", [("Home", "/"), ("About", "/about/"), ("Services", "/services/"), ("Projects", "/projects/")] + ([("Plugins", "/plugins/")] if STORE_ON else []) + [("Blog", "/blog/"), ("Contact", "/contact/"), ("Privacy policy", "/privacy/"), ("Terms of use", "/terms/")])}
      {group("Services", [(x["name"], f"/services/{x['slug']}/") for x in SERVICES])}
      {group("Blog", [(x["title"], f"/blog/{x['slug']}/") for x in sorted(POSTS, key=lambda x: x["date"], reverse=True)])}
      {group("Plugins", [(x["name"], f"/plugins/{x['slug']}/") for x in PLUGINS]) if HAS_PLUGINS else ""}
      {group("Projects by platform", [(c["name"], f"/projects/#{c['key']}") for c in CATEGORIES if c["key"] != "all"])}
      {group("For machines", [("XML sitemap", "/sitemap.xml"), ("RSS feed", "/blog/rss.xml"), ("llms.txt", "/llms.txt"), ("robots.txt", "/robots.txt")])}
    </div>
  </div>
</section>"""
    render("/sitemap/", f"Sitemap | {NAME}", f"A complete list of pages on {NAME}'s website: services, projects, plugins and blog articles.",
           body, schema=[breadcrumbs_schema(trail)], priority="0.3")


# ------------------------------------------------------------------ SEO FILES
HTACCESS = r"""# Apache config (cPanel / Hostinger / most shared hosting). Ignored by other servers.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
  RewriteEngine On
  # Force HTTPS
  RewriteCond %{HTTPS} off
  RewriteCond %{HTTP:X-Forwarded-Proto} !https
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  # One canonical host (no www) - must match SITE_URL in build.py
  RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
  RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
  # Add trailing slash to folder URLs (/about -> /about/)
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^(.*[^/])$ /$1/ [L,R=301]
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript text/xml application/xml application/rss+xml text/plain image/svg+xml application/ld+json
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
</IfModule>

AddType image/webp .webp
AddType image/svg+xml .svg
AddType text/plain .txt
"""


def build_seo_files():
    host = SITE_URL.split("://", 1)[1]
    htaccess = HTACCESS
    if host.startswith("www."):  # canonical host is www: redirect bare domain -> www instead
        htaccess = htaccess.replace(
            "  # One canonical host (no www) - must match SITE_URL in build.py\n  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]\n  RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]",
            "  # One canonical host (www) - must match SITE_URL in build.py\n  RewriteCond %{HTTP_HOST} !^www\\. [NC]\n  RewriteRule ^ https://www.%{HTTP_HOST}%{REQUEST_URI} [L,R=301]")
    (OUT / ".htaccess").write_text(htaccess, encoding="utf-8")

    def url_entry(u, m, p, imgs, title):
        im = "".join(f"\n    <image:image><image:loc>{abs_url(i)}</image:loc></image:image>" for i in imgs)
        return f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{m}</lastmod>\n    <priority>{p}</priority>{im}\n  </url>"
    urls = "\n".join(url_entry(*e) for e in SITEMAP)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        f'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{urls}\n</urlset>\n', encoding="utf-8")
    build_extras()

    ai_bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot",
               "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "DuckAssistBot"]
    robots = ("# robots.txt for " + SITE_URL + "\n"
              "# Search engines and AI assistants are welcome to crawl and cite this site.\n\n"
              "User-agent: *\nAllow: /\nDisallow: /404.html\nDisallow: /api/\nDisallow: /*?*service=\n\n")
    robots += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ai_bots)
    robots += f"Sitemap: {SITE_URL}/sitemap.xml\n"
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")

    svc = "\n".join(f"- [{s['name']}]({abs_url('/services/' + s['slug'] + '/')}): {s['desc']}" for s in SERVICES)
    posts = "\n".join(f"- [{p['title']}]({abs_url('/blog/' + p['slug'] + '/')}): {p['desc']}" for p in POSTS)
    plugins = "\n".join(f"- [{p['name']}]({abs_url('/plugins/' + p['slug'] + '/')}): {p['desc']}" for p in PLUGINS)
    llms = f"""# {NAME}

> {NAME} is a freelance full-stack web developer based in the {LOCATION}, specialising in WordPress (custom themes, plugins, headless WordPress with Next.js, Elementor, Divi, ACF, WooCommerce) and Shopify (custom Online Store 2.0 themes, Shopify Admin/Storefront REST & GraphQL APIs, Hydrogen). Renie has built more than 1,000 websites (most under NDA for agencies and brands), and also builds Stripe/PayPal payment integrations, online booking systems, business automations (Zapier, Make, n8n), Figma-to-WordPress conversions and custom web apps (Laravel, React, Node.js). Renie also built and runs two SaaS products: tarsiflow (https://tarsiflow.com/, client management for freelancers and agencies) and MyTindahan (https://mytindahan.store/, a store app for sari-sari and grocery stores in the Philippines with 1,500+ sign-ups). Clients across {", ".join(COUNTRIES)}. Contact: {EMAIL}

## Key pages
- [Home]({SITE_URL}/)
- [About]({abs_url('/about/')})
- [Services]({abs_url('/services/')})
- [Projects]({abs_url('/projects/')})
{"- [Plugins](" + abs_url('/plugins/') + ")" + chr(10) if STORE_ON else ""}- [Blog]({abs_url('/blog/')})
- [Contact]({abs_url('/contact/')})

## Services
{svc}

{("## Plugins" + chr(10) + plugins + chr(10) + chr(10)) if HAS_PLUGINS else ""}## Articles
{posts}
"""
    (OUT / "llms.txt").write_text(llms, encoding="utf-8")

    items = "".join(f"""<item><title>{esc(p['title'])}</title><link>{abs_url('/blog/' + p['slug'] + '/')}</link><guid>{abs_url('/blog/' + p['slug'] + '/')}</guid><pubDate>{date.fromisoformat(p['date']).strftime('%a, %d %b %Y')} 00:00:00 +0000</pubDate><description>{esc(p['desc'])}</description></item>"""
                    for p in sorted(POSTS, key=lambda x: x["date"], reverse=True))
    (OUT / "blog").mkdir(parents=True, exist_ok=True)
    (OUT / "blog" / "rss.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{NAME}: Blog</title><link>{abs_url("/blog/")}</link><description>WordPress, Shopify and SEO insights</description><language>en</language>{items}</channel></rss>',
        encoding="utf-8")


def build_extras():
    from PIL import Image, ImageDraw
    # --- app icons rendered from the RN mark (supersampled for smooth edges)
    def mark(size, pad=0.0, bg_square=False):
        k = 16
        S = 40 * k
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if bg_square:
            d.rectangle((0, 0, S, S), fill="#0B0B0C")
        else:
            d.rounded_rectangle((0, 0, S - 1, S - 1), 11 * k, fill="#0B0B0C")
        sc = (1 - pad * 2)
        off = pad * S
        P = lambda x, y: (off + x * k * sc, off + y * k * sc)
        sw = int(3.4 * k * sc)
        for seg in ([(8.5, 31), (8.5, 9), (15, 9)], [(15, 19), (11.5, 19), (26, 31), (26, 9)]):
            d.line([P(*pt) for pt in seg], fill="white", width=sw, joint="curve")
            for pt in (seg[0], seg[-1]):
                x, y = P(*pt)
                d.ellipse((x - sw / 2, y - sw / 2, x + sw / 2, y + sw / 2), fill="white")
        x0, y0 = P(10, 9)
        x1, y1 = P(20, 19)
        d.arc((x0 - sw / 2, y0 - sw / 2, x1 + sw / 2, y1 + sw / 2), -90, 90, fill="white", width=sw)
        cx, cy = P(31, 30.6)
        r = 2.3 * k * sc
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#4F6BFF")
        return im.resize((size, size), Image.LANCZOS)

    app = ASSETS / "img" / "icons-app"
    app.mkdir(parents=True, exist_ok=True)
    for n in (48, 192, 512):
        mark(n).save(app / f"icon-{n}.png", optimize=True)
    mark(512, pad=0.1, bg_square=True).save(app / "icon-maskable-512.png", optimize=True)
    mark(180, pad=0.06, bg_square=True).convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)
    mark(48).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    manifest = {
        "name": f"{NAME}: {TAGLINE}", "short_name": NAME, "description": f"{JOB}: WordPress, Shopify and custom web development.",
        "start_url": "/", "scope": "/", "display": "standalone", "background_color": "#F6F6F3", "theme_color": "#0B0B0C",
        "icons": [
            {"src": "/assets/img/icons-app/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/img/icons-app/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/assets/img/icons-app/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    (OUT / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # --- IndexNow key file + list of URLs to submit
    if INDEXNOW_KEY:
        (OUT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")

    # --- security.txt (RFC 9116)
    wk = OUT / ".well-known"
    wk.mkdir(exist_ok=True)
    expires = date(date.today().year + 1, date.today().month, 1).isoformat()
    (wk / "security.txt").write_text(
        f"Contact: mailto:{EMAIL}\nExpires: {expires}T00:00:00.000Z\nPreferred-Languages: en\nCanonical: {SITE_URL}/.well-known/security.txt\n",
        encoding="utf-8")

    # --- llms-full.txt: the full text of key pages, for AI assistants
    strip = lambda h: re.sub(r"\n{3,}", "\n\n", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
    parts = [f"# {NAME}: full content\n\n> {JOB} ({TAGLINE}) based in the {LOCATION}. Contact: {EMAIL}. Website: {SITE_URL}/\n"]
    for x in SERVICES:
        faqs = "\n".join(f"Q: {q}\nA: {a}" for q, a in x["faqs"])
        offers = "\n".join(f"- {t}: {d}" for t, d in x["offers"])
        parts.append(f"## {x['name']}\nURL: {abs_url('/services/' + x['slug'] + '/')}\n\n{x['lead']}\n\n{offers}\n\n{strip(x['body'])}\n\n{faqs}\n")
    for x in sorted(POSTS, key=lambda x: x["date"], reverse=True):
        parts.append(f"## {x['title']}\nURL: {abs_url('/blog/' + x['slug'] + '/')}\nPublished: {x['date']}\n\n{strip(x['body'])}\n")
    parts.append("## Projects\n" + "\n".join(f"- {x['title']} ({x['label']}): {x['summary']} {x.get('url', '')}" for x in PROJECTS))
    (OUT / "llms-full.txt").write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def submit_indexnow():
    """POST every sitemap URL to IndexNow (Bing, Yandex, Seznam, Naver...). Run AFTER uploading the site."""
    import urllib.request
    host = SITE_URL.split("://", 1)[1]
    payload = json.dumps({"host": host, "key": INDEXNOW_KEY, "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
                          "urlList": [u for u, *_ in SITEMAP]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: submitted {len(SITEMAP)} URLs -> HTTP {r.status} (200/202 = accepted)")


# ------------------------------------------------------------------ MAIN
def main():
    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():  # clear contents (keeps the folder, so a running preview server is fine)
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    for p in PROJECTS:  # pre-cache every icon the project modal can show
        for s in p["stack"]:
            icon(s)
    build_home()
    build_about()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_projects()
    if STORE_ON:
        build_plugins()
    for p in PLUGINS:
        build_plugin(p)
    build_blog_index()
    for p in POSTS:
        build_post(p)
    build_contact()
    build_legal("/privacy/", "Privacy", 'Privacy &amp; <span class="serif">cookies.</span>', f"Privacy & Cookie Policy | {NAME}",
                f"How {NAME}'s website handles your personal data: contact messages, the visitor counter, cookies and your privacy rights.", PRIVACY)
    build_legal("/terms/", "Terms", 'Terms of <span class="serif">use.</span>', f"Terms of Use | {NAME}",
                f"Terms for using {NAME}'s website, articles and content, plus how project work and plugin licences are covered.", TERMS)
    build_404()
    build_html_sitemap()
    build_seo_files()
    shutil.copytree(ROOT / "assets", OUT / "assets")  # copied last so newly downloaded files are included
    shutil.copytree(SRC / "api", OUT / "api")  # PHP visitor counter (runs on Hostinger/cPanel)
    (OUT / "api" / "data").mkdir(exist_ok=True)
    (OUT / "api" / "data" / ".htaccess").write_text("Require all denied\n", encoding="utf-8")
    print(f"Built {len(SITEMAP)} indexable pages into {OUT}")
    if "--indexnow" in sys.argv:
        submit_indexnow()
    if "--serve" in sys.argv:
        import functools, http.server, socketserver
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        with socketserver.TCPServer(("", 5173), handler) as httpd:
            print("Serving on http://localhost:5173")
            httpd.serve_forever()


if __name__ == "__main__":
    main()
