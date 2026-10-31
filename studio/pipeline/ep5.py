"""Ep 5: Why cold season = sick season.  python3 ep5.py stills|video"""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
import engine as G
from engine import wt, k_at, E, FX
import render as R
from render import W, H, font, F_XB, F_SB, F_BLACK, CREAM, GOLD, CORAL, INK, TEAL_L, PW, PH, lerp, ease, pill, paste_alpha

G.init("/home/claude/ep5", "scarf", drop=(0, "Nah"), halloween=False,
       hits=[(0, "sick"), (1, "vesicles"), (2, "weakens"), (3, "warm"), (4, "subscribe")])
ICE = (170, 220, 255)

def snow(f, ta, n=60, heavy=1.0):
    rnd = random.Random(9)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(int(n * heavy)):
        x0 = rnd.uniform(0, W); sp = rnd.uniform(80, 220); r = rnd.uniform(3, 9); ph = rnd.uniform(0, H)
        y = (ph + ta * sp) % (H + 40) - 20
        x = x0 + math.sin(ta * 1.5 + i) * 30
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 200))
    f.alpha_composite(lay)

def virus(size, alpha=255):
    s = 3; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2
    for i in range(10):
        a = i / 10 * 2 * math.pi
        d.line((c, c, c + math.cos(a) * c * .95, c + math.sin(a) * c * .95), fill=(200, 40, 70, alpha), width=4 * s)
        d.ellipse((c + math.cos(a) * c * .85 - 5 * s, c + math.sin(a) * c * .85 - 5 * s, c + math.cos(a) * c * .85 + 5 * s, c + math.sin(a) * c * .85 + 5 * s), fill=(200, 40, 70, alpha))
    d.ellipse((c * .35, c * .35, c * 1.65, c * 1.65), fill=(236, 70, 96, alpha))
    return im.resize((size, size), Image.LANCZOS)

def draw_nose(ta, t_fire, cold):
    """cold: 0..1 — fewer, weaker vesicles; viruses get through"""
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "INSIDE YOUR NOSE", font=font(F_BLACK, 40), fill=CREAM)
    # nasal lining: row of cells along the bottom
    for i in range(10):
        x = 20 + i * 92
        d.rounded_rectangle((x, 500, x + 86, 650), radius=26, fill=(236, 150, 150), outline=(190, 100, 104), width=4)
        d.ellipse((x + 30, 560, x + 56, 586), fill=(150, 70, 110))
    d.text((PW - 40, 476), "nasal lining", font=font(F_SB, 24), fill=(236, 170, 170), anchor="rs")
    # viruses drifting down
    rnd = random.Random(4)
    vs = []
    for i in range(5):
        vx = 120 + i * 170 + rnd.uniform(-30, 30)
        vy = 130 + ((ta * 40 + i * 37) % 220)
        vs.append((vx, vy))
    # vesicles: fired from cells toward viruses
    n_ves = int(round(lerp(18, 6, cold)))
    neutral = set()
    if ta >= t_fire:
        tt = ta - t_fire
        for j in range(n_ves):
            tgt = vs[j % 5]
            src = (66 + (j * 3 % 10) * 92, 500)
            u = (tt * 0.8 + j / n_ves) % 1.0
            miss = (j % 3 == 0) and cold > 0.5
            tx = tgt[0] + (90 if miss else 0)
            x, y = lerp(src[0], tx, ease(u)), lerp(src[1], tgt[1], ease(u))
            r = lerp(13, 8, cold)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(160, 230, 255), outline=(255, 255, 255), width=2)
            if u > 0.85 and not miss: neutral.add(j % 5)
    for i, (vx, vy) in enumerate(vs):
        a = 90 if (i in neutral and cold < 0.5) else 255
        v = virus(64, a)
        img.alpha_composite(v, (int(vx - 32), int(vy - 32)))
    if cold > 0:
        fr = Image.new("RGBA", img.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(fr)
        fd.rounded_rectangle((0, 0, PW - 1, PH - 1), radius=34, outline=ICE + (int(200 * cold),), width=18)
        img.alpha_composite(fr.filter(ImageFilter.GaussianBlur(6)))
        d = ImageDraw.Draw(img)
        # thermometer
        tx, ty = PW - 90, 120
        d.rounded_rectangle((tx, ty, tx + 40, ty + 260), radius=20, fill=(240, 240, 240), outline=INK, width=3)
        lvl = lerp(200, 40, cold)
        d.rounded_rectangle((tx + 10, ty + 250 - lvl, tx + 30, ty + 250), radius=10, fill=(90, 160, 255))
        d.ellipse((tx - 10, ty + 240, tx + 50, ty + 300), fill=(90, 160, 255), outline=INK, width=3)
    return img

def s0(ta):
    f = G.base(ta)
    snow(f, ta)
    G.big_title(f, ta, wt(0, "sick"), ["EVERYONE'S SICK"], y=430, size=100)
    G.stamp(f, ta, wt(0, "Coincidence"), "COINCIDENCE?", (540, 600), size=50, fg=CREAM, bg=CORAL, rot=-5)
    G.put_cyto(f, 500, (540, 1040), ta, G.mouth(ta), "shrug" if ta < E["drop"] else "rest", shiver=6 if ta < E["drop"] else 0)
    G.put_caption(f, ta, 1400)
    return f

def s1(ta):
    f = G.base(ta)
    G.panel_in(f, draw_nose(ta, wt(1, "firing"), 0.0), ta)
    G.card_in(f, ta, ("EXTRACELLULAR VESICLES", "Tiny bubbles nose cells release to trap viruses."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s2(ta):
    f = G.base(ta)
    cold = k_at(ta, wt(2, "cold"), 0.8)
    f.alpha_composite(draw_nose(ta, E["cuts"][2] - 1.5, cold), R.PANEL_XY)
    G.stamp(f, ta, wt(2, "Fewer"), "FEWER + WEAKER", (R.PANEL_XY[0] + 430, R.PANEL_XY[1] + 330), size=48, fg=INK, bg=ICE, rot=-4)
    G.card_in(f, ta, ("J ALLERGY CLIN IMMUNOL", "Harvard Medical School team, 2023."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s3(ta):
    f = G.base(ta)
    snow(f, ta, 40)
    G.stamp(f, ta, wt(3, "nose"), "KEEP YOUR NOSE WARM", (540, 470), size=58, bg=GOLD, rot=-3)
    G.put_cyto(f, 560, R.HOST_C, ta, G.mouth(ta), "point", (0, -1))
    G.put_caption(f, ta, R.HOST_CAP_Y)
    return f

def s4(ta):
    f = G.base(ta)
    snow(f, ta, 30)
    G.sources_card(f, ta, E["cuts"][4] + 0.1, ["Huang et al., J Allergy Clin Immunol 2023"])
    G.outro(f, ta, 4)
    G.put_cyto(f, 460, (540, 1080), ta, G.mouth(ta), G.wave(ta))
    G.put_caption(f, ta, 1420)
    return f

SCENES = [s0, s1, s2, s3, s4]
if __name__ == "__main__":
    FX["shakes"] = [wt(0, "Nah"), wt(2, "weakens"), wt(4, "out") + 0.35]
    FX["bursts"] = [(wt(1, "vesicles"), (540, 600), (160, 230, 255)), (wt(3, "warm"), (540, 470), GOLD), (wt(4, "subscribe") + 0.55, (640, 480), GOLD)]
    ev = [("pop", wt(0, "Coincidence")), ("zap", wt(1, "firing")), ("pop", wt(1, "grab")), ("boom", wt(2, "weakens")),
          ("pop", wt(2, "Fewer")), ("ding", wt(3, "warm")), ("pop", wt(4, "Like") + 0.35), ("ding", wt(4, "subscribe") + 0.55), ("boom", wt(4, "out") + 0.35)]
    G.run_v3(SCENES, "cyto-ep5-cold-season.mp4", sys.argv[1],
             still_times=[wt(0, "Coincidence") + 0.3, wt(1, "in"), wt(2, "weaker"), wt(3, "warm") + 0.3, wt(4, "subscribe") + 0.8, wt(4, "out") + 0.3], events=ev)
