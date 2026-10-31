"""Ep 7 (Leafs overtime) rebuilt on the Cyto puppet rig in HyperFrames.  python3 build.py"""
import json, sys, os, subprocess
sys.path.insert(0, "/home/claude/hf")
import cytohf as C
from PIL import Image

P = "/home/claude/hf/ep07"; os.chdir(P)
TM = json.load(open("/home/claude/ep7/timing.json")); WORDS = TM["words"]
T = 34.87
CUTS = [0, 4.07, 7.4, 14.67, 20.03, 21.93, 24.03, 31.5, T]

def wt(line, word, k="t0"):
    for w in WORDS:
        if w["line"] == line and w["w"].lower().strip(".,?!:").startswith(word.lower()):
            return round(w[k], 3)
    raise KeyError((line, word))

# ---------- assets ----------
ff = Image.open("/home/claude/ep7/assets/ff_crop.png"); ff = ff.resize((900, int(ff.height * 900 / ff.width)), Image.LANCZOS)
os.makedirs("assets", exist_ok=True); ff.save("assets/ff.png"); FFH = ff.height
C.copy_assets(P, [("/home/claude/cyto2/photos/cn-tower-dusk.jpg", "bg.jpg"), ("/home/claude/cyto2/photos/skyline-aurora.jpg", "bg2.jpg")])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/home/claude/ep7/cyto-ep7-leafs-overtime.mp4", "-vn", "-c:a", "pcm_s16le", "assets/audio.wav"], check=True)

O_WORDS = {"bro", "overtime", "youre", "boy", "cyto", "from", "your", "to", "monitors", "about", "you", "know", "doctor", "out", "most", "common", "workout", "go"}
mouth = C.mouth_track("/home/claude/ep7/voice.wav", WORDS, o_words=O_WORDS)

# ---------- Cyto placement per scene ----------
HOST = C.place(540, 1060, 0.84)
SMALL = C.place(215, 1215, 0.40)
MID = C.place(540, 1180, 0.62)
place = [(0, HOST), (CUTS[2], SMALL), (CUTS[5], HOST), (CUTS[6], MID), (CUTS[7], HOST)]

# ---------- captions ----------
KEYS = {"overtime": "#FF7A59", "gym": "#FFD166", "cyto": "#FFD166", "6ix": "#FF7A59", "body": "#FFD166", "114": "#FF7A59", "60": "#5AE68C",
        "vigorous": "#FF7A59", "fightorflight": "#FFD166", "leafs": "#6FA8FF", "emergencies": "#FF7A59", "doctor": "#FFD166", "subscribe": "#FF7A59"}
cap_html, cap_js = C.captions(WORDS, KEYS, y=1500)

# ---------- blinks / gestures ----------
blinks = [(t, 0.1) for t in (1.3, 3.6, 6.9, 9.4, 12.2, 16.1, 18.8, 21.4, 23.2, 26.0, 28.7, 30.9, 32.6)]
SIP1 = (14.45, 0.9)       # pause after the study line
SIP2 = (33.95, 0.9)      # final sip -> loops into the hook
blinks += [(SIP1[0] + 0.25, 0.5), (SIP2[0] + 0.25, 0.6)]
gest = dict(
    waves=[0.1, wt(7, "Like")],
    points=[(wt(0, "overtime"), 0.7), (wt(2, "114") - 0.1, 0.8), (wt(3, "vigorous"), 0.7), (wt(4, "Overtime"), 0.6), (wt(6, "emergencies"), 0.8), (wt(6, "doctor") - 0.1, 0.6)],
    raises=[(wt(1, "6ix") - 0.05, 0.45), (wt(7, "out") - 0.05, 0.38)],
    sips=[SIP1, SIP2],
    tilts=[(wt(1, "inside"), 0.75, 7), (wt(5, "We"), 1.1, -8), (wt(0, "gym") - 0.1, 0.5, 6)],
    shrugs=[(wt(5, "Leafs"), 0.6)],
)
rig_js = C.rig_js(mouth, blinks, T=T, mute=[(SIP1[0], 0), (SIP2[0], 0)], **gest) + C.cup_down(CUTS[6] + 0.1, CUTS[7] - 0.15)

# ---------- transitions ----------
TRS = [("membrane", CUTS[1]), ("whip", CUTS[2]), ("zoom", CUTS[3]), ("doors", CUTS[4]), ("whip", CUTS[5]), ("membrane", CUTS[6]), ("doors", CUTS[7])]
tr_html, tr_js = zip(*[C.transition(k, t) for k, t in TRS])

# ---------- heart beat schedules ----------
def beats(t0, t1, b0, b1):
    out, t = [], t0
    while t < t1:
        out.append(round(t, 3)); bpm = b0 + (b1 - b0) * (t - t0) / max(0.01, t1 - t0); t += 60 / bpm
    return out
hb0 = beats(0.2, CUTS[1] - 0.1, 80, 160)
hb6 = beats(CUTS[6] + 0.3, CUTS[7] - 0.1, 66, 66)

def heart_svg(id_, size):
    return (f'<svg id="{id_}" class="heart" width="{size}" height="{size}" viewBox="0 0 100 100">'
            '<path d="M50 88 C20 66 4 50 4 30 C4 14 16 4 30 4 C40 4 47 10 50 17 C53 10 60 4 70 4 C84 4 96 14 96 30 C96 50 80 66 50 88 Z" fill="#E2394B" stroke="#8C1424" stroke-width="3"/>'
            '<ellipse cx="30" cy="24" rx="9" ry="6" fill="#ff8a96" opacity=".8"/></svg>')

# ECG path: repeating PQRST, 220px per beat
def ecg_path(n=40, per=110):
    d = "M0 150"
    for i in range(n):
        x = i * per
        d += f" L{x+25} 150 L{x+32} 140 L{x+39} 150 L{x+50} 150 L{x+55} 160 L{x+61} 40 L{x+67} 185 L{x+73} 150 L{x+88} 150 L{x+96} 128 L{x+104} 150"
    return d

# ---------- HTML ----------
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:InterXB; }}
#cam, #shaker {{ position:absolute; inset:0; transform-origin:540px 960px; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.bgphoto {{ position:absolute; left:-140px; top:-100px; width:1360px; height:2120px; background-size:cover; background-position:center; }}
.shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(12,22,34,.55) 0%, rgba(12,22,34,.2) 40%, rgba(12,22,34,.85) 76%, #0c1622 100%); }}
.navy {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #17304d 0%, #0c1622 70%); }}
.dots {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; background-image:radial-gradient(rgba(120,170,220,.10) 3px, transparent 4px); background-size:70px 70px; }}
.panel {{ position:absolute; left:60px; top:230px; width:960px; height:780px; border-radius:36px; background:#0f2236; border:3px solid #24425f; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,.4); }}
.ptitle {{ position:absolute; left:40px; top:30px; font:30px InterXB; color:#96b0c4; letter-spacing:.04em; }}
.card {{ position:absolute; left:440px; top:1095px; width:590px; min-height:200px; padding:26px 30px 26px 40px; border-radius:26px; background:#FAF4E8; border-left:14px solid #FF7A59; box-shadow:0 14px 30px rgba(0,0,0,.35); z-index:30; }}
.card h3 {{ font:30px InterBlack; color:#FF7A59; letter-spacing:.03em; margin-bottom:10px; }}
.card p {{ font:31px/1.3 InterSB; color:#0c1622; }}
.card.wide {{ left:110px; width:860px; top:760px; }}
.stamp {{ position:absolute; font:64px InterBlack; padding:16px 34px; border-radius:20px; white-space:nowrap; z-index:35; box-shadow:0 10px 0 rgba(0,0,0,.25); }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-170px; width:340px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
#progress {{ position:absolute; left:0; top:0; height:10px; width:1080px; background:#FF7A59; transform-origin:0 0; z-index:61; }}
.bpm {{ position:absolute; font:150px InterBlack; color:#FAF4E8; text-align:right; }}
.unit {{ position:absolute; font:34px InterXB; color:#FAF4E8; }}
.heart {{ position:absolute; }}
.gauge {{ position:absolute; top:150px; width:340px; height:340px; }}
.needle {{ position:absolute; left:167px; top:40px; width:8px; height:140px; border-radius:4px; background:#FAF4E8; transform-origin:4px 140px; }}
.hub {{ position:absolute; left:155px; top:165px; width:32px; height:32px; border-radius:50%; background:#FAF4E8; }}
.glab {{ position:absolute; top:225px; width:340px; text-align:center; font:34px InterBlack; color:#FAF4E8; }}
.gsub {{ position:absolute; top:272px; width:340px; text-align:center; font:30px InterXB; }}
.bar {{ position:absolute; left:60px; height:56px; border-radius:16px; width:10px; }}
.blab {{ position:absolute; left:60px; font:34px InterXB; color:#FAF4E8; }}
.bval {{ position:absolute; font:42px InterBlack; color:#FAF4E8; }}
.btn {{ position:absolute; font:52px InterBlack; padding:22px 44px; border-radius:22px; white-space:nowrap; z-index:40; }}
.src {{ position:absolute; left:110px; width:860px; top:250px; padding:26px 34px; border-radius:26px; background:rgba(12,22,34,.86); border:3px solid #FFD166; z-index:40; }}
.src h3 {{ font:28px InterBlack; color:#FFD166; letter-spacing:.05em; margin-bottom:10px; }}
.src p {{ font:30px/1.35 InterSB; color:#FAF4E8; }}
{C.rig_css()}
{C.CAP_CSS}
{C.TR_CSS}
#cytoLayer {{ position:absolute; inset:0; z-index:20; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="shaker" class="clip" data-start="0" data-duration="{T}"><div id="cam">

  <!-- S0 hook -->
  <div id="s0" class="scene clip" data-start="0" data-duration="{CUTS[1]}">
    <div id="bg0" class="bgphoto" style="background-image:url(assets/bg.jpg)"></div><div class="shade"></div>
    {heart_svg("h0", 230)}
    <div id="bpm0" class="bpm" style="left:560px; top:300px; width:300px; text-align:left; font-size:120px">80</div>
    <div class="unit" style="left:565px; top:440px">BPM</div>
    <div id="st0" class="stamp" style="left:150px; top:600px; background:#FF7A59; color:#FAF4E8">OVERTIME = WORKOUT?!</div>
  </div>

  <!-- S1 intro -->
  <div id="s1" class="scene clip" data-start="{CUTS[1]}" data-duration="{CUTS[2]-CUTS[1]}">
    <div id="bg1" class="bgphoto" style="background-image:url(assets/bg2.jpg)"></div><div class="shade"></div>
    <div id="st1" class="stamp" style="left:190px; top:360px; background:#FFD166; color:#0c1622; font-size:72px">LIVE FROM THE 6IX</div>
    <div id="st1b" class="stamp" style="left:270px; top:530px; background:#3CC4B0; color:#0c1622; font-size:48px">…INSIDE YOUR BODY</div>
  </div>

  <!-- S2 study / ECG -->
  <div id="s2" class="scene clip" data-start="{CUTS[2]}" data-duration="{CUTS[3]-CUTS[2]}">
    <div class="navy"></div><div id="dots2" class="dots"></div>
    <div id="pn2" class="panel">
      <div class="ptitle">HEART MONITOR · HOCKEY FAN</div>
      <div id="bpm2" class="bpm" style="right:40px; top:70px; color:#5AE68C">60</div>
      <div class="unit" style="right:44px; top:235px">BPM</div>
      <svg style="position:absolute; left:0; top:300px" width="960" height="300"><g id="ecg"><path d="{ecg_path()}" fill="none" stroke="#FF7A59" stroke-width="6" stroke-linejoin="round"/></g></svg>
      <div style="position:absolute; left:40px; bottom:30px; font:24px InterSB; color:#7892a6">Montreal Canadiens fans · Holter monitors</div>
    </div>
    <div id="cd2" class="card"><h3>CAN J CARDIOL, 2017</h3><p>20 healthy fans wore heart monitors during games.</p></div>
  </div>

  <!-- S3 fight-or-flight -> gauges -->
  <div id="s3" class="scene clip" data-start="{CUTS[3]}" data-duration="{CUTS[4]-CUTS[3]}">
    <div class="navy"></div><div id="dots3" class="dots"></div>
    <div id="pn3" class="panel">
      <img id="ff" src="assets/ff.png" style="position:absolute; left:30px; top:80px; width:900px">
      <div style="position:absolute; left:0; top:0; width:960px; height:76px; background:#0f2236"></div>
      <div class="ptitle">FIGHT-OR-FLIGHT · diagram: Mermaid</div>
      <div id="gz" style="position:absolute; inset:0; background:#0f2236; opacity:0">
        <div style="position:absolute; top:44px; width:960px; text-align:center; font:40px InterBlack; color:#FAF4E8">HOW HARD YOUR HEART WORKS</div>
        <div class="gauge" style="left:60px"><svg width="340" height="200"><path d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#2a4866" stroke-width="30"/><path id="arcA" d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#FFD166" stroke-width="30" stroke-dasharray="440" stroke-dashoffset="440"/></svg>
          <div id="ndA" class="needle"></div><div class="hub"></div><div class="glab">ON TV</div><div class="gsub" style="color:#FFD166">moderate</div></div>
        <div class="gauge" style="left:560px"><svg width="340" height="200"><path d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#2a4866" stroke-width="30"/><path id="arcB" d="M30 180 A140 140 0 0 1 310 180" fill="none" stroke="#FF7A59" stroke-width="30" stroke-dasharray="440" stroke-dashoffset="440"/></svg>
          <div id="ndB" class="needle"></div><div class="hub"></div><div class="glab">AT THE ARENA</div><div class="gsub" style="color:#FF7A59">vigorous</div></div>
      </div>
    </div>
    <div id="cd3a" class="card"><h3>FIGHT-OR-FLIGHT</h3><p>Your sympathetic nervous system revs the heart up.</p></div>
    <div id="cd3b" class="card" style="opacity:0"><h3>SAME STUDY</h3><p>Live game = vigorous exercise. TV = moderate.</p></div>
  </div>

  <!-- S4 peaks -->
  <div id="s4" class="scene clip" data-start="{CUTS[4]}" data-duration="{CUTS[5]-CUTS[4]}">
    <div class="navy"></div><div id="dots4" class="dots"></div>
    <div id="pn4" class="panel">
      <div style="position:absolute; left:40px; top:34px; font:40px InterBlack; color:#FAF4E8">When fans' heart rate peaked</div>
      <div style="position:absolute; left:40px; top:90px; font:26px InterSB; color:#96b0c4">share of peaks · Can J Cardiol 2017</div>
      <div class="blab" style="top:190px">Overtime</div><div id="b1" class="bar" style="top:240px; background:#FF7A59"></div><div id="v1" class="bval" style="top:244px">40%</div>
      <div class="blab" style="top:360px">Scoring chance FOR</div><div id="b2" class="bar" style="top:410px; background:#FFD166"></div><div id="v2" class="bval" style="top:414px">25%</div>
      <div class="blab" style="top:530px">Scoring chance AGAINST</div><div id="b3" class="bar" style="top:580px; background:#7896b0"></div><div id="v3" class="bval" style="top:584px">15%</div>
    </div>
    <div id="st4" class="stamp" style="left:520px; top:700px; background:#FF7A59; color:#FAF4E8">OVERTIME</div>
    <div id="cd4" class="card"><h3>40% OF PEAKS</h3><p>Overtime was the #1 moment hearts maxed out.</p></div>
  </div>

  <!-- S5 leafs joke -->
  <div id="s5" class="scene clip" data-start="{CUTS[5]}" data-duration="{CUTS[6]-CUTS[5]}">
    <div id="bg5" class="bgphoto" style="background-image:url(assets/bg.jpg)"></div><div class="shade"></div>
    <div id="st5a" class="stamp" style="left:200px; top:400px; background:#1E4FA8; color:#FAF4E8; font-size:84px">LEAFS FANS??</div>
    <div id="st5b" class="stamp" style="left:220px; top:580px; background:#FFD166; color:#0c1622; font-size:48px">WE DON'T WANNA KNOW</div>
  </div>

  <!-- S6 serious -->
  <div id="s6" class="scene clip" data-start="{CUTS[6]}" data-duration="{CUTS[7]-CUTS[6]}">
    <div class="navy"></div><div id="dots6" class="dots"></div>
    {heart_svg("h6", 250)}
    <div id="bpm6" class="bpm" style="left:390px; top:330px; width:300px; text-align:center; font-size:96px; color:#FAF4E8">66</div>
    <div class="unit" style="left:500px; top:440px; color:#FAF4E8">BPM</div>
    <div id="cd6a" class="card wide" style="top:600px"><h3>NEJM, 2008</h3><p>Cardiac emergencies hit 2.66x on World Cup match days in Munich.</p></div>
    <div id="cd6b" class="card wide" style="top:600px; opacity:0"><h3>NOT MEDICAL ADVICE</h3><p>Heart condition? Talk to your doctor before big-game nights.</p></div>
  </div>

  <!-- S7 outro -->
  <div id="s7" class="scene clip" data-start="{CUTS[7]}" data-duration="{T-CUTS[7]}">
    <div id="bg7" class="bgphoto" style="background-image:url(assets/bg.jpg)"></div><div class="shade"></div>
    <div id="src" class="src"><h3>SOURCES · PUBMED</h3><p>Khairy et al., Can J Cardiol 2017<br>Wilbert-Lampen et al., N Engl J Med 2008</p></div>
    <div id="like" class="btn" style="left:130px; top:560px; background:#FAF4E8; color:#0c1622">♥ LIKE</div>
    <div id="sub" class="btn" style="left:480px; top:560px; background:#E2394B; color:#FAF4E8">SUBSCRIBE</div>
    <div id="subd" class="btn" style="left:480px; top:560px; background:#5d6770; color:#FAF4E8; opacity:0">SUBSCRIBED ✓</div>
    <svg id="cursor" style="position:absolute; left:900px; top:820px; z-index:45" width="70" height="90" viewBox="0 0 70 90"><path d="M5 5 L5 70 L22 55 L34 82 L46 76 L34 50 L58 50 Z" fill="#FAF4E8" stroke="#0c1622" stroke-width="5" stroke-linejoin="round"/></svg>
    <svg id="bell" style="position:absolute; left:930px; top:560px; z-index:45" width="100" height="110" viewBox="0 0 100 110"><path d="M50 10 C28 10 20 30 20 50 L20 70 L10 82 L90 82 L80 70 L80 50 C80 30 72 10 50 10 Z" fill="#FFD166" stroke="#0c1622" stroke-width="5"/><circle cx="50" cy="94" r="10" fill="#FFD166" stroke="#0c1622" stroke-width="5"/></svg>
    {''.join(f'<svg id="hz{i}" class="heart" style="left:{150+i*55}px; top:640px; z-index:44" width="60" height="60" viewBox="0 0 100 100"><path d="M50 88 C20 66 4 50 4 30 C4 14 16 4 30 4 C40 4 47 10 50 17 C53 10 60 4 70 4 C84 4 96 14 96 30 C96 50 80 66 50 88 Z" fill="#E2394B"/></svg>' for i in range(5))}
  </div>

  <div id="cytoLayer">{C.rig_html("outfit_jersey", "cup_blue")}</div>
</div></div>
<div id="pill" class="clip" data-start="0" data-duration="{T}">THE BODY IS THE 6IX</div>
<div id="progress" class="clip" data-start="0" data-duration="{T}"></div>
{cap_html}
{''.join(tr_html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const T = {T};
// progress bar + header
tl.fromTo("#progress",{{scaleX:0}},{{scaleX:1,duration:T,ease:"none"}},0);
tl.fromTo("#pill",{{y:-140}},{{y:0,duration:0.4,ease:"back.out(2)"}},0.1);
tl.set("#shaker",{{x:0,y:0,scale:1}},0); tl.set("#cam",{{scale:1}},0);
// ---- camera: slow push per scene, punches on hits, shakes on "bro WHAT" beats
const CUTS = {CUTS};
for (let i=0;i<CUTS.length-1;i++) tl.fromTo("#cam",{{scale:1.0}},{{scale:1.05,duration:CUTS[i+1]-CUTS[i]-0.05,ease:"none",immediateRender:false}},CUTS[i]+0.01);
const punch=(t)=>{{ tl.to("#shaker",{{scale:1.08,duration:0.08,ease:"power2.out"}},t); tl.to("#shaker",{{scale:1,duration:0.3,ease:"power2.inOut"}},t+0.08); }};
const shake=(t)=>{{ [[-12,7],[10,-8],[-7,5],[5,-3],[0,0]].forEach((p,i)=>tl.to("#shaker",{{x:p[0],y:p[1],duration:0.04}},t+i*0.04)); }};
[{wt(0,"overtime")},{wt(1,"6ix")},{wt(2,"114")},{wt(4,"Overtime")},{wt(7,"subscribe")+0.55}].forEach(punch);
[{wt(0,"Bro")},{wt(5,"Leafs")},{wt(6,"emergencies")},{wt(7,"out")+0.35}].forEach(shake);
// ---- Cyto placement (moves between host / corner / mid) + entrance
tl.set("#cytoPos",{json.dumps(HOST)},0);
tl.fromTo("#cyto",{{y:500}},{{y:0,duration:0.45,ease:"back.out(1.5)",immediateRender:false}},0);
{chr(10).join(f'tl.to("#cytoPos",{json.dumps({**v, "duration":0.4, "ease":"power3.inOut"})},{t-0.2:.3f});' for t, v in place[1:])}
{rig_js}
// ---- Ken Burns on every photo / figure
["#bg0","#bg1","#bg5","#bg7"].forEach((b,i)=>{{ const s=[CUTS[0],CUTS[1],CUTS[5],CUTS[7]][i], e=[CUTS[1],CUTS[2],CUTS[6],T][i];
  tl.fromTo(b,{{x:i%2?-60:0,y:0,scale:1.0}},{{x:i%2?20:-80,y:-50,scale:1.09,duration:e-s,ease:"none"}},s); }});
["#dots2","#dots3","#dots4","#dots6"].forEach((b,i)=>{{ const s=[CUTS[2],CUTS[3],CUTS[4],CUTS[6]][i], e=[CUTS[3],CUTS[4],CUTS[5],CUTS[7]][i];
  tl.fromTo(b,{{x:0,y:0}},{{x:70,y:140,duration:e-s,ease:"none"}},s); }});
// ---- S0: racing heart + BPM climbing
tl.set("#h0",{{left:300,top:250}},0);
{chr(10).join(f'tl.fromTo("#h0",{{scale:1.18}},{{scale:1,duration:0.22,ease:"power2.out"}},{b});' for b in hb0)}
tl.fromTo("#bpm0",{{innerText:80}},{{innerText:160,snap:{{innerText:1}},duration:{CUTS[1]-0.5},ease:"power1.in"}},0.2);
tl.fromTo("#st0",{{scale:2.2,opacity:0,rotation:-4}},{{scale:1,opacity:1,rotation:-4,duration:0.25,ease:"back.out(2.5)"}},{wt(0,"gym")-0.2});
// ---- S1
tl.fromTo("#st1",{{scale:0,rotation:-12}},{{scale:1,rotation:-3,duration:0.3,ease:"back.out(2.5)"}},{wt(1,"live")-0.05});
tl.fromTo("#st1b",{{x:-900}},{{x:0,rotation:3,duration:0.3,ease:"power3.out"}},{wt(1,"inside")-0.05});
tl.to("#st1",{{y:-12,duration:0.5,yoyo:true,repeat:5,ease:"sine.inOut"}},{wt(1,"live")+0.3});
// ---- S2: ECG scroll (speeds up), BPM 60 -> 114, card
tl.fromTo("#pn2",{{y:900}},{{y:0,duration:0.45,ease:"power3.out"}},{CUTS[2]});
tl.fromTo("#ecg",{{x:0}},{{x:-1900,duration:{CUTS[3]-CUTS[2]},ease:"power1.in"}},{CUTS[2]});
tl.fromTo("#bpm2",{{innerText:60}},{{innerText:114,snap:{{innerText:1}},duration:{wt(2,"114","t1")-wt(2,"jumped")},ease:"power2.in"}},{wt(2,"jumped")});
tl.to("#bpm2",{{color:"#FF7A59",duration:0.3}},{wt(2,"114")-0.4});
tl.fromTo("#bpm2",{{scale:1.35}},{{scale:1,duration:0.3,ease:"back.out(3)"}},{wt(2,"114")});
tl.fromTo("#cd2",{{x:700}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{wt(2,"Scientists")+0.2});
// ---- S3: Mermaid diagram pans + scales in, then gauges
tl.fromTo("#ff",{{y:0,scale:1.05}},{{y:{-(FFH-640)},scale:1,duration:{wt(3,"arena")-CUTS[3]},ease:"power1.inOut"}},{CUTS[3]});
tl.fromTo("#cd3a",{{x:700}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{wt(3,"fight")});
tl.to("#gz",{{opacity:1,duration:0.25}},{wt(3,"arena")-0.15});
tl.fromTo("#gz",{{scale:1.3}},{{scale:1,duration:0.35,ease:"power3.out"}},{wt(3,"arena")-0.15});
tl.fromTo("#ndA",{{rotation:-90}},{{rotation:5,duration:0.7,ease:"back.out(1.6)"}},{wt(3,"arena")+0.1});
tl.fromTo("#arcA",{{attr:{{"stroke-dashoffset":440}}}},{{attr:{{"stroke-dashoffset":209}},duration:0.7,ease:"power2.out"}},{wt(3,"arena")+0.1});
tl.fromTo("#ndB",{{rotation:-90}},{{rotation:68,duration:0.8,ease:"back.out(1.6)"}},{wt(3,"vigorous")-0.1});
tl.fromTo("#arcB",{{attr:{{"stroke-dashoffset":440}}}},{{attr:{{"stroke-dashoffset":53}},duration:0.8,ease:"power2.out"}},{wt(3,"vigorous")-0.1});
tl.to("#ndB",{{rotation:63,duration:0.08,yoyo:true,repeat:7}},{wt(3,"vigorous")+0.75});
tl.to("#cd3a",{{opacity:0,duration:0.15}},{wt(3,"arena")}); tl.fromTo("#cd3b",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.6)"}},{wt(3,"arena")+0.05});
// ---- S4: bars grow, OVERTIME stamp
[["#b1","#v1",0.40],["#b2","#v2",0.25],["#b3","#v3",0.15]].forEach(([b,v,f],i)=>{{ const t={CUTS[4]+0.15}+i*0.18;
  tl.fromTo(b,{{width:10}},{{width:10+1780*f,duration:0.6,ease:"power3.out"}},t);
  tl.fromTo(v,{{x:80,opacity:0}},{{x:100+1780*f,opacity:1,duration:0.6,ease:"power3.out"}},t); }});
tl.fromTo("#st4",{{scale:2.4,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:-6,duration:0.22,ease:"back.out(2.5)"}},{wt(4,"Overtime")-0.05});
tl.fromTo("#cd4",{{x:700}},{{x:0,duration:0.3,ease:"back.out(1.4)"}},{CUTS[4]+0.25});
// ---- S5: Leafs joke stamps
tl.fromTo("#st5a",{{scale:2.6,opacity:0,rotation:-5}},{{scale:1,opacity:1,rotation:-5,duration:0.22,ease:"back.out(2.5)"}},{wt(5,"Leafs")-0.05});
tl.fromTo("#st5b",{{scale:0,rotation:10}},{{scale:1,rotation:4,duration:0.3,ease:"back.out(2.5)"}},{wt(5,"don't")-0.1});
tl.to("#st5a",{{rotation:-2,duration:0.12,yoyo:true,repeat:9}},{wt(5,"Leafs")+0.3});
// ---- S6: calm heart, cards swap
tl.set("#h6",{{left:415,top:230}},{CUTS[6]});
{chr(10).join(f'tl.fromTo("#h6",{{scale:1.08}},{{scale:1,duration:0.35,ease:"power2.out"}},{b});' for b in hb6)}
tl.fromTo("#cd6a",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{wt(6,"emergencies")-0.3});
tl.to("#cd6a",{{opacity:0,y:-30,duration:0.2}},{wt(6,"Not")-0.1});
tl.fromTo("#cd6b",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"power3.out"}},{wt(6,"Not")-0.05});
// ---- S7: outro — like hearts, cursor clicks subscribe, bell rings, sources
tl.fromTo("#src",{{y:-200,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(1.5)"}},{CUTS[7]+0.1});
tl.fromTo("#like",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2.5)"}},{wt(7,"Like")});
tl.fromTo("#sub",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2.5)"}},{wt(7,"Like")+0.15});
tl.fromTo("#bell",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2.5)"}},{wt(7,"Like")+0.3});
[0,1,2,3,4].forEach(i=>tl.fromTo("#hz"+i,{{y:0,opacity:0,scale:0.5}},{{y:-260-i*30,x:(i-2)*30,opacity:0,scale:1.2,duration:1.0,ease:"power1.out",keyframes:{{opacity:[0,1,1,0]}}}},{wt(7,"Like")+0.25}+i*0.07));
tl.fromTo("#cursor",{{x:0,y:0}},{{x:-260,y:-210,duration:0.45,ease:"power2.inOut"}},{wt(7,"subscribe")});
tl.to("#cursor",{{scale:0.85,duration:0.08,yoyo:true,repeat:1}},{wt(7,"subscribe")+0.5});
tl.set("#sub",{{opacity:0}},{wt(7,"subscribe")+0.55}); tl.set("#subd",{{opacity:1}},{wt(7,"subscribe")+0.55});
tl.fromTo("#subd",{{scale:1.15}},{{scale:1,duration:0.25,ease:"back.out(3)"}},{wt(7,"subscribe")+0.55});
tl.to("#bell",{{rotation:18,duration:0.07,yoyo:true,repeat:9,transformOrigin:"50% 10%"}},{wt(7,"subscribe")+0.6});
// ---- transitions + captions
{chr(10).join(tr_js)}
{cap_js}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
json.dump({"name": "ep07"}, open("meta.json", "w"))
print("built", len(html), "bytes; mouth changes", len(mouth))
