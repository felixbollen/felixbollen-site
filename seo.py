"""SEO helpers for felixbollen.com: structured data (JSON-LD), sitemap, robots, llms.txt.
Imported by build.py. Content comes from content/*.json; nothing here needs editing for new projects."""
import json, os, re, html
from datetime import date, datetime, timezone

SITE = "https://felixbollen.com"
PID = SITE + "/#felix"          # Person @id
WID = SITE + "/#website"
SID = SITE + "/#services"       # ProfessionalService @id

# Country / schema type per project (falls back to CreativeWork subject "Organization").
VENUE = {
    "german-kraft": ("Brewery", "London", "GB"),
    "german-kraft-mayfair": ("Brewery", "London", "GB"),
    "kraft-dalston": ("BarOrPub", "London", "GB"),
    "jim-and-tonic": ("Organization", "London", "GB"),
    "the-lokal": ("BarOrPub", "Hounslow, London", "GB"),
    "gleis-garten": ("FoodEstablishment", "Vienna", "AT"),
    "vienna-kraft": ("Brewery", "Vienna", "AT"),
    "model-market": ("FoodEstablishment", "London", "GB"),
    "dufte-berlin": ("FoodEstablishment", "Berlin", "DE"),
    "emancipator-baralku": ("MusicAlbum", None, None),
    "the-square-gallery": ("ArtGallery", "London", "GB"),
}

KNOWS = [
    "Graphic design", "Brand identity design", "Logo design", "Corporate design", "Packaging design",
    "Beer label design", "Menu and print design", "Signage and wayfinding", "Art direction", "Venue concepts",
    "Hospitality branding", "Restaurant and bar branding", "Brewery branding", "Food market branding",
    "Marketing strategy", "Go-to-market and positioning", "Launch campaigns", "Event and festival marketing",
    "Social media marketing", "Paid social (Meta Ads)", "Google Ads", "CRM and email marketing",
    "Public relations", "Ticketing and event sales", "Website design (Webflow, Squarespace)",
    "Photo and video direction", "Fractional CMO", "Hospitality management",
]

SERVICES = [
    ("Brand identity & logo design", "Logos, corporate design and complete brand identities, built from scratch."),
    ("Packaging, labels & print", "Beer labels, cans, bottles, gift boxes, menus, posters and merchandise."),
    ("Art direction & venue concepts", "The look and feel of a whole venue or business: shopfront, interior details, signage, glassware and online presence."),
    ("Marketing strategy & launches", "Positioning, go-to-market plans and launch campaigns, measured against the P&L."),
    ("Social media, paid ads & CRM", "Meta and Google Ads, social content, email marketing and CRM (Mailchimp, Zoho)."),
    ("PR & press", "Press releases, media relations and working with PR agencies."),
    ("Events, festivals & ticketing", "Event concepts, festival marketing and ticket sales."),
    ("Websites", "Simple, fast websites on Webflow, Squarespace or custom-built."),
    ("Photo & video direction", "Briefing and directing photographers, videographers and creators."),
    ("Part-time / fractional CMO", "A senior marketing lead for a few days a week, remote or on site."),
]

def ab(u, media=""):
    """Absolute URL for a site path (media served from GitHub Pages when configured)."""
    if not u: return ""
    if u.startswith("http"): return u
    return (media or SITE) + u if re.match(r"^/(a|v|ds|media|press)/", u) and media else SITE + u

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"

def person(home, media=""):
    return {
        "@type": "Person", "@id": PID, "name": "Felix Bollen", "givenName": "Felix", "familyName": "Bollen",
        "url": SITE + "/", "email": "mailto:" + home.get("email", ""),
        "image": ab(home.get("about_image") or "/og.jpg", media),
        "jobTitle": ["Graphic Designer", "Art Director", "Marketing Consultant"],
        "description": "Freelance graphic designer, art director and marketing consultant based in Berlin and London. Co-founder of German Kraft Brewery (London) and Gleis//Garten (Vienna).",
        "knowsAbout": KNOWS,
        "knowsLanguage": [{"@type": "Language", "name": "German", "alternateName": "de"}, {"@type": "Language", "name": "English", "alternateName": "en"}],
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "London College of Communication, University of the Arts London", "alternateName": "UAL LCC", "url": "https://www.arts.ac.uk/colleges/london-college-of-communication"},
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "BA (Hons) Graphic & Media Design"},
        "homeLocation": [{"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Berlin", "addressCountry": "DE"}},
                         {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"}}],
        "hasOccupation": [
            {"@type": "Occupation", "name": "Graphic Designer", "occupationLocation": [{"@type": "City", "name": "Berlin"}, {"@type": "City", "name": "London"}], "skills": "Brand identity, logo design, packaging, print, signage, websites"},
            {"@type": "Occupation", "name": "Marketing Consultant", "occupationLocation": [{"@type": "City", "name": "Berlin"}, {"@type": "City", "name": "London"}], "skills": "Go-to-market, campaigns, paid social, CRM, PR, event marketing"},
            {"@type": "Occupation", "name": "Art Director", "skills": "Venue concepts, brand worlds, photo and video direction"},
        ],
        "sameAs": [u for u in home.get("same_as", []) if u],
    }

def website():
    return {"@type": "WebSite", "@id": WID, "url": SITE + "/", "name": "Felix Bollen", "alternateName": ["felixbollen.com", "Felix Bollen Portfolio"],
            "inLanguage": "en-GB", "publisher": {"@id": PID}, "about": {"@id": PID}}

def service():
    return {"@type": "ProfessionalService", "@id": SID, "name": "Felix Bollen – Graphic Design, Art Direction & Marketing",
            "url": SITE + "/services/", "image": SITE + "/og.jpg", "logo": SITE + "/logo-512.png", "founder": {"@id": PID}, "employee": {"@id": PID},
            "description": "Freelance graphic design, branding, art direction and marketing for hospitality, drinks, culture and small businesses. Berlin, London and remote.",
            "address": {"@type": "PostalAddress", "addressLocality": "Berlin", "addressCountry": "DE"},
            "areaServed": [{"@type": "City", "name": n} for n in ("Berlin", "London", "Vienna", "Hamburg", "Munich")] + [{"@type": "Country", "name": n} for n in ("Germany", "Austria", "Switzerland", "United Kingdom")],
            "availableLanguage": ["German", "English"], "knowsAbout": KNOWS, "priceRange": "££",
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d, "provider": {"@id": PID}}} for n, d in SERVICES]}}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def project_images(p):
    out = []
    h = p.get("hero") or {}
    for k in ("image", "poster"):
        if h.get(k): out.append((h[k], p["name"]))
    for sl in (h.get("slides") or [])[:6]:
        if isinstance(sl, dict) and sl.get("image"): out.append((sl["image"], p["name"]))
    for s in p.get("sections", []):
        for k in ("images", "photos", "bricks"):
            for i in (s.get(k) or []):
                if isinstance(i, dict) and i.get("image"): out.append((i["image"], i.get("caption") or p["name"]))
    for i in p.get("gallery", []):
        if i.get("image"): out.append((i["image"], i.get("caption") or p["name"]))
    seen, res = set(), []
    for u, c in out:
        if u not in seen and re.search(r"\.(jpe?g|png|webp|gif)$", u, re.I): seen.add(u); res.append((u, c))
    return res

def project_ld(p, media=""):
    url = f"{SITE}/work/{p['slug']}/"
    typ, city, cc = VENUE.get(p["slug"], ("Organization", p.get("city"), None))
    imgs = project_images(p)
    # Venues are described as Organization (+ additionalType) so Google does not treat this portfolio page as the venue's own business listing.
    subj = {"@type": "MusicAlbum" if typ == "MusicAlbum" else "Organization", "name": p["name"]}
    if typ not in ("MusicAlbum", "Organization"): subj["additionalType"] = "https://schema.org/" + typ
    if p.get("aka"): subj["alternateName"] = p["aka"]
    if typ == "MusicAlbum":
        subj.update({"name": "Baralku", "byArtist": {"@type": "MusicGroup", "name": "Emancipator"}, "image": ab(imgs[0][0], media) if imgs else None})
    elif city:
        subj["address"] = {"@type": "PostalAddress", "addressLocality": city, "addressCountry": cc}
    for d in p.get("details", []):
        if d.get("url"): subj.setdefault("sameAs", []).append(d["url"])
    work = {"@type": "CreativeWork", "@id": url + "#work", "name": f"{p['name']}: {p.get('kind')}",
            "headline": p.get("seo_title") or p["name"], "description": p.get("seo_description") or p.get("intro"),
            "url": url, "creator": {"@id": PID}, "author": {"@id": PID}, "about": subj,
            "keywords": ", ".join([p["name"]] + (p.get("aka") or []) + (p.get("disciplines") or []) + [p.get("kind") or "", p.get("city") or ""]),
            "image": [ab(u, media) for u, _ in imgs[:12]], "inLanguage": "en-GB"}
    if p.get("years"): work["temporalCoverage"] = str(p["years"]).replace("–today", "/..").replace("–", "/")
    if p.get("role"): work["creditText"] = f"Felix Bollen – {p['role']}"
    page = {"@type": "WebPage", "@id": url, "url": url, "name": p.get("seo_title") or p["name"], "description": p.get("seo_description") or p.get("intro"),
            "isPartOf": {"@id": WID}, "mainEntity": {"@id": url + "#work"}, "author": {"@id": PID}, "inLanguage": "en-GB",
            "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/og/{p['slug']}.jpg", "width": 1200, "height": 630},
            "breadcrumb": crumbs([("Felix Bollen", "/"), ("Work", "/#work"), (p["name"], f"/work/{p['slug']}/")])}
    return ld({"@context": "https://schema.org", "@graph": [page, work, {"@type": "Person", "@id": PID, "name": "Felix Bollen", "url": SITE + "/"}]})

def home_ld(home, P, media="", press=()):
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/work/{p['slug']}/", "name": p["name"]} for i, p in enumerate(P)]
    prof = {"@type": "ProfilePage", "@id": SITE + "/", "url": SITE + "/", "name": home.get("seo_title") or home.get("title"),
            "description": home.get("seo_description") or home.get("description"), "isPartOf": {"@id": WID},
            "mainEntity": {"@id": PID}, "about": {"@id": PID}, "inLanguage": "en-GB", "dateModified": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "dateCreated": "2026-11-01T00:00:00+00:00",
            "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/og.jpg", "width": 1200, "height": 630}}
    pe = person(home, media)
    feat = [{"@type": "Article", "headline": x.get("title"), "url": x["url"], "publisher": {"@type": "Organization", "name": x.get("outlet")}} for x in press if x.get("about_felix") and x.get("url")]
    if feat: pe["subjectOf"] = feat
    return ld({"@context": "https://schema.org", "@graph": [prof, pe, website(), service(),
               {"@type": "ItemList", "name": "Selected works by Felix Bollen", "itemListElement": items}]})

def press_ld(pr, proj, base, its):
    url = SITE + base
    arts = [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Article", "headline": x.get("title") or x.get("outlet"),
             "publisher": {"@type": "Organization", "name": x.get("outlet")}, **({"url": x["url"]} if x.get("url", "").startswith("http") else {}),
             **({"about": [{"@type": "Thing", "name": proj["name"]}] + ([{"@id": PID}] if x.get("about_felix") else [])} if proj else {}),
             **({"mentions": {"@id": PID}} if x.get("about_felix") else {})}} for i, x in enumerate(its)]
    cr = [("Felix Bollen", "/"), ("Work", "/#work")] + ([(proj["name"], f"/work/{proj['slug']}/")] if proj else []) + [(pr.get("heading") or "Press", base)]
    return ld({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": pr.get("seo_title") or pr.get("title"), "description": pr.get("seo_description") or pr.get("intro"),
         "isPartOf": {"@id": WID}, "inLanguage": pr.get("lang") or "en-GB", "breadcrumb": crumbs(cr),
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(its), "itemListElement": arts}}]})

def faq_ld(url, faqs, lang="en-GB", name="", desc="", crumbs_=None):
    g = [{"@type": "WebPage", "@id": url, "url": url, "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": WID},
          "about": {"@id": PID}, "mainEntity": {"@id": SID}, **({"breadcrumb": crumbs(crumbs_)} if crumbs_ else {})},
         {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
             {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]},
         service(), {"@type": "Person", "@id": PID, "name": "Felix Bollen", "url": SITE + "/"}]
    return ld({"@context": "https://schema.org", "@graph": g})

def sitemap(pages, media=""):
    """pages: list of (path, lastmod, priority, [(img, caption)], alternates{lang: path})"""
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, lm, pr, imgs, alt in pages:
        x.append(f"<url><loc>{SITE}{path}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority>")
        for lang, ap in (alt or {}).items(): x.append(f'<xhtml:link rel="alternate" hreflang="{lang}" href="{SITE}{ap}"/>')
        for u, c in imgs[:1000]:
            x.append(f"<image:image><image:loc>{html.escape(ab(u, media))}</image:loc></image:image>")
        x.append("</url>")
    x.append("</urlset>")
    return "\n".join(x)

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai", "PerplexityBot",
           "Perplexity-User", "Google-Extended", "GoogleOther", "Applebot", "Applebot-Extended", "Bingbot", "DuckDuckBot", "DuckAssistBot",
           "meta-externalagent", "Meta-ExternalFetcher", "FacebookBot", "Amazonbot", "cohere-ai", "MistralAI-User", "YouBot", "CCBot", "Bytespider"]

def robots():
    r = ["# felixbollen.com – everyone is welcome, including AI assistants and search engines.", "User-agent: *", "Allow: /", "Disallow: /admin/", ""]
    for b in AI_BOTS: r += [f"User-agent: {b}", "Allow: /", "Disallow: /admin/", ""]
    r += [f"Sitemap: {SITE}/sitemap.xml", f"# LLM-friendly summary: {SITE}/llms.txt", ""]
    return "\n".join(r)
