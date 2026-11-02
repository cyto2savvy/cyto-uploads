"""Shared HyperFrames helpers for Cyto episodes (rig, mouth sync, blinks, captions, transitions).
Coordinates: stage 1080x1920. Rig canvas 1200x1200, body centre (600,640).
"""
import json, re, subprocess, numpy as np, shutil, os

RIG_DIR = "/home/claude/cyto2/rig"
RIG = json.load(open(f"{RIG_DIR}/rig.json"))
SH_L, HAND_L, SH_R = RIG["shoulder_left"], RIG["hand_left"], RIG["shoulder_right"]
CW, CH = RIG["cup_size"]
CUP_LEFT = HAND_L[0] + .22 * CW - CW / 2
CUP_TOP = HAND_L[1] - .80 * CH
FONTS = ["/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
         "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"]


def place(X, Y, s):
    """GSAP vars to put Cyto's body centre at stage (X,Y) at scale s."""
    return {"x": round(X - 600 * s, 1), "y": round(Y - 640 * s, 1), "scale": s}


def copy_assets(proj, extra=()):
    a = os.path.join(proj, "assets"); os.makedirs(a, exist_ok=True)
    for f in os.listdir(RIG_DIR):
        if f.endswith(".png") and f != "rig_sheet.png":
            shutil.copy(os.path.join(RIG_DIR, f), a)
    for f in FONTS: shutil.copy(f, a)
    shutil.copy("/home/claude/hf/node_modules/gsap/dist/gsap.min.js", a)
    for src, dst in extra: shutil.copy(src, os.path.join(a, dst))


def mouth_track(voice_wav, words, fps=30, o_words=()):
    SR = 16000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", voice_wav, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    hop = SR // fps
    rms = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)])
    rms /= np.percentile(rms, 98)
    track, prev, hold = [], None, 0
    for f, e in enumerate(rms):
        t = f / fps
        w = next((w for w in words if w["t0"] - .03 <= t <= w["t1"] + .03), None)
        wn = re.sub(r"[^a-z0-9]", "", w["w"].lower()) if w else ""
        if e < 0.08: s = "closed"
        elif wn in o_words and e > 0.25: s = "o"
        elif e > 0.50: s = "wide"
        else: s = "small"
        if s != prev and hold <= 0:
            track.append([round(t, 3), s]); prev = s; hold = 2
        hold -= 1
    return track


def rig_html(outfit="outfit_jersey", cup="cup_blue"):
    of = f'<img class="L" src="assets/{outfit}.png">' if outfit else ""
    return f"""
<div id="cytoPos"><div id="cyto">
  <div id="armR" class="G"><img class="L" src="assets/arm_right.png"><img class="L" src="assets/hand_right.png"></div>
  <img class="L" src="assets/body.png">{of}
  <img class="L" src="assets/outfit_toque.png">
  <img id="eo" class="L" src="assets/eyes_open.png"><img id="ec" class="L" src="assets/eyes_closed.png" style="opacity:0">
  <img id="m_closed" class="L" src="assets/mouth_closed.png">
  <img id="m_small" class="L" src="assets/mouth_small.png" style="opacity:0">
  <img id="m_wide" class="L" src="assets/mouth_wide.png" style="opacity:0">
  <img id="m_o" class="L" src="assets/mouth_o.png" style="opacity:0">
  <img id="cupTable" src="assets/{cup}.png">
  <div id="armL" class="G"><img class="L" src="assets/arm_left.png"><img id="cup" src="assets/{cup}.png"><img class="L" src="assets/hand_left.png"></div>
</div></div>"""


def rig_css():
    return f"""
#cytoPos {{ position:absolute; left:0; top:0; width:1200px; height:1200px; transform-origin:0 0; }}
#cyto {{ position:absolute; left:0; top:0; width:1200px; height:1200px; transform-origin:600px 960px; }}
#cyto .L, #cyto .G {{ position:absolute; left:0; top:0; width:1200px; height:1200px; }}
#armL {{ transform-origin:{SH_L[0]}px {SH_L[1]}px; }}
#armR {{ transform-origin:{SH_R[0]}px {SH_R[1]}px; }}
#cup {{ position:absolute; left:{CUP_LEFT:.1f}px; top:{CUP_TOP:.1f}px; width:{CW}px; height:{CH}px; transform-origin:{HAND_L[0]-CUP_LEFT:.1f}px {HAND_L[1]-CUP_TOP:.1f}px; }}
#cupTable {{ position:absolute; left:{140}px; top:{975 - CH}px; width:{CW}px; height:{CH}px; opacity:0; }}
"""


def rig_js(mouth, blinks, sips=(), raises=(), waves=(), points=(), tilts=(), shrugs=(), T=30.0, mute=()):
    """Return JS (string) adding all puppet animation to `tl`."""
    js = [f"const MOUTH={json.dumps(mouth)};",
          'const MO=["#m_closed","#m_small","#m_wide","#m_o"];',
          'MOUTH.forEach(([t,s])=>{MO.forEach(m=>tl.set(m,{opacity:0},t)); tl.set("#m_"+s,{opacity:1},t);});']
    for a, b in mute:   # force closed mouth (sips)
        js.append(f'MO.forEach(m=>tl.set(m,{{opacity:0}},{a})); tl.set("#m_closed",{{opacity:1}},{a});')
    js.append(f'tl.fromTo("#cyto",{{y:0,scaleY:1,scaleX:1}},{{y:-12,scaleY:1.022,scaleX:0.988,duration:0.32,ease:"sine.inOut",repeat:{int((T-0.5)/0.32)},yoyo:true,immediateRender:false}},0.46);')
    for t, d in blinks:
        js.append(f'tl.set("#ec",{{opacity:1}},{t});tl.set("#eo",{{opacity:0}},{t});tl.set("#ec",{{opacity:0}},{t+d});tl.set("#eo",{{opacity:1}},{t+d});')
    for t in waves:
        js.append(f'tl.to("#armR",{{rotation:-118,duration:0.2,ease:"back.out(2)"}},{t});')
        for i, a in enumerate((-100, -128, -102, -125)):
            js.append(f'tl.to("#armR",{{rotation:{a},duration:0.13,ease:"sine.inOut"}},{t+0.2+i*0.13:.3f});')
        js.append(f'tl.to("#armR",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t+0.75:.3f});')
    for t, d in points:
        js.append(f'tl.to("#armR",{{rotation:-118,duration:0.18,ease:"back.out(2)"}},{t});tl.to("#armR",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t+d});')
    for t, d in shrugs:
        js.append(f'tl.to("#armR",{{rotation:-60,duration:0.18,ease:"back.out(2)"}},{t});tl.to("#armR",{{rotation:0,duration:0.3}},{t+d});')
    for t, d, ang in tilts:
        js.append(f'tl.to("#cyto",{{rotation:{ang},duration:0.18,ease:"power2.out"}},{t});tl.to("#cyto",{{rotation:0,duration:0.35,ease:"power2.inOut"}},{t+d});')
    for t, d in raises:   # "cheers"
        js.append(f'tl.to("#armL",{{rotation:-28,duration:0.2,ease:"back.out(2)"}},{t});tl.to("#cup",{{rotation:28,duration:0.2,ease:"back.out(2)"}},{t});'
                  f'tl.to("#armL",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t+d});tl.to("#cup",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t+d});')
    for t, d in sips:
        js.append(f'tl.to("#armL",{{rotation:-42,duration:0.28,ease:"power2.out"}},{t});tl.to("#cup",{{rotation:94,duration:0.28,ease:"power2.out"}},{t});'
                  f'tl.to("#cup",{{rotation:102,duration:{(d-0.6)/2:.3f},ease:"sine.inOut",yoyo:true,repeat:1}},{t+0.28:.3f});'
                  f'tl.to("#armL",{{rotation:0,duration:0.28,ease:"power2.inOut"}},{t+d-0.28:.3f});tl.to("#cup",{{rotation:0,duration:0.28,ease:"power2.inOut"}},{t+d-0.28:.3f});')
    return "\n".join(js)


def cup_down(t0, t1):
    """Serious moment: lower the hand, put the cup on the 'table' beside Cyto, pick it back up at t1."""
    return (f'tl.to("#armL",{{rotation:12,duration:0.3,ease:"power2.inOut"}},{t0});'
            f'tl.to("#cup",{{opacity:0,duration:0.12}},{t0+0.15});tl.fromTo("#cupTable",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.25,ease:"bounce.out"}},{t0+0.15});'
            f'tl.to("#cupTable",{{opacity:0,duration:0.12}},{t1});tl.to("#cup",{{opacity:1,duration:0.12}},{t1});'
            f'tl.to("#armL",{{rotation:0,duration:0.3,ease:"back.out(2)"}},{t1});')


def captions(words, keys, y=1500, max_words=4):
    """Word-by-word karaoke captions in chunks. Returns (html, js)."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        long_ = sum(len(words[j]["w"]) for j in cur) > 17
        if len(cur) >= max_words or long_ or re.search(r"[.,?!:]$", w["w"]) or (i + 1 < len(words) and words[i + 1]["t0"] - w["t1"] > 0.25):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    html, js = [], []
    for ci, ch in enumerate(chunks):
        a = words[ch[0]]["t0"] - 0.05
        b = words[chunks[ci + 1][0]]["t0"] - 0.05 if ci + 1 < len(chunks) else words[ch[-1]]["t1"] + 1.2
        spans = []
        for i in ch:
            raw = words[i]["w"]; key = re.sub(r"[^A-Za-z0-9]", "", raw).lower()
            col = keys.get(key)
            st = f' style="color:{col}"' if col else ""
            spans.append(f'<span id="w{i}" class="w{" key" if col else ""}"{st}>{raw.upper()}</span>')
            js.append(f'tl.fromTo("#w{i}",{{opacity:0,scale:{1.6 if col else 1.25},y:18}},{{opacity:1,scale:1,y:0,duration:{0.22 if col else 0.14},ease:"back.out(2.4)"}},{words[i]["t0"] - 0.03:.3f});')
        html.append(f'<div id="cap{ci}" class="cap clip" data-start="{a:.3f}" data-duration="{b - a:.3f}" style="top:{y}px">{" ".join(spans)}</div>')
    return "\n".join(html), "\n".join(js)


CAP_CSS = """
.cap { position:absolute; left:50px; right:50px; text-align:center; font:72px/1.1 InterBlack; color:#FAF4E8; -webkit-text-stroke:3px #0c1622; paint-order:stroke fill; text-shadow:0 6px 0 rgba(0,0,0,.35); z-index:50; }
.w { display:inline-block; opacity:0; }
.key { font-size:90px; }
"""

FONT_CSS = """
@font-face { font-family:"InterBlack"; src:url("assets/InterDisplay-Black.otf"); }
@font-face { font-family:"InterXB"; src:url("assets/Inter-ExtraBold.otf"); }
@font-face { font-family:"InterSB"; src:url("assets/Inter-SemiBold.otf"); }
"""


def transition(kind, t):
    """Overlay transition centred on cut time t. Returns (html, js). kinds: whip, membrane, doors, zoom."""
    i = int(t * 1000)
    if kind == "whip":
        h = f'<div id="tr{i}" class="clip trw" data-start="{t-0.2:.3f}" data-duration="0.4"></div>'
        j = f'tl.fromTo("#tr{i}",{{x:-1500}},{{x:1500,duration:0.4,ease:"power2.inOut"}},{t-0.2:.3f});tl.fromTo("#shaker",{{x:0}},{{x:-60,duration:0.18,ease:"power2.in",yoyo:true,repeat:1}},{t-0.18:.3f});'
    elif kind == "membrane":
        h = f'<div id="tr{i}" class="clip trm" data-start="{t-0.25:.3f}" data-duration="0.55"></div>'
        j = f'tl.fromTo("#tr{i}",{{scale:0,opacity:1}},{{scale:1,duration:0.25,ease:"power2.in"}},{t-0.25:.3f});tl.to("#tr{i}",{{scale:2.4,opacity:0,duration:0.3,ease:"power2.out"}},{t:.3f});'
    elif kind == "doors":
        h = (f'<div id="trA{i}" class="clip trd" data-start="{t-0.25:.3f}" data-duration="0.6" style="left:-540px"><div class="win"></div></div>'
             f'<div id="trB{i}" class="clip trd" data-start="{t-0.25:.3f}" data-duration="0.6" style="left:1080px"><div class="win"></div></div>')
        j = (f'tl.fromTo("#trA{i}",{{x:0}},{{x:540,duration:0.22,ease:"power3.in"}},{t-0.25:.3f});tl.fromTo("#trB{i}",{{x:0}},{{x:-540,duration:0.22,ease:"power3.in"}},{t-0.25:.3f});'
             f'tl.to("#trA{i}",{{x:0,duration:0.3,ease:"power3.out"}},{t+0.05:.3f});tl.to("#trB{i}",{{x:0,duration:0.3,ease:"power3.out"}},{t+0.05:.3f});')
    else:  # zoom-through
        h = f'<div id="tr{i}" class="clip trz" data-start="{t-0.15:.3f}" data-duration="0.35"></div>'
        j = (f'tl.fromTo("#tr{i}",{{opacity:0}},{{opacity:0.9,duration:0.15}},{t-0.15:.3f});tl.to("#tr{i}",{{opacity:0,duration:0.2}},{t:.3f});'
             f'tl.fromTo("#shaker",{{scale:1.5}},{{scale:1.0,duration:0.35,ease:"power3.out"}},{t:.3f});')
    return h, j


TR_CSS = """
.trw { position:absolute; top:0; left:0; width:1400px; height:1920px; z-index:90; background:linear-gradient(90deg, rgba(255,122,89,0) 0%, #FF7A59 25%, #FFD166 50%, #FF7A59 75%, rgba(255,122,89,0) 100%); filter:blur(6px); }
.trm { position:absolute; left:-460px; top:-40px; width:2000px; height:2000px; border-radius:50%; z-index:90; background:radial-gradient(circle, #3CC4B0 0 62%, #1E8C80 62% 70%, rgba(30,140,128,.0) 71%); }
.trd { position:absolute; top:0; width:540px; height:1920px; z-index:90; background:linear-gradient(90deg,#9aa3ab,#d6dde2 50%,#9aa3ab); border-left:10px solid #C8102E; border-right:10px solid #C8102E; }
.trd .win { position:absolute; left:90px; right:90px; top:420px; height:520px; border-radius:24px; background:#1b2733; border:10px solid #5d6770; }
.trz { position:absolute; inset:0; z-index:90; background:#FAF4E8; opacity:0; }
"""


# =====================================================================================
# v2 (Ep 8 onward) — approved Oct 30 2026 after the v2 test (studio/hf/v2test).
#   1. Everything readable stays in the Shorts SAFE zone (YouTube's title/buttons cover the rest).
#   2. Cyto is big (CYTO_V2) and on screen the whole time — never a corner sticker.
#   3. Diagrams: Mermaid in the Cyto theme, inlined as SVG, built node-by-node (mermaid_svg + mermaid_js).
#   4. One LottieFiles animation per science scene where it fits (lottie_js). Fetch JSON via lottie/list.txt.
#   5. Hard cap ~30s.
# =====================================================================================
V2_DIR = "/home/claude/hf/v2"
SAFE = dict(left=60, right=940, top=200, bottom=1480)       # 1080x1920 stage
CYTO_V2 = place(300, 1300, 0.56)                            # Cyto lower-left, big
CAP_Y_V2 = 880                                              # captions under the figure panel
MAX_T_V2 = 60.0  # was 45 (Nov 2 2026, Utsha: shorts up to 60s, series = '6ixty Seconds of Science'); 30.5 before Nov 1

V2_CSS = """
.panel { position:absolute; left:60px; top:200px; width:880px; height:650px; border-radius:36px; background:#0f2236; border:3px solid #24425f; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,.4); }
.ptitle { position:absolute; left:36px; top:28px; font:28px InterXB; color:#96b0c4; letter-spacing:.04em; }
.card { position:absolute; left:560px; top:1090px; width:380px; padding:24px 26px 24px 34px; border-radius:26px; background:#FAF4E8; border-left:14px solid #FF7A59; box-shadow:0 14px 30px rgba(0,0,0,.35); z-index:30; }
.card h3 { font:28px InterBlack; color:#FF7A59; letter-spacing:.03em; margin-bottom:8px; }
.card p { font:32px/1.25 InterSB; color:#0c1622; }
.cap { left:60px; right:140px; }
.mmd { position:absolute; left:70px; top:90px; width:740px; height:540px; }
.mmd .nodeLabel, .mmd .nodeLabel p { font-family:InterBlack !important; }
"""


def copy_assets_v2(proj, extra=(), lotties=()):
    """copy_assets + lottie player + any Lottie JSON from the repo's lottie/ folder."""
    copy_assets(proj, extra)
    a = os.path.join(proj, "assets")
    shutil.copy("/home/claude/hf/node_modules/lottie-web/build/player/lottie_svg.min.js", a)
    for n in lotties: shutil.copy(os.path.join("/home/claude/lottie", n), a)


def mermaid_svg(mmd_src, out_svg):
    """Render Mermaid source in the Cyto theme; returns SVG markup ready to inline in a .mmd div.
    Keep it to 3 levels / <=5 boxes so it reads on a phone. Keep the svg id 'my-svg' (its styles depend on it)."""
    src = out_svg.replace(".svg", ".mmd"); open(src, "w").write(mmd_src)
    subprocess.run(["/home/claude/hf/node_modules/.bin/mmdc", "-i", src, "-o", out_svg, "-c", f"{V2_DIR}/mermaid_theme.json",
                    "-C", f"{V2_DIR}/mermaid_style.css", "-p", f"{V2_DIR}/pup.json", "-b", "transparent"], check=True, capture_output=True)
    svg = open(out_svg).read()
    return re.sub(r'style="max-width:[^"]*"', 'style="width:100%;height:100%"', svg, count=1).replace('width="100%"', '', 1)


def mermaid_js(container, node_times, edge_times):
    """Build-on animation. node_times: {text_fragment: t} (matched on box text, case-insensitive).
    edge_times: list of t, in the order Mermaid writes the edges."""
    return (f'(()=>{{const NT={json.dumps({k.upper(): v for k, v in node_times.items()})}, ET={json.dumps(edge_times)};'
            f'document.querySelectorAll("{container} .node").forEach(n=>{{const x=n.textContent.toUpperCase();const k=Object.keys(NT).find(k=>x.includes(k));if(k===undefined)return;'
            f'tl.fromTo(n,{{opacity:0,scale:0.3,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)",immediateRender:true}},NT[k]);}});'
            f'document.querySelectorAll("{container} .edgePaths path").forEach((e,i)=>{{const L=e.getTotalLength();e.style.strokeDasharray=L;const t=ET[Math.min(i,ET.length-1)];'
            f'tl.fromTo(e,{{strokeDashoffset:L,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:0.3,ease:"power2.out",immediateRender:true}},t);}});}})();')


def lottie_js(container_id, json_file, t0, t1, loops=1, ease="none"):
    """Drive a Lottie frame-by-frame from the GSAP timeline (deterministic renders).
    Needs <script src="assets/lottie_svg.min.js"> in <head> and an empty <div id=container_id>.
    ease="power1.in" makes it speed up (e.g. heart rate climbing)."""
    data = open(json_file).read(); v = container_id.replace("-", "_")
    return (f'const L_{v}=lottie.loadAnimation({{container:document.getElementById("{container_id}"),renderer:"svg",loop:false,autoplay:false,animationData:{data}}});'
            f'const P_{v}={{f:0}};tl.fromTo(P_{v},{{f:0}},{{f:L_{v}.totalFrames*{loops}-0.01,duration:{t1 - t0:.3f},ease:"{ease}",'
            f'onUpdate:()=>L_{v}.goToAndStop(P_{v}.f % L_{v}.totalFrames,true)}},{t0:.3f});')


def safe_sheet(snap_dir, out_jpg):
    """Frame check: composite the Shorts UI mock onto every snapshot so overlaps are obvious."""
    from PIL import Image
    import glob
    ui = Image.open(f"{V2_DIR}/shorts_ui.png")
    fs = sorted(glob.glob(os.path.join(snap_dir, "frame*.png")))
    ims = [Image.alpha_composite(Image.open(f).convert("RGBA").resize((1080, 1920)), ui).convert("RGB").resize((360, 640)) for f in fs]
    W = Image.new("RGB", (360 * len(ims), 640))
    for i, im in enumerate(ims): W.paste(im, (i * 360, 0))
    W.save(out_jpg, quality=85)
    return out_jpg
