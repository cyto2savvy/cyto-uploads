"""Ep 4: Clocks fall back.  python3 ep4.py stills|video"""
import math, sys
from PIL import Image, ImageDraw, ImageFilter
import engine as G
from engine import wt, k_at, E, FX
import render as R
from render import W, H, font, F_XB, F_SB, F_BLACK, CREAM, GOLD, CORAL, INK, TEAL_L, PW, PH, lerp, ease, pill, paste_alpha

G.init("/home/claude/ep4", None, drop=(0, "clocks"), halloween=False,
       hits=[(0, "clocks"), (1, "switch"), (2, "twice"), (3, "Ontario"), (4, "subscribe")])
CAPY = R.HOST_CAP_Y

def clock_face(size, ang_min, ang_hr):
    s = 3; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2
    d.ellipse((0, 0, S - 1, S - 1), fill=(250, 244, 232), outline=INK, width=10 * s)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        r0, r1 = c * (0.78 if i % 3 else 0.70), c * 0.88
        d.line((c + math.sin(a) * r0, c - math.cos(a) * r0, c + math.sin(a) * r1, c - math.cos(a) * r1), fill=INK, width=(8 if i % 3 == 0 else 4) * s)
    for ang, ln, wd, col in ((ang_hr, 0.48, 14, INK), (ang_min, 0.72, 9, CORAL)):
        d.line((c, c, c + math.sin(ang) * c * ln, c - math.cos(ang) * c * ln), fill=col, width=wd * s)
    d.ellipse((c - 16 * s, c - 16 * s, c + 16 * s, c + 16 * s), fill=INK)
    return im.resize((size, size), Image.LANCZOS)

def s0(ta):
    f = G.base(ta)
    t_fb = wt(0, "fall")
    spin = -max(0.0, min(1.0, (ta - t_fb) / 1.2)) * 2 * math.pi   # minute hand winds back one hour
    c = clock_face(250, 0.0 + spin, math.radians(60) + spin / 12)
    paste_alpha(f, c, (W / 2 - 125, 270), k_at(ta, 0.1, 0.3))
    G.big_title(f, ta, wt(0, "clocks"), ["CLOCKS FALL BACK"], y=640, size=96)
    G.stamp(f, ta, wt(0, "Free"), "+1 HOUR?", (880, 390), size=40, bg=TEAL_L, rot=8)
    G.stamp(f, ta, wt(0, "Not"), "NOT EXACTLY", (205, 390), size=40, fg=CREAM, bg=CORAL, rot=-8)
    G.put_cyto(f, 460, (540, 1060), ta, G.mouth(ta), G.wave(ta) if ta < wt(0, "Free") else "shrug")
    G.put_caption(f, ta, 1400)
    return f

def draw_rhythm(ta, t_switch):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "YOUR BODY CLOCK", font=font(F_BLACK, 40), fill=CREAM)
    d.text((40, 82), "SCN = the master clock in your brain, set by light", font=font(F_SB, 24), fill=(150, 176, 196))
    x0, x1, yc, amp = 60, 880, 380, 120
    shift = 0.0
    if ta >= t_switch:
        shift = min(1.0, (ta - t_switch) / 0.25) * (PW / 24) * 1.5       # one hour jolt
    for h in range(0, 25, 6):
        x = x0 + (x1 - x0) * h / 24
        d.line((x, yc - amp - 20, x, yc + amp + 20), fill=(34, 56, 80), width=2)
        d.text((x, yc + amp + 48), f"{h:02d}:00", font=font(F_SB, 22), fill=(150, 176, 196), anchor="mm")
    def wave(off, col, wdt):
        pts = [(x0 + (x1 - x0) * i / 200, yc - amp * math.sin((i / 200) * 2 * math.pi - math.pi / 2 + off)) for i in range(201)]
        d.line(pts, fill=col, width=wdt, joint="curve")
    if ta >= t_switch:
        wave(0, (80, 110, 140), 6)
        wave(-shift / (x1 - x0) * 2 * math.pi, GOLD, 9)
        d.text((x1 - 10, 150), "OFF BEAT", font=font(F_BLACK, 36), fill=CORAL, anchor="rm")
    else:
        wave(0, GOLD, 9)
    return img

def s1(ta):
    f = G.base(ta)
    G.panel_in(f, draw_rhythm(ta, wt(1, "switch")), ta)
    G.card_in(f, ta, ("CIRCADIAN RHYTHM", "Your ~24-hour cycle of sleep, hunger and alertness."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def draw_rank(ta, t_reveal):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "Strain on your body clock", font=font(F_BLACK, 38), fill=CREAM)
    d.text((40, 80), "ranking from a Stanford model · PNAS 2025", font=font(F_SB, 24), fill=(150, 176, 196))
    rows = [("Switching twice a year", 1.0, CORAL), ("Permanent daylight time", 0.62, (120, 150, 176)), ("Permanent standard time", 0.45, TEAL_L)]
    for i, (lab, v, col) in enumerate(rows):
        y = 170 + i * 150
        k = ease((ta - t_reveal - i * 0.25) / 0.6)
        d.text((60, y), lab, font=font(F_XB, 30), fill=CREAM)
        wmax = 760
        if k > 0.01:
            d.rounded_rectangle((60, y + 48, 60 + max(24, wmax * v * k), y + 98), radius=14, fill=col)
        if i == 0 and k > 0.95:
            d.text((60 + wmax * v - 16, y + 73), "WORST", font=font(F_BLACK, 30), fill=INK, anchor="rm")
    d.text((60, 640), "Bar length shows the ranking only, not exact values.", font=font(F_SB, 20), fill=(120, 146, 166))
    return img

def s2(ta):
    f = G.base(ta)
    G.panel_in(f, draw_rank(ta, wt(2, "switching")), ta)
    G.card_in(f, ta, ("PNAS, 2025", "Picking one time and sticking to it beats switching."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def draw_board(ta, t_on):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.rectangle((30, 28, PW - 30, 92), fill=(20, 20, 26))
    d.text((50, 60), "CLOCK CHANGE · DEPARTURES", font=font(F_BLACK, 32), fill=(255, 196, 60), anchor="lm")
    rows = [("MANITOBA", "DONE SWITCHING", TEAL_L), ("ALBERTA · B.C.", "PERMANENT TIME", TEAL_L), ("SASK · YUKON · N.W.T.", "PERMANENT TIME", TEAL_L),
            ("ONTARIO", "STILL SWITCHING", CORAL)]
    mf = font(F_XB, 30)
    for i, (prov, status, col) in enumerate(rows):
        y = 130 + i * 92
        k = k_at(ta, t_on + i * 0.18, 0.15)
        if k <= 0: continue
        d.rectangle((30, y, PW - 30, y + 76), fill=(16, 16, 22))
        flip = "".join(chr(65 + (int(ta * 30) + j) % 26) if k < 1 and c != " " else c for j, c in enumerate(status))
        d.text((50, y + 38), prov, font=mf, fill=CREAM, anchor="lm")
        d.text((PW - 50, y + 38), flip, font=mf, fill=col, anchor="rm")
    d.text((PW / 2, 545), "ONTARIO IS WAITING ON:", font=font(F_XB, 28), fill=(150, 176, 196), anchor="mm")
    d.text((PW / 2, 600), "QUEBEC + NEW YORK", font=font(F_BLACK, 44), fill=GOLD, anchor="mm")
    return img

def s3(ta):
    f = G.base(ta)
    G.panel_in(f, draw_board(ta, wt(3, "Manitoba")), ta)
    G.card_in(f, ta, ("BILL 214", "Ontario only drops the switch if Quebec and New York do."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def s4(ta):
    f = G.base(ta)
    G.sources_card(f, ta, E["cuts"][4] + 0.1, ["Weed & Zeitzer, PNAS 2025 (PubMed)", "Province status: blogTO, Oct 2026"], title="SOURCES")
    G.outro(f, ta, 4)
    G.put_cyto(f, 460, (540, 1080), ta, G.mouth(ta), G.wave(ta))
    G.put_caption(f, ta, 1420)
    return f

SCENES = [s0, s1, s2, s3, s4]
if __name__ == "__main__":
    FX["shakes"] = [wt(1, "switch"), wt(2, "twice"), wt(3, "Ontario"), wt(4, "out") + 0.35]
    FX["bursts"] = [(wt(0, "clocks"), (540, 640), GOLD), (wt(2, "twice"), (540, 1060), CORAL), (wt(4, "subscribe") + 0.55, (640, 480), GOLD)]
    ev = [("pop", wt(0, "Free")), ("pop", wt(0, "Not")), ("zap", wt(1, "switch")), ("boom", wt(2, "twice")),
          ("pop", wt(3, "Manitoba")), ("boom", wt(3, "Ontario")), ("pop", wt(4, "Like") + 0.35), ("ding", wt(4, "subscribe") + 0.55), ("boom", wt(4, "out") + 0.35)]
    G.run_v3(SCENES, "cyto-ep4-clocks-fall-back.mp4", sys.argv[1],
             still_times=[wt(0, "Not") + 0.3, wt(1, "beat"), wt(2, "sticking"), wt(3, "York"), wt(4, "subscribe") + 0.8, wt(4, "out") + 0.3], events=ev)
