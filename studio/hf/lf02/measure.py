"""LF02 fix pass - the step-11 measurements, run the SAME way on the old and the new mp4.
python3 measure.py OLD.mp4 OLD_timing.json NEW.mp4 NEW_timing.json OUTDIR
 (a) speaker-change gaps from timing.json      (b) frozen runs (ffmpeg freezedetect) + empty/flat frames around every cut
 (c) audio silence < -45 dB > 0.35 s           (d) 3-frame strips at speaker changes (12 listed + 10 random)
 + a 30 s before/after reel of the 12 listed handoffs (side by side)."""
import json, subprocess, sys, os, re, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OLD, OLDT, NEW, NEWT, OUT = sys.argv[1:6]
os.makedirs(OUT, exist_ok=True)
LISTED = [(1, 2), (12, 13), (18, 19), (22, 23), (28, 29), (32, 33), (39, 40), (42, 43), (50, 51), (60, 61), (61, 62), (63, 64)]
FONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 30)


def gaps(tj):
    L = json.load(open(tj))["lines"]
    g = [(round(b["t0"] - a["t1"], 3), a["n"], b["n"], a, b) for a, b in zip(L, L[1:]) if a["who"] != b["who"]]
    return g, L


def frame(mp4, t, w=640):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", mp4, "-frames:v", "1", "-vf", f"scale={w}:-1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def edge_density(im):
    a = np.asarray(im.convert("L")).astype(np.float32)
    gx = np.abs(np.diff(a, axis=1)).mean(); gy = np.abs(np.diff(a, axis=0)).mean()
    return float(gx + gy)


def freeze(mp4):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", mp4, "-vf", "freezedetect=n=0.003:d=0.3", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", r)]; du = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", r)]
    return list(zip(st, du))


def silence(mp4):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", mp4, "-af", "silencedetect=n=-45dB:d=0.35", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; du = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", r)]
    return list(zip(st, du))


def dur(mp4):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout)


def scene_cuts(mp4):
    """hard picture changes (scene score) - used to find every cut in BOTH videos the same way."""
    r = subprocess.run(["ffmpeg", "-nostats", "-i", mp4, "-vf", "select='gt(scene,0.35)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", r)]


rep = {}
for tag, mp4, tj in (("before", OLD, OLDT), ("after", NEW, NEWT)):
    g, L = gaps(tj)
    gs = np.array([x[0] for x in g])
    listed = {f"{a}>{b}": next((round(x[0], 3) for x in g if x[1] == a and x[2] == b), None) for a, b in LISTED}
    fz = freeze(mp4); sl = silence(mp4); cuts = scene_cuts(mp4)
    flat = []
    for c in cuts:
        for dt in (-1 / 30, 0, 1 / 30):
            e = edge_density(frame(mp4, c + dt, 480))
            if e < 2.0: flat.append((round(c + dt, 3), round(e, 2)))
    rep[tag] = dict(duration=round(dur(mp4), 2), speaker_changes=len(g), gap_median=round(float(np.median(gs)), 3), gap_max=round(float(gs.max()), 3),
                    gaps_over_1s=[(x[0], f"{x[1]}>{x[2]}") for x in g if x[0] > 1.0], gaps_over_0_5s=len([x for x in g if x[0] > .5]), listed=listed,
                    frozen_runs_over_0_3s=[(round(a, 2), round(b, 2)) for a, b in fz], hard_cuts=len(cuts), flat_frames_at_cuts=flat,
                    silences=[(round(a, 2), round(b, 2)) for a, b in sl])
json.dump(rep, open(f"{OUT}/measure.json", "w"), indent=1)
for k, v in rep.items():
    print(f"== {k}: {v['duration']}s, {v['speaker_changes']} speaker changes, gap median {v['gap_median']}s max {v['gap_max']}s, >1.0s: {v['gaps_over_1s']}")
    print(f"   listed: {v['listed']}")
    print(f"   frozen >0.3s: {v['frozen_runs_over_0_3s']}   flat frames at {v['hard_cuts']} cuts: {v['flat_frames_at_cuts']}")
    print(f"   silences <-45dB >0.35s: {v['silences']}")

# (d) 3-frame strips at speaker changes: frame before, the change, +0.25 s (12 listed + 10 random)
g, L = gaps(NEWT)
rnd = random.Random(11)
others = [x for x in g if (x[1], x[2]) not in LISTED]
pick = [x for x in g if (x[1], x[2]) in LISTED] + rnd.sample(others, 10)
strips = []
for gap, a, b, la, lb in pick:
    t = lb["t0"]
    ims = [frame(NEW, t - 1 / 30), frame(NEW, t), frame(NEW, t + .25)]
    s = Image.new("RGB", (640 * 3, 360 + 44), "#111"); d = ImageDraw.Draw(s)
    for i, im in enumerate(ims): s.paste(im.resize((640, 360)), (640 * i, 44))
    d.text((10, 6), f"{a}>{b}  {la['who']}->{lb['who']}  gap {gap:.2f}s   t={t:.2f}   [-1f | change | +0.25s]  \"{lb['text'][:40]}\"", fill="#FFD166", font=FONT)
    s.save(f"{OUT}/strip_{a:02d}_{b:02d}.jpg", quality=82); strips.append(s)
for k in range(0, len(strips), 6):
    grp = strips[k:k + 6]; sh = Image.new("RGB", (1920, 404 * len(grp)))
    for i, s in enumerate(grp): sh.paste(s, (0, 404 * i))
    sh.save(f"{OUT}/strips_{k // 6 + 1}.jpg", quality=80)

# 30 s before/after reel of the 12 listed handoffs (2.5 s each, side by side, AFTER audio; labels show the gap)
go, Lo = gaps(OLDT)
parts = []
for i, (a, b) in enumerate(LISTED):
    xo = next(x for x in go if x[1] == a and x[2] == b); xn = next(x for x in g if x[1] == a and x[2] == b)
    to = xo[3]["t1"] - .7; tn = xn[3]["t1"] - .7
    p = f"{OUT}/rp{i:02d}.mp4"
    lab = lambda s: s.replace(":", "\\:")
    fc = (f"[0:v]trim=start={to:.3f}:duration=2.5,setpts=PTS-STARTPTS,scale=960:540,drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Black.otf:text='{lab(f'BEFORE  {a}>{b}  gap {xo[0]:.2f}s')}':x=20:y=20:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=8[l];"
          f"[1:v]trim=start={tn:.3f}:duration=2.5,setpts=PTS-STARTPTS,scale=960:540,drawtext=fontfile=/usr/share/fonts/opentype/inter/InterDisplay-Black.otf:text='{lab(f'AFTER  gap {xn[0]:.2f}s')}':x=20:y=20:fontsize=34:fontcolor=#FFD166:box=1:boxcolor=black@0.7:boxborderw=8[r];"
          f"[l][r]hstack,pad=1920:1080:0:270:black[v];[0:a]atrim=start={to:.3f}:duration=2.5,asetpts=PTS-STARTPTS,pan=stereo|c0=c0|c1=c0[ao];[1:a]atrim=start={tn:.3f}:duration=2.5,asetpts=PTS-STARTPTS,pan=stereo|c0=c1|c1=c1[an];[ao][an]amerge=inputs=2,pan=stereo|c0=c0|c1=c3[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OLD, "-i", NEW, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", p], check=True)
    parts.append(p)
open(f"{OUT}/reel.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/reel.txt", "-c", "copy", f"{OUT}/lf02_handoffs_before_after.mp4"], check=True)
print("reel", f"{OUT}/lf02_handoffs_before_after.mp4", dur(f"{OUT}/lf02_handoffs_before_after.mp4"))
