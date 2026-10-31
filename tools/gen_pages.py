#!/usr/bin/env python3
"""Generate the KMB Electric service pages and the projects gallery from one template.

Run from the repo root:  python3 tools/gen_pages.py
Writes: ev-chargers.html, panel-upgrades.html, hot-tubs.html, generators.html, projects.html,
and appends the subpage CSS block to assets/site.css if it is not there yet.

The generated pages are plain HTML and can be hand-edited afterwards. If you re-run this
script it overwrites them, so fold hand edits back into the content below.
Rules: facts only, no prices, no em dashes, service copy stays in plain English.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PHONE = "719-963-5191"
TEL = "tel:+17199635191"
SMS = "sms:+17199635191"
SITE = "https://kmbelectric.com"

# ---------------------------------------------------------------- shared chrome

HEAD_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://unpkg.com/aos@2.3.1/dist/aos.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="/assets/site.css?v=4">
<meta name="theme-color" content="#0B1220">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/icon-180.png">"""

ANALYTICS = """<script data-goatcounter="https://kmbstats.fusehq.cloud/count" async src="https://kmbstats.fusehq.cloud/count.js"></script>"""

def header(active=""):
    def a(href, label, key):
        cls = ' class="is-active"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f"""<div id="scroll-progress" aria-hidden="true"></div>

<header class="site-header" id="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="KMB Electric home">
      <img src="/assets/logo-480.png" alt="" width="44" height="56">
      <span class="brand-name">KMB Electric<small>Veteran Owned</small></span>
    </a>
    <nav class="nav" aria-label="Primary">
      <div class="nav-links">
        {a("/#services", "Services", "services")}
        {a("/projects", "Projects", "projects")}
        {a("/#why", "Why KMB", "why")}
        {a("/#reviews", "Reviews", "reviews")}
        {a("#contact", "Contact", "contact")}
      </div>
      <a class="nav-phone" href="{TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i>{PHONE}</a>
      <a class="btn btn-primary nav-cta" href="#contact">Get a Free Estimate</a>
      <button class="menu-toggle" id="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>

<div class="mobile-menu" id="mobile-menu" data-lenis-prevent>
  <a class="mm-link" href="/#services">Services</a>
  <a class="mm-link" href="/projects">Projects</a>
  <a class="mm-link" href="/#why">Why KMB</a>
  <a class="mm-link" href="/#reviews">Reviews</a>
  <a class="mm-link" href="#contact">Contact</a>
  <a class="mm-phone" href="{TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i> {PHONE}</a>
  <a class="btn btn-primary" href="#contact">Get a Free Estimate</a>
</div>
"""

FOOTER = f"""<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="f-brand"><img src="/assets/logo-480.png" alt="KMB Electric shield and bolt logo" width="52" height="66"><span class="n">KMB Electric LLC<small>Veteran Owned, Quality Work</small></span></div>
        <p class="f-tag">Licensed and insured electrical contractor serving Colorado Springs and the Front Range. Residential, small scale commercial, and everything in between.</p>
        <div class="f-social">
          <a href="https://www.google.com/maps/search/KMB+Electric+LLC+Colorado+Springs+CO" target="_blank" rel="noopener" aria-label="KMB Electric on Google"><i class="fa-brands fa-google"></i></a>
          <a href="https://www.facebook.com/" target="_blank" rel="noopener" aria-label="KMB Electric on Facebook"><i class="fa-brands fa-facebook-f"></i></a>
          <a href="https://www.instagram.com/" target="_blank" rel="noopener" aria-label="KMB Electric on Instagram"><i class="fa-brands fa-instagram"></i></a>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/panel-upgrades">Service &amp; Panel Upgrades</a></li>
          <li><a href="/ev-chargers">EV Charger Installation</a></li>
          <li><a href="/hot-tubs">Hot Tub &amp; Spa Wiring</a></li>
          <li><a href="/generators">Generators &amp; Transfer Switches</a></li>
          <li><a href="/#services">Custom Homes &amp; New Construction</a></li>
          <li><a href="/#services">Remodels, Additions &amp; Basements</a></li>
          <li><a href="/#services">Small Scale Tenant Finishes</a></li>
          <li><a href="/#services">Lighting, Circuits &amp; Service Calls</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact Us</h4>
        <ul>
          <li><a href="{TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i>{PHONE}</a></li>
          <li><a href="{SMS}"><i class="fa-solid fa-comment-sms" aria-hidden="true"></i>Text us</a></li>
          <li><a href="mailto:kylebashford@kmbelectric.com"><i class="fa-solid fa-envelope" aria-hidden="true"></i>kylebashford@kmbelectric.com</a></li>
          <li><a href="#contact"><i class="fa-solid fa-location-dot" aria-hidden="true"></i>Colorado Springs, CO</a></li>
          <li><a href="#contact"><i class="fa-solid fa-clock" aria-hidden="true"></i>Mon to Fri 7 AM to 5 PM, weekends closed</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/projects">Projects</a></li>
          <li><a href="/#why">About KMB</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="/#reviews">Reviews</a></li>
          <li><a href="/privacy">Privacy Policy</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">&copy; <span id="year">2026</span> KMB Electric LLC. All rights reserved. &#183; Licensed &amp; Insured &#183; Colorado Electrical Contractor #102799 &#183; Veteran Owned &amp; Operated</div>
  </div>
</footer>

<div class="tw" id="tw">
  <button class="tw-fab" id="tw-open" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="tw-panel"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span>Text us</span></button>
  <div class="tw-panel" id="tw-panel" role="dialog" aria-labelledby="tw-title" hidden>
    <div class="tw-head">
      <div><strong id="tw-title">Text KMB Electric</strong><span>Leave your number and Kyle texts you back.</span></div>
      <button class="tw-close" id="tw-close" type="button" aria-label="Close"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
    </div>
    <form class="tw-form" id="tw-form" novalidate>
      <label>Your name<input name="name" type="text" autocomplete="name" placeholder="First name is fine"></label>
      <label>Cell number<input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(719) 555-0100"></label>
      <label>What do you need?<textarea name="message" rows="3" placeholder="Panel keeps tripping, need an EV charger, hot tub going in next week..."></textarea></label>
      <button class="tw-send" id="tw-send" type="submit">Send text</button>
      <p class="tw-fine">Or text Kyle directly at <a href="{SMS}">{PHONE}</a>. Standard rates apply. We never sell your number.</p>
    </form>
  </div>
</div>
<a class="call-fab" href="{TEL}" aria-label="Call KMB Electric now"><i class="fa-solid fa-phone" aria-hidden="true"></i></a>

<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
<script src="/assets/site.js?v=4"></script>
{ANALYTICS}
</body>
</html>
"""

SERVICE_OPTIONS = [
    "Service or panel upgrade", "EV charger installation", "Hot tub or spa wiring",
    "Custom home or new construction", "Remodel, addition or basement finish",
    "Small scale commercial tenant finish", "Generator or transfer switch",
    "Lighting, circuits or a service call", "Something else",
]

def contact_section(preselect, heading, hint):
    opts = []
    for o in SERVICE_OPTIONS:
        sel = " selected" if o == preselect else ""
        opts.append(f"              <option{sel}>{o}</option>")
    first = '              <option value="" disabled>Choose a service</option>' if preselect else '              <option value="" disabled selected>Choose a service</option>'
    return f"""<section class="contact" id="contact">
  <div class="container">
    <h2 data-aos="fade-up">{heading}</h2>
    <div class="contact-grid">
      <div class="contact-info" data-aos="fade-up">
        <h3>Ready to talk?</h3>
        <p class="area">Proudly serving Colorado Springs and the surrounding Pikes Peak region.</p>
        <div class="c-row">
          <div class="ic"><i class="fa-solid fa-phone" aria-hidden="true"></i></div>
          <div><div class="lbl">Call or text</div><div class="val phone"><a href="{TEL}">{PHONE}</a></div><div class="note">Texts welcome. Send a photo of the panel or the job.</div></div>
        </div>
        <div class="c-row">
          <div class="ic"><i class="fa-solid fa-envelope" aria-hidden="true"></i></div>
          <div><div class="lbl">Email</div><div class="val"><a href="mailto:kylebashford@kmbelectric.com">kylebashford@kmbelectric.com</a></div></div>
        </div>
        <div class="c-row">
          <div class="ic"><i class="fa-solid fa-clock" aria-hidden="true"></i></div>
          <div><div class="lbl">Hours</div>
            <dl class="hours">
              <dt>Monday to Friday</dt><dd>7:00 AM to 5:00 PM</dd>
              <dt>Saturday</dt><dd>Closed</dd>
              <dt>Sunday</dt><dd>Closed</dd>
            </dl>
          </div>
        </div>
        <div class="c-row">
          <div class="ic"><i class="fa-solid fa-location-dot" aria-hidden="true"></i></div>
          <div><div class="lbl">Based in</div><div class="val">Colorado Springs, CO 80923</div></div>
        </div>
        <div class="areas">
          <div class="lbl">Also serving</div>
          <div class="chips">
            <span>Monument</span><span>Black Forest</span><span>Falcon</span><span>Peyton</span><span>Fountain</span><span>Security-Widefield</span><span>Manitou Springs</span><span>Woodland Park</span><span>Calhan</span>
          </div>
        </div>
      </div>
      <div class="form-card" data-aos="fade-up" data-aos-delay="100">
        <h3>Request a Free Estimate</h3>
        <p class="hint">{hint}</p>
        <form id="estimate-form" novalidate>
          <input type="text" name="_honey" class="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="field">
            <label for="f-name">Full Name</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required placeholder="Your name">
          </div>
          <div class="field">
            <label for="f-phone">Phone Number</label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="(719) 555-0100">
          </div>
          <div class="field">
            <label for="f-service">Service Needed</label>
            <select id="f-service" name="service" required>
{first}
{chr(10).join(opts)}
            </select>
          </div>
          <div class="field">
            <label for="f-msg">Anything else we should know? (optional)</label>
            <textarea id="f-msg" name="message" placeholder="Address, timeline, what you are seeing, anything that helps us quote it right."></textarea>
          </div>
          <button class="btn btn-primary" type="submit" id="f-submit">Send My Request <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></button>
          <p class="form-fine">No spam, no sales calls. Just Kyle or Melissa getting back to you.</p>
        </form>
      </div>
    </div>
  </div>
</section>
"""

def cta_banner(h2, sub):
    return f"""<section class="cta">
  <div class="container">
    <span class="section-label" data-aos="fade-up">Ready to get started?</span>
    <h2 data-aos="fade-up" data-aos-delay="80">{h2}</h2>
    <p class="sub" data-aos="fade-up" data-aos-delay="160">{sub}</p>
    <a class="cta-phone" href="{TEL}" data-aos="fade-up" data-aos-delay="200"><i class="fa-solid fa-phone" aria-hidden="true"></i>{PHONE}</a>
    <div class="cta-actions" data-aos="fade-up" data-aos-delay="250">
      <a class="btn btn-primary btn-lg" href="#contact">Book Your Free Estimate</a>
      <a class="btn btn-dark btn-lg" href="{SMS}"><i class="fa-solid fa-comment-sms" aria-hidden="true"></i>Text Us</a>
    </div>
    <p class="cta-reassure" data-aos="fade-up" data-aos-delay="300">Free estimates &#183; Licensed &amp; Insured &#183; Veteran Owned &#183; Permitted and inspected work</p>
  </div>
</section>
"""

def head(title, desc, path, og_image, ld_blocks):
    url = f"{SITE}{path}"
    ld = "\n".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=2)}\n</script>' for b in ld_blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KMB Electric LLC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/{og_image}">
{HEAD_LINKS}
{ld}
</head>
<body>
"""

def breadcrumb_ld(name, path):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path},
        ],
    }

def faq_ld(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }

def service_ld(name, desc, path, image=None):
    d = {
        "@context": "https://schema.org", "@type": "Service",
        "name": name, "serviceType": name, "description": desc, "url": SITE + path,
        "provider": {"@id": SITE + "/#business"},
        "areaServed": [{"@type": "City", "name": c} for c in ["Colorado Springs", "Monument", "Fountain", "Falcon", "Peyton", "Black Forest", "Woodland Park", "Manitou Springs"]],
    }
    if image:
        d["image"] = SITE + "/" + image
    return d

def faq_html(faqs):
    items = []
    for q, a in faqs:
        items.append(f"""      <details class="faq-item">
        <summary>{q}<i class="fa-solid fa-chevron-down" aria-hidden="true"></i></summary>
        <div class="faq-a"><p>{a}</p></div>
      </details>""")
    return "\n".join(items)

# ---------------------------------------------------------------- service content

SERVICES = {
 "ev-chargers": {
  "slug": "/ev-chargers",
  "name": "EV Charger Installation",
  "title": "EV Charger Installation in Colorado Springs | KMB Electric",
  "desc": "Level 2 EV charger installation in Colorado Springs by a licensed, veteran owned electrician. Sized to your panel and your vehicle, permitted and inspected. Free estimates, call or text 719-963-5191.",
  "label": "EV Charger Installation",
  "h1": "Charge at Home. <span class=\"accent\">Wake Up Full.</span>",
  "sub": "KMB Electric installs Level 2 EV chargers in garages and driveways across Colorado Springs and the Pikes Peak region, sized to your panel and your vehicle, permitted and inspected.",
  "image": "assets/work-ev-charger-install.jpg", "image_pos": "center 32%",
  "image_alt": "Level 2 EV wall charger installed beside an electrical panel in a residential garage",
  "preselect": "EV charger installation",
  "intro_h2": "What a Level 2 install from KMB includes",
  "intro_p": "A Level 2 charger runs on a dedicated 240 volt circuit, the same kind of circuit that feeds a dryer or a range. Done right it is a clean, permitted install that adds value to the house and charges most EVs overnight. Done wrong it trips breakers, overheats, or fails inspection when you sell. We do it right the first time.",
  "glance": [
   "A look at your panel and a load calculation, so the charger fits the service you have",
   "A dedicated 240 volt circuit, typically 40 to 60 amps depending on the charger",
   "Hardwired or a NEMA 14-50 outlet, inside the garage or weatherproof outside",
   "Any UL listed charger: Tesla Wall Connector, ChargePoint, Emporia, Wallbox, Grizzl-E and more",
   "Permit pulled and inspection passed through the Pikes Peak Regional Building Department",
   "Panel upgrade or load management options if your service is already near its limit",
  ],
  "steps": [
   ("Text us a photo of your panel", "A picture of the breaker panel with the cover on, plus where you park, tells us most of what we need."),
   ("Written estimate", "You get a clear scope and a straight price. We tell you if the panel can handle it or what it would take if it cannot."),
   ("Permit and install", "We pull the permit, run the circuit, mount the charger and test it with your vehicle. Most installs are finished in a day."),
   ("Inspection and paperwork", "The inspector signs off, you get the paperwork, and it shows clean on the permit record when you sell."),
  ],
  "faqs": [
   ("Can my panel handle an EV charger?", "Usually, yes. We do a load calculation on your existing service before quoting. Many 200 amp homes have room; a 100 amp service may need a smaller charger, a load management device or a panel upgrade. We tell you which before any work starts."),
   ("Hardwired or plug-in outlet?", "Both are fine when installed correctly. A hardwired charger is cleaner and required for some higher amperage units. A NEMA 14-50 outlet gives you flexibility if you change vehicles. We walk you through the trade off for your setup."),
   ("Do I need a permit for an EV charger in Colorado Springs?", "Yes. A new 240 volt circuit requires an electrical permit and inspection in Colorado Springs and El Paso County. We pull it and schedule the inspection as part of the job."),
   ("Can you install the charger outside?", "Yes. Outdoor installs use weather rated equipment and conduit, and we place the charger so the cable reaches your parking spot without crossing a walkway."),
   ("How long does the install take?", "Most garage installs are done in a single visit once the permit is issued. Longer runs, finished walls or a panel upgrade add time, and we tell you that in the estimate."),
   ("Which chargers do you install?", "Any UL listed Level 2 charger, including Tesla Wall Connector, ChargePoint Home Flex, Emporia, Wallbox and Grizzl-E. If you already bought one, we install it. If not, we recommend one that fits your vehicle and panel."),
  ],
  "related": [("/panel-upgrades", "Service &amp; Panel Upgrades"), ("/generators", "Generators &amp; Transfer Switches"), ("/hot-tubs", "Hot Tub &amp; Spa Wiring")],
  "cta_h2": "Ready to Charge at Home?",
  "cta_sub": "Text a photo of your panel and where you park. Kyle will tell you straight what it takes.",
 },
 "panel-upgrades": {
  "slug": "/panel-upgrades",
  "name": "Electrical Service and Panel Upgrades",
  "title": "Electrical Panel Upgrades in Colorado Springs | 200 Amp Service | KMB Electric",
  "desc": "Electrical panel and service upgrades in Colorado Springs. 100 to 200 amp upgrades, outdated panel replacement, sub panels and surge protection by a licensed, veteran owned electrician. Free estimates, 719-963-5191.",
  "label": "Service &amp; Panel Upgrades",
  "h1": "More Power. <span class=\"accent\">Safer Panel.</span>",
  "sub": "Older panels, tripping breakers and homes that need more capacity for EV chargers, hot tubs and AC. KMB Electric upgrades services, replaces outdated panels and adds the power your home actually needs.",
  "image": "assets/work-panel-conduit.jpg", "image_pos": "center",
  "image_alt": "Open breaker panel with metal conduit runs in an unfinished mechanical room",
  "preselect": "Service or panel upgrade",
  "intro_h2": "When a panel upgrade makes sense",
  "intro_p": "Most homes built before the 1990s came with 100 amp service, and many of those panels are at the end of their life. If you are adding an EV charger, a hot tub, central air or a shop, or if breakers trip when two big loads run at once, the panel is usually the bottleneck. Some older brands are a safety issue on their own and insurers increasingly ask for them to be replaced.",
  "glance": [
   "100 amp to 200 amp service upgrades, and 400 amp for larger homes and shops",
   "Replacement of outdated or recalled panels, including Federal Pacific and Zinsco",
   "New meter base and service entrance where needed, coordinated with your utility",
   "Sub panels for garages, basements, additions and detached buildings",
   "Whole house surge protection and clearly labeled circuits",
   "Permit, inspection and utility reconnect handled start to finish",
  ],
  "steps": [
   ("Panel check", "Send a photo or we come look. We check capacity, condition, grounding and what you plan to add."),
   ("Written estimate", "A clear scope with the amperage, the equipment and the price. No surprises on the day."),
   ("Utility and permit", "We pull the permit and coordinate the disconnect and reconnect with Colorado Springs Utilities or Mountain View Electric, whichever serves your address."),
   ("Install and inspection", "Power is off for part of a day while we set the new panel, land and label every circuit, and pass inspection."),
  ],
  "faqs": [
   ("How do I know if I need a panel upgrade?", "Common signs are breakers that trip often, a panel with no open spaces, flickering when big appliances start, a 100 amp service on a home you want to add an EV charger or hot tub to, or a panel brand with a known safety history. A quick look tells us which."),
   ("Will my power be off?", "Yes, for part of a day. The utility disconnects the service, we set the new panel and reconnect every circuit, the inspector signs off, and power comes back on. We schedule it so you know the window in advance."),
   ("Do you replace Federal Pacific and Zinsco panels?", "Yes. Those panels have a documented history of breakers failing to trip. Replacing one is a straightforward job and often a requirement for insurance or a home sale."),
   ("Do I need a permit?", "Yes. Service and panel work always requires an electrical permit and inspection in Colorado Springs and El Paso County. We pull the permit, meet the inspector and give you the paperwork."),
   ("Can I add a sub panel instead of upgrading the whole service?", "Sometimes. If your main service has capacity and you just need more breaker spaces in a garage or basement, a sub panel is the right answer. If the service itself is maxed out, the main has to be upgraded. The load calculation decides it."),
   ("Is whole house surge protection worth it?", "For most homes, yes. A panel mounted surge protector guards appliances, electronics and EV chargers from utility spikes and nearby lightning for a small added cost during an upgrade."),
  ],
  "related": [("/ev-chargers", "EV Charger Installation"), ("/generators", "Generators &amp; Transfer Switches"), ("/hot-tubs", "Hot Tub &amp; Spa Wiring")],
  "cta_h2": "Ready for a Panel That Keeps Up?",
  "cta_sub": "Text a photo of your panel. Kyle will tell you whether it needs replacing and what it would take.",
 },
 "hot-tubs": {
  "slug": "/hot-tubs",
  "name": "Hot Tub and Spa Wiring",
  "title": "Hot Tub Wiring in Colorado Springs | Spa Electrical Hookup | KMB Electric",
  "desc": "Hot tub and spa electrical hookups in Colorado Springs. Dedicated 240 volt circuits, GFCI disconnects and clean underground runs, permitted and inspected, by a licensed, veteran owned electrician. Call or text 719-963-5191.",
  "label": "Hot Tub &amp; Spa Wiring",
  "h1": "Spa Day Starts <span class=\"accent\">With Safe Power.</span>",
  "sub": "A hot tub needs its own 240 volt circuit, GFCI protection and a disconnect within sight. KMB Electric gets it wired, permitted and inspected so the tub is ready the day it arrives.",
  "image": None, "image_pos": "center",
  "image_alt": "",
  "preselect": "Hot tub or spa wiring",
  "intro_h2": "What a hot tub hookup involves",
  "intro_p": "Water and electricity are an unforgiving combination, which is why the code for spas is specific. Most tubs call for a dedicated 240 volt circuit, commonly 50 or 60 amps, with GFCI protection, a disconnect you can see from the tub and at least five feet from the water, proper bonding, and a buried run in conduit from the house. We handle all of it and coordinate with your spa dealer on the exact requirements for your model.",
  "glance": [
   "Dedicated 240 volt circuit sized to the manufacturer spec, commonly 50 or 60 amps",
   "GFCI protected disconnect in sight of the tub and at least five feet from the water",
   "Underground run in conduit from the panel to the pad, trenched and backfilled clean",
   "Bonding of the tub and nearby metal as the code requires",
   "120 volt plug and play tubs on a dedicated GFCI circuit where that is what you bought",
   "Permit pulled and inspection scheduled before your first soak",
  ],
  "steps": [
   ("Tell us about the tub", "Send the model or the dealer spec sheet and a photo of where it is going and where your panel is."),
   ("Written estimate", "Circuit size, route, disconnect location and a clear price. We flag it early if your panel needs capacity."),
   ("Rough in before delivery", "We trench, run conduit and set the disconnect so the pad is ready when the tub shows up."),
   ("Hookup and inspection", "Once the tub is set we make the final connections, test the GFCI and pass inspection."),
  ],
  "faqs": [
   ("What does a hot tub need electrically?", "Most full size tubs need a dedicated 240 volt circuit, commonly 50 or 60 amps, with GFCI protection and a disconnect in sight of the tub. Smaller plug and play models run on a dedicated 120 volt GFCI circuit. Your spa manual lists the exact requirement and we match it."),
   ("Can I just plug my hot tub in?", "Only if it is a 120 volt plug and play model, and even then it should be on its own GFCI protected circuit, not shared with a garage or patio outlet. Anything 240 volt has to be hardwired through a disconnect."),
   ("When should I call the electrician?", "Before the tub is delivered. We can trench and rough in the circuit ahead of time so the pad is ready, then finish the connection once the tub is set."),
   ("Do I need a permit for hot tub wiring in Colorado Springs?", "Yes. A new spa circuit requires an electrical permit and inspection. We pull it and handle the inspection as part of the job."),
   ("How far from the house can the tub be?", "As far as you like, within reason. Longer runs need larger wire and a longer trench, which affects the price, so tell us the spot early and we will quote it accurately."),
   ("Can my panel handle a hot tub?", "Many can. A 50 or 60 amp circuit is a significant load, so we check your service first. If it is already near capacity we will show you the options, including a panel upgrade if that is what it takes."),
  ],
  "related": [("/panel-upgrades", "Service &amp; Panel Upgrades"), ("/ev-chargers", "EV Charger Installation"), ("/generators", "Generators &amp; Transfer Switches")],
  "cta_h2": "Tub on Order?",
  "cta_sub": "Send the spec sheet and a photo of the spot. We will have the power ready before it arrives.",
 },
 "generators": {
  "slug": "/generators",
  "name": "Standby Generators and Transfer Switches",
  "title": "Standby Generator Installation in Colorado Springs | Transfer Switches | KMB Electric",
  "desc": "Standby generator and transfer switch installation in Colorado Springs and the Front Range. Generac and other whole home generators, automatic transfer switches and portable generator interlocks, permitted and inspected. Call or text 719-963-5191.",
  "label": "Generators &amp; Transfer Switches",
  "h1": "When the Grid Goes Down, <span class=\"accent\">Your House Does Not.</span>",
  "sub": "Standby generators with automatic transfer switches, sized to the loads you want covered, installed and coordinated with the utility by KMB Electric.",
  "image": "assets/work-generator-install.jpg", "image_pos": "center 62%",
  "image_alt": "Generac standby generator on a concrete pad beside a control cabinet in an open field",
  "preselect": "Generator or transfer switch",
  "intro_h2": "Whole home or just the essentials",
  "intro_p": "Front Range storms, wind and wildfire season all take the power out, and rural properties on wells and electric heat feel it first. A standby generator with an automatic transfer switch starts itself within seconds of an outage and shuts down when the utility comes back. We handle the electrical side end to end: the transfer switch, the wiring, the pad placement and the permit. The fuel line is run by a licensed gas fitter we coordinate with.",
  "glance": [
   "Whole home standby generators and automatic transfer switches, Generac and other major brands",
   "Essential circuits packages when you only need the well, furnace, fridge and a few rooms",
   "Load calculation so the generator is sized right, not oversold",
   "Manual transfer switches and interlock kits for portable generators, the safe way to backfeed",
   "Pad location, clearances and utility coordination handled for you",
   "Permit and inspection included, with a startup test before we leave",
  ],
  "steps": [
   ("Walk through", "We look at your panel, what you need to keep running and where the generator can sit, then talk through whole home versus essentials."),
   ("Written estimate", "Generator size, transfer switch, electrical scope and price in one document. Gas line is quoted separately by the gas fitter."),
   ("Install", "We set the transfer switch, run the wiring, and coordinate the pad, the gas connection and the utility."),
   ("Startup and inspection", "Startup test under load, inspection signed off, and a quick lesson on the controls."),
  ],
  "faqs": [
   ("Whole home generator or essential circuits only?", "It depends on what you cannot do without. Many families are covered by a smaller unit that runs the well pump, furnace, refrigerator, a few lights and outlets. Others want everything including AC. We do a load calculation and show you both options with real numbers."),
   ("What fuel do standby generators use?", "Natural gas where it is available, propane where it is not. The generator ties into your existing supply. A licensed gas fitter runs the line and we coordinate the timing so the install goes smoothly."),
   ("Can I use my portable generator instead?", "Yes, safely, with a manual transfer switch or an interlock kit on your panel. That lets you power selected circuits without the extension cords and without the risk of backfeeding the utility lines. We install both."),
   ("Do I need a permit?", "Yes. The transfer switch and generator wiring require an electrical permit and inspection, and the gas connection has its own. We pull the electrical permit and coordinate the rest."),
   ("How long does a standby generator install take?", "Usually one to two days on site once the generator and permit are in hand, plus the gas fitter's visit. Lead times on the generator itself vary by model, so starting before storm season is smart."),
   ("Do you service generators after the install?", "We handle the electrical side and can point you to the manufacturer's maintenance schedule and dealer service for the engine. Call us any time something electrical does not behave."),
  ],
  "related": [("/panel-upgrades", "Service &amp; Panel Upgrades"), ("/ev-chargers", "EV Charger Installation"), ("/hot-tubs", "Hot Tub &amp; Spa Wiring")],
  "cta_h2": "Ready to Stop Worrying About Outages?",
  "cta_sub": "Tell us what has to stay on. Kyle will size it and give you a straight price.",
 },
}

REVIEW_SNIPPET = """<section class="svc-review">
  <div class="container">
    <div class="svc-review-card" data-aos="fade-up">
      <div class="t-stars" aria-label="Five stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p class="t-quote">Kyle and his crew at KMB Electric were recommended to me by a buddy to do an electrical upgrade and air conditioning connect on my house. Very professional, time conscious and always kept me updated. More than competitively priced, and the quality of work was beyond top notch.</p>
      <div class="t-sep"></div>
      <div class="t-who"><span class="t-name">Ryan F.</span><span class="t-src">via Angi</span></div>
      <a class="svc-review-more" href="/#reviews">Read more reviews <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
    </div>
  </div>
</section>
"""

def service_page(key):
    s = SERVICES[key]
    path = s["slug"]
    ld = [breadcrumb_ld(s["name"], path), service_ld(s["name"], s["desc"], path, s["image"]), faq_ld(s["faqs"])]
    og = s["image"] or "assets/og.png"
    hero_style = ""
    hero_cls = "page-hero"
    if s["image"]:
        hero_style = f' style="--hero-img:url(\'/{s["image"]}\');--hero-pos:{s["image_pos"]}"'
        hero_cls += " has-photo"
    glance = "\n".join(f'        <li><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>{g}</span></li>' for g in s["glance"])
    steps = "\n".join(
        f'      <li class="step" data-aos="fade-up" data-aos-delay="{i*80}"><span class="step-n">{i+1}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (t, d) in enumerate(s["steps"]))
    related = "\n".join(f'        <a class="related-link" href="{h}">{l} <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>' for h, l in s["related"])
    body = f"""{header("services")}
<main id="top">

<section class="{hero_cls}"{hero_style}>
  <div class="container page-hero-inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/#services">Services</a><span>/</span><span aria-current="page">{s["label"]}</span></nav>
    <p class="hero-label">{s["label"]} in Colorado Springs</p>
    <h1 class="page-h1">{s["h1"]}</h1>
    <p class="page-sub">{s["sub"]}</p>
    <div class="hero-ctas is-in">
      <a class="btn btn-primary" href="#contact">Get Your Free Estimate</a>
      <a class="btn btn-outline" href="{TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i>Call or Text {PHONE}</a>
    </div>
    <p class="hero-trust"><span class="stars" aria-label="Five stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5.0 Google Rating <span class="dot">&#183;</span> Licensed &amp; Insured <span class="dot">&#183;</span> Permitted &amp; Inspected <span class="dot">&#183;</span> Military Discounts</p>
  </div>
</section>

<section class="svc-intro">
  <div class="container svc-grid">
    <div data-aos="fade-up">
      <span class="section-label">The Job</span>
      <h2>{s["intro_h2"]}</h2>
      <p class="svc-p">{s["intro_p"]}</p>
    </div>
    <aside class="glance" data-aos="fade-up" data-aos-delay="100">
      <h3>At a glance</h3>
      <ul class="checklist">
{glance}
      </ul>
    </aside>
  </div>
</section>

<section class="svc-steps">
  <div class="container">
    <div class="section-head" data-aos="fade-up">
      <span class="section-label">How It Works</span>
      <h2>Four steps, no runaround</h2>
    </div>
    <ol class="steps">
{steps}
    </ol>
  </div>
</section>

{REVIEW_SNIPPET}
<section class="svc-faq" id="faq">
  <div class="container">
    <div class="section-head" data-aos="fade-up">
      <span class="section-label">Questions</span>
      <h2>{s["name"]} FAQ</h2>
    </div>
    <div class="faq-list" data-aos="fade-up">
{faq_html(s["faqs"])}
    </div>
    <div class="related" data-aos="fade-up">
      <span class="related-label">Related services</span>
      <div class="related-links">
{related}
      </div>
    </div>
  </div>
</section>

{cta_banner(s["cta_h2"], s["cta_sub"])}
{contact_section(s["preselect"], "Get In Touch", "Four quick fields. We call or text back during business hours.")}
</main>

{FOOTER}"""
    html = head(s["title"], s["desc"], path, og, ld) + body
    return html

# ---------------------------------------------------------------- projects gallery

PHOTOS = [
    ("assets/work-soffit-lighting.jpg", "Exterior soffit and accent lighting", "Stone and stucco home exterior with new soffit and accent lighting along the gable and roofline"),
    ("assets/work-ev-charger-install.jpg", "Level 2 EV charger installation", "Level 2 wall charger installed beside an electrical panel in a residential garage"),
    ("assets/work-generator-install.jpg", "Standby generator installation", "Generac standby generator on a concrete pad beside a control cabinet in an open field"),
    ("assets/work-panel-conduit.jpg", "Electrical panel and conduit work", "Open breaker panel with metal conduit runs in an unfinished mechanical room"),
    ("assets/work-boom-lift.jpg", "Elevated exterior electrical work", "Two KMB crew members in hard hats and safety vests working from a boom lift in a residential development"),
    ("assets/work-service-fleet.jpg", "The KMB service fleet on site", "Three KMB service vans parked in front of a red barn workshop at a rural job site"),
]

def projects_page():
    path = "/projects"
    title = "Recent Electrical Projects in Colorado Springs | KMB Electric"
    desc = "Real jobs by KMB Electric: panel upgrades, EV chargers, standby generators, exterior lighting and more across Colorado Springs and the Pikes Peak region. Veteran owned, licensed and insured."
    ld = [breadcrumb_ld("Projects", path), {
        "@context": "https://schema.org", "@type": "ImageGallery", "name": "KMB Electric recent projects", "url": SITE + path,
        "image": [{"@type": "ImageObject", "contentUrl": f"{SITE}/{src}", "caption": cap, "description": alt} for src, cap, alt in PHOTOS],
    }]
    figs = "\n".join(
        f"""      <figure class="g-item" data-aos="fade-up" data-aos-delay="{(i%3)*70}">
        <a href="/{src}" data-caption="{cap}" data-alt="{alt}"><img src="/{src}" alt="{alt}" loading="lazy" decoding="async"></a>
        <figcaption>{cap}</figcaption>
      </figure>""" for i, (src, cap, alt) in enumerate(PHOTOS))
    body = f"""{header("projects")}
<main id="top">

<section class="page-hero">
  <div class="container page-hero-inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Projects</span></nav>
    <p class="hero-label">Recent Work</p>
    <h1 class="page-h1">Real Jobs. <span class="accent">Real Photos.</span></h1>
    <p class="page-sub">Every picture here is a KMB job in the Colorado Springs area, shot by the crew that did the work. New projects get added as they finish.</p>
    <div class="hero-ctas is-in">
      <a class="btn btn-primary" href="#contact">Get Your Free Estimate</a>
      <a class="btn btn-outline" href="{TEL}"><i class="fa-solid fa-phone" aria-hidden="true"></i>Call or Text {PHONE}</a>
    </div>
  </div>
</section>

<section class="gallery-section">
  <div class="container">
    <div class="gallery">
{figs}
    </div>
    <p class="gallery-note" data-aos="fade-up"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> Want to see work like yours? Tell us the job and we will share examples.</p>
  </div>
</section>

<dialog id="lightbox" class="lightbox" aria-label="Project photo">
  <button class="lb-close" type="button" aria-label="Close">&times;</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
</dialog>

{cta_banner("Have a Project in Mind?", "Call, text or send the form. Kyle or Melissa will get back to you with a clear scope and a straight price.")}
{contact_section("", "Get In Touch", "Four quick fields. We call or text back during business hours.")}
</main>

{FOOTER}"""
    return head(title, desc, path, "assets/work-soffit-lighting.jpg", ld) + body

# ---------------------------------------------------------------- subpage CSS

SUBPAGE_CSS = """
/* ===== Subpages (service pages, projects, FAQ) ===== */
.page-hero{position:relative;overflow:hidden;background:linear-gradient(135deg,var(--navy) 0%,var(--navy-3) 55%,var(--gold-deep) 130%);color:var(--white);padding:150px 0 70px;min-height:60vh;display:flex;align-items:center}
.page-hero.has-photo::before{content:'';position:absolute;inset:0;background-image:var(--hero-img);background-size:cover;background-position:var(--hero-pos,center);opacity:.38;z-index:0}
.page-hero::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,18,32,.55) 0%,rgba(11,18,32,.35) 50%,rgba(11,18,32,.85) 100%);z-index:0}
.page-hero-inner{position:relative;z-index:1;max-width:860px}
.page-hero .hero-label{justify-content:flex-start;margin-bottom:16px}
.page-hero .hero-label::before{display:none}
.page-h1{font-size:64px;line-height:1.02;color:var(--white);margin-bottom:18px;text-wrap:balance}
.page-h1 .accent{color:var(--gold)}
.page-sub{font-size:19px;line-height:1.6;color:rgba(255,255,255,.85);max-width:640px;margin-bottom:30px}
.page-hero .hero-ctas{justify-content:flex-start;opacity:1}
.page-hero .hero-trust{justify-content:flex-start}
.breadcrumbs{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:13px;color:rgba(255,255,255,.6);margin-bottom:18px}
.breadcrumbs a:hover{color:var(--gold)}
.breadcrumbs span{opacity:.6}
.breadcrumbs [aria-current]{color:rgba(255,255,255,.85);opacity:1}
.nav-links a.is-active{color:var(--gold)}

.svc-intro{background:var(--cream);padding:90px 0}
.svc-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:start}
.svc-intro h2{font-size:44px;color:var(--navy);margin:14px 0 18px;line-height:1.1}
.svc-p{font-size:18px;line-height:1.75;color:var(--ink)}
.glance{background:var(--white);border:1px solid var(--cream-2);border-radius:18px;padding:30px 30px 18px;box-shadow:0 14px 34px rgba(15,23,42,.08)}
.glance h3{font-size:24px;color:var(--navy);margin-bottom:16px}
.glance .checklist li{font-size:16px;margin-bottom:12px}

.svc-steps{background:var(--white);padding:90px 0}
.svc-steps .section-head h2{color:var(--navy)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;list-style:none;margin:0;padding:0}
.step{position:relative;background:var(--cream);border-radius:16px;padding:30px 24px 26px;border:1px solid var(--cream-2)}
.step-n{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--gold);color:var(--navy);font-family:var(--display);font-size:20px;font-weight:700;margin-bottom:16px}
.step h3{font-size:22px;color:var(--navy);margin-bottom:8px}
.step p{font-size:15px;color:var(--muted);line-height:1.6}

.svc-review{background:var(--navy);padding:70px 0;color:var(--white)}
.svc-review-card{max-width:820px;margin:0 auto;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:34px}
.svc-review-more{display:inline-flex;align-items:center;gap:8px;color:var(--gold);font-weight:600;font-size:14px;margin-top:18px}
.svc-review-more:hover i{transform:translateX(4px)}
.svc-review-more i{transition:transform .3s var(--ease)}

.svc-faq,.faq{background:var(--cream);padding:90px 0}
.svc-faq .section-head h2,.faq .section-head h2{color:var(--navy)}
.faq-list{max-width:860px}
.faq-item{background:var(--white);border:1px solid var(--cream-2);border-radius:14px;margin-bottom:12px;overflow:hidden}
.faq-item summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px 22px;font-family:var(--display);font-size:22px;font-weight:700;color:var(--navy)}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary i{color:var(--gold);font-size:14px;transition:transform .3s var(--ease);flex:none}
.faq-item[open] summary i{transform:rotate(180deg)}
.faq-a{padding:0 22px 20px}
.faq-a p{font-size:16px;line-height:1.7;color:var(--ink)}
.related{margin-top:40px}
.related-label{display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-bottom:12px}
.related-links{display:flex;flex-wrap:wrap;gap:12px}
.related-link{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:100px;background:var(--white);border:1px solid var(--cream-2);color:var(--navy);font-weight:600;font-size:14px;transition:border-color .2s,transform .2s}
.related-link:hover{border-color:var(--gold);transform:translateY(-2px)}

.gallery-section{background:var(--cream);padding:80px 0}
.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.g-item{margin:0;background:var(--white);border-radius:16px;overflow:hidden;border:1px solid var(--cream-2);box-shadow:0 14px 34px rgba(15,23,42,.08)}
.g-item a{display:block;aspect-ratio:4/3;overflow:hidden;background:var(--navy-3)}
.g-item img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.g-item:hover img{transform:scale(1.04)}
.g-item figcaption{padding:14px 16px;font-size:14px;font-weight:600;color:var(--navy)}
.gallery-note{margin-top:28px;display:flex;align-items:center;gap:12px;font-size:15px;color:var(--muted)}
.gallery-note i{color:var(--gold)}
.lightbox{border:0;padding:0;background:transparent;max-width:min(1100px,94vw);width:auto}
.lightbox::backdrop{background:rgba(11,18,32,.9)}
.lightbox figure{margin:0;position:relative}
.lightbox img{max-width:94vw;max-height:84vh;width:auto;height:auto;border-radius:12px;display:block;margin:0 auto}
.lightbox figcaption{color:var(--white);text-align:center;padding:12px;font-size:15px}
.lb-close{position:fixed;top:16px;right:20px;width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.14);color:var(--white);font-size:28px;line-height:1;cursor:pointer;z-index:2}
.lb-close:hover{background:rgba(255,255,255,.3)}

.review-cta{display:inline-flex;align-items:center;gap:10px;margin-top:22px}

@media(max-width:1000px){
  .steps{grid-template-columns:1fr 1fr}
  .gallery{grid-template-columns:1fr 1fr}
}
@media(max-width:900px){
  .svc-grid{grid-template-columns:1fr;gap:36px}
}
@media(max-width:767px){
  .page-hero{padding:120px 0 56px;min-height:0}
  .page-h1{font-size:40px}
  .page-sub{font-size:17px}
  .svc-intro h2{font-size:32px}
  .svc-intro,.svc-steps,.svc-faq,.faq,.gallery-section{padding:64px 0}
  .steps{grid-template-columns:1fr}
  .gallery{grid-template-columns:1fr}
  .faq-item summary{font-size:19px;padding:16px 18px}
  .faq-a{padding:0 18px 16px}
}
"""

def main():
    out = {}
    for key in SERVICES:
        out[key + ".html"] = service_page(key)
    out["projects.html"] = projects_page()
    for name, html in out.items():
        assert not re.search("[–—]", html), f"dash in {name}"
        open(name, "w").write(html)
        print("wrote", name, len(html), "bytes")
    css = open("assets/site.css").read()
    if "===== Subpages" not in css:
        open("assets/site.css", "a").write(SUBPAGE_CSS)
        print("appended subpage css")
    else:
        print("subpage css already present (edit it in assets/site.css directly)")

if __name__ == "__main__":
    main()
