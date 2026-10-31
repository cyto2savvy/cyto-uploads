"""v3 TEST — character quality. Ep 7 audio 4.0s–15.5s (catchphrase, Habs study, a sip).
python3 build.py v2   -> current PNG rig    |   python3 build.py v3 -> vector rig (brows, lids, visemes, organelles, sip SFX)"""
import json, sys, os, subprocess
sys.path.insert(0, "/home/claude/hf")
import cytohf as C, cyto3 as R

MODE = sys.argv[1] if len(sys.argv) > 1 else "v3"
P = f"/home/claude/hf/v3test/{MODE}"; os.makedirs(P, exist_ok=True); os.chdir(P)
OFF, END = 4.0, 15.5
T = round(END - OFF, 3)
ALL = json.load(open("/home/claude/ep7/timing.json"))["words"]
WORDS = [dict(w, t0=round(w["t0"] - OFF, 3), t1=round(w["t1"] - OFF, 3)) for w in ALL if OFF <= w["t0"] < END]

def wt(line, word):
    for w in WORDS:
        if w["line"] == line and w["w"].lower().strip(".,?!:").startswith(word.lower()): return w["t0"]
    raise KeyError((line, word))

C.copy_assets(P, [("/home/claude/cyto2/photos/cn-tower-dusk.jpg", "bg.jpg")])
for f in ("hyperframes.json", "package.json"): subprocess.run(["cp", f"/home/claude/hf/v2test/{f}", f])
if not os.path.exists("node_modules"): os.symlink("/home/claude/hf/node_modules", "node_modules")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(OFF), "-t", str(T), "-i", "/home/claude/ep7/cyto-ep7-leafs-overtime.mp4",
                "-vn", "-c:a", "pcm_s16le", "-ar", "48000", "assets/base.wav"], check=True)

SIP = (14.45 - OFF, 0.95)
blinks = [(t, 0.1) for t in (1.4, 3.3, 5.9, 8.1)]
gest = dict(raises=[(wt(1, "6ix") - 0.05, 0.45)], points=[(wt(2, "114") - 0.1, 0.8)], sips=[SIP],
            tilts=[(wt(1, "inside"), 0.75, 7), (wt(2, "Habs"), 0.7, -6)], shrugs=[(wt(2, "jumped"), 0.45)])
HOST = C.place(540, 1020, 0.86)

if MODE == "v2":
    mouth = [[round(t - OFF, 3), s] for t, s in C.mouth_track("/home/claude/ep7/voice.wav", ALL,
             o_words={"boy", "cyto", "from", "your", "monitors", "about", "to"}) if OFF <= t < END]
    mouth.insert(0, [0, "closed"])
    rig_h, rig_c = C.rig_html(None, "cup_red"), C.rig_css()
    rig_j = C.rig_js(mouth, blinks + [(SIP[0] + 0.25, 0.5)], T=T, mute=[(SIP[0], 0)], waves=[0.05], **gest)
    subprocess.run(["cp", "assets/base.wav", "assets/audio.wav"])
else:
    mouth = R.viseme_track("/home/claude/ep7/voice.wav", ALL, t_off=OFF, t_end=END)
    if not mouth or mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
    rig_h, rig_c = R.rig3_html(None, "cup_red"), R.rig3_css()
    expr = [(wt(1, "6ix") - 0.05, 0.5, "hype"), (wt(2, "Habs") - 0.05, 0.75, "skeptic"), (wt(2, "114") - 0.08, 0.9, "shock")]
    looks = [(wt(2, "Scientists"), 14, -6), (wt(2, "put") + 0.4, 0, 0)]
    rig_j = R.rig3_js(mouth, T, blinks=blinks, mute=[(SIP[0], 0)], waves=[0.05], expr=expr, looks=looks, **gest)
    R.make_sip(); R.mix_sips("assets/base.wav", [SIP[0]], "assets/audio.wav")

KEYS = {"cyto": "#FFD166", "6ix": "#FF7A59", "body": "#FFD166", "habs": "#E2394B", "60": "#5AE68C", "114": "#FF7A59"}
cap_html, cap_js = C.captions(WORDS, KEYS, y=1330)

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
#cam {{ position:absolute; inset:0; transform-origin:540px 960px; }}
.bgphoto {{ position:absolute; left:-140px; top:-100px; width:1360px; height:2120px; background-size:cover; background-position:center; }}
.shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(12,22,34,.5) 0%, rgba(12,22,34,.15) 40%, rgba(12,22,34,.85) 74%, #0c1622 100%); }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-170px; width:340px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
{rig_c}
{C.CAP_CSS}
.cap {{ left:60px; right:140px; }}
#cytoLayer {{ position:absolute; inset:0; z-index:20; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="cam" class="clip" data-start="0" data-duration="{T}">
  <div id="bg" class="bgphoto" style="background-image:url(assets/bg.jpg)"></div><div class="shade"></div>
  <div id="cytoLayer">{rig_h}</div>
</div>
<div id="pill" class="clip" data-start="0" data-duration="{T}">THE BODY IS THE 6IX</div>
{cap_html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const T = {T};
tl.fromTo("#bg",{{x:0,y:0,scale:1}},{{x:-60,y:-40,scale:1.08,duration:T,ease:"none"}},0);
tl.fromTo("#cam",{{scale:1}},{{scale:1.04,duration:T,ease:"none"}},0);
tl.set("#cytoPos",{json.dumps(HOST)},0);
{rig_j}
{cap_js}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>"""
open("index.html", "w").write(html)
json.dump({"name": f"v3test-{MODE}"}, open("meta.json", "w"))
print(MODE, "built", len(html), "bytes; mouth changes", len(mouth))
