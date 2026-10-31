"""Episode 1 v2: Toronto Cyto, youth voice, karaoke captions, subway scene, glitch, original beat + SFX.
python3 ep.py stills | audio | video
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R
from render import (W, H, FPS, ease, lerp, font, F_BLACK, F_XB, CREAM, CORAL, GOLD, TEAL_L, INK,
                    PANEL_XY, PW, PH, SKIN_Y, HAIR_X, to_frame, label, paste_alpha, term_card, note, pill, cyto)

TM = json.load(open(os.path.join(HERE, "timing.json")))
WORDS = TM["words"]; SEGS = TM["segs"]; TOTAL = TM["total"]
END = round((TOTAL + 0.05) * FPS) / FPS

def wt(line, word, which="t0"):
    """time of the first word in `line` starting with `word`"""
    for w in WORDS:
        if w["line"] == line and w["w"].lower().startswith(word.lower()):
            return w[which]
    raise KeyError((line, word))

LINE_RANGE = []
for li in range(7):
    ws = [w for w in WORDS if w["line"] == li]
    LINE_RANGE.append((ws[0]["t0"], ws[-1]["t1"]))
CUTS = [0.0] + [round(((LINE_RANGE[i][1] + LINE_RANGE[i + 1][0]) / 2) * FPS) / FPS for i in range(6)] + [END]

T_DROP = wt(0, "drops")
BPM = 140.0
BEAT = 60 / BPM
GLITCH = wt(5, "glitch")
HITS = [T_DROP, wt(0, "goosebumps"), wt(1, "arrector"), wt(2, "TTC"), wt(3, "bump"), wt(4, "bigger"), GLITCH]

# ---------------------------------------------------------------- voice envelope -> mouth
def load_mono(path, sr):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
_v = load_mono(os.path.join(HERE, "voice.wav"), 16000)
_hop = 16000 // FPS
_n = len(_v) // _hop
ENV = np.sqrt(np.mean(_v[: _n * _hop].reshape(_n, _hop) ** 2, axis=1))
ENV = ENV / (np.percentile(ENV, 95) + 1e-9)
ENV = np.convolve(ENV, [0.25, 0.5, 0.25], mode="same")

def in_gap(ta, min_gap=0.18):
    for (a, b, _), (c, d, _) in zip(SEGS, SEGS[1:]):
        if b <= ta < c and c - b >= min_gap:
            return True
    return ta < SEGS[0][0] or ta >= SEGS[-1][1]

def mouth(ta, idle="smile"):
    if in_gap(ta):
        return idle
    i = int(ta * FPS)
    v = ENV[i] if 0 <= i < len(ENV) else 0
    return "closed" if v < 0.13 else ("mid" if v < 0.5 else "open")

def put_cyto(f, S, center, ta, mouth_state, arms="rest", look=(0, 0), eyes="open", vibe=False):
    blink = (ta % 3.7) < 0.12
    e = "closed" if (blink and eyes == "open") else eyes
    spr = cyto(S, e, mouth_state, arms, look, None if arms == "shrug" else "mystery")
    if vibe and ta >= T_DROP:
        ph = ((ta - T_DROP) / BEAT) % 1.0
        bob = 1 - abs(math.sin(math.pi * ph)) * 2  # snaps down on each beat
        amp = 14
    else:
        bob = math.sin(ta * 2 * math.pi * 0.8); amp = 8
    sq = 1 + 0.022 * bob
    w, h = spr.size
    spr2 = spr.resize((int(w / sq), int(h * sq)), Image.BILINEAR)
    f.alpha_composite(spr2, (int(center[0] - spr2.width / 2), int(center[1] - spr2.height / 2 - bob * amp)))

# ---------------------------------------------------------------- karaoke captions
def build_chunks():
    chunks = []
    for li in range(7):
        ws = [w for w in WORDS if w["line"] == li]
        cur = []
        for w in ws:
            cur.append(w)
            if len(cur) == 3 or w["w"][-1] in ",.?:" or w["w"].endswith("..."):
                chunks.append(cur); cur = []
        if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        a = c[0]["t0"] - 0.04
        b = c[-1]["t1"] + 0.3
        if i + 1 < len(chunks):
            b = min(b, chunks[i + 1][0]["t0"] - 0.04)
            if chunks[i + 1][0]["line"] == c[0]["line"]:
                b = chunks[i + 1][0]["t0"] - 0.04
        out.append((a, b, c))
    return out
CHUNKS = build_chunks()

_cap_cache = {}
def caption(chunk_words, active):
    key = (tuple(w["w"] for w in chunk_words), active)
    if key in _cap_cache: return _cap_cache[key]
    size = 88
    fnt = font(F_BLACK, size)
    sp = fnt.getlength(" ")
    texts = [w["w"].replace("styll", "styll") for w in chunk_words]
    widths = [fnt.getlength(t) for t in texts]
    total = sum(widths) + sp * (len(texts) - 1)
    lines = [list(range(len(texts)))]
    if total > 960 and len(texts) > 1:
        lines = [list(range(len(texts) - 1)), [len(texts) - 1]]
    lh = int(size * 1.25)
    img = Image.new("RGBA", (1040, lh * len(lines) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for li, idxs in enumerate(lines):
        lw = sum(widths[i] for i in idxs) + sp * (len(idxs) - 1)
        x = (img.width - lw) / 2; y = 20 + li * lh
        for i in idxs:
            if i == active:
                bb = fnt.getbbox(texts[i])
                d.rounded_rectangle((x - 12, y + bb[1] - 10, x + widths[i] + 12, y + bb[3] + 12), radius=16, fill=GOLD)
                d.text((x, y), texts[i], font=fnt, fill=INK)
            else:
                d.text((x, y), texts[i], font=fnt, fill=CREAM, stroke_width=10, stroke_fill=INK)
            x += widths[i] + sp
    _cap_cache[key] = img
    return img

def put_caption(f, ta, cy):
    for a, b, c in CHUNKS:
        if a <= ta < b:
            act = 0
            for i, w in enumerate(c):
                if ta >= w["t0"] - 0.03: act = i
            img = caption(c, act)
            k = ease((ta - a) / 0.12)
            s = 0.8 + 0.2 * k
            im = img.resize((int(img.width * s), int(img.height * s)), Image.BILINEAR) if k < 1 else img
            f.alpha_composite(im, (int(W / 2 - im.width / 2), int(cy - im.height / 2)))
            return

# ---------------------------------------------------------------- subway scene
YEL = (255, 204, 0)
STN = [(120, 470, "BRAIN"), (300, 250, "SPINAL CORD"), (650, 250, "NERVE"), (830, 470, "HAIR MUSCLE")]
def path_pt(p):
    pts = [(x, y) for x, y, _ in STN]
    L = [math.dist(pts[i], pts[i + 1]) for i in range(3)]
    d = p * sum(L)
    for i in range(3):
        if d <= L[i] or i == 2:
            u = min(1, d / L[i])
            return (lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u)), math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
        d -= L[i]

_train_cache = {}
def train_sprite():
    if "t" in _train_cache: return _train_cache["t"]
    s = 3; tw, th = 150, 56
    im = Image.new("RGBA", (tw * s, th * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw * s - 1, th * s - 1), radius=18 * s, fill=(222, 228, 234), outline=(40, 50, 60), width=3 * s)
    d.rectangle((0, 34 * s, tw * s, 42 * s), fill=(214, 40, 48))
    for i in range(4):
        x = 16 + i * 32
        d.rounded_rectangle((x * s, 9 * s, (x + 22) * s, 27 * s), radius=4 * s, fill=(40, 60, 84))
    im = im.resize((tw, th), Image.LANCZOS)
    _train_cache["t"] = im
    return im

def draw_subway(tl_cold, tl_shook, train_p, trail, stamp_k, sig_k):
    s = 2
    img = Image.new("RGBA", (PW * s, PH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, PW * s - 1, PH * s - 1), radius=34 * s, fill=(12, 24, 40), outline=(52, 86, 112), width=3 * s)
    for gx in range(40, PW, 60):
        d.line((gx * s, 20 * s, gx * s, (PH - 20) * s), fill=(20, 36, 56), width=s)
    for gy in range(40, PH, 60):
        d.line((20 * s, gy * s, (PW - 20) * s, gy * s), fill=(20, 36, 56), width=s)
    pts = [(x * s, y * s) for x, y, _ in STN]
    d.line(pts, fill=YEL, width=30 * s, joint="curve")
    for x, y, _ in STN:
        d.ellipse(((x - 26) * s, (y - 26) * s, (x + 26) * s, (y + 26) * s), fill=(250, 250, 250), outline=(20, 20, 20), width=6 * s)
    img = img.resize((PW, PH), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    lf = font(F_XB, 30)
    for x, y, name in STN:
        tw = lf.getlength(name)
        ty = y + 40 if y > 300 else y - 76
        tx = min(max(30, x - tw / 2), PW - 30 - tw)
        d.text((tx, ty), name, font=lf, fill=CREAM)
    hdr = pill("NERVE LINE · FIGHT-OR-FLIGHT", 26, INK, YEL)
    img.alpha_composite(hdr, (30, PH - 90))
    # cold / shook triggers next to the brain
    for k, txt, xy in ((tl_cold, "COLD", (30, 290)), (tl_shook, "SHOOK", (30, 365))):
        if k > 0:
            p = pill(txt, 30, INK, TEAL_L if txt == "COLD" else CORAL)
            ps = p.resize((max(1, int(p.width * (0.6 + 0.4 * k))), max(1, int(p.height * (0.6 + 0.4 * k)))), Image.BILINEAR)
            paste_alpha(img, ps, xy, k)
    # signal glow along the travelled path
    if sig_k > 0 and train_p is not None:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        n = 40
        seg = [path_pt(train_p * i / n)[0] for i in range(n + 1)]
        gd.line(seg, fill=(255, 245, 180, int(200 * sig_k)), width=18, joint="curve")
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
    if train_p is not None:
        tr = train_sprite()
        for g in range(trail, 0, -1):
            pp = max(0.0, train_p - g * 0.045)
            (x, y), ang = path_pt(pp)
            r_ = tr.rotate(-math.degrees(ang), expand=True, resample=Image.BICUBIC)
            paste_alpha(img, r_, (x - r_.width / 2, y - r_.height / 2), 0.18 * (trail - g + 1) / trail)
        (x, y), ang = path_pt(train_p)
        r_ = tr.rotate(-math.degrees(ang), expand=True, resample=Image.BICUBIC)
        img.alpha_composite(r_, (int(x - r_.width / 2), int(y - r_.height / 2)))
    if stamp_k > 0:
        st = pill("TTC COULD NEVER", 52, (255, 255, 255), CORAL, padx=30, pady=18)
        sc = 1.6 - 0.6 * stamp_k
        st = st.resize((int(st.width * sc), int(st.height * sc)), Image.BILINEAR).rotate(8, expand=True, resample=Image.BICUBIC)
        paste_alpha(img, st, (PW / 2 - st.width / 2, PH / 2 - st.height / 2 + 30), min(1, stamp_k * 1.5))
    return img

# ---------------------------------------------------------------- shared bits
def k_at(ta, t0, d=0.25):
    return ease((ta - t0) / d)

def card_in(f, ta, scene_start, card):
    k = ease((ta - scene_start - 0.2) / 0.35)
    c = term_card(*card)
    paste_alpha(f, c, (R.CARD_XY[0] + (1 - k) * 120, R.CARD_XY[1]), k)

def small_cyto(f, ta):
    put_cyto(f, 330, R.SMALL_C, ta, mouth(ta, "closed"), "point", (1, -1), vibe=True)

def zoom_glitch(f, ta):
    z = 1.0
    for h in HITS:
        if 0 <= ta - h < 0.8:
            z = max(z, 1 + 0.06 * math.exp(-(ta - h) / 0.16))
    if z > 1.001:
        zw, zh = int(W * z), int(H * z)
        f = f.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
    if 0 <= ta - GLITCH < 0.5:
        a = np.array(f.convert("RGB"))
        rnd = random.Random(int(ta * FPS))
        sh = rnd.randint(8, 20)
        out = a.copy()
        out[:, :, 0] = np.roll(a[:, :, 0], sh, axis=1)
        out[:, :, 2] = np.roll(a[:, :, 2], -sh, axis=1)
        for _ in range(5):
            y0 = rnd.randint(200, H - 300); hgt = rnd.randint(20, 90)
            out[y0:y0 + hgt] = np.roll(out[y0:y0 + hgt], rnd.randint(-60, 60), axis=1)
        return Image.fromarray(out)
    return f.convert("RGB")

# ---------------------------------------------------------------- scenes (absolute time ta)
def sc_hook(ta):
    f = R.base()
    gb = wt(0, "goosebumps")
    if ta >= gb - 0.05:
        big = R.caption_img("GOOSEBUMPS?", size=128, maxw=1000)
        k = k_at(ta, gb - 0.05, 0.2)
        shake = math.sin(ta * 40) * 6 * max(0, 1 - (ta - gb) / 0.6)
        im = big.resize((int(big.width * (0.6 + 0.4 * k)), int(big.height * (0.6 + 0.4 * k))), Image.BILINEAR)
        paste_alpha(f, im, (W / 2 - im.width / 2 + shake, 430 - im.height / 2), k)
    if ta >= T_DROP:
        for (x0, ph, sz, col) in [(150, 0.0, 80, GOLD), (880, 0.5, 96, CORAL)]:
            u = ((ta - T_DROP) * 0.4 + ph) % 1.0
            paste_alpha(f, note(sz, col), (x0, 900 - u * 380), min(1, u * 4, (ta - T_DROP) * 3) * (1 - max(0, u - 0.75) * 4))
    arms = "wave1" if ta < T_DROP and int(ta * FPS / 7) % 2 == 0 else ("wave2" if ta < T_DROP else "rest")
    put_cyto(f, 560, R.HOST_C, ta, mouth(ta), arms, vibe=True)
    put_caption(f, ta, R.HOST_CAP_Y)
    return f

def sc_muscle(ta):
    st = CUTS[1]
    f = R.base()
    t_ar = wt(1, "arrector")
    panel, main = R.draw_skin(lift=0.0, pulse=max(0, math.sin((ta - t_ar) * 6)) if ta > t_ar else 0.0)
    k = ease((ta - st) / 0.35)
    paste_alpha(f, panel, (PANEL_XY[0], PANEL_XY[1] + (1 - k) * 60), k)
    fx, fy, ex, ey = main
    label(f, "hair", (PANEL_XY[0] + 620, PANEL_XY[1] + 60), to_frame((HAIR_X + 85, SKIN_Y - 42)), k_at(ta, wt(1, "hair")), side="right")
    label(f, "arrector pili muscle", (PANEL_XY[0] + 560, PANEL_XY[1] + 560), to_frame((lerp(fx, ex, .55), lerp(fy, ey, .55))), k_at(ta, t_ar), side="right")
    card_in(f, ta, st, ("ARRECTOR PILI", "Latin for “raiser of the hair.”"))
    small_cyto(f, ta)
    put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def sc_subway(ta):
    st = CUTS[2]
    f = R.base()
    t_fire, t_ttc = wt(2, "fire"), wt(2, "TTC")
    run = (ta - t_fire) / 0.55
    train_p = 0.0 if ta < t_fire else min(1.0, ease(run))
    trail = 6 if 0 < run < 1.3 else 0
    panel = draw_subway(k_at(ta, wt(2, "cold")), k_at(ta, wt(2, "shook")), train_p, trail, k_at(ta, t_ttc - 0.05, 0.15), k_at(ta, t_fire, 0.4))
    k = ease((ta - st) / 0.3)
    paste_alpha(f, panel, (PANEL_XY[0], PANEL_XY[1] + (1 - k) * 60), k)
    card_in(f, ta, st, ("SYMPATHETIC NERVES", "Your automatic fight-or-flight wiring."))
    small_cyto(f, ta)
    put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def sc_bump(ta):
    st = CUTS[3]
    f = R.base()
    t_sq, t_up = wt(3, "squeezes"), wt(3, "up", "t1")
    lift = ease((ta - t_sq) / max(0.4, t_up - t_sq))
    panel, main = R.draw_skin(lift=lift, pulse=0.45 if t_sq < ta < t_up + 0.3 else 0.0,
                              impulse=((ta - st) * 0.9) % 1.0 if ta < t_sq else None)
    f.alpha_composite(panel, PANEL_XY)
    label(f, "goosebump!", (PANEL_XY[0] + 30, PANEL_XY[1] + 40), to_frame((HAIR_X + 30, SKIN_Y - 36)), k_at(ta, wt(3, "bump")))
    card_in(f, ta, st, ("PILOERECTION", "The science word for goosebumps."))
    small_cyto(f, ta)
    put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def sc_fur(ta):
    st = CUTS[4]
    f = R.base()
    panel, main = R.draw_skin(lift=1.0, fur=ease((ta - st) / 0.6), warm=ease((ta - wt(4, "puffed")) / 0.6))
    f.alpha_composite(panel, PANEL_XY)
    label(f, "trapped warm air", (PANEL_XY[0] + 40, PANEL_XY[1] + 40), to_frame((PW * 0.62, SKIN_Y - 120)), k_at(ta, wt(4, "Warmer")))
    card_in(f, ta, st, ("INSULATION", "Fluffed fur holds a layer of warm air."))
    small_cyto(f, ta)
    put_caption(f, ta, R.DIAG_CAP_Y)
    return f

def sc_glitch(ta):
    f = R.base()
    t_lo = wt(5, "leftover")
    k = k_at(ta, t_lo - 0.1, 0.3) * (1 - k_at(ta, wt(5, "No") - 0.1, 0.12))
    c = term_card("VESTIGIAL", "A trait that has lost most of its original job.", 620, 220)
    paste_alpha(f, c, (W / 2 - c.width / 2, 330 + (1 - k) * 40), k)
    if ta >= wt(5, "No"):
        p = pill("NO CAP", 56, INK, GOLD, padx=34, pady=18)
        kk = k_at(ta, wt(5, "No"), 0.15)
        p2 = p.resize((int(p.width * (1.5 - 0.5 * kk)), int(p.height * (1.5 - 0.5 * kk))), Image.BILINEAR).rotate(-6, expand=True, resample=Image.BICUBIC)
        paste_alpha(f, p2, (W / 2 - p2.width / 2, 400), kk)
    shrug = wt(5, "lost") - 0.1 <= ta < wt(5, "fur", "t1") + 0.4
    put_cyto(f, 560, R.HOST_C, ta, mouth(ta), "shrug" if shrug else "rest", vibe=True)
    put_caption(f, ta, R.HOST_CAP_Y)
    return f

def sc_outro(ta):
    f = R.base()
    st = CUTS[6]
    for (x0, ph, sz, col) in [(150, 0.0, 90, GOLD), (870, 0.35, 110, CORAL), (300, 0.7, 70, TEAL_L), (760, 0.15, 80, GOLD)]:
        u = ((ta - st) * 0.45 + ph) % 1.0
        paste_alpha(f, note(sz, col), (x0 + math.sin((ta + ph) * 3) * 25, 860 - u * 520), min(1, u * 4, (ta - st) * 4) * (1 - max(0, u - 0.75) * 4))
    put_cyto(f, 560, R.HOST_C, ta, mouth(ta), "wave1" if int(ta * FPS / 7) % 2 == 0 else "wave2", eyes="open", vibe=True)
    put_caption(f, ta, R.HOST_CAP_Y)
    return f

SCENES = [sc_hook, sc_muscle, sc_subway, sc_bump, sc_fur, sc_glitch, sc_outro]

def frame(ta):
    for i in range(7):
        if CUTS[i] <= ta < CUTS[i + 1]:
            return zoom_glitch(SCENES[i](ta), ta)
    return zoom_glitch(SCENES[-1](ta), ta)

# ---------------------------------------------------------------- audio: original beat + SFX
SR = 44100
def tone(f0, f1, dur, decay, sr=SR):
    t = np.arange(int(dur * sr)) / sr
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / sr
    return np.sin(ph) * np.exp(-t / decay)
def noise(dur, seed=0):
    return np.random.default_rng(seed).standard_normal(int(dur * SR)).astype(np.float32)
def hp(x, a=0.95):
    y = np.zeros_like(x); prev_x = prev_y = 0.0
    for i in range(len(x)):
        prev_y = a * (prev_y + x[i] - prev_x); prev_x = x[i]; y[i] = prev_y
    return y
def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y
def add(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    sig = sig[: len(buf) - i]
    buf[i:i + len(sig)] += sig * gain

def make_audio():
    n = int((END + 0.5) * SR)
    music = np.zeros(n, np.float32)
    kick = tone(150, 42, 0.45, 0.18)
    sub = np.tanh(2.2 * tone(49, 46, 0.9, 0.45)) * 0.7
    snare = hp(noise(0.22, 1)) * np.exp(-np.arange(int(0.22 * SR)) / SR / 0.06) * 0.6
    snare[: int(0.12 * SR)] += tone(220, 180, 0.12, 0.05)[: int(0.12 * SR)] * 0.3
    hat = hp(noise(0.05, 2), 0.6) * np.exp(-np.arange(int(0.05 * SR)) / SR / 0.012) * 0.35
    # minor-key bell loop (A minor / F / C / G feel)
    notes = [69, 72, 76, 72, 65, 69, 72, 69, 72, 76, 79, 76, 67, 71, 74, 71]
    def bell(m, dur=0.5):
        f = 440 * 2 ** ((m - 69) / 12)
        t = np.arange(int(dur * SR)) / SR
        return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)) * np.exp(-t / 0.22) * 0.18
    step = BEAT / 2
    t = 0.0; i = 0
    while t < END + 0.4:
        add(music, bell(notes[i % 16]), t)
        t += step; i += 1
    intro = music.copy()
    # drums from the drop
    t = T_DROP; s = 0
    while t < END + 0.4:
        pos = s % 16                         # 16 eighth-notes = 2 bars of half-time trap
        if pos in (0, 7, 10): add(music, kick, t); add(music, sub, t)
        if pos in (4, 12): add(music, snare, t)
        add(music, hat, t, 0.8 if pos % 2 == 0 else 0.5)
        if pos in (14, 15):                  # hat roll
            add(music, hat, t + step / 3, 0.45); add(music, hat, t + 2 * step / 3, 0.45)
        t += step; s += 1
    # before the drop only a muffled bell loop
    i_drop = int(T_DROP * SR)
    music[:i_drop] = lp(intro[:i_drop], 0.08) * 1.6
    # glitch stutter: repeat a 1/16 slice
    gi = int(GLITCH * SR); sl = int(step / 2 * SR)
    piece = music[gi:gi + sl].copy()
    for r_ in range(int(0.45 / (step / 2))):
        a = gi + r_ * sl
        music[a:a + sl] = piece[: max(0, min(sl, n - a))]
    # duck under the voice
    v = load_mono(os.path.join(HERE, "voice.wav"), SR)
    vv = np.zeros(n, np.float32); vv[: min(n, len(v))] = v[:n]
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same")
    env = env / (env.max() + 1e-9)
    music *= (1 - 0.6 * np.clip(env * 3, 0, 1))
    music *= 0.32
    sfx = np.zeros(n, np.float32)
    whoosh = lp(noise(0.4, 3), 0.25) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))) ** 2 * 0.5
    for c in CUTS[1:-1]:
        add(sfx, whoosh, c - 0.18)
    boom = tone(90, 35, 0.9, 0.35) * 0.9
    for tb in (T_DROP, wt(2, "TTC") - 0.05, wt(3, "bump")):
        add(sfx, boom, tb)
    # riser into the drop
    rd = min(T_DROP, 1.0)
    rise = hp(noise(rd, 5), 0.9) * np.linspace(0, 1, int(rd * SR)) ** 2 * 0.25
    add(sfx, rise, T_DROP - rd)
    pop = tone(1200, 380, 0.08, 0.03) * 0.35
    for tp in (wt(1, "hair"), wt(2, "cold"), wt(2, "shook"), wt(4, "Warmer"), wt(5, "No"), wt(0, "goosebumps")):
        add(sfx, pop, tp)
    ding = (tone(1760, 1760, 0.6, 0.18) + 0.5 * tone(2640, 2640, 0.6, 0.12)) * 0.22
    add(sfx, ding, wt(1, "arrector"))
    zap = np.sign(np.sin(np.linspace(0, 2 * np.pi * 900 * 0.12, int(0.12 * SR)))) * np.linspace(1, 0, int(0.12 * SR)) * 0.12
    add(sfx, zap, wt(2, "fire"))
    crush = np.round(noise(0.4, 6) * 3) / 3 * 0.1 * np.repeat(np.random.default_rng(7).random(40) > 0.4, int(0.4 * SR) // 40 + 1)[: int(0.4 * SR)]
    add(sfx, crush, GLITCH)
    mix = music + sfx
    m = min(n, len(v))
    mix[:m] += v[:m]
    peak = np.max(np.abs(mix))
    mix = np.tanh(mix / max(1.0, peak * 0.9)) * 0.95
    mix = mix[: int(END * SR)]
    pcm = (mix * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "aac", "-b:a", "192k", os.path.join(HERE, "mix.m4a")], input=pcm, check=True)

# ---------------------------------------------------------------- render
def render_range(name, a, b):
    final = os.path.join(HERE, f"{name}.mp4"); tmp = os.path.join(HERE, f"{name}.part.mp4")
    fa, fb = round(a * FPS), round(b * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(fa, fb):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit("ffmpeg failed " + name)
    os.replace(tmp, final)
    return final

if __name__ == "__main__":
    R.BG = R.make_bg()
    mode = sys.argv[1]
    if mode == "stills":
        ts = [wt(0, "goosebumps") + 0.3, wt(1, "arrector") + 0.4, wt(2, "TTC") + 0.25, wt(3, "bump") + 0.4, GLITCH + 0.1, wt(6, "every")]
        ims = [frame(t) for t in ts]
        sheet = Image.new("RGB", (W * 3 // 2, H), (0, 0, 0))
        for i, im in enumerate(ims):
            sheet.paste(im.resize((W // 2, H // 2)), ((i % 3) * W // 2, (i // 3) * H // 2))
        sheet.save(os.path.join(HERE, "check.jpg"), quality=88)
        print("cuts", [round(c, 2) for c in CUTS], "drop", round(T_DROP, 2), "end", END)
    elif mode == "audio":
        make_audio(); print("audio ok")
    else:
        files = [render_range(f"p{i}", CUTS[i], CUTS[i + 1]) for i in range(7)]
        lst = os.path.join(HERE, "list.txt")
        open(lst, "w").writelines(f"file '{f}'\n" for f in files)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(HERE, "silent.mp4")], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "silent.mp4"), "-i", os.path.join(HERE, "mix.m4a"), "-map", "0:v", "-map", "1:a",
                        "-c", "copy", "-shortest", "-movflags", "+faststart", os.path.join(HERE, "cyto-ep1-goosebumps.mp4")], check=True)
        print("done")
