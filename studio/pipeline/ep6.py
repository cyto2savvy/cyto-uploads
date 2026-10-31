"""Ep 6: Why you procrastinate.  python3 ep6.py stills|video"""
import math, sys
from PIL import Image, ImageDraw
import engine as G
from engine import wt, k_at, E, FX
import render as R
from render import W, H, font, F_XB, F_SB, F_BLACK, CREAM, GOLD, CORAL, INK, TEAL_L, PW, PH, lerp, ease, pill, paste_alpha

G.init("/home/claude/ep6", None, drop=(0, "It's"), halloween=False,
       hits=[(0, "laziness"), (1, "mood"), (2, "3,500"), (2, "stress"), (3, "five"), (4, "subscribe")])

def phone(size=200, ta=0):
    s = 3; w_, h_ = size, int(size * 1.9)
    im = Image.new("RGBA", (w_ * s, h_ * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w_ * s - 1, h_ * s - 1), radius=26 * s, fill=(20, 20, 26))
    d.rounded_rectangle((10 * s, 30 * s, (w_ - 10) * s, (h_ - 30) * s), radius=14 * s, fill=(40, 46, 60))
    off = (ta * 260) % 120
    for i in range(-1, 4):
        y = 40 + i * 120 + 120 - off
        if 34 < y < h_ - 110:
            d.rounded_rectangle((20 * s, y * s, (w_ - 20) * s, (y + 100) * s), radius=10 * s, fill=(90 + i * 30 % 120, 120, 200 - i * 20 % 80))
    return im.resize((w_, h_), Image.LANCZOS)

def s0(ta):
    f = G.base(ta)
    p = phone(170, ta).rotate(12, expand=True, resample=Image.BICUBIC)
    paste_alpha(f, p, (780, 640), k_at(ta, 0.2, 0.3))
    G.stamp(f, ta, 0.3, "DUE TOMORROW", (290, 300), size=46, fg=CREAM, bg=CORAL, rot=-6)
    G.big_title(f, ta, wt(0, "procrastinate"), ["PROCRASTINATING?"], y=460, size=96)
    G.stamp(f, ta, wt(0, "laziness"), "NOT LAZINESS", (540, 620), size=54, bg=GOLD, rot=4)
    G.put_cyto(f, 480, (480, 1060), ta, G.mouth(ta), "shrug" if ta < E["drop"] else "point", (1, -1))
    G.put_caption(f, ta, 1410)
    return f

def draw_scale(ta, t_tip):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    d.text((40, 30), "YOUR BRAIN'S CHOICE", font=font(F_BLACK, 40), fill=CREAM)
    tip = ease((ta - t_tip) / 0.6) * math.radians(14)
    cx, cy, L = PW / 2, 330, 340
    lx, ly = cx - math.cos(tip) * L, cy + math.sin(tip) * L
    rx, ry = cx + math.cos(tip) * L, cy - math.sin(tip) * L
    d.polygon([(cx - 50, 620), (cx + 50, 620), (cx, cy)], fill=(120, 140, 160))
    d.line((lx, ly, rx, ry), fill=CREAM, width=12)
    for (x, y, lab, col, sub) in ((lx, ly, "MOOD NOW", CORAL, "scroll · snack · nap"), (rx, ry, "GOALS LATER", TEAL_L, "grades · health · plans")):
        d.line((x, y, x, y + 70), fill=CREAM, width=4)
        d.rounded_rectangle((x - 150, y + 70, x + 150, y + 190), radius=20, fill=col)
        d.text((x, y + 112), lab, font=font(F_BLACK, 36), fill=INK, anchor="mm")
        d.text((x, y + 156), sub, font=font(F_SB, 22), fill=INK, anchor="mm")
    return img

def s1(ta):
    f = G.base(ta)
    G.panel_in(f, draw_scale(ta, wt(1, "picking")), ta)
    G.card_in(f, ta, ("MOOD REPAIR", "Delay = the brain trading long-term goals for feeling better now."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def draw_study(ta, t_count, t_res):
    img, d, s = G.panel_base()
    img = img.resize((PW, PH), Image.LANCZOS); d = ImageDraw.Draw(img)
    n = int(3525 * ease((ta - t_count) / 1.0)) if ta >= t_count else 0
    d.text((PW / 2, 110), f"{n:,}", font=font(F_BLACK, 110), fill=GOLD, anchor="mm")
    d.text((PW / 2, 190), "university students, tracked for 9 months", font=font(F_XB, 30), fill=CREAM, anchor="mm")
    items = [("STRESS", "up", CORAL), ("ANXIETY", "up", CORAL), ("SLEEP QUALITY", "down", (120, 150, 176))]
    for i, (lab, dirn, col) in enumerate(items):
        k = k_at(ta, t_res + i * 0.35, 0.25)
        if k <= 0: continue
        x = 170 + i * 300; y = 400
        d.rounded_rectangle((x - 130, y - 90, x + 130, y + 150), radius=24, fill=(20, 36, 56), outline=col, width=5)
        ay = y - 20 + (1 - k) * 30
        if dirn == "up":
            d.polygon([(x, ay - 60), (x - 50, ay), (x - 18, ay), (x - 18, ay + 50), (x + 18, ay + 50), (x + 18, ay), (x + 50, ay)], fill=col)
        else:
            d.polygon([(x, ay + 60), (x - 50, ay), (x - 18, ay), (x - 18, ay - 50), (x + 18, ay - 50), (x + 18, ay), (x + 50, ay)], fill=col)
        d.text((x, y + 110), lab, font=font(F_XB, 28), fill=CREAM, anchor="mm")
    d.text((PW / 2, 640), "More procrastination → worse outcomes 9 months later", font=font(F_SB, 22), fill=(150, 176, 196), anchor="mm")
    return img

def s2(ta):
    f = G.base(ta)
    G.panel_in(f, draw_study(ta, wt(2, "3,500"), wt(2, "stress")), ta)
    G.card_in(f, ta, ("JAMA NETW OPEN, 2023", "Swedish university students; linked to stress, anxiety, poor sleep."))
    G.small_cyto(f, ta); G.put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def timer(size, frac, label):
    s = 3; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=(20, 36, 56))
    d.arc((14 * s, 14 * s, S - 14 * s, S - 14 * s), -90, -90 + int(360 * frac), fill=GOLD, width=26 * s)
    im = im.resize((size, size), Image.LANCZOS)
    ImageDraw.Draw(im).text((size / 2, size / 2), label, font=font(F_BLACK, int(size * .26)), fill=CREAM, anchor="mm")
    return im

def s3(ta):
    f = G.base(ta)
    t5 = wt(3, "five")
    if ta >= t5 - 0.1:
        el = max(0.0, ta - t5) * 20          # sped-up countdown for the vibe
        rem = max(0, 300 - el)
        t_ = timer(300, rem / 300, f"{int(rem // 60)}:{int(rem % 60):02d}")
        paste_alpha(f, t_, (W / 2 - 150, 300), k_at(ta, t5 - 0.1, 0.25))
    G.stamp(f, ta, wt(3, "Future"), "FUTURE YOU: THANKS", (540, 660), size=48, bg=TEAL_L, rot=3)
    G.put_cyto(f, 480, (540, 1080), ta, G.mouth(ta), "rest")
    G.put_caption(f, ta, 1410)
    return f

def s4(ta):
    f = G.base(ta)
    G.sources_card(f, ta, E["cuts"][4] + 0.1, ["Johansson et al., JAMA Netw Open 2023", "Zhang et al., WIREs Cogn Sci 2019"])
    G.outro(f, ta, 4)
    G.put_cyto(f, 460, (540, 1080), ta, G.mouth(ta), G.wave(ta))
    G.put_caption(f, ta, 1420)
    return f

SCENES = [s0, s1, s2, s3, s4]
if __name__ == "__main__":
    FX["shakes"] = [wt(0, "laziness"), wt(2, "stress"), wt(4, "out") + 0.35]
    FX["bursts"] = [(wt(0, "laziness"), (540, 620), GOLD), (wt(2, "3,500") + 1.0, (540, 360), GOLD), (wt(4, "subscribe") + 0.55, (640, 480), GOLD)]
    ev = [("pop", 0.3), ("boom", wt(0, "laziness")), ("zap", wt(1, "picking")), ("ding", wt(2, "3,500") + 1.0), ("pop", wt(2, "stress")),
          ("pop", wt(2, "anxiety")), ("pop", wt(2, "bad")), ("ding", wt(3, "five")), ("pop", wt(3, "Future")),
          ("pop", wt(4, "Like") + 0.35), ("ding", wt(4, "subscribe") + 0.55), ("boom", wt(4, "out") + 0.35)]
    G.run_v3(SCENES, "cyto-ep6-procrastination.mp4", sys.argv[1],
             still_times=[wt(0, "laziness") + 0.3, wt(1, "later"), wt(2, "later"), wt(3, "thanks"), wt(4, "subscribe") + 0.8, wt(4, "out") + 0.3], events=ev)
