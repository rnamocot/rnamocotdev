"""Privacy policy and terms of use, rendered at /privacy/ and /terms/.

Placeholders filled in by build.py:
  [[NAME]] [[EMAIL]] [[SITE]] [[LOCATION]] [[UPDATED]]
  [[ANALYTICS]]  -> the analytics section (changes automatically when GA4_ID is set in build.py)

Edit the wording here, then run `python build.py`.
This is a general template, not legal advice. Review it, and have it checked if you sell
plugins, process payments or handle a lot of personal data.
"""

PRIVACY = """
<p class="tldr"><strong>In short:</strong> this website collects as little as possible. There are no advertising trackers, and fonts and images are served from this site, not from third parties. If you send a message, I use your details only to reply to you. [[ANALYTICS_SHORT]] You can ask me to see or delete your data at any time by emailing <a href="mailto:[[EMAIL]]">[[EMAIL]]</a>.</p>

<h2>Who I am</h2>
<p>This website, [[SITE]], is run by [[NAME]], a freelance web developer based in the [[LOCATION]]. I’m responsible for the personal data collected through this website (the “data controller”). You can contact me about privacy at <a href="mailto:[[EMAIL]]">[[EMAIL]]</a>.</p>

<h2>What I collect and why</h2>
<h3>When you send a message</h3>
<p>If you use the contact form or the chat box, I receive your <strong>name, email address, the service and budget you selected, the page you sent it from, and your message</strong>. I use this only to reply to your enquiry and, if we work together, to manage the project.</p>
<ul>
<li>Messages are delivered to my email inbox (Gmail, provided by Google).</li>
<li>A backup copy is stored in a private, non-public folder on this website’s server, in case an email fails to arrive.</li>
<li>To stop spam, the form keeps a scrambled (hashed) version of your IP address for one hour to limit how many messages can be sent. Your actual IP address is not stored.</li>
</ul>
<p><strong>Legal basis:</strong> taking steps at your request before entering into a contract, and my legitimate interest in answering enquiries.</p>

<h3>Visitor counter</h3>
<p>The visitor count in the footer is calculated on this website’s own server. It uses a scrambled code made from your IP address, browser type and today’s date to count each visitor once per day. That code can’t be turned back into your IP address, and the list is deleted every day. It doesn’t use cookies. Your browser remembers that you’ve been counted in “session storage”, which is cleared when you close the tab.</p>
<p><strong>Legal basis:</strong> my legitimate interest in knowing roughly how many people visit the site.</p>

<h3>Server logs</h3>
<p>Like almost every website, my hosting provider automatically records technical information when pages are requested, such as IP address, date and time, the page requested and browser type. These logs are used for security and to keep the site running, and are kept for a limited time by the host.</p>

[[ANALYTICS]]

<h2>Cookies and similar technologies</h2>
[[COOKIES]]

<h2>Who I share data with</h2>
<p>I don’t sell or rent your personal data, and I don’t share it for advertising. It’s only handled by the services needed to run this website:</p>
<ul>
<li><strong>My web hosting provider</strong>, which stores the website, server logs and message backups.</li>
<li><strong>Google (Gmail)</strong>, which delivers and stores email.</li>
[[ANALYTICS_PROCESSOR]]
</ul>
<p>These providers may store data outside your country, including in the United States. Where required, they use safeguards such as the European Commission’s Standard Contractual Clauses.</p>

<h2>How long I keep data</h2>
<ul>
<li><strong>Enquiries that don’t lead to a project:</strong> deleted within 2 years.</li>
<li><strong>Client communications and project records:</strong> kept for as long as needed for the project and for legal, tax and accounting requirements.</li>
<li><strong>Spam-limit data:</strong> 1 hour. <strong>Visitor counter data:</strong> 1 day.</li>
</ul>

<h2>Your rights</h2>
<p>Depending on where you live, including under the EU and UK GDPR, the Australian Privacy Act, the Philippine Data Privacy Act of 2012 and US state privacy laws, you have the right to:</p>
<ul>
<li>ask for a copy of the personal data I hold about you;</li>
<li>ask me to correct or delete it;</li>
<li>object to or restrict how I use it;</li>
<li>withdraw consent at any time, where I rely on consent;</li>
<li>complain to your local data protection authority (for example, the National Privacy Commission in the Philippines, the ICO in the UK or the OAIC in Australia).</li>
</ul>
<p>To use any of these rights, email <a href="mailto:[[EMAIL]]">[[EMAIL]]</a>. I’ll reply within 30 days. I don’t sell personal data, so there’s nothing to opt out of under “do not sell” laws.</p>

<h2>Security</h2>
<p>The site is served over HTTPS, the message backups and counter data are stored in a folder that can’t be reached from the web, and IP addresses are hashed rather than stored. No method of storage or transmission is completely secure, but I take reasonable steps to protect your data.</p>

<h2>Children</h2>
<p>This website is for businesses and isn’t aimed at children under 16. I don’t knowingly collect their data.</p>

<h2>Changes to this policy</h2>
<p>If I change how I handle personal data, I’ll update this page and the date at the top.</p>
"""

TERMS = """
<p class="tldr"><strong>In short:</strong> you’re welcome to read and share this website. Please don’t copy its design, code or articles as your own. Client projects and plugin purchases are covered by their own written agreements, which take priority over these terms.</p>

<h2>About these terms</h2>
<p>These terms apply to your use of [[SITE]], run by [[NAME]], a freelance web developer based in the [[LOCATION]]. By using the website, you agree to them. If you don’t agree, please don’t use the site.</p>

<h2>Using this website</h2>
<ul>
<li>You may read, link to and share pages from this website.</li>
<li>Don’t try to break, overload or gain unauthorised access to the site, its server or its contact form.</li>
<li>Don’t use the contact form or chat to send spam, malware or unlawful content.</li>
</ul>

<h2>Content and intellectual property</h2>
<p>Unless stated otherwise, the text, design, code, graphics and articles on this website belong to [[NAME]]. You may quote short extracts with a link back to the original page. Client project screenshots and logos belong to their owners and are shown as portfolio examples. Stock photos are used under their own licences, and brand names and logos belong to their respective owners.</p>

<h2>Articles and advice</h2>
<p>Blog articles are general information, written in good faith and accurate at the time of writing. Technology, prices and security advice change quickly, so they aren’t professional advice for your specific situation. Check important details, and get advice before making decisions that depend on them.</p>

<h2>Project work</h2>
<p>Web development, design and other services are provided under a separate written proposal or agreement, which sets out the scope, price, timeline, payment terms and ownership of the work. If that agreement conflicts with these terms, the agreement applies.</p>

<h2>Plugins</h2>
<p>Plugins listed on this website are licensed, not sold. Each plugin’s licence, support period, updates and refund policy are shown at checkout and in the plugin’s documentation, and apply to your purchase. Plugins marked “coming soon” aren’t available yet, and their features and prices may change before release.</p>

<h2>Links to other websites</h2>
<p>This website links to other sites, such as client projects and my own products. I’m not responsible for their content or their privacy practices.</p>

<h2>No warranty and limitation of liability</h2>
<p>The website is provided “as is”. I try to keep it accurate and available, but I don’t guarantee it will always be error-free or online. To the extent the law allows, I’m not liable for any loss arising from your use of this website or reliance on its content. Nothing in these terms limits rights you have under consumer protection law that can’t be excluded.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of the Republic of the Philippines. This doesn’t remove any protection you have under the laws of the country where you live.</p>

<h2>Changes and contact</h2>
<p>I may update these terms from time to time. The date at the top shows the latest version. Questions? Email <a href="mailto:[[EMAIL]]">[[EMAIL]]</a>.</p>
"""
