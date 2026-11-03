"""LF02 dialogue assembly: cut every line out of the 4 ElevenLabs takes (Scribe word timings) and sequence them
in script order with comedy timing + silent action beats.  Writes:
  /home/claude/lf02/dialogue.wav   (48 kHz mono)
  /home/claude/lf02/timing.json    {"T":..., "lines":[{n,who,t0,t1,text,words:[{w,t0,t1}]}], "beats":{name:[t0,t1]}}
Captions use the real spellings from lines.json "text" (wys fam, ahlie, 6ix), timings come from the TTS words.
"""
import json, re, subprocess, numpy as np, os

D = "/home/claude/lf02"
LINES = json.load(open("/root/cyto-uploads/studio/episodes/lf02/lines.json"))
SR = 48000
TAKES = {"cyto1": "lf02_cyto1", "cyto2": "lf02_cyto2", "neutro": "lf02_neutro", "mito": "lf02_mito"}
CAP_OVERRIDE = {14: "Wys fam! Let's run it!", 6: None}


def load(name):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{D}/{name}.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).copy()
    return x


norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("1", "one"))

# ---------- 1. map each line to its take + word span
audio, words = {}, {}
for k, f in TAKES.items():
    audio[k] = load(f)
    words[k] = [w for w in json.load(open(f"{D}/lf02_words_{k}.json"))["words"] if w.get("type", "word") == "word"]
ptr = {k: 0 for k in TAKES}
cyto_split = 35            # cyto1 holds Cyto's lines up to n=35 ("On PURPOSE?")
cut = {}
for L in LINES:
    if not norm(L["tts"]):       # silent "…" lines
        continue
    k = L["who"].lower() if L["who"] != "CYTO" else ("cyto1" if L["n"] <= cyto_split else "cyto2")
    toks = L["tts"].split()
    span = words[k][ptr[k]:ptr[k] + len(toks)]
    assert [norm(t) for t in toks] == [norm(w["text"]) for w in span], (L["n"], toks, [w["text"] for w in span])
    ptr[k] += len(toks)
    cut[L["n"]] = (k, span)
for k in TAKES: assert ptr[k] == len(words[k]), (k, ptr[k], len(words[k]))

# ---------- 2. episode running order: ("L", n, gap_before) or ("B", name, seconds of silent action)
F, P = 0.25, 0.6          # fast banter gap, punchline gap
ORDER = [
    ("L", 1, 0.5), ("B", "alarm", 1.3), ("L", 2, 0.15), ("L", 3, F), ("L", 4, 0.45), ("L", 5, 0.7), ("B", "title", 2.6),
    ("B", "fly", 1.0), ("L", 6, 0.2), ("B", "to_report", 0.8),
    ("L", 7, 0.3), ("L", 8, 0.55), ("L", 9, 0.55), ("L", 10, 0.55), ("L", 11, P), ("L", 12, 0.35), ("B", "to_condos", 2.2),
    ("L", 13, 0.3), ("L", 14, F), ("L", 15, 0.35), ("L", 16, 0.3), ("L", 17, 0.35), ("L", 18, 0.15), ("B", "dunk", 3.0),
    ("L", 19, 0.3), ("L", 20, 0.35), ("L", 21, P), ("L", 22, 0.7), ("B", "subbed", 1.5), ("L", 23, 0.2), ("L", 24, F), ("L", 25, 0.5),
    ("B", "countdown", 1.6), ("L", 26, 0.2), ("B", "bench", 0.6), ("L", 27, 0.2), ("L", 28, 0.5), ("B", "crumb", 1.1), ("L", 29, 0.1),
    ("L", 30, P), ("L", 31, 0.5), ("L", 32, 0.6), ("B", "heist", 3.0),
    ("B", "noir", 1.6), ("L", 33, 0.2), ("L", 34, 0.5), ("L", 35, 0.35), ("L", 36, 0.3), ("B", "reenact", 2.0), ("L", 37, 0.2),
    ("L", 38, 0.5), ("L", 39, 0.5), ("B", "silence", 1.2), ("L", 40, 0.0), ("L", 41, 0.6), ("L", 42, 0.5), ("B", "smirk", 1.4),
    ("L", 43, 0.4), ("L", 44, 0.3), ("B", "seccam", 3.2), ("L", 45, 0.0), ("L", 46, 0.0), ("L", 47, 0.0),
    ("B", "to_heart", 1.6), ("L", 48, 0.3), ("L", 49, 0.4), ("L", 50, 0.35),
    ("B", "to_cheats", 0.8), ("L", 51, 0.3), ("L", 52, 0.5), ("B", "breathe", 1.8), ("L", 53, 0.4), ("L", 54, 0.35), ("L", 55, 0.3),
    ("L", 56, 0.5), ("B", "sidequest", 1.3), ("L", 57, 0.4), ("B", "mute", 1.4),
    ("B", "chirp", 1.8), ("L", 58, 0.0), ("L", 59, 0.4), ("L", 60, 0.45), ("B", "spot", 1.0), ("L", 61, 0.2), ("B", "achoo", 2.6),
    ("L", 62, 0.1), ("L", 63, 0.3),
    ("B", "breakstarts", 1.4), ("L", 64, 0.2), ("L", 65, 0.4), ("L", 66, 0.5), ("B", "end", 1.8),
]
SILENT_HOLD = {45: 0.9, 46: 0.9}      # the twist's "…" reaction holds (no audio)

# ---------- 3. assemble
out, t, lines_out, beats = [], 0.0, [], {}
def pad(sec):
    out.append(np.zeros(int(round(sec * SR)), np.float32))

TARGET = 0.085   # per-line RMS match so the three voices sit at one level
for item in ORDER:
    kind, key, g = item
    if kind == "B":
        beats[key] = [round(t, 3), round(t + g, 3)]; pad(g); t += g; continue
    pad(g); t += g
    L = next(l for l in LINES if l["n"] == key)
    if key in SILENT_HOLD:
        d = SILENT_HOLD[key]
        lines_out.append(dict(n=key, who=L["who"], t0=round(t, 3), t1=round(t + d, 3), text=L["text"], words=[]))
        pad(d); t += d; continue
    k, span = cut[key]
    a0, a1 = max(0, span[0]["start"] - 0.05), span[-1]["end"] + 0.14
    seg = audio[k][int(a0 * SR):int(a1 * SR)].copy()
    rms = np.sqrt(np.mean(seg ** 2)) + 1e-9
    seg *= min(3.0, TARGET / rms)
    fade = int(0.012 * SR); seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    # caption words: real spelling, TTS timing
    tw = [dict(w=w["text"], t0=round(t + w["start"] - a0, 3), t1=round(t + w["end"] - a0, 3)) for w in span]
    cap = (CAP_OVERRIDE.get(key) or L["text"]).replace("the six", "the 6ix").split()
    if len(cap) == len(tw):
        cw = [dict(w, w=c) for w, c in zip(tw, cap)]
    elif key == 14:   # "Waaah you sayinnn, fam!" (4 TTS words) -> "Wys fam!" (2)
        cw = [dict(w=cap[0], t0=tw[0]["t0"], t1=tw[2]["t1"]), dict(tw[3], w=cap[1])] + [dict(w, w=c) for w, c in zip(tw[4:], cap[2:])]
    else:
        raise SystemExit(f"caption/tts word mismatch line {key}: {cap} vs {[w['w'] for w in tw]}")
    lines_out.append(dict(n=key, who=L["who"], t0=round(t, 3), t1=round(t + len(seg) / SR, 3), text=" ".join(cap), words=cw))
    out.append(seg); t += len(seg) / SR

y = np.concatenate(out)
y = y / max(1e-9, np.abs(y).max()) * 0.89
import wave
with wave.open(f"{D}/dialogue.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())
T = round(len(y) / SR, 3)
json.dump(dict(T=T, lines=lines_out, beats=beats), open(f"{D}/timing.json", "w"), indent=1)
print(f"T = {T:.2f}s ({int(T // 60)}:{T % 60:04.1f}), {len(lines_out)} lines, {len(beats)} beats")
