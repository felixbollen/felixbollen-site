"""Run locally: python3 tools/make_og.py  -> static/og/<slug>.jpg (1200x630 share images)."""
import json, glob, os, subprocess, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ST = R + "/static"
os.makedirs(ST + "/og", exist_ok=True); os.makedirs("/tmp/ogf", exist_ok=True)
def ttf(n):
    p = "/tmp/ogf/%s.ttf" % n
    if not os.path.exists(p): f = TTFont(f"{ST}/fonts/{n}.woff2"); f.flavor = None; f.save(p)
    return p
SUP, MED = ttf("hero-super"), ttf("hero-medium")
mono = Image.open(io.BytesIO(subprocess.run(["rsvg-convert", "-h", "64", f"{ST}/l/fb-logo.svg"], capture_output=True).stdout)).convert("RGBA")
a = mono.split()[3]; mono = Image.new("RGBA", mono.size, "white"); mono.putalpha(a)
for f in glob.glob(R + "/content/projects/*.json"):
    p = json.load(open(f)); h = p.get("hero") or {}
    src = h.get("image") or h.get("poster") or ((h.get("slides") or [{}])[0].get("image"))
    if not src:
        src = next((i["image"] for s in p.get("sections", []) for k in ("images", "photos") for i in (s.get(k) or []) if isinstance(i, dict) and i.get("image")), None)
    if not src or not os.path.exists(ST + src): print("skip", p["slug"]); continue
    im = Image.open(ST + src).convert("RGB")
    W, H = 1200, 630; s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    g = Image.new("L", (1, H)); [g.putpixel((0, y), int(215 * max(0, (y - H * .35) / (H * .65)) ** 1.2)) for y in range(H)]
    im = Image.composite(Image.new("RGB", (W, H), "black"), im, g.resize((W, H)))
    top = Image.new("L", (1, H)); [top.putpixel((0, y), int(120 * max(0, 1 - y / 160))) for y in range(H)]
    im = Image.composite(Image.new("RGB", (W, H), "black"), im, top.resize((W, H)))
    d = ImageDraw.Draw(im); name = p["name"]; fs = 92
    while ImageFont.truetype(SUP, fs).getlength(name.upper()) > W - 120: fs -= 4
    d.text((60, H - 70 - fs * .2), name.upper(), font=ImageFont.truetype(SUP, fs), fill="white", anchor="ls")
    d.text((62, H - 46), f"{p.get('kind')} · {p.get('city')}   —   Felix Bollen", font=ImageFont.truetype(MED, 28), fill=(235, 235, 235), anchor="ls")
    im.paste(mono, (60, 48), mono)
    im.save(f"{ST}/og/{p['slug']}.jpg", quality=84, optimize=True, progressive=True); print("og", p["slug"], src)
