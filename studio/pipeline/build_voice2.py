"""python3 build_voice2.py <dir>  — reads <dir>/raw.mp3 and <dir>/segs.json, writes voice.wav + timing.json"""
import subprocess, json, re, sys, os, numpy as np
D = sys.argv[1]; SR = 44100
cfg = json.load(open(os.path.join(D, "segs.json")))
SEG, TEMPO = cfg["segs"], cfg.get("tempo", 1.0)
raw = subprocess.run(["ffmpeg","-v","error","-i",os.path.join(D,"raw.mp3"),"-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True,check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32)/32768
dur = len(x)/SR
PRE, POST, LINE_GAP, IN_GAP, LEAD = 0.03, 0.06, 0.26, 0.11, 0.12
def syl(w):
    w = re.sub(r"[^a-z0-9]", "", w.lower().replace("pov","peeohvee"))
    if w.isdigit(): return {"2": 1, "23": 4}.get(w, len(w))
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(1, n)
out, words, segs, t = [np.zeros(int(LEAD*SR), np.float32)], [], [], LEAD
for i,(a,b,li,ph) in enumerate(SEG):
    b = min(b, dur)
    a2, b2 = max(0, a-PRE), min(dur, b+POST)
    ch = x[int(a2*SR):int(b2*SR)].copy(); f = int(0.01*SR); ch[:f] *= np.linspace(0,1,f); ch[-f:] *= np.linspace(1,0,f)
    s0 = t + (a - a2); s1 = s0 + (b - a)
    ws = ph.split(); ss = [syl(w) for w in ws]; tot = sum(ss); c = 0
    for w, s_ in zip(ws, ss):
        words.append(dict(line=li, w=w, t0=s0+(s1-s0)*c/tot, t1=s0+(s1-s0)*(c+s_)/tot)); c += s_
    segs.append((s0, s1, li)); out.append(ch); t += len(ch)/SR
    if i+1 < len(SEG):
        g = LINE_GAP if SEG[i+1][2] != li else IN_GAP
        out.append(np.zeros(int(g*SR), np.float32)); t += g
out.append(np.zeros(int(0.08*SR), np.float32))
y = np.concatenate(out)
subprocess.run(["ffmpeg","-y","-v","error","-f","s16le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={TEMPO}","-ar",str(SR),os.path.join(D,"voice.wav")],
               input=(np.clip(y,-1,1)*32767).astype(np.int16).tobytes(), check=True)
k = 1/TEMPO
for w in words: w["t0"]*=k; w["t1"]*=k
json.dump(dict(words=words, segs=[(a*k,b*k,l) for a,b,l in segs], total=len(y)/SR*k), open(os.path.join(D,"timing.json"),"w"), indent=0)
print(D, "total", round(len(y)/SR*k, 2))
