"""Ep12 U1: segs.json from silencedetect regions + ElevenLabs Scribe word times; after build_voice2, remap scribe times into timing.json."""
import json, sys, subprocess, re
D = "/home/claude/ep12"
W = json.load(open(f"{D}/words_scribe.json"))
# line index per word (scene lines): hook, catchphrase, stat, twist, cup-down, payoff, outro
LINE_START = {"Movember.": 0, "Yo,": 1, "Testicular": 2, "Now": 3, "But": None, "Grow": 5, "Like,": 6}
lines = []; cur = 0
for i, (w, a, b) in enumerate(W):
    if w == "Yo,": cur = 1
    elif w == "Testicular": cur = 2
    elif w == "Now": cur = 3
    elif w == "But" and a > 27: cur = 4
    elif w == "Grow": cur = 5
    elif w == "Like,": cur = 6
    lines.append(cur)
if sys.argv[1] == "segs":
    out = subprocess.run(["ffmpeg", "-i", f"{D}/raw.mp3", "-af", "silencedetect=n=-35dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = 42.762
    regions = []; a = 0.0
    for s, e in zip(ss, se):
        regions.append([a, s]); a = e
    regions.append([a, dur])
    if regions[-1][1] - regions[-1][0] < 0.1: regions[-2][1] = dur; regions.pop()
    segs = []
    for a, b in regions:
        idx = [i for i, (w, x, y) in enumerate(W) if a - 0.15 <= (x + y) / 2 <= b + 0.15]
        if not idx: continue
        # split a region if it spans two lines
        groups = {}
        for i in idx: groups.setdefault(lines[i], []).append(i)
        for li, ii in groups.items():
            segs.append([round(max(a, W[ii[0]][1] - 0.05) if len(groups) > 1 else a, 3), round(b if len(groups) == 1 else W[ii[-1]][2], 3), li, " ".join(W[i][0] for i in ii)])
    used = sorted(i for s in segs for i in range(len(W)) if False)
    assert sum(len(s[3].split()) for s in segs) == len(W), (sum(len(s[3].split()) for s in segs), len(W))
    json.dump(dict(tempo=1.0, line_gap=0.24, in_gap=0.12, segs=segs), open(f"{D}/segs.json", "w"), indent=1)
    for s in segs: print(s)
else:   # remap
    cfg = json.load(open(f"{D}/segs.json")); tm = json.load(open(f"{D}/timing.json"))
    k = 0; out = []
    for (a, b, li, ph), (s0, s1, _) in zip(cfg["segs"], tm["segs"]):
        for w in ph.split():
            ww, x, y = W[k]; assert ww == w
            out.append(dict(line=li, w=w, t0=round(s0 + (x - a), 3), t1=round(min(s1 + 0.05, s0 + (y - a)), 3))); k += 1
    tm["words"] = out; tm["word_source"] = "elevenlabs scribe_v1 word timestamps remapped through build_voice2 segment shifts"
    json.dump(tm, open(f"{D}/timing.json", "w"), indent=0); print("remapped", k, "words; total", round(tm["total"], 2))
