# KMB Electric LLC website

Marketing site for KMB Electric LLC, a veteran owned electrical contractor in Colorado Springs, CO. Owner: Kyle Bashford. Built by FuseHQ, September 2026, to replace the old GoDaddy Website Builder page at kmbelectric.com.

## What is in here

- `index.html`: the whole site, one page, all CSS and JS inline. Sections: nav, hero, trust marquee, stats, services, why KMB, reviews, estimate CTA, contact + form, footer.
- `privacy.html`: privacy policy linked from the footer.
- `assets/`: Kyle's shield-and-bolt logo (pulled from the old site), favicons, and `og.png` for link previews.
- `robots.txt`, `sitemap.xml`, `llms.txt`: search and AI crawler files, all pointed at https://kmbelectric.com.
- `vercel.json`: clean URLs and long cache for assets when hosted on Vercel.
- `BUSINESS-FACTS.md`: every fact used on the site and where it came from.
- `DEMO-NOTES.md`: what is real, what is sample, and the go-live checklist.

No build step. Any static host works. Locally: `python3 -m http.server 8765` in this folder.

## Libraries (CDN)

GSAP 3.12, Splitting.js, AOS 2.3, Swiper 11, Lenis 1.0.42, tsParticles 2.12, Vanilla Tilt 1.8, Font Awesome 6.4, Google Fonts (Barlow Condensed + Inter).

## Design

Navy `#0B1220` base, gold `#D9A63A` accent taken from Kyle's logo, warm off-white `#F6F3EC` sections. Barlow Condensed for headlines, Inter for body. Section rhythm alternates dark and light.

## Lead form

The estimate form posts to FormSubmit (ajax) and shows an inline confirmation. See `DEMO-NOTES.md` for where leads go now and how to point them at Kyle.
