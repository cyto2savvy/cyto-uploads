"""Ep 7: What happens to your body during a Leafs overtime.  python3 ep7.py stills|video"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter
import engine as G
from engine import wt, k_at, E, FX
import render as R
from render import W, H, font, F_XB, F_SB, F_BLACK, CREAM, GOLD, CORAL, INK, TEAL_L, PW, PH, lerp, ease, pill, paste_alpha

D = "/home/claude/ep7"
G.init(D, "jersey", drop=(1, "It's"), halloween=False,
       hits=[(0, "overtime"), (2, "114"), (3, "vigorous"), (4, "Overtime"), (6, "emergencies"), (7, "subscribe")])
LEAFS = (24, 70, 160)
RED = (226, 52, 72)

# ---------------------------------------------------------------- optional Unsplash photo background
PHOTO = os.path.join(D, "assets", "cn.jpg")
if os.path.exists(PHOTO):
    ph = Image.open(PHOTO).convert("RGB")
    k = max(W / ph.width, H / ph.height); ph = ph.resize((int(ph.width * k), int(ph.height * k)), Image.LANCZOS)
    ph = ph.crop(((ph.width - W) // 2, (ph.height - H) // 2, (ph.width - W) // 2 + W, (ph.height - H) // 2 + H))
    ph = ph.filter(ImageFilter.GaussianBlur(3)).convert("RGBA")
    shade = Image.new("RGBA", (W, H), (8, 16, 30, 150)); ph.alpha_composite(shade)
    PHOTO_BG = ph
else:
    PHOTO_BG = None

def photo_base(ta):
    if PHOTO_BG is None: return G.base(ta)
    f = PHOTO_BG.copy()
    paste_alpha(f, pill("THE BODY IS THE 6IX", 28, INK, GOLD), (W / 2 - pill("THE BODY IS THE 6IX", 28, INK, GOLD).width / 2, 120))
    return f

# ---------------------------------------------------------------- heart + BPM
def heart_pts(cx, cy, size):
    pts = []
    for i in range(80):
        t = 2 * math.pi * i / 80
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * size / 32, cy - y * size / 32))
    return pts

def bpm_at(ta, t0, t1, a=60, b=114):
    return int(round(lerp(a, b, ease((ta - t0) / max(0.1, t1 - t0)))))

def beat_pulse(ta, bpm):
    per = 60 / bpm
    return math.exp(-((ta % per) / per) / 0.18)

def draw_heart_big(f, ta, center, size, bpm):
    p = beat_pulse(ta, bpm)
    s = size * (1 + 0.10 * p)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.polygon(heart_pts(center[0], center[1], s * 1.08), fill=(255, 90, 110, int(70 + 80 * p)))
    lay = lay.filter(ImageFilter.GaussianBlur(18)); f.alpha_composite(lay)
    d = ImageDraw.Draw(f)
    d.polygon(heart_pts(center[0], center[1], s), fill=RED)
    d.polygon(heart_pts(center[0] - s * .14, center[1] - s * .16, s * .34), fill=(250, 120, 136))
    d.text((center[0], center[1] - s * .02), f"{bpm}", font=font(F_BLACK, int(s * .30)), fill=CREAM, anchor="mm", stroke_width=6, stroke_fill=INK)
    d.text((center[0], center[1] + s * .20), "BPM", font=font(F_XB, int(s * .10)), fill=CREAM, anchor="mm")

def s0(ta):
    f = photo_base(ta)
    t_ot = wt(0, "overtime")
    bpm = bpm_at(ta, t_ot, wt(0, "gym", "t1"), 72, 150)
    draw_heart_big(f, ta, (540, 470), 330, bpm)
    G.stamp(f, ta, wt(0, "gym"), "OVERTIME = WORKOUT?!", (540, 760), size=54, fg=CREAM, bg=CORAL, rot=-4)
    G.put_cyto(f, 440, (540, 1130), ta, G.mouth(ta), "shrug", eyes="open", shiver=4)
    G.put_caption(f, ta, 1450)
    return f

def s1(ta):
    f = photo_base(ta)
    k = k_at(ta, E["cuts"][1], 0.3)
    card = pill("LIVE FROM THE 6IX", 72, INK, GOLD, padx=40, pady=24)
    paste_alpha(f, card, (W / 2 - card.width / 2, 520 + (1 - k) * 40), k)
    ins = pill("…INSIDE YOUR BODY", 44, CREAM, CORAL, padx=28, pady=14)
    paste_alpha(f, ins, (W / 2 - ins.width / 2, 660), k_at(ta, wt(1, "inside"), 0.2))
    G.put_cyto(f, 520, (540, 1100), ta, G.mouth(ta), G.wave(ta))
    G.put_caption(f, ta, 1450)
    return f

# ---------------------------------------------------------------- ECG monitor
def draw_monitor(ta, t0, t1):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    bpm = bpm_at(ta, t0, t1)
    d.text((40, 30), "HEART MONITOR · HOCKEY FAN", font=font(F_XB, 30), fill=(150, 176, 196))
    d.text((PW - 40, 120), f"{bpm}", font=font(F_BLACK, 150), fill=(90, 230, 140) if bpm < 90 else CORAL, anchor="rm")
    d.text((PW - 40, 210), "BPM", font=font(F_XB, 34), fill=CREAM, anchor="rm")
    span, y0, x0, x1 = 3.0, 450, 40, PW - 40
    pts = []
    t_now = ta
    for i in range(300):
        tx = t_now - span + span * i / 299
        b = bpm_at(tx, t0, t1)
        per = 60 / b
        ph = tx % per
        y = 0
        if ph < 0.03: y = -0.25
        elif ph < 0.06: y = 1.0 * (1 - (ph - 0.03) / 0.03)
        elif ph < 0.09: y = -0.4
        elif 0.18 < ph < 0.30: y = 0.18 * math.sin((ph - 0.18) / 0.12 * math.pi)
        pts.append((x0 + (x1 - x0) * i / 299, y0 - y * 120))
    for gx in range(x0, x1, 60): d.line((gx, 300, gx, 620), fill=(20, 40, 52), width=1)
    d.line(pts, fill=(90, 230, 140) if bpm < 90 else CORAL, width=6, joint="curve")
    d.text((40, 620), "Montreal Canadiens fans · Holter monitors", font=font(F_SB, 22), fill=(120, 146, 166))
    return img

def s2(ta):
    f = G.base(ta)
    G.panel_in(f, draw_monitor(ta, wt(2, "jumped"), wt(2, "114", "t1")), ta)
    G.card_in(f, ta, ("CAN J CARDIOL, 2017", "20 healthy fans wore heart monitors during games."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

# ---------------------------------------------------------------- Mermaid diagram pan + gauge + Mito
_ff = {}
def ff_img():
    if "i" not in _ff:
        im = Image.open(os.path.join(D, "assets", "ff_crop.png")).convert("RGBA")
        k = 860 / im.width; _ff["i"] = im.resize((860, int(im.height * k)), Image.LANCZOS)
    return _ff["i"]

def draw_ff(ta, t0, t1):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS)
    dg = ff_img()
    u = ease((ta - t0) / max(0.5, t1 - t0))
    y = int(lerp(0, dg.height - (PH - 80), u))
    crop = dg.crop((0, y, dg.width, y + PH - 80))
    img.alpha_composite(crop, ((PW - dg.width) // 2, 60))
    ImageDraw.Draw(img).text((40, 18), "FIGHT-OR-FLIGHT · diagram: Mermaid", font=font(F_XB, 24), fill=(150, 176, 196))
    return img

def mito(size, ta, run=True):
    s = 3; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = S / 100
    bob = math.sin(ta * 14) * 3 * u if run else 0
    d.rounded_rectangle((10 * u, 30 * u + bob, 90 * u, 70 * u + bob), radius=20 * u, fill=(255, 159, 90), outline=(217, 106, 43), width=3 * s)
    zz = [(22 * u + i * 11 * u, 50 * u + bob + (6 * u if i % 2 else -6 * u)) for i in range(7)]
    d.line(zz, fill=(217, 106, 43), width=3 * s, joint="curve")
    for ex in (38, 60):
        d.ellipse((ex * u - 5 * u, 38 * u + bob, ex * u + 5 * u, 48 * u + bob), fill=(255, 255, 255))
        d.ellipse((ex * u - 2.5 * u, 41 * u + bob, ex * u + 2.5 * u, 46 * u + bob), fill=INK)
    d.ellipse((46 * u, 56 * u + bob, 54 * u, 64 * u + bob), fill=(80, 20, 30))        # panting mouth
    d.rounded_rectangle((8 * u, 26 * u + bob, 92 * u, 32 * u + bob), radius=3 * u, fill=CORAL)   # sweatband
    lg = math.sin(ta * 14) * 8 * u
    d.line((35 * u, 70 * u + bob, 35 * u + lg, 88 * u), fill=(217, 106, 43), width=4 * s)
    d.line((65 * u, 70 * u + bob, 65 * u - lg, 88 * u), fill=(217, 106, 43), width=4 * s)
    d.rounded_rectangle((0, 88 * u, 100 * u, 96 * u), radius=3 * u, fill=(60, 70, 84))     # treadmill
    return im.resize((size, size), Image.LANCZOS)

def gauge(d, cx, cy, r, val, col, label):
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(52, 76, 100), width=26)
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 180 + int(180 * val), fill=col, width=26)
    a = math.pi * (1 - val)
    d.line((cx, cy, cx + math.cos(a) * (r - 12), cy - math.sin(a) * (r - 12)), fill=CREAM, width=8)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=CREAM)
    d.text((cx, cy + 50), label, font=font(F_BLACK, 34), fill=CREAM, anchor="mm")

def draw_gauges(ta, t0):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((PW / 2, 50), "HOW HARD YOUR HEART WORKS", font=font(F_BLACK, 36), fill=CREAM, anchor="mm")
    k = ease((ta - t0) / 0.8)
    gauge(d, 250, 330, 160, 0.30 + 0.25 * k, GOLD, "ON TV")
    gauge(d, 690, 330, 160, 0.30 + 0.55 * k, CORAL, "AT THE ARENA")
    d.text((250, 430), "moderate", font=font(F_XB, 30), fill=GOLD, anchor="mm")
    d.text((690, 430), "vigorous", font=font(F_XB, 30), fill=CORAL, anchor="mm")
    m = mito(180, ta)
    img.alpha_composite(m, (PW // 2 - 90, 470))
    d.text((PW / 2, 470), "Mito felt that", font=font(F_SB, 22), fill=(255, 170, 110), anchor="mm")
    return img

def s3(ta):
    f = G.base(ta)
    t_arena = wt(3, "At") - 0.15
    if ta < t_arena:
        G.panel_in(f, draw_ff(ta, E["cuts"][3] + 0.2, t_arena - 0.2), ta)
        G.card_in(f, ta, ("FIGHT-OR-FLIGHT", "Your sympathetic nervous system revs the heart up."))
    else:
        panel = draw_gauges(ta, t_arena)
        k = k_at(ta, t_arena, 0.25)
        paste_alpha(f, panel, (R.PANEL_XY[0], R.PANEL_XY[1] + (1 - k) * 40), k)
        G.card_in(f, ta, ("SAME STUDY", "Live game = vigorous exercise. TV = moderate."), start=t_arena)
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

# ---------------------------------------------------------------- peak chart
def draw_peaks(ta, t0):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "When fans' heart rate peaked", font=font(F_BLACK, 38), fill=CREAM)
    d.text((40, 80), "share of peaks · Can J Cardiol 2017", font=font(F_SB, 24), fill=(150, 176, 196))
    rows = [("Overtime", 40, CORAL), ("Scoring chance FOR", 25, GOLD), ("Scoring chance AGAINST", 15, (120, 150, 176))]
    for i, (lab, v, col) in enumerate(rows):
        y = 170 + i * 150
        k = ease((ta - t0 - i * 0.2) / 0.6)
        d.text((60, y), lab, font=font(F_XB, 32), fill=CREAM)
        wmax = 700 * v / 40
        if k > 0.02: d.rounded_rectangle((60, y + 50, 60 + max(26, wmax * k), y + 104), radius=14, fill=col)
        if k > 0.5: d.text((60 + wmax * k + 18, y + 77), f"{int(round(v * k))}%", font=font(F_BLACK, 40), fill=CREAM, anchor="lm")
    return img

def s4(ta):
    f = G.base(ta)
    G.panel_in(f, draw_peaks(ta, E["cuts"][4] + 0.15), ta)
    G.stamp(f, ta, wt(4, "Overtime"), "OVERTIME", (R.PANEL_XY[0] + 600, R.PANEL_XY[1] + 560), size=64, fg=CREAM, bg=CORAL, rot=-6)
    G.card_in(f, ta, ("40% OF PEAKS", "Overtime was the #1 moment hearts maxed out."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s5(ta):
    f = photo_base(ta)
    G.stamp(f, ta, wt(5, "Leafs"), "LEAFS FANS??", (540, 520), size=78, fg=CREAM, bg=LEAFS, rot=-5)
    G.stamp(f, ta, wt(5, "don't"), "WE DON'T WANNA KNOW", (540, 700), size=44, bg=GOLD, rot=4)
    G.put_cyto(f, 520, (540, 1100), ta, G.mouth(ta), "shrug", look=(1, 0))
    G.put_caption(f, ta, 1450)
    return f

def s6(ta):
    f = G.base(ta)
    calm = 66
    draw_heart_big(f, ta, (540, 470), 280, calm)
    t_na = wt(6, "Not")
    k = k_at(ta, t_na - 0.1, 0.25)
    c = R.term_card("NOT MEDICAL ADVICE", "Heart condition? Talk to your doctor before big-game nights.", 860, 230)
    paste_alpha(f, c, (W / 2 - c.width / 2, 720 + (1 - k) * 30), k)
    k2 = k_at(ta, wt(6, "emergencies"), 0.25) * (1 - k)
    c2 = R.term_card("NEJM, 2008", "Cardiac emergencies hit 2.66x on World Cup match days in Munich.", 860, 230)
    paste_alpha(f, c2, (W / 2 - c2.width / 2, 720), k2)
    G.put_cyto(f, 400, (540, 1200), ta, G.mouth(ta), "point", (0, -1))
    G.put_caption(f, ta, 1490)
    return f

def s7(ta):
    f = photo_base(ta)
    G.sources_card(f, ta, E["cuts"][7] + 0.05, ["Khairy et al., Can J Cardiol 2017", "Wilbert-Lampen et al., N Engl J Med 2008"])
    G.outro(f, ta, 7)
    G.put_cyto(f, 460, (540, 1080), ta, G.mouth(ta), G.wave(ta))
    G.put_caption(f, ta, 1420)
    return f

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7]
if __name__ == "__main__":
    FX["shakes"] = [wt(0, "overtime"), wt(4, "Overtime"), wt(5, "Leafs"), wt(7, "out") + 0.35]
    FX["bursts"] = [(wt(1, "6ix"), (540, 560), GOLD), (wt(2, "114"), (R.PANEL_XY[0] + 700, R.PANEL_XY[1] + 150), CORAL),
                    (wt(4, "Overtime"), (R.PANEL_XY[0] + 600, R.PANEL_XY[1] + 560), GOLD), (wt(7, "subscribe") + 0.55, (640, 480), GOLD)]
    beats = []
    t = wt(2, "jumped")
    while t < wt(2, "minute", "t1"):
        beats.append(t); t += 60 / bpm_at(t, wt(2, "jumped"), wt(2, "114", "t1"))
    ev = [("boom", wt(0, "overtime")), ("pop", wt(0, "gym")), ("ding", wt(1, "6ix")), ("zap", wt(3, "fight")),
          ("pop", wt(3, "vigorous")), ("boom", wt(4, "Overtime")), ("crunch", wt(5, "Leafs")), ("pop", wt(5, "don't")),
          ("pop", wt(6, "Not")), ("pop", wt(7, "Like") + 0.35), ("ding", wt(7, "subscribe") + 0.55), ("boom", wt(7, "out") + 0.35)] + [("beat", b) for b in beats]
    G.run_v3(SCENES, "cyto-ep7-leafs-overtime.mp4", sys.argv[1],
             still_times=[wt(0, "gym") + 0.3, wt(2, "114") + 0.5, wt(3, "kicking"), wt(3, "vigorous") + 0.3, wt(5, "know"), wt(6, "doctor")], events=ev)
