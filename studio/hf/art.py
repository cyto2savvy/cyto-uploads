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
