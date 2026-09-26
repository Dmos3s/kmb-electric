# kmbelectric.com cutover to the new site (GitHub Pages)

Prepared 2026-09-25. Current DNS is at GoDaddy (ns05/ns06.domaincontrol.com). Email is Microsoft 365 through GoDaddy: MX kmbelectric-com.mail.protection.outlook.com, SPF "v=spf1 include:secureserver.net -all", TXT NETORGFT15025653.onmicrosoft.com, CNAME autodiscover, CNAME email. NONE of those change.

## 1. In GoDaddy DNS (Dan, logged in as Kyle)

Delete the two A records for @ (they point at GoDaddy Website Builder):
- A  @  76.223.105.230
- A  @  13.248.243.5

Add four A records for @ (GitHub Pages), TTL 600:
- A  @  185.199.108.153
- A  @  185.199.109.153
- A  @  185.199.110.153
- A  @  185.199.111.153

Edit the www record: CNAME  www  ->  dmos3s.github.io  (it currently points at kmbelectric.com)

Touch nothing else. Leave MX, all TXT, autodiscover, email, _domainconnect, and any Microsoft records alone.

## 2. On GitHub (Fable, right after step 1)

    gh api -X PUT repos/Dmos3s/kmb-electric/pages -f cname=kmbelectric.com
    # wait for the DNS check, then once the certificate is issued:
    gh api -X PUT repos/Dmos3s/kmb-electric/pages -F https_enforced=true

The demo URL https://dmos3s.github.io/kmb-electric/ then redirects to https://kmbelectric.com/.

## 3. Verify

- https://kmbelectric.com/ and https://www.kmbelectric.com/ return 200 with the new site, padlock valid.
- https://kmbelectric.com/privacy.html, /assets/og.png, /robots.txt, /sitemap.xml all 200.
- Estimate form: submit once with ?test=1 on the URL. FormSubmit activates per host, so the first submission from kmbelectric.com triggers an "Activate Form" email to Dan; open it, then resubmit. The Text-us bubble hits the Hermes bridge, which already allows the kmbelectric.com origin.
- Kyle still receives email (MX untouched); ask him to send one to be sure.

## 4. After

- Cancel the GoDaddy Website Builder subscription (Kyle), not the domain and not the email.
- Google Search Console: Kyle's own verification TXT is already on the domain. Dan's verification file google76fd77a199aeb7be.html and BingSiteAuth.xml are in this repo so Dan can add the property under his accounts too, then submit sitemap.xml in both.
- Update the website link on Kyle's Google Business Profile if it is not already kmbelectric.com.
