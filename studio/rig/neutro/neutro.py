"""Neutro — neutrophil security guard (Cyto cast, introduced Ep 13). Flat-ink vector puppet in the cyto3.py style.
Design: pale-pink ruffled granulocyte (NOT round like Cyto), purple 3-lobed nucleus on top (the neutrophil tell),
lilac granules, stern heavy brows, high-vis vest with reflective stripes + shield badge, coiled earpiece, stubby legs + boots.
Poses: idle / cross (arms crossed) / flex.  Canvas 600x720, feet at y~650.  Usage:
    neutro_html("nt")  -> inline <svg> (wrap it in an outer positioned div; animate the inner #nt group)
    neutro_js("nt", poses=[(t,"cross")], blinks=[t], mouths=[(t,"open")], brows=[(t,"up")], nods=[t], looks=[(t,dx,dy)])
"""
import math, random

INK, SKIN, SKIN_L, NUC, NUC_L, GRAN = "#0c1622", "#f2c6da", "#fbe1ec", "#6f45a3", "#9d77cf", "#d49ac0"
VEST, VEST_D, STRIPE = "#d6f03a", "#a9c41c", "#e8ecf2"
CX, CY, RX, RY = 300, 380, 205, 232
EYES = [(250, 336), (352, 336)]


def _blob():
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        r = 1 + 0.03 * math.sin(11 * a) + 0.015 * math.sin(23 * a + 1)
        pts.append((CX + RX * r * math.cos(a), CY + RY * r * math.sin(a)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


BLOB = _blob()


def _arm(d, idp, k):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="74" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{SKIN}" stroke-width="58" stroke-linecap="round" stroke-linejoin="round"/>')


def _fist(x, y, r=40):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M{x - r * .55:.0f} {y - r * .15:.0f} h{r * 1.1:.0f} M{x - r * .55:.0f} {y + r * .2:.0f} h{r * 1.1:.0f}" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity=".5"/>')


def _eye(i, idp, ex, ey):
    k = "LR"[i]
    return f"""<clipPath id="{idp}ec{k}"><ellipse cx="{ex}" cy="{ey}" rx="30" ry="34"/></clipPath>
 <g clip-path="url(#{idp}ec{k})"><ellipse cx="{ex}" cy="{ey}" rx="30" ry="34" fill="#fff"/>
  <g id="{idp}pup{k}"><ellipse cx="{ex}" cy="{ey + 6}" rx="16" ry="19" fill="{INK}"/><circle cx="{ex + 6}" cy="{ey}" r="5" fill="#fff"/></g>
  <g id="{idp}lid{k}" transform="translate(0 -4)"><rect x="{ex - 40}" y="{ey - 110}" width="80" height="110" fill="{SKIN}"/>
   <rect x="{ex - 40}" y="{ey - 4}" width="80" height="8" rx="4" fill="{INK}"/></g></g>
 <ellipse cx="{ex}" cy="{ey}" rx="30" ry="34" fill="none" stroke="{INK}" stroke-width="6"/>"""


def neutro_html(idp="nt", pose="cross", w=600, h=720, style="position:absolute;left:0;top:0;overflow:visible"):
    rnd = random.Random(13)
    gran = "".join(f'<circle cx="{CX + rnd.uniform(-170, 170):.0f}" cy="{CY + rnd.uniform(-60, 200):.0f}" r="{rnd.uniform(5, 9):.0f}" fill="{GRAN}"/>' for _ in range(26))
    lobes = [(226, 238, 36), (300, 218, 41), (374, 238, 36)]
    nuc = (f'<path d="M226 238 Q262 204 300 218 Q338 204 374 238" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>'
           f'<path d="M226 238 Q262 204 300 218 Q338 204 374 238" fill="none" stroke="{NUC}" stroke-width="14" stroke-linecap="round"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{NUC}" stroke="{INK}" stroke-width="6"/><circle cx="{x - r * .3:.0f}" cy="{y - r * .3:.0f}" r="{r * .3:.0f}" fill="{NUC_L}" opacity=".8"/>' for x, y, r in lobes))
    vest = (f'<g clip-path="url(#{idp}clip)"><path d="M60 420 Q300 380 540 420 L560 700 L40 700Z" fill="{VEST}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M262 405 L300 470 L338 405" fill="{SKIN}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M300 470 V640" stroke="{VEST_D}" stroke-width="6"/>'
            + "".join(f'<rect x="40" y="{y}" width="520" height="26" fill="{STRIPE}" stroke="{INK}" stroke-width="5"/>' for y in (500, 556))
            + f'</g><g transform="translate(400,445)"><path d="M0 -24 L22 -16 L20 10 Q14 26 0 32 Q-14 26 -20 10 L-22 -16Z" fill="#4f86ff" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M0 -12 L5 0 L16 1 L7 8 L10 20 L0 13 L-10 20 L-7 8 L-16 1 L-5 0Z" fill="#FFD166"/></g>')
    ear = (f'<path d="M500 330 C540 350 510 372 540 392 C566 410 520 430 540 452 C552 466 520 480 500 470" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
           f'<ellipse cx="500" cy="324" rx="16" ry="20" fill="#2b2f3a" stroke="{INK}" stroke-width="5"/><circle cx="496" cy="318" r="5" fill="#5a6070"/>')
    legs = "".join(f'<rect x="{x - 26}" y="560" width="52" height="80" rx="16" fill="#2b3550" stroke="{INK}" stroke-width="6"/>'
                   f'<path d="M{x - 38} 650 Q{x - 38} 620 {x} 620 Q{x + 48} 620 {x + 50} 650Z" fill="#1a1d24" stroke="{INK}" stroke-width="6"/>' for x in (232, 368))
    idle = f'<g id="{idp}Idle" opacity="{1 if pose == "idle" else 0}">{_arm("M118 430 Q84 500 96 572", idp, "a")}{_fist(96, 580)}{_arm("M482 430 Q516 500 504 572", idp, "b")}{_fist(504, 580)}</g>'
    cross = (f'<g id="{idp}Cross" opacity="{1 if pose == "cross" else 0}">{_arm("M118 432 Q170 520 392 486", idp, "c")}'
             f'{_arm("M482 432 Q430 540 206 500", idp, "d")}{_fist(196, 500, 38)}{_fist(410, 482, 38)}</g>')
    flex = (f'<g id="{idp}Flex" opacity="{1 if pose == "flex" else 0}">{_arm("M118 430 Q84 500 96 572", idp, "e")}{_fist(96, 580)}'
            f'{_arm("M482 430 Q600 452 584 330", idp, "f")}{_fist(578, 300, 44)}'
            f'<path d="M520 420 Q560 380 590 410" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".55"/></g>')
    mouths = (f'<g id="{idp}mSmirk"><path d="M266 404 Q300 418 336 398" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/></g>'
              f'<g id="{idp}mFrown" opacity="0"><path d="M268 414 Q300 396 334 414" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/></g>'
              f'<g id="{idp}mOpen" opacity="0"><path d="M268 398 Q300 396 334 398 Q330 438 300 440 Q270 438 268 398Z" fill="#7a1f2e" stroke="{INK}" stroke-width="7"/>'
              f'<path d="M276 400 H326 V410 H276Z" fill="#fff"/></g>')
    brows = (f'<g id="{idp}browL"><path d="M214 290 L284 306" stroke="{INK}" stroke-width="16" stroke-linecap="round"/></g>'
             f'<g id="{idp}browR"><path d="M318 306 L388 290" stroke="{INK}" stroke-width="16" stroke-linecap="round"/></g>')
    return f"""<svg viewBox="0 0 600 720" width="{w}" height="{h}" style="{style}"><defs><clipPath id="{idp}clip"><path d="{BLOB}"/></clipPath>
 <radialGradient id="{idp}sh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<g id="{idp}">
 <ellipse cx="300" cy="652" rx="190" ry="26" fill="url(#{idp}sh)"/>
 {legs}
 <g id="{idp}Body">
  <path d="{BLOB}" fill="{SKIN}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
  <g clip-path="url(#{idp}clip)"><ellipse cx="{CX}" cy="{CY + 10}" rx="{RX - 22}" ry="{RY - 24}" fill="{SKIN_L}" opacity=".55"/>{gran}</g>
  <g id="{idp}Nuc">{nuc}</g>
  {vest}
  {ear}
  <ellipse cx="206" cy="388" rx="24" ry="14" fill="#ff8078" opacity=".45"/><ellipse cx="396" cy="388" rx="24" ry="14" fill="#ff8078" opacity=".45"/>
  <g id="{idp}Face">{"".join(_eye(i, idp, ex, ey) for i, (ex, ey) in enumerate(EYES))}{brows}{mouths}</g>
  {idle}{cross}{flex}
 </g>
</g></svg>"""


def neutro_js(idp, poses=(), blinks=(), mouths=(), brows=(), nods=(), looks=(), bob=None, t_end=60):
    """GSAP calls on the global `tl`. poses: (t, idle|cross|flex) with a squash pop; mouths: (t, smirk|frown|open);
    brows: (t, up|down|flat); nods: t (chin-down nod); looks: (t, dx, dy) pupils, clamped to +-7 / -6..+5, return after 1s;
    bob: (t0, t1) idle breathing."""
    J = [f'gsap.set("#{idp}",{{svgOrigin:"300 650"}});gsap.set(["#{idp}browL","#{idp}browR"],{{svgOrigin:"300 300"}});']
    names = {"idle": "Idle", "cross": "Cross", "flex": "Flex"}
    for t, p in poses:
        for k, v in names.items():
            J.append(f'tl.set("#{idp}{v}",{{opacity:{1 if k == p else 0}}},{t:.3f});')
        J.append(f'tl.fromTo("#{idp}",{{scaleX:1.06,scaleY:.94}},{{scaleX:1,scaleY:1,duration:0.35,ease:"back.out(3)",immediateRender:false}},{t:.3f});')
    for t, m in mouths:
        for k in ("Smirk", "Frown", "Open"):
            J.append(f'tl.set("#{idp}m{k}",{{opacity:{1 if k.lower() == m else 0}}},{t:.3f});')
    for t, b in brows:
        dy, rl = {"up": (-16, 6), "down": (6, -4), "flat": (0, 0)}[b]
        J.append(f'tl.to("#{idp}browL",{{y:{dy},rotation:{rl},duration:0.15,ease:"back.out(2)"}},{t:.3f});'
                 f'tl.to("#{idp}browR",{{y:{dy},rotation:{-rl},duration:0.15,ease:"back.out(2)"}},{t:.3f});')
    for t in blinks:
        J.append(f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:40,duration:0.06}},{t:.3f});tl.to(["#{idp}lidL","#{idp}lidR"],{{y:-4,duration:0.08}},{t + 0.1:.3f});')
    for t in nods:
        J.append(f'tl.to("#{idp}Body",{{y:10,duration:0.12,ease:"power2.out",yoyo:true,repeat:1}},{t:.3f});')
    for t, dx, dy in looks:
        dx, dy = max(-7, min(7, dx)), max(-6, min(5, dy))
        J.append(f'tl.to(["#{idp}pupL","#{idp}pupR"],{{x:{dx},y:{dy},duration:0.15}},{t:.3f});tl.to(["#{idp}pupL","#{idp}pupR"],{{x:0,y:0,duration:0.25}},{t + 1.0:.3f});')
    if bob:
        a, b = bob; n = max(1, int((b - a) / 0.9))
        J.append(f'tl.fromTo("#{idp}Body",{{scaleY:1}},{{scaleY:1.02,svgOrigin:"300 640",duration:0.9,yoyo:true,repeat:{n},ease:"sine.inOut",immediateRender:false}},{a:.3f});')
    return "\n".join(J)
