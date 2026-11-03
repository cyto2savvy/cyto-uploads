"""Reusable flat-cutout art for Cyto episodes (same ink-outline style + palette as the v3 rig).
Every function returns SVG markup (no <svg> wrapper unless noted) so scenes can place/animate the parts by id.
Toronto set pieces: skyline(), city_hall(), night_bus(); props: phone(), body_clock(); figures: hypnogram().
Add new pieces here, not inside an episode build, so every episode can reuse them."""
import random, math

INK, NAVY, CREAM, GOLD, CORAL, TEAL, TEAL_D, BLUE = "#0c1622", "#0c1622", "#FAF4E8", "#FFD166", "#FF7A59", "#3fc1b0", "#188076", "#4f86ff"


def stars(W, H, n, seed=1, maxy=.55):
    rnd = random.Random(seed)
    return "".join(f'<circle class="star" cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H * maxy):.0f}" r="{rnd.choice((2, 2, 3, 4))}" fill="{CREAM}" opacity="{rnd.uniform(.25, .75):.2f}"/>' for _ in range(n))


def moon(x, y, r=60, bg="#101d31"):
    return (f'<g id="moon"><circle cx="{x}" cy="{y}" r="{r * 1.9:.0f}" fill="{GOLD}" opacity=".10"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="{x + r * .45:.0f}" cy="{y - r * .3:.0f}" r="{r * .82:.0f}" fill="{bg}"/></g>')


def skyline(W, H, base, scale=1.0, seed=4, lit=.35, cn=None, ground=NAVY):
    """Flat Toronto skyline: CN Tower, the dome, condo towers with lit windows (windows have class 'win')."""
    rnd = random.Random(seed); s = scale; out = []
    cn = W * .5 if cn is None else cn
    x = -20
    while x < W:
        w = rnd.uniform(70, 150) * s; h = rnd.uniform(140, 380) * s
        out.append(f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#13263d"/>'); x += w + rnd.uniform(4, 18) * s
    out.append(f'<path d="M{cn + 150 * s:.0f} {base} A{150 * s:.0f} {95 * s:.0f} 0 0 1 {cn + 450 * s:.0f} {base} Z" fill="#1a3150" stroke="{INK}" stroke-width="{5 * s:.0f}"/>')
    for k in range(1, 5):
        out.append(f'<path d="M{cn + 300 * s:.0f} {base - 95 * s:.0f} L{cn + 150 * s + k * 60 * s:.0f} {base}" stroke="#2a4866" stroke-width="{4 * s:.0f}"/>')
    sh = 860 * s; pod_y = base - sh * .62
    out.append(f'<g id="cnTower"><path d="M{cn - 34 * s:.0f} {base} L{cn - 12 * s:.0f} {base - sh * .9:.0f} L{cn + 12 * s:.0f} {base - sh * .9:.0f} L{cn + 34 * s:.0f} {base} Z" fill="#1c3656" stroke="{INK}" stroke-width="{6 * s:.0f}"/>'
               f'<rect x="{cn - 4 * s:.0f}" y="{base - sh:.0f}" width="{8 * s:.0f}" height="{sh * .12:.0f}" fill="#1c3656" stroke="{INK}" stroke-width="{4 * s:.0f}"/>'
               f'<ellipse cx="{cn}" cy="{pod_y:.0f}" rx="{62 * s:.0f}" ry="{30 * s:.0f}" fill="#22406a" stroke="{INK}" stroke-width="{6 * s:.0f}"/>'
               f'<rect class="podLight" x="{cn - 56 * s:.0f}" y="{pod_y - 6 * s:.0f}" width="{112 * s:.0f}" height="{10 * s:.0f}" fill="{GOLD}" opacity=".85"/>'
               f'<ellipse cx="{cn}" cy="{base - sh * .78:.0f}" rx="{20 * s:.0f}" ry="{11 * s:.0f}" fill="#22406a" stroke="{INK}" stroke-width="{4 * s:.0f}"/>'
               f'<circle class="tip" cx="{cn}" cy="{base - sh:.0f}" r="{7 * s:.0f}" fill="{CORAL}"/></g>')
    x = -10
    while x < W:
        w = rnd.uniform(90, 190) * s; h = rnd.uniform(90, 300) * s
        if abs(x + w / 2 - cn) < 70 * s: x += 80 * s; continue
        out.append(f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h + 4:.0f}" fill="#1a3150" stroke="{INK}" stroke-width="{5 * s:.0f}"/>')
        for wy in range(int(base - h + 18 * s), int(base - 12 * s), int(26 * s)):
            for wx in range(int(x + 14 * s), int(x + w - 18 * s), int(26 * s)):
                if rnd.random() < lit:
                    out.append(f'<rect class="win" x="{wx}" y="{wy}" width="{12 * s:.0f}" height="{14 * s:.0f}" fill="{GOLD}" opacity="{rnd.uniform(.55, .95):.2f}"/>')
        x += w + rnd.uniform(0, 10) * s
    out.append(f'<rect x="-50" y="{base}" width="{W + 100}" height="{H - base + 50}" fill="{ground}"/>')
    return "".join(out)


def city_hall(cx, base, s=1.0, seed=3):
    """Toronto City Hall, flat: two curved towers (west shorter) hugging the saucer council chamber, plus the
    podium and Nathan Phillips Square arches. Windows are class 'chw' (for alarm strobes)."""
    rnd = random.Random(seed); out = []
    def tower(x0, w, h, flip):
        # curved tower: flat back, concave inner face
        xb, xi = (x0, x0 + w) if not flip else (x0 + w, x0)
        top = base - h
        d = (f"M{xb:.0f} {base} L{xb:.0f} {top:.0f} Q{(xb + xi) / 2:.0f} {top - 22 * s:.0f} {xi:.0f} {top + 10 * s:.0f} "
             f"Q{xi + (-1 if not flip else 1) * 0 * s:.0f} {base - h / 2:.0f} {xi:.0f} {base} Z")
        g = [f'<path d="{d}" fill="#d9dde3" stroke="{INK}" stroke-width="{7 * s:.0f}" stroke-linejoin="round"/>']
        for r_ in range(int(top + 30 * s), int(base - 20 * s), int(24 * s)):
            for k in range(5):
                wx = min(xb, xi) + 16 * s + k * (w - 32 * s) / 5
                g.append(f'<rect class="chw" x="{wx:.0f}" y="{r_}" width="{(w - 32 * s) / 5 - 8 * s:.0f}" height="{12 * s:.0f}" fill="{GOLD if rnd.random() < .45 else "#5a6b80"}" opacity="{rnd.uniform(.6, .95):.2f}"/>')
        # vertical ribs
        for k in range(1, 4):
            rx = min(xb, xi) + k * w / 4
            g.append(f'<path d="M{rx:.0f} {top + 12 * s:.0f} V{base}" stroke="#aeb6c0" stroke-width="{4 * s:.0f}"/>')
        return "".join(g)
    out.append(f'<g id="chEast">{tower(cx + 40 * s, 170 * s, 560 * s, True)}</g>')
    out.append(f'<g id="chWest">{tower(cx - 210 * s, 170 * s, 440 * s, False)}</g>')
    # saucer
    out.append(f'<g id="chSaucer"><path d="M{cx - 120 * s:.0f} {base - 70 * s:.0f} Q{cx:.0f} {base - 200 * s:.0f} {cx + 120 * s:.0f} {base - 70 * s:.0f} Z" fill="#eef0f3" stroke="{INK}" stroke-width="{7 * s:.0f}"/>'
               f'<rect x="{cx - 46 * s:.0f}" y="{base - 70 * s:.0f}" width="{92 * s:.0f}" height="{40 * s:.0f}" fill="#aeb6c0" stroke="{INK}" stroke-width="{6 * s:.0f}"/></g>')
    # podium
    out.append(f'<rect x="{cx - 330 * s:.0f}" y="{base - 30 * s:.0f}" width="{660 * s:.0f}" height="{56 * s:.0f}" fill="#b9c1cb" stroke="{INK}" stroke-width="{7 * s:.0f}"/>')
    # arches over the square
    for k in range(3):
        ax = cx - 300 * s + k * 300 * s
        out.append(f'<path d="M{ax - 70 * s:.0f} {base + 120 * s:.0f} Q{ax:.0f} {base + 20 * s:.0f} {ax + 70 * s:.0f} {base + 120 * s:.0f}" fill="none" stroke="#e8ecf0" stroke-width="{12 * s:.0f}"/>')
    # beacon (alarm light) on east tower roof
    out.append(f'<g id="beacon"><rect x="{cx + 105 * s:.0f}" y="{base - 600 * s:.0f}" width="{40 * s:.0f}" height="{28 * s:.0f}" rx="{8 * s:.0f}" fill="#e2394b" stroke="{INK}" stroke-width="{5 * s:.0f}"/>'
               f'<circle id="beaconGlow" cx="{cx + 125 * s:.0f}" cy="{base - 590 * s:.0f}" r="{90 * s:.0f}" fill="#ff3b3b" opacity="0"/></g>')
    return "".join(out)


def phone(x, y, w=440, h=800, time="3:00", day="THURSDAY", note=True, idp="ph"):
    """Lock-screen phone, top-left at (x,y). ids: {idp}Glow, {idp}Time, {idp}Note."""
    sc = w / 440
    return f'''<g id="{idp}">
 <rect id="{idp}Glow" x="{x}" y="{y}" width="{w}" height="{h}" rx="{70 * sc:.0f}" fill="#7fb0ff" opacity=".7" filter="url(#blur38)"/>
 <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{70 * sc:.0f}" fill="#1a1f2b" stroke="{INK}" stroke-width="12"/>
 <rect id="{idp}Scr" x="{x + 24 * sc:.0f}" y="{y + 24 * sc:.0f}" width="{w - 48 * sc:.0f}" height="{h - 48 * sc:.0f}" rx="{50 * sc:.0f}" fill="url(#scrGrad)"/>
 <rect x="{x + w / 2 - 50 * sc:.0f}" y="{y + 46 * sc:.0f}" width="{100 * sc:.0f}" height="{26 * sc:.0f}" rx="{13 * sc:.0f}" fill="#05070c"/>
 <text x="{x + w / 2:.0f}" y="{y + 140 * sc:.0f}" text-anchor="middle" font-family="InterXB" font-size="{30 * sc:.0f}" fill="#cfe0ff" letter-spacing="2">{day}</text>
 <text id="{idp}Time" x="{x + w / 2:.0f}" y="{y + 300 * sc:.0f}" text-anchor="middle" font-family="InterBlack" font-size="{196 * sc:.0f}" fill="#fff" letter-spacing="-6">{time}</text>
 <text x="{x + w / 2:.0f}" y="{y + 368 * sc:.0f}" text-anchor="middle" font-family="InterBlack" font-size="{58 * sc:.0f}" fill="{GOLD}">AM</text>
 {f"""<g id="{idp}Note"><rect x="{x + 50 * sc:.0f}" y="{y + 520 * sc:.0f}" width="{340 * sc:.0f}" height="{150 * sc:.0f}" rx="{30 * sc:.0f}" fill="#fff" opacity=".93"/>
 <circle cx="{x + 102 * sc:.0f}" cy="{y + 570 * sc:.0f}" r="{28 * sc:.0f}" fill="{TEAL}" stroke="{INK}" stroke-width="4"/>
 <text x="{x + 144 * sc:.0f}" y="{y + 566 * sc:.0f}" font-family="InterBlack" font-size="{26 * sc:.0f}" fill="{INK}">YOUR BODY</text>
 <text x="{x + 144 * sc:.0f}" y="{y + 602 * sc:.0f}" font-family="InterXB" font-size="{24 * sc:.0f}" fill="#334">wake up. rn.</text>
 <text x="{x + 70 * sc:.0f}" y="{y + 648 * sc:.0f}" font-family="InterXB" font-size="{20 * sc:.0f}" fill="#667">every. single. night.</text></g>""" if note else ""}
</g>'''


PHONE_DEFS = ('<filter id="blur38" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="38"/></filter>'
              '<linearGradient id="scrGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d3f8f"/><stop offset="1" stop-color="#0b1838"/></linearGradient>')


def body_clock(cx, cy, r=190, idp="bc"):
    """Cell-style clock (teal membrane rim, organelle dots at the hours). Hands: {idp}H (hour) / {idp}M (minute),
    drawn pointing at 12 — rotate them about (cx,cy)."""
    ticks = "".join(f'<circle cx="{cx + math.sin(math.radians(a)) * r * .8:.0f}" cy="{cy - math.cos(math.radians(a)) * r * .8:.0f}" r="{11 if a % 90 == 0 else 7}" fill="{"#7a5cc7" if a % 90 == 0 else TEAL_D}"/>'
                    for a in range(0, 360, 30))
    return f'''<g id="{idp}">
 <circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEAL_D}" stroke="{INK}" stroke-width="10"/>
 <circle cx="{cx}" cy="{cy}" r="{r * .9:.0f}" fill="#d9f5f0"/>{ticks}
 <g id="{idp}H"><path d="M{cx} {cy} L{cx} {cy - r * .45:.0f}" stroke="{INK}" stroke-width="18" stroke-linecap="round"/></g>
 <g id="{idp}M"><path d="M{cx} {cy} L{cx} {cy - r * .68:.0f}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/></g>
 <circle cx="{cx}" cy="{cy}" r="16" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>
</g>'''


def night_bus(x, y, s=1.0, sign="NIGHT BUS"):
    """Generic city bus side view (no real logos), top-left (x,y), ~700x300 at s=1. Wheels: class 'wheel'."""
    W_, H_ = 700 * s, 260 * s
    win = "".join(f'<rect x="{x + (60 + k * 118) * s:.0f}" y="{y + 50 * s:.0f}" width="{96 * s:.0f}" height="{86 * s:.0f}" rx="{10 * s:.0f}" fill="#ffe7a3" stroke="{INK}" stroke-width="{5 * s:.0f}"/>' for k in range(5))
    def wheel(wx): return (f'<g class="wheel"><circle cx="{wx:.0f}" cy="{y + H_:.0f}" r="{46 * s:.0f}" fill="#20242e" stroke="{INK}" stroke-width="{6 * s:.0f}"/>'
                           f'<circle cx="{wx:.0f}" cy="{y + H_:.0f}" r="{18 * s:.0f}" fill="#9aa3ab"/><path d="M{wx - 30 * s:.0f} {y + H_:.0f} H{wx + 30 * s:.0f}" stroke="#9aa3ab" stroke-width="{6 * s:.0f}"/></g>')
    return f'''<g id="bus">
 <ellipse cx="{x + W_ / 2:.0f}" cy="{y + H_ + 46 * s:.0f}" rx="{W_ * .55:.0f}" ry="{18 * s:.0f}" fill="#000" opacity=".35"/>
 <rect x="{x}" y="{y}" width="{W_:.0f}" height="{H_:.0f}" rx="{36 * s:.0f}" fill="#f4f4ef" stroke="{INK}" stroke-width="{8 * s:.0f}"/>
 <rect x="{x}" y="{y + 160 * s:.0f}" width="{W_:.0f}" height="{30 * s:.0f}" fill="#e2394b"/>
 <rect x="{x + 30 * s:.0f}" y="{y + 12 * s:.0f}" width="{260 * s:.0f}" height="{30 * s:.0f}" rx="{6 * s:.0f}" fill="#111"/>
 <text x="{x + 160 * s:.0f}" y="{y + 36 * s:.0f}" text-anchor="middle" font-family="InterBlack" font-size="{22 * s:.0f}" fill="#ff9a2e" letter-spacing="2">{sign}</text>
 {win}
 <rect x="{x + W_ - 70 * s:.0f}" y="{y + 50 * s:.0f}" width="{48 * s:.0f}" height="{150 * s:.0f}" rx="{8 * s:.0f}" fill="#9fc3e8" stroke="{INK}" stroke-width="{5 * s:.0f}"/>
 <rect x="{x + W_ - 10 * s:.0f}" y="{y + 190 * s:.0f}" width="{14 * s:.0f}" height="{26 * s:.0f}" rx="4" fill="{GOLD}"/>
 <rect x="{x + 20 * s:.0f}" y="{y + 210 * s:.0f}" width="{60 * s:.0f}" height="{14 * s:.0f}" rx="4" fill="{BLUE}"/>
 {wheel(x + 140 * s)}{wheel(x + W_ - 150 * s)}
</g>'''


# ---- sleep figure ---------------------------------------------------------------------------------------
# stages, y-levels top->bottom: AWAKE, REM, LIGHT, DEEP.  Times in hours after 11 PM (0..8).
HYPNO = [(0, 0), (.15, 2), (.45, 2.6), (.6, 3), (1.05, 3), (1.2, 2), (1.35, 1), (1.5, 1),       # cycle 1: long deep
         (1.65, 2), (1.95, 2.6), (2.1, 3), (2.45, 3), (2.6, 2), (2.85, 1), (3.1, 1),             # cycle 2
         (3.25, 2), (3.6, 2.5), (3.85, 2), (4.0, 0), (4.08, 0), (4.2, 1), (4.6, 1),              # cycle 3 -> brief wake ~3 AM
         (4.75, 2), (5.1, 2.2), (5.35, 1), (5.9, 1), (6.05, 2), (6.4, 2), (6.55, 1), (7.3, 1), (7.6, 0), (8, 0)]
CORT = [(0, .18), (1, .12), (2, .12), (3, .2), (4, .34), (5, .52), (6, .74), (7, .95), (8, 1.0)]


def hypnogram(x0, y0, w, h, idp="hy"):
    """Sleep-stage graph (11 PM - 7 AM) + cortisol curve. Returns (svg_markup, helpers dict with x_of(hours), y_of(level)).
    ids: {idp}Line (stage path), {idp}Deep (deep shading), {idp}Cort (cortisol path), {idp}Axis."""
    x_of = lambda t: x0 + w * t / 8
    y_of = lambda lv: y0 + h * lv / 3
    pts = " ".join(f"{x_of(t):.1f},{y_of(l):.1f}" for t, l in HYPNO)
    # step-ish line: use straight segments (already shaped above)
    deep = "".join(f'<rect x="{x_of(a):.0f}" y="{y_of(2.75):.0f}" width="{x_of(b) - x_of(a):.0f}" height="{y_of(3.2) - y_of(2.75):.0f}" rx="8" fill="#4f86ff" opacity=".35"/>'
                   for a, b in ((.55, 1.1), (2.05, 2.5)))
    labels = "".join(f'<text x="{x0 - 18}" y="{y_of(l) + 10:.0f}" text-anchor="end" font-family="InterBlack" font-size="26" fill="{c}">{n}</text>'
                     for l, n, c in ((0, "AWAKE", CORAL), (1, "DREAM", "#c4b0ff"), (2, "LIGHT", "#cfe0ff"), (3, "DEEP", BLUE)))
    grid = "".join(f'<path d="M{x0} {y_of(l):.0f} H{x0 + w}" stroke="#24425f" stroke-width="3" stroke-dasharray="6 10"/>' for l in range(4))
    hrs = "".join(f'<text x="{x_of(t):.0f}" y="{y0 + h + 56}" text-anchor="middle" font-family="InterXB" font-size="26" fill="#96b0c4">{lab}</text>'
                  for t, lab in ((0, "11PM"), (2, "1AM"), (4, "3AM"), (6, "5AM"), (8, "7AM")))
    cpts = " ".join(f"{x_of(t):.1f},{y0 + h - h * v:.1f}" for t, v in CORT)
    svg = f'''<g id="{idp}Axis">{grid}{labels}{hrs}</g>
 <g id="{idp}Deep" opacity="0">{deep}</g>
 <polyline id="{idp}Line" points="{pts}" fill="none" stroke="#FAF4E8" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>
 <polyline id="{idp}Cort" points="{cpts}" fill="none" stroke="{CORAL}" stroke-width="11" stroke-linejoin="round" stroke-linecap="round"/>'''
    return svg, dict(x_of=x_of, y_of=y_of)


def streetcar(x, y, s=1.0, sign="501 QUEEN"):
    """Generic Toronto-style red/white streetcar, side view, top-left (x,y), ~860x300 at s=1. No logos.
    ids: tram (group), tramWin (windows, class 'tw'), wheels class 'wheel', pole 'tramPole'."""
    W_, H_ = 860 * s, 250 * s
    win = "".join(f'<rect class="tw" x="{x + (70 + k * 128) * s:.0f}" y="{y + 52 * s:.0f}" width="{104 * s:.0f}" height="{92 * s:.0f}" rx="{12 * s:.0f}" fill="#ffe7a3" stroke="{INK}" stroke-width="{5 * s:.0f}"/>' for k in range(6))
    def wheel(wx): return (f'<g class="wheel"><circle cx="{wx:.0f}" cy="{y + H_ + 6 * s:.0f}" r="{30 * s:.0f}" fill="#20242e" stroke="{INK}" stroke-width="{6 * s:.0f}"/>'
                           f'<path d="M{wx - 18 * s:.0f} {y + H_ + 6 * s:.0f} H{wx + 18 * s:.0f}" stroke="#9aa3ab" stroke-width="{6 * s:.0f}"/></g>')
    return f'''<g id="tram">
 <path id="tramPole" d="M{x + 300 * s:.0f} {y} L{x + 420 * s:.0f} {y - 150 * s:.0f}" stroke="{INK}" stroke-width="{8 * s:.0f}" stroke-linecap="round"/>
 <path d="M{x + 400 * s:.0f} {y - 150 * s:.0f} H{x + 470 * s:.0f}" stroke="{INK}" stroke-width="{10 * s:.0f}" stroke-linecap="round"/>
 <ellipse cx="{x + W_ / 2:.0f}" cy="{y + H_ + 34 * s:.0f}" rx="{W_ * .55:.0f}" ry="{16 * s:.0f}" fill="#000" opacity=".35"/>
 <path d="M{x + 40 * s:.0f} {y} H{x + W_ - 40 * s:.0f} Q{x + W_:.0f} {y} {x + W_:.0f} {y + 60 * s:.0f} V{y + H_:.0f} H{x:.0f} V{y + 60 * s:.0f} Q{x:.0f} {y} {x + 40 * s:.0f} {y}Z" fill="#d7262e" stroke="{INK}" stroke-width="{8 * s:.0f}"/>
 <rect x="{x}" y="{y + 160 * s:.0f}" width="{W_:.0f}" height="{36 * s:.0f}" fill="#f4f4ef"/>
 <rect x="{x}" y="{y + 196 * s:.0f}" width="{W_:.0f}" height="{12 * s:.0f}" fill="{INK}" opacity=".85"/>
 <rect x="{x + W_ - 230 * s:.0f}" y="{y + 12 * s:.0f}" width="{190 * s:.0f}" height="{30 * s:.0f}" rx="{6 * s:.0f}" fill="#111"/>
 <text x="{x + W_ - 135 * s:.0f}" y="{y + 35 * s:.0f}" text-anchor="middle" font-family="InterBlack" font-size="{20 * s:.0f}" fill="#ff9a2e" letter-spacing="1">{sign}</text>
 {win}
 <rect x="{x + 20 * s:.0f}" y="{y + 52 * s:.0f}" width="{40 * s:.0f}" height="{140 * s:.0f}" rx="{8 * s:.0f}" fill="#9fc3e8" stroke="{INK}" stroke-width="{5 * s:.0f}"/>
 <circle cx="{x + W_ - 14 * s:.0f}" cy="{y + 214 * s:.0f}" r="{10 * s:.0f}" fill="{GOLD}"/>
 {wheel(x + 130 * s)}{wheel(x + 230 * s)}{wheel(x + W_ - 230 * s)}{wheel(x + W_ - 130 * s)}
</g>'''


def stop_pole(x, base, h=420, label="STOP"):
    """Streetcar stop pole with a red-and-white sign (generic)."""
    return (f'<g id="stopPole"><rect x="{x - 9}" y="{base - h}" width="18" height="{h}" fill="#9aa3ab" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x - 70}" y="{base - h - 70}" width="140" height="120" rx="14" fill="#f4f4ef" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{x - 70}" y="{base - h - 70}" width="140" height="40" rx="14" fill="#d7262e" stroke="{INK}" stroke-width="7"/>'
            f'<text x="{x}" y="{base - h - 40}" text-anchor="middle" font-family="InterBlack" font-size="26" fill="#fff">{label}</text>'
            f'<path d="M{x - 40} {base - h + 6} h80 M{x - 40} {base - h + 26} h60" stroke="{INK}" stroke-width="8" stroke-linecap="round"/></g>')


def window(x, y, w=420, h=520, idp="win"):
    """Bedroom window at night: frame, panes, sill. ids: {idp}Sky (rect behind the panes, recolour it), {idp}Glass."""
    return f'''<g id="{idp}">
 <rect id="{idp}Sky" x="{x}" y="{y}" width="{w}" height="{h}" fill="#0b1630"/>
 <rect id="{idp}Glass" x="{x}" y="{y}" width="{w}" height="{h}" fill="#9fc3e8" opacity=".08"/>
 <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#f4f4ef" stroke-width="22"/>
 <path d="M{x + w / 2} {y} V{y + h} M{x} {y + h / 2} H{x + w}" stroke="#f4f4ef" stroke-width="16"/>
 <rect x="{x - 30}" y="{y + h}" width="{w + 60}" height="26" rx="8" fill="#e7e2d6" stroke="{INK}" stroke-width="6"/>
 <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="6"/>
</g>'''


def lamp(x, base, idp="lamp"):
    """Desk light-therapy lamp (flat white panel on a stand). ids: {idp}Panel (fill it bright when on), {idp}Beam."""
    return f'''<g id="{idp}">
 <path id="{idp}Beam" d="M{x - 90} {base - 330} L{x - 700} {base + 120} L{x + 500} {base + 120} L{x + 90} {base - 330}Z" fill="#fffbe8" opacity="0"/>
 <rect x="{x - 110}" y="{base - 26}" width="220" height="26" rx="10" fill="#cfd5dc" stroke="{INK}" stroke-width="6"/>
 <rect x="{x - 10}" y="{base - 200}" width="20" height="180" fill="#cfd5dc" stroke="{INK}" stroke-width="5"/>
 <rect id="{idp}Panel" x="{x - 120}" y="{base - 420}" width="240" height="230" rx="22" fill="#4a5568" stroke="{INK}" stroke-width="8"/>
 <path d="M{x - 90} {base - 390} h180 M{x - 90} {base - 350} h180 M{x - 90} {base - 310} h180 M{x - 90} {base - 270} h180 M{x - 90} {base - 230} h180" stroke="{INK}" stroke-width="3" opacity=".25"/>
</g>'''


# ---- Ep 11 (Diwali, Scarborough-led) pieces — generic shapes, no real names/logos -------------------------
SAFFRON, MAGENTA, LEAFS = "#f57c1f", "#e0457b", "#1f4fa3"


def scarb_skyline(W, base, s=1.0, seed=11, lit=.4, ground=NAVY, mall=True):
    """Scarborough Town Centre area at dusk: clusters of tall condo towers (some with crowns), low flat mall
    silhouette in front, hydro corridor pylon. Windows class 'win'. No CN Tower (that's downtown)."""
    rnd = random.Random(seed); out = []
    x = -30
    while x < W:   # far towers
        w = rnd.uniform(60, 110) * s; h = rnd.uniform(260, 520) * s
        out.append(f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#1b2c48"/>'); x += w + rnd.uniform(30, 80) * s
    x = -10
    while x < W:   # near condo towers
        w = rnd.uniform(90, 140) * s; h = rnd.uniform(300, 620) * s
        out.append(f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h + 4:.0f}" fill="#22385a" stroke="{INK}" stroke-width="{5 * s:.0f}"/>')
        if rnd.random() < .5:
            out.append(f'<rect x="{x + w * .2:.0f}" y="{base - h - 26 * s:.0f}" width="{w * .6:.0f}" height="{26 * s:.0f}" fill="#2c4670" stroke="{INK}" stroke-width="{4 * s:.0f}"/>')
        for wy in range(int(base - h + 16 * s), int(base - 10 * s), int(24 * s)):
            out.append(f'<rect x="{x + 6 * s:.0f}" y="{wy + 14 * s:.0f}" width="{w - 12 * s:.0f}" height="{3 * s:.0f}" fill="#30507c"/>')   # balcony lines
            for wx in range(int(x + 12 * s), int(x + w - 14 * s), int(22 * s)):
                if rnd.random() < lit:
                    out.append(f'<rect class="win" x="{wx}" y="{wy}" width="{11 * s:.0f}" height="{12 * s:.0f}" fill="{GOLD}" opacity="{rnd.uniform(.55, .95):.2f}"/>')
        x += w + rnd.uniform(40, 120) * s
    if mall:   # long low mall box with a flat roof band (generic, no signage)
        out.append(f'<rect id="mall" x="{W * .05:.0f}" y="{base - 90 * s:.0f}" width="{W * .6:.0f}" height="{94 * s:.0f}" fill="#2a3c5c" stroke="{INK}" stroke-width="{6 * s:.0f}"/>'
                   f'<rect x="{W * .05:.0f}" y="{base - 90 * s:.0f}" width="{W * .6:.0f}" height="{18 * s:.0f}" fill="#3a5482"/>'
                   + "".join(f'<rect x="{W * .08 + k * 70 * s:.0f}" y="{base - 52 * s:.0f}" width="{40 * s:.0f}" height="{30 * s:.0f}" fill="#ffe7a3" opacity=".7"/>' for k in range(int(W * .55 / (70 * s)))))
    out.append(f'<rect x="-50" y="{base}" width="{W + 100}" height="1200" fill="{ground}"/>')
    return "".join(out)


def diya(x, y, s=1.0, cls="diyaF"):
    """Small clay oil lamp with a flame (flame class `cls` for flicker)."""
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="-30" rx="40" ry="34" fill="{GOLD}" opacity=".18"/>'
            f'<path class="{cls}" d="M0 -58 Q12 -38 0 -24 Q-12 -38 0 -58Z" fill="{GOLD}" stroke="{CORAL}" stroke-width="3" style="transform-box:fill-box;transform-origin:50% 100%"/>'
            f'<path d="M-34 -20 Q0 -14 34 -20 Q28 6 0 8 Q-28 6 -34 -20Z" fill="#c4542a" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-24 -10 h48" stroke="{GOLD}" stroke-width="4" stroke-dasharray="4 6"/></g>')


def balcony(x, y, w, n_diya=5, raccoon=False):
    """Condo balcony railing with a row of diyas on the ledge (+ optional raccoon easter egg)."""
    rails = "".join(f'<rect x="{x + k * 34}" y="{y + 10}" width="10" height="120" fill="#9aa3ab"/>' for k in range(int(w / 34)))
    ds = "".join(diya(x + 40 + k * (w - 80) / max(1, n_diya - 1), y, .9) for k in range(n_diya))
    rc = ""
    if raccoon:
        rx, ry = x + w - 120, y + 4
        rc = (f'<g id="raccoon"><ellipse cx="{rx}" cy="{ry - 40}" rx="46" ry="36" fill="#7d8590" stroke="{INK}" stroke-width="6"/>'
              f'<path d="M{rx - 40} {ry - 44} q40 -18 80 0 v16 q-40 -14 -80 0z" fill="{INK}"/>'
              f'<circle cx="{rx - 18}" cy="{ry - 38}" r="6" fill="#fff"/><circle cx="{rx + 18}" cy="{ry - 38}" r="6" fill="#fff"/>'
              f'<path d="M{rx - 40} {ry - 66} l8 -22 l14 16z M{rx + 40} {ry - 66} l-8 -22 l-14 16z" fill="#7d8590" stroke="{INK}" stroke-width="5"/>'
              f'<circle cx="{rx}" cy="{ry - 22}" r="6" fill="{INK}"/></g>')
    return (f'<g id="balcony">{rc}{ds}<rect x="{x}" y="{y}" width="{w}" height="16" rx="6" fill="#cfd5dc" stroke="{INK}" stroke-width="5"/>{rails}'
            f'<rect x="{x}" y="{y + 126}" width="{w}" height="14" fill="#cfd5dc" stroke="{INK}" stroke-width="5"/></g>')


def bluffs_view(x, y, w, h, idp="bv"):
    """What a Scarborough window sees at dusk: lake glow + the pale Bluffs cliffs dropping to the water."""
    return (f'<g id="{idp}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#2b3f6b"/>'
            f'<rect x="{x}" y="{y + h * .45:.0f}" width="{w}" height="{h * .2:.0f}" fill="#f2a76a" opacity=".55"/>'
            f'<rect x="{x}" y="{y + h * .58:.0f}" width="{w}" height="{h * .42:.0f}" fill="#22508a"/>'
            f'<path d="M{x + w * .55:.0f} {y + h * .58:.0f} h{w * .4:.0f}" stroke="#ffd9a8" stroke-width="5" opacity=".7"/>'
            f'<path d="M{x} {y + h * .32:.0f} L{x + w * .18:.0f} {y + h * .3:.0f} L{x + w * .3:.0f} {y + h * .44:.0f} L{x + w * .42:.0f} {y + h * .4:.0f} L{x + w * .52:.0f} {y + h * .66:.0f} L{x} {y + h * .7:.0f}Z" fill="#e8dcc0" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M{x + w * .1:.0f} {y + h * .36:.0f} l18 60 M{x + w * .24:.0f} {y + h * .36:.0f} l14 70 M{x + w * .36:.0f} {y + h * .45:.0f} l12 60" stroke="#c9b892" stroke-width="5"/>'
            f'<path d="M{x} {y + h * .32:.0f} L{x + w * .18:.0f} {y + h * .3:.0f} L{x + w * .3:.0f} {y + h * .44:.0f}" stroke="#3d6b3a" stroke-width="12" fill="none"/></g>')


def platform_view(x, y, w, h, idp="pv"):
    """Kennedy-style end-of-line subway platform seen through a window: yellow edge strip, train with doors, bus bay behind."""
    return (f'<g id="{idp}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1c2a40"/>'
            f'<rect x="{x}" y="{y + h * .12:.0f}" width="{w}" height="{h * .08:.0f}" fill="#2a3a55"/>'
            + "".join(f'<rect x="{x + 20 + k * 90}" y="{y + h * .14:.0f}" width="60" height="10" fill="#fff8d0" opacity=".8"/>' for k in range(int(w / 90)))
            + f'<g id="{idp}Train"><rect x="{x - 20}" y="{y + h * .3:.0f}" width="{w * 1.4:.0f}" height="{h * .36:.0f}" rx="16" fill="#cfd5dc" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x - 20}" y="{y + h * .5:.0f}" width="{w * 1.4:.0f}" height="{h * .05:.0f}" fill="#d7262e"/>'
            + "".join(f'<rect x="{x + k * 150}" y="{y + h * .35:.0f}" width="90" height="{h * .12:.0f}" rx="8" fill="#ffe7a3" stroke="{INK}" stroke-width="4"/>' for k in range(int(w * 1.4 / 150)))
            + f'</g><rect x="{x}" y="{y + h * .7:.0f}" width="{w}" height="{h * .06:.0f}" fill="{GOLD}"/>'
            f'<rect x="{x}" y="{y + h * .76:.0f}" width="{w}" height="{h * .24:.0f}" fill="#5b6472"/></g>')


def hallway(W, H, idp="hw"):
    """Scarborough high-rise hallway: patterned carpet, elevator doors (ids {idp}DL/{idp}DR), apartment door with mail slot."""
    carpet = "".join(f'<path d="M{-200 + k * 120} 1920 L{420 + k * 40} 980" stroke="#7a2f3a" stroke-width="18" opacity=".5"/>' for k in range(14))
    return f'''<g id="{idp}">
 <rect x="0" y="0" width="{W}" height="{H}" fill="#c9b99a"/>
 <rect x="0" y="0" width="{W}" height="140" fill="#e8e0cc"/>{"".join(f'<rect x="{80 + k * 260}" y="40" width="140" height="40" rx="10" fill="#fffbe8"/>' for k in range(4))}
 <rect x="0" y="960" width="{W}" height="{H - 960}" fill="#8e3c48"/>{carpet}
 <rect x="0" y="940" width="{W}" height="26" fill="#6b5a44"/>
 <g id="{idp}Elev"><rect x="80" y="330" width="420" height="612" fill="#7b8592" stroke="{INK}" stroke-width="8"/>
  <rect x="96" y="346" width="388" height="596" fill="#2a3346"/>
  <rect id="{idp}DL" x="96" y="346" width="194" height="596" fill="#b9c1ca" stroke="{INK}" stroke-width="5"/>
  <rect id="{idp}DR" x="290" y="346" width="194" height="596" fill="#b9c1ca" stroke="{INK}" stroke-width="5"/>
  <rect x="200" y="270" width="180" height="44" rx="8" fill="#111"/><path id="{idp}Arrow" d="M290 280 l16 22 h-32z" fill="{GOLD}"/>
  <circle cx="540" cy="620" r="16" fill="#e8e0cc" stroke="{INK}" stroke-width="5"/><circle cx="540" cy="670" r="16" fill="#e8e0cc" stroke="{INK}" stroke-width="5"/></g>
 <g id="{idp}Door"><rect x="680" y="380" width="300" height="562" fill="#6e4a2e" stroke="{INK}" stroke-width="8"/>
  <rect x="700" y="400" width="260" height="240" fill="#80583a" stroke="{INK}" stroke-width="4"/>
  <rect id="{idp}Slot" x="760" y="700" width="140" height="28" rx="6" fill="#d9c27a" stroke="{INK}" stroke-width="5"/>
  <circle cx="940" cy="760" r="14" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>
  <rect x="800" y="440" width="60" height="60" rx="30" fill="#2a3346" stroke="#d9c27a" stroke-width="6"/></g>
</g>'''


def il1_cell(x, y, s=1.0, idp="m1"):
    """IL-1 messenger: tiny round immune-messenger cartoon holding a 'zzz' flag. Groups {idp} / {idp}Flag."""
    return (f'<g id="{idp}" transform="translate({x},{y}) scale({s})"><g class="bob">'
            f'<g id="{idp}Flag"><path d="M34 -10 V-120" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M34 -120 h86 l-16 26 l16 26 h-86z" fill="#c4b0ff" stroke="{INK}" stroke-width="5"/>'
            f'<text x="74" y="-84" text-anchor="middle" font-family="InterBlack" font-size="30" fill="{INK}">zzz</text></g>'
            f'<circle cx="0" cy="0" r="46" fill="{CORAL}" stroke="{INK}" stroke-width="7"/>'
            + "".join(f'<circle cx="{46 * math.cos(a):.0f}" cy="{46 * math.sin(a):.0f}" r="9" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>' for a in [k * math.pi / 4 for k in range(8)])
            + f'<circle cx="-14" cy="-8" r="9" fill="#fff" stroke="{INK}" stroke-width="3"/><circle cx="14" cy="-8" r="9" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="-14" cy="-6" r="4" fill="{INK}"/><circle cx="14" cy="-6" r="4" fill="{INK}"/>'
            f'<path d="M-12 14 q12 10 24 0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/></g></g>')


def mithai_plate(cx, cy, s=1.0, idp="mp"):
    """Steel thali with mithai: ladoos (orange balls), barfi diamonds (silver leaf), jalebi spirals. Pieces class 'sweet'."""
    lad = "".join(f'<g class="sweet"><circle cx="{cx + dx * s:.0f}" cy="{cy + dy * s:.0f}" r="{34 * s:.0f}" fill="#f5a524" stroke="{INK}" stroke-width="5"/>'
                  + "".join(f'<circle cx="{cx + (dx + ex) * s:.0f}" cy="{cy + (dy + ey) * s:.0f}" r="{4 * s:.0f}" fill="#e07b10"/>' for ex, ey in ((-12, -8), (10, -12), (0, 8), (14, 10), (-14, 12)))
                  + '</g>' for dx, dy in ((-120, -20), (-60, -50), (-80, 20)))
    bar = "".join(f'<g class="sweet"><path d="M{cx + dx * s:.0f} {cy + (dy - 34) * s:.0f} l{34 * s:.0f} {34 * s:.0f} l{-34 * s:.0f} {34 * s:.0f} l{-34 * s:.0f} {-34 * s:.0f}z" fill="#f4ecd8" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M{cx + (dx - 14) * s:.0f} {cy + dy * s:.0f} l{14 * s:.0f} {-14 * s:.0f} l{14 * s:.0f} {14 * s:.0f}" stroke="#b9c1ca" stroke-width="{5 * s:.0f}" fill="none"/></g>' for dx, dy in ((40, -40), (100, -10), (50, 30)))
    jal = "".join(f'<g class="sweet"><path d="M{cx + dx * s:.0f} {cy + dy * s:.0f} m-30 0 a30 30 0 1 1 60 0 a22 22 0 1 1 -44 0 a14 14 0 1 1 28 0 a6 6 0 1 1 -12 0" fill="none" stroke="#f08a1c" stroke-width="{11 * s:.0f}" stroke-linecap="round"/></g>' for dx, dy in ((150, 50), (-20, 60)))
    return (f'<g id="{idp}"><ellipse cx="{cx}" cy="{cy + 30 * s:.0f}" rx="{230 * s:.0f}" ry="{70 * s:.0f}" fill="#000" opacity=".25"/>'
            f'<ellipse cx="{cx}" cy="{cy + 6 * s:.0f}" rx="{230 * s:.0f}" ry="{120 * s:.0f}" fill="#c7cdd4" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="{cx}" cy="{cy + 6 * s:.0f}" rx="{190 * s:.0f}" ry="{96 * s:.0f}" fill="#e2e6ea"/>{lad}{bar}{jal}</g>')


def couch(x, y, w=760, idp="couch"):
    """Living-room couch with a Leafs-blue throw blanket (no logo). Top-left (x,y)."""
    return (f'<g id="{idp}"><rect x="{x}" y="{y}" width="{w}" height="200" rx="40" fill="#7a5a8c" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="{x + 30}" y="{y + 150}" width="{w - 60}" height="140" rx="30" fill="#8d6aa0" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="{x - 30}" y="{y + 100}" width="90" height="210" rx="34" fill="#6b4c7c" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="{x + w - 60}" y="{y + 100}" width="90" height="210" rx="34" fill="#6b4c7c" stroke="{INK}" stroke-width="8"/>'
            f'<path id="{idp}Blanket" d="M{x + w * .62:.0f} {y + 30} q{w * .15:.0f} -26 {w * .3:.0f} 6 l-6 230 q{-w * .16:.0f} 34 {-w * .3:.0f} 4 q20 -110 6 -240z" fill="{LEAFS}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M{x + w * .66:.0f} {y + 120} q{w * .12:.0f} 10 {w * .24:.0f} 0 M{x + w * .66:.0f} {y + 150} q{w * .12:.0f} 10 {w * .24:.0f} 0" stroke="#fff" stroke-width="9" fill="none"/></g>')


def rangoli(cx, cy, r=180, idp="rg"):
    """Flat rangoli rug: concentric petal rings in saffron/magenta/teal/gold. Rings class 'rring' (spin them)."""
    rings = []
    for k, (n, rr, col) in enumerate(((16, r, SAFFRON), (12, r * .72, MAGENTA), (8, r * .46, TEAL), (6, r * .24, GOLD))):
        pet = "".join(f'<ellipse cx="{cx + rr * .78 * math.cos(2 * math.pi * i / n):.0f}" cy="{cy + rr * .78 * math.sin(2 * math.pi * i / n):.0f}" rx="{rr * .26:.0f}" ry="{rr * .12:.0f}" '
                      f'transform="rotate({360 * i / n:.0f} {cx + rr * .78 * math.cos(2 * math.pi * i / n):.0f} {cy + rr * .78 * math.sin(2 * math.pi * i / n):.0f})" fill="{col}" stroke="{INK}" stroke-width="4"/>' for i in range(n))
        rings.append(f'<g class="rring" style="transform-origin:{cx}px {cy}px">{pet}</g>')
    return f'<g id="{idp}" transform="translate(0,0)"><circle cx="{cx}" cy="{cy}" r="{r * 1.08:.0f}" fill="#f4ecd8" stroke="{INK}" stroke-width="6"/>{"".join(rings)}<circle cx="{cx}" cy="{cy}" r="{r * .1:.0f}" fill="{MAGENTA}" stroke="{INK}" stroke-width="4"/></g>'


def string_lights(W, y, n=18, sag=40, idp="sl", seed=5):
    """Festive string lights across a street (bulbs class 'bulb')."""
    rnd = random.Random(seed); cols = (GOLD, SAFFRON, MAGENTA, TEAL, "#c4b0ff")
    pts = [(W * i / (n - 1), y + sag * math.sin(math.pi * i / (n - 1))) for i in range(n)]
    path = "M" + " L".join(f"{x:.0f} {yy:.0f}" for x, yy in pts)
    bulbs = "".join(f'<circle class="bulb" cx="{x:.0f}" cy="{yy + 14:.0f}" r="11" fill="{rnd.choice(cols)}" stroke="{INK}" stroke-width="3"/>' for x, yy in pts)
    return f'<g id="{idp}"><path d="{path}" stroke="{INK}" stroke-width="4" fill="none"/>{bulbs}</g>'


def stomach(cx, cy, s=1.0, idp="st"):
    """Cartoon stomach (J-shape) that can fill up: fill rect id {idp}Fill clipped to the stomach."""
    d = (f"M{cx - 40 * s:.0f} {cy - 150 * s:.0f} q0 60 30 80 q120 -40 140 60 q20 130 -120 150 q-90 10 -130 -40 "
         f"q-20 -30 10 -40 q40 30 90 10 q60 -30 30 -90 q-20 -40 -60 -10 q-40 -20 -40 -120z")
    return (f'<g id="{idp}"><clipPath id="{idp}Clip"><path d="{d}"/></clipPath>'
            f'<path d="{d}" fill="#f2b8b8" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<g clip-path="url(#{idp}Clip)"><rect id="{idp}Fill" x="{cx - 200 * s:.0f}" y="{cy - 160 * s:.0f}" width="{420 * s:.0f}" height="{340 * s:.0f}" fill="#e07b5a"/></g>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/></g>')


# ---- Ep 12 (Movember) Toronto pieces ---------------------------------------------------------------------
def univ_ave(W, base, idp="ua"):
    """University Ave 'hospital row' at dawn (generic boxy towers, rooftop helipad 'H', no signage) with the
    Queen's Park legislature outline (central tower + small dome) closing the avenue, median planters with trees.
    Windows class 'win'. ids: {idp}QP (legislature), {idp}Trees."""
    rnd = random.Random(12); out = []
    # far towers
    x = -20
    while x < W:
        w = rnd.uniform(80, 150); h = rnd.uniform(260, 520)
        out.append(f'<rect x="{x:.0f}" y="{base - 260 - h:.0f}" width="{w:.0f}" height="{h + 260:.0f}" fill="#6b5a86" opacity=".55"/>'); x += w + rnd.uniform(6, 20)
    # Queen's Park, centre back
    cx = W / 2; qb = base - 150
    out.append(f'<g id="{idp}QP"><rect x="{cx - 230}" y="{qb - 120}" width="460" height="120" fill="#a0644e" stroke="{INK}" stroke-width="6"/>'
               + "".join(f'<path d="M{cx - 210 + k * 46} {qb - 20} v-60 a14 14 0 0 1 28 0 v60z" fill="#5a3326"/>' for k in range(10))
               + f'<rect x="{cx - 60}" y="{qb - 220}" width="120" height="110" fill="#b06f56" stroke="{INK}" stroke-width="6"/>'
               f'<path d="M{cx - 40} {qb - 220} Q{cx} {qb - 300} {cx + 40} {qb - 220}Z" fill="#6f8f7e" stroke="{INK}" stroke-width="6"/>'
               f'<rect x="{cx - 5}" y="{qb - 330}" width="10" height="40" fill="{INK}"/>'
               f'<path d="M{cx - 240} {qb - 120} L{cx - 200} {qb - 160} L{cx - 150} {qb - 120}Z M{cx + 150} {qb - 120} L{cx + 200} {qb - 160} L{cx + 240} {qb - 120}Z" fill="#8a4f3d" stroke="{INK}" stroke-width="5"/></g>')
    # hospital-row slabs, both sides of the avenue (perspective-ish: big on the edges)
    for side in (-1, 1):
        for k, (w, h) in enumerate(((300, 900), (220, 700), (160, 520))):
            x0 = (0 - 40 + k * 150) if side < 0 else (W + 40 - k * 150 - w)
            top = base - h
            out.append(f'<rect x="{x0}" y="{top}" width="{w}" height="{h + 4}" fill="{["#3d4f6e", "#4a5d7d", "#576a8a"][k]}" stroke="{INK}" stroke-width="6"/>')
            if k == 0:
                hx = x0 + w / 2
                out.append(f'<rect x="{hx - 70}" y="{top - 24}" width="140" height="24" fill="#2b3a55" stroke="{INK}" stroke-width="5"/>'
                           f'<circle cx="{hx}" cy="{top - 24}" r="0"/><ellipse cx="{hx}" cy="{top - 26}" rx="62" ry="12" fill="#e8e0cc" stroke="{INK}" stroke-width="4"/>'
                           f'<path d="M{hx - 12} {top - 32} v12 M{hx + 12} {top - 32} v12 M{hx - 12} {top - 26} h24" stroke="{INK}" stroke-width="4"/>')
            for wy in range(int(top + 30), int(base - 20), 34):
                for wx in range(int(x0 + 18), int(x0 + w - 24), 30):
                    if rnd.random() < .42:
                        out.append(f'<rect class="win" x="{wx}" y="{wy}" width="16" height="18" fill="{GOLD}" opacity="{rnd.uniform(.5, .95):.2f}"/>')
    # avenue + median planters
    out.append(f'<rect x="-50" y="{base}" width="{W + 100}" height="900" fill="#262c3c"/>'
               f'<path d="M{W / 2 - 140} {base} L{W / 2 - 520} {base + 600} L{W / 2 + 520} {base + 600} L{W / 2 + 140} {base}Z" fill="#323a4f"/>'
               f'<path d="M{W / 2} {base + 10} V{base + 600}" stroke="#e8e0cc" stroke-width="8" stroke-dasharray="40 34"/>')
    trees = "".join(f'<g><rect x="{x - 40}" y="{base + 22 + d}" width="80" height="30" rx="6" fill="#8a8f99" stroke="{INK}" stroke-width="4"/>'
                    f'<circle cx="{x}" cy="{base + 4 + d}" r="{30 + d * .2:.0f}" fill="#6b4a2a" stroke="{INK}" stroke-width="4"/></g>' for x, d in ((W / 2 - 300, 40), (W / 2 + 300, 40), (W / 2 - 170, 0), (W / 2 + 170, 0)))
    out.append(f'<g id="{idp}Trees">{trees}</g>')
    return "".join(out)


def subway_platform(W, H, idp="bp"):
    """Bloor-Yonge-style Line 1/2 platform: rounded wall tiles, station name band (place name only, generic font),
    hanging 'NEXT TRAIN 2 MIN' board (generic), yellow tactile edge, a train ({idp}Train) that can slide in/out."""
    tiles = "".join(f'<rect x="{x}" y="{y}" width="52" height="26" rx="6" fill="{c}" stroke="#9aa3ab" stroke-width="2"/>'
                    for y in range(330, 1060, 30) for x in range(-20 + (15 if (y // 30) % 2 else 0), W, 56)
                    for c in [("#e8e4d6" if (x // 56 + y // 30) % 7 else "#d7c9a2")])
    return f'''<g id="{idp}">
 <rect x="0" y="0" width="{W}" height="{H}" fill="#2a2f3a"/>
 <rect x="0" y="0" width="{W}" height="330" fill="#3a404d"/>
 {"".join(f'<rect x="{x}" y="250" width="110" height="16" rx="6" fill="#fff8d0" opacity=".85"/>' for x in range(30, W, 200))}
 {tiles}
 <rect x="-10" y="560" width="{W + 20}" height="40" fill="#d9c27a" stroke="{INK}" stroke-width="6"/>
 <g id="{idp}Sign"><path d="M150 120 V180 M520 120 V180" stroke="{INK}" stroke-width="8"/>
  <rect x="80" y="180" width="510" height="88" rx="12" fill="#d9c27a" stroke="{INK}" stroke-width="6"/>
  <text x="335" y="240" text-anchor="middle" font-family="InterBlack" font-size="46" fill="{INK}" letter-spacing="4">BLOOR-YONGE</text></g>
 <g id="{idp}Train"><rect x="-40" y="700" width="{W + 900}" height="330" rx="26" fill="#cfd5dc" stroke="{INK}" stroke-width="8"/>
  <rect x="-40" y="900" width="{W + 900}" height="26" fill="#d7262e"/>
  {"".join(f'<rect x="{30 + k * 230}" y="740" width="150" height="120" rx="12" fill="#ffe7a3" stroke="{INK}" stroke-width="6"/>' for k in range(int((W + 900) / 230)))}</g>
 <rect x="-10" y="1060" width="{W + 20}" height="40" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>
 <rect x="-10" y="1100" width="{W + 20}" height="{H - 1100}" fill="#5b6472"/>
 <g id="{idp}Board"><path d="M720 120 V170 M920 120 V170" stroke="{INK}" stroke-width="8"/>
  <rect x="660" y="170" width="320" height="110" rx="12" fill="#111" stroke="{INK}" stroke-width="6"/>
  <text x="820" y="215" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#ff9a2e" letter-spacing="2">NEXT TRAIN</text>
  <text id="{idp}Min" x="820" y="260" text-anchor="middle" font-family="InterBlack" font-size="38" fill="#ff9a2e" letter-spacing="2">2 MIN</text></g>
</g>'''


def clinic_street(W, H, idp="cs"):
    """Danforth/Bloor-style low-rise main street: brick storefronts with awnings, one generic 'WALK-IN CLINIC'
    (plain cross, no brand), lamp posts, sidewalk + road with streetcar tracks. Door: {idp}Door."""
    shops = []
    for x, w, c, aw in ((-30, 330, "#8a4b3b", "#3fc1b0"), (300, 480, "#6e7b8a", "#e2394b"), (780, 330, "#7a5a3b", "#FFD166")):
        shops.append(f'<rect x="{x}" y="420" width="{w}" height="620" fill="{c}" stroke="{INK}" stroke-width="6"/>'
                     + "".join(f'<rect x="{x + 30 + k * 90}" y="460" width="60" height="90" rx="6" fill="#ffe7a3" opacity=".7" stroke="{INK}" stroke-width="4"/>' for k in range(int((w - 40) / 90))))
    clinic = (f'<rect x="300" y="640" width="480" height="70" fill="#f4f4ef" stroke="{INK}" stroke-width="6"/>'
              f'<text x="560" y="690" text-anchor="middle" font-family="InterBlack" font-size="40" fill="{INK}" letter-spacing="2">WALK-IN CLINIC</text>'
              f'<g transform="translate(340,675)"><rect x="-10" y="-26" width="20" height="52" fill="#e2394b"/><rect x="-26" y="-10" width="52" height="20" fill="#e2394b"/></g>'
              f'<path d="M290 710 h500 l-30 60 h-440z" fill="#4f86ff" stroke="{INK}" stroke-width="5"/>'
              f'<rect x="330" y="780" width="250" height="230" fill="#cfe6f5" opacity=".85" stroke="{INK}" stroke-width="6"/>'
              f'<rect id="{idp}Door" x="610" y="780" width="140" height="260" fill="#2a4a6a" stroke="{INK}" stroke-width="6"/><circle cx="730" cy="910" r="8" fill="{GOLD}"/>')
    awn = "".join(f'<path d="M{x} 760 h{w} l-20 50 h{-(w - 40)}z" fill="{aw}" stroke="{INK}" stroke-width="5"/>' for x, w, aw in ((-30, 330, "#3fc1b0"), (780, 330, "#FFD166")))
    lamps = "".join(f'<rect x="{x - 7}" y="820" width="14" height="300" fill="#2b3340"/><circle cx="{x}" cy="815" r="22" fill="#ffe7a3" stroke="{INK}" stroke-width="5"/>' for x in (120, 960))
    return f'''<g id="{idp}">{"".join(shops)}{clinic}{awn}
 <rect x="-20" y="1040" width="{W + 40}" height="80" fill="#9aa0a8" stroke="{INK}" stroke-width="5"/>{lamps}
 <rect x="-20" y="1120" width="{W + 40}" height="{H - 1120}" fill="#3a3f4a"/>
 <path d="M-20 1300 H{W + 20} M-20 1340 H{W + 20}" stroke="#7d848e" stroke-width="7"/></g>'''


def ferry_view(W, H, idp="fv"):
    """Toronto skyline from the Island ferry: skyline (CN Tower at x=700), lake with ripples ({idp}Rip), ferry deck rail
    in the foreground. Returns markup; the CN Tower pod sits at about (700, 560) at this scale."""
    rip = "".join(f'<path class="rip" d="M{x} {y} q30 -10 60 0 t60 0" fill="none" stroke="#9fc3e8" stroke-width="5" opacity=".6"/>'
                  for x, y in ((60, 1010), (380, 1040), (700, 1000), (200, 1090), (560, 1120), (860, 1070), (120, 1170), (760, 1180)))
    return f'''<g id="{idp}">{skyline(W, H, 980, 1.0, seed=8, lit=.3, cn=700, ground="#2c5d86")}
 <rect x="-20" y="980" width="{W + 40}" height="300" fill="#2c5d86"/><g id="{idp}Rip">{rip}</g>
 <rect x="-20" y="1250" width="{W + 40}" height="{H - 1250}" fill="#c9cdd2"/>
 <rect x="-20" y="1200" width="{W + 40}" height="22" rx="10" fill="#f4f4ef" stroke="{INK}" stroke-width="6"/>
 {"".join(f'<rect x="{x}" y="1220" width="14" height="60" fill="#f4f4ef" stroke="{INK}" stroke-width="4"/>' for x in range(20, W, 110))}
 <rect x="-20" y="1270" width="{W + 40}" height="16" fill="#9aa0a8"/></g>'''


def handlebar(cx, cy, w=150, fill="#4a2c1a", sticker=True):
    """Cartoon handlebar moustache centred at (cx,cy), width w. sticker=True adds a white die-cut border."""
    k = w / 226
    d = ("M0 -3 C-21 -19 -51 -19 -66 -3 C-79 11 -99 13 -113 -3 C-105 23 -71 27 -46 15 C-25 7 -11 9 0 13 "
         "C11 9 25 7 46 15 C71 27 105 23 113 -3 C99 13 79 11 66 -3 C51 -19 21 -19 0 -3Z")
    tr = f'transform="translate({cx},{cy}) scale({k:.3f})"'
    return ((f'<path d="{d}" {tr} fill="#fff" stroke="#fff" stroke-width="{14 / k:.0f}" stroke-linejoin="round"/>' if sticker else "")
            + f'<path d="{d}" {tr} fill="{fill}" stroke="{INK}" stroke-width="{5 / k:.0f}" stroke-linejoin="round"/>'
            + f'<path d="M-50 -2 C-30 -10 -14 -8 -4 0 M50 -2 C30 -10 14 -8 4 0" {tr} fill="none" stroke="#7a4a2c" stroke-width="{3 / k:.0f}" stroke-linecap="round"/>')


def awareness_ribbon(cx, cy, s=1.0, fill="#4f86ff", hole="#1e56ac"):
    """Generic awareness ribbon (loop + two tails). No logo."""
    return (f'<g transform="translate({cx},{cy}) scale({s})"><path d="M0 -34 C-28 -34 -26 0 -2 20 L-22 50 L-8 56 L4 34 L16 56 L30 50 L10 20 C26 0 28 -34 0 -34Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M0 -20 C-10 -20 -10 -4 2 6 C12 -4 10 -20 0 -20Z" fill="{hole}"/></g>')


# ---------------------------------------------------------------- Ep 13 (Neutro vs the flu)
def union_station(W, base, idp="us"):
    """Union Station front, flat: long colonnade of tall columns under a heavy cornice, three arched entry doors
    (the 'airway entrance'), steps, Front St sidewalk. Carved band reads UNION (place name, no logo). ids: {idp}Doors."""
    top = base - 760
    cols = "".join(f'<rect x="{x}" y="{top + 190}" width="46" height="460" fill="#d9cdb2" stroke="{INK}" stroke-width="5"/>'
                   f'<rect x="{x - 8}" y="{top + 176}" width="62" height="22" fill="#cbbd9e" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="{x - 8}" y="{top + 642}" width="62" height="20" fill="#cbbd9e" stroke="{INK}" stroke-width="4"/>' for x in range(40, W, 108))
    doors = "".join(f'<path d="M{x} {base - 40} V{base - 230} Q{x + 60} {base - 300} {x + 120} {base - 230} V{base - 40}Z" fill="#ffd98a" stroke="{INK}" stroke-width="6"/>'
                    f'<path d="M{x + 60} {base - 40} V{base - 262}" stroke="{INK}" stroke-width="5"/>' for x in (250, 480, 710))
    return f'''<g id="{idp}">
 <rect x="0" y="{top}" width="{W}" height="{base - top}" fill="#c9b994" stroke="{INK}" stroke-width="6"/>
 <rect x="-10" y="{top}" width="{W + 20}" height="120" fill="#bfae86" stroke="{INK}" stroke-width="6"/>
 <rect x="-10" y="{top + 120}" width="{W + 20}" height="56" fill="#d9cdb2" stroke="{INK}" stroke-width="5"/>
 <text x="{W / 2:.0f}" y="{top + 86}" text-anchor="middle" font-family="InterBlack" font-size="64" fill="#8a7a58" letter-spacing="22">UNION</text>
 <rect x="0" y="{top + 196}" width="{W}" height="{base - top - 236}" fill="#3a3326"/>
 <g id="{idp}Doors">{doors}</g>{cols}
 <rect x="-10" y="{base - 40}" width="{W + 20}" height="22" fill="#b3a582" stroke="{INK}" stroke-width="5"/>
 <rect x="-10" y="{base - 18}" width="{W + 20}" height="22" fill="#a49572" stroke="{INK}" stroke-width="5"/>
 <rect x="-10" y="{base + 4}" width="{W + 20}" height="600" fill="#6b7383"/>
</g>'''


def raccoon(x, y, s=1.0, idp="rc"):
    """Little Toronto raccoon, sitting, facing right. (x,y) = bottom centre. Tail id {idp}Tail."""
    return f'''<g transform="translate({x},{y}) scale({s})"><g id="{idp}">
 <g id="{idp}Tail"><path d="M-40 -20 Q-110 -30 -100 -90 Q-70 -60 -36 -48Z" fill="#8a8f99" stroke="{INK}" stroke-width="5"/>
  <path d="M-92 -70 L-74 -56 M-84 -40 L-64 -40" stroke="{INK}" stroke-width="8"/></g>
 <ellipse cx="0" cy="-50" rx="48" ry="52" fill="#9aa0aa" stroke="{INK}" stroke-width="5"/>
 <circle cx="18" cy="-118" r="40" fill="#a8aeb8" stroke="{INK}" stroke-width="5"/>
 <path d="M-8 -150 L-2 -176 L14 -156Z M30 -156 L44 -174 L48 -148Z" fill="#7d838d" stroke="{INK}" stroke-width="4"/>
 <path d="M-14 -126 Q18 -142 54 -124 Q52 -106 18 -110 Q-12 -106 -14 -126Z" fill="{INK}"/>
 <circle cx="6" cy="-122" r="6" fill="#fff"/><circle cx="36" cy="-122" r="6" fill="#fff"/>
 <ellipse cx="52" cy="-102" rx="9" ry="7" fill="{INK}"/>
</g></g>'''


def go_train(x, y, s=1.0, cars=4, idp="go"):
    """Generic GO-style bi-level commuter train, side view (white with green band, no logo), top-left (x,y)."""
    out = []
    for k in range(cars):
        cx = x + k * 520 * s
        out.append(f'<path d="M{cx} {y + 40 * s:.0f} Q{cx} {y} {cx + 40 * s:.0f} {y} H{cx + 470 * s:.0f} Q{cx + 510 * s:.0f} {y} {cx + 510 * s:.0f} {y + 40 * s:.0f} V{y + 200 * s:.0f} H{cx}Z" fill="#f2f2ec" stroke="{INK}" stroke-width="{6 * s:.0f}"/>'
                   f'<rect x="{cx}" y="{y + 150 * s:.0f}" width="{510 * s:.0f}" height="{30 * s:.0f}" fill="#2f8f4e"/>'
                   + "".join(f'<rect x="{cx + (30 + j * 80) * s:.0f}" y="{y + r * s:.0f}" width="{56 * s:.0f}" height="{40 * s:.0f}" rx="{6 * s:.0f}" fill="#33415a" stroke="{INK}" stroke-width="{3 * s:.0f}"/>' for j in range(6) for r in (30, 92)))
    return f'<g id="{idp}">{"".join(out)}</g>'


def queen_snow(W, H, idp="qs"):
    """Snowy Queen St East, flat: grey sky, low-rise brick shops, a raised rail corridor with a GO train
    ({idp}Go) crossing behind, snowbanks, road with streetcar tracks (the 'thin line'). Snow drift id {idp}Banks."""
    rnd = random.Random(31)
    shops = "".join(f'<rect x="{x}" y="{560 - h}" width="{w}" height="{h + 300}" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                    f'<rect x="{x + 18}" y="{660}" width="{w - 36}" height="110" fill="#ffe7a3" stroke="{INK}" stroke-width="4"/>'
                    + "".join(f'<rect x="{x + 22 + k * 52}" y="{590 - h + 40}" width="34" height="46" fill="#fff4c8" stroke="{INK}" stroke-width="3"/>' for k in range(max(1, (w - 30) // 52)))
                    for x, w, h, c in [(-20, 220, 120, "#9a4f3c"), (200, 180, 160, "#b5674a"), (380, 240, 100, "#7e4a3a"), (620, 200, 150, "#a3593f"), (820, 280, 130, "#8c4e3c")])
    flakes = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(260, 1500):.0f}" r="{rnd.uniform(3, 7):.0f}" fill="#fff" opacity=".7"/>' for _ in range(40))
    return f'''<g id="{idp}">
 <rect x="0" y="0" width="{W}" height="{H}" fill="#aab4c4"/>
 <rect x="-10" y="300" width="{W + 20}" height="120" fill="#7a8292" stroke="{INK}" stroke-width="5"/>
 <g id="{idp}Go">{go_train(0, 190, .55, 5)}</g>
 <path d="M-10 404 H{W + 10}" stroke="{INK}" stroke-width="8"/>
 {shops}
 <rect x="-10" y="860" width="{W + 20}" height="{H - 860}" fill="#5d6574"/>
 <path id="{idp}Banks" d="M-10 880 Q120 840 260 878 Q420 846 560 880 Q740 842 900 878 Q1000 852 1090 870 V900 H-10Z" fill="#f4f6fa" stroke="{INK}" stroke-width="5"/>
 <path d="M-10 1180 H{W + 10} M-10 1240 H{W + 10}" stroke="#2c323e" stroke-width="10"/>
 <path d="M-10 1180 H{W + 10} M-10 1240 H{W + 10}" stroke="#a7afbd" stroke-width="4"/>
 {flakes}
</g>'''


def pharmacy_nps(W, H, idp="ph", py=0, shop=True):
    """Nathan Phillips Square at dusk (city_hall + rink with skaters + arches) seen past a generic corner pharmacy
    window: green cross, 'FLU SHOTS' sign in the glass (no brand). ids: {idp}Sign, {idp}Skaters (class 'sk')."""
    sk = "".join(f'<g class="sk" transform="translate({x},{1000})"><circle cx="0" cy="-58" r="14" fill="{c}" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M0 -44 V-14 M0 -14 L-12 6 M0 -14 L14 4 M0 -36 L-16 -24 M0 -36 L18 -28" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>'
                 for x, c in ((470, "#FF7A59"), (640, "#4f86ff"), (820, "#FFD166"), (960, "#5AE68C")))
    return f'''<g id="{idp}">
 <rect x="0" y="0" width="{W}" height="{H}" fill="url(#{idp}Sky)"/>
 <defs><linearGradient id="{idp}Sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3566"/><stop offset=".5" stroke-color="#6a5a8a" stop-color="#7a6a96"/><stop offset="1" stop-color="#e3a07a"/></linearGradient></defs>
 <g transform="translate(160,0)">{city_hall(560, 900, .78)}</g>
 <rect x="380" y="900" width="{W - 380}" height="140" fill="#cfe6f2" stroke="{INK}" stroke-width="5"/>
 <g id="{idp}Skaters">{sk}</g>
 <rect x="-10" y="1040" width="{W + 20}" height="{H - 1040}" fill="#4d5566"/>
 <g transform="translate(0,{py})" display="{'inline' if shop else 'none'}"><rect x="0" y="180" width="400" height="1100" fill="#e8e2d2" stroke="{INK}" stroke-width="6"/>
 <rect x="30" y="300" width="340" height="560" rx="10" fill="#bfe0ee" stroke="{INK}" stroke-width="6"/>
 <path d="M30 300 L370 600 M120 300 L370 520" stroke="#fff" stroke-width="10" opacity=".35"/>
 <g transform="translate(200,240)"><rect x="-90" y="-40" width="180" height="70" rx="12" fill="#fff" stroke="{INK}" stroke-width="5"/>
  <path d="M-14 -30 H14 V-12 H32 V16 H14 V34 H-14 V16 H-32 V-12 H-14Z" transform="scale(.8)" fill="#2fa36b" stroke="{INK}" stroke-width="4"/></g>
 <g id="{idp}Sign"><rect x="66" y="380" width="268" height="150" rx="14" fill="#FAF4E8" stroke="#2fa36b" stroke-width="8"/>
  <text x="200" y="448" text-anchor="middle" font-family="InterBlack" font-size="44" fill="#2fa36b">FLU</text>
  <text x="200" y="500" text-anchor="middle" font-family="InterBlack" font-size="44" fill="#2fa36b">SHOTS</text></g>
 <rect x="30" y="860" width="340" height="40" fill="#2fa36b" stroke="{INK}" stroke-width="5"/></g>
</g>'''


def virus(cx, cy, r=26, fill="#7fd36b", cls="vir"):
    """Flu virus: green ball with spikes (class cls for animation). Origin = centre."""
    spikes = "".join(f'<path d="M{math.cos(a) * r:.1f} {math.sin(a) * r:.1f} L{math.cos(a) * r * 1.45:.1f} {math.sin(a) * r * 1.45:.1f}" stroke="{INK}" stroke-width="{max(3, r * .16):.0f}" stroke-linecap="round"/>'
                     f'<circle cx="{math.cos(a) * r * 1.5:.1f}" cy="{math.sin(a) * r * 1.5:.1f}" r="{r * .16:.1f}" fill="#FF7A59" stroke="{INK}" stroke-width="2"/>' for a in [k * math.pi / 4 for k in range(8)])
    return (f'<g transform="translate({cx},{cy})"><g class="{cls}">{spikes}<circle r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{max(3, r * .15):.0f}"/>'
            f'<circle cx="{-r * .3:.1f}" cy="{-r * .3:.1f}" r="{r * .25:.1f}" fill="#fff" opacity=".5"/></g></g>')


def lungs(cx, cy, s=1.0, idp="lg"):
    """Pair of flat lungs + trachea. Lobes {idp}L / {idp}R (fill can be animated), damage cracks {idp}Hurt (class 'crk')."""
    L = "M-30 -120 Q-150 -140 -190 40 Q-210 190 -110 200 Q-40 205 -30 120Z"
    R = "M30 -120 Q150 -140 190 40 Q210 190 110 200 Q40 205 30 120Z"
    cr = "".join(f'<path class="crk" d="{d}" fill="none" stroke="#b3142a" stroke-width="7" stroke-linecap="round" stroke-dasharray="200" stroke-dashoffset="200"/>'
                 for d in ("M-150 20 L-120 50 L-140 90 L-100 120", "M-90 -40 L-70 0 L-96 30", "M150 30 L120 60 L140 100 L104 130", "M96 -30 L74 6 L100 40"))
    return f'''<g transform="translate({cx},{cy}) scale({s})"><g id="{idp}">
 <path d="M0 -230 V-110 M0 -110 Q-20 -100 -40 -80 M0 -110 Q20 -100 40 -80" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>
 <path d="M0 -230 V-110 M0 -110 Q-20 -100 -40 -80 M0 -110 Q20 -100 40 -80" fill="none" stroke="#e8c0c8" stroke-width="18" stroke-linecap="round"/>
 <path id="{idp}L" d="{L}" fill="#f29aa8" stroke="{INK}" stroke-width="8"/><path id="{idp}R" d="{R}" fill="#f29aa8" stroke="{INK}" stroke-width="8"/>
 <path d="M-60 -60 Q-110 0 -90 80 M60 -60 Q110 0 90 80" fill="none" stroke="#c46a7a" stroke-width="6" stroke-linecap="round"/>
 <g id="{idp}Hurt">{cr}</g>
</g></g>'''
