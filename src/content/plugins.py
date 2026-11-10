"""Plugin store. Each entry becomes /plugins/<slug>/.

These are DRAFT concepts and are hidden from the site.
When a plugin is real, set "published": True and it appears everywhere
(nav, homepage, /plugins/, sitemap, llms.txt) on the next build.

  published  True to show this plugin on the site

  status     "coming-soon" (shows waitlist button) or "available" (shows price + buy button)
  price      e.g. "49"  (USD, per year). Used for Product schema only when status is "available"
  buy_url    checkout link from Freemius / Lemon Squeezy / Gumroad / your WooCommerce store
  demo_url   optional live demo link
  docs_url   optional documentation link
"""

PLUGINS = [
    {
        "slug": "rn-booking-pro",
        "name": "RN Booking Pro",
        "tagline": "Appointments and deposits for WordPress, without the bloat.",
        "desc": "A lightweight WordPress booking plugin with real-time availability, Stripe & PayPal deposits, reminders and Google Calendar sync.",
        "icon": "googlecalendar",
        "img": "photo-1600880292203-757bb62b4baf",
        "published": False,
        "status": "coming-soon",
        "price": "",
        "buy_url": "",
        "demo_url": "",
        "docs_url": "",
        "works_with": ["wordpress", "stripe", "paypal", "googlecalendar"],
        "features": [
            ("Real-time availability", "Staff, services and locations with buffers, breaks and holidays."),
            ("Deposits & full payments", "Take payment at booking through Stripe or PayPal."),
            ("Automated reminders", "Email and SMS confirmations and reminders to cut no-shows."),
            ("Calendar sync", "Two-way Google Calendar sync to prevent double bookings."),
            ("Block & shortcode", "Drop the booking form into Gutenberg, Elementor or Divi."),
            ("Developer hooks", "Actions, filters and REST endpoints for custom workflows."),
        ],
    },
    {
        "slug": "rn-stripe-checkout",
        "name": "RN Stripe Checkout",
        "tagline": "Sell services and subscriptions with Stripe, no store required.",
        "desc": "Accept one-off payments, subscriptions and deposits on any WordPress page with Stripe Checkout, Apple Pay and Google Pay. No WooCommerce needed.",
        "icon": "stripe",
        "img": "photo-1556742049-0cfed4f6a45d",
        "published": False,
        "status": "coming-soon",
        "price": "",
        "buy_url": "",
        "demo_url": "",
        "docs_url": "",
        "works_with": ["wordpress", "stripe", "elementor"],
        "features": [
            ("Payment buttons & forms", "Add a payment button or form to any page with a block."),
            ("Subscriptions", "Recurring plans, trials and a customer billing portal."),
            ("Wallets", "Apple Pay, Google Pay and Link out of the box."),
            ("Webhooks", "Verified webhooks to trigger emails, access and CRM updates."),
            ("Payment log", "See every payment and its status inside WordPress."),
            ("Automation-ready", "Send events to Zapier, Make or n8n."),
        ],
    },
    {
        "slug": "rn-acf-blocks-kit",
        "name": "RN ACF Blocks Kit",
        "tagline": "Production-ready ACF blocks for faster custom builds.",
        "desc": "A library of clean, accessible ACF Pro Gutenberg blocks such as heroes, features, pricing, FAQs with schema and testimonials, ready to style to any brand.",
        "icon": "acf",
        "img": "photo-1504384308090-c894fdcc538d",
        "published": False,
        "status": "coming-soon",
        "price": "",
        "buy_url": "",
        "demo_url": "",
        "docs_url": "",
        "works_with": ["wordpress", "acf", "tailwindcss"],
        "features": [
            ("20+ ACF blocks", "Heroes, features, pricing, logos, CTAs, FAQs and more."),
            ("FAQ schema built in", "FAQ blocks output valid FAQPage structured data."),
            ("theme.json aware", "Blocks inherit your theme's colours, fonts and spacing."),
            ("Accessible markup", "Semantic HTML and keyboard-friendly interactions."),
            ("Lightweight", "Assets load only on pages that use each block."),
            ("Developer-friendly", "Override any template from your theme."),
        ],
    },
]
