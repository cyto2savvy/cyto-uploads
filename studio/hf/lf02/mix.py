"""LF02 audio: dialogue + synthesized per-scene music bed (ducked under speech) + SFX -> /home/claude/lf02/mix.wav"""
import json, subprocess, numpy as np, os, wave
SR = 48000
D = "/home/claude/lf02"; A = "/home/user/cyto-uploads/audio"
rng = np.random.default_rng(7)


def load(path):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).copy()
    return x


def env(n, a=.005, r=.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)


def tone(f, d, kind="sine", a=.005, r=.2, vib=0):
    t = np.arange(int(d * SR)) / SR
    ph = 2 * np.pi * (f * t + (vib * np.sin(2 * np.pi * 5 * t) / 5 if vib else 0))
    w = np.sin(ph) if kind == "sine" else (np.sign(np.sin(ph)) * .5 if kind == "sq" else 2 * (t * f % 1) - 1)
    return w * env(len(t), a, r)


def noise(d, lo=None, hi=None, r=.1, a=.002):
    n = int(d * SR); x = rng.standard_normal(n)
    if lo or hi:
        F = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
        F[(f < (lo or 0)) | (f > (hi or SR))] = 0; x = np.fft.irfft(F, n)
    return x / (np.abs(x).max() + 1e-9) * env(n, a, r)


def sweep(f0, f1, d, kind="sine", r=None):
    t = np.arange(int(d * SR)) / SR; f = f0 + (f1 - f0) * t / d
    ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sin(ph) if kind == "sine" else np.sign(np.sin(ph)) * .5
    return w * (env(len(t), .005, r) if r else np.minimum(1, t / .01) * np.minimum(1, (d - t) / .03))


cat = lambda *xs: np.concatenate(xs)


def M(a, b):
    n = max(len(a), len(b)); y = np.zeros(n); y[:len(a)] += a; y[:len(b)] += b; return y

SYN = {
    "buzz": lambda: (np.sign(np.sin(2 * np.pi * 180 * np.arange(int(.35 * SR)) / SR)) * .4 * (np.sin(2 * np.pi * 22 * np.arange(int(.35 * SR)) / SR) > 0)),
    "whoosh": lambda: noise(.45, 300, 3000, r=.18, a=.15),
    "hit": lambda: M(noise(.3, 40, 500, r=.12), tone(60, .4, r=.15)),
    "kick": lambda: M(noise(.25, 60, 1200, r=.06), sweep(140, 50, .3, r=.08)),
    "blip": lambda: tone(1320, .12, "sq", r=.06),
    "zap": lambda: sweep(1800, 200, .35, "sq") * .6,
    "boing": lambda: sweep(220, 520, .35, r=.2) * np.sin(2 * np.pi * 9 * np.arange(int(.35 * SR)) / SR),
    "buzzer": lambda: tone(110, .5, "saw", a=.01, r=1) * .5,
    "catch": lambda: noise(.12, 100, 2000, r=.03),
    "roar": lambda: noise(.9, 60, 500, r=.5, a=.1) * 1.2,
    "pop": lambda: sweep(400, 1200, .08, r=.04),
    "radio": lambda: M(noise(.5, 1500, 4000, r=.3) * .5, tone(1000, .1, "sq")),
    "rain": lambda: noise(14, 2000, 9000, r=99, a=1) * .5,
    "typewriter": lambda: cat(*[cat(noise(.03, 2000, 8000, r=.01), np.zeros(int(.04 * SR))) for _ in range(14)]),
    "click": lambda: noise(.04, 2000, 9000, r=.01),
    "drip": lambda: sweep(800, 1800, .1, r=.05),
    "stamp": lambda: M(noise(.15, 50, 900, r=.05), tone(90, .2, r=.06)),
    "slam": lambda: M(noise(.4, 40, 1200, r=.1), tone(55, .5, r=.15)),
    "clunk": lambda: M(tone(140, .25, "sq", r=.06), noise(.15, 200, 2000, r=.04)),
    "static": lambda: noise(3.2, 500, 9000, r=99, a=.05) * .5,
    "coin": lambda: cat(tone(988, .08, "sq", r=1), tone(1319, .3, "sq", r=.15)),
    "levelup": lambda: cat(*[tone(f, .09, "sq", r=1) for f in (523, 659, 784, 1047)], tone(1319, .35, "sq", r=.2)),
    "inhale": lambda: noise(1.6, 300, 2500, r=99, a=.8) * np.linspace(.2, 1, int(1.6 * SR)) * .4,
    "yawn": lambda: sweep(300, 180, 1.0, r=.6) * .5,
    "skate": lambda: noise(1.2, 3000, 9000, r=.6, a=.1) * .5,
    "rip": lambda: noise(.35, 1000, 6000, r=.25, a=.05),
    "slap": lambda: noise(.12, 300, 5000, r=.03),
    "sniff": lambda: cat(noise(.18, 1000, 5000, r=.1, a=.05), np.zeros(int(.1 * SR)), noise(.25, 1000, 5000, r=.12, a=.05)) * .5,
    "powerdown": lambda: sweep(600, 60, .9, "sq") * .5,
    "gulp": lambda: sweep(300, 120, .18, r=.1),
    "tiptoe": lambda: cat(*[cat(tone(900, .05, r=.02), np.zeros(int(.25 * SR))) for _ in range(6)]) * .6,
    "tap": lambda: cat(noise(.05, 1000, 5000, r=.01), np.zeros(int(.12 * SR)), noise(.05, 1000, 5000, r=.01)),
    "flip": lambda: cat(*[noise(.04, 800, 6000, r=.01) for _ in range(4)]),
    "sting": lambda: sum(tone(f, .8, "saw", r=.4) for f in (196, 233, 277)) * .3,
}
FILES = {"siren": "lf02_sfx_siren.mp3", "crowd": "lf02_sfx_crowd.mp3", "cheer": "lf02_sfx_crowd.mp3", "shatter": "lf02_sfx_shatter.mp3",
         "sax": "lf02_sfx_sax.mp3", "achoo": "lf02_sfx_achoo.mp3", "chirp": "lf02_sfx_chirp.mp3"}
cache = {}


def sfx(name):
    if name in cache: return cache[name]
    if name == "sip":
        import sys; sys.path.insert(0, "/home/claude/hf"); import cyto3 as R
        if not os.path.exists(R.SIP_WAV): R.make_sip()
        x = load(R.SIP_WAV)
    elif name == "siren_short":
        x = sfx("siren")[:int(1.2 * SR)].copy(); x[-2000:] *= np.linspace(1, 0, 2000)
    elif name in FILES and os.path.exists(f"{A}/{FILES[name]}"):
        x = load(f"{A}/{FILES[name]}")
        if name == "chirp": x = x[:int(1.0 * SR)]
    elif name in SYN:
        x = SYN[name]().astype(np.float32)
    else:
        x = SYN["whoosh"]().astype(np.float32)
    x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9)          # unit RMS
    cache[name] = x.astype(np.float32); return cache[name]


# ---------------------------------------------------------------- music beds (synth, loopable)
def drums(bpm, bars, kick=(0, 2), snare=(1, 3), hat=8, swing=0):
    beat = 60 / bpm; n = int(bars * 4 * beat * SR); y = np.zeros(n)
    K = (sweep(120, 45, .25, r=.08)).astype(np.float32); Sn = noise(.18, 200, 6000, r=.05); Hh = noise(.05, 6000, 12000, r=.015) * .5
    for b in range(bars * 4):
        t0 = b * beat
        for s, smp in ((kick, K), (snare, Sn)):
            if b % 4 in s:
                i = int(t0 * SR); y[i:i + len(smp)] += smp[:max(0, n - i)]
        for h in range(hat // 4):
            i = int((t0 + h * beat / (hat // 4) + (swing * beat / 4 if h % 2 else 0)) * SR); y[i:i + len(Hh)] += Hh[:max(0, n - i)]
    return y


def chords(prog, bpm, kind="sine", oct_=1, dur_beats=4, r=1.2, arp=False):
    beat = 60 / bpm; y = []
    for ch in prog:
        if arp:
            seg = np.concatenate([tone(f * oct_, beat / 2, kind, r=.15) for _ in range(dur_beats // 2) for f in ch[:2]] + [np.zeros(1)])
            seg = np.concatenate([tone(ch[i % len(ch)] * oct_, beat / 4, kind, r=.1) for i in range(dur_beats * 4)])
        else:
            seg = sum(tone(f * oct_, dur_beats * beat, kind, a=.05, r=r) for f in ch) / len(ch)
        y.append(seg)
    return np.concatenate(y)


def bass(notes, bpm, per=1, kind="sine", r=.25):
    beat = 60 / bpm
    return np.concatenate([tone(f, beat * per, kind, r=r) for f in notes])


def fit(x, n):
    reps = int(np.ceil(n / len(x))); return np.tile(x, reps)[:n]


Am, F, C, G, Dm, E = [220, 262, 330], [175, 220, 262], [262, 330, 392], [196, 247, 294], [147, 175, 220], [165, 208, 247]


def bed(kind, d):
    n = int(d * SR)
    if kind == "cozy":
        y = fit(chords([F, Am, C, G], 80, r=2.5), n) * .8 + fit(drums(80, 4, hat=8, swing=.3), n) * .25
    elif kind in ("alarm", "alarm_low"):
        t = np.arange(n) / SR
        y = np.sin(2 * np.pi * 55 * t) * (.6 + .4 * np.sin(2 * np.pi * 1.4 * t)) + fit(drums(120, 4, kick=(0, 1, 2, 3), snare=(), hat=0), n) * .5
        y *= .7 if kind == "alarm_low" else 1
    elif kind in ("intro", "outro"):
        y = fit(drums(96, 4, hat=8, swing=.2), n) * .5 + fit(bass([110, 110, 131, 98] * 2, 96, per=2, kind="saw", r=.3), n) * .25 + fit(chords([Am, F, C, G], 96, r=1.5), n) * .5
    elif kind == "court":
        y = fit(drums(92, 4, kick=(0, 2, 3), hat=16, swing=.1), n) * .6 + fit(bass([82, 82, 98, 73] * 2, 92, per=2, kind="saw", r=.25), n) * .35
    elif kind == "moody":
        y = fit(chords([Dm, Am, F, E], 70, r=3), n) * .7 + fit(drums(70, 4, kick=(0,), snare=(2,), hat=4), n) * .2
    elif kind == "heist":
        y = fit(bass([110, 0.1, 131, 0.1, 147, 0.1, 131, 0.1] * 2, 130, per=.5, kind="sq", r=.08), n) * .4 + fit(drums(130, 2, kick=(0, 2), snare=(), hat=8), n) * .3
    elif kind == "noir":
        y = fit(bass([98, 110, 123, 131, 147, 131, 123, 110], 84, per=1, r=.35), n) * .6 + fit(drums(84, 4, kick=(), snare=(1, 3), hat=12, swing=.4), n) * .2 \
            + fit(chords([[196, 247, 349], [220, 262, 392]], 84, r=2.5), n) * .3
    elif kind == "calm":
        y = fit(chords([C, Am, F, G], 60, r=4), n) * .8
    elif kind == "game":
        y = fit(chords([C, Am, F, G], 120, kind="sq", oct_=2, arp=True), n) * .25 + fit(drums(120, 4, hat=8), n) * .35 + fit(bass([131, 110, 87, 98], 120, per=4, kind="sq", r=.4), n) * .2
    else:   # quiet
        y = fit(chords([C, G], 50, r=5), n) * .25
    y = np.asarray(y, np.float64)
    return y / (np.sqrt(np.mean(y ** 2)) + 1e-9)


# ---------------------------------------------------------------- mix
dlg = load(f"{D}/dialogue.wav"); N = len(dlg) + SR
out = np.zeros(N); out[:len(dlg)] += dlg
vr = np.sqrt(np.mean(dlg[np.abs(dlg) > .01] ** 2))
ev = json.load(open(f"{D}/events.json"))
music = sorted({tuple(m) for v in ev.values() for m in v["music"]})
# speech envelope for ducking
fr = SR // 50; e = np.array([np.sqrt(np.mean(dlg[i:i + fr] ** 2)) for i in range(0, len(dlg), fr)])
act = np.convolve((e > vr * .25).astype(float), np.ones(15) / 15, "same") > 0
duck = np.repeat(np.where(act, .5, 1.0), fr)[:N]; duck = np.pad(duck, (0, N - len(duck)), constant_values=1)
duck = np.convolve(duck, np.ones(2400) / 2400, "same")
MUS_DB = {"quiet": -34, "calm": -27, "noir": -24}
for t0, t1, kind in music:
    i0, i1 = int(t0 * SR), min(N, int(t1 * SR)); b = bed(kind, (i1 - i0) / SR)[:i1 - i0]
    fade = int(.15 * SR); b[:fade] *= np.linspace(0, 1, fade); b[-fade:] *= np.linspace(1, 0, fade)
    out[i0:i1] += b * vr * 10 ** (MUS_DB.get(kind, -22) / 20) * duck[i0:i1]
for v in ev.values():
    for t, name, g in v["sfx"]:
        x = sfx(name); i = int(t * SR)
        if i >= N: continue
        seg = x[:N - i] * vr * 10 ** ((-14 + g) / 20)
        out[i:i + len(seg)] += seg
out = out / max(1e-9, np.abs(out).max()) * .95
with wave.open(f"{D}/mix_raw.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/mix_raw.wav", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", f"{D}/mix.wav"], check=True)
print("mix", N / SR, "s; music segs", len(music))
