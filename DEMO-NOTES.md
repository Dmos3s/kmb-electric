# Demo notes for Dan

Built 2026-09-13 overnight for the Kyle Bashford demo. Everything here is what to say and what to swap before this goes live on kmbelectric.com.

## What is real (verified from public listings)

- Phone 719-963-5191, email kylebashford@kmbelectric.com, Colorado Springs 80922, veteran owned, military discounts. All from his current GoDaddy site and Google listing.
- Hours Mon to Fri 7 to 5, Sat 9 to 3, Sun closed (Angi/HomeAdvisor listing; his old site left Saturday blank, confirm with Kyle).
- Colorado Electrical Contractor license #102799 and Castle Rock CR26-0392 (BuildZoom license verification, June and August 2026).
- 118 permitted projects over three years, top 3 percent of Colorado contractors, BuildZoom score 112 of 55,949 (BuildZoom permit data).
- 5.0 rating on Google (11 reviews), Angi and HomeAdvisor (2 reviews each).
- All five testimonials are real reviews, quoted from Google and Angi with names as shown publicly. Two Google reviews were truncated on the listing, so they end at the last full sentence.
- The logo is his actual shield-and-bolt PNG from the old site.
- Services list is the union of his old site, his Angi profile, and the work types in his permit history (400 amp services, generators, hot tubs, EV chargers, kitchen and basement remodels, ADUs).
- "Melissa" is named in a Google review as his scheduler. If that is wrong, remove her from the CTA and form copy.

## What is sample or assumed (tell Kyle)

- Photos are stock (Unsplash) placeholders. Kyle has 37 photos on his Google listing; swap those in, especially the four "recent work" collage tiles, which are captioned with job types from his permit record but are not photos of those jobs.
- The four collage captions name real permit cities and job types (Denver 400 amp, Colorado Springs EV, Old Colorado City kitchen, Monument generator) but the photos are not his.
- "Warranty on our workmanship" comes from his Angi profile ("Warranties: Yes"); confirm terms.
- Facebook and Instagram footer icons point at facebook.com and instagram.com; his old site only had GoDaddy placeholders. Replace with real pages or delete.
- Privacy policy is a plain default.

## Lead form

The estimate form posts to FormSubmit using Dan's already-activated hash, so demo submissions land in daniel.g.moses@gmail.com with subject "KMB Electric estimate request: <service>". No Doll rule fires on that subject.

To route leads to Kyle at go-live: change `ENDPOINT` in `index.html` to `https://formsubmit.co/ajax/kylebashford@kmbelectric.com`, submit once, and have Kyle click the activation email. Or point it at whatever CRM he picks later.

## Hosting

- Source: GitHub `Dmos3s/kmb-electric` (public, static, no secrets).
- Demo URL: GitHub Pages at https://dmos3s.github.io/kmb-electric/ (and a Vercel temporary URL if that step worked, see the session summary).
- Go-live options once Kyle signs: Vercel or Lovable passthrough like Swann's Nest, then point kmbelectric.com at it.

## Domain (Kyle keeps kmbelectric.com)

The domain is registered at GoDaddy and currently serves GoDaddy Website Builder. At cutover:

1. Kyle stays the registrant. Nothing transfers.
2. In GoDaddy DNS, change the A record for `@` and the CNAME for `www` to the new host (Vercel: A 76.76.21.21 and CNAME cname.vercel-dns.com; Lovable: A 185.158.133.1 plus its TXT verification).
3. Keep his GoDaddy email/MX records untouched so kylebashford@kmbelectric.com keeps working. Check whether email is GoDaddy Workspace or Microsoft 365 before touching DNS.
4. Cancel the Website Builder subscription only after the new site is live on the domain.
5. Add the site to Google Search Console and Bing, submit `sitemap.xml`, and set the website URL on his Google Business Profile.

## Ideas for the pitch

- CRM: his Google reviews mention scheduling and follow-up, so a simple lead inbox plus text-back (the same Doll lead-text pattern used for Swann's Nest and Brenda) is an easy add.
- Review funnel: a "leave us a review" link straight to his Google listing on the invoice or a thank-you text.
- Service pages for SEO (EV chargers, hot tubs, panel upgrades) each with its own URL once the design is approved.
