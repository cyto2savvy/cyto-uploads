import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw, ImageFilter
from render import font, F_BLACK, F_XB, F_SB, CREAM, GOLD, CORAL, INK, TEAL_L

def skyline(w, h, top, col=(28, 52, 84, 255), tower_x=None, scale=1.0, seed=11):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rb = random.Random(seed); x = -10
    while x < w:
        bw = int(rb.randint(60, 150) * scale); bh = int(rb.randint(60, 260) * scale)
        d.rectangle((x, h - bh, x + bw, h), fill=col); x += bw + rb.randint(3, 12)
    if tower_x:
        s = scale; tx = tower_x
        d.polygon([(tx - 16 * s, h), (tx + 16 * s, h), (tx + 5 * s, top + 110 * s), (tx - 5 * s, top + 110 * s)], fill=col)
        d.ellipse((tx - 40 * s, top + 190 * s, tx + 40 * s, top + 228 * s), fill=col)
        d.rectangle((tx - 25 * s, top + 205 * s, tx + 25 * s, top + 238 * s), fill=col)
        d.ellipse((tx - 14 * s, top + 120 * s, tx + 14 * s, top + 138 * s), fill=col)
        d.rectangle((tx - 2 * s, top, tx + 2 * s, top + 120 * s), fill=col)
    return im

def gradient(w, h):
    g = Image.new("RGB", (w, h))
    px = g.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(R.BG_TOP[i] + (R.BG_BOT[i] - R.BG_TOP[i]) * t) for i in range(3))
        for x in range(w): px[x, y] = c
    return g.convert("RGBA")

# ---- profile picture 800x800 (YouTube crops to a circle)
pp = gradient(800, 800)
d = ImageDraw.Draw(pp)
d.ellipse((60, 60, 740, 740), fill=(22, 46, 76))
pp.alpha_composite(skyline(800, 800, 470, (34, 62, 98, 255), tower_x=600, scale=1.1))
mask = Image.new("L", (800, 800), 0); ImageDraw.Draw(mask).ellipse((60, 60, 740, 740), fill=255)
inner = Image.new("RGBA", (800, 800), (0, 0, 0, 0)); inner.paste(pp, (0, 0), mask)
pp = gradient(800, 800); pp.alpha_composite(inner)
ImageDraw.Draw(pp).ellipse((60, 60, 740, 740), outline=GOLD, width=14)
c = R.cyto(520, "open", "smile", "wave1", (0, 0), "mystery")
pp.alpha_composite(c, (400 - c.width // 2, 430 - c.height // 2))
pp.convert("RGB").save("channel-profile-800.png")

# ---- banner 2560x1440; everything important inside the 1546x423 centre safe area
W, H = 2560, 1440
bn = gradient(W, H)
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
rnd = random.Random(7)
for _ in range(70):
    r = rnd.randint(30, 140); x, y = rnd.randint(0, W), rnd.randint(0, H)
    ld.ellipse((x - r, y - r, x + r, y + r), outline=(120, 200, 220, 22), width=3)
bn.alpha_composite(lay)
sk = skyline(W, H, 640, (28, 52, 84, 255), tower_x=1900, scale=1.6)
bn.alpha_composite(sk)
sx0, sy0, sx1, sy1 = (W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2
cy = R.cyto(300, "open", "smile", "wave1", (0, 0), "mystery")
pad = 24
bn.alpha_composite(cy, (sx0 + pad, (H - cy.height) // 2 + 4))
d = ImageDraw.Draw(bn)
tx = sx0 + pad + cy.width + 20
tf = font(F_BLACK, 104)
d.text((tx, sy0 + 34), "THE BODY IS", font=tf, fill=CREAM, stroke_width=6, stroke_fill=INK)
d.text((tx, sy0 + 140), "THE ", font=tf, fill=CREAM, stroke_width=6, stroke_fill=INK)
d.text((tx + tf.getlength("THE "), sy0 + 140), "6IX", font=tf, fill=GOLD, stroke_width=6, stroke_fill=INK)
sf = font(F_SB, 38)
d.text((tx + 4, sy0 + 274), "Your body, explained by a cell from Toronto.", font=sf, fill=TEAL_L)
p = R.pill("NEW SHORTS EVERY WEEK", 28, INK, GOLD)
bn.alpha_composite(p, (tx + 4, sy0 + 330))
right = max(tx + 4 + int(sf.getlength("Your body, explained by a cell from Toronto.")), tx + int(tf.getlength("THE BODY IS")))
print("content right edge", right, "safe right", sx1, "| cyto top", (H - cy.height) // 2 + 4, "safe top", sy0)
bn.convert("RGB").save("channel-banner-2560x1440.png", optimize=True)
# preview of how the banner looks on desktop (centre strip)
bn.crop((0, sy0 - 60, W, sy1 + 60)).resize((1280, (sy1 - sy0 + 120) // 2)).convert("RGB").save("banner-preview.jpg", quality=88)
print(os.path.getsize("channel-banner-2560x1440.png") // 1024, "KB")
