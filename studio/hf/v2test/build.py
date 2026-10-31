"""v2 TEST — Ep 7's middle section (7.4s–20.03s) rebuilt with the proposed v2 changes.
Changes vs Ep 7: captions inside the Shorts safe zone, Cyto big (not a corner sticker),
Cyto-themed Mermaid diagram that builds node-by-node, LottieFiles heart synced to the BPM.
python3 build.py  ->  index.html"""
import json, sys, os, subprocess, re
sys.path.insert(0, "/home/claude/hf")
import cytohf as C

P = "/home/claude/hf/v2test"; os.chdir(P)
OFF, END = 7.4, 20.03
T = round(END - OFF, 3)
ALL = json.load(open("/home/claude/ep7/timing.json"))["words"]
WORDS = [dict(w, t0=round(w["t0"] - OFF, 3), t1=round(w["t1"] - OFF, 3)) for w in ALL if OFF <= w["t0"] < END]
CUT = round(14.67 - OFF, 3)   # S2 -> S3

def wt(line, word):
    for w in WORDS:
        if w["line"] == line and w["w"].lower().strip(".,?!:").startswith(word.lower()):
            return w["t0"]
    raise KeyError((line, word))

# ---------- assets ----------
C.copy_assets(P)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(OFF), "-t", str(T), "-i", "/root/cyto-uploads/ep07/cyto-ep7-leafs-overtime.mp4",
                "-vn", "-c:a", "pcm_s16le", "assets/audio.wav"], check=True)
FF_SVG = open("assets/ff.svg").read()
FF_SVG = re.sub(r'style="max-width:[^"]*"', 'style="width:100%;height:100%"', FF_SVG, count=1).replace('width="100%"', '', 1)
HEART = open("assets/heart-beat.json").read()

O_WORDS = {"monitors", "about", "to", "your", "fight", "flight"}
full = C.mouth_track("/home/claude/ep7/voice.wav", ALL, o_words=O_WORDS)
mouth = [[round(t - OFF, 3), s] for t, s in full if OFF <= t < END]
mouth.insert(0, [0, "closed"])

# ---------- v2 layout (Shorts safe zone: x 60–940, y 200–1480) ----------
CYTO = C.place(300, 1300, 0.56)        # big, lower-left — never a corner sticker
CAP_Y = 880                            # captions under the figure, above Cyto
KEYS = {"60": "#5AE68C", "114": "#FF7A59", "fightorflight": "#FFD166", "vigorous": "#FF7A59", "habs": "#E2394B", "arena": "#FFD166"}
cap_html, cap_js = C.captions(WORDS, KEYS, y=CAP_Y)

SIP = (14.45 - OFF, 0.9)
blinks = [(t, 0.1) for t in (1.2, 3.9, 6.2, 9.6, 11.8)] + [(SIP[0] + 0.25, 0.5)]
gest = dict(points=[(wt(2, "114") - 0.1, 0.8), (wt(3, "vigorous"), 0.7)], sips=[SIP],
            tilts=[(wt(2, "Habs"), 0.6, 6), (wt(3, "fight"), 0.7, -7)], shrugs=[(wt(2, "jumped"), 0.5)])
rig_js = C.rig_js(mouth, blinks, T=T, mute=[(SIP[0], 0)], **gest)
tr_html, tr_js = C.transition("zoom", CUT)

def ecg_path(n=40, per=110):
    d = "M0 150"
    for i in range(n):
        x = i * per
        d += f" L{x+25} 150 L{x+32} 140 L{x+39} 150 L{x+50} 150 L{x+55} 160 L{x+61} 40 L{x+67} 185 L{x+73} 150 L{x+88} 150 L{x+96} 128 L{x+104} 150"
    return d

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<script src="assets/lottie_svg.min.js"></script>
<style>
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:InterXB; }}
#cam, #shaker {{ position:absolute; inset:0; transform-origin:540px 960px; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.navy {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #17304d 0%, #0c1622 70%); }}
.dots {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; background-image:radial-gradient(rgba(120,170,220,.10) 3px, transparent 4px); background-size:70px 70px; }}
.panel {{ position:absolute; left:60px; top:200px; width:880px; height:650px; border-radius:36px; background:#0f2236; border:3px solid #24425f; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,.4); }}
.ptitle {{ position:absolute; left:36px; top:28px; font:28px InterXB; color:#96b0c4; letter-spacing:.04em; }}
.card {{ position:absolute; left:560px; top:1090px; width:380px; padding:24px 26px 24px 34px; border-radius:26px; background:#FAF4E8; border-left:14px solid #FF7A59; box-shadow:0 14px 30px rgba(0,0,0,.35); z-index:30; }}
.card h3 {{ font:28px InterBlack; color:#FF7A59; letter-spacing:.03em; margin-bottom:8px; }}
.card p {{ font:32px/1.25 InterSB; color:#0c1622; }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-170px; width:340px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
.bpm {{ position:absolute; font:150px InterBlack; color:#FAF4E8; text-align:right; }}
.unit {{ position:absolute; font:34px InterXB; color:#FAF4E8; }}
#lot {{ position:absolute; left:20px; top:70px; width:330px; height:250px; }}
#ffw {{ position:absolute; left:70px; top:90px; width:740px; height:540px; }}
#ffw .nodeLabel, #ffw .nodeLabel p {{ font-family:InterBlack !important; }}
.gauge {{ position:absolute; top:150px; width:340px; height:340px; }}
.needle {{ position:absolute; left:167px; top:40px; width:8px; height:140px; border-radius:4px; background:#FAF4E8; transform-origin:4px 140px; }}
.hub {{ position:absolute; left:155px; top:165px; width:32px; height:32px; border-radius:50%; background:#FAF4E8; }}
.glab {{ position:absolute; top:225px; width:340px; text-align:center; font:34px InterBlack; color:#FAF4E8; }}
.gsub {{ position:absolute; top:272px; width:340px; text-align:center; font:30px InterXB; }}
{C.rig_css()}
{C.CAP_CSS}
.cap {{ left:60px; right:140px; }}   /* keep clear of the Shorts action buttons */
{C.TR_CSS}
#cytoLayer {{ position:absolute; inset:0; z-index:20; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="shaker" class="clip" data-start="0" data-duration="{T}"><div id="cam">

  <div id="s2" class="scene clip" data-start="0" data-duration="{CUT}">
    <div class="navy"></div><div id="dots2" class="dots"></div>
    <div id="pn2" class="panel">
      <div class="ptitle">HEART MONITOR · HOCKEY FAN</div>
      <div id="lot"></div>
      <div id="bpm2" class="bpm" style="right:40px; top:70px; color:#5AE68C">60</div>
      <div class="unit" style="right:44px; top:235px">BPM</div>
      <svg style="position:absolute; left:0; top:310px" width="880" height="300"><g id="ecg"><path d="{ecg_path()}" fill="none" stroke="#FF7A59" stroke-width="6" stroke-linejoin="round"/></g></svg>
    </div>
    <div id="cd2" class="card"><h3>CAN J CARDIOL, 2017</h3><p>20 fans wore heart monitors at games.</p></div>
  </div>

  <div id="s3" class="scene clip" data-start="{CUT}" data-duration="{T-CUT}">
    <div class="navy"></div><div id="dots3" class="dots"></div>
    <div id="pn3" class="panel">
      <div class="ptitle">FIGHT-OR-FLIGHT</div>
      <div id="ffw">{FF_SVG}</div>
      <div id="gz" style="position:absolute; inset:0; background:#0f2236; opacity:0">
        <div style="position:absolute; top:44px; width:880px; text-align:center; font:40px InterBlack; color:#FAF4E8">HOW HARD YOUR HEART WORKS</div>
        <div class="gauge" style="left:40px"><svg width="340" height="200"><path d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#2a4866" stroke-width="30"/><path id="arcA" d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#FFD166" stroke-width="30" stroke-dasharray="440" stroke-dashoffset="440"/></svg>
          <div id="ndA" class="needle"></div><div class="hub"></div><div class="glab">ON TV</div><div class="gsub" style="color:#FFD166">moderate</div></div>
        <div class="gauge" style="left:500px"><svg width="340" height="200"><path d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#2a4866" stroke-width="30"/><path id="arcB" d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#FF7A59" stroke-width="30" stroke-dasharray="440" stroke-dashoffset="440"/></svg>
          <div id="ndB" class="needle"></div><div class="hub"></div><div class="glab">AT THE ARENA</div><div class="gsub" style="color:#FF7A59">vigorous</div></div>
      </div>
    </div>
    <div id="cd3a" class="card"><h3>FIGHT-OR-FLIGHT</h3><p>Your nervous system revs the heart up.</p></div>
    <div id="cd3b" class="card" style="opacity:0"><h3>SAME STUDY</h3><p>Live game = vigorous exercise.</p></div>
  </div>

  <div id="cytoLayer">{C.rig_html("outfit_jersey", "cup_blue")}</div>
</div></div>
<div id="pill" class="clip" data-start="0" data-duration="{T}">THE BODY IS THE 6IX</div>
{cap_html}
{tr_html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const T = {T};
// ---- Lottie heart (LottieFiles), driven frame-by-frame by the timeline so renders are deterministic
const heart = lottie.loadAnimation({{container:document.getElementById("lot"), renderer:"svg", loop:false, autoplay:false, animationData:{HEART}}});
const NF = heart.totalFrames, hb = {{f:0}};
tl.fromTo(hb,{{f:0}},{{f:NF*14,duration:{CUT},ease:"power1.in",onUpdate:()=>heart.goToAndStop(hb.f % NF,true)}},0);
// ---- camera
tl.set("#shaker",{{x:0,y:0,scale:1}},0);
[[0,{CUT}],[{CUT},T]].forEach(([a,b])=>tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:b-a-0.05,ease:"none",immediateRender:false}},a+0.01));
const punch=(t)=>{{ tl.to("#shaker",{{scale:1.08,duration:0.08,ease:"power2.out"}},t); tl.to("#shaker",{{scale:1,duration:0.3,ease:"power2.inOut"}},t+0.08); }};
[{wt(2,"114")},{wt(3,"vigorous")}].forEach(punch);
["#dots2","#dots3"].forEach((b,i)=>tl.fromTo(b,{{x:0,y:0}},{{x:70,y:140,duration:[{CUT},T-{CUT}][i],ease:"none"}},[0,{CUT}][i]));
// ---- Cyto: big, present the whole time
tl.set("#cytoPos",{json.dumps(CYTO)},0);
{rig_js}
// ---- S2
tl.fromTo("#pn2",{{y:900}},{{y:0,duration:0.45,ease:"power3.out"}},0);
tl.fromTo("#ecg",{{x:0}},{{x:-1900,duration:{CUT},ease:"power1.in"}},0);
tl.fromTo("#bpm2",{{innerText:60}},{{innerText:114,snap:{{innerText:1}},duration:{wt(2,"114")-wt(2,"jumped")+0.3},ease:"power2.in"}},{wt(2,"jumped")});
tl.to("#bpm2",{{color:"#FF7A59",duration:0.3}},{wt(2,"114")-0.4});
tl.fromTo("#bpm2",{{scale:1.35}},{{scale:1,duration:0.3,ease:"back.out(3)"}},{wt(2,"114")});
tl.fromTo("#cd2",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{wt(2,"Scientists")+0.2});
// ---- S3: themed Mermaid builds itself — nodes pop, arrows draw on
const nodes=[...document.querySelectorAll("#ffw .node")], edges=[...document.querySelectorAll("#ffw .edgePaths path")];
const NT=[{CUT+0.15},{wt(3,"fight")},{wt(3,"kicking")},{wt(3,"in")}];
const nodeAt=(n)=>{{ const txt=n.textContent.toUpperCase(); return txt.includes("PLAY")?NT[0]:txt.includes("ADREN")?NT[1]:txt.includes("HEART")?NT[2]:NT[3]; }};
nodes.forEach(n=>tl.fromTo(n,{{opacity:0,scale:0.3,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)",immediateRender:true}},nodeAt(n)));
edges.forEach((e,i)=>{{ const L=e.getTotalLength(); e.style.strokeDasharray=L; const t=[NT[1],NT[2],NT[3]][Math.min(i,2)]-0.25;
  tl.fromTo(e,{{strokeDashoffset:L,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.3,ease:"power2.out",immediateRender:true}},t); }});
tl.fromTo("#ffw",{{scale:1.08}},{{scale:1,duration:{wt(3,"arena")-CUT},ease:"none"}},{CUT});
tl.fromTo("#cd3a",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{wt(3,"fight")});
tl.to("#gz",{{opacity:1,duration:0.25}},{wt(3,"arena")-0.15});
tl.fromTo("#gz",{{scale:1.3}},{{scale:1,duration:0.35,ease:"power3.out"}},{wt(3,"arena")-0.15});
tl.fromTo("#ndA",{{rotation:-90}},{{rotation:5,duration:0.7,ease:"back.out(1.6)"}},{wt(3,"arena")+0.1});
tl.fromTo("#arcA",{{attr:{{"stroke-dashoffset":440}}}},{{attr:{{"stroke-dashoffset":209}},duration:0.7,ease:"power2.out"}},{wt(3,"arena")+0.1});
tl.fromTo("#ndB",{{rotation:-90}},{{rotation:68,duration:0.8,ease:"back.out(1.6)"}},{wt(3,"vigorous")-0.1});
tl.fromTo("#arcB",{{attr:{{"stroke-dashoffset":440}}}},{{attr:{{"stroke-dashoffset":53}},duration:0.8,ease:"power2.out"}},{wt(3,"vigorous")-0.1});
tl.to("#cd3a",{{x:600,duration:0.2,ease:"power2.in"}},{wt(3,"arena")-0.2}); tl.fromTo("#cd3b",{{opacity:1,x:600}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.6)",immediateRender:false}},{wt(3,"arena")+0.02}); tl.set("#cd3b",{{opacity:0}},0);
{tr_js}
{cap_js}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
for f in ("hyperframes.json", "package.json"):
    if not os.path.exists(f): subprocess.run(["cp", f"/home/claude/hf/ep07/{f}", f])
json.dump({"name": "v2test"}, open("meta.json", "w"))
print("built", len(html), "bytes; T", T, "cut", CUT, "words", len(WORDS))
