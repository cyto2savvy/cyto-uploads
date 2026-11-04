"""LF02 v3 character rigs: limb-based (2-segment arms, mitten hands with 4 shape sets, rotatable legs), procedural eyes
(pupil wrapper #{idp}pg{L,R} + blink lid #{idp}bk{L,R}) and a face-turn wrapper #{idp}fT.  Element ids keep the v2 API
(#{idp}, #{idp}Body, #{idp}m_<shape>, #{idp}brow/lid/pup{L,R}) so chars.act_js (lip sync, expressions, pops) still drives them.

NEUTRO fix: mouth on the LOWER FACE centred under the eyes (y 380) and the uniform collar moved down (top y >= 446), so the
largest mouth shape ends >= 12 px above the collar; trench collar moved with it; props live in the hands, below the chest.
MITO redesign: round body, short 2-segment arms (arm = 40 % of body height) with mitten hands (relaxed / grip / fist / point),
legs + sneakers on hip pivots, headband, half-lid eyes, chest-out posture; the ball is a separate world-space prop."""
import math, random, re, sys
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/hf/lf02")
import cyto3 as R
import motion as MO

INK = "#0c1622"


# ------------------------------------------------------------------ face
def face(idp, eyes, skin, rx, ry, brow_len, mouth, ms=1.0, glasses=False, brow_w=12, lid_rest=-.35):
    out = []
    for i, (ex, ey) in enumerate(eyes):
        k = "LR"[i]
        if not glasses:
            out.append(f"""<clipPath id="{idp}ec{k}"><ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}"/></clipPath>
<g clip-path="url(#{idp}ec{k})"><ellipse id="{idp}eye{k}" cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="#fff"/>
 <g id="{idp}pg{k}"><g id="{idp}pup{k}"><ellipse cx="{ex}" cy="{ey + ry * .12:.1f}" rx="{rx * .52:.1f}" ry="{ry * .55:.1f}" fill="{INK}"/><circle cx="{ex + rx * .2:.1f}" cy="{ey - ry * .08:.1f}" r="{rx * .16:.1f}" fill="#fff"/></g></g>
 <g id="{idp}lid{k}" transform="translate(0 {lid_rest * ry:.1f})"><rect x="{ex - rx - 8}" y="{ey - ry * 3}" width="{2 * rx + 16}" height="{ry * 3}" fill="{skin}"/>
  <rect x="{ex - rx - 8}" y="{ey - 4}" width="{2 * rx + 16}" height="8" rx="4" fill="{INK}"/></g>
 <g id="{idp}bk{k}" transform="translate(0 {-ry * 1.4:.1f})"><rect x="{ex - rx - 8}" y="{ey - ry * 3}" width="{2 * rx + 16}" height="{ry * 3}" fill="{skin}"/>
  <rect x="{ex - rx - 8}" y="{ey - 4}" width="{2 * rx + 16}" height="8" rx="4" fill="{INK}"/></g></g>
<ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="6"/>""")
        else:
            out.append(f'<g id="{idp}pg{k}"><g id="{idp}pup{k}"></g></g><g id="{idp}lid{k}"></g><g id="{idp}bk{k}"></g>')
        out.append(f'<g id="{idp}brow{k}"><path d="M{ex - brow_len / 2:.0f} {ey - ry - 22:.0f} Q{ex:.0f} {ey - ry - 34:.0f} {ex + brow_len / 2:.0f} {ey - ry - 22:.0f}" fill="none" stroke="{INK}" stroke-width="{brow_w}" stroke-linecap="round"/></g>')
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
    out.append(f'<g id="{idp}mouth">' + "".join(f'<g id="{idp}m_{k}" opacity="{1 if k == "rest" else 0}">{v}</g>' for k, v in M.items()) + '</g>')
    return f'<g id="{idp}fT"><g id="{idp}Face">{"".join(out)}</g></g>'


# ------------------------------------------------------------------ limbs
def seg(x0, y0, x1, y1, col, w):
    d = f"M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 14}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


def mitten(hx, hy, col, side, r=30, cuff=None):
    """4 hand shapes pointing DOWN (+y) from the wrist (hx,hy). side=+1: thumb toward +x."""
    sw = 6
    c = (f'<rect x="{hx - r * .62:.1f}" y="{hy - r * .38:.1f}" width="{r * 1.24:.1f}" height="{r * .5:.1f}" rx="{r * .2:.1f}" fill="{cuff}" stroke="{INK}" stroke-width="5"/>' if cuff else "")
    palm_y = hy + r * .62
    relaxed = (f'<ellipse cx="{hx + side * r * .78:.1f}" cy="{hy + r * .5:.1f}" rx="{r * .3:.1f}" ry="{r * .5:.1f}" transform="rotate({-side * 32} {hx + side * r * .78:.1f} {hy + r * .5:.1f})" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
               f'<path d="M{hx - r * .82:.1f} {hy + r * .1:.1f} Q{hx - r * .95:.1f} {hy + r * 1.55:.1f} {hx:.1f} {hy + r * 1.6:.1f} Q{hx + r * .95:.1f} {hy + r * 1.55:.1f} {hx + r * .82:.1f} {hy + r * .1:.1f}Z" fill="{col}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    grip = (f'<ellipse cx="{hx:.1f}" cy="{palm_y:.1f}" rx="{r * .92:.1f}" ry="{r * .86:.1f}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
            + "".join(f'<path d="M{hx - r * .55 + i * r * .37:.1f} {palm_y + r * .25:.1f} q{r * .18:.1f} {r * .4:.1f} {r * .36:.1f} 0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>' for i in range(3))
            + f'<ellipse cx="{hx + side * r * .7:.1f}" cy="{palm_y - r * .15:.1f}" rx="{r * .28:.1f}" ry="{r * .45:.1f}" transform="rotate({side * 40} {hx + side * r * .7:.1f} {palm_y - r * .15:.1f})" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>')
    fist = (f'<rect x="{hx - r * .85:.1f}" y="{hy - r * .05:.1f}" width="{r * 1.7:.1f}" height="{r * 1.4:.1f}" rx="{r * .55:.1f}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>'
            + "".join(f'<path d="M{hx - r * .5 + i * r * .5:.1f} {hy + r * 1.05:.1f} v{r * .26:.1f}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>' for i in range(3))
            + f'<path d="M{hx - side * r * .6:.1f} {hy + r * .55:.1f} H{hx + side * r * .55:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    point = (fist + f'<rect x="{hx - r * .2:.1f}" y="{hy + r * 1.1:.1f}" width="{r * .42:.1f}" height="{r * 1.05:.1f}" rx="{r * .21:.1f}" fill="{col}" stroke="{INK}" stroke-width="{sw}"/>')
    return c, dict(relaxed=relaxed, grip=grip, fist=fist, point=point)


def arm_svg(p, S, L1, L2, col, w, side, r=30, hand_extra="", cuff=None, hand_col=None):
    """nested: #{p}UA (shoulder) > #{p}FA (elbow) > #{p}HD (wrist). Hand shapes #{p}h_<shape>."""
    sx, sy = S; ex, ey = sx, sy + L1; hx, hy = sx, sy + L1 + L2
    cuffs, shp = mitten(hx, hy + 4, hand_col or col, side, r, cuff)
    hands = "".join(f'<g id="{p}h_{k}" opacity="{1 if k == "relaxed" else 0}">{v}</g>' for k, v in shp.items())
    return (f'<g id="{p}UA">{seg(sx, sy, ex, ey, col, w)}<g id="{p}FA">{seg(ex, ey, hx, hy, col, w * .92)}'
            f'<circle cx="{ex}" cy="{ey}" r="{w * .46:.1f}" fill="{col}"/>'
            f'<g id="{p}HD">{hand_extra}{cuffs}{hands}</g></g></g>')


def leg_svg(p, hip, L, col, shoe="#fbfbf6", trim="#c8102e", side=1, w=40, sock=True):
    hx, hy = hip; fy = hy + L
    sk = (f'<rect x="{hx - w * .52:.1f}" y="{fy - 34:.1f}" width="{w * 1.04:.1f}" height="22" fill="#fff" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M{hx - w * .52:.1f} {fy - 26:.1f} h{w * 1.04:.1f}" stroke="{trim}" stroke-width="5"/>') if sock else ""
    shoe_p = (f'<path d="M{hx - 34 * side:.1f} {fy + 30:.1f} L{hx - 30 * side:.1f} {fy - 14:.1f} Q{hx:.1f} {fy - 24:.1f} {hx + 22 * side:.1f} {fy - 8:.1f} L{hx + 52 * side:.1f} {fy + 10:.1f} L{hx + 54 * side:.1f} {fy + 30:.1f}Z" fill="{shoe}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
              f'<path d="M{hx - 34 * side:.1f} {fy + 22:.1f} L{hx + 54 * side:.1f} {fy + 22:.1f}" stroke="{trim}" stroke-width="8"/>'
              f'<path d="M{hx - 14 * side:.1f} {fy - 4:.1f} l{22 * side:.1f} 6" stroke="{trim}" stroke-width="6" stroke-linecap="round"/>')
    return (f'<g id="{p}"><path d="M{hx:.1f} {hy:.1f} V{fy - 10:.1f}" stroke="{INK}" stroke-width="{w + 12}" stroke-linecap="round"/>'
            f'<path d="M{hx:.1f} {hy:.1f} V{fy - 10:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>{sk}{shoe_p}</g>')


# ------------------------------------------------------------------ NEUTRO
N_SKIN, N_SKIN_L, N_NUC, N_NUC_L, N_GRAN = "#f2c6da", "#fbe1ec", "#6f45a3", "#9d77cf", "#d49ac0"
NAVY, NAVY_D, GOLD = "#1f2b4d", "#141c33", "#f2c14e"
N_CX, N_CY, N_RX, N_RY = 300, 380, 205, 232
N_MOUTH = (300, 380); N_MS = .92; N_COLLAR = 36          # shirt/trench moved down 36 px (collar top ~447 at centre)
N_SH = {"L": (118, 456), "R": (482, 456)}; N_L1, N_L2 = 80, 76
N_REST = {"L": (98, 600), "R": (502, 600)}
NPOSE = {      # hand targets (char canvas) + shapes + hand abs angle (None = along the forearm)
    "idle":    dict(L=((98, 600), None, "relaxed"), R=((502, 600), None, "relaxed")),
    "cross":   dict(L=((404, 548), -95, "fist"), R=((198, 560), 95, "fist")),
    "notepad": dict(L=((236, 606), -12, "grip"), R=((372, 600), -30, "grip")),
    "radio":   dict(L=((98, 600), None, "relaxed"), R=((456, 438), 160, "fist")),
    "point":   dict(L=((98, 600), None, "relaxed"), R=((616, 360), None, "point")),
    "ticket":  dict(L=((98, 600), None, "relaxed"), R=((610, 470), -110, "grip")),
    "walk":    dict(L=((98, 600), None, "relaxed"), R=((502, 600), None, "relaxed")),
}


def _nblob(scale=1.0):
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        r = 1 + 0.03 * math.sin(11 * a) + 0.015 * math.sin(23 * a + 1)
        pts.append((N_CX + N_RX * r * math.cos(a), N_CY + N_RY * r * math.sin(a)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


NBLOB = _nblob()


def neutro_html(idp="nt", trench=False):
    rnd = random.Random(13)
    gran = "".join(f'<circle cx="{N_CX + rnd.uniform(-170, 170):.0f}" cy="{N_CY + rnd.uniform(-10, 80):.0f}" r="{rnd.uniform(5, 9):.0f}" fill="{N_GRAN}"/>' for _ in range(14))
    nuc = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{N_NUC}" stroke="{INK}" stroke-width="6"/><circle cx="{x - r * .3:.0f}" cy="{y - r * .3:.0f}" r="{r * .3:.0f}" fill="{N_NUC_L}" opacity=".8"/>' for x, y, r in [(150, 230, 44), (450, 230, 44)])
    shirt = (f'<g clip-path="url(#{idp}clip)"><g transform="translate(0 {N_COLLAR})">'
             f'<path id="{idp}collar" d="M30 418 Q300 404 570 418 L570 760 L30 760Z" fill="{NAVY}" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M300 446 V700" stroke="{NAVY_D}" stroke-width="7"/>'
             + "".join(f'<circle cx="300" cy="{y}" r="7" fill="#c9cfd8" stroke="{INK}" stroke-width="3"/>' for y in (480, 530, 580))
             + f'<path d="M256 414 L300 446 L344 414 L330 466 L300 446 L270 466Z" fill="{NAVY_D}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<rect x="96" y="500" width="78" height="56" rx="8" fill="{NAVY_D}" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="424" y="500" width="78" height="56" rx="8" fill="{NAVY_D}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M96 428 L190 414 L196 436 L104 452Z" fill="{NAVY_D}" stroke="{INK}" stroke-width="5"/><path d="M504 428 L410 414 L404 436 L496 452Z" fill="{NAVY_D}" stroke="{INK}" stroke-width="5"/></g></g>'
             f'<g transform="translate(206,{486 + N_COLLAR})"><path d="M0 -26 L22 -14 L18 12 Q10 26 0 32 Q-10 26 -18 12 L-22 -14Z" fill="{GOLD}" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="2" r="9" fill="#d29a24"/></g>')
    radio = (f'<g id="{idp}radio" transform="translate(0 {N_COLLAR})"><path d="M452 436 C470 470 430 488 452 520" fill="none" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="424" y="392" width="54" height="74" rx="10" fill="#22252c" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="438" y="356" width="10" height="40" rx="4" fill="#22252c" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M434 412 h34 M434 424 h34 M434 436 h34" stroke="#5a6070" stroke-width="5"/><circle id="{idp}led" cx="462" cy="452" r="6" fill="#ff4d4d"/></g>')
    chk = "".join(f'<rect x="{168 + i * 22}" y="{196 + (i % 2) * 13}" width="22" height="13" fill="#111"/>' for i in range(12))
    cap = (f'<g id="{idp}Cap"><path d="M178 196 Q160 120 300 104 Q440 120 422 196Z" fill="{NAVY}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<rect x="166" y="194" width="268" height="28" fill="#fff" stroke="{INK}" stroke-width="6"/>{chk}<rect x="166" y="194" width="268" height="28" fill="none" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M170 222 Q300 262 430 222 Q300 242 170 222Z" fill="#0d0f14" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M300 132 l16 10 -4 20 -12 10 -12 -10 -4 -20Z" fill="{GOLD}" stroke="{INK}" stroke-width="4"/></g>')
    legs = "".join(leg_svg(f"{idp}leg{k}", (x, 596), 64, NAVY_D, shoe="#0d0f14", trim="#0d0f14", side=(-1 if k == "L" else 1), w=50, sock=False) for k, x in (("L", 232), ("R", 368)))
    trench_g = ""
    if trench:
        trench_g = (f'<g id="{idp}trench" clip-path="url(#{idp}clip2)"><g transform="translate(0 {N_COLLAR})"><path id="{idp}collar2" d="M30 420 Q300 402 570 420 L590 730 L10 730Z" fill="#b59a6a" stroke="{INK}" stroke-width="7"/>'
                    f'<path d="M210 414 L300 540 L260 700 M390 414 L300 540 L340 700" fill="none" stroke="{INK}" stroke-width="6"/>'
                    f'<path d="M160 420 L250 408 L232 500Z M440 420 L350 408 L368 500Z" fill="#a08657" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                    f'<rect x="40" y="580" width="520" height="26" fill="#8b7349" stroke="{INK}" stroke-width="5"/></g></g>')
    pad = (f'<g id="{idp}pad" opacity="0"><g transform="translate({N_SH["L"][0] - 50} {N_SH["L"][1] + N_L1 + N_L2 + 18})"><rect x="0" y="0" width="112" height="140" rx="8" fill="#fbf7ef" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="0" y="0" width="112" height="22" rx="6" fill="#9a2a2a" stroke="{INK}" stroke-width="5"/>'
           + "".join(f'<path d="M14 {44 + i * 20} H98" stroke="#9fb4c8" stroke-width="4"/>' for i in range(5)) + '</g></g>')
    pen = f'<g id="{idp}pen" opacity="0"><path d="M{N_SH["R"][0]} {N_SH["R"][1] + N_L1 + N_L2 + 20} l-8 58" stroke="#2b5fb3" stroke-width="12" stroke-linecap="round"/></g>'
    tk = (f'<g id="{idp}tkt" opacity="0"><g transform="translate({N_SH["R"][0] - 40} {N_SH["R"][1] + N_L1 + N_L2 + 30})"><rect x="0" y="0" width="80" height="100" rx="6" fill="#fff6c8" stroke="{INK}" stroke-width="6"/>'
          f'<path d="M12 24 H68 M12 44 H68 M12 64 H50" stroke="#c0392b" stroke-width="6"/></g></g>')
    armL = arm_svg(f"{idp}aL", N_SH["L"], N_L1, N_L2, N_SKIN, 50, +1, 32, hand_extra=pad, cuff=NAVY)
    armR = arm_svg(f"{idp}aR", N_SH["R"], N_L1, N_L2, N_SKIN, 50, -1, 32, hand_extra=pen + tk, cuff=NAVY)
    fc = face(idp, [(250, 316), (352, 316)], N_SKIN, 30, 34, 76, N_MOUTH, N_MS, brow_w=16)
    return f"""<svg viewBox="0 0 640 720" width="640" height="720" style="position:absolute;left:0;top:0;overflow:visible"><defs>
<clipPath id="{idp}clip"><path d="{NBLOB}"/></clipPath><clipPath id="{idp}clip2"><path d="{NBLOB}" transform="translate(300 380) scale(1.04) translate(-300 -380)"/><rect x="0" y="560" width="640" height="200"/></clipPath>
<radialGradient id="{idp}sh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<g id="{idp}"><g id="{idp}Mv"><ellipse cx="300" cy="692" rx="190" ry="24" fill="url(#{idp}sh)"/>{legs}
<g id="{idp}Body">
 {nuc}
 <path d="{NBLOB}" fill="{N_SKIN}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
 <g clip-path="url(#{idp}clip)"><ellipse cx="{N_CX}" cy="{N_CY + 10}" rx="{N_RX - 22}" ry="{N_RY - 24}" fill="{N_SKIN_L}" opacity=".55"/>{gran}</g>
 {shirt}{trench_g}{radio}
 <ellipse cx="204" cy="364" rx="24" ry="13" fill="#ff8078" opacity=".45"/><ellipse cx="398" cy="364" rx="24" ry="13" fill="#ff8078" opacity=".45"/>
 {fc}{cap}{armL}{armR}
</g></g></g></svg>"""


# ------------------------------------------------------------------ MITO (redesign)
M_SKIN, M_SKIN_D, M_CRIS, JERSEY, JERSEY_D = "#ff9f5a", "#e07a35", "#c95a22", "#c8102e", "#8e0b20"
M_CX, M_CY, M_RX, M_RY = 300, 350, 182, 192             # round body: height 384
M_SH = {"L": (136, 392), "R": (464, 392)}; M_L1, M_L2 = 80, 74      # arm = 154 = 40 % of body height
M_HIP = {"L": (248, 548), "R": (352, 548)}; M_LEG = 112
M_FEET_Y = 548 + 112 + 30
M_REST = {"L": (118, 540), "R": (482, 540)}
MPOSE = {
    "idle":  dict(L=((118, 540), None, "relaxed"), R=((482, 540), None, "relaxed")),
    "hype":  dict(L=((92, 262), 172, "fist"), R=((508, 262), -172, "fist")),           # fist-pump, both up
    "ball":  dict(L=((118, 540), None, "relaxed"), R=((508, 536), None, "grip")),
    "dunk":  dict(L=((92, 300), None, "fist"), R=((440, 246), 170, "grip")),
    "slump": dict(L=((176, 560), None, "relaxed"), R=((424, 560), None, "relaxed")),
    "point": dict(L=((118, 540), None, "relaxed"), R=((594, 318), None, "point")),
    "shrug": dict(L=((40, 352), 120, "relaxed"), R=((560, 352), -120, "relaxed")),
}


def mito_html(idp="mt", gassed=False):
    sk = M_SKIN
    body = f'<ellipse cx="{M_CX}" cy="{M_CY}" rx="{M_RX}" ry="{M_RY}"/>'
    cris = "".join(f'<path d="M{170 + i * 6} {255 + i * 30} q16 -16 32 0 t32 0 t32 0 t32 0 t32 0 t32 0 t32 0" fill="none" stroke="{M_CRIS}" stroke-width="6" stroke-linecap="round" opacity=".55"/>' for i in range(2))
    jersey = (f'<g clip-path="url(#{idp}clip)">'
              f'<path d="M60 404 L214 392 L300 462 L386 392 L540 404 L560 600 L40 600Z" fill="{JERSEY}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M214 392 L300 462 L386 392" fill="none" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
              f'<path d="M60 404 Q112 470 92 540" fill="none" stroke="#fff" stroke-width="10"/><path d="M540 404 Q488 470 508 540" fill="none" stroke="#fff" stroke-width="10"/></g>'
              f'<text x="300" y="530" text-anchor="middle" font-family="InterBlack" font-size="78" fill="#fff" stroke="#111" stroke-width="5" paint-order="stroke">6</text>')
    shorts = (f'<path d="M168 520 L432 520 L446 600 L316 600 L300 574 L284 600 L154 600Z" fill="{JERSEY}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              f'<path d="M160 572 L170 522 M440 572 L430 522" stroke="#fff" stroke-width="9"/>')
    legs = "".join(leg_svg(f"{idp}leg{k}", M_HIP[k], M_LEG, sk, side=(-1 if k == "L" else 1), w=40) for k in "LR")
    band = (f'<g id="{idp}band" clip-path="url(#{idp}clip)"><path d="M100 226 Q300 158 500 226" fill="none" stroke="{INK}" stroke-width="44"/>'
            f'<path d="M100 226 Q300 158 500 226" fill="none" stroke="#fff" stroke-width="32"/><path d="M100 226 Q300 158 500 226" fill="none" stroke="{JERSEY}" stroke-width="8"/></g>')
    towel = ""
    if gassed:
        towel = (f'<g id="{idp}towel"><path d="M118 262 Q108 120 300 104 Q492 120 482 262 L462 360 Q444 300 436 244 Q300 192 164 244 Q156 300 138 360Z" fill="#f4f4ee" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
                 f'<path d="M132 310 Q300 248 468 310" fill="none" stroke="{JERSEY}" stroke-width="10" opacity=".8"/></g>'
                 f'<g id="{idp}sweat"><path d="M470 272 q10 18 0 26 q-10 -8 0 -26Z M132 290 q10 18 0 26 q-10 -8 0 -26Z" fill="#8fd3ff" stroke="{INK}" stroke-width="3"/></g>')
    armL = arm_svg(f"{idp}aL", M_SH["L"], M_L1, M_L2, sk, 44, +1, 30, cuff="#fff")
    armR = arm_svg(f"{idp}aR", M_SH["R"], M_L1, M_L2, sk, 44, -1, 30, cuff="#fff")
    fc = face(idp, [(250, 286), (352, 286)], sk, 30, 36, 64, (302, 352), 1.0, brow_w=14, lid_rest=-.05)
    return f"""<svg viewBox="0 0 620 760" width="620" height="760" style="position:absolute;left:0;top:0;overflow:visible"><defs>
<clipPath id="{idp}clip">{body}</clipPath>
<radialGradient id="{idp}sh"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>
<g id="{idp}"><g id="{idp}Mv"><ellipse id="{idp}shadow" cx="300" cy="{M_FEET_Y}" rx="160" ry="20" fill="url(#{idp}sh)"/>{legs}{shorts}
<g id="{idp}Body">
 <ellipse cx="{M_CX}" cy="{M_CY}" rx="{M_RX}" ry="{M_RY}" fill="{sk}" stroke="{INK}" stroke-width="9"/>
 <g clip-path="url(#{idp}clip)"><ellipse cx="{M_CX - 60}" cy="{M_CY - 70}" rx="60" ry="40" fill="#ffc28f" opacity=".45"/>{cris}</g>
 {jersey}
 <ellipse cx="204" cy="334" rx="24" ry="13" fill="#ff5f4f" opacity=".4"/><ellipse cx="400" cy="334" rx="24" ry="13" fill="#ff5f4f" opacity=".4"/>
 {band}{fc}{towel}{armL}{armR}
</g></g></g></svg>"""


def ball_svg(id_, r=40):
    """world-space basketball: #{id}S shadow (separate), #{id} ball (squash via transform), seams rotate inside."""
    return (f'<g id="{id_}"><circle cx="0" cy="0" r="{r}" fill="#f07a1a" stroke="{INK}" stroke-width="6"/>'
            f'<g id="{id_}seam"><path d="M{-r} 0 H{r} M0 {-r} V{r} M{-r * .7:.1f} {-r * .7:.1f} Q0 0 {-r * .7:.1f} {r * .7:.1f} M{r * .7:.1f} {-r * .7:.1f} Q0 0 {r * .7:.1f} {r * .7:.1f}" fill="none" stroke="{INK}" stroke-width="4"/></g>'
            f'<ellipse cx="{-r * .35:.1f}" cy="{-r * .4:.1f}" rx="{r * .28:.1f}" ry="{r * .16:.1f}" fill="#fff" opacity=".35"/></g>')


# ------------------------------------------------------------------ CYTO: 2-segment arms + procedural eyes, same ids
C_L1, C_L2 = 120, 118


def _cy_eye(i, ex, ey):
    k = "LR"[i]; T = R.TEAL
    return f"""
  <clipPath id="eclip{k}"><ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="40" ry="49"/></clipPath>
  <g id="eye{k}"><g clip-path="url(#eclip{k})">
    <ellipse id="cyeye{k}" cx="{ex:.0f}" cy="{ey:.0f}" rx="40" ry="49" fill="#fff"/>
    <g id="cypg{k}"><g id="pup{k}"><ellipse cx="{ex:.0f}" cy="{ey + 6:.0f}" rx="22" ry="26" fill="{INK}"/><circle cx="{ex + 8:.0f}" cy="{ey - 4:.0f}" r="7" fill="#fff"/></g></g>
    <g id="lid{k}" transform="translate(0 {R.LID_REST})"><rect x="{ex - 50:.0f}" y="{ey - 140:.0f}" width="100" height="140" fill="{T}"/>
      <rect x="{ex - 50:.0f}" y="{ey - 5:.0f}" width="100" height="10" rx="5" fill="{INK}"/></g>
    <g id="cybk{k}" transform="translate(0 -70)"><rect x="{ex - 50:.0f}" y="{ey - 140:.0f}" width="100" height="140" fill="{T}"/>
      <rect x="{ex - 50:.0f}" y="{ey - 5:.0f}" width="100" height="10" rx="5" fill="{INK}"/></g>
  </g>
  <ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="40" ry="49" fill="none" stroke="{INK}" stroke-width="7"/></g>
  <path id="ec{k}" opacity="0" d="M{ex - 36:.0f} {ey + 2:.0f} Q{ex:.0f} {ey + 26:.0f} {ex + 36:.0f} {ey + 2:.0f}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
  <g id="brow{k}"><path d="M{ex - 36:.0f} {ey - 88:.0f} Q{ex:.0f} {ey - 101:.0f} {ex + 36:.0f} {ey - 88:.0f}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/></g>"""


def _cy_arm(sh, hand, side):
    p = "cyaR" if side == 1 else "cyaL"
    extra = "<!--CUP-->" if side == -1 else "<!--PHONE-->"
    return arm_svg(p, sh, C_L1, C_L2, R.TEAL_D, 62, -side, 46, hand_extra=extra, hand_col=R.TEAL)


def cyto_rig(outfit, cup, face_extra="", toque_extra="", phone=False):
    R.LID_REST = -4                                      # v3: half-lid default
    o_eye, o_arm, o_hand = R._eye, R._arm, R._hand
    R._eye, R._arm, R._hand = _cy_eye, _cy_arm, (lambda p, id_: "")
    try:
        h = R.rig3_html(outfit, cup, face_extra=face_extra, toque_extra=toque_extra)
    finally:
        R._eye, R._arm, R._hand = o_eye, o_arm, o_hand
    m = re.search(r'<image id="cup"[^>]*/>', h)
    cupimg = m.group(0); h = h.replace(cupimg, "")
    # cup sits in the hand at the same absolute place/size as v2 (never rescaled)
    h = h.replace("<!--CUP-->", cupimg)
    ph = ""
    if phone:
        hx, hy = R.SH_R[0], R.SH_R[1] + C_L1 + C_L2
        ph = (f'<g transform="translate({hx + 4} {hy - 112})"><g id="cyPhone"><rect x="0" y="0" width="92" height="160" rx="16" fill="#1b1f2a" stroke="#0c1622" stroke-width="7"/>'
              f'<rect id="cyScreen" x="9" y="14" width="74" height="126" rx="6" fill="#8ce2d6"/>'
              f'<rect id="cyNotif" x="14" y="24" width="64" height="30" rx="7" fill="#fff"/><circle cx="26" cy="39" r="7" fill="#3fc1b0"/><rect x="38" y="33" width="34" height="5" fill="#9aa"/><rect x="38" y="43" width="24" height="5" fill="#9aa"/></g></g>')
    h = h.replace("<!--PHONE-->", ph)
    h = h.replace('<g id="face">', '<g id="cyfT"><g id="face">', 1)
    h = h.replace(f'{face_extra}</g>\n </g>\n <g id="toque">', f'{face_extra}</g></g>\n </g>\n <g id="toque">', 1)
    assert 'id="cyfT"' in h and h.count("<g") == h.count("</g>"), "cyto rig patch failed"
    return h


CY_SH = {"L": tuple(R.SH_L), "R": tuple(R.SH_R)}
CY_REST = {"L": tuple(R.HAND_L), "R": tuple(R.HAND_R)}
