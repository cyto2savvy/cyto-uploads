"""Ep 3: The sugar rush is fake.  python3 ep3.py stills|video"""
import math, random, sys
from PIL import Image, ImageDraw
import engine as G
from engine import wt, k_at, E
import render as R
from render import W, H, font, F_XB, F_SB, F_BLACK, CREAM, GOLD, CORAL, INK, TEAL_L, PW, PH, lerp, ease, pill, paste_alpha

G.init("/home/claude/ep3", "streetcar", drop=(1, "Nah"),
       hits=[(0, "Sugar"), (2, "didn't"), (3, "hyper"), (4, "heads"), (5, "cooked")])

PINK = (255, 130, 170)
CANDY = [(255, 120, 60), (170, 90, 230), (90, 200, 120), (255, 200, 60), (255, 90, 130)]

_cd = {}
def candy(col, size=90):
    key = (col, size)
    if key in _cd: return _cd[key]
    s = 3; w_, h_ = size * 2, size
    im = Image.new("RGBA", (w_ * s, h_ * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, h_ * .15 * s), (w_ * .3 * s, h_ * .5 * s), (0, h_ * .85 * s)], fill=col)
    d.polygon([(w_ * s, h_ * .15 * s), (w_ * .7 * s, h_ * .5 * s), (w_ * s, h_ * .85 * s)], fill=col)
    d.ellipse((w_ * .25 * s, h_ * .1 * s, w_ * .75 * s, h_ * .9 * s), fill=col)
    d.arc((w_ * .32 * s, h_ * .2 * s, w_ * .62 * s, h_ * .7 * s), 200, 300, fill=(255, 255, 255), width=4 * s)
    im = im.resize((w_, h_), Image.LANCZOS); _cd[key] = im
    return im

def candies(f, ta, t0, n=8):
    rnd = random.Random(3)
    for i in range(n):
        x0 = rnd.uniform(60, 900); vx = rnd.uniform(-160, 160); ph = rnd.uniform(0, 1)
        tt = ta - t0 + ph
        if ta < t0: continue
        y = 1250 - abs(math.sin(tt * 3.2 + i)) * rnd.uniform(500, 800)
        x = (x0 + vx * tt) % 1000
        c = candy(CANDY[i % 5], rnd.choice((70, 90)))
        c = c.rotate((tt * 200 + i * 40) % 360, expand=True, resample=Image.BICUBIC)
        paste_alpha(f, c, (x, y), min(1, (ta - t0) * 4))

# ---------------------------------------------------------------- 23 blinded studies
def draw_studies(ta, t_split, t_blind):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "23 BLINDED STUDIES", font=font(F_BLACK, 40), fill=CREAM)
    sk, bk = k_at(ta, t_split, 0.3), k_at(ta, t_blind, 0.3)
    cols, rows, cw, ch = 8, 3, 100, 130
    x_0, y_0 = (PW - cols * cw) / 2 + 10, 110
    qf = font(F_BLACK, 44)
    for i in range(23):
        r, c = divmod(i, cols)
        x, y = x_0 + c * cw, y_0 + r * (ch + 16)
        appear = k_at(ta, E["cuts"][1] + 0.1 + i * 0.03, 0.15)
        if appear <= 0: continue
        d.rounded_rectangle((x, y, x + 80, y + ch - 20), radius=10, fill=(236, 240, 244))
        for l in range(3):
            d.line((x + 12, y + 16 + l * 14, x + 66, y + 16 + l * 14), fill=(170, 182, 194), width=4)
        if sk > 0:
            if i % 2 == 0:
                d.rectangle((x + 22, y + 62, x + 58, y + 98), fill=(255, 255, 255), outline=(150, 160, 170), width=3)
            else:
                d.rounded_rectangle((x + 16, y + 66, x + 64, y + 94), radius=6, fill=PINK)
        if bk > 0:
            d.rounded_rectangle((x - 4, y + 54, x + 84, y + 106), radius=10, fill=(30, 30, 40))
            d.text((x + 40, y + 80), "?", font=qf, fill=GOLD, anchor="mm")
    lf = font(F_XB, 26)
    if sk > 0:
        d.rectangle((60, 600, 90, 630), fill=(255, 255, 255)); d.text((104, 615), "REAL SUGAR", font=lf, fill=CREAM, anchor="lm")
        d.rounded_rectangle((370, 602, 410, 628), radius=6, fill=PINK); d.text((424, 615), "FAKE SWEETENER", font=lf, fill=CREAM, anchor="lm")
    return img

# ---------------------------------------------------------------- result
def draw_result(ta, t_res):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "Behavior & focus", font=font(F_BLACK, 40), fill=CREAM)
    d.text((40, 82), "All 14 measures: no real difference · JAMA 1995", font=font(F_SB, 24), fill=(150, 176, 196))
    k = ease((ta - E["cuts"][2] - 0.2) / 1.0)
    base_y, hgt = 540, 300 * k
    for cx, lab, col in ((300, "SUGAR", (245, 245, 245)), (640, "FAKE SWEETENER", PINK)):
        if hgt > 2:
            d.rounded_rectangle((cx - 110, base_y - hgt, cx + 110, base_y), radius=12, fill=col)
        d.text((cx, base_y + 40), lab, font=font(F_XB, 30), fill=CREAM, anchor="mm")
    d.line((140, base_y - 300, 800, base_y - 300), fill=GOLD, width=4)
    if k > 0.9:
        d.text((470, base_y - 330), "same", font=font(F_XB, 28), fill=GOLD, anchor="mm")
    return img

# ---------------------------------------------------------------- the twist
def gauge(d, cx, cy, r, val, col):
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(52, 76, 100), width=24)
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 180 + int(180 * val), fill=col, width=24)
    a = math.pi * (1 - val)
    d.line((cx, cy, cx + math.cos(a) * (r - 10), cy - math.sin(a) * (r - 10)), fill=CREAM, width=8)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=CREAM)

def draw_twist(ta, t_hyper):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    lf, sf = font(F_XB, 28), font(F_SB, 24)
    hk = k_at(ta, t_hyper, 0.5)
    for cx, told, col, v_end in ((240, "SUGAR", CORAL, 0.88), (700, "NOTHING", TEAL_L, 0.35)):
        p = pill(f"MOM TOLD: {told}", 26, INK, col)
        img.alpha_composite(p, (int(cx - p.width / 2), 40))
        d = ImageDraw.Draw(img)
        d.polygon([(cx - 55, 120), (cx + 55, 120), (cx + 42, 260), (cx - 42, 260)], fill=PINK, outline=(200, 90, 130))
        d.text((cx, 190), "FAKE", font=font(F_BLACK, 34), fill=INK, anchor="mm")
        wob = math.sin(ta * 6) * 0.03
        gauge(d, cx, 500, 150, (0.35 + (v_end - 0.35) * hk) + wob, col)
        d.text((cx, 560), "hyper rating", font=sf, fill=(150, 176, 196), anchor="mm")
    d.text((470, 625), "Every kid got the fake sweetener", font=lf, fill=CREAM, anchor="mm")
    return img

# ---------------------------------------------------------------- tooth
_t = {}
def tooth(cook):
    s = 3; w_, h_ = 300, 340
    im = Image.new("RGBA", (w_ * s, h_ * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *p: [v * s for v in p]
    d.rounded_rectangle(S(20, 20, 280, 200), radius=90 * s, fill=(250, 248, 240), outline=(200, 196, 186), width=6 * s)
    d.polygon(S(40, 150, 140, 150, 110, 330, 70, 330), fill=(250, 248, 240))
    d.polygon(S(160, 150, 260, 150, 230, 330, 190, 330), fill=(250, 248, 240))
    if cook > 0:
        d.ellipse(S(150, 50, 230, 120), fill=(60, 40, 30))
        d.line(S(120, 40, 140, 100, 115, 150, 135, 200), fill=(70, 50, 40), width=8 * s, joint="curve")
    return im.resize((w_, h_), Image.LANCZOS)

# ---------------------------------------------------------------- scenes
def s0(ta):
    f = G.base(ta)
    candies(f, ta, 0.4)
    G.big_title(f, ta, wt(0, "Sugar"), ["SUGAR", "RUSH?"], y=400)
    G.host_cyto(f, ta, G.wave(ta), bounce=70, shiver=4)
    G.put_caption(f, ta, R.HOST_CAP_Y)
    return f

def s1(ta):
    f = G.base(ta)
    G.panel_in(f, draw_studies(ta, wt(1, "real"), wt(1, "nobody")), ta)
    G.card_in(f, ta, ("BLINDED", "Kids, parents and researchers didn't know who got what."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s2(ta):
    f = G.base(ta)
    G.panel_in(f, draw_result(ta, wt(2, "didn't")), ta)
    G.stamp(f, ta, wt(2, "didn't"), "NO CHANGE", (R.PANEL_XY[0] + 470, R.PANEL_XY[1] + 330), size=54, bg=GOLD)
    G.card_in(f, ta, ("JAMA, 1995", "A meta-analysis pooling 23 studies on sugar and kids."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s3(ta):
    f = G.base(ta)
    G.panel_in(f, draw_twist(ta, wt(3, "hyper")), ta)
    G.stamp(f, ta, wt(3, "Plot"), "PLOT TWIST", (R.PANEL_XY[0] + 470, R.PANEL_XY[1] + 200), size=54, fg=CREAM, bg=CORAL, rot=4)
    G.card_in(f, ta, ("EXPECTATIONS", "Expecting a sugar rush changed what moms saw."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s4(ta):
    f = G.base(ta)
    G.stamp(f, ta, wt(4, "heads"), "IT'S IN OUR HEADS", (540, 520), size=60, bg=GOLD, rot=-4)
    G.host_cyto(f, ta, "rest")
    G.put_caption(f, ta, R.HOST_CAP_Y)
    return f

def s5(ta):
    f = G.base(ta)
    ck = k_at(ta, wt(5, "cooked"), 0.15)
    t_ = tooth(ck); t_ = t_.resize((240, 272), Image.LANCZOS)
    paste_alpha(f, t_, (60, 470 + math.sin(ta * 30) * 5 * ck), k_at(ta, wt(5, "teeth") - 0.1, 0.2))
    G.stamp(f, ta, wt(5, "cooked"), "COOKED", (800, 640), size=58, fg=CREAM, bg=CORAL, rot=6)
    G.host_cyto(f, ta, "shrug" if ta < wt(5, "cooked") + 0.6 else G.wave(ta))
    G.sources_card(f, ta, wt(5, "teeth"), ["Wolraich et al., JAMA 1995", "Hoover & Milich, J Abnorm Child Psychol 1994"])
    G.put_caption(f, ta, R.HOST_CAP_Y)
    return f

SCENES = [s0, s1, s2, s3, s4, s5]
if __name__ == "__main__":
    events = [("pop", wt(0, "bouncing")), ("pop", wt(0, "walls")), ("pop", wt(1, "real")), ("pop", wt(1, "nobody")),
              ("zap", wt(2, "didn't")), ("ding", wt(3, "Plot")), ("boom", wt(3, "hyper")), ("boom", wt(4, "heads")),
              ("crunch", wt(5, "teeth")), ("boom", wt(5, "cooked"))]
    G.run(SCENES, "cyto-ep3-sugar-rush.mp4", sys.argv[1],
          still_times=[wt(0, "right"), wt(1, "which"), wt(2, "focus"), wt(3, "hyper") + 0.4, wt(4, "heads") + 0.2, wt(5, "cooked") + 0.3], events=events)
