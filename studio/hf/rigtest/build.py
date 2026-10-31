"""Generate index.html (HyperFrames composition) for the 5s Cyto rig test."""
import json
D = json.load(open("data.json"))
R = json.load(open("/home/claude/cyto2/rig/rig.json"))
SH_L, HAND_L, SH_R = R["shoulder_left"], R["hand_left"], R["shoulder_right"]
CW, CH = R["cup_size"]
cup_left = HAND_L[0] + .22 * CW - CW / 2
cup_top = HAND_L[1] - .80 * CH
T = 5.2

caps = [  # (words idx range, line)
    ([0, 1, 2, 3, 4], 0.20, 1.86),
    ([5, 6, 7, 8], 1.86, 2.98),
    ([9, 10, 11], 2.98, T),
]
KEY = {"Cyto,": "#FFD166", "6ix...": "#FF7A59", "body.": "#FFD166"}

cap_html = []
for li, (idx, a, b) in enumerate(caps):
    spans = []
    for i in idx:
        w = D["words"][i][0]
        cls = "w key" if w in KEY else "w"
        col = f' style="color:{KEY[w]}"' if w in KEY else ""
        spans.append(f'<span id="w{i}" class="{cls}"{col}>{w.upper()}</span>')
    cap_html.append(f'<div id="cap{li}" class="cap clip" data-start="{a}" data-duration="{round(b - a, 3)}">{" ".join(spans)}</div>')

bokeh = "".join(f'<div class="bk" id="bk{i}" style="left:{(i*137)%1000+20}px;top:{(i*263)%1500+120}px;width:{30+(i*17)%60}px;height:{30+(i*17)%60}px"></div>' for i in range(14))

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face {{ font-family: "InterBlack"; src: url("assets/InterDisplay-Black.otf"); }}
@font-face {{ font-family: "InterXB"; src: url("assets/Inter-ExtraBold.otf"); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
#cam {{ position:absolute; inset:0; transform-origin:540px 900px; }}
#bg {{ position:absolute; left:-120px; top:-80px; width:1320px; height:2080px; background:url(assets/bg.jpg) center/cover; }}
#shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(12,22,34,.55) 0%, rgba(12,22,34,.25) 40%, rgba(12,22,34,.85) 78%, #0c1622 100%); }}
.bk {{ position:absolute; border-radius:50%; background:radial-gradient(circle, rgba(255,209,102,.35), rgba(255,209,102,0) 70%); }}
#pill {{ position:absolute; top:120px; left:50%; transform:translateX(-50%); background:#FFD166; color:#0c1622; font:22px InterBlack; letter-spacing:.06em; padding:12px 26px; border-radius:40px; white-space:nowrap; }}
#cytoPos {{ position:absolute; left:-60px; top:300px; width:1200px; height:1200px; transform-origin:600px 940px; transform:scale(.84); }}
#cyto {{ position:absolute; left:0; top:0; width:1200px; height:1200px; transform-origin:600px 940px; }}
#cyto .L, #cyto .G {{ position:absolute; left:0; top:0; width:1200px; height:1200px; }}
#armL {{ transform-origin:{SH_L[0]}px {SH_L[1]}px; }}
#armR {{ transform-origin:{SH_R[0]}px {SH_R[1]}px; }}
#cup {{ position:absolute; left:{cup_left:.1f}px; top:{cup_top:.1f}px; width:{CW}px; height:{CH}px; transform-origin:{HAND_L[0]-cup_left:.1f}px {HAND_L[1]-cup_top:.1f}px; }}
.cap {{ position:absolute; left:60px; right:60px; top:1440px; text-align:center; font:78px/1.12 InterBlack; color:#FAF4E8; -webkit-text-stroke:3px #0c1622; paint-order:stroke fill; text-shadow:0 6px 0 rgba(0,0,0,.35); }}
.w {{ display:inline-block; opacity:0; }}
.key {{ font-size:98px; }}
#wipe {{ position:absolute; left:-400px; top:0; width:300px; height:1920px; background:#FF7A59; transform:skewX(-14deg); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
  <audio id="vo" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
  <div id="cam" class="clip" data-start="0" data-duration="{T}">
    <div id="bg"></div><div id="shade"></div>{bokeh}
    <div id="cytoPos"><div id="cyto">
      <div id="armR" class="G"><img class="L" src="assets/arm_right.png"><img class="L" src="assets/hand_right.png"></div>
      <img class="L" src="assets/body.png">
      <img class="L" src="assets/outfit_toque.png">
      <img id="eo" class="L" src="assets/eyes_open.png"><img id="ec" class="L" src="assets/eyes_closed.png" style="opacity:0">
      <img id="m_closed" class="L mo" src="assets/mouth_closed.png">
      <img id="m_small" class="L mo" src="assets/mouth_small.png" style="opacity:0">
      <img id="m_wide" class="L mo" src="assets/mouth_wide.png" style="opacity:0">
      <img id="m_o" class="L mo" src="assets/mouth_o.png" style="opacity:0">
      <div id="armL" class="G"><img class="L" src="assets/arm_left.png"><img id="cup" src="assets/cup_red.png"><img class="L" src="assets/hand_left.png"></div>
    </div></div>
  </div>
  <div id="pill" class="clip" data-start="0" data-duration="{T}">THE BODY IS THE 6IX</div>
  {''.join(cap_html)}
  <div id="wipe" class="clip" data-start="0" data-duration="0.5"></div>
</div>
<script>
const D = {json.dumps(D)};
const T = {T};
const tl = gsap.timeline({{ paused: true }});
// --- camera: punch-in on the hook, slow push, punch on 6ix, shake on body
tl.fromTo("#cam", {{scale:1.18}}, {{scale:1.0, duration:0.35, ease:"power3.out"}}, 0);
tl.to("#cam", {{scale:1.06, duration:2.2, ease:"none"}}, 0.35);
tl.to("#cam", {{scale:1.13, duration:0.10, ease:"power2.out"}}, 2.61);
tl.to("#cam", {{scale:1.07, duration:0.30, ease:"power2.inOut"}}, 2.71);
[[-10,6],[9,-7],[-6,4],[4,-3],[0,0]].forEach((p,i)=>tl.to("#cam", {{x:p[0], y:p[1], duration:0.04}}, 3.46+i*0.04));
tl.to("#cam", {{scale:1.10, duration:1.4, ease:"none"}}, 3.8);
// --- background Ken Burns + drifting bokeh
tl.fromTo("#bg", {{x:0, y:0, scale:1.0}}, {{x:-90, y:-40, scale:1.08, duration:T, ease:"none"}}, 0);
document.querySelectorAll(".bk").forEach((b,i)=>tl.fromTo(b, {{y:0, opacity:.25+(i%3)*.2}}, {{y:-160-(i%5)*40, opacity:.15, duration:T, ease:"none"}}, 0));
// --- orange swipe transition in
tl.fromTo("#wipe", {{x:0}}, {{x:1700, duration:0.45, ease:"power2.in"}}, 0);
// --- Cyto entrance + idle breathing / bounce
tl.fromTo("#cyto", {{y:420}}, {{y:0, duration:0.45, ease:"back.out(1.6)"}}, 0.0);
for (let k=0; k<8; k++) {{
  const t0 = 0.45 + k*0.6;
  tl.to("#cyto", {{y:-14, scaleY:1.025, scaleX:0.985, duration:0.3, ease:"sine.inOut"}}, t0);
  tl.to("#cyto", {{y:0, scaleY:1.0, scaleX:1.0, duration:0.3, ease:"sine.inOut"}}, t0+0.3);
}}
// head tilt on the joke ("inside your body")
tl.to("#cyto", {{rotation:7, duration:0.18, ease:"power2.out"}}, 3.0);
tl.to("#cyto", {{rotation:0, duration:0.35, ease:"power2.inOut"}}, 3.75);
// --- right arm: wave on "Yo", point on "6ix"
tl.to("#armR", {{rotation:-122, duration:0.22, ease:"back.out(2)"}}, 0.12);
[-100,-128,-102,-125].forEach((a,i)=>tl.to("#armR", {{rotation:a, duration:0.14, ease:"sine.inOut"}}, 0.34+i*0.14));
tl.to("#armR", {{rotation:0, duration:0.3, ease:"power2.inOut"}}, 0.95);
tl.to("#armR", {{rotation:-118, duration:0.18, ease:"back.out(2)"}}, 2.50);
tl.to("#armR", {{rotation:0, duration:0.3, ease:"power2.inOut"}}, 3.0);
// --- cup: raise ("cheers") on 6ix, sip after "body", set down
tl.to("#armL", {{rotation:-28, duration:0.2, ease:"back.out(2)"}}, 2.55);
tl.to("#cup", {{rotation:28, duration:0.2, ease:"back.out(2)"}}, 2.55);
tl.to("#armL", {{rotation:0, duration:0.3, ease:"power2.inOut"}}, 3.0);
tl.to("#cup", {{rotation:0, duration:0.3, ease:"power2.inOut"}}, 3.0);
tl.to("#armL", {{rotation:-42, duration:0.32, ease:"power2.out"}}, 3.85);
tl.to("#cup", {{rotation:94, duration:0.32, ease:"power2.out"}}, 3.85);
tl.to("#cup", {{rotation:102, duration:0.25, ease:"sine.inOut", yoyo:true, repeat:1}}, 4.2);
tl.to("#armL", {{rotation:0, duration:0.3, ease:"power2.inOut"}}, 4.75);
tl.to("#cup", {{rotation:0, duration:0.3, ease:"power2.inOut"}}, 4.75);
// --- eyes: blinks + content close during sip
const blink=(t,d=0.1)=>{{ tl.set("#ec",{{opacity:1}},t); tl.set("#eo",{{opacity:0}},t); tl.set("#ec",{{opacity:0}},t+d); tl.set("#eo",{{opacity:1}},t+d); }};
blink(1.55); blink(3.92, 0.85);
// --- mouth sync (shape per syllable from the voice envelope)
const mo=["#m_closed","#m_small","#m_wide","#m_o"];
D.mouth.forEach(([t,s])=>{{ mo.forEach(m=>tl.set(m,{{opacity:0}},t)); tl.set("#m_"+s,{{opacity:1}},t); }});
mo.forEach(m=>tl.set(m,{{opacity:0}},3.95)); tl.set("#m_closed",{{opacity:1}},3.95);
tl.set("#m_closed",{{opacity:0}},4.95); tl.set("#m_wide",{{opacity:1}},4.95);
// --- word-by-word captions, key words pop bigger
D.words.forEach((w,i)=>{{
  const k = ["Cyto,","6ix...","body."].includes(w[0]);
  tl.fromTo("#w"+i, {{opacity:0, scale:k?1.6:1.25, y:18}}, {{opacity:1, scale:1, y:0, duration:k?0.22:0.14, ease:"back.out(2.4)"}}, w[1]-0.03);
}});
tl.fromTo("#pill", {{y:-120}}, {{y:0, duration:0.4, ease:"back.out(2)"}}, 0.1);
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
print("ok")
