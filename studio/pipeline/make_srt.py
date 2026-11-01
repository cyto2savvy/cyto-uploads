"""Accurate captions file from the episode's word timings (YouTube's auto-captions mangle slang + names).
python3 make_srt.py /home/claude/epN [offset_s]  ->  epN/captions.srt   (upload in Studio → Subtitles → English → Upload file → With timing)
offset_s: seconds of video before the voice starts (default 0)."""
import json, sys, os

d = sys.argv[1]; off = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
W = json.load(open(os.path.join(d, "timing.json")))["words"]


def ts(t):
    t = max(0, t + off); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}"


cues, cur = [], []
for i, w in enumerate(W):
    cur.append(w)
    text = " ".join(x["w"] for x in cur)
    gap = W[i + 1]["t0"] - w["t1"] if i + 1 < len(W) else 9
    nxt = len(text) + 1 + len(W[i + 1]["w"]) if i + 1 < len(W) else 99
    if nxt > 34 or w["w"][-1] in ".?!" or gap > 0.35 or (w["line"] != W[i + 1]["line"] if i + 1 < len(W) else True):
        cues.append(cur); cur = []
if cur: cues.append(cur)

out = []
for n, c in enumerate(cues, 1):
    end = min(c[-1]["t1"] + 0.25, cues[n][0]["t0"] - 0.02) if n < len(cues) else c[-1]["t1"] + 0.6
    out.append(f"{n}\n{ts(c[0]['t0'])} --> {ts(end)}\n{' '.join(x['w'] for x in c)}\n")
p = os.path.join(d, "captions.srt"); open(p, "w").write("\n".join(out))
print(p, len(cues), "cues")
