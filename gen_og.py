from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, os

W, H = 1200, 630
BG   = (8, 8, 20)        # near-black navy
ACC  = (109, 93, 255)     # brand purple
ACC2 = (200, 195, 255)    # soft lavender
WHITE = (255, 255, 255)
MUTED = (160, 155, 200)

out = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(out)

# ── Subtle geometric accent lines ────────────────────────────────────
# Thin horizontal rule full width
d.rectangle([0, H-4, W, H], fill=ACC)

# Thin vertical accent bar left of text block
BAR_X = 360
d.rectangle([BAR_X, 60, BAR_X+3, H-4], fill=(109, 93, 255, 60))

# Very faint large circle top-right (geometric decoration)
def draw_circle_ring(img, cx, cy, r, color, width=1, alpha=40):
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color+(alpha,), width=width)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

out = draw_circle_ring(out, 1050, -80, 320, (109, 93, 255), width=1, alpha=25)
out = draw_circle_ring(out, 1050, -80, 200, (109, 93, 255), width=1, alpha=18)
out = draw_circle_ring(out, 1100, 580, 180, (219, 39, 119), width=1, alpha=20)
d = ImageDraw.Draw(out)

# ── Dot grid (subtle texture, top-right corner) ──────────────────────
import random
rng = random.Random(7)
for gx in range(820, 1160, 28):
    for gy in range(40, 320, 28):
        a = rng.randint(12, 35)
        d.ellipse([gx-1, gy-1, gx+1, gy+1], fill=(109,93,255,a))

# ── Photo circle ─────────────────────────────────────────────────────
photo_path = os.path.join(os.path.dirname(__file__), "img/ernestine.jpg")
PHOTO_X, PHOTO_Y, PHOTO_SIZE = 72, (H - 240) // 2, 240

if os.path.exists(photo_path):
    photo = Image.open(photo_path).convert("RGBA")
    photo = photo.resize((PHOTO_SIZE, PHOTO_SIZE), Image.LANCZOS)
    # circle mask
    mask = Image.new("L", (PHOTO_SIZE, PHOTO_SIZE), 0)
    ImageDraw.Draw(mask).ellipse([0,0,PHOTO_SIZE,PHOTO_SIZE], fill=255)
    photo.putalpha(mask)

    # glow ring (brand purple)
    ring_size = PHOTO_SIZE + 12
    ring = Image.new("RGBA", (ring_size, ring_size), (0,0,0,0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse([0,0,ring_size-1,ring_size-1], outline=(109,93,255,180), width=3)
    # outer faint ring
    rd.ellipse([4,4,ring_size-5,ring_size-5], outline=(109,93,255,60), width=1)

    out_rgba = out.convert("RGBA")
    out_rgba.paste(ring, (PHOTO_X-6, PHOTO_Y-6), ring)
    out_rgba.paste(photo, (PHOTO_X, PHOTO_Y), photo)
    out = out_rgba.convert("RGB")
    d = ImageDraw.Draw(out)

# ── Typography ───────────────────────────────────────────────────────
def get_font(size, bold=False):
    candidates_bold = [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
    ]
    candidates = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
    ]
    for p in (candidates_bold if bold else candidates):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

TX = 390   # text column X

# Thin purple left border for text block
d.rectangle([TX-18, 58, TX-15, H-20], fill=(109,93,255,90))

# Name — large, white, bold
font_name  = get_font(66, bold=True)
font_title = get_font(27)
font_sub   = get_font(20)
font_tag   = get_font(18)
font_url   = get_font(16)

d.text((TX, 68), "Ernestine Matjabo", font=font_name, fill=WHITE)

# Title — brand lavender
d.text((TX, 152), "Senior Product Manager · Product Owner", font=font_title, fill=ACC2)

# Thin separator
d.rectangle([TX, 196, TX+500, 198], fill=(109,93,255,80))

# Key facts — bold label + light description
facts = [
    ("8+ ans",        "en produit digital & fintech"),
    ("Hello Bank!",   "Orange Money · Catenda · Eko Education"),
    ("Conversion",    "Rétention · AB Tests · Mobile"),
]
sy = 216
for bold_txt, light_txt in facts:
    fb = get_font(18, bold=True)
    fl = get_font(18)
    bw = d.textlength(bold_txt + "  ", font=fb)
    d.text((TX, sy), bold_txt + "  ", font=fb, fill=WHITE)
    d.text((TX + bw, sy), light_txt, font=fl, fill=MUTED)
    sy += 34

# Thin separator
d.rectangle([TX, sy+6, TX+500, sy+8], fill=(109,93,255,50))
sy += 22

# Tagline — two lines, soft lavender
d.text((TX, sy),    "Je transforme des besoins complexes", font=font_sub, fill=(235, 232, 255))
d.text((TX, sy+30), "en expériences impactantes.",          font=font_sub, fill=(235, 232, 255))

# URL badge — minimal, clean
badge_y = H - 68
badge_text = "ernestinematjabo.com"
bw2 = int(d.textlength(badge_text, font=font_url)) + 24
d.rounded_rectangle([TX, badge_y, TX+bw2, badge_y+30], radius=6, fill=(109,93,255,35))
d.rounded_rectangle([TX, badge_y, TX+bw2, badge_y+30], radius=6, outline=(109,93,255,120), width=1)
d.text((TX+12, badge_y+7), badge_text, font=font_url, fill=(200, 195, 255))

# ── Small accent dots top-right ─────────────────────────────────────
for dx2, dy2, r2, a2 in [
    (1140, 90, 4, 90), (1165, 130, 2, 55), (1115, 155, 3, 65),
    (1155, 60, 2, 45), (1130, 185, 2, 40),
]:
    d.ellipse([dx2-r2, dy2-r2, dx2+r2, dy2+r2], fill=(109,93,255,a2))

# ── Save ─────────────────────────────────────────────────────────────
dest = os.path.join(os.path.dirname(__file__), "img/og-image.png")
out.save(dest, "PNG", optimize=True)
print(f"OG image saved → {dest}  ({W}x{H})")
