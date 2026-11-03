"""LF01: concat the 8 ElevenLabs chunks with 0.35 s gaps -> /home/claude/lf01/voice.wav + timing.json (global Scribe word times,
display spellings for captions). Chapter offsets = chunk starts."""
import json, subprocess, numpy as np, re
D = "/home/claude/lf01"; A = "/home/user/cyto-uploads/audio"; SR = 44100; GAP = 0.35
NAMES = ["Hook+Intro", "What's in the smoke", "First hours", "The first week", "Weeks 2-4", "Months to years", "Cyto's tips", "Outro"]
DISP = {"six…": "6ix…", "six,": "6ix,", "six.": "6ix.", "six": "6ix", "five-oh-one": "501", "twenty-four": "24/7", "iQuit": "iQuit"}
out, words, chap, t = [], [], [], 0.0
for k in range(8):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{A}/lf01_c{k}.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).copy()
    chap.append(dict(k=k, name=NAMES[k], t0=round(t, 3), dur=round(len(x) / SR, 3)))
    for w in json.load(open(f"{D}/words_c{k}.json")):
        ww = w["w"]
        # caption spellings
        prev = words[-1]["w"].lower() if words else ""
        if ww.lower().startswith("six") and prev != "the": pass          # "about six." stays a number
        else: ww = DISP.get(ww, ww)
        words.append(dict(w=ww, t0=round(t + w["t0"], 3), t1=round(t + w["t1"], 3), ch=k))
    if k == 7:   # 4 s music-only hold after "description." so the 6 source screens each get >=2.5 s
        wd = [w for w in json.load(open(f"{D}/words_c7.json"))]
        i = [j for j, w in enumerate(wd) if w["w"].startswith("description")][0]
        cut = (wd[i]["t1"] + wd[i + 1]["t0"]) / 2; HOLD = 4.0; cs = int(cut * SR)
        x = np.concatenate([x[:cs], np.zeros(int(HOLD * SR), np.float32), x[cs:]])
        for w in words:
            if w["ch"] == 7 and w["t0"] > t + cut: w["t0"] = round(w["t0"] + HOLD, 3); w["t1"] = round(w["t1"] + HOLD, 3)
        chap[-1]["dur"] = round(len(x) / SR, 3); chap[-1]["hold"] = [round(t + cut, 3), HOLD]
    out.append(x); t += len(x) / SR
    if k < 7: out.append(np.zeros(int(GAP * SR), np.float32)); t += GAP
# "twenty-four seven" -> "24/7" (drop the 'seven' that follows)
fixed = []
for w in words:
    if fixed and fixed[-1]["w"] == "24/7" and w["w"].lower().startswith("seven"):
        fixed[-1]["t1"] = w["t1"]; fixed[-1]["w"] = "24/7" + w["w"][5:]; continue
    fixed.append(w)
y = np.concatenate(out)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", f"{D}/voice.wav"], input=y.tobytes(), check=True)
json.dump(dict(words=fixed, chapters=chap, total=round(len(y) / SR, 3)), open(f"{D}/timing.json", "w"), indent=0)
for c in chap: print(c, f"{int(c['t0']//60)}:{c['t0']%60:05.2f}")
print("total", round(len(y) / SR, 2), "words", len(fixed))
