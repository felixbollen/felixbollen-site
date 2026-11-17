#!/usr/bin/env python3
"""Builds felixbollen.com from content/*.json + static/ into public/.
Edit content through /admin (Decap CMS); Netlify runs this on every save."""
import os, re, json, shutil, html, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ST = os.path.join(ROOT, "static")
VER = (os.environ.get("COMMIT_REF") or "dev")[:7]
MEDIA = os.environ.get("MEDIA_BASE") or ("https://felixbollen.github.io/felixbollen-site/static" if os.environ.get("NETLIFY") else "")
esc = lambda s: html.escape(str(s or ""))
br = lambda s: esc(s).replace("\n", "<br>")

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(ST, OUT)
os.makedirs(OUT + "/admin", exist_ok=True)
for f in glob.glob(os.path.join(ROOT, "admin", "*")): shutil.copy(f, OUT + "/admin/")

HOME = json.load(open(os.path.join(ROOT, "content/home.json"), encoding="utf-8"))
P = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(ROOT, "content/projects/*.json"))]
P = [p for p in P if not p.get("hidden")]
def slugify(t): return re.sub(r"[^a-z0-9]+", "-", t.lower().replace("&", "and")).strip("-")
for p in P:
    p["slug"] = p.get("slug") or slugify(p["name"])
    p.setdefault("logo", ""); p.setdefault("background", "#ffffff"); p.setdefault("text_colour", "#0b0b0b"); p.setdefault("card", "#0b0b0b")
    p["background"] = p["background"] or "#ffffff"; p["text_colour"] = p["text_colour"] or "#0b0b0b"; p["card"] = p["card"] or "#0b0b0b"
    h = p.setdefault("hero", {}) or {}; p["hero"] = h
    if not h.get("type"):
        h["type"] = "video" if h.get("video") else "slides" if h.get("slides") else "vimeo" if h.get("vimeo_id") else "lottie" if h.get("animation") else "image"
    if h["type"] == "image" and not h.get("image"):
        imgs = [i["image"] for s in p.get("sections", []) for i in s.get("images", []) if i.get("image")]
        h["image"] = imgs[0] if imgs else ""
P.sort(key=lambda p: (float(p.get("order") or 99), p["name"]))

SEC = {"Branding": ("Branding", ""), "Marketing": ("Marketing", ""), "P.R.": ("P.R.", ""), "Conceptualisation": ("Conceptualisation", "Architecture & build"),
       "Website": ("Website", ""), "Photography & videography": ("Photography & videography", ""),
       "branding": ("Branding", ""), "marketing": ("Marketing", ""), "pr": ("P.R.", ""), "concept": ("Conceptualisation", "Architecture & build"),
       "website": ("Website", ""), "photo": ("Photography & videography", "")}

# ---------- logos ----------
def sym(path, sid):
    s = open(path, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    paths = re.findall(r'<path[^>]*?\sd="([^"]+)"', s)
    fr = re.search(r'fill-rule="(\w+)"', s); fr = fr.group(1) if fr else "nonzero"
    return vb, paths[0], f'<symbol id="{sid}" viewBox="{vb}">' + "".join(f'<path fill="currentColor" fill-rule="{fr}" d="{d}"/>' for d in paths) + "</symbol>"
syms = []
for k in sorted(set(p["logo"] for p in P if p["logo"])):
    f = f"{ST}/l/{k}.mono.svg"
    if os.path.exists(f): syms.append(sym(f, "l-" + k)[2])
fvb, fp, fs = sym(f"{ST}/l/fb-logo.svg", "fb"); syms.append(fs)
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(syms) + "</svg>"
HASLOGO = lambda k: bool(k) and os.path.exists(f"{ST}/l/{k}.mono.svg")
HASCOL = lambda k: bool(k) and os.path.exists(f"{ST}/l/{k}-colour.webp")
mono = lambda k, lab="": f'<svg viewBox="0 0 10 10" role="img" aria-label="{esc(lab)}"><use href="#l-{k}"/></svg>' if HASLOGO(k) else f'<span class="lgt">{esc(lab)}</span>'
FBS = f'<svg viewBox="{fvb}" aria-hidden="true"><use href="#fb"/></svg>'
EMAIL = HOME.get("email", "felixbollen@gmail.com")

def head(title, desc, path, og="/v/gk-home.jpg", style="", extra=""):
    return f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website">
<meta property="og:url" content="https://felixbollen.com{path}"><meta property="og:image" content="https://felixbollen.com/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Felix Bollen monogram"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://felixbollen.com/og.jpg"><link rel="canonical" href="https://felixbollen.com{path}">
<meta name="theme-color" content="#ffffff"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/hero-super.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/hero-light.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css?{VER}">{f"<style>:root{{{style}}}</style>" if style else ""}{extra}</head><body>{SPRITE}'''

def header(ov=False):
    return f'''<header class="hd{' ov' if ov else ''}"><a class="br" href="/" aria-label="Felix Bollen, home">{FBS}Felix Bollen</a>
<nav><a href="/#work">Work</a><a class="hm" href="/#about">About</a><a href="/#contact">Contact</a></nav></header>'''

FOOT = f'''<footer class="ft"><div class="r"><a href="/" aria-label="Home">{FBS}</a><span>© 2026 Felix Bollen. Marketing & Sales, Art Direction, Graphic Design.</span>
<span><a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a> · <button id="imp">Imprint & privacy</button></span></div></footer>
<dialog id="impd"><h3>Imprint</h3><p><b>Felix Bollen</b><br>Felix Bollen Graphic Design<br>Richmond, London, United Kingdom<br>{esc(EMAIL)}</p>
<h3 style="margin-top:20px">Privacy</h3><p>No cookies, trackers or analytics. Fonts are hosted on this site. The Gleis//Garten page embeds a Vimeo video. Messages from the contact form are delivered by Netlify and only used to reply to you.</p>
<p>Dufte Berlin logo, animation and brand identity © Plusminus Studio. Gleis//Garten interior photographs © Stefan Joham. German Kraft photography in part from germankraft.com. TV clips © the respective broadcasters.</p><form method="dialog" style="display:block"><button>Close</button></form></dialog>
<script src="/app.js?{VER}" defer></script></body></html>'''

def stats(st):
    st = [s for s in (st or []) if s.get("figure")]
    return '<div class="stats">' + "".join(f'<div><b>{esc(s["figure"])}</b><span>{esc(s.get("label"))}</span></div>' for s in st) + "</div>" if st else ""

def gfig(i):
    cap = i.get("caption") or ""; c = " c" if i.get("cutout") else ""; src = esc(i["image"])
    return f'<a href="{src}" data-lb data-cap="{esc(cap)}"><figure><div class="t{c}"><img data-src="{src}" alt="{esc(cap)}"></div><figcaption>{esc(cap)}</figcaption></figure></a>'

def vfig(v):
    cap = v.get("caption") or ""; poster = v.get("poster") or ""
    th = f'<img data-src="{esc(poster)}" alt="{esc(cap)}">' if poster else f'<video muted playsinline preload="metadata" src="{esc(v["video"])}#t=0.5"></video>'
    return f'<a href="{esc(v["video"])}" data-lb data-type="video" data-cap="{esc(cap)}"><figure><div class="t">{th}</div><figcaption>▶ {esc(cap)}</figcaption></figure></a>'

def navlogo(w):
    m = '<span class="m">%s</span>' % (mono(w["logo"], w["name"]) if HASLOGO(w["logo"]) else '<span class="lgt">%s</span>' % esc(w.get("card_name") or w["name"]))
    c = '<img class="c" src="/l/%s-colour.webp" alt="" loading="lazy">' % w["logo"] if HASCOL(w["logo"]) else ""
    return m + c
def cardcol(p):
    return '<img class="col" src="/l/%s-colour.webp" alt="" loading="lazy">' % p["logo"] if HASCOL(p["logo"]) else ""

# ---------- home ----------
cards = []
for i, p in enumerate(P):
    cards.append(f'''<a class="vc rv" href="/work/{p['slug']}/" style="--cb:{esc(p['card'])};--cf:{esc(p['text_colour'])};transition-delay:{(i%3)*70}ms"><span class="ix">{i+1:02d}</span>
<div class="lg">{mono(p['logo'], p.get('card_name') or p['name'])}{cardcol(p)}</div><div class="meta"><b>{esc(p['name'])}</b><span>{esc(p['city'])}</span></div></a>''')
disc = "".join(f'<div class="rv"><span class="lbl mute">{n+1:02d}</span><h3>{esc(d["title"])}</h3><p>{esc(d["text"])}</p><ul>{"".join(f"<li>{esc(x)}</li>" for x in d.get("items", []))}</ul></div>' for n, d in enumerate(HOME["disciplines"]))
nums = "".join(f'<div><b>{esc(n["figure"])}</b><span>{esc(n["label"])}</span></div>' for n in HOME.get("numbers", []))
also = "".join(f'<li><b>{esc(a["name"])}</b><span>{esc(a["text"])}</span><em>{esc(a.get("tag"))}</em></li>' for a in HOME.get("also", []))
abt = "".join(f"<p>{esc(x)}</p>" for x in HOME.get("about", []))
dets = "".join(f'<div><dt class="lbl">{esc(d["label"])}</dt><dd>{esc(d["value"])}</dd></div>' for d in HOME.get("details", []))
dl = "".join(f"<li>{esc(d['title'])}<span>{n+1:02d}</span></li>" for n, d in enumerate(HOME["disciplines"]))
opts = "".join(f"<option>{esc(d['title'])}</option>" for d in HOME["disciplines"]) + "<option>All of the above</option>"
IMAP = f'<script type="importmap">{{"imports":{{"three":"/js/three.module.min.js"}}}}</script><script type="module" src="/home3d.js?{VER}"></script>'
home = head(HOME["title"], HOME["description"], "/", extra=IMAP) + header() + f'''
<main id="top">
<section class="hero"><div class="mark"><div class="stk"><svg class="main" viewBox="{fvb}" aria-hidden="true"><path fill-rule="evenodd" d="{fp}"/></svg></div><button class="gyro" type="button">Tap to move with your phone</button></div>
<div class="tx rv"><h1>{"<br>".join(esc(w) for w in HOME["name"].split(" ", 1))}</h1><p>{esc(HOME["intro"])}</p><ul>{dl}</ul></div>
<span class="scroll lbl mute">Scroll</span></section>
<section class="sec" id="work"><div class="sh rv"><h2>Work</h2><span class="lbl mute">{len(P):02d}</span></div><div class="vg">{"".join(cards)}</div></section>
<section class="sec"><div class="sh rv"><h2>Disciplines</h2><span class="lbl mute">{len(HOME["disciplines"]):02d}</span></div><div class="dc">{disc}</div></section>
{f'<section class="sec"><div class="sh rv"><h2>In numbers</h2></div><div class="nm rv">{nums}</div></section>' if nums else ""}
{f'<section class="sec al"><div class="sh rv"><h2>Also</h2></div><ul class="rv">{also}</ul></section>' if also else ""}
<section class="sec" id="about"><div class="sh rv"><h2>About</h2></div><div class="ab">
<h3 class="rv">{br(HOME.get("about_heading"))}</h3><div class="rv">{abt}<dl>{dets}</dl></div></div></section>
<section class="ct" id="contact"><h2 class="rv">{br(HOME.get("contact_heading"))}</h2>
<div class="cg"><div class="rv"><span class="lbl mute">Write to me</span><br><br><a class="ml" href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a>
<p>{esc(HOME.get("contact_text"))}</p></div>
<div class="rv"><form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot" id="cf"><input type="hidden" name="form-name" value="contact"><p class="hp"><label>Leave empty <input name="bot"></label></p>
<div class="fr"><div><label class="lbl" for="n">Name</label><input id="n" name="name" required></div><div><label class="lbl" for="e">Email</label><input id="e" type="email" name="email" required></div></div>
<div><label class="lbl" for="t">Interested in</label><select id="t" name="topic">{opts}</select></div>
<div><label class="lbl" for="m">Project</label><textarea id="m" name="message" required></textarea></div>
<button class="bt" type="submit">Send message →</button></form><p class="ty">Thank you. I'll be in touch shortly.</p></div></div></section>
</main>''' + FOOT
open(OUT + "/index.html", "w", encoding="utf-8").write(home)


def fest_block(s):
    if not s.get("fest_heading"): return ""
    v = s.get("fest_video") or {}; r = s.get("fest_report") or {}; ch = s.get("fest_chart") or {}
    uid = "rep-" + slugify(s["fest_heading"])
    fs = "".join('<div><b>%s</b><span>%s</span></div>' % (esc(x["figure"]), esc(x["label"])) for x in s.get("fest_stats", []))
    vid = ('<div class="fv"><video autoplay muted loop playsinline preload="metadata" poster="%s" src="%s"></video><button type="button" class="snd" aria-label="Sound on">Sound on</button></div>' % (esc(v.get("poster")), esc(v["video"]))) if v.get("video") else ""
    bars = ch.get("bars", []); mx = max([b.get("value") or 0 for b in bars] or [1])
    chart = ('<div class="fchart"><span class="lbl">%s</span><div class="fb">%s</div><p class="fn">%s</p></div>' % (esc(ch.get("title")), "".join(
        '<div class="bar" style="--h:%.1f%%"><em>%s</em><i></i><b>%s</b><small>%s</small></div>' % (100 * (b.get("value") or 0) / mx, esc(b.get("text")), esc(b.get("label")), esc(b.get("sub"))) for b in bars), esc(ch.get("note")))) if bars else ""
    rep = ('<figure class="frep"><img data-src="%s" alt="%s"></figure>' % (esc(r["image"]), esc(r.get("caption")))) if r.get("image") else ""
    dl = ('<a class="fdl" href="%s" target="_blank" rel="noopener">Download PDF ↓</a>' % esc(r["pdf"])) if r.get("pdf") else ""
    more = ('<button type="button" class="fmore" data-open="%s">%s <span>→</span></button>' % (uid, esc(s.get("fest_more_label") or "More info")))
    ov = ('<div class="lbg frpt" id="%s"><button class="x" aria-label="Close">✕</button><span class="lbl">Report</span><h2>%s</h2><p class="frt">%s</p>%s%s%s</div>' % (uid, esc(s["fest_heading"]), esc(s.get("fest_text")), chart, rep, dl))
    gl = [g for g in s.get("fest_gallery", []) if g.get("image")]
    gal = ('<div class="fgal"><span class="lbl">%s</span><div class="gal5" data-lbg>%s</div></div>' % (esc(s.get("fest_gallery_title") or "Campaign"), "".join(gfig(g) for g in gl))) if gl else ""
    return '<div class="fest"><div class="fh"><span class="lbl">Highlight</span><h4>%s</h4></div><div class="fs">%s</div>%s%s%s%s</div>' % (esc(s["fest_heading"]), fs, more, vid, gal, ov)

def reels_block(s):
    rl = [r for r in s.get("reels", []) if r.get("video")]
    if not rl: return ""
    items = "".join('<a class="reel" href="%s" data-lb data-type="video" data-cap="%s"><video muted loop playsinline preload="none" poster="%s" data-src="%s"></video><span class="rp">▶</span></a>' % (esc(r["video"]), esc(r.get("caption")), esc(r.get("poster")), esc(r["video"])) for r in rl)
    return '<div class="reels"><div class="rh"><span class="lbl">%s</span><span class="lbl mute">%d videos · swipe →</span></div><div class="rr" data-lbg>%s</div></div>' % (esc(s.get("reels_title") or "Videos"), len(rl), items)

# ---------- case-study pages (one-pagers) ----------
def vnav(p, pv, nx):
    nav = "".join(f'<a href="/work/{w["slug"]}/"{" class=cu aria-current=page" if w is p else ""} style="--cb:{esc(w["card"])}" aria-label="{esc(w["name"])}" title="{esc(w["name"])}">{navlogo(w)}</a>' for w in P)
    return f'''<section class="vn"><div class="row">{nav}</div><div class="pn"><a href="/work/{pv['slug']}/"><small class="lbl">← Previous</small><b>{esc(pv['name'])}</b></a>
<a href="/work/{nx['slug']}/" style="text-align:right"><small class="lbl">Next →</small><b>{esc(nx['name'])}</b></a></div></section>'''

def render_case(i, p, pv, nx):
    H = p.get("hero") or {}; hero = H.get("image", ""); wide = H.get("shape") == "wide"
    if wide:
        herofig = '<figure class="cwide rvc" data-lbg><a href="%s" data-lb data-cap="%s"><img src="%s" alt=""></a>%s</figure>' % (esc(hero), esc(H.get("caption")), esc(hero), ('<figcaption>%s</figcaption>' % esc(H.get("caption"))) if H.get("caption") else "")
    else:
        herofig = '<div class="tiltw"><div class="tilt" data-lbg><a href="%s" data-lb data-cap="%s"><img src="%s" alt=""></a><span class="sheen"></span></div></div>' % (esc(hero), esc(p["name"]), esc(hero))
    lists = "".join('<div class="cl rv"><span class="lbl">%s</span><ul>%s</ul></div>' % (esc(L.get("heading")), "".join('<li><b>%s</b><span>%s</span></li>' % (esc(it.get("a")), esc(it.get("b"))) for it in L.get("items", []))) for L in p.get("lists", []))
    title = p["name"].split(":")[-1].strip(); artist = p["name"].split(":")[0].strip() if ":" in p["name"] else ""
    facts = "".join(f'<div><dt class="lbl">{esc(f["label"])}</dt><dd>{esc(f["value"])}</dd></div>' for f in p.get("facts", []))
    chs = ""
    for j, c in enumerate(p.get("chapters", [])):
        paras = "".join(f"<p>{esc(t)}</p>" for t in (c.get("text") or []))
        fig = ('<figure class="cfig rvc"><a href="%s" data-lb data-cap="%s"><img src="%s" alt="%s" loading="lazy"></a><figcaption>%s</figcaption></figure>' % (esc(c["image"]), esc(c.get("caption")), esc(c["image"]), esc(c.get("caption")), esc(c.get("caption")))) if c.get("image") else ""
        chs += f'''<section class="ch{" rev" if j % 2 else ""}{"" if fig else " solo"}" data-lbg><div class="ct2 rv"><span class="lbl">{esc(c.get("label"))}</span><h2>{br(c.get("heading"))}</h2>{paras}</div>{fig}</section>'''
    apps = "".join('<a class="ap rv" style="transition-delay:%dms" href="%s" data-lb data-cap="%s"><div class="ai"><img src="%s" alt="%s" loading="lazy"></div><span>%s</span></a>' % ((k%3)*80, esc(a["image"]), esc(a.get("caption")), esc(a["image"]), esc(a.get("caption")), esc(a.get("caption"))) for k, a in enumerate(p.get("applications", [])))
    def dval(d):
        return '<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (esc(d["url"]), esc(d["value"])) if d.get("url") else esc(d["value"])
    dets = "".join('<div><dt class="lbl">%s</dt><dd>%s</dd></div>' % (esc(d["label"]), dval(d)) for d in p.get("details", []))
    page = head(f"{p['name']}: Felix Bollen", p.get("intro", ""), f"/work/{p['slug']}/") + header() + f'''
<main id="top" class="case">
<section class="chero{' wide' if wide else ''}"><div class="cht"><span class="lbl rv">Case study · {esc(p.get("kind"))} · {esc(p.get("years"))}</span><h1 class="rv">{esc(title)}</h1>{f'<div class="art rv">{esc(artist)}</div>' if artist else ""}<p class="lead rv">{esc(p.get("intro"))}</p></div>
{herofig}</section>
<dl class="facts rv">{facts}</dl>
{chs}
<section class="apps{' wide' if p.get('apps_shape')=='wide' else ''}" data-lbg><div class="ah rv"><span class="lbl">{esc(p.get("apps_label"))}</span><h2>{br(p.get("apps_heading"))}</h2>{f'<p class="lede">{esc(p.get("apps_text"))}</p>' if p.get("apps_text") else ""}</div><div class="ag">{apps}</div></section>
{f'<section class="clists">{lists}</section>' if lists else ""}
<dl class="facts dets rv">{dets}</dl>
{f'<p class="ccr">{esc(p["credit"])}</p>' if p.get("credit") else ""}
{vnav(p, pv, nx)}</main>
<script>
(function(){{var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.1}});document.querySelectorAll('.rvc').forEach(function(e){{io.observe(e)}});
var w=document.querySelector('.tilt');if(!w)return;var tx=0,ty=0,cx=0,cy=0,last=0,RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
function set(x,y){{tx=Math.max(-1,Math.min(1,x));ty=Math.max(-1,Math.min(1,y));last=performance.now()}}
addEventListener('pointermove',function(e){{if(e.pointerType==='mouse')set((e.clientX/innerWidth-.5)*2,(e.clientY/innerHeight-.5)*2)}});
var b0=null,g0=null;function ori(e){{if(e.gamma==null)return;if(b0==null){{b0=e.beta;g0=e.gamma}}set((e.gamma-g0)/20,(e.beta-b0)/20)}}
if(window.DeviceOrientationEvent){{if(typeof DeviceOrientationEvent.requestPermission==='function'){{document.addEventListener('touchend',function(){{DeviceOrientationEvent.requestPermission().then(function(s){{if(s==='granted')addEventListener('deviceorientation',ori)}}).catch(function(){{}})}},{{once:true}})}}else addEventListener('deviceorientation',ori)}}
(function loop(t){{requestAnimationFrame(loop);var x=tx,y=ty;if(t-last>2500&&!RM){{x=Math.sin(t/2600)*.5;y=Math.cos(t/3300)*.35}}cx+=(x-cx)*.07;cy+=(y-cy)*.07;
var sy=Math.min(1,scrollY/innerHeight);w.style.transform='rotateY('+(cx*14)+'deg) rotateX('+(-cy*10)+'deg) translateY('+(sy*-40)+'px) scale('+(1-sy*.06)+')';w.style.setProperty('--sx',(50+cx*40)+'%');w.style.setProperty('--sy',(50+cy*40)+'%')}})(0);
}})();
</script>''' + FOOT
    os.makedirs(f"{OUT}/work/{p['slug']}", exist_ok=True)
    open(f"{OUT}/work/{p['slug']}/index.html", "w", encoding="utf-8").write(page)

# ---------- project pages ----------
N = len(P)
for i, p in enumerate(P):
    pv, nx = P[(i-1) % N], P[(i+1) % N]
    if p.get("template") == "case":
        render_case(i, p, pv, nx); continue
    style = f"--bg:{p['background']};--fg:{p['text_colour']};--tile:{p.get('tile') or p['background']}"; extra = ""
    h = p.get("hero") or {}; ht = h.get("type", "image"); og = "/v/gk-home.jpg"
    lgo = "" if (p.get("hero") or {}).get("hide_logo") else f'<div class="lgo">{mono(p["logo"], p["name"])}</div>'
    if ht == "video" and h.get("video"):
        og = h.get("poster") or og
        hero = f'<section class="vh vid"><video autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" poster="{esc(h.get("poster"))}"><source src="{esc(h["video"])}" type="video/mp4"></video>{lgo}'
    elif ht == "vimeo":
        og = h.get("poster") or og
        hero = f'<section class="vh vid vim"><img class="po" src="{esc(h.get("poster"))}" alt=""><iframe src="https://player.vimeo.com/video/{esc(h.get("vimeo_id"))}?background=1&autoplay=1&loop=1&muted=1&dnt=1" allow="autoplay; fullscreen" title="{esc(p["name"])}" loading="eager"></iframe>{lgo}'
    elif ht == "slides":
        sl = [s["image"] for s in h.get("slides", [])]; og = sl[0] if sl else og
        imgs = "".join(f'<img {"src" if j==0 else "data-src"}="{esc(s)}" alt="">' for j, s in enumerate(sl))
        spin = h.get("spin_logo")
        coin = f'<div class="spin3d"><div class="coin"><img src="{esc(spin)}" alt="{esc(p["name"])}"><img class="b" src="{esc(spin)}" alt=""></div></div>' if spin else lgo
        hero = f'<section class="vh"><div class="slides">{imgs}</div>{coin}'
    elif ht == "lottie":
        extra = '<script src="/js/lottie_light.min.js" defer></script>'
        hero = f'<section class="vh lot"><div id="lot" data-src="{esc(h.get("animation"))}" aria-label="{esc(p["name"])} animation"></div>'
    else:
        og = h.get("image") or og
        hero = f'<section class="vh"><img class="po img" src="{esc(h.get("image"))}" alt="">{lgo}'
    first = rest = ""
    # bricks story
    br_ = [b for b in p.get("bricks", []) if b.get("image")]
    if br_:
        steps = "".join(f'<div class="step"><span class="n">{j+1:02d} / {len(br_):02d}</span><p>{esc(b.get("text"))}</p></div>' for j, b in enumerate(br_))
        pics = "".join(f'<img {"src" if j==0 else "data-src"}="{esc(b["image"])}" alt="">' for j, b in enumerate(br_))
        first = f'''<section class="bricks" style="--n:{len(br_)}" data-to="{int(p.get("bricks_counter") or 0)}"><div class="stage"><span class="hd2">{esc(p.get("bricks_heading"))}</span><div class="txt">{steps}</div><div class="pics">{pics}</div>
<div class="meter"><b>0</b><span class="lbl">bricks</span></div><span class="bar"></span></div></section>'''
    # TV clips
    tv = p.get("tv", [])
    if tv:
        nw = "".join(f'<button type="button" onclick="this.closest(\'section\').querySelectorAll(\'a[data-lb]\')[{j}].click()"><img src="{esc(t.get("poster"))}" alt="{esc(t.get("channel"))}" loading="lazy"><span class="pl">▶</span><span class="cap"><b>{esc(t.get("channel"))}</b>{esc(t.get("title"))}</span></button>' for j, t in enumerate(tv))
        hid = "".join(f'<a hidden href="{esc(t["video"])}" data-lb data-type="video" data-cap="{esc(t.get("channel"))}: {esc(t.get("title"))}"></a>' for t in tv)
        rest += f'<section class="blk" data-lbg><span class="lbl">On TV</span><h2 class="big rv">{br(p.get("tv_heading"))}</h2><div class="news rv">{nw}</div>{hid}</section>'
    # labels
    labs = [l for l in p.get("labels", []) if l.get("image")]
    if labs:
        spin = "".join(f'<img {"class=on " if j==0 else ""}src="{esc(l["image"])}" alt="{esc(l.get("name"))}" loading="lazy">' for j, l in enumerate(labs))
        grid = "".join(f'<a href="{esc(l["image"])}" data-lb data-cap="{esc(l.get("name"))}"><img data-src="{esc(l["image"])}" alt="">{esc(l.get("name"))}</a>' for l in labs)
        lh = br((p.get("labels_heading") or "").replace("{n}", str(len(labs))))
        rest += f'''<section class="blk"><div class="labs"><div class="spinlab" data-open="labgrid" role="button" aria-label="Open all beer labels">{spin}<span class="tag lbl"></span></div>
<div><span class="lbl">Beer labels</span><h2 class="big rv">{lh}</h2><p class="lede">{esc(p.get("labels_text"))}</p>
<button class="btn" type="button" data-open="labgrid">See all labels →</button></div></div></section>
<div class="lbg" id="labgrid" data-lbg><button class="x" aria-label="Close">✕</button><span class="lbl">{esc(p["name"])}</span><h2 style="font-size:clamp(34px,5vw,80px);font-weight:900;text-transform:uppercase;letter-spacing:-.05em;line-height:.9;margin-top:10px">All beer labels</h2><div class="g">{grid}</div></div>'''
    # sections
    secs = []
    for n, s in enumerate(p.get("sections", [])):
        title, sub = SEC.get(s.get("type"), (s.get("type", "").title(), ""))
        if s.get("title"): title = s["title"]
        ims = [x for x in s.get("images", []) if x.get("image")]; vids = [x for x in s.get("videos", []) if x.get("video")]
        deck = [x for x in s.get("deck", []) if x.get("image")]
        dk = ""
        if deck:
            dk = f'<div class="deck"><span class="lbl">{esc(s.get("deck_title") or "Presentation")}</span><div class="rail">' + "".join(
                f'<figure><img data-src="{esc(d["image"])}" alt=""><figcaption><b>{j+1:02d} / {len(deck):02d}</b>{esc(d.get("caption"))}</figcaption></figure>' for j, d in enumerate(deck)) + '</div><div class="nv"><button type="button" data-d="0" aria-label="Previous">←</button><button type="button" data-d="1" aria-label="Next">→</button></div></div>'
        body = stats(s.get("stats")) + f'<p class="lede">{esc(s.get("text"))}</p>'
        body += fest_block(s) + reels_block(s)
        lk = f'<p class="sl"><a class="btn" href="{esc(s["link"])}">{esc(s.get("link_label") or "More")}</a></p>' if s.get("link") else ""
        pano = [x for x in s.get("pano", []) if x.get("image")]
        if pano:
            pj = json.dumps([{"image": MEDIA + x["image"] if x["image"].startswith("/") else x["image"], "thumb": (MEDIA + x["thumb"] if (x.get("thumb") or "").startswith("/") else x.get("thumb") or ""), "caption": x.get("caption", ""), "vto": x.get("vto") or 1} for x in pano]).replace("</", "<\\/")
            lk += f'<p class="sl"><a class="btn" href="#" data-pano-open>Open the 360° tour ↗</a></p><script type="application/json" class="pano-data" data-title="{esc(s.get("pano_title") or "360°")}">{pj}</script>'
            extra += '<script type="importmap">{"imports":{"three":"/js/three.module.min.js"}}</script><script type="module" src="/js/pano.js?' + VER + '"></script>'

        body += lk
        gal = f'<div class="gal5" data-lbg>{"".join(vfig(v) for v in vids)}{"".join(gfig(x) for x in ims)}</div>' if (ims or vids) else ""
        subh = f"<small>{esc(sub)}</small>" if sub else ""
        secs.append(f'''<div class="sec5"><button type="button" aria-expanded="false"><span class="n">{n+1:02d}</span><h3>{esc(title)}{subh}</h3><span class="c">{(len(ims)+len(vids)) or ''}</span><span class="pm"></span></button>
<div class="bd"><div><div class="in">{body}{dk}{gal}</div></div></div></div>''')
    meta = "".join(f'<div><dt>{a}</dt><dd>{esc(b)}</dd></div>' for a, b in [("Role", p.get("role")), ("Location", p.get("city")), ("Years", p.get("years") or "—"), ("Disciplines", ", ".join(p.get("disciplines", [])))])
    nav = "".join(f'<a href="/work/{w["slug"]}/"{" class=cu aria-current=page" if w is p else ""} style="--cb:{esc(w["card"])}" aria-label="{esc(w["name"])}" title="{esc(w["name"])}">{navlogo(w)}</a>' for w in P)
    cr = f'<p class="cr">{esc(p["credit"])}</p>' if p.get("credit") else ""
    page = head(f"{p['name']}: Felix Bollen", f"{p['name']}, {p.get('kind')}, {p.get('city')}. {p.get('intro')}", f"/work/{p['slug']}/", og, style, extra) + header(ov=(ht != "lottie")) + f'''
<main id="top">{hero}
<div class="bot"><div><h1>{esc(p['name'])}</h1><div class="kd">{esc(p.get('kind'))} · {esc(p.get('city'))}{" · " + esc(p['years']) if p.get('years') else ""}</div></div><span class="lbl">{i+1:02d} / {N:02d}</span></div></section>
{first}
<section class="vi"><div class="rv"><p class="lead">{esc(p.get('intro'))}</p>{cr}</div><dl class="rv">{meta}</dl></section>
{rest}
<section class="sec" id="did"><div class="sh rv"><h2>What I did</h2><span class="lbl mute">{len(secs):02d}</span></div><div class="acc">{"".join(secs)}</div></section>
<section class="vn"><div class="row">{nav}</div><div class="pn"><a href="/work/{pv['slug']}/"><small class="lbl">← Previous</small><b>{esc(pv['name'])}</b></a>
<a href="/work/{nx['slug']}/" style="text-align:right"><small class="lbl">Next →</small><b>{esc(nx['name'])}</b></a></div></section></main>''' + FOOT
    os.makedirs(f"{OUT}/work/{p['slug']}", exist_ok=True)
    open(f"{OUT}/work/{p['slug']}/index.html", "w", encoding="utf-8").write(page)
# ---------- press pages ----------
for f in sorted(glob.glob(os.path.join(ROOT, "content/press-*.json"))):
    pr = json.load(open(f, encoding="utf-8"))
    proj = next((p for p in P if p["slug"] == pr.get("project")), None)
    base = f"/work/{pr.get('project')}/presse/" if proj else f"/presse/{os.path.basename(f)[6:-5]}/"
    its = [x for x in pr.get("items", []) if x.get("outlet") or x.get("title")]
    def card(x):
        url = x.get("pdf") or x.get("url") or ""; ext = url.lower().endswith(".pdf"); tag = "PDF ↓" if ext else "Read article ↗"
        im = f'<div class="pt"><img src="{esc(x["image"])}" alt="" loading="lazy"></div>' if x.get("image") else '<div class="pt e"></div>'
        inner = f'{im}<div class="pc"><span class="lbl">{esc(x.get("outlet"))}</span>{("<h3>" + esc(x["title"]) + "</h3>") if x.get("title") else ""}<div class="pd"><span>{esc(x.get("date"))}</span><span>{tag if url else ""}</span></div></div>'
        return f'<a class="pi rv" href="{esc(url)}" target="_blank" rel="noopener">{inner}</a>' if url else f'<div class="pi rv">{inner}</div>'
    back = f'<a class="bk lbl" href="/work/{proj["slug"]}/">← {esc(proj["name"])}</a>' if proj else ""
    page = head(pr.get("title") or "Press", pr.get("intro") or "", base) + header() + f'''
<main id="top" class="press"><section class="ph">{back}<h1>{br(pr.get("heading") or "Press")}</h1><p class="lead">{esc(pr.get("intro"))}</p>
<div class="pm"><span class="lbl mute">{len(its)} articles</span><span class="lbl mute">{esc(pr.get("contact"))}</span></div></section>
<section class="pg">{"".join(card(x) for x in its)}</section></main>''' + FOOT
    os.makedirs(OUT + base, exist_ok=True); open(OUT + base + "index.html", "w", encoding="utf-8").write(page)
# ---------- serve media from GitHub Pages (free bandwidth) ----------
if MEDIA:
    rx = re.compile(r'((?:src|href|data-src|poster)=")/((?:v|a|ds|media|press)/)')
    for f in glob.glob(OUT + "/**/*.html", recursive=True):
        if "/admin/" in f: continue
        t = open(f, encoding="utf-8").read(); t2 = rx.sub(lambda m: m.group(1) + MEDIA + "/" + m.group(2), t)
        if t2 != t: open(f, "w", encoding="utf-8").write(t2)
print("built", N, "projects")
