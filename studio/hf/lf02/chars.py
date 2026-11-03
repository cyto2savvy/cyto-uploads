"""LF02 cast rigs (flat-ink vector puppets in the cyto3.py style) + one shared face/acting system.

Every character = an inline <svg> with an id prefix (idp) so several can share a page:
  #{idp}        whole character (squash & stretch origin = feet)
  #{idp}Body    breathing / nods
  #{idp}browL/R, #{idp}lidL/R, #{idp}pupL/R    face
  #{idp}m_<shape>   mouths: rest smirk grin frown flat small a e o mbp
  #{idp}P_<pose>    pose groups (arms etc.), toggled by poses
Expressions (all chars): smug shocked deadpan hype exhausted determined sideeye  (+ neutral)
Cyto keeps cyto3.py (global ids); cyto_expr_js() adds the same expression names to him.
"""
import math, random, json, sys
sys.path.insert(0, "/home/claude/hf")
import cyto3 as R

INK = "#0c1622"


# =============================================================== shared face
def face_svg(idp, eyes, skin, rx, ry, brow_len, mouth, ms=1.0, glasses=False, brow_w=12, brow_col=INK):
    """eyes: [(x,y),(x,y)]; mouth: (x,y) centre; ms: mouth scale."""
    out = []
    for i, (ex, ey) in enumerate(eyes):
        k = "LR"[i]
        if not glasses:
            out.append(f"""<clipPath id="{idp}ec{k}"><ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}"/></clipPath>
<g clip-path="url(#{idp}ec{k})"><ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="#fff"/>
 <g id="{idp}pup{k}"><ellipse cx="{ex}" cy="{ey + ry * .12:.1f}" rx="{rx * .56:.1f}" ry="{ry * .58:.1f}" fill="{INK}"/><circle cx="{ex + rx * .22:.1f}" cy="{ey - ry * .1:.1f}" r="{rx * .17:.1f}" fill="#fff"/></g>
 <g id="{idp}lid{k}" transform="translate(0 {-ry * .35:.1f})"><rect x="{ex - rx - 8}" y="{ey - ry * 3}" width="{2 * rx + 16}" height="{ry * 3}" fill="{skin}"/>
  <rect x="{ex - rx - 8}" y="{ey - 4}" width="{2 * rx + 16}" height="8" rx="4" fill="{INK}"/></g></g>
<ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="6"/>""")
        else:   # sunglasses: lenses hide the eyes; lids/pupils exist (invisible) so the API stays the same
            out.append(f'<g id="{idp}pup{k}"></g><g id="{idp}lid{k}"></g>')
        bx = ex
        out.append(f'<g id="{idp}brow{k}"><path d="M{bx - brow_len / 2:.0f} {ey - ry - 22:.0f} Q{bx:.0f} {ey - ry - 34:.0f} {bx + brow_len / 2:.0f} {ey - ry - 22:.0f}" fill="none" stroke="{brow_col}" stroke-width="{brow_w}" stroke-linecap="round"/></g>')
    if glasses:
        (x0, y0), (x1, y1) = eyes
        out.append(f'<g id="{idp}shades"><path d="M{x0 - rx - 14} {y0 - ry * .7:.0f} H{x1 + rx + 14} L{x1 + rx + 6} {y1 + ry * .5:.0f} Q{x1} {y1 + ry * 1.0:.0f} {x1 - rx + 2} {y1 + ry * .4:.0f} L{(x0 + x1) / 2:.0f} {y0 - ry * .2:.0f} L{x0 + rx - 2} {y0 + ry * .4:.0f} Q{x0} {y0 + ry * 1.0:.0f} {x0 - rx - 6} {y0 + ry * .5:.0f}Z" fill="#111" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                   f'<path d="M{x0 - rx * .6:.0f} {y0 - ry * .3:.0f} l{rx * .5:.0f} 0" stroke="#7fa0c0" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
                   f'<path d="M{x1 - rx * .3:.0f} {y1 - ry * .3:.0f} l{rx * .4:.0f} 0" stroke="#7fa0c0" stroke-width="7" stroke-linecap="round" opacity=".8"/></g>')
    x, y = mouth; s = ms
    dk, tg, wt = "#4a1426", "#ff7878", "#fbf7ef"
    st = f'stroke="{INK}" stroke-width="{5 * s:.1f}" stroke-linejoin="round"'
    M = {
        "rest":  f'<path d="M{x - 26 * s} {y - 6 * s} Q{x} {y + 16 * s} {x + 26 * s} {y - 6 * s}" fill="none" stroke="{INK}" stroke-width="{8 * s:.1f}" stroke-linecap="round"/>',
        "smirk": f'<path d="M{x - 26 * s} {y + 4 * s} Q{x + 4 * s} {y + 14 * s} {x + 30 * s} {y - 12 * s}" fill="none" stroke="{INK}" stroke-width="{8 * s:.1f}" stroke-linecap="round"/>',
        "grin":  f'<path d="M{x - 40 * s} {y - 8 * s} Q{x} {y + 52 * s} {x + 40 * s} {y - 8 * s} Z" fill="{dk}" {st}/><path d="M{x - 34 * s} {y - 5 * s} Q{x} {y + 8 * s} {x + 34 * s} {y - 5 * s} Z" fill="{wt}"/>',
        "frown": f'<path d="M{x - 26 * s} {y + 10 * s} Q{x} {y - 10 * s} {x + 26 * s} {y + 10 * s}" fill="none" stroke="{INK}" stroke-width="{8 * s:.1f}" stroke-linecap="round"/>',
        "flat":  f'<path d="M{x - 22 * s} {y + 2 * s} H{x + 22 * s}" stroke="{INK}" stroke-width="{8 * s:.1f}" stroke-linecap="round"/>',
        "small": f'<ellipse cx="{x}" cy="{y + 3 * s}" rx="{18 * s}" ry="{11 * s}" fill="{dk}" {st}/>',
        "a":     f'<path d="M{x - 34 * s} {y - 5 * s} Q{x} {y + 58 * s} {x + 34 * s} {y - 5 * s} Z" fill="{dk}" {st}/><path d="M{x - 17 * s} {y + 27 * s} Q{x} {y + 16 * s} {x + 17 * s} {y + 27 * s} Q{x} {y + 40 * s} {x - 17 * s} {y + 27 * s}Z" fill="{tg}"/>',
        "e":     f'<rect x="{x - 32 * s}" y="{y - 8 * s}" width="{64 * s}" height="{25 * s}" rx="{12 * s}" fill="{dk}" {st}/><rect x="{x - 26 * s}" y="{y - 6 * s}" width="{52 * s}" height="{8 * s}" rx="3" fill="{wt}"/>',
        "o":     f'<ellipse cx="{x}" cy="{y + 9 * s}" rx="{17 * s}" ry="{23 * s}" fill="{dk}" {st}/>',
        "mbp":   f'<path d="M{x - 22 * s} {y + 2 * s} Q{x} {y + 7 * s} {x + 22 * s} {y + 2 * s}" fill="none" stroke="{INK}" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>',
    }
    out.append("".join(f'<g id="{idp}m_{k}" opacity="{1 if k == "rest" else 0}">{v}</g>' for k, v in M.items()))
    return f'<g id="{idp}Face">{"".join(out)}</g>'


MOUTHS = ["rest", "smirk", "grin", "frown", "flat", "small", "a", "e", "o", "mbp"]
VMAP = {"fv": "e", "u": "o"}
# expression -> (browL dy, browL rot, browR dy, browR rot, lid frac, pupil scale, pupil dx, idle mouth)
EXPR = {
    "neutral":    (0, 0, 0, 0, -.35, 1, 0, "rest"),
    "smug":       (-14, -8, 4, 6, .15, 1, 0, "smirk"),
    "shocked":    (-22, 0, -22, 0, -1.15, .72, 0, "o"),
    "deadpan":    (2, 0, 2, 0, .22, 1, 0, "flat"),
    "hype":       (-16, -6, -16, 6, -.75, 1, 0, "grin"),
    "exhausted":  (-4, 14, -4, -14, .5, 1, 0, "frown"),
    "determined": (8, 14, 8, -14, .05, 1, 0, "flat"),
    "sideeye":    (6, 6, -12, 4, .2, 1, 1, "smirk"),
    "worried":    (-10, 16, -10, -16, -.6, .9, 0, "frown"),
}


def mouth_track(dialogue_wav, words, expr, t_off, t_end, default="rest"):
    """Visemes while this character talks (cyto3 viseme_track), the expression's mouth when quiet."""
    w2 = [dict(w=x["w"], t0=x["t0"], t1=x["t1"]) for x in words]
    tr = R.viseme_track(dialogue_wav, w2, t_off=t_off, t_end=t_end) if w2 else []
    tr = [[t, VMAP.get(s, s)] for t, s in tr]
    def idle_at(t):
        m = default
        for a, d, k in sorted(expr):
            if a <= t < a + d: m = EXPR[k][7]
        return m
    out = []
    for t, s in tr:
        out.append([t, idle_at(t) if s == "rest" else s])
    for a, d, k in expr:           # expression mouth changes while quiet
        for tt in (a, a + d):
            talking = any(x["t0"] - t_off - .05 <= tt <= x["t1"] - t_off + .05 for x in words)
            if not talking: out.append([round(tt, 3), idle_at(tt + 1e-3)])
    out.sort()
    if not out or out[0][0] > 0: out.insert(0, [0, idle_at(0)])
    return out


def act_js(idp, ry, rx, mouths=(), expr=(), blinks=None, looks=(), nods=(), poses=(), pops=(), T=10.0, bob=True,
           seed=1, shut_at=()):
    """GSAP for one character on the global `tl`.  expr: (t, dur, kind). poses: (t, name) toggles #{idp}P_*.
    pops: (t, strength) squash & stretch + anticipation. blinks=None -> automatic every 2.4-4.6s."""
    J = [f'gsap.set("#{idp}Body",{{transformOrigin:"50% 100%"}});gsap.set(["#{idp}browL","#{idp}browR","#{idp}pupL","#{idp}pupR"],{{transformOrigin:"50% 50%"}});']
    for t, s in mouths:
        J.append("".join(f'tl.set("#{idp}m_{m}",{{opacity:{1 if m == s else 0}}},{t:.3f});' for m in MOUTHS))
    for a, d, k in sorted(expr):
        bl, rl, br, rr, lid, ps, pdx, _ = EXPR[k]
        q = 0.09
        J.append(f'tl.to("#{idp}browL",{{y:{bl},rotation:{rl},duration:{q},ease:"back.out(2)"}},{a:.3f});'
                 f'tl.to("#{idp}browR",{{y:{br},rotation:{rr},duration:{q},ease:"back.out(2)"}},{a:.3f});'
                 f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{lid * ry:.1f},duration:{q}}},{a:.3f});'
                 f'tl.to(["#{idp}pupL","#{idp}pupR"],{{scale:{ps},x:{pdx * rx * .28:.1f},duration:{q}}},{a:.3f});')
        if k in ("shocked", "hype"):
            J.append(f'tl.fromTo("#{idp}",{{scaleX:1.12,scaleY:.86}},{{scaleX:1,scaleY:1,duration:.45,ease:"elastic.out(1.1,0.35)",immediateRender:false}},{a:.3f});')
        bl, rl, br, rr, lid, ps, pdx, _ = EXPR["neutral"]
        e = a + d
        J.append(f'tl.to(["#{idp}browL","#{idp}browR"],{{y:0,rotation:0,duration:.14}},{e:.3f});'
                 f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{lid * ry:.1f},duration:.14}},{e:.3f});tl.to(["#{idp}pupL","#{idp}pupR"],{{scale:1,x:0,duration:.14}},{e:.3f});')
    if blinks is None:
        rnd = random.Random(seed); t = rnd.uniform(.6, 2); blinks = []
        while t < T - .3:
            if not any(a <= t <= a + d and k in ("shocked",) for a, d, k in expr): blinks.append(round(t, 2))
            t += rnd.uniform(2.4, 4.6)
    for t in blinks:
        J.append(f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{ry * 1.1:.1f},duration:.05}},{t:.3f});'
                 f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{-.35 * ry:.1f},duration:.07}},{t + .1:.3f});')
    for t, d in shut_at:
        J.append(f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{ry * 1.1:.1f},duration:.12}},{t:.3f});tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{-.35 * ry:.1f},duration:.12}},{t + d:.3f});')
    for t, dx, dy in looks:     # eye darts, clamped inside the eye, return after ~0.9s
        dx = max(-.3, min(.3, dx)) * rx; dy = max(-.25, min(.2, dy)) * ry
        J.append(f'tl.to(["#{idp}pupL","#{idp}pupR"],{{x:{dx:.1f},y:{dy:.1f},duration:.07,ease:"power3.out"}},{t:.3f});'
                 f'tl.to(["#{idp}pupL","#{idp}pupR"],{{x:0,y:0,duration:.14}},{t + .9:.3f});')
    for t in nods:
        J.append(f'tl.to("#{idp}Body",{{y:9,duration:.11,ease:"power2.out",yoyo:true,repeat:1}},{t:.3f});')
    names = sorted({p for _, p in poses})
    for t, p in poses:
        J.append("".join(f'tl.set("#{idp}P_{n}",{{opacity:{1 if n == p else 0}}},{t:.3f});' for n in names))
        if t > 0.05:
            J.append(f'tl.fromTo("#{idp}",{{scaleX:1.07,scaleY:.93}},{{scaleX:1,scaleY:1,duration:.32,ease:"back.out(3)",immediateRender:false}},{t:.3f});')
    for t, s in pops:      # anticipation (crouch) -> stretch -> settle
        J.append(f'tl.to("#{idp}",{{scaleX:{1 + .08 * s:.3f},scaleY:{1 - .1 * s:.3f},duration:.1,ease:"power2.in"}},{t - .12:.3f});'
                 f'tl.to("#{idp}",{{scaleX:{1 - .07 * s:.3f},scaleY:{1 + .12 * s:.3f},y:{-30 * s:.0f},duration:.12,ease:"power3.out"}},{t - .02:.3f});'
                 f'tl.to("#{idp}",{{scaleX:1,scaleY:1,y:0,duration:.35,ease:"bounce.out"}},{t + .12:.3f});')
    if bob:
        J.append(f'tl.fromTo("#{idp}Body",{{scaleY:1}},{{scaleY:1.022,duration:.95,yoyo:true,repeat:{int(T / .95) + 1},ease:"sine.inOut",immediateRender:false}},0);')
    return "\n".join(J)


def cyto_expr_js(expr):
    """Extra Cyto expressions on the cyto3 ids (the rig's own expr= handles shock/hype/skeptic/squint/sad)."""
    J = []
    for a, d, k in expr:
        bl, rl, br, rr, lid, ps, pdx, _ = EXPR[k]
        lidv = {-.35: R.LID_REST}.get(lid, int(-14 + (lid + .35) * 52))
        J.append(f'tl.to("#browL",{{y:{bl},rotation:{rl},duration:.09}},{a:.3f});tl.to("#browR",{{y:{br},rotation:{rr},duration:.09}},{a:.3f});'
                 f'tl.to(["#lidL","#lidR"],{{y:{max(R.LID_WIDE, min(30, lidv))},duration:.09}},{a:.3f});tl.to(["#pupL","#pupR"],{{x:{pdx * 6:.0f},scale:{ps},duration:.09,transformOrigin:"50% 50%"}},{a:.3f});'
                 f'tl.to(["#lidL","#lidR"],{{y:{R.LID_REST},duration:.14}},{a + d:.3f});tl.to(["#browL","#browR"],{{y:0,rotation:0,duration:.14}},{a + d:.3f});tl.to(["#pupL","#pupR"],{{x:0,scale:1,duration:.14}},{a + d:.3f});')
        if k in ("shocked", "hype"):
            J.append(f'tl.fromTo("#cyto",{{scaleY:.86,scaleX:1.1}},{{scaleY:1,scaleX:1,duration:.45,ease:"elastic.out(1.1,0.35)",immediateRender:false}},{a:.3f});')
    return "\n".join(J)


# =============================================================== NEUTRO (Toronto-police-style officer)
N_SKIN, N_SKIN_L, N_NUC, N_NUC_L, N_GRAN = "#f2c6da", "#fbe1ec", "#6f45a3", "#9d77cf", "#d49ac0"
NAVY, NAVY_D, GOLD = "#1f2b4d", "#141c33", "#f2c14e"
N_CX, N_CY, N_RX, N_RY = 300, 380, 205, 232


def _nblob():
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        r = 1 + 0.03 * math.sin(11 * a) + 0.015 * math.sin(23 * a + 1)
        pts.append((N_CX + N_RX * r * math.cos(a), N_CY + N_RY * r * math.sin(a)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


NBLOB = _nblob()


def _limb(d, col, w=58):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 16}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def _fist(x, y, col, r=40):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="7"/>'


def neutro_html(idp="nt", pose="idle", trench=False):
    rnd = random.Random(13)
    gran = "".join(f'<circle cx="{N_CX + rnd.uniform(-170, 170):.0f}" cy="{N_CY + rnd.uniform(-40, 60):.0f}" r="{rnd.uniform(5, 9):.0f}" fill="{N_GRAN}"/>' for _ in range(14))
    lobes = [(150, 230, 44), (450, 230, 44)]
    nuc = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{N_NUC}" stroke="{INK}" stroke-width="6"/><circle cx="{x - r * .3:.0f}" cy="{y - r * .3:.0f}" r="{r * .3:.0f}" fill="{N_NUC_L}" opacity=".8"/>' for x, y, r in lobes)
    shirt = (f'<g clip-path="url(#{idp}clip)"><path d="M40 430 Q300 392 560 430 L560 720 L40 720Z" fill="{NAVY}" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M300 452 V700" stroke="{NAVY_D}" stroke-width="7"/>'
             + "".join(f'<circle cx="300" cy="{y}" r="7" fill="#c9cfd8" stroke="{INK}" stroke-width="3"/>' for y in (480, 530, 580, 630))
             + f'<path d="M250 418 L300 456 L350 418 L332 476 L300 456 L268 476Z" fill="{NAVY_D}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<rect x="96" y="500" width="78" height="56" rx="8" fill="{NAVY_D}" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="424" y="500" width="78" height="56" rx="8" fill="{NAVY_D}" stroke="{INK}" stroke-width="4"/></g>'
             f'<g transform="translate(212,486)"><path d="M0 -26 L22 -14 L18 12 Q10 26 0 32 Q-10 26 -18 12 L-22 -14Z" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="2" r="9" fill="#d29a24"/></g>'
             f'<path d="M96 428 L190 412 L196 436 L104 452Z" fill="{NAVY_D}" stroke="{INK}" stroke-width="5"/><path d="M504 428 L410 412 L404 436 L496 452Z" fill="{NAVY_D}" stroke="{INK}" stroke-width="5"/>')
    radio = (f'<g id="{idp}radio"><path d="M452 436 C470 470 430 488 452 520" fill="none" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="424" y="392" width="54" height="74" rx="10" fill="#22252c" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="438" y="350" width="10" height="46" rx="4" fill="#22252c" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M434 412 h34 M434 424 h34 M434 436 h34" stroke="#5a6070" stroke-width="5"/><circle id="{idp}led" cx="462" cy="452" r="6" fill="#ff4d4d"/></g>')
    chk = "".join(f'<rect x="{168 + i * 22}" y="{196 + (i % 2) * 13}" width="22" height="13" fill="#111"/>' for i in range(12))
    cap = (f'<g id="{idp}Cap"><path d="M178 196 Q160 120 300 104 Q440 120 422 196Z" fill="{NAVY}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<rect x="166" y="194" width="268" height="28" fill="#fff" stroke="{INK}" stroke-width="6"/>{chk}<rect x="166" y="194" width="268" height="28" fill="none" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M170 222 Q300 268 430 222 Q300 246 170 222Z" fill="#0d0f14" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M300 132 l16 10 -4 20 -12 10 -12 -10 -4 -20Z" fill="{GOLD}" stroke="{INK}" stroke-width="4"/></g>')
    legs = "".join(f'<rect x="{x - 26}" y="600" width="52" height="50" rx="14" fill="{NAVY_D}" stroke="{INK}" stroke-width="6"/>'
                   f'<path d="M{x - 38} 672 Q{x - 38} 640 {x} 640 Q{x + 48} 640 {x + 50} 672Z" fill="#0d0f14" stroke="{INK}" stroke-width="6"/>' for x in (232, 368))
    sk = N_SKIN
    pad = (f'<g transform="translate(330,470) rotate(-8)"><rect x="0" y="0" width="120" height="150" rx="8" fill="#fbf7ef" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="0" y="0" width="120" height="22" rx="6" fill="#9a2a2a" stroke="{INK}" stroke-width="5"/>'
           + "".join(f'<path d="M14 {44 + i * 22} H106" stroke="#9fb4c8" stroke-width="4"/>' for i in range(5)) + '</g>')
    poses = {
        "idle": _limb("M118 440 Q84 510 96 580", sk) + _fist(96, 588, sk) + _limb("M482 440 Q516 510 504 580", sk) + _fist(504, 588, sk),
        "cross": _limb("M118 440 Q170 530 392 496", sk) + _limb("M482 440 Q430 550 206 510", sk) + _fist(196, 510, sk, 38) + _fist(410, 492, sk, 38),
        "notepad": _limb("M118 440 Q150 560 330 560", sk) + pad + _fist(340, 560, sk, 36) + _limb("M482 440 Q540 520 470 540", sk) + _fist(456, 536, sk, 34)
                   + f'<path d="M440 540 L392 500" stroke="#2b5fb3" stroke-width="12" stroke-linecap="round"/>',
        "radio": _limb("M118 440 Q84 510 96 580", sk) + _fist(96, 588, sk) + _limb("M482 440 Q560 500 470 430", sk) + _fist(462, 426, sk, 36),
        "point": _limb("M118 440 Q84 510 96 580", sk) + _fist(96, 588, sk) + _limb("M482 440 Q560 420 590 340", sk) + _fist(592, 330, sk, 36),
        "facepalm": _limb("M118 440 Q84 510 96 580", sk) + _fist(96, 588, sk) + _limb("M482 440 Q470 380 360 340", sk) + f'<ellipse cx="320" cy="330" rx="62" ry="50" fill="{sk}" stroke="{INK}" stroke-width="7"/>'
                    + "".join(f'<path d="M{280 + i * 22} 296 v58" stroke="{INK}" stroke-width="4" opacity=".5"/>' for i in range(4)),
        "ticket": _limb("M118 440 Q84 510 96 580", sk) + _fist(96, 588, sk) + _limb("M482 440 Q580 470 600 420", sk)
                  + f'<g transform="translate(590,380) rotate(12)"><rect x="-10" y="-40" width="84" height="104" rx="6" fill="#fff6c8" stroke="{INK}" stroke-width="6"/><path d="M4 -16 H60 M4 4 H60 M4 24 H44" stroke="#c0392b" stroke-width="6"/></g>' + _fist(600, 420, sk, 36),
    }
    pose_g = "".join(f'<g id="{idp}P_{k}" opacity="{1 if k == pose else 0}">{v}</g>' for k, v in poses.items())
    trench_g = ""
    if trench:
        trench_g = (f'<g id="{idp}trench" clip-path="url(#{idp}clip2)"><path d="M30 420 Q300 380 570 420 L590 730 L10 730Z" fill="#b59a6a" stroke="{INK}" stroke-width="7"/>'
                    f'<path d="M200 410 L300 560 L250 720 M400 410 L300 560 L350 720" fill="none" stroke="{INK}" stroke-width="6"/>'
                    f'<path d="M150 418 L250 400 L230 500Z M450 418 L350 400 L370 500Z" fill="#a08657" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                    f'<rect x="40" y="600" width="520" height="26" fill="#8b7349" stroke="{INK}" stroke-width="5"/></g>')
    face = face_svg(idp, [(250, 330), (352, 330)], N_SKIN, 30, 34, 76, (300, 405), 1.0, brow_w=16)
    return f"""<svg viewBox="0 0 640 720" width="640" height="720" style="position:absolute;left:0;top:0;overflow:visible"><defs>
<clipPath id="{idp}clip"><path d="{NBLOB}"/></clipPath><clipPath id="{idp}clip2"><path d="{NBLOB}" transform="translate(300 380) scale(1.04) translate(-300 -380)"/><rect x="0" y="560" width="640" height="200"/></clipPath>
<radialGradient id="{idp}sh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<g id="{idp}"><ellipse cx="300" cy="672" rx="190" ry="24" fill="url(#{idp}sh)"/>{legs}
<g id="{idp}Body">
 {nuc}
 <path d="{NBLOB}" fill="{N_SKIN}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
 <g clip-path="url(#{idp}clip)"><ellipse cx="{N_CX}" cy="{N_CY + 10}" rx="{N_RX - 22}" ry="{N_RY - 24}" fill="{N_SKIN_L}" opacity=".55"/>{gran}</g>
 {shirt}{trench_g}{radio}
 <ellipse cx="206" cy="384" rx="24" ry="14" fill="#ff8078" opacity=".45"/><ellipse cx="396" cy="384" rx="24" ry="14" fill="#ff8078" opacity=".45"/>
 {face}{cap}{pose_g}
</g></g></svg>"""


# =============================================================== MITO (mitochondrion hooper)
M_SKIN, M_SKIN_D, M_CRIS, JERSEY, JERSEY_D = "#ff9f5a", "#e07a35", "#c95a22", "#c8102e", "#8e0b20"


def _bean(cx=300, cy=330, rx=165, ry=225):
    pts = []
    for k in range(140):
        a = 2 * math.pi * k / 140
        x = cx + rx * math.cos(a); y = cy + ry * math.sin(a)
        x += 34 * math.exp(-((a - math.pi) % (2 * math.pi) - 0) ** 2 / .25) if False else 0
        dent = 30 * math.exp(-(((a - math.pi + math.pi) % (2 * math.pi) - math.pi) ** 2) / .18)   # dent on the left side (a≈π)
        x += dent
        pts.append((x, y))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


MBEAN = _bean()


def mito_html(idp="mt", pose="idle", gassed=False):
    sk = M_SKIN
    cris = "".join(f'<path d="M{226 + i * 0} {380 + i * 34} q12 -14 24 0 t24 0 t24 0 t24 0 t24 0 t24 0" fill="none" stroke="{M_CRIS}" stroke-width="6" stroke-linecap="round"/>' for i in range(3))
    jersey = (f'<g clip-path="url(#{idp}clip)">'
              f'<path d="M80 360 L210 350 L300 470 L390 350 L520 360 L560 720 L40 720Z" fill="{JERSEY}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M210 350 L300 470 L390 350" fill="none" stroke="#fff" stroke-width="14" stroke-linejoin="round"/>'
              f'<path d="M210 350 L300 470 L390 350" fill="none" stroke="#111" stroke-width="5" stroke-linejoin="round" transform="translate(0 10)"/>'
              f'<path d="M80 360 Q120 440 96 520" fill="none" stroke="#fff" stroke-width="12"/><path d="M520 360 Q480 440 504 520" fill="none" stroke="#fff" stroke-width="12"/>'
              f'<rect x="40" y="530" width="520" height="16" fill="#111"/><rect x="40" y="546" width="520" height="8" fill="#fff"/></g>'
              f'<text x="300" y="530" text-anchor="middle" font-family="InterBlack" font-size="92" fill="#fff" stroke="#111" stroke-width="5" paint-order="stroke">6</text>')
    shorts = (f'<path d="M150 548 L450 548 L462 640 L320 640 L300 600 L280 640 L138 640Z" fill="{JERSEY}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M144 600 L154 548 M456 600 L446 548" stroke="#fff" stroke-width="10"/>')
    legs = "".join(f'<rect x="{x - 20}" y="630" width="40" height="52" fill="{sk}" stroke="{INK}" stroke-width="6"/>'
                   f'<path d="M{x - 40} 724 L{x - 36} 676 Q{x} 664 {x + 26} 680 L{x + 52} 700 L{x + 52} 724Z" fill="#fbfbf6" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                   f'<rect x="{x - 40}" y="714" width="92" height="14" rx="6" fill="{JERSEY}" stroke="{INK}" stroke-width="5"/>'
                   f'<path d="M{x - 30} 688 h40" stroke="{JERSEY}" stroke-width="7"/>' for x in (236, 364))
    band = (f'<g id="{idp}band" clip-path="url(#{idp}clip)"><path d="M90 168 Q300 96 510 168" fill="none" stroke="{INK}" stroke-width="44"/>'
            f'<path d="M90 168 Q300 96 510 168" fill="none" stroke="#fff" stroke-width="32"/><path d="M90 168 Q300 96 510 168" fill="none" stroke="{JERSEY}" stroke-width="8"/></g>')
    towel = ""
    if gassed:
        towel = (f'<g id="{idp}towel"><path d="M110 250 Q100 90 300 70 Q500 90 490 250 L470 360 Q450 300 440 230 Q300 170 160 230 Q150 300 130 360Z" fill="#f4f4ee" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
                 f'<path d="M126 300 Q300 230 474 300" fill="none" stroke="{JERSEY}" stroke-width="10" opacity=".8"/></g>'
                 f'<g id="{idp}sweat"><path d="M470 250 q10 18 0 26 q-10 -8 0 -26Z M140 270 q10 18 0 26 q-10 -8 0 -26Z" fill="#8fd3ff" stroke="{INK}" stroke-width="3"/></g>')
    ball = lambda x, y, r=48: (f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="#f07a1a" stroke="{INK}" stroke-width="6"/>'
                               f'<path d="M{x - r} {y} H{x + r} M{x} {y - r} V{y + r} M{x - r * .7} {y - r * .7} Q{x} {y} {x - r * .7} {y + r * .7} M{x + r * .7} {y - r * .7} Q{x} {y} {x + r * .7} {y + r * .7}" fill="none" stroke="{INK}" stroke-width="4"/></g>')
    poses = {
        "idle": _limb("M110 400 Q70 470 92 540", sk, 50) + _fist(92, 548, sk, 36) + _limb("M490 400 Q530 470 508 540", sk, 50) + _fist(508, 548, sk, 36),
        "hype": _limb("M110 400 Q40 320 70 190", sk, 50) + _fist(72, 180, sk, 38) + _limb("M490 400 Q560 320 530 190", sk, 50) + _fist(528, 180, sk, 38),
        "ball": _limb("M110 400 Q70 470 92 540", sk, 50) + _fist(92, 548, sk, 36) + _limb("M490 400 Q560 470 540 560", sk, 50) + ball(560, 640) + _fist(540, 566, sk, 36),
        "dunk": _limb("M110 400 Q120 250 230 110", sk, 50) + _limb("M490 400 Q480 250 370 110", sk, 50) + ball(300, 70, 54) + _fist(236, 104, sk, 36) + _fist(364, 104, sk, 36),
        "slump": _limb("M110 410 Q90 500 140 590", sk, 50) + _fist(146, 598, sk, 34) + _limb("M490 410 Q510 500 460 590", sk, 50) + _fist(454, 598, sk, 34),
        "point": _limb("M110 400 Q70 470 92 540", sk, 50) + _fist(92, 548, sk, 36) + _limb("M490 400 Q570 360 600 300", sk, 50) + _fist(604, 292, sk, 36),
        "shrug": _limb("M110 400 Q30 400 50 320", sk, 50) + _fist(50, 312, sk, 36) + _limb("M490 400 Q570 400 550 320", sk, 50) + _fist(550, 312, sk, 36),
    }
    pose_g = "".join(f'<g id="{idp}P_{k}" opacity="{1 if k == pose else 0}">{v}</g>' for k, v in poses.items())
    face = face_svg(idp, [(250, 262), (354, 262)], sk, 32, 38, 66, (302, 330), 1.1, brow_w=14)
    return f"""<svg viewBox="0 0 620 760" width="620" height="760" style="position:absolute;left:0;top:0;overflow:visible"><defs>
<clipPath id="{idp}clip"><path d="{MBEAN}"/></clipPath>
<radialGradient id="{idp}sh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<g id="{idp}"><ellipse cx="300" cy="728" rx="170" ry="22" fill="url(#{idp}sh)"/>{legs}{shorts}
<g id="{idp}Body">
 <path d="{MBEAN}" fill="{sk}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
 <g clip-path="url(#{idp}clip)"><path d="M200 120 q30 -20 60 0 t60 0 t60 0" fill="none" stroke="{M_SKIN_D}" stroke-width="6" opacity=".6"/>
   <path d="M216 360 L300 470 L384 360Z" fill="{M_SKIN_D}"/>{cris}</g>
 {jersey}
 <ellipse cx="206" cy="304" rx="24" ry="13" fill="#ff5f4f" opacity=".4"/><ellipse cx="398" cy="304" rx="24" ry="13" fill="#ff5f4f" opacity=".4"/>
 {band}{face}{towel}{pose_g}
</g></g></svg>"""


# =============================================================== RHINO (cold virus, silent)
V_GREEN, V_GREEN_D = "#7fd34e", "#4e9a2a"


def rhino_html(idp="rh", pose="sneak"):
    cx, cy, r = 200, 190, 104
    spikes = ""
    for k in range(14):
        a = 2 * math.pi * k / 14 + .1
        x0, y0 = cx + r * .92 * math.cos(a), cy + r * .92 * math.sin(a)
        x1, y1 = cx + (r + 38) * math.cos(a), cy + (r + 38) * math.sin(a)
        if 40 < math.degrees(a) % 360 < 140: continue      # hoodie covers the bottom
        spikes += (f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{V_GREEN_D}" stroke-width="10" stroke-linecap="round"/>'
                   f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="15" fill="#ff6b8b" stroke="{INK}" stroke-width="5"/>')
    hood = (f'<path d="M66 214 Q50 70 200 52 Q350 70 334 214 L320 260 Q300 150 200 140 Q100 150 80 260Z" fill="#2c303b" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    torso = (f'<path d="M80 250 Q200 300 320 250 L340 400 Q200 420 60 400Z" fill="#2c303b" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M150 330 H250 L240 380 H160Z" fill="#26292f" stroke="{INK}" stroke-width="4"/><path d="M180 262 v40 M220 262 v40" stroke="#d6d6d6" stroke-width="4"/>')
    legs = "".join(f'<rect x="{x - 15}" y="398" width="30" height="26" fill="#2a2d35" stroke="{INK}" stroke-width="5"/>'
                   f'<path d="M{x - 28} 440 Q{x - 28} 418 {x} 418 Q{x + 36} 418 {x + 38} 440Z" fill="#f2f2f2" stroke="{INK}" stroke-width="5"/>' for x in (160, 240))
    sk = "#2c303b"
    poses = {
        "sneak": _limb("M84 280 Q30 250 40 190", sk, 34) + _fist(40, 182, V_GREEN, 26) + _limb("M316 280 Q370 250 360 190", sk, 34) + _fist(360, 182, V_GREEN, 26),
        "wave": _limb("M84 280 Q60 340 70 380", sk, 34) + _fist(70, 388, V_GREEN, 26) + _limb("M316 280 Q380 230 370 150", sk, 34) + _fist(370, 140, V_GREEN, 28),
        "idle": _limb("M84 280 Q60 340 70 380", sk, 34) + _fist(70, 388, V_GREEN, 26) + _limb("M316 280 Q340 340 330 380", sk, 34) + _fist(330, 388, V_GREEN, 26),
        "spread": _limb("M84 280 Q20 260 0 200", sk, 34) + _fist(0, 192, V_GREEN, 26) + _limb("M316 280 Q380 260 400 200", sk, 34) + _fist(400, 192, V_GREEN, 26),
        "duck": _limb("M84 280 Q130 230 150 170", sk, 34) + _fist(152, 160, V_GREEN, 26) + _limb("M316 280 Q270 230 250 170", sk, 34) + _fist(248, 160, V_GREEN, 26),
    }
    pose_g = "".join(f'<g id="{idp}P_{k}" opacity="{1 if k == pose else 0}">{v}</g>' for k, v in poses.items())
    face = face_svg(idp, [(160, 182), (240, 182)], V_GREEN, 26, 28, 56, (204, 236), .9, glasses=True, brow_w=13)
    return f"""<svg viewBox="0 0 400 460" width="400" height="460" style="position:absolute;left:0;top:0;overflow:visible"><defs>
<radialGradient id="{idp}sh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<g id="{idp}"><ellipse cx="200" cy="442" rx="120" ry="16" fill="url(#{idp}sh)"/>{legs}
<g id="{idp}Body">{torso}{hood}{spikes}
 <circle cx="{cx}" cy="{cy}" r="{r}" fill="{V_GREEN}" stroke="{INK}" stroke-width="8"/>
 <circle cx="{cx - 40}" cy="{cy - 50}" r="16" fill="#a9ec7c" opacity=".7"/><circle cx="{cx + 52}" cy="{cy + 40}" r="10" fill="{V_GREEN_D}" opacity=".6"/>
 {face}{pose_g}
</g></g></svg>"""


def wrap(inner, id_, x, y, s, z=20, flip=False, extra=""):
    """Outer placement div (CSS) — animate the inner svg groups, or #id_ for travel moves."""
    sx = -s if flip else s
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:10px;height:10px;z-index:{z};{extra}">'
            f'<div style="position:absolute;left:0;top:0;transform:scale({sx},{s});transform-origin:0 0">{inner}</div></div>')
