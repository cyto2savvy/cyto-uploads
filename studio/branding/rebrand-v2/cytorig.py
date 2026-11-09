"""Canon-v2 Cyto rig for HyperFrames episodes (replaces the old PNG rig cyto3.py).
Builds the layered SVG from studio/branding/rebrand-v2/cyto2d.js (RIG=1) and drives it with cyto_rig_runtime.js.
Box: 1200x1200, body centre at (600,640) -> same placement maths as cytohf.place()."""
import os, re, json, random, subprocess, tempfile
import numpy as np

REPO = os.path.expanduser("~/cyto-uploads/studio/branding/rebrand-v2")
VIS = [("mbp", "closed"), ("oo", "o"), ("ou", "o"), ("ow", "o"), ("ee", "small"), ("ea", "small"), ("th", "small"), ("sh", "small"), ("ch", "small")]
SINGLE = {**{c: "closed" for c in "mbp"}, **{c: "small" for c in "fv"}, "o": "o", "u": "o", "w": "o", "q": "o", "r": "o",
          "a": "wide", "h": "wide", "i": "small", "e": "small", "y": "small"}
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}


def word_shapes(w):
    w = re.sub(r"[^a-z]", "", "".join(NUM.get(c, c) for c in w.lower()))
    out, i = [], 0
    while i < len(w):
        hit = next((v for k, v in VIS if w[i:i + 2] == k), None)
        if hit: out.append(hit); i += 2; continue
        out.append(SINGLE.get(w[i], "small")); i += 1
    col = [v for j, v in enumerate(out) if j == 0 or v != out[j - 1]]
    return col or ["small"]


def mouth_track(voice_wav, words, fps=30):
    """Mouth shape per frame from the letters of each word, gated by loudness: silent -> closed. Min hold 2 frames (no flicker)."""
    SR = 16000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", voice_wav, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    hop = SR // fps
    rms = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); rms /= np.percentile(rms, 98)
    track, prev, hold = [[0.0, "closed"]], "closed", 0
    for f, e in enumerate(rms):
        t = f / fps
        w = next((w for w in words if w["t0"] - .02 <= t <= w["t1"] + .02), None)
        if e < 0.07 or not w:
            s = "closed"
        else:
            vs = word_shapes(w["w"]); k = min(len(vs) - 1, int((t - w["t0"]) / max(.01, w["t1"] - w["t0"]) * len(vs)))
            s = vs[k]
            if s == "wide" and e < 0.35: s = "small"
            if s == "small" and e > 0.75: s = "wide"
        if s != prev and (hold <= 0 or (s == "closed" and e < 0.07)):   # silence closes the mouth at once
            track.append([round(t, 3), s]); prev = s; hold = 2
        hold -= 1
    return track


def blink_times(T, seed=14, lo=2.0, hi=4.0, avoid=()):
    """A blink every 2-4 s (seeded), skipping windows in `avoid` [(a,b), ...]."""
    r, t, out = random.Random(seed), 1.2, []
    while t < T - 0.3:
        if not any(a - 0.2 <= t <= b for a, b in avoid): out.append(round(t, 2))
        t += r.uniform(lo, hi)
    return out


def build_svg(fit="hoodie", expr="solemn", seed=3):
    d = tempfile.mkdtemp(prefix="rig_")
    subprocess.run(["node", os.path.join(REPO, "cyto2d.js")], cwd=d, check=True, capture_output=True,
                   env=dict(os.environ, RIG="1", EXPR=expr, SEED=str(seed)))
    s = open(os.path.join(d, f"cyto_rig_{fit}{'' if expr == 'chill' else '_' + expr}.svg")).read()
    return s


def rig_html(fit="hoodie", expr="solemn", seed=3):
    s = build_svg(fit, expr, seed)
    s = s.replace('width="1100" height="1100" viewBox="-550 -550 1100 1100"', 'width="1200" height="1200" viewBox="-600 -640 1200 1200" style="position:absolute;left:0;top:0;overflow:visible"')
    s = re.sub(r"^<svg ", '<svg id="cytoSvg" ', s)
    return f'<div id="cytoPos"><div id="cytoWrap">{s}</div></div>'


def rig_css():
    return ("#cytoPos { position:absolute; left:0; top:0; width:1200px; height:1200px; transform-origin:0 0; }\n"
            "#cytoWrap { position:absolute; left:0; top:0; width:1200px; height:1200px; }\n")


def runtime_js():
    return open(os.path.join(REPO, "cyto_rig_runtime.js")).read()


def rig_js(mouth, T, blinks, bob=None, armR=None):
    """Seek-safe: one proxy tween over the whole video calls rig.update(t)."""
    o = {"mouth": mouth, "blinks": blinks, "bob": bob or {"amp": 3, "period": 4}, "armR": armR or {"deg": 2, "period": 6.4}}
    return (f'const RIG=CytoRig(document.getElementById("cytoSvg"),{json.dumps(o)});const RP={{t:0}};RIG.update(0);'
            f'tl.fromTo(RP,{{t:0}},{{t:{T},duration:{T},ease:"none",immediateRender:false,onUpdate:()=>RIG.update(RP.t)}},0);')
