"""Cyto puppet rig: exports separate transparent PNG layers on one shared canvas.
python3 rig.py [outdir]
All full-canvas layers are CANVAS x CANVAS and line up when stacked at (0,0).
Arm/hand/cup layers are drawn at REST pose; animate by rotating around SHOULDER_L / SHOULDER_R.
"""
import math, os, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import TEAL, TEAL_D, TEAL_L, INK, F_BLACK

SS = 2                      # supersample
CANVAS = 1200
cx, cy, r = 600, 640, 300   # body centre / radius (final px)
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/cyto2/rig"
os.makedirs(OUT, exist_ok=True)

SHOULDER_L = (cx - r * .86, cy + r * .10)
ELBOW_L = (cx - r * 1.12, cy + r * .45)
HAND_L = (cx - r * 1.10, cy + r * .78)
SHOULDER_R = (cx + r * .86, cy + r * .10)
ELBOW_R = (cx + r * 1.12, cy + r * .45)
HAND_R = (cx + r * 1.10, cy + r * .78)
MOUTH = (cx - r * .03, cy + r * .30)
AW, HR = 0.085 * 2.5 * r * .4 / .4, None


def layer():
    im = Image.new("RGBA", (CANVAS * SS, CANVAS * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def P(*xy):  # scale coords
    return tuple(v * SS for v in xy)


def save(im, name):
    im.resize((im.width // SS, im.height // SS), Image.LANCZOS).save(os.path.join(OUT, name + ".png"))


aw = 0.085 * (r / .40) * SS * .40 / .40 * .40 / .40  # = .085*S where S=r/.40
aw = 0.085 * (r / 0.40) * SS
hr = 0.07 * (r / 0.40) * SS
lw = int(SS * 6 * 1.0)


# ---------- body (membrane, cytoplasm, organelles, cheeks, toque, shadow) ----------
def body():
    im, d = layer()
    sh, sd = layer()
    sd.ellipse(P(cx - .72 * r, cy + 1.02 * r, cx + .72 * r, cy + 1.16 * r), fill=(0, 0, 0, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(SS * 6)))
    d = ImageDraw.Draw(im)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=TEAL_D)
    m = r * .92
    d.ellipse(P(cx - m, cy - m, cx + m, cy + m), fill=TEAL)
    hl, hd = layer()
    hd.ellipse(P(cx - m * .90, cy - m * .30, cx - m * .50, cy + m * .35), fill=TEAL_L + (110,))
    im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(SS * 14)))
    d = ImageDraw.Draw(im)
    nx, ny, nr = cx + r * .50, cy + r * .50, r * .17
    d.ellipse(P(nx - nr, ny - nr, nx + nr, ny + nr), fill=(122, 92, 199), outline=(88, 62, 160), width=SS * 4)
    d.ellipse(P(nx + nr * .05, ny - nr * .45, nx + nr * .45, ny - nr * .05), fill=(196, 176, 255))
    mx, my = cx - r * .50, cy + r * .56
    d.rounded_rectangle(P(mx - r * .19, my - r * .085, mx + r * .19, my + r * .085), radius=r * .085 * SS,
                        fill=(255, 159, 90), outline=(217, 106, 43), width=SS * 3)
    zz = [P(mx - r * .13 + i * r * .052, my + (r * .04 if i % 2 else -r * .04)) for i in range(6)]
    d.line(zz, fill=(217, 106, 43), width=SS * 3, joint="curve")
    ck, cd = layer()
    for sx in (-.50, .48):
        cd.ellipse(P(cx + r * sx - r * .10, cy + r * .14, cx + r * sx + r * .10, cy + r * .26), fill=(255, 128, 120, 120))
    im.alpha_composite(ck.filter(ImageFilter.GaussianBlur(SS * 3)))
    return im


def toque():
    im, d = layer()
    TQ, TQ_D, TW = (30, 86, 172), (20, 58, 124), (246, 246, 240)
    d.ellipse(P(cx - r * .97, cy - r * 1.24, cx + r * .97, cy - r * .30), fill=TQ)
    for k in range(-4, 5):
        x0 = cx + k * r * .2
        d.line(P(x0, cy - r * 1.05 + abs(k) * r * .04, x0, cy - r * .50), fill=(24, 72, 150), width=SS * 2)
    d.rounded_rectangle(P(cx - r * 1.03, cy - r * .54, cx + r * 1.03, cy - r * .24), radius=r * .12 * SS, fill=TQ_D)
    d.rectangle(P(cx - r * 1.01, cy - r * .43, cx + r * 1.01, cy - r * .35), fill=TW)
    for k in range(-9, 10):
        x0 = cx + k * r * .105
        d.line(P(x0, cy - r * .52, x0, cy - r * .44), fill=(12, 40, 92), width=SS * 2)
        d.line(P(x0, cy - r * .34, x0, cy - r * .26), fill=(12, 40, 92), width=SS * 2)
    pr = r * .18
    d.ellipse(P(cx - pr, cy - r * 1.27 - pr, cx + pr, cy - r * 1.27 + pr), fill=TW, outline=(214, 214, 206), width=SS * 2)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        qx, qy = cx + math.cos(a) * pr * .55, cy - r * 1.27 + math.sin(a) * pr * .55
        d.ellipse(P(qx - pr * .12, qy - pr * .12, qx + pr * .12, qy + pr * .12), fill=(226, 226, 218))
    return im


EYES = [(cx - r * .26, cy), (cx + r * .20, cy)]


def eyes(state):
    im, d = layer()
    for ex, ey in EYES:
        if state == "closed":
            d.arc(P(ex - r * .12, ey - r * .02, ex + r * .12, ey + r * .12), 20, 160, fill=INK, width=lw)
        else:
            d.ellipse(P(ex - r * .13, ey - r * .16, ex + r * .13, ey + r * .16), fill=(255, 255, 255), outline=INK, width=SS * 3)
            d.ellipse(P(ex - r * .075, ey - r * .085, ex + r * .075, ey + r * .085), fill=INK)
            d.ellipse(P(ex + r * .01, ey - r * .065, ex + r * .045, ey - r * .03), fill=(255, 255, 255))
            d.chord(P(ex - r * .14, ey - r * .17, ex + r * .14, ey + r * .17), 195, 345, fill=TEAL)
            d.line(P(ex - r * .125, ey - r * .085, ex + r * .125, ey - r * .085), fill=INK, width=lw)
    return im


def mouth(shape):
    im, d = layer()
    mx, my = MOUTH
    dark, tongue = (70, 18, 34), (255, 120, 120)
    if shape == "closed":
        d.arc(P(mx - r * .12, my - r * .10, mx + r * .12, my + r * .06), 25, 155, fill=INK, width=lw)
    elif shape == "small":
        d.ellipse(P(mx - r * .085, my - r * .035, mx + r * .085, my + r * .06), fill=dark)
    elif shape == "wide":
        d.chord(P(mx - r * .15, my - r * .10, mx + r * .15, my + r * .16), 0, 180, fill=dark)
        d.rectangle(P(mx - r * .15, my + r * .025, mx + r * .15, my + r * .035), fill=dark)
        d.chord(P(mx - r * .08, my + r * .05, mx + r * .08, my + r * .15), 180, 360, fill=tongue)
    elif shape == "o":
        d.ellipse(P(mx - r * .065, my - r * .06, mx + r * .065, my + r * .11), fill=dark, outline=INK, width=SS * 2)
    return im


def limb(pts):
    im, d = layer()
    sp = [P(*p) for p in pts]
    d.line(sp, fill=TEAL_D, width=int(aw), joint="curve")
    for p in sp:
        d.ellipse((p[0] - aw / 2, p[1] - aw / 2, p[0] + aw / 2, p[1] + aw / 2), fill=TEAL_D)
    return im


def hand(pt):
    im, d = layer()
    hx, hy = P(*pt)
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=TEAL, outline=TEAL_D, width=SS * 3)
    return im


# ---------- the double-stacked face cup (standalone image, anchor = hand point) ----------
CUP_COLORS = {
    "red": ((214, 40, 46), (168, 24, 32)),
    "orange": ((246, 128, 30), (196, 92, 14)),     # Halloween
    "blue": ((26, 78, 168), (16, 52, 120)),        # game night
}


def cup(color="red", face="cyto", h=270):
    S = SS * 2
    W_, H_ = int(h * .80), int(h * 1.08)
    im = Image.new("RGBA", (W_ * S, H_ * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c, cd_ = CUP_COLORS[color]
    tw, bw = W_ * .88, W_ * .62
    mid = W_ / 2
    def trap(y0, y1, w0, w1, fill):
        d.polygon([((mid - w0 / 2) * S, y0 * S), ((mid + w0 / 2) * S, y0 * S), ((mid + w1 / 2) * S, y1 * S), ((mid - w1 / 2) * S, y1 * S)], fill=fill)
    def w_at(y):  # width of the outer cup at height y
        return tw + (bw - tw) * (y - off) / (H_ - off)
    # inner (top) cup peeking out above the outer one
    off = h * .14
    trap(2, off + 8, tw * 1.03, tw * 1.0, c)
    d.line(((mid - tw * .50) * S, (off - 3) * S, (mid + tw * .50) * S, (off - 3) * S), fill=cd_, width=4 * S)
    d.rounded_rectangle(((mid - tw * .53) * S, 1 * S, (mid + tw * .53) * S, (h * .045 + 2) * S), radius=4 * S, fill=(246, 244, 238))
    # outer cup
    trap(off, H_ - 2, tw, bw, c)
    d.rounded_rectangle(((mid - tw * .52) * S, off * S, (mid + tw * .52) * S, (off + h * .045) * S), radius=4 * S, fill=(246, 244, 238))
    for fy in (.58, .70):                                    # party-cup ridges
        y = off + (H_ - off) * fy
        ww = w_at(y)
        d.line(((mid - ww / 2 + 3) * S, y * S, (mid + ww / 2 - 3) * S, y * S), fill=cd_, width=3 * S)
    # left-side sheen
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([((mid - tw * .40) * S, (off + 10) * S), ((mid - tw * .30) * S, (off + 10) * S), ((mid - bw * .22) * S, (H_ - 10) * S), ((mid - bw * .32) * S, (H_ - 10) * S)], fill=(255, 255, 255, 70))
    im.alpha_composite(sh)
    # Cyto face logo (flat)
    lx, ly, lr = mid, off + (H_ - off) * .33, h * .16
    d.ellipse(((lx - lr * 1.12) * S, (ly - lr * 1.12) * S, (lx + lr * 1.12) * S, (ly + lr * 1.12) * S), fill=(246, 244, 238))
    if face == "pumpkin":
        d.ellipse(((lx - lr) * S, (ly - lr * .85) * S, (lx + lr) * S, (ly + lr) * S), fill=(255, 150, 40))
        d.rectangle(((lx - lr * .10) * S, (ly - lr * 1.05) * S, (lx + lr * .10) * S, (ly - lr * .75) * S), fill=(60, 120, 50))
        for sx in (-1, 1):
            d.polygon([((lx + sx * lr * .40) * S, (ly - lr * .30) * S), ((lx + sx * lr * .18) * S, (ly + lr * .02) * S), ((lx + sx * lr * .62) * S, (ly + lr * .02) * S)], fill=INK)
        d.chord(((lx - lr * .55) * S, (ly - lr * .10) * S, (lx + lr * .55) * S, (ly + lr * .60) * S), 0, 180, fill=INK)
    else:
        d.ellipse(((lx - lr) * S, (ly - lr) * S, (lx + lr) * S, (ly + lr) * S), fill=TEAL, outline=TEAL_D, width=2 * S)
        d.chord(((lx - lr * .98) * S, (ly - lr * 1.1) * S, (lx + lr * .98) * S, (ly + lr * .10) * S), 180, 360, fill=(30, 86, 172))
        d.rectangle(((lx - lr * .98) * S, (ly - lr * .40) * S, (lx + lr * .98) * S, (ly - lr * .25) * S), fill=(246, 246, 240))
        d.ellipse(((lx - lr * .22) * S, (ly - lr * 1.32) * S, (lx + lr * .22) * S, (ly - lr * .88) * S), fill=(246, 246, 240))
        for ex in (lx - lr * .36, lx + lr * .30):
            d.ellipse(((ex - lr * .14) * S, (ly - lr * .08) * S, (ex + lr * .14) * S, (ly + lr * .22) * S), fill=INK)
            d.rectangle(((ex - lr * .17) * S, (ly - lr * .10) * S, (ex + lr * .17) * S, (ly + lr * .04) * S), fill=TEAL)
        d.arc(((lx - lr * .30) * S, (ly + lr * .18) * S, (lx + lr * .30) * S, (ly + lr * .58) * S), 20, 160, fill=INK, width=int(2.5 * S))
    return im.resize((W_, H_), Image.LANCZOS)


# outfits (swap layer only) -------------------------------------------------
def outfit_jersey():
    im, d = layer()
    JB, JW, JD = (24, 70, 160), (246, 246, 240), (14, 44, 110)
    m = Image.new("L", im.size, 0); md = ImageDraw.Draw(m)
    md.ellipse(P(cx - r * .99, cy - r * .99, cx + r * .99, cy + r * .99), fill=255)
    md.rectangle(P(0, 0, CANVAS, cy + r * .50), fill=0)
    lay = Image.new("RGBA", im.size, JB + (255,)); ld = ImageDraw.Draw(lay)
    ld.rectangle(P(0, cy + r * .64, CANVAS, cy + r * .70), fill=JW)
    ld.rectangle(P(0, cy + r * .75, CANVAS, cy + r * .80), fill=JW)
    im.paste(lay, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.polygon([P(cx - r * .22, cy + r * .50), P(cx + r * .22, cy + r * .50), P(cx, cy + r * .62)], fill=JW)
    nf = ImageFont.truetype(F_BLACK, int(r * .22 * SS))
    d.text(P(cx + r * .02, cy + r * .89), "6IX", font=nf, fill=JW, anchor="mm", stroke_width=SS * 3, stroke_fill=JD)
    return im


if __name__ == "__main__":
    save(body(), "body")
    save(toque(), "outfit_toque")          # default outfit (always on)
    save(outfit_jersey(), "outfit_jersey")
    for s in ("open", "closed"):
        save(eyes(s), f"eyes_{s}")
    for s in ("closed", "small", "wide", "o"):
        save(mouth(s), f"mouth_{s}")
    save(limb([SHOULDER_L, ELBOW_L, HAND_L]), "arm_left")
    save(hand(HAND_L), "hand_left")
    save(limb([SHOULDER_R, ELBOW_R, HAND_R]), "arm_right")
    save(hand(HAND_R), "hand_right")
    for col, face in (("red", "cyto"), ("orange", "pumpkin"), ("blue", "cyto")):
        cup(col, face).save(os.path.join(OUT, f"cup_{col}.png"))
    meta = {"canvas": CANVAS, "body_center": [cx, cy], "radius": r,
            "shoulder_left": SHOULDER_L, "hand_left": HAND_L, "shoulder_right": SHOULDER_R, "hand_right": HAND_R,
            "mouth": MOUTH, "cup_size": list(Image.open(os.path.join(OUT, "cup_red.png")).size),
            "cup_anchor": "cup centre x = hand_left.x + 0.22*cup_w; cup top = hand_left.y - 0.80*cup_h"}
    json.dump(meta, open(os.path.join(OUT, "rig.json"), "w"), indent=1)
    print("rig ->", OUT, sorted(os.listdir(OUT)))
