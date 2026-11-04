"""LF02 dialogue assembly (FIX pass, Nov 2026): cut every line out of the 4 ElevenLabs takes (Scribe word timings)
and lay them on ONE timeline with conversation-style handoffs.  Writes:
  /home/claude/lf02/dialogue.wav   (48 kHz mono, voices only, shared room reverb, per-line LUFS match)
  /home/claude/lf02/timing.json    {"T", "lines":[{n,who,t0,t1,text,words,kind}], "beats":{name:[t0,t1]}}
timing.json t0/t1 = SPEECH start/end (first word start / last word end), so speaker-change gaps read off directly.

Handoff rules (see SETUP.md "LF02 fix lessons"):
  cut      = first word -0.03s .. last word +0.05s (pushed to the energy valley if the take still rings), 6 ms fades
  R reply  = 0.14s   F fast banter = 0.05s   O overlap/interrupt = -0.08s (tail of the interrupted line ducked -6 dB)
  P punchline setup = 0.42s   H "..." reaction hold = 0.58s   S same speaker continues = 0.30s  L list item = 0.36s
  beats    = silent action, <=1.0s speaker-to-speaker, dunk/heist/seccam/achoo <=2.0s (filled with SFX/music in mix.py)
"""
import json, re, subprocess, numpy as np, os, wave
import pyloudnorm as pyln
from scipy.signal import fftconvolve, butter, sosfilt

D = "/home/claude/lf02"
LINES = json.load(open("/home/user/cyto-uploads/studio/episodes/lf02/lines.json"))
SR = 48000
TAKES = {"cyto1": "lf02_cyto1", "cyto2": "lf02_cyto2", "cyto3": "lf02v3_cyto3", "neutro": "lf02v3_neutro", "mito": "lf02_mito"}
WORDS = {"cyto1": "lf02_words_cyto1", "cyto2": "lf02_words_cyto2", "cyto3": "words_cyto3", "neutro": "words_neutro_v3", "mito": "lf02_words_mito"}   # v3: NEW Neutro take (old voice retired)
CAP_OVERRIDE = {14: "Wys fam! Let's run it!", 6: None}


def load(name):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{D}/{name}.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, np.float32).astype(np.float64)


norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("1", "one"))

# ---------- 1. map each line to its take + word span
audio, words = {}, {}
for k, f in TAKES.items():
    audio[k] = load(f)
    words[k] = [w for w in json.load(open(f"{D}/{WORDS[k]}.json"))["words"] if w.get("type", "word") == "word"]
ptr = {k: 0 for k in TAKES}
cyto_split = 35
cut = {}
for L in LINES:   # list order = take order
    if not norm(L["tts"]):
        continue
    k = L.get("take") or (L["who"].lower() if L["who"] != "CYTO" else ("cyto1" if L["n"] <= cyto_split else "cyto2"))
    toks = L["tts"].split()
    span = words[k][ptr[k]:ptr[k] + len(toks)]
    assert [norm(t) for t in toks] == [norm(w["text"]) for w in span], (L["n"], toks, [w["text"] for w in span])
    ptr[k] += len(toks)
    cut[L["n"]] = (k, span)
for k in TAKES: assert ptr[k] == len(words[k]), (k, ptr[k], len(words[k]))

# ---------- 2. running order. ("L", n, handoff kind) / ("B", name, seconds of action between the two speeches)
GAP = {"R": .14, "F": .06, "O": -.08, "P": .42, "H": .58, "S": .30, "L": .36, "J": .0}
# v3 running order: every location change is a named beat (walk-out + subway doors + 0.6-0.8 s establishing wide w/ title card)
ORDER = [
    ("L", 1, "J"), ("L", 2, "P"), ("L", 3, "F"), ("L", 4, "P"), ("L", 5, "H"),
    ("B", "title", .80), ("L", 6, "J"),
    ("B", "to_report", 1.15), ("L", 7, "J"), ("L", 8, "L"), ("L", 9, "L"), ("L", 10, "L"), ("L", 11, "R"), ("L", 12, "F"),
    ("L", 67, "R"),                                   # N1 "That's the evidence... Follow me."
    ("B", "to_court", 1.85), ("L", 13, "J"),          # walk out -> doors -> court establishing + title card
    ("L", 14, "R"), ("L", 15, "R"), ("L", 16, "S"), ("L", 17, "S"), ("L", 18, "F"),
    ("B", "dunk", 1.80), ("L", 19, "J"), ("L", 20, "R"), ("L", 21, "F"), ("L", 22, "H"),
    ("B", "subbed", .75), ("L", 23, "J"), ("L", 24, "O"), ("L", 25, "F"),
    ("B", "n2walk", .45), ("L", 68, "J"),             # N2 "That was one bad day. Now make it a month." (Neutro walks in)
    ("B", "to_bench", 1.60), ("L", 26, "J"), ("B", "bench", .40), ("L", 27, "J"), ("L", 28, "R"),
    ("B", "crumb", .75), ("L", 29, "J"), ("L", 30, "F"), ("L", 31, "F"), ("L", 32, "R"),
    ("B", "heist", 1.50), ("L", 69, "J"),             # C-bridge "Wait. Hold up. Has this happened before?"
    ("B", "noir", 1.35), ("L", 33, "J"), ("L", 34, "S"), ("L", 35, "O"), ("L", 36, "F"),
    ("B", "reenact", .85), ("L", 37, "J"), ("L", 38, "S"), ("L", 39, "S"),
    ("B", "silence", .75), ("L", 40, "J"), ("L", 41, "P"), ("L", 42, "R"),
    ("B", "smirk", .62), ("B", "to_hq", 1.20), ("L", 43, "J"), ("L", 44, "R"),
    ("B", "seccam", 1.80), ("L", 45, "J"), ("L", 46, "J"), ("L", 47, "J"),
    ("B", "to_heart", 1.25), ("L", 48, "J"), ("L", 49, "S"), ("L", 50, "R"),
    ("B", "to_recap", 1.25), ("L", 70, "J"),          # C-recap: CASE board, all clues ticked
    ("L", 51, "S"), ("L", 52, "S"), ("B", "breathe", .85), ("L", 53, "J"), ("L", 54, "R"), ("L", 55, "F"),
    ("B", "to_city", 1.15), ("L", 56, "J"), ("B", "sidequest", .85), ("B", "to_hq3", 1.15), ("L", 57, "J"),
    ("B", "mute", .80), ("B", "chirp", .90), ("L", 58, "J"), ("L", 59, "R"), ("L", 60, "P"),
    ("B", "spot", .75), ("L", 61, "J"), ("B", "achoo", 1.60), ("L", 62, "J"), ("L", 63, "R"),
    ("B", "breakstarts", .75), ("L", 64, "J"), ("L", 65, "R"), ("L", 66, "S"), ("B", "end", 1.6),
]
SILENT_HOLD = {45: 0.9, 46: 0.9}      # the twist's "…" reaction holds (no audio)
BEAT_PAD = (.06, .08)                 # beat interval starts 0.06 after the speech; next speech 0.08 after the beat


def edb(x, i, win=int(.012 * SR)):
    i = int(min(max(i, win), len(x) - win)); s = x[i - win // 2:i + win // 2]
    return 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-9)


def trim(x, w0, w1, lo=0.0, hi=1e9):
    """sample bounds: first word -0.03 .. last word +0.05, pushed to the energy valley if speech still rings."""
    peak = 20 * np.log10(np.abs(x[int(w0 * SR):int(w1 * SR)]).max() + 1e-9)
    thr = peak - 30
    a = int((w0 - .03) * SR); back = 0
    while edb(x, a - 120) > thr and back < .06:   # Scribe starts can be late on soft consonants
        a -= 240; back += 240 / SR
    b = int((w1 + .05) * SR); ext = 0
    while edb(x, b) > thr and ext < .10:          # tail still ringing (Scribe ends early on "-s", "-ff")
        b += 240; ext += 240 / SR
    b = min(range(b - int(.02 * SR), b + int(.03 * SR), 120), key=lambda i: edb(x, i))   # local valley
    b = max(b, int((w1 + .03) * SR))
    # never leak the neighbouring line of the take: stay inside the valley between words
    if hi < 1e8:
        hb = int((hi - .012) * SR)
        if b > hb: b = min(range(int(w1 * SR), max(int(w1 * SR) + 1, hb), 60), key=lambda i: edb(x, i, int(.006 * SR))) if hb > int(w1 * SR) else hb
    a = max(a, int((lo + .012) * SR)) if lo else a
    return max(0, a), min(len(x), b)


meter = pyln.Meter(SR, block_size=0.2)
TARGET_LUFS = -21.0


def lufs_match(seg):
    l = None
    if len(seg) > .25 * SR:
        try: l = meter.integrated_loudness(seg)
        except Exception: l = None
    if l is None or not np.isfinite(l):
        l = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) - 3.0
    return seg * min(10 ** ((TARGET_LUFS - l) / 20), 4.0), l


# ---------- 3. lay out on one timeline
segs, lines_out, beats = [], [], {}
t_end, pending_beat = 0.25, 0.0      # first word at 0.25 s (the alarm drop + room tone are already rolling)
fade = int(.006 * SR)
for kind, key, g in ORDER:
    if kind == "B":
        b0 = t_end + (BEAT_PAD[0] if pending_beat == 0 else 0)
        beats[key] = [round(b0, 3), round(b0 + g, 3)]
        t_end = b0 + g; pending_beat += g; continue
    L = next(l for l in LINES if l["n"] == key)
    start = t_end + (BEAT_PAD[1] if pending_beat else (0 if not lines_out else GAP[g]))
    pending_beat = 0.0
    if key in SILENT_HOLD:
        d = SILENT_HOLD[key]
        lines_out.append(dict(n=key, who=L["who"], t0=round(start, 3), t1=round(start + d, 3), text=L["text"], words=[], kind=g))
        t_end = start + d; continue
    k, span = cut[key]
    w0, w1 = span[0]["start"], span[-1]["end"]
    i_s = words[k].index(span[0]); i_e = words[k].index(span[-1])
    lo = words[k][i_s - 1]["end"] if i_s > 0 else 0.0
    hi = words[k][i_e + 1]["start"] if i_e + 1 < len(words[k]) else 1e9
    a, b = trim(audio[k], w0, w1, lo, hi)
    seg, lu = lufs_match(audio[k][a:b].copy())
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    off = start - (w0 - a / SR)
    tw = [dict(w=w["text"], t0=round(start + w["start"] - w0, 3), t1=round(start + w["end"] - w0, 3)) for w in span]
    cap = (CAP_OVERRIDE.get(key) or L["text"]).replace("the six", "the 6ix").split()
    if len(cap) == len(tw):
        cw = [dict(w, w=c) for w, c in zip(tw, cap)]
    elif key == 14:
        cw = [dict(w=cap[0], t0=tw[0]["t0"], t1=tw[2]["t1"]), dict(tw[3], w=cap[1])] + [dict(w, w=c) for w, c in zip(tw[4:], cap[2:])]
    else:
        raise SystemExit(f"caption/tts word mismatch line {key}: {cap} vs {[w['w'] for w in tw]}")
    if g == "O" and segs:                # interruption: duck the interrupted tail -6 dB from the overlap point
        po, pseg = segs[-1]
        i0 = int((start - .02 - po) * SR)
        if 0 < i0 < len(pseg):
            r = np.ones(len(pseg)); ramp = min(int(.03 * SR), len(pseg) - i0)
            r[i0:i0 + ramp] = np.linspace(1, .5, ramp); r[i0 + ramp:] = .5
            segs[-1] = (po, pseg * r)
    segs.append((off, seg))
    s1 = round(start + w1 - w0, 3)
    lines_out.append(dict(n=key, who=L["who"], t0=round(start, 3), t1=s1, text=" ".join(cap), words=cw, kind=g,
                          cut=[round(off, 3), round(off + len(seg) / SR, 3)], lufs_in=round(lu, 1)))
    t_end = s1

T = round(max(t_end, max(o + len(s) / SR for o, s in segs)) + 0.02, 3)
y = np.zeros(int(T * SR) + SR)
for o, s in segs:
    i = int(round(o * SR)); y[i:i + len(s)] += s
y = y[:int(T * SR)]

# ---------- 4. ONE shared room on all three voices: short diffuse reverb, 0.25 s RT60, 4 % wet
rng = np.random.default_rng(3)
n = int(.25 * SR); tt = np.arange(n) / SR
ir = rng.standard_normal(n) * np.exp(-6.91 * tt / .25); ir[:int(.006 * SR)] = 0
wet = sosfilt(butter(2, [250, 6000], "bandpass", fs=SR, output="sos"), fftconvolve(y, ir)[:len(y)])
wet *= np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-9)
y = .96 * y + .04 * wet
y = y / max(1e-9, np.abs(y).max()) * 0.89
with wave.open(f"{D}/dialogue.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())
json.dump(dict(T=T, lines=lines_out, beats=beats), open(f"{D}/timing.json", "w"), indent=1)

# ---------- 5. report
gaps = [(round(b["t0"] - a["t1"], 3), a["n"], b["n"]) for a, b in zip(lines_out, lines_out[1:]) if a["who"] != b["who"]]
gs = sorted(x[0] for x in gaps)
print(f"T = {T:.2f}s ({int(T // 60)}:{T % 60:04.1f}), {len(lines_out)} lines, {len(beats)} beats; {len(gaps)} speaker changes, "
      f"median gap {np.median(gs):.3f}s, max {max(gs):.3f}s")
print("gaps > 0.5s:", [g for g in gaps if g[0] > .5])
