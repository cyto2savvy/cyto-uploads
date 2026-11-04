"""LF02 v3 packaging: timing.json + captions.srt (re-timed to the v3 audio) + meta.json chapters/duration/photo credit +
pinned_comment.txt photo credits."""
import json, re, sys
sys.argv = [sys.argv[0]]
sys.path.insert(0, "/home/claude/hf/lf02")
import os; os.environ["NOBUILD"] = "1"
EP = "/home/user/cyto-uploads/studio/episodes/lf02"
TM = json.load(open("/home/claude/lf02/timing.json"))
json.dump(TM, open(f"{EP}/timing.json", "w"), indent=1)

# ---- captions.srt: one cue per phrase (sentence / clause), <= 42 chars, real spellings from timing words
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}".replace(",1000", ",999")
cues = []
for l in TM["lines"]:
    cur = []
    for i, w in enumerate(l["words"]):
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        last = i == len(l["words"]) - 1
        if last or re.search(r"[.?!…]$", w["w"]) or (re.search(r",$", w["w"]) and len(txt) > 24) or len(txt) > 36:
            cues.append([cur[0]["t0"], cur[-1]["t1"], txt]); cur = []
for i in range(len(cues) - 1):          # hold each cue until just before the next (max +0.6 s)
    cues[i][1] = min(cues[i + 1][0] - .01, cues[i][1] + .6)
cues[-1][1] += .6
open(f"{EP}/captions.srt", "w").write("".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues)))

# ---- chapters from the new cut (scene CUTS), whole seconds, every chapter >= 10 s
import scenes as SCN
C = SCN.CUTS
chap = [(0, "Code red"), (C["s02"][0], "Today's case: who keeps pulling the alarm?"), (C["s03"][0], "Clue 1: the incident report"),
        (C["s04"][0], "Clue 2: Mito vs The Alarm"), (C["s07"][0], "When stress drags on"), (C["s09"][0], "Clue 3: cold case 1991"),
        (C["s10"][0], "The twist"), (C["s11"][0], "Holiday heart check"), (C["s11r"][0], "Case recap + cheat codes"),
        (C["s15"][0], "Quiet"), (C["s17"][0], "Break starts + sources")]
secs = [int(t) for t, _ in chap]
for a, b in zip(secs, secs[1:] + [int(TM["T"])]): assert b - a >= 10, (a, b)
fmt = lambda s: f"{s // 60}:{s % 60:02d}"
chapters = {fmt(s): n for s, (_, n) in zip(secs, chap)}
m = json.load(open(f"{EP}/meta.json"))
m["chapters"] = chapters
m["duration_s"] = round(TM["T"], 1)
d = m["description"]
d = re.sub(r"Chapters:\n(?:\d+:\d\d [^\n]+\n)+", "Chapters:\n" + "".join(f"{k} {v}\n" for k, v in chapters.items()), d)
PC = "Photos (Toronto backgrounds): Unsplash — Ronin (@roninkgd), Richard Burlton (@richardworks), Chris Stewart (@pass_lake), Zia Syed (@syedzia123)."
if "Photos (Toronto backgrounds)" not in d:
    d = d.replace("\n\nNot medical advice. If you", f"\n{PC}\n\nNot medical advice. If you")
m["description"] = d
m["end_screen"] = ("Last ~20s: subscribe element + LF01 (quit smoking) video element over the LEFT 2/3 (sources band sits on the right, "
                   "ends with the Unsplash photo credit card); the final frame (Cyto in HQ, phone buzz, alarm flicker) hard-cuts back to the cold open = loop.")
json.dump(m, open(f"{EP}/meta.json", "w"), indent=1, ensure_ascii=False)
print("chapters", chapters, "T", TM["T"], "cues", len(cues))

# ---- pinned comment: photo credits (v3)
pc_f = f"{EP}/pinned_comment.txt"; pc = open(pc_f).read().rstrip()
if "Photos:" not in pc:
    pc = pc.replace("\n\nNot medical advice.", "\n\nPhotos (Unsplash): Ronin (@roninkgd) · Richard Burlton (@richardworks) · Chris Stewart (@pass_lake) · Zia Syed (@syedzia123).\n\nNot medical advice.")
open(pc_f, "w").write(pc + "\n")
m = json.load(open(f"{EP}/meta.json")); m["pinned_comment"] = pc; json.dump(m, open(f"{EP}/meta.json", "w"), indent=1, ensure_ascii=False)
print("pinned comment:", pc[-220:])
