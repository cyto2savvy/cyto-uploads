import subprocess, json, re, numpy as np
SR = 44100
raw = subprocess.run(["ffmpeg","-v","error","-i","raw.mp3","-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True,check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32)/32768
dur = len(x)/SR
# (start, end, line, phrase) — speech segments from silencedetect, matched to the script by length
SEG = [
 (0.00, 0.733, 0, "POV:"), (1.121, 3.672, 0, "the beat drops, and your arms get goosebumps."), (4.513, 5.150, 0, "Why though?"),
 (6.035, 6.411, 1, "Bro,"), (6.745, 9.525, 1, "every hair on you has its own tiny muscle."), (10.089, 10.822, 1, "The arrector"), (11.003, 11.536, 1, "pili."),
 (12.502, 15.590, 2, "Get cold or shook, and your fight-or-flight nerves fire."), (16.188, 18.438, 2, "Faster than the TTC ever showed up."),
 (19.366, 20.350, 3, "Muscle squeezes,"), (20.529, 22.798, 3, "hair stands up, skin bunches."), (23.017, 23.514, 3, "That's the"), (23.679, 24.182, 3, "bump."),
 (25.277, 27.117, 4, "Our ancestors were bare furry,"), (27.474, 28.557, 4, "so this puffed them up."), (29.016, 31.030, 4, "Warmer, and looking way bigger."),
 (31.985, 32.977, 5, "We lost the fur,"), (33.190, 34.948, 5, "so now it's a leftover glitch."), (35.196, 35.736, 5, "No cap."),
 (36.406, 37.670, 6, "But it styll goes off"), (37.929, 38.457, 6, "every"), (38.757, dur, 6, "time..."),
]
PRE, POST = 0.03, 0.06
LINE_GAP, IN_GAP, LEAD = 0.26, 0.11, 0.12
TEMPO = 1.10
def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower().replace("ttc","teeteecee").replace("pov","peeohvee"))
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(1, n)
out, words, t = [np.zeros(int(LEAD*SR), np.float32)], [], LEAD
seg_new = []
for i,(a,b,li,ph) in enumerate(SEG):
    a2, b2 = max(0, a-PRE), min(dur, b+POST)
    chunk = x[int(a2*SR):int(b2*SR)].copy()
    f = int(0.01*SR); chunk[:f] *= np.linspace(0,1,f); chunk[-f:] *= np.linspace(1,0,f)
    s_new = t + (a - a2); e_new = s_new + (b - a)
    ws = ph.split(); ss = [syl(w) for w in ws]; tot = sum(ss); c = 0
    for w,s in zip(ws, ss):
        words.append(dict(line=li, w=w, t0=s_new + (e_new-s_new)*c/tot, t1=s_new + (e_new-s_new)*(c+s)/tot)); c += s
    seg_new.append((s_new, e_new, li))
    out.append(chunk); t += len(chunk)/SR
    if i+1 < len(SEG):
        g = LINE_GAP if SEG[i+1][2] != li else IN_GAP
        out.append(np.zeros(int(g*SR), np.float32)); t += g
out.append(np.zeros(int(0.08*SR), np.float32))
y = np.concatenate(out)
pcm = (np.clip(y, -1, 1)*32767).astype(np.int16).tobytes()
subprocess.run(["ffmpeg","-y","-v","error","-f","s16le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={TEMPO}","-ar",str(SR),"voice.wav"],input=pcm,check=True)
k = 1/TEMPO
for w in words: w["t0"]*=k; w["t1"]*=k
seg_new = [(a*k,b*k,li) for a,b,li in seg_new]
total = len(y)/SR*k
json.dump(dict(words=words, segs=seg_new, total=total), open("timing.json","w"), indent=0)
print("total", round(total,2))
for li in range(7):
    ws=[w for w in words if w["line"]==li]; print(li, round(ws[0]["t0"],2), round(ws[-1]["t1"],2), " ".join(f'{w["w"]}@{w["t0"]:.2f}' for w in ws))
