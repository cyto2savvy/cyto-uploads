"""Shared episode engine: timing, mouth sync, karaoke captions, punch zooms, Halloween bg, sources card, audio, render."""
import json, math, os, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
from render import (W, H, FPS, ease, lerp, font, F_BLACK, F_XB, F_SB, CREAM, CORAL, GOLD, TEAL_L, INK,
                    PANEL_XY, PW, PH, paste_alpha, term_card, pill, cyto)

ORANGE = (255, 140, 40)
E = {}  # episode state

# ---------------------------------------------------------------- setup
def init(D, costume, drop, tail=1.3, hits=(), glitch=None, halloween=True):
    E.update(D=D, costume=costume, halloween=halloween)
    tm = json.load(open(os.path.join(D, "timing.json")))
    E["words"], E["segs"], E["total"] = tm["words"], tm["segs"], tm["total"]
    E["end"] = round((E["total"] + tail) * FPS) / FPS
    nl = max(w["line"] for w in E["words"]) + 1
    rng = []
    for li in range(nl):
        ws = [w for w in E["words"] if w["line"] == li]; rng.append((ws[0]["t0"], ws[-1]["t1"]))
    E["lines"] = rng
    E["cuts"] = [0.0] + [round(((rng[i][1] + rng[i + 1][0]) / 2) * FPS) / FPS for i in range(nl - 1)] + [E["end"]]
    E["drop"] = wt(*drop)
    E["hits"] = [wt(*h) for h in hits]
    E["glitch"] = wt(*glitch) if glitch else None
    v = load_mono(os.path.join(D, "voice.wav"), 16000); hop = 16000 // FPS; n = len(v) // hop
    env = np.sqrt(np.mean(v[: n * hop].reshape(n, hop) ** 2, axis=1))
    env = env / (np.percentile(env, 95) + 1e-9)
    E["env"] = np.convolve(env, [0.25, 0.5, 0.25], mode="same")
    E["chunks"] = build_chunks()
    R.BG = halloween_bg() if halloween else R.make_bg()

def wt(line, word, which="t0"):
    for w in E["words"]:
        if w["line"] == line and w["w"].lower().strip('".,?!:').startswith(word.lower()):
            return w[which]
    raise KeyError((line, word))

def load_mono(path, sr):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768

def k_at(ta, t0, d=0.25):
    return ease((ta - t0) / d)

# ---------------------------------------------------------------- background
def halloween_bg():
    bg = R.make_bg()
    lay = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    mx, my, mr = 1720, 520, 150
    d.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=(255, 214, 130, 255))
    for cx_, cy_, cr in ((1680, 470, 30), (1780, 580, 22), (1700, 600, 14)):
        d.ellipse((cx_ - cr, cy_ - cr, cx_ + cr, cy_ + cr), fill=(236, 190, 110, 255))
    lay = lay.resize((W, H), Image.LANCZOS)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((860 - 150, 260 - 150, 860 + 150, 260 + 150), fill=(255, 170, 60, 90))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    bg.alpha_composite(lay)
    return bg

_bat = {}
def bat(size):
    if size in _bat: return _bat[size]
    s = 3; w_, h_ = size * s, int(size * .5) * s
    im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = (14, 18, 26, 255)
    d.polygon([(w_ * .5, h_ * .35), (w_ * .02, h_ * .05), (w_ * .12, h_ * .55), (w_ * .22, h_ * .45), (w_ * .30, h_ * .75), (w_ * .42, h_ * .6), (w_ * .5, h_ * .95),
               (w_ * .58, h_ * .6), (w_ * .70, h_ * .75), (w_ * .78, h_ * .45), (w_ * .88, h_ * .55), (w_ * .98, h_ * .05)], fill=c)
    d.ellipse((w_ * .42, h_ * .15, w_ * .58, h_ * .6), fill=c)
    im = im.resize((size, int(size * .5)), Image.LANCZOS); _bat[size] = im
    return im

def bats(f, ta):
    for i, (y0, sp, sz, ph) in enumerate(((330, 160, 70, 0.0), (420, 120, 54, 0.45), (260, 200, 46, 0.7))):
        x = ((ta * sp + ph * W) % (W + 200)) - 100
        y = y0 + math.sin(ta * 3 + i) * 20
        b = bat(sz)
        flap = 0.6 + 0.4 * abs(math.sin(ta * 12 + i))
        bb = b.resize((b.width, max(1, int(b.height * flap))), Image.BILINEAR)
        f.alpha_composite(bb, (int(x), int(y)))

def base(ta):
    f = R.base()
    if E.get("halloween", True): bats(f, ta)
    return f

# ---------------------------------------------------------------- Cyto
def in_gap(ta, min_gap=0.18):
    S = E["segs"]
    for (a, b, _), (c, d, _) in zip(S, S[1:]):
        if b <= ta < c and c - b >= min_gap: return True
    return ta < S[0][0] or ta >= S[-1][1]

def mouth(ta, idle="smile"):
    if in_gap(ta): return idle
    i = int(ta * FPS); env = E["env"]
    v = env[i] if 0 <= i < len(env) else 0
    return "closed" if v < 0.13 else ("mid" if v < 0.5 else "open")

BEAT = 60 / 140
def put_cyto(f, S, center, ta, mouth_state, arms="rest", look=(0, 0), eyes="open", hyper=1.0, shiver=0.0, bounce=0.0):
    blink = (ta % 3.7) < 0.12
    e = "closed" if (blink and eyes == "open") else eyes
    spr = cyto(S, e, mouth_state, arms, look, None if arms == "shrug" else "mystery", E["costume"])
    if ta >= E["drop"]:
        ph = ((ta - E["drop"]) / BEAT) % 1.0
        bob = 1 - abs(math.sin(math.pi * ph)) * 2; amp = 14 * hyper
    else:
        bob = math.sin(ta * 2 * math.pi * 0.8); amp = 8
    sq = 1 + 0.022 * bob * min(hyper, 2)
    w, h = spr.size
    spr2 = spr.resize((int(w / sq), int(h * sq)), Image.BILINEAR)
    jx = math.sin(ta * 70) * shiver
    by = abs(math.sin(ta * 9)) * bounce
    f.alpha_composite(spr2, (int(center[0] - spr2.width / 2 + jx), int(center[1] - spr2.height / 2 - bob * amp - by)))

def small_cyto(f, ta):
    put_cyto(f, 330, R.SMALL_C, ta, mouth(ta, "closed"), "point", (1, -1))

def host_cyto(f, ta, arms="rest", **kw):
    put_cyto(f, 560, R.HOST_C, ta, mouth(ta), arms, **kw)

def wave(ta):
    return "wave1" if int(ta * FPS / 7) % 2 == 0 else "wave2"

def card_in(f, ta, card, start=None):
    st = scene_start(ta) if start is None else start
    k = ease((ta - st - 0.2) / 0.35)
    c = term_card(*card)
    paste_alpha(f, c, (R.CARD_XY[0] + (1 - k) * 120, R.CARD_XY[1]), k)

def scene_start(ta):
    c = E["cuts"]
    for i in range(len(c) - 1):
        if c[i] <= ta < c[i + 1]: return c[i]
    return c[-2]

def panel_in(f, panel, ta):
    k = ease((ta - scene_start(ta)) / 0.3)
    paste_alpha(f, panel, (PANEL_XY[0], PANEL_XY[1] + (1 - k) * 60), k)

def panel_base():
    s = 2
    img = Image.new("RGBA", (PW * s, PH * s), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, PW * s - 1, PH * s - 1), radius=34 * s, fill=(12, 24, 40), outline=(52, 86, 112), width=3 * s)
    return img, ImageDraw.Draw(img), s

def big_title(f, ta, t0, lines, y=430, colors=(GOLD, CREAM), size=128):
    if ta < t0 - 0.05: return
    k = k_at(ta, t0 - 0.05, 0.2)
    shake = math.sin(ta * 40) * 6 * max(0, 1 - (ta - t0) / 0.6)
    yy = y
    for i, ln in enumerate(lines):
        im = R.caption_img(("*" + ln.replace(" ", "* *") + "*") if colors[i % 2] == GOLD else ln, size=size, maxw=1000)
        im = im.resize((int(im.width * (0.6 + 0.4 * k)), int(im.height * (0.6 + 0.4 * k))), Image.BILINEAR)
        paste_alpha(f, im, (W / 2 - im.width / 2 + shake, yy - im.height / 2), k)
        yy += int(size * 1.05)

def stamp(f, ta, t0, text, xy, size=56, fg=INK, bg=GOLD, rot=-6):
    if ta < t0 - 0.03: return
    kk = k_at(ta, t0 - 0.03, 0.15)
    p = pill(text, size, fg, bg, padx=34, pady=18)
    p2 = p.resize((int(p.width * (1.5 - 0.5 * kk)), int(p.height * (1.5 - 0.5 * kk))), Image.BILINEAR).rotate(rot, expand=True, resample=Image.BICUBIC)
    paste_alpha(f, p2, (xy[0] - p2.width / 2, xy[1] - p2.height / 2), kk)

def sources_card(f, ta, t0, lines, title="SOURCES · PUBMED"):
    k = k_at(ta, t0, 0.3)
    if k <= 0: return
    w, h = 980, 70 + 44 * len(lines)
    img = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius=40, fill=(250, 244, 232, 245))
    img = img.resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.text((32, 20), title, font=font(F_XB, 28), fill=CORAL)
    for i, ln in enumerate(lines):
        d.text((32, 64 + i * 44), ln, font=font(F_SB, 30), fill=INK)
    paste_alpha(f, img, (W / 2 - w / 2, 200 + (1 - k) * 30), k)

# ---------------------------------------------------------------- karaoke captions
def build_chunks():
    words = E["words"]; nl = len(E["lines"]); chunks = []
    for li in range(nl):
        cur = []
        for w in [w for w in words if w["line"] == li]:
            cur.append(w)
            if len(cur) == 3 or w["w"][-1] in ",.?:!" or w["w"].endswith("..."):
                chunks.append(cur); cur = []
        if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        a = c[0]["t0"] - 0.04; b = c[-1]["t1"] + 0.3
        if i + 1 < len(chunks):
            b = min(b, chunks[i + 1][0]["t0"] - 0.04)
            if chunks[i + 1][0]["line"] == c[0]["line"]: b = chunks[i + 1][0]["t0"] - 0.04
        else:
            b = E["end"]
        out.append((a, b, c))
    return out

_cap = {}
def caption(cw, active):
    key = (tuple(w["w"] for w in cw), active)
    if key in _cap: return _cap[key]
    size = 88; fnt = font(F_BLACK, size); sp = fnt.getlength(" ")
    texts = [w["w"] for w in cw]; widths = [fnt.getlength(t) for t in texts]
    total = sum(widths) + sp * (len(texts) - 1)
    lines = [list(range(len(texts)))]
    if total > 960 and len(texts) > 1:
        lines = [list(range(len(texts) - 1)), [len(texts) - 1]]
    lh = int(size * 1.25)
    img = Image.new("RGBA", (1040, lh * len(lines) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for li, idxs in enumerate(lines):
        lw = sum(widths[i] for i in idxs) + sp * (len(idxs) - 1)
        x = (img.width - lw) / 2; y = 20 + li * lh
        for i in idxs:
            if i == active:
                bb = fnt.getbbox(texts[i])
                d.rounded_rectangle((x - 12, y + bb[1] - 10, x + widths[i] + 12, y + bb[3] + 12), radius=16, fill=ORANGE)
                d.text((x, y), texts[i], font=fnt, fill=INK)
            else:
                d.text((x, y), texts[i], font=fnt, fill=CREAM, stroke_width=10, stroke_fill=INK)
            x += widths[i] + sp
    _cap[key] = img
    return img

def put_caption(f, ta, cy):
    for a, b, c in E["chunks"]:
        if a <= ta < b:
            act = 0
            for i, w in enumerate(c):
                if ta >= w["t0"] - 0.03: act = i
            img = caption(c, act)
            k = ease((ta - a) / 0.12); s = 0.8 + 0.2 * k
            im = img.resize((int(img.width * s), int(img.height * s)), Image.BILINEAR) if k < 1 else img
            f.alpha_composite(im, (int(W / 2 - im.width / 2), int(cy - im.height / 2)))
            return

# ---------------------------------------------------------------- post: punch zoom + glitch
def post(f, ta):
    z = 1.0
    for h in E["hits"]:
        if 0 <= ta - h < 0.8: z = max(z, 1 + 0.06 * math.exp(-(ta - h) / 0.16))
    if z > 1.001:
        zw, zh = int(W * z), int(H * z)
        f = f.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
    g = E["glitch"]
    if g is not None and 0 <= ta - g < 0.45:
        a = np.array(f.convert("RGB")); rnd = random.Random(int(ta * FPS)); sh = rnd.randint(8, 20)
        out = a.copy(); out[:, :, 0] = np.roll(a[:, :, 0], sh, axis=1); out[:, :, 2] = np.roll(a[:, :, 2], -sh, axis=1)
        for _ in range(5):
            y0 = rnd.randint(200, H - 300); hg = rnd.randint(20, 90)
            out[y0:y0 + hg] = np.roll(out[y0:y0 + hg], rnd.randint(-60, 60), axis=1)
        return Image.fromarray(out)
    return f.convert("RGB")

# ---------------------------------------------------------------- audio
SR = 44100
def tone(f0, f1, dur, decay):
    t = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR) * np.exp(-t / decay)
def noise(dur, seed=0):
    return np.random.default_rng(seed).standard_normal(int(dur * SR)).astype(np.float32)
def hp(x, a=0.95):
    y = np.zeros_like(x); px = py = 0.0
    for i in range(len(x)):
        py = a * (py + x[i] - px); px = x[i]; y[i] = py
    return y
def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y
def add(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i < 0 or i >= len(buf): return
    sig = sig[: len(buf) - i]; buf[i:i + len(sig)] += sig * gain

SPOOKY = [62, 65, 69, 68, 62, 65, 68, 65, 61, 65, 68, 64, 62, 65, 69, 70]
def make_audio(events):
    """events: list of (kind, time) with kind in boom/pop/ding/whoosh/zap/beat/crunch"""
    D, END, T_DROP = E["D"], E["end"], E["drop"]
    n = int((END + 0.5) * SR); music = np.zeros(n, np.float32)
    kick = tone(150, 42, 0.45, 0.18); sub = np.tanh(2.2 * tone(49, 46, 0.9, 0.45)) * 0.7
    snare = hp(noise(0.22, 1)) * np.exp(-np.arange(int(0.22 * SR)) / SR / 0.06) * 0.6
    hat = hp(noise(0.05, 2), 0.6) * np.exp(-np.arange(int(0.05 * SR)) / SR / 0.012) * 0.35
    def bell(m, dur=0.55):
        f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
        vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
        return (np.sin(2 * np.pi * f * t * vib) + 0.3 * np.sin(4 * np.pi * f * t) + 0.15 * np.sin(6 * np.pi * f * t)) * np.exp(-t / 0.25) * 0.17
    step = BEAT / 2; t = 0.0; i = 0
    while t < END + 0.4:
        add(music, bell(SPOOKY[i % 16]), t); t += step; i += 1
    intro = music.copy()
    t = T_DROP; s = 0
    while t < END + 0.4:
        pos = s % 16
        if pos in (0, 7, 10): add(music, kick, t); add(music, sub, t)
        if pos in (4, 12): add(music, snare, t)
        add(music, hat, t, 0.8 if pos % 2 == 0 else 0.5)
        if pos in (14, 15): add(music, hat, t + step / 3, 0.45); add(music, hat, t + 2 * step / 3, 0.45)
        t += step; s += 1
    idr = int(T_DROP * SR); music[:idr] = lp(intro[:idr], 0.08) * 1.6
    v = load_mono(os.path.join(D, "voice.wav"), SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.6 * np.clip(env * 3, 0, 1)); music *= 0.32
    sfx = np.zeros(n, np.float32)
    S = {
        "whoosh": lp(noise(0.4, 3), 0.25) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))) ** 2 * 0.5,
        "boom": tone(90, 35, 0.9, 0.35) * 0.9,
        "pop": tone(1200, 380, 0.08, 0.03) * 0.35,
        "ding": (tone(1760, 1760, 0.6, 0.18) + 0.5 * tone(2640, 2640, 0.6, 0.12)) * 0.22,
        "zap": np.sign(np.sin(np.linspace(0, 2 * np.pi * 900 * 0.12, int(0.12 * SR)))) * np.linspace(1, 0, int(0.12 * SR)) * 0.12,
        "beat": np.concatenate([tone(70, 50, 0.12, 0.05), np.zeros(int(0.06 * SR)), tone(65, 45, 0.14, 0.06)]) * 0.9,
        "crunch": np.round(noise(0.3, 6) * 3) / 3 * 0.12 * np.linspace(1, 0, int(0.3 * SR)),
        "beep": tone(1000, 1000, 0.09, 0.08) * 0.15,
    }
    for c in E["cuts"][1:-1]: add(sfx, S["whoosh"], c - 0.18)
    rd = min(T_DROP, 1.0)
    add(sfx, hp(noise(rd, 5), 0.9) * np.linspace(0, 1, int(rd * SR)) ** 2 * 0.25, T_DROP - rd)
    add(sfx, S["boom"], T_DROP)
    for kind, tt in events: add(sfx, S[kind], tt)
    mix = music + sfx; mix[:m] += v[:m]
    mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[: int(END * SR)]
    tmp = os.path.join(D, "mix_raw.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", tmp], input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", os.path.join(D, "mix.m4a")], check=True)

# ---------------------------------------------------------------- render
def run(scenes, out_name, mode, still_times=(), events=()):
    def frame(ta):
        c = E["cuts"]
        for i in range(len(scenes)):
            if c[i] <= ta < c[i + 1]: return (post_v3 if FX.get("on") else post)(scenes[i](ta), ta)
        return (post_v3 if FX.get("on") else post)(scenes[-1](ta), ta)
    D = E["D"]
    if mode == "stills":
        ims = [frame(t) for t in still_times]
        sheet = Image.new("RGB", (W * 3 // 2, H), (0, 0, 0))
        for i, im in enumerate(ims[:6]):
            sheet.paste(im.resize((W // 2, H // 2)), ((i % 3) * W // 2, (i // 3) * H // 2))
        sheet.save(os.path.join(D, "check.jpg"), quality=88)
        print("cuts", [round(x, 2) for x in E["cuts"]], "drop", round(E["drop"], 2))
        return
    make_audio(events)
    files = []
    for i in range(len(scenes)):
        a, b = E["cuts"][i], E["cuts"][i + 1]
        fin = os.path.join(D, f"p{i}.mp4"); tmp = os.path.join(D, f"p{i}.part.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for fi in range(round(a * FPS), round(b * FPS)):
            p.stdin.write(frame(fi / FPS).tobytes())
        p.stdin.close()
        if p.wait() != 0: raise SystemExit("ffmpeg failed")
        os.replace(tmp, fin); files.append(fin); print("scene", i, flush=True)
    lst = os.path.join(D, "list.txt"); open(lst, "w").writelines(f"file '{x}'\n" for x in files)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(D, "silent.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(D, "silent.mp4"), "-i", os.path.join(D, "mix.m4a"), "-map", "0:v", "-map", "1:a",
                    "-c", "copy", "-shortest", "-movflags", "+faststart", os.path.join(D, out_name)], check=True)
    print("done", out_name)

# ================================================================= v3 effects
FX = {"shakes": [], "bursts": [], "wipes": True, "progress": True}
RED_BTN = (230, 33, 23)

def post_v3(f, ta):
    f = post(f, ta)                                   # punch zoom + glitch, returns RGB
    f = f.convert("RGBA")
    d = ImageDraw.Draw(f)
    # sparkle bursts
    for t0, (cx, cy), col in FX["bursts"]:
        u = ta - t0
        if 0 <= u < 0.7:
            k = ease(u / 0.7); a = int(255 * (1 - u / 0.7))
            for i in range(14):
                ang = i / 14 * 2 * math.pi + t0
                rr = 40 + 240 * k * (0.7 + 0.3 * ((i * 37) % 7) / 7)
                x, y = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr
                sz = 14 * (1 - k) + 4
                d.polygon([(x, y - sz), (x + sz * .35, y - sz * .35), (x + sz, y), (x + sz * .35, y + sz * .35), (x, y + sz),
                           (x - sz * .35, y + sz * .35), (x - sz, y), (x - sz * .35, y - sz * .35)], fill=col + (a,))
    # swipe transitions
    if FX["wipes"]:
        for c in E["cuts"][1:-1]:
            u = (ta - c + 0.16) / 0.32
            if 0 <= u <= 1:
                x = -700 + (W + 1400) * ease(u)
                for off, col in ((0, ORANGE), (160, GOLD)):
                    d.polygon([(x - 260 - off, 0), (x - off, 0), (x - 400 - off, H), (x - 660 - off, H)], fill=col + (235,))
    # progress bar
    if FX["progress"]:
        k = min(1, ta / E["end"])
        d.rectangle((0, 0, W, 10), fill=(255, 255, 255, 50)); d.rectangle((0, 0, int(W * k), 10), fill=ORANGE + (255,))
    # screen shake
    sx = sy = 0
    for t0 in FX["shakes"]:
        u = ta - t0
        if 0 <= u < 0.3:
            amp = 18 * (1 - u / 0.3)
            rnd = random.Random(int(ta * FPS) + 11)
            sx += rnd.uniform(-amp, amp); sy += rnd.uniform(-amp, amp)
    f = f.convert("RGB")
    if sx or sy:
        f = Image.Image.transform(f, f.size, Image.AFFINE, (1, 0, -sx, 0, 1, -sy), resample=Image.BILINEAR)
    return f

_ic = {}
def thumbs_up(size=170, col=(255, 255, 255)):
    key = (size, col)
    if key in _ic: return _ic[key]
    s = 4; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=(30, 30, 36), outline=(255, 255, 255), width=5 * s)
    u = S / 100
    d.rounded_rectangle((22 * u, 46 * u, 36 * u, 76 * u), radius=3 * u, fill=col)
    d.rounded_rectangle((40 * u, 44 * u, 76 * u, 76 * u), radius=8 * u, fill=col)
    d.polygon([(40 * u, 48 * u), (52 * u, 22 * u), (60 * u, 24 * u), (58 * u, 46 * u)], fill=col)
    im = im.resize((size, size), Image.LANCZOS); _ic[key] = im
    return im

def heart_icon(size, col=(255, 70, 100)):
    im = Image.new("RGBA", (size * 3, size * 3), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for i in range(60):
        t = 2 * math.pi * i / 60
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((size * 1.5 + x * size * 3 / 36, size * 1.5 - y * size * 3 / 36))
    d.polygon(pts, fill=col)
    return im.resize((size, size), Image.LANCZOS)

def sub_button(subscribed):
    fnt = font(F_BLACK, 56)
    txt = "SUBSCRIBED" if subscribed else "SUBSCRIBE"
    w = int(fnt.getlength(txt)) + 90; h = 116
    im = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius=h, fill=(90, 96, 104) if subscribed else RED_BTN)
    im = im.resize((w, h), Image.LANCZOS)
    ImageDraw.Draw(im).text((w / 2, h / 2), txt, font=fnt, fill=(255, 255, 255), anchor="mm")
    return im

def bell(size, ring):
    s = 4; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = S / 100
    d.chord((22 * u, 14 * u, 78 * u, 74 * u), 180, 360, fill=GOLD)
    d.rectangle((22 * u, 44 * u, 78 * u, 70 * u), fill=GOLD)
    d.rounded_rectangle((14 * u, 66 * u, 86 * u, 76 * u), radius=4 * u, fill=GOLD)
    d.ellipse((42 * u, 76 * u, 58 * u, 90 * u), fill=GOLD)
    im = im.resize((size, size), Image.LANCZOS)
    return im.rotate(math.sin(ring * 40) * 22 * max(0, 1 - ring / 1.2), resample=Image.BICUBIC)

def cursor(size=70):
    im = Image.new("RGBA", (size * 3, size * 3), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = size * 3 / 100
    pts = [(10 * u, 5 * u), (10 * u, 80 * u), (30 * u, 62 * u), (44 * u, 92 * u), (56 * u, 86 * u), (42 * u, 57 * u), (68 * u, 57 * u)]
    d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0)); d.line(pts + [pts[0]], fill=(0, 0, 0), width=int(4 * u))
    return im.resize((size, size), Image.LANCZOS)

def mic(size=120):
    s = 3; S = size * s
    im = Image.new("RGBA", (S, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((S * .25, 0, S * .75, S * .6), radius=S * .25, fill=(190, 196, 204), outline=(90, 96, 104), width=3 * s)
    for i in range(1, 4): d.line((S * .28, S * .15 * i, S * .72, S * .15 * i), fill=(120, 126, 134), width=2 * s)
    d.rounded_rectangle((S * .38, S * .58, S * .62, S * 1.8), radius=S * .1, fill=(30, 30, 34))
    return im.resize((size, size * 2), Image.LANCZOS)

def outro(f, ta, line):
    """Like + subscribe + mic drop. `line` = index of the outro line."""
    t_like, t_sub, t_out = wt(line, "Like"), wt(line, "subscribe"), wt(line, "out")
    t_click = t_sub + 0.55
    if ta >= t_like - 0.05:
        k = k_at(ta, t_like - 0.05, 0.18)
        ic = thumbs_up(200, (255, 255, 255) if ta < t_like + 0.35 else (90, 170, 255))
        sc = 0.5 + 0.5 * k + 0.12 * math.exp(-max(0, ta - t_like - 0.35) / 0.12) * (ta > t_like + 0.35)
        ic = ic.resize((int(200 * sc), int(200 * sc)), Image.BILINEAR)
        paste_alpha(f, ic, (200 - ic.width / 2, 480 - ic.height / 2), k)
        for i in range(6):
            u = ta - t_like - 0.35 - i * 0.12
            if 0 <= u < 1.4:
                h = heart_icon(54 + (i % 3) * 10, (255, 70 + i * 20, 110))
                paste_alpha(f, h, (150 - u * 120 + math.sin(u * 6 + i) * 30, 560 - u * 90 + i * 8), max(0, 1 - u / 1.4))
    if ta >= t_sub - 0.05:
        k = k_at(ta, t_sub - 0.05, 0.18)
        b = sub_button(ta >= t_click)
        press = 0.92 if t_click <= ta < t_click + 0.12 else 1.0
        bw, bh = int(b.width * (0.6 + 0.4 * k) * press), int(b.height * (0.6 + 0.4 * k) * press)
        b2 = b.resize((max(1, bw), max(1, bh)), Image.BILINEAR)
        bx, by = 640 - b2.width / 2, 480 - b2.height / 2
        paste_alpha(f, b2, (bx, by), k)
        if ta >= t_click:
            paste_alpha(f, bell(110, ta - t_click), (640 + b2.width / 2 - 30, 370), k_at(ta, t_click, 0.15))
        # cursor glides in and clicks
        u = ease((ta - t_sub) / 0.5)
        cx_, cy_ = lerp(1000, 690, u), lerp(820, 500, u)
        if ta < t_click + 0.7:
            paste_alpha(f, cursor(80), (cx_, cy_), min(1, (ta - t_sub) * 5) * (1 - k_at(ta, t_click + 0.4, 0.3)))
    if ta >= t_out:
        u = ta - t_out
        y = 700 + min(1.0, u / 0.35) ** 2 * 560
        m = mic(110).rotate(-25 - 40 * min(1, u / 0.35), expand=True, resample=Image.BICUBIC)
        paste_alpha(f, m, (760, y - m.height / 2), 1 - k_at(ta, t_out + 0.9, 0.3))

def run_v3(scenes, out_name, mode, still_times=(), events=()):
    FX["on"] = True
    run(scenes, out_name, mode, still_times, events)
