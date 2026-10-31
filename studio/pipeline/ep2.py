"""Ep 2: Can you get scared to death?  python3 ep2.py stills|video"""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
import engine as G
from engine import wt, k_at, E
import render as R
from render import W, H, font, F_XB, F_SB, F_BLACK, CREAM, GOLD, CORAL, INK, TEAL_L, PW, PH, lerp, ease, pill, paste_alpha

G.init("/home/claude/ep2", "raccoon", drop=(0, "Bro"),
       hits=[(0, "scared"), (2, "three"), (3, "broken"), (5, "raccoon")])

RED = (222, 52, 72)

def bez(p0, p1, p2, u):
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])

def heart_poly(cx, cy, size):
    pts = []
    for i in range(80):
        t = 2 * math.pi * i / 80
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * size / 32, cy - y * size / 32))
    return pts

# ---------------------------------------------------------------- adrenal scene
def draw_adrenal(ta, flow_t0):
    img, d, s = G.panel_base()
    S = lambda *p: [v * s for v in p]
    d.ellipse(S(110, 250, 370, 580), fill=(186, 78, 78), outline=(140, 50, 50), width=4 * s)
    d.ellipse(S(310, 360, 410, 470), fill=(12, 24, 40))
    d.polygon(S(140, 268, 340, 268, 250, 160), fill=(246, 188, 64))
    d.line(S(140, 268, 340, 268), fill=(214, 150, 40), width=6 * s)
    p0, p1, p2 = (330, 225), (560, 60), (720, 300)
    path = [bez(p0, p1, p2, i / 40) for i in range(41)]
    d.line([(x * s, y * s) for x, y in path], fill=(150, 36, 56), width=54 * s, joint="curve")
    d.line([(x * s, y * s) for x, y in path], fill=(196, 64, 84), width=34 * s, joint="curve")
    hp_ = heart_poly(800 * s, 330 * s, 190 * s)
    d.polygon(hp_, fill=RED, outline=(160, 30, 50))
    img = img.resize((PW, PH), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    lf = font(F_XB, 28)
    d.text((110, 120), "ADRENAL GLAND", font=lf, fill=GOLD)
    d.text((170, 600), "KIDNEY", font=lf, fill=CREAM)
    d.text((740, 460), "HEART", font=lf, fill=CREAM)
    if ta >= flow_t0:
        tt = ta - flow_t0
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.polygon([(140, 268), (340, 268), (250, 160)], fill=(255, 220, 120, int(150 * min(1, tt * 3))))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(img)
        af = font(F_BLACK, 22)
        for i in range(6):
            u = (tt * 0.45 + i / 6) % 1.0
            if tt * 0.45 < i / 6: continue
            x, y = bez(p0, p1, p2, u)
            d.ellipse((x - 17, y - 17, x + 17, y + 17), fill=GOLD, outline=INK, width=3)
            d.text((x, y), "A", font=af, fill=INK, anchor="mm")
    return img

# ---------------------------------------------------------------- bar chart (Wittstein 2005, median epinephrine)
def draw_bars(k, show_ratio):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "Adrenaline in the blood", font=font(F_XB, 34), fill=CREAM)
    d.text((40, 76), "median, pg/mL · Wittstein et al., NEJM 2005", font=font(F_SB, 24), fill=(150, 176, 196))
    x0, x1, y0, y1, vmax = 150, 890, 560, 150, 1500
    yv = lambda v: y0 - (y0 - y1) * v / vmax
    tf = font(F_SB, 24)
    for v in (0, 500, 1000, 1500):
        d.line((x0, yv(v), x1, yv(v)), fill=(34, 56, 80), width=2)
        d.text((x0 - 14, yv(v)), f"{v:,}", font=tf, fill=(150, 176, 196), anchor="rm")
    bars = [(370, 376, "Heart attack", (120, 150, 176)), (680, 1264, "Stunned by stress", (255, 140, 40))]
    vf = font(F_BLACK, 40); lf = font(F_XB, 28)
    for cx, val, lab, col in bars:
        v = val * k
        if y0 - yv(v) > 26:
            d.rounded_rectangle((cx - 100, yv(v), cx + 100, y0), radius=12, fill=col)
            d.rectangle((cx - 100, yv(v) + 12, cx + 100, y0), fill=col)
        elif y0 - yv(v) >= 1:
            d.rectangle((cx - 100, yv(v), cx + 100, y0), fill=col)
        d.text((cx, y0 + 34), lab, font=lf, fill=CREAM, anchor="mm")
        if k > 0.05:
            d.text((cx, yv(v) - 30), f"{int(round(v)):,}", font=vf, fill=CREAM, anchor="mm")
    if show_ratio > 0:
        p = pill("3.4× MORE", 44, INK, GOLD, padx=26, pady=14).rotate(-6, expand=True, resample=Image.BICUBIC)
        sc = 1.4 - 0.4 * show_ratio
        p = p.resize((int(p.width * sc), int(p.height * sc)), Image.BILINEAR)
        paste_alpha(img, p, (370 - p.width / 2, 250 - p.height / 2), show_ratio)
    return img

# ---------------------------------------------------------------- heart + ECG
def beat_times(t_from, t_to, irregular_from):
    out, t, rnd = [], 0.0, random.Random(5)
    while t < t_to + 3:
        out.append(t)
        t += rnd.uniform(0.28, 1.1) if t >= irregular_from else 0.72
    return out

def draw_heart(ta, stun_t, irr_t, crack_t, heal_t):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS)
    bts = beat_times(0, ta, irr_t)
    last = max([b for b in bts if b <= ta] or [0])
    since = ta - last
    stun = k_at(ta, stun_t, 0.5) * (1 - k_at(ta, heal_t, 0.8)) if heal_t else k_at(ta, stun_t, 0.5)
    pulse = math.exp(-since / 0.12) * (1 - 0.6 * stun)
    size = 330 * (1 + 0.09 * pulse)
    col = tuple(int(lerp(c1, c2, stun)) for c1, c2 in zip(RED, (150, 110, 124)))
    lay = Image.new("RGBA", (PW * 2, PH * 2), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.polygon(heart_poly(470 * 2, 270 * 2, size * 2), fill=col)
    ld.polygon(heart_poly(430 * 2, 220 * 2, size * 0.5), fill=tuple(min(255, c + 40) for c in col))
    ck = k_at(ta, crack_t, 0.2) if crack_t else 0
    hk = k_at(ta, heal_t, 0.8) if heal_t else 0
    if ck > 0:
        zz = [(470, 120), (440, 190), (500, 240), (450, 300), (490, 360), (470, 420)]
        n = max(2, int(len(zz) * ck))
        ld.line([(x * 2, y * 2) for x, y in zz[:n]], fill=(30, 10, 20, int(255 * (1 - hk))), width=22, joint="curve")
    if hk > 0:
        b = Image.new("RGBA", (300, 90), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
        bd.rounded_rectangle((0, 0, 299, 89), radius=40, fill=(242, 206, 168, int(255 * hk)))
        bd.rounded_rectangle((110, 10, 190, 79), radius=12, fill=(226, 180, 140, int(255 * hk)))
        b = b.rotate(35, expand=True, resample=Image.BICUBIC)
        lay.alpha_composite(b, (470 * 2 - b.width // 2, 270 * 2 - b.height // 2))
    img.alpha_composite(lay.resize((PW, PH), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    # ECG strip: last 3 seconds scroll right-to-left
    y_base, x0, x1, span = 560, 40, 900, 3.0
    pts = []
    for i in range(240):
        tx = ta - span + span * i / 239
        y = 0.0
        for b in bts:
            dt = tx - b
            amp = 1.0 if b < irr_t else random.Random(int(b * 100)).uniform(0.4, 1.4)
            if -0.04 < dt < 0.0: y -= 0.25 * amp
            elif 0.0 <= dt < 0.04: y += 1.0 * amp * (1 - dt / 0.04)
            elif 0.04 <= dt < 0.08: y -= 0.4 * amp
            elif 0.2 < dt < 0.32: y += 0.18 * math.sin((dt - 0.2) / 0.12 * math.pi)
        pts.append((x0 + (x1 - x0) * i / 239, y_base - y * 70))
    ecg_col = (90, 230, 140) if hk > 0.5 or ta < irr_t else (255, 120, 90)
    d.line(pts, fill=ecg_col, width=5, joint="curve")
    d.text((40, 30), "HEART RHYTHM", font=font(F_XB, 26), fill=(150, 176, 196))
    return img

# ---------------------------------------------------------------- green bin
_bin = {}
def green_bin():
    if "b" in _bin: return _bin["b"]
    s = 3; w_, h_ = 230, 300
    im = Image.new("RGBA", (w_ * s, h_ * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(20 * s, 70 * s), (210 * s, 70 * s), (195 * s, 290 * s), (35 * s, 290 * s)], fill=(46, 140, 70), outline=(28, 96, 46))
    d.rounded_rectangle((8 * s, 40 * s, 222 * s, 82 * s), radius=10 * s, fill=(36, 118, 58))
    d.rounded_rectangle((90 * s, 22 * s, 140 * s, 44 * s), radius=6 * s, fill=(28, 96, 46))
    for x in (60, 115, 170):
        d.line((x * s, 110 * s, (x - 3) * s, 260 * s), fill=(36, 118, 58), width=6 * s)
    for ex in (92, 138):  # eyes glowing in the gap under the lid
        d.ellipse(((ex - 9) * s, 50 * s, (ex + 9) * s, 68 * s), fill=(255, 236, 120))
    im = im.resize((w_, h_), Image.LANCZOS); _bin["b"] = im
    return im

# ---------------------------------------------------------------- scenes
def s0(ta):
    f = G.base(ta)
    G.big_title(f, ta, wt(0, "scared"), ["SCARED", "TO DEATH?"], y=400)
    shiver = 6 if ta < E["drop"] else 0
    G.host_cyto(f, ta, "shrug" if ta < E["drop"] else G.wave(ta), shiver=shiver, look=(0, -1))
    G.put_caption(f, ta, R.HOST_CAP_Y)
    return f

def s1(ta):
    f = G.base(ta)
    G.panel_in(f, draw_adrenal(ta, wt(1, "floods")), ta)
    G.card_in(f, ta, ("ADRENALINE", "Also called epinephrine. Your adrenal glands make it."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s2(ta):
    f = G.base(ta)
    k = ease((ta - wt(2, "had")) / 1.2)
    G.panel_in(f, draw_bars(k, k_at(ta, wt(2, "three"), 0.18)), ta)
    G.card_in(f, ta, ("THE STUDY", "19 patients whose hearts were stunned by a sudden shock."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s3(ta):
    f = G.base(ta)
    G.panel_in(f, draw_heart(ta, wt(3, "stun"), wt(3, "rhythm"), wt(3, "broken"), None), ta)
    G.card_in(f, ta, ("TAKOTSUBO", "The medical name for broken heart syndrome."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s4(ta):
    f = G.base(ta)
    f.alpha_composite(draw_heart(ta, wt(3, "stun"), wt(3, "rhythm"), wt(3, "broken"), wt(4, "recover") - 0.3), R.PANEL_XY)
    G.stamp(f, ta, wt(4, "rare"), "RARE", (R.PANEL_XY[0] + 780, R.PANEL_XY[1] + 120), size=48, bg=TEAL_L)
    G.card_in(f, ta, ("GOOD NEWS", "In the study, hearts bounced back within 2–4 weeks."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s5(ta):
    f = G.base(ta)
    b = green_bin()
    k = k_at(ta, wt(5, "raccoon") - 0.1, 0.25)
    paste_alpha(f, b, (40, 1080 + (1 - k) * 60), k)
    G.stamp(f, ta, wt(5, "2"), "2:00 AM", (780, 640), size=50, fg=CREAM, bg=(60, 40, 90), rot=5)
    G.host_cyto(f, ta, G.wave(ta) if ta < wt(5, "raccoon") else "rest", eyes="open")
    G.sources_card(f, ta, wt(5, "Toronto"), ["Wittstein et al., N Engl J Med 2005", "Samuels, Cleve Clin J Med 2007"])
    G.put_caption(f, ta, R.HOST_CAP_Y)
    return f

SCENES = [s0, s1, s2, s3, s4, s5]
if __name__ == "__main__":
    beats = [b for b in beat_times(0, 30, wt(3, "rhythm")) if E["cuts"][3] <= b < E["cuts"][5]]
    events = [("pop", wt(0, "kinda")), ("zap", wt(1, "floods")), ("boom", wt(2, "three")), ("boom", wt(3, "broken")),
              ("ding", wt(4, "recover")), ("pop", wt(4, "rare")), ("pop", wt(5, "2")), ("crunch", wt(5, "raccoon"))] + [("beat", b) for b in beats]
    G.run(SCENES, "cyto-ep2-scared-to-death.mp4", sys.argv[1],
          still_times=[wt(0, "Halloween"), wt(1, "hormone"), wt(2, "patients"), wt(3, "syndrome"), wt(4, "weeks"), wt(5, "though")], events=events)
