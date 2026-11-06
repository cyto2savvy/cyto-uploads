"""Ep14: segs.json from silencedetect + Scribe words (lines by word index), then remap Scribe times into timing.json.
python3 make_segs.py segs ; python3 build_voice2.py /home/claude/ep14 ; python3 make_segs.py remap"""
import json, sys, subprocess, re
D = "/home/claude/ep14"
W = json.load(open(f"{D}/words_scribe.json"))
# line starts by word index: hook, catchphrase, research, dip, silence, payoff, lest we forget, disclaimer, outro
_k = [w for w, x, y in W]
def _at(word, after): return next(i for i in range(after, len(_k)) if _k[i] == word)
STARTS = [0, _at("Yo,", 0), _at("Researchers", 0), _at("In", 30), _at("Silence", 0), _at("So", 0), _at("Lest", 0), _at("Not", 0), _at("Like,", 0)]
lines = [max(k for k, s in enumerate(STARTS) if i >= s) for i in range(len(W))]
GAP_AFTER = {5: 0.5, 6: 1.0}          # after "...go quiet too." and after "Lest we forget." (a held moment)
if sys.argv[1] == "segs":
    out = subprocess.run(["ffmpeg", "-i", f"{D}/raw.mp3", "-af", "silencedetect=n=-45dB:d=0.15", "-f", "null", "-"], capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = 30.64
    segs = []
    for li in range(len(STARTS)):
        ii = [i for i in range(len(W)) if lines[i] == li]
        s0 = max(0.0, W[ii[0]][1] - 0.03)
        last = W[ii[-1]][1]
        nxt = W[ii[-1] + 1][1] - 0.03 if ii[-1] + 1 < len(W) else dur
        s1 = min([x for x in ss if x > last + 0.05] + [nxt, dur])
        segs.append([round(s0, 3), round(s1, 3), li, " ".join(W[i][0] for i in ii)])
    assert sum(len(s[3].split()) for s in segs) == len(W), (sum(len(s[3].split()) for s in segs), len(W))
    for k in range(len(segs) - 1):
        if segs[k + 1][2] != segs[k][2] and segs[k][2] in GAP_AFTER: segs[k].append(GAP_AFTER[segs[k][2]])
    json.dump(dict(tempo=1.0, lead=0.0, line_gap=0.22, in_gap=0.11, segs=segs), open(f"{D}/segs.json", "w"), indent=1)
    for s in segs: print(s)
else:
    cfg = json.load(open(f"{D}/segs.json")); tm = json.load(open(f"{D}/timing.json"))
    k = 0; out = []
    for (a, b, li, ph, *_), (s0, s1, _) in zip(cfg["segs"], tm["segs"]):
        for w in ph.split():
            ww, x, y = W[k]; assert ww == w
            out.append(dict(line=li, w=w, t0=round(max(0, s0 + (x - a)), 3), t1=round(min(s1 + 0.05, s0 + (y - a)), 3))); k += 1
    tm["words"] = out; tm["word_source"] = "elevenlabs scribe_v1 word timestamps remapped through build_voice2 segment shifts"
    json.dump(tm, open(f"{D}/timing.json", "w"), indent=0); print("remapped", k, "words; total", round(tm["total"], 2))
