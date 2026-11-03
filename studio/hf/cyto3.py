"""Cyto rig v3 — vector (SVG) puppet, same 1200x1200 canvas, body centre (600,640), same arm pivots and cup PNGs
as the v1/v2 PNG rig, so place(), outfits and the cup rules keep working.

New vs the PNG rig: ink outlines, eyelids that actually move (blink/squint/wide), eyebrows, pupils that look around,
8 mouth shapes picked from the sounds in each word, a wobbling toque pom-pom, and organelles (nucleus, nucleolus,
mitochondria, ER, golgi, ribosomes, vesicles) on their own layers that drift constantly and get busier while he talks.
Motion style: snappy pose-to-pose (fast in, hold, settle) — cutout-animation feel.
"""
import json, re, math, subprocess, os, random
import numpy as np

RIG = json.load(open("/home/claude/cyto2/rig/rig.json"))
CX, CY, R = 600, 640, 300
SH_L, HAND_L, SH_R, HAND_R = RIG["shoulder_left"], RIG["hand_left"], RIG["shoulder_right"], RIG["hand_right"]
CW, CH = RIG["cup_size"]
CUP_LEFT = HAND_L[0] + .22 * CW - CW / 2
CUP_TOP = HAND_L[1] - .80 * CH
MX, MY = RIG["mouth"]
EYES = [(CX - R * .26, CY), (CX + R * .20, CY)]
INK, TEAL, TEAL_D, TEAL_L = "#0c1622", "#3fc1b0", "#188076", "#8ce2d6"
LID_REST, LID_WIDE, LID_SQUINT, LID_SHUT = -14, -52, 8, 50          # lid bottom edge, relative to eye centre


def _arm(sh, hand, side):
    el = (CX + side * R * 1.12, CY + R * .45)
    d = f"M{sh[0]:.0f} {sh[1]:.0f} Q{el[0]:.0f} {el[1]:.0f} {hand[0]:.0f} {hand[1]:.0f}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="78" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{TEAL_D}" stroke-width="62" stroke-linecap="round"/>')


def _hand(p, id_):
    return f'<circle id="{id_}" cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="50" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'


def _eye(i, ex, ey):
    k = "LR"[i]
    return f"""
  <clipPath id="eclip{k}"><ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="40" ry="49"/></clipPath>
  <g id="eye{k}"><g clip-path="url(#eclip{k})">
    <ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="40" ry="49" fill="#fff"/>
    <g id="pup{k}"><ellipse cx="{ex:.0f}" cy="{ey+6:.0f}" rx="23" ry="27" fill="{INK}"/><circle cx="{ex+8:.0f}" cy="{ey-4:.0f}" r="7" fill="#fff"/></g>
    <g id="lid{k}" transform="translate(0 {LID_REST})"><rect x="{ex-50:.0f}" y="{ey-140:.0f}" width="100" height="140" fill="{TEAL}"/>
      <rect x="{ex-50:.0f}" y="{ey-5:.0f}" width="100" height="10" rx="5" fill="{INK}"/></g>
  </g>
  <ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="40" ry="49" fill="none" stroke="{INK}" stroke-width="7"/></g>
  <path id="ec{k}" opacity="0" d="M{ex-36:.0f} {ey+2:.0f} Q{ex:.0f} {ey+26:.0f} {ex+36:.0f} {ey+2:.0f}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
  <g id="brow{k}"><path d="M{ex-36:.0f} {ey-88:.0f} Q{ex:.0f} {ey-101:.0f} {ex+36:.0f} {ey-88:.0f}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/></g>"""


def _mouths():
    x, y, dk, tg, wt = MX, MY, "#46122a", "#ff7878", "#fbf7ef"
    s = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"'
    m = {
        "rest":  f'<path d="M{x-34} {y-10} Q{x} {y+22} {x+34} {y-10}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>',
        "mbp":   f'<path d="M{x-30} {y+2} Q{x} {y+8} {x+30} {y+2}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>',
        "small": f'<ellipse cx="{x}" cy="{y+4}" rx="25" ry="15" fill="{dk}" {s}/>',
        "a":     f'<path d="M{x-46} {y-6} Q{x} {y+78} {x+46} {y-6} Z" fill="{dk}" {s}/><path d="M{x-24} {y+38} Q{x} {y+22} {x+24} {y+38} Q{x} {y+56} {x-24} {y+38}Z" fill="{tg}"/>',
        "e":     f'<rect x="{x-44}" y="{y-10}" width="88" height="34" rx="16" fill="{dk}" {s}/><rect x="{x-36}" y="{y-7}" width="72" height="11" rx="4" fill="{wt}"/>',
        "o":     f'<ellipse cx="{x}" cy="{y+12}" rx="22" ry="30" fill="{dk}" {s}/>',
        "u":     f'<ellipse cx="{x}" cy="{y+6}" rx="14" ry="17" fill="{dk}" {s}/>',
        "fv":    f'<rect x="{x-30}" y="{y-2}" width="60" height="20" rx="8" fill="{dk}" {s}/><rect x="{x-26}" y="{y-1}" width="52" height="9" rx="3" fill="{wt}"/>',
    }
    return "".join(f'<g id="v_{k}" opacity="{1 if k == "rest" else 0}">{v}</g>' for k, v in m.items())


def _organelles():
    """Organelles, each on its own group so they can move. Clipped to the cytoplasm."""
    rnd = random.Random(6)
    nx, ny = CX + R * .50, CY + R * .50
    mx, my = CX - R * .50, CY + R * .56
    zz = " ".join(f"L{mx - 40 + i * 16:.0f} {my + (11 if i % 2 else -11):.0f}" for i in range(6))
    rib = "".join(f'<circle class="rib" cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice((5, 6, 7))}" fill="#2a8f84"/>'
                  for x, y in [(CX + rnd.uniform(-230, 230), CY + rnd.uniform(-60, 230)) for _ in range(40)]
                  if (x - CX) ** 2 + (y - CY) ** 2 < 255 ** 2 and not (470 < x < 720 and 590 < y < 790))
    ves = "".join(f'<circle class="ves" cx="{x}" cy="{y}" r="{rr}" fill="{TEAL_L}" stroke="#2a8f84" stroke-width="3" opacity=".9"/>'
                  for x, y, rr in ((380, 560, 13), (835, 590, 11), (420, 830, 10), (790, 840, 12), (360, 700, 9)))
    return f"""
  <g id="er"><path d="M{CX-262} {CY-30} q20 -18 40 0 t40 0 M{CX-268} {CY+5} q20 -18 40 0 t40 0 M{CX-262} {CY+40} q20 -18 40 0 t40 0"
     fill="none" stroke="#2a8f84" stroke-width="7" stroke-linecap="round"/></g>
  <g id="golgi"><path d="M{CX+205} {CY-40} q38 -22 76 0 M{CX+200} {CY-14} q42 -24 84 0 M{CX+205} {CY+12} q38 -22 76 0"
     fill="none" stroke="#e0a64b" stroke-width="9" stroke-linecap="round"/></g>
  <g id="ribs">{rib}</g><g id="vess">{ves}</g>
  <g id="mito"><rect x="{mx-57:.0f}" y="{my-26:.0f}" width="114" height="52" rx="26" fill="#ff9f5a" stroke="{INK}" stroke-width="6"/>
     <path d="M{mx-40:.0f} {my:.0f} {zz}" fill="none" stroke="#d96a2b" stroke-width="6" stroke-linejoin="round"/></g>
  <g id="nuc"><circle cx="{nx:.0f}" cy="{ny:.0f}" r="53" fill="#7a5cc7" stroke="{INK}" stroke-width="6"/>
     <path d="M{nx-30:.0f} {ny+12:.0f} q10 -14 20 0 t20 0 M{nx-14:.0f} {ny+30:.0f} q10 -12 20 0" fill="none" stroke="#5a3fa8" stroke-width="5" stroke-linecap="round"/>
     <g id="nucleolus"><circle cx="{nx+12:.0f}" cy="{ny-16:.0f}" r="15" fill="#c4b0ff" stroke="#5a3fa8" stroke-width="4"/></g></g>"""


def rig3_html(outfit=None, cup="cup_red", acc=None, face_extra="", toque_extra=""):
    """face_extra / toque_extra: inline SVG drawn on the face (e.g. a moustache sticker, id it to animate) / on the toque.
    Same element IDs the v2 JS expects (#cytoPos, #cyto, #armL, #armR, #cup, #cupTable) plus new ones."""
    of = f'<image href="assets/{outfit}.png" x="0" y="0" width="1200" height="1200"/>' if outfit else ""
    pr = R * .18
    pom_dots = "".join(f'<circle cx="{CX + math.cos(math.radians(a)) * pr * .55:.0f}" cy="{CY - R * 1.27 + math.sin(math.radians(a)) * pr * .55:.0f}" r="7" fill="#e2e2da"/>' for a in range(0, 360, 45))
    ticks = "".join(f'<path d="M{CX + k * R * .105:.0f} {CY - R * .52:.0f} v24 M{CX + k * R * .105:.0f} {CY - R * .34:.0f} v24" stroke="#0c285c" stroke-width="4"/>' for k in range(-9, 10))
    ribs = "".join(f'<path d="M{CX + k * 60} {CY - R * 1.05 + abs(k) * 12:.0f} V{CY - R * .5:.0f}" stroke="#18489a" stroke-width="5"/>' for k in range(-4, 5))
    return f"""
<div id="cytoPos"><div id="cytoJump"><div id="cyto"><svg viewBox="0 0 1200 1200" width="1200" height="1200" style="position:absolute;left:0;top:0;overflow:visible">
 <defs>
  <radialGradient id="shad"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  <radialGradient id="hil" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{TEAL_L}" stop-opacity=".55"/><stop offset="1" stop-color="{TEAL_L}" stop-opacity="0"/></radialGradient>
  <clipPath id="cyt"><circle cx="{CX}" cy="{CY}" r="{R*.92:.0f}"/></clipPath>
 </defs>
 <ellipse id="shadow" cx="{CX}" cy="{CY + R * 1.09:.0f}" rx="{R * .78:.0f}" ry="34" fill="url(#shad)"/>
 <g id="armR">{_arm(SH_R, HAND_R, 1)}{_hand(HAND_R, "handR")}</g>
 <g id="bodyG">
  <circle cx="{CX}" cy="{CY}" r="{R}" fill="{TEAL_D}" stroke="{INK}" stroke-width="8"/>
  <circle id="cytoplasm" cx="{CX}" cy="{CY}" r="{R*.92:.0f}" fill="{TEAL}"/>
  <ellipse cx="{CX - R * .64:.0f}" cy="{CY + R * .02:.0f}" rx="{R * .24:.0f}" ry="{R * .40:.0f}" fill="url(#hil)"/>
  <g clip-path="url(#cyt)">{_organelles()}</g>
  <ellipse cx="{CX - R * .50:.0f}" cy="{CY + R * .20:.0f}" rx="31" ry="19" fill="#ff8078" opacity=".55"/>
  <ellipse cx="{CX + R * .48:.0f}" cy="{CY + R * .20:.0f}" rx="31" ry="19" fill="#ff8078" opacity=".55"/>
  {of}
  <g id="face">{"".join(_eye(i, ex, ey) for i, (ex, ey) in enumerate(EYES))}<g id="mouths">{_mouths()}</g>{face_extra}</g>
 </g>
 <g id="toque">
  <ellipse cx="{CX}" cy="{CY - R * .77:.0f}" rx="{R * .97:.0f}" ry="{R * .47:.0f}" fill="#1e56ac" stroke="{INK}" stroke-width="8"/>
  {ribs}
  <rect x="{CX - R * 1.03:.0f}" y="{CY - R * .54:.0f}" width="{R * 2.06:.0f}" height="{R * .30:.0f}" rx="36" fill="#143a7c" stroke="{INK}" stroke-width="8"/>
  <rect x="{CX - R * 1.01:.0f}" y="{CY - R * .43:.0f}" width="{R * 2.02:.0f}" height="{R * .08:.0f}" fill="#f6f6f0"/>{ticks}
  {toque_extra}
  <g id="pom"><circle cx="{CX}" cy="{CY - R * 1.27:.0f}" r="{pr:.0f}" fill="#f6f6f0" stroke="{INK}" stroke-width="7"/>{pom_dots}</g>
 </g>
 {f'<image id="acc" href="assets/{acc}.png" x="0" y="0" width="1200" height="1200"/>' if acc else ""}
 <image id="cupTable" href="assets/{cup}.png" x="140" y="{975 - CH}" width="{CW}" height="{CH}" opacity="0"/>
 <g id="armL">{_arm(SH_L, HAND_L, -1)}<image id="cup" href="assets/{cup}.png" x="{CUP_LEFT:.1f}" y="{CUP_TOP:.1f}" width="{CW}" height="{CH}"/>{_hand(HAND_L, "handL")}</g>
</svg></div></div></div>"""


def rig3_css():
    return """
#cytoPos { position:absolute; left:0; top:0; width:1200px; height:1200px; transform-origin:0 0; }
#cytoJump { position:absolute; left:0; top:0; width:1200px; height:1200px; }
#cyto { position:absolute; left:0; top:0; width:1200px; height:1200px; transform-origin:600px 960px; }
"""


# ---------------------------------------------------------------- lip sync
VIS = [("mbp", "mbp"), ("fv", "fv"), ("oo", "u"), ("ou", "o"), ("ow", "o"), ("ee", "e"), ("ea", "e"),
       ("th", "e"), ("sh", "e"), ("ch", "e")]
SINGLE = {**{c: "mbp" for c in "mbp"}, **{c: "fv" for c in "fv"}, **{c: "o" for c in "o"}, **{c: "u" for c in "uwq"},
          "a": "a", "i": "e", "e": "e", "y": "e", "s": "e", "z": "e", "c": "e", "x": "e", "j": "e", "g": "small", "k": "small",
          "t": "small", "d": "small", "n": "small", "l": "small", "r": "o", "h": "a"}
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}


def _word_visemes(w):
    w = "".join(NUM.get(c, c) for c in w.lower())
    w = re.sub(r"[^a-z]", "", w)
    out, i = [], 0
    while i < len(w):
        two = w[i:i + 2]
        hit = next((v for k, v in VIS if two == k), None)
        if hit: out.append(hit); i += 2; continue
        out.append(SINGLE.get(w[i], "small")); i += 1
    # vowels carry the shape; collapse runs
    col = [v for j, v in enumerate(out) if j == 0 or v != out[j - 1]]
    return col or ["small"]


def viseme_track(voice_wav, words, fps=30, t_off=0.0, t_end=None):
    """Mouth shapes from the letters of each word, gated by loudness (silence -> rest/mbp). Snappy: min hold 2 frames."""
    SR = 16000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", voice_wav, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    hop = SR // fps
    rms = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(len(x) // hop)]); rms /= np.percentile(rms, 98)
    track, prev, hold = [], None, 0
    for f, e in enumerate(rms):
        t = f / fps
        if t < t_off or (t_end and t > t_end): continue
        w = next((w for w in words if w["t0"] - .02 <= t <= w["t1"] + .02), None)
        if e < 0.07 or not w:
            s = "rest" if not w else "mbp"
        else:
            vs = _word_visemes(w["w"]); k = min(len(vs) - 1, int((t - w["t0"]) / max(.01, w["t1"] - w["t0"]) * len(vs)))
            s = vs[k]
            if s == "a" and e < 0.35: s = "small"
            if s == "small" and e > 0.7: s = "a"
        if s != prev and hold <= 0:
            track.append([round(t - t_off, 3), s]); prev = s; hold = 2
        hold -= 1
    return track


# ---------------------------------------------------------------- animation
def rig3_js(mouth, T, blinks=(), sips=(), raises=(), points=(), waves=(), tilts=(), shrugs=(), expr=(), looks=(), mute=()):
    """expr: (t, dur, kind) kind in shock|skeptic|hype|squint|sad.  looks: (t, dx, dy) pupils glance (px)."""
    E = [f"const MOUTH={json.dumps(mouth)};",
         'const VS=["#v_rest","#v_mbp","#v_small","#v_a","#v_e","#v_o","#v_u","#v_fv"];',
         'MOUTH.forEach(([t,s])=>{VS.forEach(m=>tl.set(m,{opacity:0},t)); tl.set("#v_"+s,{opacity:1},t);});',
         f'gsap.set("#armL",{{svgOrigin:"{SH_L[0]} {SH_L[1]}"}}); gsap.set("#armR",{{svgOrigin:"{SH_R[0]} {SH_R[1]}"}});',
         f'gsap.set("#cup",{{svgOrigin:"{HAND_L[0]} {HAND_L[1]}"}}); gsap.set("#pom",{{svgOrigin:"{CX} {CY - R * 1.12:.0f}"}});',
         f'gsap.set(["#browL","#browR"],{{transformOrigin:"50% 50%"}});']
    for a, _ in mute:
        E.append(f'VS.forEach(m=>tl.set(m,{{opacity:0}},{a})); tl.set("#v_mbp",{{opacity:1}},{a});')
    # breathing idle (slower, softer than the old constant bounce) + talk-driven bob on open mouths
    E.append(f'tl.fromTo("#cyto",{{y:0,scaleY:1,scaleX:1}},{{y:-7,scaleY:1.015,scaleX:0.992,duration:0.9,ease:"sine.inOut",repeat:{int(T / 0.9)},yoyo:true,immediateRender:false}},0.3);')
    opens = [t for t, s in mouth if s in ("a", "o", "e")]
    for t in opens[::2]:
        E.append(f'tl.fromTo("#bodyG",{{y:-4}},{{y:0,duration:0.18,ease:"power2.out"}},{t});')
    # ---- organelles: always drifting, busier while talking
    loops = [("#nuc", "x:8,y:-6", 1.7), ("#nucleolus", "x:5,y:4", 0.9), ("#mito", "rotation:9,x:-6", 1.3), ("#er", "y:6,x:4", 2.1),
             ("#golgi", "y:-5,rotation:-4", 1.9), ("#ribs", "x:-5,y:3", 1.1)]
    for sel, to, d in loops:
        E.append(f'gsap.set("{sel}",{{transformOrigin:"50% 50%"}}); tl.to("{sel}",{{{to},duration:{d},ease:"sine.inOut",repeat:{int(T / d)},yoyo:true}},0);')
    E.append(f'document.querySelectorAll("#vess .ves").forEach((v,i)=>{{ tl.fromTo(v,{{y:0,opacity:.9}},{{y:-60-i*8,opacity:0,duration:2.4+i*.3,ease:"none",repeat:{int(T / 2.4)}}},i*.45); }});')
    E.append(f'document.querySelectorAll("#ribs .rib").forEach((v,i)=>{{ tl.to(v,{{y:(i%2?4:-4),x:(i%3-1)*3,duration:.35+(i%5)*.07,ease:"sine.inOut",repeat:{int(T / .35)},yoyo:true}},(i%7)*.05); }});')
    for t in opens[::3]:   # nucleus throbs on the beats he hits
        E.append(f'tl.fromTo("#nuc",{{scale:1.09}},{{scale:1,duration:0.28,ease:"power2.out"}},{t});')
        E.append(f'tl.fromTo("#mito",{{scaleX:1.12,scaleY:0.9}},{{scaleX:1,scaleY:1,duration:0.3,ease:"elastic.out(1,0.4)"}},{t+0.05:.3f});')
    # ---- eyes
    for t, d in blinks:
        E.append(f'tl.set(["#eyeL","#eyeR"],{{opacity:0}},{t});tl.set(["#ecL","#ecR"],{{opacity:1}},{t});tl.set(["#eyeL","#eyeR"],{{opacity:1}},{t + d});tl.set(["#ecL","#ecR"],{{opacity:0}},{t + d});')
    for t, dx, dy in looks:   # Nov 2: clamp glances (old +-12..18px pushed pupils out of the eye = "off" look) and always return to centre
        dx, dy = max(-7, min(7, dx * .5)), max(-6, min(4, dy * .35))
        E.append(f'tl.to(["#pupL","#pupR"],{{x:{dx:.1f},y:{dy:.1f},duration:0.08,ease:"power3.out"}},{t});'
                 f'tl.to(["#pupL","#pupR"],{{x:0,y:0,duration:0.15,ease:"power2.inOut"}},{t + 1.1:.2f});')
    pom = lambda t, a: E.append(f'tl.fromTo("#pom",{{rotation:{a}}},{{rotation:0,duration:0.9,ease:"elastic.out(1.2,0.25)",immediateRender:false}},{t:.3f});')
    for t, d, kind in expr:
        if kind == "shock":
            E.append(f'tl.to(["#lidL","#lidR"],{{y:{LID_WIDE},duration:0.06}},{t});tl.to(["#browL","#browR"],{{y:-18,duration:0.06}},{t});'
                     f'tl.to(["#pupL","#pupR"],{{scale:0.75,duration:0.06,transformOrigin:"50% 50%"}},{t});'
                     f'tl.fromTo("#cyto",{{scaleY:0.86,scaleX:1.1}},{{scaleY:1,scaleX:1,duration:0.45,ease:"elastic.out(1.1,0.35)",immediateRender:false}},{t});')
            pom(t, -22)
        elif kind == "hype":
            E.append(f'tl.to(["#browL","#browR"],{{y:-12,duration:0.06}},{t});tl.to(["#lidL","#lidR"],{{y:{LID_REST - 12},duration:0.06}},{t});'
                     f'tl.fromTo("#cytoJump",{{y:0}},{{y:-46,duration:0.12,ease:"power3.out",yoyo:true,repeat:1,immediateRender:false}},{t});')
            pom(t + 0.1, 18)
        elif kind == "skeptic":
            E.append(f'tl.to("#browL",{{y:-14,rotation:-10,duration:0.07}},{t});tl.to("#browR",{{y:6,rotation:8,duration:0.07}},{t});'
                     f'tl.to("#lidR",{{y:{LID_SQUINT},duration:0.07}},{t});tl.to(["#pupL","#pupR"],{{x:-6,duration:0.07}},{t});')
        elif kind == "squint":
            E.append(f'tl.to(["#lidL","#lidR"],{{y:{LID_SQUINT},duration:0.07}},{t});tl.to(["#browL","#browR"],{{y:6,duration:0.07}},{t});')
        elif kind == "sad":
            E.append(f'tl.to("#browL",{{rotation:14,y:-4,duration:0.1}},{t});tl.to("#browR",{{rotation:-14,y:-4,duration:0.1}},{t});')
        # settle back to neutral (pose-to-pose: snap in, hold, settle)
        E.append(f'tl.to(["#lidL","#lidR"],{{y:{LID_REST},duration:0.12}},{t + d});tl.to(["#browL","#browR"],{{y:0,rotation:0,duration:0.12}},{t + d});'
                 f'tl.to(["#pupL","#pupR"],{{x:0,y:0,scale:1,duration:0.12}},{t + d});')
    # ---- gestures: snap in fast, hold, settle — and the pom-pom follows through
    for t, d in points:
        E.append(f'tl.to("#armR",{{rotation:-124,duration:0.1,ease:"power4.out"}},{t});tl.to("#armR",{{rotation:-116,duration:0.15,ease:"power1.out"}},{t + 0.1:.3f});tl.to("#armR",{{rotation:0,duration:0.18,ease:"power3.inOut"}},{t + d});')
        pom(t, 12)
    for t in waves:
        E.append(f'tl.to("#armR",{{rotation:-120,duration:0.12,ease:"power4.out"}},{t});')
        for i, a in enumerate((-98, -130, -100, -128)):
            E.append(f'tl.to("#armR",{{rotation:{a},duration:0.11,ease:"sine.inOut"}},{t + 0.12 + i * 0.11:.3f});')
        E.append(f'tl.to("#armR",{{rotation:0,duration:0.2,ease:"power3.inOut"}},{t + 0.6:.3f});'); pom(t, 15)
    for t, d in shrugs:
        E.append(f'tl.to("#armR",{{rotation:-62,duration:0.1,ease:"power4.out"}},{t});tl.to("#armR",{{rotation:0,duration:0.2}},{t + d});'
                 f'tl.to(["#browL","#browR"],{{y:-10,duration:0.08}},{t});tl.to(["#browL","#browR"],{{y:0,duration:0.12}},{t + d});')
    for t, d, ang in tilts:
        E.append(f'tl.to("#cyto",{{rotation:{ang},duration:0.1,ease:"power3.out"}},{t});tl.to("#cyto",{{rotation:0,duration:0.22,ease:"power2.inOut"}},{t + d});')
        pom(t, -ang * 2.2)
    for t, d in raises:
        E.append(f'tl.to("#armL",{{rotation:-30,duration:0.11,ease:"power4.out"}},{t});tl.to("#cup",{{rotation:30,duration:0.11,ease:"power4.out"}},{t});'
                 f'tl.to("#armL",{{rotation:0,duration:0.2,ease:"power3.inOut"}},{t + d});tl.to("#cup",{{rotation:0,duration:0.2,ease:"power3.inOut"}},{t + d});')
        pom(t, 14)
    for t, d in sips:   # eyes close contentedly, cheeks puff, cup tips
        E.append(f'tl.to("#armL",{{rotation:-42,duration:0.2,ease:"power3.out"}},{t});tl.to("#cup",{{rotation:94,duration:0.2,ease:"power3.out"}},{t});'
                 f'tl.to("#cup",{{rotation:102,duration:{(d - 0.45) / 2:.3f},ease:"sine.inOut",yoyo:true,repeat:1}},{t + 0.2:.3f});'
                 f'tl.set(["#eyeL","#eyeR"],{{opacity:0}},{t + 0.18:.3f});tl.set(["#ecL","#ecR"],{{opacity:1}},{t + 0.18:.3f});tl.set(["#eyeL","#eyeR"],{{opacity:1}},{t + d - 0.2:.3f});tl.set(["#ecL","#ecR"],{{opacity:0}},{t + d - 0.2:.3f});'
                 f'tl.to("#armL",{{rotation:0,duration:0.22,ease:"power3.inOut"}},{t + d - 0.22:.3f});tl.to("#cup",{{rotation:0,duration:0.22,ease:"power3.inOut"}},{t + d - 0.22:.3f});')
    return "\n".join(E)


# ---------------------------------------------------------------- sip sound
SIP_WAV = "/home/claude/hf/v3/sip.wav"


def make_sip(path=SIP_WAV, sr=44100):
    """Synth slurp: band-passed noise that gurgles (15–20 Hz flutter) and rises, then a soft 'gulp' + tiny 'ahh' breath."""
    rng = np.random.default_rng(3); n = int(sr * 0.78); t = np.arange(n) / sr
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    # sweep a resonant band 700 -> 2400 Hz across the slurp (cheap time-varying filter via short FFT blocks)
    blk = 1024
    for i in range(0, n, blk):
        seg = noise[i:i + blk]; f = np.fft.rfftfreq(len(seg), 1 / sr); prog = min(1, i / (sr * 0.5))
        fc = 700 + 1700 * prog; bw = 450 + 300 * prog
        out[i:i + blk] = np.fft.irfft(np.fft.rfft(seg) * np.exp(-((f - fc) / bw) ** 2), len(seg))
    flutter = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * (15 + 6 * t) * t)) * np.abs(np.sin(2 * np.pi * 7 * t))
    env = np.clip(t / 0.04, 0, 1) * np.clip((0.55 - t) / 0.12, 0, 1)
    slurp = out * flutter * env
    gulp_t = t - 0.56; gulp = np.where(gulp_t > 0, np.sin(2 * np.pi * (170 - 90 * np.clip(gulp_t / .1, 0, 1)) * gulp_t) * np.exp(-gulp_t / .045), 0)
    y = slurp / (np.abs(slurp).max() + 1e-9) * 0.8 + gulp * 0.55
    y = (y / np.abs(y).max() * 0.85 * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.tobytes())
    return path


def mix_sips(base_wav, sip_times, out_wav, gain_db=5, duck=0.45):
    """Lay the sip sound on the episode mix at every sip (starts as the cup reaches the mouth)."""
    if not os.path.exists(SIP_WAV): make_sip()
    if not sip_times:
        subprocess.run(["cp", base_wav, out_wav], check=True); return out_wav
    ins = ["-i", base_wav] + sum((["-i", SIP_WAV] for _ in sip_times), [])
    fl = "".join(f"[{i + 1}:a]aresample=48000,volume={gain_db}dB,adelay={int((t + 0.18) * 1000)}|{int((t + 0.18) * 1000)}[s{i}];" for i, t in enumerate(sip_times))
    dk = ",".join(f"volume={duck}:enable='between(t,{t + 0.15:.2f},{t + 0.95:.2f})'" for t in sip_times)   # dip the music under each sip
    fl += "[0:a]aresample=48000," + dk + "[b];[b]" + "".join(f"[s{i}]" for i in range(len(sip_times))) + f"amix=inputs={len(sip_times) + 1}:normalize=0:duration=first,alimiter=limit=0.89[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fl, "-map", "[o]", "-c:a", "pcm_s16le", out_wav], check=True)
    return out_wav
