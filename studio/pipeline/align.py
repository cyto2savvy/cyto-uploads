import subprocess, re, json, numpy as np
SR = 44100
raw = subprocess.run(["ffmpeg","-v","error","-i","raw.mp3","-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True,check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32)/32768
dur = len(x)/SR
log = subprocess.run(["ffmpeg","-hide_banner","-i","raw.mp3","-af","silencedetect=noise=-35dB:d=0.15","-f","null","-"],capture_output=True,text=True).stderr
st = [float(v) for v in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(v) for v in re.findall(r"silence_end: ([0-9.]+)", log)]
gaps = list(zip(st, en))
# speech segments
segs, prev = [], 0.0
for a,b in gaps:
    if a > prev: segs.append((prev, a))
    prev = b
if prev < dur: segs.append((prev, dur))
LINES = [
 "POV: the beat drops, and your arms get goosebumps. Why though?",
 "Bro, every hair on you has its own tiny muscle. The arrector pili.",
 "Get cold or shook, and your fight-or-flight nerves fire. Faster than the TTC ever showed up.",
 "Muscle squeezes, hair stands up, skin bunches. That's the bump.",
 "Our ancestors were bare furry, so this puffed them up. Warmer, and looking way bigger.",
 "We lost the fur, so now it's a leftover glitch. No cap.",
 "But it styll goes off every time...",
]
def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower().replace("ttc","teeteecee").replace("pov","peeohvee"))
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(1, n)
words = [(li, w, syl(w)) for li, ln in enumerate(LINES) for w in ln.split()]
S = sum(s for _,_,s in words)
# map syllable position -> time through speech-only segments
seg_d = [b-a for a,b in segs]; T = sum(seg_d)
def t_at(frac):
    tgt = frac*T
    for (a,b),d in zip(segs, seg_d):
        if tgt <= d + 1e-9: return a + tgt
        tgt -= d
    return segs[-1][1]
# line boundaries snapped to nearest gap
cum = 0; line_end_syl = []
for li in range(len(LINES)):
    cum += sum(s for l,_,s in words if l == li); line_end_syl.append(cum)
gap_speech_before = []
acc = 0
for (a,b),d in zip(segs, seg_d):
    acc += d; gap_speech_before.append((acc, b))  # boundary after this segment
bounds = []
for li in range(len(LINES)-1):
    tgt = line_end_syl[li]/S*T
    best = min(gap_speech_before[:-1], key=lambda g: abs(g[0]-tgt))
    bounds.append(best)
print("line boundaries (speech-time target vs chosen):")
for li,(sp,tb) in enumerate(bounds): print(li, round(line_end_syl[li]/S*T,2), "->", round(sp,2), "at", round(tb,2))
# per-line word timings: syllables spread over that line's speech segments
line_ranges = []
start_sp = 0.0
for li in range(len(LINES)):
    end_sp = bounds[li][0] if li < len(bounds) else T
    line_ranges.append((start_sp, end_sp)); start_sp = end_sp
def sp_to_t(sp):
    return t_at(sp/T)
out = []
for li in range(len(LINES)):
    lw = [(w,s) for l,w,s in words if l == li]
    ls = sum(s for _,s in lw); a, b = line_ranges[li]
    c = 0
    for w,s in lw:
        t0 = sp_to_t(a + (b-a)*c/ls); c += s; t1 = sp_to_t(a + (b-a)*c/ls)
        out.append(dict(line=li, w=w, t0=t0, t1=t1))
json.dump(dict(words=out, gaps=gaps, segs=segs, dur=dur), open("align_raw.json","w"), indent=0)
for li in range(len(LINES)):
    ws = [o for o in out if o["line"]==li]
    print(li, round(ws[0]["t0"],2), round(ws[-1]["t1"],2), " ".join(f'{o["w"]}@{o["t0"]:.1f}' for o in ws))
