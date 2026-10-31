"""Cyto Short renderer: 'Why do you get goosebumps?'
Usage: python3 render.py stills   -> writes check frames
       python3 render.py video    -> renders scenes and joins them
"""
import math, os, subprocess, sys, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
OUT = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/opentype/inter/"
F_BLACK = FD + "InterDisplay-Black.otf"
F_XB = FD + "Inter-ExtraBold.otf"
F_SB = FD + "Inter-SemiBold.otf"
for f in (F_BLACK, F_XB, F_SB):
    if not os.path.exists(f):
        raise SystemExit("missing font " + f)

def font(path, size):
    return ImageFont.truetype(path, size)

# palette
BG_TOP, BG_BOT = (16, 33, 58), (9, 20, 36)
CREAM = (250, 244, 232)
CORAL = (255, 122, 89)
GOLD = (255, 209, 102)
TEAL, TEAL_D, TEAL_L = (63, 193, 176), (24, 128, 118), (140, 226, 214)
INK = (12, 22, 34)

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

def lerp(a, b, t):
    return a + (b - a) * t

# ---------------------------------------------------------------- background
def make_bg():
    bg = Image.new("RGB", (W, H))
    px = bg.load()
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(lerp(BG_TOP[i], BG_BOT[i], t)) for i in range(3))
        for x in range(W):
            px[x, y] = c
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rnd = random.Random(7)
    for _ in range(34):
        r = rnd.randint(30, 120)
        x, y = rnd.randint(-50, W + 50), rnd.randint(-50, H + 50)
        d.ellipse((x - r, y - r, x + r, y + r), outline=(120, 200, 220, 22), width=3)
        d.ellipse((x - r * .3, y - r * .3, x + r * .3, y + r * .3), fill=(120, 200, 220, 12))
    bg = bg.convert("RGBA")
    bg.alpha_composite(lay)
    sk = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sk)
    col = (28, 52, 84, 255)
    x = -20
    rb = random.Random(11)
    while x < W * 2:
        bw = rb.randint(70, 170); bh = rb.randint(120, 520)
        sd.rectangle((x, H * 2 - bh, x + bw, H * 2), fill=col)
        x += bw + rb.randint(4, 18)
    tx = 1760
    sd.polygon([(tx - 30, H * 2), (tx + 30, H * 2), (tx + 9, 2620), (tx - 9, 2620)], fill=col)
    sd.ellipse((tx - 72, 2780, tx + 72, 2850), fill=col)
    sd.rectangle((tx - 44, 2810, tx + 44, 2870), fill=col)
    sd.ellipse((tx - 26, 2640, tx + 26, 2672), fill=col)
    sd.rectangle((tx - 4, 2330, tx + 4, 2640), fill=col)
    sk = sk.resize((W, H), Image.LANCZOS)
    a = sk.getchannel("A").point(lambda v: int(v * 0.75))
    sk.putalpha(a)
    bg.alpha_composite(sk)
    return bg

# ---------------------------------------------------------------- character
SS = 3

@lru_cache(maxsize=None)
def cyto(S, eyes="open", mouth="closed", arms="rest", look=(0, 0), prop=None, costume=None):
    C = int(S * 1.45) * SS
    img = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, r = C / 2, C * 0.50, 0.40 * S * SS
    # shadow
    sh = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - .72 * r, cy + 1.02 * r, cx + .72 * r, cy + 1.16 * r), fill=(0, 0, 0, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(SS * 6)))
    d = ImageDraw.Draw(img)
    if costume == "raccoon":
        GR, GD = (128, 128, 138), (52, 52, 60)
        for i in range(14):
            u = i / 13
            tx_ = cx + r * (0.55 + 0.75 * u)
            ty_ = cy + r * (0.75 - 1.15 * u * u)
            tr_ = r * (0.20 + 0.06 * math.sin(u * math.pi))
            d.ellipse((tx_ - tr_, ty_ - tr_, tx_ + tr_, ty_ + tr_), fill=GD if (i // 2) % 2 else GR)
        d.ellipse((tx_ - tr_, ty_ - tr_, tx_ + tr_, ty_ + tr_), fill=GD)
    aw = 0.085 * S * SS
    hr = 0.07 * S * SS

    def limb(pts):
        d.line(pts, fill=TEAL_D, width=int(aw), joint="curve")
        for p in pts:
            d.ellipse((p[0] - aw / 2, p[1] - aw / 2, p[0] + aw / 2, p[1] + aw / 2), fill=TEAL_D)
        hx, hy = pts[-1]
        d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=TEAL, outline=TEAL_D, width=int(SS * 3))

    L = (cx - r * .86, cy + r * .10)
    R = (cx + r * .86, cy + r * .10)
    poses = {
        "rest": ([L, (cx - r * 1.12, cy + r * .45), (cx - r * 1.10, cy + r * .78)],
                 [R, (cx + r * 1.12, cy + r * .45), (cx + r * 1.10, cy + r * .78)]),
        "point": ([L, (cx - r * 1.12, cy + r * .45), (cx - r * 1.10, cy + r * .78)],
                  [R, (cx + r * 1.20, cy - r * .15), (cx + r * 1.42, cy - r * .70)]),
        "wave1": ([L, (cx - r * 1.12, cy + r * .45), (cx - r * 1.10, cy + r * .78)],
                  [R, (cx + r * 1.22, cy - r * .05), (cx + r * 1.22, cy - r * .80)]),
        "wave2": ([L, (cx - r * 1.12, cy + r * .45), (cx - r * 1.10, cy + r * .78)],
                  [R, (cx + r * 1.22, cy - r * .05), (cx + r * 1.55, cy - r * .58)]),
        "shrug": ([L, (cx - r * 1.25, cy + r * .40), (cx - r * 1.42, cy - r * .22)],
                  [R, (cx + r * 1.25, cy + r * .40), (cx + r * 1.42, cy - r * .22)]),
    }
    la, ra = poses[arms]
    limb(la); limb(ra)
    # body: membrane, cytoplasm, highlight
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=TEAL_D)
    m = r * 0.92
    d.ellipse((cx - m, cy - m, cx + m, cy + m), fill=TEAL)
    hl = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse((cx - m * .90, cy - m * .30, cx - m * .50, cy + m * .35), fill=TEAL_L + (110,))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(SS * 14)))
    d = ImageDraw.Draw(img)
    # nucleus + nucleolus (top right)
    nx, ny, nr = cx + r * .50, cy + r * .50, r * .17
    d.ellipse((nx - nr, ny - nr, nx + nr, ny + nr), fill=(122, 92, 199), outline=(88, 62, 160), width=int(SS * 4))
    d.ellipse((nx + nr * .05, ny - nr * .45, nx + nr * .45, ny - nr * .05), fill=(196, 176, 255))
    # mitochondrion (bottom left)
    mx, my = cx - r * .50, cy + r * .56
    d.rounded_rectangle((mx - r * .19, my - r * .085, mx + r * .19, my + r * .085), radius=r * .085,
                        fill=(255, 159, 90), outline=(217, 106, 43), width=int(SS * 3))
    zz = [(mx - r * .13 + i * r * .052, my + (r * .04 if i % 2 else -r * .04)) for i in range(6)]
    d.line(zz, fill=(217, 106, 43), width=int(SS * 3), joint="curve")
    if costume == "raccoon":
        for sx in (-1, 1):
            ex0 = cx + sx * r * .62
            d.polygon([(ex0 - r * .26, cy - r * .95), (ex0 + r * .26, cy - r * .95), (ex0 + sx * r * .10, cy - r * 1.42)], fill=(128, 128, 138))
            d.polygon([(ex0 - r * .14, cy - r * .98), (ex0 + r * .14, cy - r * .98), (ex0 + sx * r * .07, cy - r * 1.28)], fill=(52, 52, 60))
    # toque: dome, folded cuff with stripe, pom-pom
    TQ, TQ_D, TW = (30, 86, 172), (20, 58, 124), (246, 246, 240)
    d.ellipse((cx - r * .97, cy - r * 1.24, cx + r * .97, cy - r * .30), fill=TQ)
    for k in range(-4, 5):
        x0 = cx + k * r * .2
        d.line((x0, cy - r * 1.05 + abs(k) * r * .04, x0, cy - r * .50), fill=(24, 72, 150), width=int(SS * 2))
    d.rounded_rectangle((cx - r * 1.03, cy - r * .54, cx + r * 1.03, cy - r * .24), radius=r * .12, fill=TQ_D)
    d.rectangle((cx - r * 1.01, cy - r * .43, cx + r * 1.01, cy - r * .35), fill=TW)
    for k in range(-9, 10):
        x0 = cx + k * r * .105
        d.line((x0, cy - r * .52, x0, cy - r * .44), fill=(12, 40, 92), width=int(SS * 2))
        d.line((x0, cy - r * .34, x0, cy - r * .26), fill=(12, 40, 92), width=int(SS * 2))
    pr = r * .18
    d.ellipse((cx - pr, cy - r * 1.27 - pr, cx + pr, cy - r * 1.27 + pr), fill=TW, outline=(214, 214, 206), width=int(SS * 2))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        qx, qy = cx + math.cos(a) * pr * .55, cy - r * 1.27 + math.sin(a) * pr * .55
        d.ellipse((qx - pr * .12, qy - pr * .12, qx + pr * .12, qy + pr * .12), fill=(226, 226, 218))
    # cheeks
    ck = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    cd = ImageDraw.Draw(ck)
    for sx in (-.50, .48):
        cd.ellipse((cx + r * sx - r * .10, cy + r * .20 - r * .06, cx + r * sx + r * .10, cy + r * .20 + r * .06),
                   fill=(255, 128, 120, 120))
    img.alpha_composite(ck.filter(ImageFilter.GaussianBlur(SS * 3)))
    d = ImageDraw.Draw(img)
    if costume == "raccoon":
        MK = (46, 46, 54)
        d.rounded_rectangle((cx - r * .50, cy - r * .16, cx + r * .44, cy + r * .13), radius=r * .14, fill=MK)
        d.polygon([(cx - r * .50, cy - r * .10), (cx - r * .70, cy + r * .02), (cx - r * .50, cy + r * .10)], fill=MK)
        d.polygon([(cx + r * .44, cy - r * .10), (cx + r * .64, cy + r * .02), (cx + r * .44, cy + r * .10)], fill=MK)
    # eyes
    lw = int(SS * 6)
    for ex in (cx - r * .26, cx + r * .20):
        ey = cy + r * .00
        if eyes == "closed":
            d.arc((ex - r * .12, ey - r * .08, ex + r * .12, ey + r * .10), 20, 160, fill=INK, width=lw)
        elif eyes == "happy":
            d.arc((ex - r * .12, ey - r * .05, ex + r * .12, ey + r * .16), 200, 340, fill=INK, width=lw)
        else:
            d.ellipse((ex - r * .13, ey - r * .16, ex + r * .13, ey + r * .16), fill=(255, 255, 255), outline=INK, width=int(SS * 3))
            px_, py_ = ex + look[0] * r * .04, ey + look[1] * r * .05
            d.ellipse((px_ - r * .075, py_ - r * .085, px_ + r * .075, py_ + r * .085), fill=INK)
            d.ellipse((px_ + r * .01, py_ - r * .065, px_ + r * .045, py_ - r * .03), fill=(255, 255, 255))
            # chill half-lid
            d.chord((ex - r * .14, ey - r * .17, ex + r * .14, ey + r * .17), 195, 345, fill=TEAL)
            d.line((ex - r * .125, ey - r * .085, ex + r * .125, ey - r * .085), fill=INK, width=lw)
    # mouth
    mx, my = cx - r * .03, cy + r * .30
    dark, tongue = (70, 18, 34), (255, 120, 120)
    if mouth == "closed":
        d.arc((mx - r * .12, my - r * .10, mx + r * .12, my + r * .06), 25, 155, fill=INK, width=lw)
    elif mouth == "mid":
        d.ellipse((mx - r * .08, my - r * .045, mx + r * .08, my + r * .055), fill=dark)
    elif mouth == "open":
        d.ellipse((mx - r * .10, my - r * .08, mx + r * .10, my + r * .10), fill=dark)
        d.chord((mx - r * .07, my + r * .00, mx + r * .07, my + r * .11), 180, 360, fill=tongue)
    elif mouth == "smile":
        d.chord((mx - r * .16, my - r * .13, mx + r * .16, my + r * .13), 0, 180, fill=dark)
        d.chord((mx - r * .09, my + r * .03, mx + r * .09, my + r * .15), 180, 360, fill=tongue)
    if costume == "jersey":
        JB, JW, JD = (24, 70, 160), (246, 246, 240), (14, 44, 110)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        top_y = cy + r * .50
        ld.rectangle((cx - r * 1.1, top_y, cx + r * 1.1, cy + r * 1.1), fill=JB)
        ld.rectangle((cx - r * 1.1, cy + r * .80, cx + r * 1.1, cy + r * .86), fill=JW)
        ld.rectangle((cx - r * 1.1, cy + r * .90, cx + r * 1.1, cy + r * .94), fill=JW)
        ld.polygon([(cx - r * .20, top_y - 1), (cx + r * .20, top_y - 1), (cx, top_y + r * .12)], fill=JW)
        jf = ImageFont.truetype(F_BLACK, int(r * .20))
        ld.text((cx, cy + r * .69), "6IX", font=jf, fill=JW, anchor="mm", stroke_width=int(SS * 2), stroke_fill=JD)
        m = Image.new("L", img.size, 0); ImageDraw.Draw(m).ellipse((cx - r + SS * 2, cy - r + SS * 2, cx + r - SS * 2, cy + r - SS * 2), fill=255)
        clip = Image.new("RGBA", img.size, (0, 0, 0, 0)); clip.paste(lay, (0, 0), m)
        img.alpha_composite(clip)
        d = ImageDraw.Draw(img)
        d.arc((cx - r, cy - r, cx + r, cy + r), 15, 165, fill=TEAL_D, width=int(SS * 5))
    if costume == "jersey":
        JB, JW, JD = (24, 70, 160), (246, 246, 240), (14, 44, 110)
        # jersey covers lower 55% of the body: clip with the body circle
        jm = Image.new("L", (C, C), 0); jd = ImageDraw.Draw(jm)
        jd.ellipse((cx - r * .99, cy - r * .99, cx + r * .99, cy + r * .99), fill=255)
        cut = Image.new("L", (C, C), 0); ImageDraw.Draw(cut).rectangle((0, cy + r * .50, C, C), fill=255)
        from PIL import ImageChops
        jm = ImageChops.multiply(jm, cut)
        lay = Image.new("RGBA", (C, C), JB + (255,)); ld = ImageDraw.Draw(lay)
        ld.rectangle((0, cy + r * .64, C, cy + r * .70), fill=JW)
        ld.rectangle((0, cy + r * .75, C, cy + r * .80), fill=JW)
        img.paste(lay, (0, 0), jm)
        d = ImageDraw.Draw(img)
        d.polygon([(cx - r * .22, cy + r * .50), (cx + r * .22, cy + r * .50), (cx, cy + r * .62)], fill=JW)        # V collar
        nf = ImageFont.truetype(F_BLACK, int(r * .22))
        d.text((cx + r * .02, cy + r * .89), "6IX", font=nf, fill=JW, anchor="mm", stroke_width=int(SS * 3), stroke_fill=JD)
    if costume == "scarf":
        SC, SC2 = (214, 40, 52), (246, 246, 240)
        d.rounded_rectangle((cx - r * .98, cy + r * .44, cx + r * .98, cy + r * .70), radius=r * .12, fill=SC)
        for k in range(-4, 5):
            x0 = cx + k * r * .22
            d.line((x0, cy + r * .46, x0 - r * .06, cy + r * .68), fill=SC2, width=int(SS * 5))
        d.polygon([(cx + r * .30, cy + r * .62), (cx + r * .62, cy + r * .62), (cx + r * .66, cy + r * 1.22), (cx + r * .36, cy + r * 1.20)], fill=SC)
        for yy in (0.82, 1.0):
            d.line((cx + r * .33, cy + r * yy, cx + r * .65, cy + r * yy), fill=SC2, width=int(SS * 6))
        for i in range(5):
            fx_ = cx + r * (.38 + i * .065)
            d.line((fx_, cy + r * 1.21, fx_, cy + r * 1.32), fill=SC, width=int(SS * 4))
    if costume == "streetcar":
        RD, RDD, WH = (220, 38, 32), (160, 22, 22), (246, 246, 240)
        bx0, bx1, by0, by1 = cx - r * 1.18, cx + r * 1.18, cy + r * .46, cy + r * 1.06
        # trolley pole from the back of the box up past the head
        d.line((cx - r * .95, by0 + r * .05, cx - r * 1.55, cy - r * 1.20), fill=(40, 40, 46), width=int(SS * 5))
        d.ellipse((cx - r * 1.61, cy - r * 1.26, cx - r * 1.49, cy - r * 1.14), fill=(40, 40, 46))
        for sx in (-1, 1):  # suspender straps
            d.line((cx + sx * r * .55, by0 + r * .02, cx + sx * r * .72, cy - r * .18), fill=WH, width=int(SS * 7))
        d.rounded_rectangle((bx0, by0, bx1, by1), radius=r * .14, fill=RD, outline=RDD, width=int(SS * 4))
        d.rectangle((bx0 + r * .02, by0 + r * .36, bx1 - r * .02, by0 + r * .42), fill=WH)
        for i in range(5):
            wx = bx0 + r * .16 + i * r * .42
            d.rounded_rectangle((wx, by0 + r * .08, wx + r * .30, by0 + r * .30), radius=r * .04, fill=(34, 54, 78), outline=WH, width=int(SS * 2))
        for wx in (bx0 + r * .40, bx1 - r * .40):
            d.ellipse((wx - r * .12, by1 - r * .10, wx + r * .12, by1 + r * .14), fill=(30, 30, 34))
        sf = ImageFont.truetype(F_XB, int(r * .10))
        d.rounded_rectangle((cx - r * .34, by0 - r * .17, cx + r * .34, by0 + r * .01), radius=r * .03, fill=(20, 20, 24))
        d.text((cx, by0 - r * .08), "SPOOKY ST", font=sf, fill=(255, 196, 60), anchor="mm")
        for pts in (la, ra):
            hx_, hy_ = pts[-1]
            d.ellipse((hx_ - hr, hy_ - hr, hx_ + hr, hy_ + hr), fill=TEAL, outline=TEAL_D, width=int(SS * 3))
    if prop in ("coffee", "mystery"):
        hx, hy = la[-1]
        cw, cb, ch = r * .30, r * .23, r * .40
        top, bot = hy - ch * .75, hy + ch * .25
        d.polygon([(hx - cw / 2, top), (hx + cw / 2, top), (hx + cb / 2, bot), (hx - cb / 2, bot)], fill=(214, 52, 58))
        d.polygon([(hx - cw * .47, top + ch * .30), (hx + cw * .47, top + ch * .30), (hx + cw * .43, top + ch * .62), (hx - cw * .43, top + ch * .62)], fill=(176, 112, 70))
        d.rounded_rectangle((hx - cw * .58, top - r * .06, hx + cw * .58, top + r * .03), radius=r * .03, fill=(92, 58, 40))
        st = Image.new("RGBA", (C, C), (0, 0, 0, 0))
        sdd = ImageDraw.Draw(st)
        for i in (-1, 1):
            sdd.arc((hx + i * r * .05 - r * .05, top - r * .32, hx + i * r * .05 + r * .05, top - r * .10), 100, 260, fill=(255, 255, 255, 150), width=int(SS * 3))
        img.alpha_composite(st.filter(ImageFilter.GaussianBlur(SS * 1.5)))
        d = ImageDraw.Draw(img)
        if prop == "mystery":
            # censor: pixelate + blur the whole cup, steam and all
            bx0, by0 = int(hx - cw * 1.05), int(top - r * .42)
            bx1, by1 = int(hx + cw * 1.05), int(bot + r * .08)
            reg = img.crop((bx0, by0, bx1, by1))
            bs = max(1, int(r * .075))
            pix = reg.resize((max(1, (bx1 - bx0) // bs), max(1, (by1 - by0) // bs)), Image.BILINEAR).resize(reg.size, Image.NEAREST)
            pix = pix.filter(ImageFilter.GaussianBlur(SS * 1.2))
            base_ = Image.new("RGBA", reg.size, (90, 120, 140, 255))
            base_.alpha_composite(pix)
            m = Image.new("L", reg.size, 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.size[0] - 1, reg.size[1] - 1), radius=int(r * .08), fill=255)
            img.paste(base_, (bx0, by0), m)
            d = ImageDraw.Draw(img)
        d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=TEAL, outline=TEAL_D, width=int(SS * 3))
    return img.resize((C // SS, C // SS), Image.LANCZOS)

def paste_cyto(frame, S, center, t, eyes="open", mouth="closed", arms="rest", look=(0, 0), prop="mystery"):
    blink = (t % 3.7) < 0.12
    e = "closed" if (blink and eyes == "open") else eyes
    spr = cyto(S, e, mouth, arms, look, None if arms == "shrug" else prop)
    bob = math.sin(t * 2 * math.pi * 0.8)
    sq = 1 + 0.018 * bob
    w, h = spr.size
    spr2 = spr.resize((int(w / sq), int(h * sq)), Image.BILINEAR)
    x = int(center[0] - spr2.width / 2)
    y = int(center[1] - spr2.height / 2 - bob * 8 - (h * sq - h) * 0.5)
    frame.alpha_composite(spr2, (x, y))

MOUTH_PATTERN = ["mid", "open", "mid", "closed", "open", "open", "mid", "closed", "mid", "open"]
def talk_mouth(t, speaking, idle="closed"):
    if not speaking:
        return idle
    return MOUTH_PATTERN[int(t * FPS) // 3 % len(MOUTH_PATTERN)]

# ---------------------------------------------------------------- text bits
def rich_lines(text, fnt, maxw):
    words = text.split(" ")
    lines, cur = [], []
    sp = fnt.getlength(" ")
    for wd in words:
        trial = cur + [wd]
        width = sum(fnt.getlength(x.strip("*")) for x in trial) + sp * (len(trial) - 1)
        if width > maxw and cur:
            lines.append(cur); cur = [wd]
        else:
            cur = trial
    if cur: lines.append(cur)
    return lines

@lru_cache(maxsize=None)
def caption_img(text, size=66, maxw=960):
    fnt = font(F_BLACK, size)
    lines = rich_lines(text, fnt, maxw)
    sp = fnt.getlength(" ")
    maxw = int(max([maxw] + [sum(fnt.getlength(x.strip("*")) for x in ln) + sp * (len(ln) - 1) for ln in lines]) + 20)
    lh = int(size * 1.18)
    pad = 20
    img = Image.new("RGBA", (maxw + pad * 2, lh * len(lines) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        lw = sum(fnt.getlength(x.strip("*")) for x in ln) + sp * (len(ln) - 1)
        x = (img.width - lw) / 2
        y = pad + i * lh
        for wd in ln:
            hi = wd.startswith("*")
            clean = wd.strip("*")
            d.text((x, y), clean, font=fnt, fill=GOLD if hi else CREAM, stroke_width=9, stroke_fill=INK)
            x += fnt.getlength(clean) + sp
    return img

def paste_caption(frame, caps, t, cy):
    for (a, b, txt) in caps:
        if a <= t < b:
            img = caption_img(txt)
            k = ease((t - a) / 0.18)
            s = 0.86 + 0.14 * k
            im = img.resize((int(img.width * s), int(img.height * s)), Image.BILINEAR) if k < 1 else img
            if k < 1:
                al = im.getchannel("A").point(lambda v: int(v * k))
                im.putalpha(al)
            frame.alpha_composite(im, (int(W / 2 - im.width / 2), int(cy - im.height / 2)))

def speaking(caps, t):
    return any(a + 0.05 <= t < b - 0.25 for a, b, _ in caps)

@lru_cache(maxsize=None)
def pill(text, size=30, fg=INK, bg=GOLD, padx=22, pady=12, fnt_path=F_XB):
    fnt = font(fnt_path, size)
    tw = fnt.getlength(text)
    bb = fnt.getbbox(text)
    th = bb[3] - bb[1]
    w, h = int(tw + padx * 2), int(th + pady * 2)
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=h * SS // 2, fill=bg)
    img = img.resize((w, h), Image.LANCZOS)
    ImageDraw.Draw(img).text((padx, pady - bb[1]), text, font=fnt, fill=fg)
    return img

def paste_alpha(frame, im, xy, a=1.0):
    if a <= 0: return
    if a < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(im, (int(xy[0]), int(xy[1])))

@lru_cache(maxsize=None)
def term_card(title, body, w=560, h=250):
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=28 * SS, fill=(250, 244, 232, 250))
    d.rounded_rectangle((0, 0, 14 * SS, h * SS - 1), radius=7 * SS, fill=CORAL)
    img = img.resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    tf = font(F_XB, 30)
    bf = font(F_SB, 34)
    d.text((40, 30), title, font=tf, fill=CORAL)
    lines = rich_lines(body, bf, w - 70)
    for i, ln in enumerate(lines):
        d.text((40, 82 + i * 46), " ".join(x.strip("*") for x in ln), font=bf, fill=INK)
    return img

# ---------------------------------------------------------------- skin diagram
PW, PH = 940, 680
PANEL_XY = (70, 250)
DS = 2
SKIN_Y = 0.36 * PH
HAIR_X = 0.46 * PW

def surf_y(x, lift):
    y = SKIN_Y
    for hx, amp in ((HAIR_X, 1.0), (0.17 * PW, 0.7), (0.78 * PW, 0.7)):
        y -= 40 * lift * amp * math.exp(-((x - (hx + 18)) / 38) ** 2)
    return y

def draw_skin(lift=0.0, pulse=0.0, impulse=None, fur=0.0, warm=0.0, label_alpha=None):
    s = DS
    img = Image.new("RGBA", (PW * s, PH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, PW * s - 1, PH * s - 1), radius=34 * s, fill=(10, 22, 38), outline=(52, 86, 112), width=3 * s)
    # warm air glow (fur scene)
    if warm > 0:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((40 * s, (SKIN_Y - 260) * s, (PW - 40) * s, (SKIN_Y + 30) * s), fill=(255, 150, 60, int(110 * warm)))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(40 * s)))
        d = ImageDraw.Draw(img)
    # skin layers (clipped to the panel by a mask at the end)
    xs = list(range(0, PW + 1, 6))
    top = [(x * s, surf_y(x, lift) * s) for x in xs]
    epi_b = SKIN_Y + 64
    hypo_t = PH - 120
    d.polygon(top + [(PW * s, PH * s), (0, PH * s)], fill=(232, 150, 128))
    d.polygon(top + [(PW * s, epi_b * s), (0, epi_b * s)], fill=(246, 198, 172))
    d.line(top, fill=(255, 222, 200), width=4 * s)
    d.rectangle((0, hypo_t * s, PW * s, PH * s), fill=(244, 212, 150))
    rnd = random.Random(3)
    for i in range(16):
        fx = 30 + i * 60 + rnd.randint(-8, 8)
        fy = hypo_t + 55 + rnd.randint(-10, 10)
        fr = rnd.randint(26, 34)
        d.ellipse(((fx - fr) * s, (fy - fr) * s, (fx + fr) * s, (fy + fr) * s), fill=(250, 226, 160), outline=(214, 172, 92), width=3 * s)
    # follicles + hairs
    def follicle(hx, scale=1.0, main=False):
        sy = surf_y(hx, lift)
        depth = 250 * scale
        rx, ry = hx - 70 * scale, sy + depth
        d.line(((hx * s, sy * s), (rx * s, ry * s)), fill=(196, 112, 96), width=int(34 * scale * s))
        d.line(((hx * s, sy * s), (rx * s, ry * s)), fill=(70, 46, 36), width=int(9 * scale * s))
        br = 24 * scale
        d.ellipse(((rx - br) * s, (ry - br) * s, (rx + br) * s, (ry + br) * s), fill=(150, 80, 66))
        # arrector pili muscle: from 60% down the follicle to under the epidermis on the right
        fx, fy = lerp(hx, rx, .62), lerp(sy, ry, .62)
        ex, ey = hx + 120 * scale, epi_b + 6
        mw = (24 + 12 * lift) * scale
        if main and pulse > 0:
            d.line(((fx * s, fy * s), (ex * s, ey * s)), fill=(255, 220, 120), width=int((mw + 18 * pulse) * s))
        d.line(((fx * s, fy * s), (ex * s, ey * s)), fill=(205, 62, 72), width=int(mw * s))
        for k in range(1, 5):
            px, py = lerp(fx, ex, k / 5), lerp(fy, ey, k / 5)
            d.line(((px - 6 * scale) * s, (py - 9 * scale) * s, (px + 6 * scale) * s, (py + 9 * scale) * s), fill=(160, 38, 52), width=2 * s)
        # hair shaft above the surface
        ang = math.radians(lerp(64, 10, lift))
        Lh = 190 * scale
        d.line(((hx * s, sy * s), ((hx + math.sin(ang) * Lh) * s, (sy - math.cos(ang) * Lh) * s)), fill=(58, 40, 30), width=int(8 * scale * s))
        return (fx, fy, ex, ey)

    follicle(0.17 * PW, 0.8)
    follicle(0.78 * PW, 0.8)
    main = follicle(HAIR_X, 1.0, main=True)
    if fur > 0:
        for i in range(14):
            hx = 40 + i * 64
            if abs(hx - HAIR_X) < 40 or abs(hx - 0.17 * PW) < 40 or abs(hx - 0.78 * PW) < 40:
                continue
            sy = surf_y(hx, lift)
            ang = math.radians(lerp(64, 12, lift) + (i % 3 - 1) * 4)
            Lh = 230 * fur
            d.line(((hx * s, sy * s), ((hx + math.sin(ang) * Lh) * s, (sy - math.cos(ang) * Lh) * s)), fill=(58, 40, 30), width=7 * s)
    # sympathetic nerve to the main muscle
    if impulse is not None:
        fx, fy, ex, ey = main
        mx, my = lerp(fx, ex, .5), lerp(fy, ey, .5)
        p0, p1, p2 = (PW - 30, PH - 150), (PW - 160, mx and my + 40), (mx + 6, my + 6)
        p1 = (PW - 170, my + 60)
        pts = []
        for i in range(41):
            u = i / 40
            pts.append(((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
                        (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]))
        d.line([(x * s, y * s) for x, y in pts], fill=(255, 209, 102), width=7 * s, joint="curve")
        for off in (0.0, 0.33, 0.66):
            u = (impulse + off) % 1.0
            x, y = pts[int(u * 40)]
            gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).ellipse(((x - 22) * s, (y - 22) * s, (x + 22) * s, (y + 22) * s), fill=(255, 240, 170, 200))
            img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(8 * s)))
            d = ImageDraw.Draw(img)
            d.ellipse(((x - 9) * s, (y - 9) * s, (x + 9) * s, (y + 9) * s), fill=(255, 255, 230))
    # clip to rounded panel
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((3 * s, 3 * s, PW * s - 4, PH * s - 4), radius=32 * s, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, PW * s - 1, PH * s - 1), radius=34 * s, outline=(52, 86, 112), width=3 * s)
    out = out.resize((PW, PH), Image.LANCZOS)
    return out, main

def label(frame, text, at, anchor_pt, a, side="left"):
    """Pill label with a leader line to anchor_pt (frame coords)."""
    if a <= 0: return
    p = pill(text, 30, INK, CREAM)
    lx, ly = at
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).line((lx + (p.width if side == "left" else 0), ly + p.height / 2, anchor_pt[0], anchor_pt[1]), fill=CREAM + (int(230 * a),), width=4)
    ImageDraw.Draw(lay).ellipse((anchor_pt[0] - 8, anchor_pt[1] - 8, anchor_pt[0] + 8, anchor_pt[1] + 8), fill=CREAM + (int(255 * a),))
    frame.alpha_composite(lay)
    paste_alpha(frame, p, (lx, ly), a)

# ---------------------------------------------------------------- music notes
@lru_cache(maxsize=None)
def note(size=90, color=GOLD):
    img = Image.new("RGBA", (size * SS, int(size * 1.3) * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    u = size * SS
    d.ellipse((0, u * .85, u * .42, u * 1.18), fill=color)
    d.rectangle((u * .34, u * .15, u * .42, u * 1.02), fill=color)
    d.polygon([(u * .38, u * .15), (u * .80, u * .30), (u * .80, u * .48), (u * .38, u * .34)], fill=color)
    return img.resize((size, int(size * 1.3)), Image.LANCZOS)

# ---------------------------------------------------------------- scenes
BG = None
def base():
    f = BG.copy()
    paste_alpha(f, pill("THE BODY IS THE 6IX", 28, INK, GOLD), (W / 2 - pill("THE BODY IS THE 6IX", 28, INK, GOLD).width / 2, 120))
    return f

HOST_C = (540, 980)
SMALL_C = (250, 1380)
CARD_XY = (450, 1250)
DIAG_CAP_Y = 1060
HOST_CAP_Y = 1390

def host_scene(caps, arms_fn, idle="smile", props=None, eyes="open"):
    def fr(t):
        f = base()
        if props: props(f, t)
        paste_cyto(f, 560, HOST_C, t, eyes, talk_mouth(t, speaking(caps, t), idle), arms_fn(t))
        paste_caption(f, caps, t, HOST_CAP_Y)
        return f
    return fr

def diagram_scene(caps, skin_fn, card=None, labels=None, enter=False):
    def fr(t):
        f = base()
        params = skin_fn(t)
        panel, main = draw_skin(**params)
        dy = 0
        a = 1.0
        if enter:
            k = ease(t / 0.45); dy = (1 - k) * 70; a = k
        paste_alpha(f, panel, (PANEL_XY[0], PANEL_XY[1] + dy), a)
        if labels: labels(f, t, main)
        if card:
            k = ease((t - 0.25) / 0.35)
            c = term_card(*card)
            paste_alpha(f, c, (CARD_XY[0] + (1 - k) * 120, CARD_XY[1]), k)
        paste_cyto(f, 330, SMALL_C, t, "open", talk_mouth(t, speaking(caps, t)), "point", (1, -1))
        paste_caption(f, caps, t, DIAG_CAP_Y)
        return f
    return fr

def to_frame(pt):
    return (PANEL_XY[0] + pt[0], PANEL_XY[1] + pt[1])

def wave(t):
    return "wave1" if int(t * FPS / 7) % 2 == 0 else "wave2"

# S1 hook
S1_CAPS = [(0.2, 3.4, "Yo, why does your skin get *goosebumps?*")]
def s1_props(f, t):
    big = caption_img("GOOSEBUMPS?", size=128, maxw=1000)
    k = ease((t - 0.1) / 0.35)
    wob = math.sin(t * 9) * 4 if t > 0.5 else 0
    im = big.resize((int(big.width * (0.7 + 0.3 * k)), int(big.height * (0.7 + 0.3 * k))), Image.BILINEAR)
    paste_alpha(f, im, (W / 2 - im.width / 2, 430 - im.height / 2 + wob), k)
s1 = host_scene(S1_CAPS, wave, props=s1_props)

# S2 meet the muscle
S2_CAPS = [(0.1, 4.2, "Every hair's got its own *tiny* *muscle:* the *arrector* *pili.*")]
def s2_skin(t):
    return dict(lift=0.0, pulse=max(0, math.sin((t - 1.8) * 5)) if t > 1.8 else 0.0)
def s2_labels(f, t, main):
    fx, fy, ex, ey = main
    mid = to_frame((lerp(fx, ex, .55), lerp(fy, ey, .55)))
    label(f, "arrector pili muscle", (PANEL_XY[0] + 560, PANEL_XY[1] + 560), mid, ease((t - 1.9) / 0.3), side="right")
    hair_pt = to_frame((HAIR_X + 85, SKIN_Y - 42))
    label(f, "hair", (PANEL_XY[0] + 620, PANEL_XY[1] + 60), hair_pt, ease((t - 0.5) / 0.3), side="right")
s2 = diagram_scene(S2_CAPS, s2_skin, ("ARRECTOR PILI", "Latin for “raiser of the hair.”"), s2_labels, enter=True)

# S3 the nerve fires
S3_CAPS = [(0.1, 3.6, "When you're *cold* or *shook,* your *fight-or-flight* nerves fire...")]
def s3_skin(t):
    return dict(lift=0.0, impulse=(t * 0.8) % 1.0 if t > 0.8 else None, pulse=0.6 if t > 2.8 else 0.0)
def s3_labels(f, t, main):
    label(f, "sympathetic nerve", (PANEL_XY[0] + 30, PANEL_XY[1] + 590), to_frame((PW - 120, PH - 150)), ease((t - 0.9) / 0.3))
s3 = diagram_scene(S3_CAPS, s3_skin, ("FIGHT-OR-FLIGHT", "Your sympathetic nervous system. Runs on autopilot."), s3_labels)

# S4 hair stands up, bump forms
S4_CAPS = [(0.05, 2.2, "...the muscle *squeezes,* the hair *stands* *up,*"),
           (2.2, 4.4, "and the skin forms a *bump.*")]
def s4_skin(t):
    return dict(lift=ease((t - 0.2) / 1.4), pulse=0.4 if 0.2 < t < 1.6 else 0.0, impulse=(t * 0.8) % 1.0 if t < 1.6 else None)
def s4_labels(f, t, main):
    label(f, "goosebump!", (PANEL_XY[0] + 30, PANEL_XY[1] + 40), to_frame((HAIR_X + 30, SKIN_Y - 36)), ease((t - 2.3) / 0.3))
s4 = diagram_scene(S4_CAPS, s4_skin, ("PILOERECTION", "The science word for goosebumps."), s4_labels)

# S5 the fur story
S5_CAPS = [(0.05, 2.9, "When our ancestors were *bare* *furry,* that trapped *warm* *air*"),
           (2.9, 5.0, "and made them look *bigger.*")]
def s5_skin(t):
    return dict(lift=1.0, fur=ease(t / 0.6), warm=ease((t - 0.8) / 0.8))
def s5_labels(f, t, main):
    label(f, "trapped warm air", (PANEL_XY[0] + 40, PANEL_XY[1] + 40), to_frame((PW * 0.62, SKIN_Y - 120)), ease((t - 1.1) / 0.3))
s5 = diagram_scene(S5_CAPS, s5_skin, ("INSULATION", "Fluffed fur holds a layer of warm air."), s5_labels)

# S6 leftover reflex + music chills
S6_CAPS = [(0.05, 3.0, "We lost the fur, so now it's a *leftover* *reflex.*"),
           (3.0, 6.0, "Styll goes off when a *song* *hits* though.")]
def s6_props(f, t):
    k = ease((t - 0.6) / 0.35) * (1 - ease((t - 2.8) / 0.25))
    c = term_card("VESTIGIAL", "A trait that has lost most of its original job.", 620, 220)
    paste_alpha(f, c, (W / 2 - c.width / 2, 330 + (1 - k) * 40), k)
    if t > 3.0:
        tt = t - 3.0
        for (x0, ph, sz, col) in [(170, 0.0, 90, GOLD), (860, 0.4, 110, CORAL), (300, 0.75, 70, TEAL_L), (760, 1.1, 80, GOLD)]:
            u = ((tt * 0.32 + ph) % 1.0)
            y = 820 - u * 520
            x = x0 + math.sin((tt + ph) * 3) * 25
            paste_alpha(f, note(sz, col), (x, y), min(1, u * 4, tt * 3) * (1 - max(0, u - 0.75) * 4))
s6 = host_scene(S6_CAPS, lambda t: "shrug" if 0.8 < t < 3.0 else "rest", idle="smile", props=s6_props)

# S7 outro
S7_CAPS = [(0.1, 3.0, "Follow for more, *ahlie.*")]
def s7_props(f, t):
    k = ease((t - 0.2) / 0.35)
    p = pill("CYTO · FROM THE 6IX", 34, INK, CREAM)
    paste_alpha(f, p, (W / 2 - p.width / 2, 560 + (1 - k) * 30), k)
s7 = host_scene(S7_CAPS, wave, idle="smile", props=s7_props)

SCENES = [("s1", s1, 3.4), ("s2", s2, 4.2), ("s3", s3, 3.6), ("s4", s4, 4.4),
          ("s5", s5, 5.0), ("s6", s6, 6.0), ("s7", s7, 3.0)]

def render_scene(name, fn, dur):
    final = os.path.join(OUT, f"{name}.mp4")
    tmp = os.path.join(OUT, f"{name}.part.mp4")
    n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, final)
    else:
        raise SystemExit(f"ffmpeg failed on {name}")
    return final

if __name__ == "__main__":
    BG = make_bg()
    mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
    if mode == "stills":
        picks = [("s1", s1, 1.8), ("s2", s2, 3.0), ("s4", s4, 3.0), ("s5", s5, 3.5), ("s6", s6, 4.2), ("s7", s7, 1.5)]
        ims = [fn(t).convert("RGB") for _, fn, t in picks]
        sheet = Image.new("RGB", (W * 3 // 2, H * 2 // 2), (0, 0, 0))
        for i, im in enumerate(ims):
            sheet.paste(im.resize((W // 2, H // 2)), ((i % 3) * W // 2, (i // 3) * H // 2))
        sheet.save(os.path.join(OUT, "check_sheet.jpg"), quality=88)
        ims[1].save(os.path.join(OUT, "check_s2.jpg"), quality=90)
        print("ok")
    else:
        files = []
        for name, fn, dur in SCENES:
            files.append(render_scene(name, fn, dur)); print("rendered", name, flush=True)
        lst = os.path.join(OUT, "list.txt")
        with open(lst, "w") as fh:
            fh.writelines(f"file '{f}'\n" for f in files)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                        os.path.join(OUT, "cyto-goosebumps.mp4")], check=True)
        print("done")
