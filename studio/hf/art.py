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
