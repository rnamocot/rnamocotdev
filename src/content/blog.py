"""Blog posts. Each entry becomes /blog/<slug>/.

To add a post: copy an entry, change the slug/title/desc/date, and write the
body as HTML. Use <h2> for main sections (they feed the table of contents).
`services` links the post to relevant service pages (internal linking).
"""

POSTS = [
    {
        "slug": "mytindahan-sari-sari-store-app",
        "seo_title": "MyTindahan: A Store App for Sari-Sari Stores",
        "title": "Building MyTindahan: A Simple Store App for Sari-Sari, Grocery and Convenience Stores",
        "desc": "Why I built MyTindahan, a phone-friendly back-office app for Philippine store owners that tracks inventory, sales, utang, GCash and e-load, and keeps selling when the internet drops.",
        "date": "2026-11-10",
        "category": "Case study",
        "img": "/assets/img/work/mytindahan-store-1200.webp",
        "services": ["custom-web-development", "web-design"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> <a href="https://www.mytindahan.store/" rel="noopener">MyTindahan</a> is a store app I built for sari-sari, grocery and convenience store owners in the Philippines. It replaces the notebook: inventory with low-stock and expiry alerts, sales, utang (customer credit), GCash cash-in and cash-out, and e-load, all on a phone, tablet or laptop. Sales keep working offline. There’s a free plan, and paid plans start at ₱1,500 a year, paid through GCash.</p>

<h2>The problem: the store notebook</h2>
<p>Most small stores in the Philippines still run on a notebook, a calculator and memory. That works until it doesn’t:</p>
<ul>
<li>You don’t know which products are about to run out until a customer asks for them.</li>
<li>Expired stock gets found too late and becomes a loss.</li>
<li>The utang list is scattered across pages, and nobody is sure who still owes what.</li>
<li>GCash and e-load cash gets mixed with sales money, so the till never quite matches.</li>
<li>When the owner is away, there’s no way to see how the store is doing.</li>
</ul>
<p>Store owners don’t need a big point-of-sale system with hardware and training. They need the notebook, made smarter, on the phone they already have. That’s the idea behind MyTindahan’s tagline: <em>“Alam mo ang benta, utang at stock. Kahit nasaan ka.”</em> (Know your sales, credit and stock, wherever you are.)</p>

<h2>What MyTindahan does</h2>
<ul>
<li><strong>Inventory:</strong> stock tracked by batch, with low-stock and expiry alerts and a list of your fastest-moving products.</li>
<li><strong>Sales:</strong> check out by cash, GCash or utang, with per-item sales reports.</li>
<li><strong>Utang:</strong> a running tab for each customer, with every payment logged.</li>
<li><strong>GCash:</strong> log cash-ins and cash-outs, track your e-wallet float and your fees.</li>
<li><strong>E-load:</strong> prepaid load sales for Globe, TM, GOMO, Smart, TNT and DITO, in their own ledger.</li>
<li><strong>Services:</strong> barbershops and talyers can sell services like haircuts or repairs next to products.</li>
<li><strong>Dashboard:</strong> today’s sales, total utang, GCash float, a 7-day sales chart, and items that are low or about to expire, on one screen.</li>
</ul>
<p>Bigger stores can add bills, staff salaries, a cash vault, a barcode scanner using the phone camera, 3,000+ ready-made product photos, separate staff logins, and delivery-truck inventory.</p>

<h2>Design decisions that mattered</h2>
<h3>A ledger, not a cash register</h3>
<p>MyTindahan is deliberately a <strong>back-office tool</strong>, not a POS terminal. It doesn’t issue official receipts, and owners keep using their own BIR-registered receipts. Keeping it a ledger means no hardware, no setup visit and no training. Owners can start in minutes.</p>
<h3>Works when the signal doesn’t</h3>
<p>Mobile data in many neighbourhoods is unreliable. Losing a sale because the internet dropped isn’t acceptable, so <strong>sales are saved on the device when offline and sync when the connection returns</strong>. Everything else (inventory, utang and GCash) needs a connection, which keeps the data consistent across devices and staff.</p>
<h3>Phone first, no app store needed</h3>
<p>It runs in the browser on any phone, tablet or laptop and can be installed to the home screen like an app. There’s nothing to download from an app store, and updates reach everyone instantly. It’s built with Next.js and React.</p>
<h3>Owners see everything, staff see what they need</h3>
<p>With staff accounts, cashiers get their own logins and can sell, while the owner keeps profit, costs and reports private. That matters for owners who can’t be at the store all day.</p>
<h3>Pricing that fits a sari-sari store</h3>
<p>Credit cards aren’t common for small store owners, so plans are <strong>paid yearly through GCash</strong>, and prices are shown per day so they make sense next to daily sales:</p>
<table>
<thead><tr><th>Plan</th><th>Price</th><th>Best for</th></tr></thead>
<tbody>
<tr><td>Starter</td><td>Free</td><td>Trying it out, up to 10 products</td></tr>
<tr><td>Growth</td><td>₱1,500/year (about ₱5/day)</td><td>Most sari-sari stores, up to 300 products, bills, payroll and cash vault</td></tr>
<tr><td>Pro</td><td>₱6,000/year (about ₱17/day)</td><td>Bigger stores, unlimited products, 3 staff logins</td></tr>
<tr><td>Business</td><td>₱15,000/year (about ₱42/day)</td><td>Stores with delivery trucks, 5 staff logins</td></tr>
</tbody>
</table>
<p>Every new store gets a free 7-day Growth trial, no credit card needed. Prices are correct at the time of writing. Check the <a href="https://www.mytindahan.store/" rel="noopener">MyTindahan website</a> for current plans.</p>

<h2>Who uses it</h2>
<p>More than 1,500 store owners have signed up, from sari-sari stores and small groceries to convenience stores, barbershops and talyers across Luzon, the Visayas and Mindanao.</p>

<h2>What I learned building it</h2>
<ul>
<li><strong>Talk the owner’s language.</strong> Words like utang, float and e-load matter more than accounting terms.</li>
<li><strong>Fewer features, used every day,</strong> beat many features nobody opens. The dashboard answers the three questions owners ask most: how much did I sell, who owes me, and what do I need to restock?</li>
<li><strong>Offline isn’t optional</strong> for small businesses in the Philippines. Design for a weak connection from day one.</li>
<li><strong>Local payment methods matter.</strong> Many small store owners don’t have credit cards, so subscriptions are paid with GCash.</li>
</ul>

<h2>Want an app like this for your business?</h2>
<p>MyTindahan started from a simple, everyday problem. If your business runs on spreadsheets, notebooks or group chats, a focused <a href="/services/custom-web-development/">custom web app</a> can save hours every week. <a href="/contact/">Tell me how your business works</a> and I’ll suggest what to build first.</p>
""",
    },
    {
        "slug": "tarsiflow-client-management-for-freelancers",
        "seo_title": "TarsiFlow: Client Management for Freelancers",
        "title": "Building TarsiFlow: Client Management for Freelancers and Agencies, From Lead to Paid Invoice",
        "desc": "Why I built TarsiFlow, a client management workspace that connects leads, clients, projects, proposals and invoices, so freelancers and agencies stop juggling five tools.",
        "date": "2026-11-10",
        "category": "Case study",
        "img": "/assets/img/work/tarsiflow-com-1200.webp",
        "services": ["custom-web-development", "stripe-paypal-payment-integration"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> <a href="https://tarsiflow.com/" rel="noopener">TarsiFlow</a> is a client management workspace I built for freelancers, agencies and consultants. Leads, clients, projects, proposals, meetings and invoices live in one place and are connected: a won lead becomes a client and a project, and an accepted proposal becomes an invoice. It’s built with Laravel, Livewire, Tailwind CSS and MySQL, and there’s a 14-day free trial with no card required.</p>

<h2>The problem: five tools for one client</h2>
<p>As a freelancer, one client can easily touch five different tools: a spreadsheet for leads, a document for the proposal, a task app for the project, a calendar for meetings, and an invoicing tool for getting paid. Every hand-off between them is manual:</p>
<ul>
<li>Client details get copied from one tool to the next, with mistakes along the way.</li>
<li>Meeting action items stay in notes and never become tasks.</li>
<li>An accepted proposal still has to be typed up again as an invoice.</li>
<li>Overdue invoices are noticed weeks late, if at all.</li>
<li>There’s no single page that shows everything about a client.</li>
</ul>
<p>TarsiFlow’s promise is in its headline: <em>win clients, deliver work and get paid in one flow.</em></p>

<h2>What TarsiFlow does</h2>
<ul>
<li><strong>Leads pipeline:</strong> a visual pipeline from first enquiry to signed deal.</li>
<li><strong>Clients and contacts:</strong> one page per client with contacts, projects, proposals, invoices, notes and an activity timeline.</li>
<li><strong>Proposals:</strong> templates with pricing tables and online acceptance.</li>
<li><strong>Projects and tasks:</strong> lists, boards, subtasks, comments and a “My tasks” view.</li>
<li><strong>Meetings and notes:</strong> agendas, rich notes and action items on a shared calendar.</li>
<li><strong>Invoices and payments:</strong> branded PDF invoices, payment tracking and overdue alerts.</li>
</ul>

<h2>Automations: the part that saves the most time</h2>
<p>The modules are useful on their own, but the real value is in how they connect. TarsiFlow handles the boring hand-offs automatically:</p>
<ol>
<li>When a lead is marked as won, a <strong>client and a project are created</strong>.</li>
<li>When a client accepts a proposal online, the <strong>acceptance details are recorded</strong>, and the proposal can be turned into an invoice.</li>
<li>When a payment is recorded, the <strong>invoice is marked paid</strong>.</li>
<li>Meeting <strong>action items become tasks</strong>.</li>
<li>People are <strong>notified</strong> when tasks are assigned to them.</li>
<li>A daily check <strong>flags overdue invoices</strong>.</li>
</ol>
<p>None of these are flashy, but together they remove most of the copy-and-paste work between winning a client and getting paid.</p>

<h2>Design decisions that mattered</h2>
<h3>One flow, not a bundle of apps</h3>
<p>Many tools offer CRM, projects and invoicing as separate modules that barely talk to each other. In TarsiFlow, every record links to the client, so the client page is a complete history: what was proposed, what was agreed, what was delivered and what’s still unpaid.</p>
<h3>Laravel and Livewire</h3>
<p>TarsiFlow is built with <strong>Laravel, Livewire, Tailwind CSS and MySQL</strong>. Livewire gives the interface a fast, app-like feel while keeping the business logic on the server, and Laravel handles the background work, like the daily overdue-invoice check.</p>
<h3>Security from the start</h3>
<p>Client data is sensitive, so the basics are built in: HTTPS everywhere, two-factor sign-in with authenticator apps, isolated workspaces that only your team can see, team roles, full data export and workspace deletion, and a public status page. Payments go through PayPal, so <strong>card numbers never touch TarsiFlow’s servers</strong>.</p>
<h3>Built for more than one country</h3>
<p>TarsiFlow is available in <strong>English, Filipino, Spanish, French and German</strong>, and can be installed as an app from the browser.</p>

<h2>Who it’s for</h2>
<p>Anyone who sells their time: solo freelancers, design studios, marketing agencies and consultancies. That includes web designers and developers, copywriters, photographers and SEO specialists. If you send proposals and invoices, it’s built for you.</p>

<h2>What I learned building it</h2>
<ul>
<li><strong>Connect the steps, not just the data.</strong> The most useful features are the ones that move a client from one stage to the next without retyping anything.</li>
<li><strong>Automations beat features.</strong> Users don’t notice another screen. They notice when they no longer have to retype an invoice.</li>
<li><strong>Trust is a feature.</strong> Two-factor sign-in, data export and a status page matter to people handing over their client list.</li>
</ul>

<h2>Need a custom system for your business?</h2>
<p>TarsiFlow is a good example of what a focused <a href="/services/custom-web-development/">custom web app</a> can do: take a messy, multi-tool process and turn it into one flow. If you need something similar, from client portals to <a href="/services/stripe-paypal-payment-integration/">payment integrations</a>, <a href="/contact/">let’s talk</a>. You can also <a href="https://tarsiflow.com/" rel="noopener">try TarsiFlow free for 14 days</a>.</p>
""",
    },
    {
        "slug": "claude-vs-codex-for-web-development",
        "seo_title": "Claude Code vs Codex for Web Development (2026)",
        "title": "Claude Code vs OpenAI Codex: Which AI Coding Agent Is Better for Web Development?",
        "desc": "A practical comparison of Claude Code and OpenAI Codex for WordPress, WooCommerce, Shopify and custom web development: workflow, context, safety, cost and when to use each.",
        "date": "2026-11-10",
        "category": "AI",
        "img": "photo-1515879218367-8466d910aaa4",
        "services": ["wordpress-plugin-development", "custom-web-development", "woocommerce-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> Both are capable AI coding agents, and the gap between them changes with every model release. Claude Code works best as a hands-on pair programmer in your terminal or editor, especially for multi-file changes in an existing codebase. Codex is strongest when you want to hand off well-defined tasks to run in the cloud in parallel and come back to a pull request. Many developers use both. Whichever you pick, the quality of your instructions, tests and code review matters more than the tool.</p>

<h2>What are Claude Code and Codex?</h2>
<p>They’re no longer just autocomplete. Both are <strong>coding agents</strong>: you describe a task in plain language, and the agent reads your files, plans changes, edits code, runs commands and tests, and reports back.</p>
<ul>
<li><strong>Claude Code</strong> is Anthropic’s agent. It started as a terminal tool and now also runs in VS Code, JetBrains IDEs, the Claude desktop app and on the web. It runs on your machine by default, working directly in your project folder.</li>
<li><strong>OpenAI Codex</strong> is OpenAI’s agent. It’s available as an open-source CLI, IDE extensions, a desktop app and as a cloud agent inside ChatGPT, where each task runs in its own sandboxed copy of your repository.</li>
</ul>
<p>Under the hood, each uses its company’s latest models. Those models leapfrog each other every few months, so treat any benchmark you read, including the ones in other comparison posts, as a snapshot rather than a verdict.</p>

<h2>The real difference: how you work with them</h2>
<p>The biggest difference isn’t raw intelligence. It’s the <strong>default workflow</strong> each tool is designed around.</p>
<h3>Claude Code: the pair programmer</h3>
<p>Claude Code shines when you stay in the loop. You ask it to build a feature, it proposes a plan, asks permission before running commands or editing files (unless you allow them), and you steer as it goes. Because it runs locally, it uses your real environment: your local WordPress install, your database, your build tools, your PHP version.</p>
<p>That makes it a good fit for messy, real-world work: fixing a bug that only shows up with a specific plugin combination, refactoring an old theme, or wiring a WooCommerce checkout to a custom API while you test in the browser.</p>
<h3>Codex: the task queue</h3>
<p>Codex’s cloud mode is built for delegation. You can send several tasks at once (“add unit tests for the cart class”, “fix this deprecation warning”, “update the README”), each runs in an isolated container, and you review the results as diffs or pull requests when they’re ready. The CLI also works locally in a similar way to Claude Code.</p>
<p>That suits well-scoped, independent tasks and teams that already work through pull requests and CI. It’s less suited to work that depends on things that only exist on your machine, like a local database with client data, unless you set up the cloud environment to match.</p>

<h2>Side-by-side comparison</h2>
<table>
<thead><tr><th></th><th>Claude Code</th><th>OpenAI Codex</th></tr></thead>
<tbody>
<tr><td><strong>Default style</strong></td><td>Interactive, you steer as it works</td><td>Interactive CLI, or hand off to the cloud</td></tr>
<tr><td><strong>Where code runs</strong></td><td>Your machine by default (cloud option available)</td><td>Cloud sandbox or your machine (CLI)</td></tr>
<tr><td><strong>Project instructions</strong></td><td><code>CLAUDE.md</code></td><td><code>AGENTS.md</code></td></tr>
<tr><td><strong>Parallel work</strong></td><td>Subagents and multiple sessions</td><td>Many cloud tasks at once</td></tr>
<tr><td><strong>Extending it</strong></td><td>MCP servers, hooks, skills, plugins</td><td>MCP servers, configuration, open-source CLI</td></tr>
<tr><td><strong>Code review</strong></td><td>Can review diffs and pull requests</td><td>Can review pull requests on GitHub</td></tr>
<tr><td><strong>Pricing</strong></td><td>Included in Claude paid plans, or pay per API use</td><td>Included in ChatGPT paid plans, or pay per API use</td></tr>
</tbody>
</table>
<p>Features and plan limits change often, so check Anthropic’s and OpenAI’s own pages before you buy.</p>

<h2>How they handle WordPress and WooCommerce work</h2>
<p>Most of my work is WordPress, WooCommerce and custom plugins, so that’s the lens I care about. Here’s what matters for that kind of project, whichever agent you use:</p>
<ul>
<li><strong>WordPress conventions:</strong> both know hooks, filters, the REST API and the block editor well. Both still sometimes forget nonce checks, capability checks and output escaping. Tell them your standards up front.</li>
<li><strong>Old codebases:</strong> client sites often have years of plugins, custom code and theme overrides. An agent that can search the whole project and run WP-CLI against a real install gives far better results than one guessing from a few files.</li>
<li><strong>WooCommerce:</strong> checkout, payment gateways and order hooks are high-risk. Use agents to draft and test, but read every line that touches money, and test on staging with real payment sandbox accounts.</li>
<li><strong>Plugins for sale:</strong> for plugins like WooCommerce extensions, Contact Form 7 add-ons, shortcodes and sliders, agents are great at boilerplate (settings pages, block registration, shortcode attributes, i18n) and at writing tests across PHP versions.</li>
</ul>

<h2>Context and instructions matter more than the tool</h2>
<p>Both agents read a project instructions file automatically: <code>CLAUDE.md</code> for Claude Code and <code>AGENTS.md</code> for Codex. This is the single highest-value thing you can set up. A good one covers:</p>
<ul>
<li>The stack and versions (WordPress, PHP, WooCommerce, build tools).</li>
<li>Coding standards (WordPress Coding Standards, prefixes, text domain).</li>
<li>How to run tests, linters and the local site.</li>
<li>What the agent must never do: touch production, commit secrets, edit vendor files.</li>
</ul>
<p>If you use both tools, keep one source of truth and point the other file at it, so your rules don’t drift.</p>

<h2>Safety: what can go wrong</h2>
<p>Coding agents can run commands, so treat them like a new team member with terminal access:</p>
<ul>
<li><strong>Permissions:</strong> both let you choose how much the agent can do without asking. Keep approvals on for anything that deletes, deploys or touches a database.</li>
<li><strong>Secrets:</strong> keep API keys and client credentials out of the repository and out of prompts. Use environment variables.</li>
<li><strong>Prompt injection:</strong> an agent that reads web pages, issues or third-party code can be tricked by instructions hidden in that content. Review what it did, not just what it says it did.</li>
<li><strong>Client data:</strong> cloud sandboxes mean your code runs on someone else’s servers. Check your client contracts and the provider’s data policies before sending client repositories anywhere.</li>
<li><strong>Review everything:</strong> AI-written code can look right and still have security holes. The <a href="/blog/php2shell-php-vulnerability-wordpress/">PHP2Shell vulnerabilities</a> are a good reminder of how much depends on server-side code being correct.</li>
</ul>

<h2>Cost: how to think about it</h2>
<p>Both tools are bundled into monthly subscriptions with usage limits, and both can also be billed per token through the API. For freelancers and small agencies, the subscription is usually the cheaper and more predictable option. Heavy agent use (long sessions, many parallel tasks, large codebases) is where limits start to bite, so watch your usage for a month before upgrading.</p>
<p>Don’t judge cost only by the price tag. An agent that gets a task right the first time is cheaper than one that needs three rounds of fixes, even if its plan costs more.</p>

<h2>So which should you choose?</h2>
<p><strong>Choose Claude Code if</strong> you want to work alongside the agent, your projects depend on a local environment (local WordPress, databases, build tools), and you do a lot of multi-file changes in existing code.</p>
<p><strong>Choose Codex if</strong> you want to hand off many small, well-defined tasks at once, your team works through GitHub pull requests and CI, and you already pay for ChatGPT.</p>
<p><strong>Use both if</strong> you can afford two subscriptions. A common pattern is to do the hands-on work in one and use the other as a second opinion for code review. Two different models catch different mistakes.</p>
<p>Try both on the same real task from your own backlog, not a toy example. Give each the same instructions file, and compare the diffs. That one afternoon will tell you more than any comparison post, including this one.</p>

<h2>What this means for clients</h2>
<p>When a developer uses AI agents well, you get faster delivery on routine work and more time spent on planning, testing and security. You should still get clean code you own, a staging site to review, and a developer who can explain every change. If you’re planning a <a href="/services/wordpress-plugin-development/">custom WordPress plugin</a> or a <a href="/services/custom-web-development/">custom web app</a>, <a href="/contact/">let’s talk</a>.</p>
""",
    },
    {
        "slug": "php2shell-php-vulnerability-wordpress",
        "seo_title": "PHP2Shell: What WordPress Site Owners Must Do",
        "title": "PHP2Shell Explained: What the Critical PHP Vulnerabilities Mean for Your WordPress Site",
        "desc": "PHP2Shell (CVE-2026-109618 and CVE-2026-109619) lets attackers run code on unpatched PHP servers. What happened, how to check your PHP version, and how to protect WordPress and WooCommerce sites.",
        "date": "2026-11-09",
        "category": "Security",
        "img": "photo-1550751827-4bd374c3f58b",
        "services": ["wordpress-development", "woocommerce-development", "technical-seo-analytics"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> PHP2Shell is the name for two critical flaws in PHP itself (CVE-2026-109618 and CVE-2026-109619) that can let an attacker run code on your server without logging in. They affect PHP 5.4 through 8.5, so almost every WordPress site was exposed. The fix is to run PHP <strong>8.2.35, 8.3.36, 8.4.27 or 8.5.12</strong> or newer, or a host-provided patched build. Check your PHP version today.</p>

<h2>What happened?</h2>
<p>In October 2026, the PHP project patched two memory-safety bugs in the PHP engine. Both are rated <strong>9.2 out of 10</strong> (CVSS 4.0) and allow <strong>remote code execution</strong>: an attacker can make a vulnerable server run their own code, without an account or password.</p>
<p>Because the bugs are in PHP itself, not in WordPress or a plugin, they affect any PHP application: WordPress, WooCommerce, Drupal, Joomla, and hosting tools like cPanel and Plesk. PHP runs roughly 7 out of 10 websites whose server language is known, which is why this was one of the biggest web security events of the year.</p>

<h2>Timeline</h2>
<ul>
<li><strong>August 2026:</strong> researchers find the bugs. One was found by Ryan Austin of the security firm Calif during OpenAI’s “Patch the Planet” project, using an AI model. Wiz independently found the related issues and named them “PHP2Shell”.</li>
<li><strong>17 October:</strong> Amazon’s threat intelligence team saw an exploitation attempt, four days before the patches were public.</li>
<li><strong>20 October:</strong> details leaked early, and PHP announced the security release.</li>
<li><strong>21 October:</strong> patched PHP versions and advisories were released. Within hours, security firms reported attacks in the wild.</li>
<li><strong>Late October:</strong> governments and large organisations took unpatched sites offline as a precaution, and agencies including CISA and the NSA urged immediate updates. Security researchers reported attackers chaining PHP2Shell with a Linux privilege-escalation bug to take full control of some servers.</li>
</ul>
<p>One uncomfortable detail: PHP’s own post-mortem reportedly showed that one of the bugs was spotted in a 2024 code audit, but wasn’t fixed because nobody had shown a practical exploit. AI tools have changed that. Bugs that were “too hard to exploit” are now being found and exploited much faster.</p>

<h2>Is my WordPress site affected?</h2>
<p>If your site runs any PHP version older than the patched releases, assume it’s vulnerable. Affected versions:</p>
<table>
<thead><tr><th>PHP branch</th><th>Patched version</th><th>Status</th></tr></thead>
<tbody>
<tr><td>8.5</td><td>8.5.12 or newer</td><td>Supported</td></tr>
<tr><td>8.4</td><td>8.4.27 or newer</td><td>Supported</td></tr>
<tr><td>8.3</td><td>8.3.36 or newer</td><td>Supported</td></tr>
<tr><td>8.2</td><td>8.2.35 or newer</td><td>Security fixes only</td></tr>
<tr><td>8.1, 8.0, 7.4</td><td>No official release</td><td>End of life: upgrade, or use a host backport</td></tr>
<tr><td>5.4 to 7.3</td><td>None</td><td>End of life: upgrade now</td></tr>
</tbody>
</table>
<p>Many hosts quietly patched their servers. cPanel and CloudLinux released backported fixes for older branches, so an old version number doesn’t always mean you’re exposed. If you’re not sure, ask your host directly.</p>

<h2>How to check your PHP version</h2>
<ol>
<li><strong>In WordPress:</strong> go to <em>Tools → Site Health → Info → Server</em> and look at “PHP version”.</li>
<li><strong>In cPanel:</strong> open <em>MultiPHP Manager</em> or <em>Select PHP Version</em> to see and change the version per domain.</li>
<li><strong>On a VPS:</strong> run <code>php -v</code>, and also check the version your web server actually uses (PHP-FPM can differ from the command-line PHP).</li>
</ol>

<h2>What to do right now</h2>
<ol>
<li><strong>Update PHP</strong> to a patched version, or confirm with your host that their build includes the fix. PHP’s maintainers said temporary workarounds were incomplete, so updating is the only real fix.</li>
<li><strong>Test on staging first if you’re jumping versions.</strong> Moving from PHP 7.4 to 8.3 can break old themes and plugins. If you can’t test quickly, put the site in maintenance mode rather than leaving it unpatched.</li>
<li><strong>Update WordPress, themes and plugins</strong> at the same time. Old plugins are often the reason sites are stuck on old PHP.</li>
<li><strong>Turn on a web application firewall.</strong> Cloudflare and other providers shipped temporary rules for PHP2Shell. A WAF helps, but it doesn’t replace patching.</li>
<li><strong>Check for signs of compromise</strong> if your site was unpatched after 21 October (see below).</li>
</ol>

<h2>Signs your site may have been hacked</h2>
<ul>
<li>New admin users you didn’t create.</li>
<li>Unknown PHP files in <code>wp-content/uploads</code>, or recently changed core files.</li>
<li>Spam pages, strange redirects, or Google showing “This site may be hacked”.</li>
<li>Unexpected cron jobs, high CPU usage, or your host reporting outgoing spam or attacks.</li>
<li>WooCommerce checkout pages with extra scripts you didn’t add (card skimmers).</li>
</ul>
<p>If you find any of these, take a full backup for evidence, then restore from a clean backup taken before the attack, update everything, and change all passwords and API keys, including database, hosting, FTP and payment gateway keys. Updating PHP closes the hole, but it doesn’t remove anything an attacker already left behind.</p>

<h2>Lessons for site owners</h2>
<ul>
<li><strong>Your hosting stack is part of your security.</strong> A fully updated WordPress install on an old PHP version is still vulnerable.</li>
<li><strong>Old PHP is a real cost.</strong> Sites stuck on PHP 7.4 for “compatibility” had no official patch. Budget for keeping themes and plugins compatible with supported PHP.</li>
<li><strong>AI is speeding up both sides.</strong> The same tools that found these bugs can help attackers find the next ones. Expect shorter gaps between disclosure and attack, and patch faster.</li>
<li><strong>Have a plan before you need it:</strong> automatic backups stored off-server, a staging site, uptime and file-change monitoring, and someone who can act the same day.</li>
</ul>

<p>Not sure if your WordPress or WooCommerce site is patched, or stuck on an old PHP version because of a theme or plugin? I can check your setup, upgrade PHP safely on staging and fix whatever breaks. <a href="/contact/">Get in touch</a>.</p>
<p><em>Sources: PHP security advisories, Palo Alto Networks Unit 42, SecurityWeek and other public reporting as of November 2026. Details may change as investigations continue.</em></p>
""",
    },
    {
        "slug": "add-ai-features-to-wordpress",
        "seo_title": "How to Add AI Features to WordPress (2026)",
        "title": "How to Add AI Features to a WordPress Website in 2026",
        "desc": "How to add AI to WordPress: chat assistants, smart search, editor tools and automations, built securely with API keys, budgets and privacy in mind.",
        "date": "2026-11-06",
        "category": "AI",
        "img": "photo-1677442136019-21780ecad995",
        "services": ["wordpress-plugin-development", "wordpress-automation", "custom-web-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> The most useful AI features for a WordPress site are an assistant trained on your own content, smarter on-site search, editor tools for drafting and summarising, and background automations. Build them server-side with your API key hidden, set usage limits, and keep a human in the loop for anything customer-facing.</p>

<h2>Which AI features are actually worth it?</h2>
<p>Skip the gimmicks and start where AI saves time or helps visitors find answers faster:</p>
<ul>
<li><strong>Site assistant (chat):</strong> answers questions using <em>your</em> pages, FAQs, docs and products, and hands off to a human when unsure.</li>
<li><strong>Semantic search:</strong> finds results by meaning, not just keywords, so “cheap flights to Cebu” matches a page titled “Budget travel to Cebu”.</li>
<li><strong>Editor tools:</strong> draft outlines, rewrite for clarity, generate alt text and meta descriptions, summarise long posts. Always reviewed before publishing.</li>
<li><strong>WooCommerce helpers:</strong> product description drafts, review summaries, “customers also asked” answers.</li>
<li><strong>Automations:</strong> classify incoming leads, summarise form submissions, route support emails, tag orders.</li>
</ul>

<h2>How it works under the hood</h2>
<p>Most AI features follow the same pattern: WordPress sends a request to an AI model provider’s API from the <strong>server</strong>, never from the browser, and shows the response. For assistants that should “know” your site, a technique called <strong>retrieval-augmented generation (RAG)</strong> is used:</p>
<ol>
<li>Your content is split into chunks and converted into embeddings (numeric fingerprints of meaning).</li>
<li>When a visitor asks something, the most relevant chunks are retrieved.</li>
<li>Only those chunks are sent to the model with the question, so answers stay grounded in your content.</li>
</ol>
<p>This can run inside a custom WordPress plugin (with a small vector index in the database or a hosted vector store), or in a separate service the site calls through the REST API.</p>

<h2>Security and cost: the part most tutorials skip</h2>
<ul>
<li><strong>Never expose API keys</strong> in JavaScript. Route every call through a server endpoint with nonce and capability checks.</li>
<li><strong>Rate-limit and cap spend:</strong> per-visitor limits, a monthly budget, and caching of repeated questions.</li>
<li><strong>Guard the prompt:</strong> restrict the assistant to your topics, and don’t let page content or user input override its instructions.</li>
<li><strong>Privacy:</strong> don’t send personal data you don’t need. Tell visitors when they’re talking to AI, and check your provider’s data-retention settings.</li>
<li><strong>Fallbacks:</strong> if the API is slow or down, the site must still work. Show a contact form instead of an error.</li>
</ul>

<h2>Plugin or custom build?</h2>
<p>Off-the-shelf AI plugins are fine for quick experiments and editor-side writing tools. For a customer-facing assistant, search, or anything tied to your products, bookings or CRM, a small <a href="/services/wordpress-plugin-development/">custom plugin</a> usually wins. You control the prompts, data, costs and UX, and you don’t pay for features you don’t use.</p>

<h2>A sensible rollout plan</h2>
<ol>
<li>Pick one job (e.g. “answer pre-sales questions”) and define what success looks like.</li>
<li>Clean up the source content. AI answers are only as good as your pages and FAQs.</li>
<li>Launch to a small share of visitors, log questions and answers, and review weekly.</li>
<li>Expand once accuracy and cost are where you want them.</li>
</ol>
<p>Want AI on your WordPress or WooCommerce site, done safely? <a href="/contact/">Tell me what you have in mind</a>.</p>
""",
    },
    {
        "slug": "ai-assisted-web-development",
        "seo_title": "AI-Assisted Web Development: What Works",
        "title": "AI-Assisted Web Development: What It’s Great At and Where It Falls Short",
        "desc": "An honest look at AI coding assistants for WordPress, Shopify and custom web development: where they speed things up, where they fail, and how to keep quality high.",
        "date": "2026-10-28",
        "category": "AI",
        "img": "photo-1555066931-4365d14bab8c",
        "services": ["custom-web-development", "custom-wordpress-theme-development", "shopify-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> AI coding assistants are excellent at boilerplate, refactors, tests, documentation and exploring unfamiliar APIs. They’re weak at architecture, security edge cases and anything that needs real context about your business. Used with code review and testing, they shorten delivery time without lowering quality.</p>

<h2>Where AI genuinely speeds up web development</h2>
<ul>
<li><strong>Boilerplate:</strong> block registration, custom post types, REST endpoints, Liquid section schemas, form validation.</li>
<li><strong>Refactoring:</strong> converting old jQuery to vanilla JS, PHP version upgrades, renaming and restructuring at scale.</li>
<li><strong>Tests and docs:</strong> generating test cases, README files, inline docs and changelogs.</li>
<li><strong>Exploration:</strong> “How does this Shopify Admin GraphQL mutation work?” gets you to a working draft fast. Then you verify it against the official docs.</li>
<li><strong>Content-heavy builds:</strong> turning structured content into templates, seeding realistic demo data, drafting alt text.</li>
</ul>

<h2>Where it still falls short</h2>
<ul>
<li><strong>Architecture:</strong> choosing between a block theme, headless or a page builder depends on your team, budget and roadmap, which a model doesn’t know.</li>
<li><strong>Security:</strong> generated code often misses nonce checks, capability checks, escaping or rate limits unless you ask for them explicitly, and reviewers still need to verify them.</li>
<li><strong>Outdated or invented APIs:</strong> models sometimes suggest deprecated functions or methods that don’t exist. Everything must be tested.</li>
<li><strong>Performance:</strong> AI-written code can be correct but slow: N+1 queries, unnecessary scripts, heavy DOM.</li>
<li><strong>Taste:</strong> pixel-perfect design and good UX copy still need a human eye.</li>
</ul>

<h2>How to keep quality high</h2>
<ol>
<li><strong>Give context:</strong> coding standards, the stack, constraints and examples from the existing codebase.</li>
<li><strong>Small, reviewable changes</strong> instead of huge generated files.</li>
<li><strong>Review every line</strong> like a pull request from a new teammate, with security and performance checks.</li>
<li><strong>Automated checks:</strong> linters, PHPCS/WordPress Coding Standards, type checks, tests, Lighthouse and accessibility audits.</li>
<li><strong>Never paste secrets</strong> or client data you don’t have permission to share into an AI tool.</li>
</ol>

<h2>What this means for clients</h2>
<p>Used well, AI shifts time away from typing and toward the things that matter: planning, UX, testing, accessibility and SEO. You should still expect clean, documented code you own, a staging site to review, and a developer who can explain every decision.</p>
<p>Planning a <a href="/services/custom-web-development/">custom web app</a> or a <a href="/services/custom-wordpress-theme-development/">custom WordPress theme</a>? <a href="/contact/">Let’s talk</a>.</p>
""",
    },
    {
        "slug": "ai-automation-for-small-business",
        "seo_title": "AI Automation for Small Business: n8n & Make",
        "title": "AI Automation for Small Businesses: Practical Workflows with n8n, Make and Zapier",
        "desc": "Practical AI automations for small businesses: lead triage, inbox summaries, order follow-ups and content repurposing with n8n, Make or Zapier.",
        "date": "2026-10-10",
        "category": "AI",
        "img": "photo-1519389950473-47ba0277781c",
        "services": ["wordpress-automation", "woocommerce-development", "online-booking-system-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> The best AI automations for small businesses take a repetitive, text-heavy task (reading enquiries, sorting emails, writing follow-ups) and let an AI step classify, summarise or draft, while a workflow tool like n8n, Make or Zapier moves the data between your website, CRM and inbox. Keep a human approving anything that goes to customers.</p>

<h2>Five workflows that pay for themselves</h2>
<ol>
<li><strong>Lead triage:</strong> a website form submission is summarised, scored (budget, urgency, fit), tagged and sent to your CRM, with a short summary posted to Slack or email.</li>
<li><strong>Inbox digest:</strong> support emails are grouped by topic each morning, with suggested replies saved as drafts for review.</li>
<li><strong>Order follow-ups:</strong> WooCommerce or Shopify orders trigger personalised thank-you notes, review requests or reorder reminders, drafted by AI from the order details.</li>
<li><strong>Booking prep:</strong> before an appointment, the customer’s form answers and history are summarised into a one-paragraph brief.</li>
<li><strong>Content repurposing:</strong> a new blog post becomes draft social posts, an email newsletter section and FAQ entries, queued for approval.</li>
</ol>

<h2>Which tool should you use?</h2>
<table>
<thead><tr><th>Tool</th><th>Best for</th><th>Watch out for</th></tr></thead>
<tbody>
<tr><td>Zapier</td><td>Fast setup, huge app library</td><td>Cost grows quickly with volume</td></tr>
<tr><td>Make</td><td>Visual, complex multi-step flows</td><td>Operations-based pricing to monitor</td></tr>
<tr><td>n8n</td><td>Self-hosting, privacy, high volume</td><td>Needs hosting and maintenance</td></tr>
</tbody>
</table>

<h2>Make it reliable, not just clever</h2>
<ul>
<li><strong>Structured outputs:</strong> ask the AI step to return JSON (e.g. <code>{"score": 1-5, "category": "..."}</code>) so the next step doesn’t break.</li>
<li><strong>Error handling and retries:</strong> every workflow should alert you on failure instead of failing silently.</li>
<li><strong>Human approval</strong> for anything customer-facing, at least until you trust the output.</li>
<li><strong>Data minimisation:</strong> send only the fields the AI needs, and avoid sensitive personal data.</li>
<li><strong>Cost controls:</strong> use smaller, cheaper models for classification and save larger models for writing.</li>
</ul>

<h2>Where to start</h2>
<p>List the tasks your team repeats every week, estimate the hours, and automate the biggest one first. A single well-built workflow often saves several hours a week and shows quickly whether AI is worth expanding.</p>
<p>I build automations that connect WordPress, WooCommerce, Shopify, booking systems and CRMs. <a href="/services/wordpress-automation/">See automation services</a> or <a href="/contact/">tell me about your workflow</a>.</p>
""",
    },
    {
        "slug": "wordpress-seo-ai-search-2026",
        "seo_title": "WordPress SEO in 2026: Rank in Google & AI Search",
        "title": "WordPress SEO in 2026: How to Rank in Google and AI Search",
        "desc": "A practical WordPress SEO checklist for 2026: technical foundations, structured data, content that AI assistants cite, and the Core Web Vitals that still matter.",
        "date": "2026-11-02",
        "updated": "2026-11-08",
        "category": "SEO",
        "img": "photo-1460925895917-afdab827c52f",
        "services": ["technical-seo-analytics", "wordpress-development", "custom-wordpress-theme-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> In 2026, ranking a WordPress site means getting the classic technical SEO right <em>and</em> making your content easy for AI systems to understand and cite. That means a clean structure, real expertise, structured data, fast pages and answer-first writing.</p>

<h2>1. Technical foundations still come first</h2>
<p>Neither Google nor an AI assistant can rank a page it can't crawl and render. Before you think about content, make sure the basics are in place:</p>
<ul>
<li><strong>One canonical URL per page</strong>, HTTPS everywhere and no accidental duplicates (tag archives, parameters, staging sites).</li>
<li><strong>An XML sitemap</strong> that lists only indexable pages and is submitted in Google Search Console and Bing Webmaster Tools.</li>
<li><strong>A robots.txt</strong> that doesn't block CSS, JS or the crawlers you want, including AI crawlers if you want to be cited.</li>
<li><strong>Server-rendered HTML.</strong> If important content only appears after JavaScript runs, some crawlers will miss it.</li>
</ul>

<h2>2. Core Web Vitals: speed is part of the experience</h2>
<p>Google still uses page experience signals. The three metrics to watch are LCP (loading), INP (responsiveness) and CLS (visual stability). On WordPress the biggest wins usually come from:</p>
<ul>
<li>A lightweight theme instead of a multipurpose theme with every feature enabled.</li>
<li>Fewer plugins, and none that load scripts site-wide when they're only needed on one page.</li>
<li>Modern image formats (WebP/AVIF) with explicit width and height, and lazy-loading below the fold.</li>
<li>Proper page caching and a CDN.</li>
</ul>

<h2>3. Structured data helps machines understand you</h2>
<p>Schema markup (JSON-LD) tells search engines and AI systems exactly what a page is about: a person, a service, an article, an FAQ, a product. For a business or freelancer site, the most useful types are <code>Organization</code> or <code>Person</code>, <code>Service</code>, <code>Article</code>/<code>BlogPosting</code>, <code>BreadcrumbList</code> and <code>FAQPage</code>. Keep the markup consistent with what is visible on the page.</p>

<h2>4. Write for answers, not just keywords</h2>
<p>AI Overviews and assistants such as ChatGPT, Claude, Perplexity and Gemini pull passages that answer a question directly. Content that gets cited usually has:</p>
<ul>
<li><strong>An answer-first intro.</strong> State the answer in the first two sentences, then explain.</li>
<li><strong>Clear question-style headings</strong> that match how people actually ask.</li>
<li><strong>Specific, verifiable details</strong>: steps, numbers, examples and trade-offs, not generic filler.</li>
<li><strong>Visible authorship</strong>: who wrote it, why they're qualified, and when it was last updated.</li>
</ul>

<h2>5. Build topical depth with internal links</h2>
<p>A single page rarely ranks on its own. Create a clear hub (for example, a services page) and supporting pages and articles that link to each other with descriptive anchor text. That shows both search engines and AI models that you cover a topic in depth.</p>

<h2>6. Make your site AI-crawler friendly</h2>
<p>Decide deliberately which AI crawlers may access your content. If you want to be cited in AI answers, allow crawlers such as GPTBot, ClaudeBot, PerplexityBot and Google-Extended in robots.txt. Many sites also publish an <code>llms.txt</code> file, a short, plain-text summary of who you are and your most important pages.</p>

<h2>A quick WordPress SEO checklist</h2>
<ol>
<li>Install one SEO plugin (Yoast, Rank Math or SEOPress) and configure titles, sitemaps and schema.</li>
<li>Give every important page a unique title (under 60 characters) and meta description.</li>
<li>Use one H1 per page and a logical H2/H3 structure.</li>
<li>Add descriptive alt text to images.</li>
<li>Fix broken links and redirect chains.</li>
<li>Measure Core Web Vitals in Search Console and fix the worst templates first.</li>
<li>Publish helpful content regularly and update older posts.</li>
</ol>
<p>If you'd like a technical SEO audit of your WordPress site, <a href="/contact/">get in touch</a>.</p>
""",
    },
    {
        "slug": "headless-wordpress-nextjs-guide",
        "seo_title": "Headless WordPress + Next.js: Is It Worth It?",
        "title": "Headless WordPress with Next.js: When It's Worth It (and When It Isn't)",
        "desc": "An honest guide to headless WordPress with Next.js: benefits, trade-offs, SEO considerations, costs and how to decide if your project needs it.",
        "date": "2026-10-18",
        "category": "Headless",
        "img": "photo-1551288049-bebda4e38f71",
        "services": ["headless-wordpress-development", "custom-web-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> Headless WordPress with Next.js is worth it when you need top-tier performance, a highly custom front end, or one content source feeding several channels. For a small brochure site, a well-built traditional theme is usually faster to ship and cheaper to run.</p>

<h2>What "headless" actually means</h2>
<p>In a traditional WordPress site, WordPress stores content <em>and</em> renders the HTML through a PHP theme. In a headless setup, WordPress only stores and serves content through an API (REST or WPGraphQL), and a separate application, usually built with Next.js, renders the website.</p>

<h2>The benefits</h2>
<ul>
<li><strong>Speed.</strong> Static generation and incremental static regeneration (ISR) serve pre-built pages from a CDN edge.</li>
<li><strong>Security.</strong> The public site doesn't expose wp-admin or PHP, which shrinks the attack surface.</li>
<li><strong>Design freedom.</strong> React components, animations and app-like interactions without fighting a theme.</li>
<li><strong>Omnichannel.</strong> The same content can feed a website, a mobile app and other platforms.</li>
</ul>

<h2>The trade-offs</h2>
<ul>
<li><strong>Two systems to host and maintain</strong>: WordPress and the front end.</li>
<li><strong>Plugins that render front-end output</strong> (forms, sliders, page builders) don't work out of the box.</li>
<li><strong>Preview and SEO need deliberate setup.</strong> They don't come for free.</li>
<li><strong>Higher initial cost</strong> than a standard theme build.</li>
</ul>

<h2>Is headless WordPress good for SEO?</h2>
<p>Yes, when it's done properly. Pages rendered on the server or at build time are fully crawlable and usually very fast. The common mistakes are forgetting to pass SEO plugin metadata to the front end, missing canonical tags, broken sitemaps and lost redirects. A good build pulls titles, descriptions, schema and redirects from WordPress (for example through WPGraphQL plus an SEO plugin extension) and renders them in Next.js metadata.</p>

<h2>A typical stack</h2>
<ul>
<li>WordPress on managed hosting, with ACF for structured fields</li>
<li>WPGraphQL (+ WPGraphQL for ACF) as the API</li>
<li>Next.js App Router, deployed to Vercel, Netlify or Cloudflare</li>
<li>On-demand revalidation triggered when editors publish</li>
</ul>

<h2>How to decide</h2>
<p>Choose headless if performance is a competitive advantage, your front end is highly interactive, or you're publishing to more than one channel. Stay traditional if your team relies heavily on page builders, your budget is tight, or the site is mostly static pages.</p>
<p>Not sure which way to go? <a href="/services/headless-wordpress-development/">See my headless WordPress service</a> or <a href="/contact/">ask me directly</a>.</p>
""",
    },
    {
        "slug": "elementor-vs-custom-wordpress-theme",
        "seo_title": "Elementor vs Custom WordPress Theme",
        "title": "Elementor vs a Custom WordPress Theme: Which Should You Choose?",
        "desc": "Elementor or a custom-coded WordPress theme? Compare speed, flexibility, cost, editing experience and long-term maintenance to choose the right approach.",
        "date": "2026-09-30",
        "category": "WordPress",
        "img": "photo-1517694712202-14dd9538aa97",
        "services": ["elementor-development", "custom-wordpress-theme-development", "acf-development"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> Choose Elementor if your marketing team needs to build and change pages visually and often. Choose a custom theme (block theme + ACF) if performance, consistency and long-term maintainability matter most. Both can be excellent when they're built well.</p>

<h2>Editing experience</h2>
<p><strong>Elementor</strong> offers true drag-and-drop editing. Non-technical teams can create landing pages without a developer. <strong>A custom theme</strong> gives editors a curated set of blocks or fields. There's less freedom, but it's also much harder to break the design.</p>

<h2>Performance</h2>
<p>A custom theme ships only the code your site needs, so it usually has the edge in Core Web Vitals. Modern Elementor (with Flexbox/Grid containers and optimised asset loading) can still perform well if the build is disciplined. Avoid nested containers, keep add-on packs to a minimum and optimise images.</p>

<h2>Cost and speed to launch</h2>
<p>Elementor builds are generally faster to deliver for marketing sites. Custom themes take more upfront development but cost less over time in licence fees, plugin conflicts and clean-up work.</p>

<h2>Long-term maintenance</h2>
<p>Page builder sites depend on the builder and any add-ons staying compatible. Custom themes depend only on WordPress core and the code you own. For sites expected to live five years or more, that difference matters.</p>

<h2>A quick comparison</h2>
<table>
<thead><tr><th>Criteria</th><th>Elementor</th><th>Custom theme</th></tr></thead>
<tbody>
<tr><td>Visual page building</td><td>Excellent</td><td>Curated blocks</td></tr>
<tr><td>Performance ceiling</td><td>Good</td><td>Excellent</td></tr>
<tr><td>Design consistency</td><td>Depends on editors</td><td>Enforced</td></tr>
<tr><td>Upfront cost</td><td>Lower</td><td>Higher</td></tr>
<tr><td>Long-term control</td><td>Builder-dependent</td><td>Full ownership</td></tr>
</tbody>
</table>

<h2>The hybrid option</h2>
<p>Many projects benefit from a custom theme for the core templates (posts, products, listings) plus a builder or block patterns for campaign landing pages. You get speed where it matters and flexibility where marketing needs it.</p>
<p>I build both. Read about my <a href="/services/elementor-development/">Elementor development</a> and <a href="/services/custom-wordpress-theme-development/">custom theme development</a> services.</p>
""",
    },
    {
        "slug": "shopify-vs-woocommerce-2026",
        "seo_title": "Shopify vs WooCommerce in 2026: Honest Comparison",
        "title": "Shopify vs WooCommerce in 2026: A Developer's Honest Comparison",
        "desc": "Shopify or WooCommerce? A developer who builds on both compares costs, customisation, SEO, payments, scalability and maintenance in 2026.",
        "date": "2026-09-12",
        "category": "E-commerce",
        "img": "photo-1472851294608-062f824d29cc",
        "services": ["shopify-development", "woocommerce-development", "stripe-paypal-payment-integration"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> Shopify is the better choice when you want a fully managed, low-maintenance store and fast time to market. WooCommerce is better when you need deep customisation, full data ownership or a content-heavy site where the store is one part of a bigger WordPress platform.</p>

<h2>Hosting and maintenance</h2>
<p><strong>Shopify</strong> is fully hosted. Security, uptime and checkout scaling are handled for you. <strong>WooCommerce</strong> runs on your own WordPress hosting, so you (or your developer) are responsible for updates, backups and performance.</p>

<h2>Customisation</h2>
<p>WooCommerce can be customised at almost every level because it's open-source PHP. Shopify themes are written in Liquid, and deeper logic is handled with apps, metafields, metaobjects and the Admin and Storefront APIs. Shopify is very capable, but some checkout and core behaviours are intentionally locked down.</p>

<h2>Costs</h2>
<p>Shopify has a monthly plan fee plus app subscriptions, and transaction fees if you don't use Shopify Payments. WooCommerce itself is free, but you pay for hosting, premium extensions and maintenance. Compare the total cost over 2–3 years, not just the first month.</p>

<h2>SEO</h2>
<p>Both platforms can rank well. WooCommerce benefits from WordPress's strong content and SEO tooling. Shopify has a few fixed URL structures (such as <code>/products/</code> and <code>/collections/</code>), but it handles technical basics well, and blogs and structured data can be extended with themes and apps.</p>

<h2>Payments</h2>
<p>Shopify Payments is seamless where available. WooCommerce integrates with Stripe, PayPal and many regional gateways, which is useful for businesses in markets Shopify Payments doesn't support.</p>

<h2>Which should you choose?</h2>
<ul>
<li><strong>Pick Shopify</strong> if you're product-focused, want minimal maintenance and plan to grow quickly.</li>
<li><strong>Pick WooCommerce</strong> if you need custom business logic, want to own everything, or already run a large WordPress site.</li>
<li><strong>Consider headless</strong> (Hydrogen or Next.js) if brand experience and performance are your main differentiators.</li>
</ul>
<p>I develop on both platforms. See <a href="/services/shopify-development/">Shopify development</a> and <a href="/services/woocommerce-development/">WooCommerce development</a>.</p>
""",
    },
    {
        "slug": "figma-to-wordpress-workflow",
        "seo_title": "Figma to WordPress: Pixel-Perfect Workflow",
        "title": "Figma to WordPress: My Step-by-Step Workflow for Pixel-Perfect Builds",
        "desc": "How I convert Figma designs into fast, responsive, editable WordPress websites: design review, tokens, components, content modelling, QA and launch.",
        "date": "2026-08-25",
        "category": "Workflow",
        "img": "photo-1581291518857-4e27b48ff24e",
        "services": ["figma-to-wordpress", "custom-wordpress-theme-development", "web-design"],
        "body": """
<p class="tldr"><strong>Short answer:</strong> A reliable Figma-to-WordPress conversion has six stages: design review, design tokens, a component library, content modelling, responsive build, and QA against the design. Skipping the first two is the most common reason builds drift from the design.</p>

<h2>1. Design review</h2>
<p>Before writing code I go through the Figma file and list anything missing: hover and focus states, empty and error states, mobile layouts, long-content cases. Agreeing on these upfront prevents surprises later.</p>

<h2>2. Design tokens</h2>
<p>Colours, type scale, spacing and radii are extracted into tokens, either in <code>theme.json</code> for block themes or in Tailwind/CSS variables. One source of truth keeps the build consistent and makes future changes easy.</p>

<h2>3. Component library</h2>
<p>Each repeating design element becomes a reusable component: a Gutenberg block, ACF block, Elementor template or Divi layout, depending on the editor the client prefers.</p>

<h2>4. Content modelling</h2>
<p>I decide what should be a page, a custom post type, a taxonomy or a global option. This is what makes the finished site easy to edit and scale.</p>

<h2>5. Responsive build</h2>
<p>I build mobile-first and fill in breakpoints the design didn't cover, staying faithful to the designer's intent. Images get proper sizes and modern formats, and fonts are loaded efficiently.</p>

<h2>6. QA against the design</h2>
<p>I compare the build to the Figma frames at each breakpoint, test in major browsers, run accessibility and Lighthouse checks, and fix the details before handover.</p>

<h2>What you get at the end</h2>
<ul>
<li>A WordPress site that matches the design</li>
<li>An editing experience your team understands</li>
<li>Clean, documented code in a Git repository</li>
<li>A short video walkthrough for content editors</li>
</ul>
<p>Have a Figma file ready? <a href="/services/figma-to-wordpress/">Learn more about Figma to WordPress</a> or <a href="/contact/">send it over for a quote</a>.</p>
""",
    },
]
