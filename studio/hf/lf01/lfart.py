"""LF01 art (1920x1080 backgrounds + panel figures). Same flat ink-outline style as art.py. Generic shapes only:
no logos, brands, store names or real people. Never draws smoking, products, lighters or smoke from a person."""
import math, random
import art as A

INK, CREAM, GOLD, CORAL, TEAL, BLUE, PINK, GREEN, SKY = "#0c1622", "#FAF4E8", "#FFD166", "#FF7A59", "#3fc1b0", "#4f86ff", "#f6a6c8", "#5AE68C", "#9fc3e8"
W, H = 1920, 1080


# ============================================================ backgrounds (Toronto, City of Toronto only)
def bg_night(idp="bn", seed=13):
    """Downtown skyline at night from the lake side (CN Tower right of centre, behind the panel, visible top)."""
    return (f'<defs><linearGradient id="{idp}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141c3e"/><stop offset=".6" stop-color="#3b3570"/>'
            f'<stop offset="1" stop-color="#b8687a"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#{idp}g)"/>'
            f'{A.stars(W, H, 60, seed, .5)}<g id="{idp}City">{A.skyline(W, H, 1000, 1.0, seed=seed, lit=.4, cn=622)}</g>'
            f'<rect y="1000" width="{W}" height="80" fill="#0e1a2e"/>')


def bg_downtown(idp="bd"):
    """Downtown at dusk (the 'Heart')."""
    return (f'<defs><linearGradient id="{idp}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9d6b"/><stop offset=".55" stop-color="#d9607a"/>'
            f'<stop offset="1" stop-color="#5a3f78"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#{idp}g)"/>'
            f'<circle cx="1500" cy="640" r="130" fill="#ffd9a0" opacity=".7"/>'
            f'<g id="{idp}City">{A.skyline(W, H, 1010, 1.15, seed=31, lit=.3, cn=622, ground="#2a2347")}</g>')


def bg_don_valley(idp="dv"):
    """Don Valley (the 'Lungs'): green ravine, river, the parkway with moving cars (class car), viaduct arch, skyline far off."""
    rnd = random.Random(7)
    trees = "".join(f'<g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})"><rect x="-6" y="0" width="12" height="40" fill="#5b3d2a"/>'
                    f'<circle cx="0" cy="-14" r="38" fill="{c}" stroke="{INK}" stroke-width="5"/></g>'
                    for x, y, s, c in [(rnd.uniform(0, W), rnd.uniform(560, 1000), rnd.uniform(.7, 1.3), rnd.choice(["#3f8f4a", "#2f7a3c", "#56a35a", "#d98a3a"])) for _ in range(34)])
    arch = "".join(f'<path d="M{620 + i * 160} 470 Q{700 + i * 160} 330 {780 + i * 160} 470" fill="none" stroke="#c9c2b0" stroke-width="16"/>' for i in range(6))
    cars = "".join(f'<g class="car"><rect x="{x}" y="{-20}" width="70" height="30" rx="10" fill="{c}" stroke="{INK}" stroke-width="4"/></g>'
                   for x, c in ((0, CORAL), (260, GOLD), (520, SKY), (900, "#e8e8e8"), (1250, CORAL), (1600, BLUE)))
    return (f'<defs><linearGradient id="{idp}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc7ef"/><stop offset="1" stop-color="#d6ecf7"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{idp}g)"/>'
            f'<g opacity=".55">{A.skyline(W, H, 470, .55, seed=5, lit=0, cn=1500, ground="#6c8fb0")}</g>'
            f'<rect x="600" y="440" width="1000" height="26" fill="#c9c2b0" stroke="{INK}" stroke-width="5"/>{arch}'
            f'<path d="M0 520 Q400 440 960 520 T1920 500 V1080 H0Z" fill="#4f9a55" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-40 760 C400 640 900 900 1960 700" fill="none" stroke="#5a6470" stroke-width="70"/>'
            f'<path d="M-40 760 C400 640 900 900 1960 700" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="30 30"/>'
            f'<g transform="translate(0,742)"><g id="{idp}Cars">{cars}</g></g>'
            f'<path d="M-40 900 C500 840 800 1010 1960 900" fill="none" stroke="#4d8fd0" stroke-width="44" stroke-linecap="round"/>{trees}')


def bg_uoft(idp="ut"):
    """U of T (the 'Brain'): generic Romanesque/gothic hall with a central tower, round front lawn, trees. No signage."""
    win = "".join(f'<path d="M{x} 620 v-50 a22 22 0 0 1 44 0 v50z" fill="#ffd27a" stroke="{INK}" stroke-width="4"/>' for x in range(330, 1600, 90) if not 860 < x < 1060)
    win2 = "".join(f'<path d="M{x} 760 v-50 a22 22 0 0 1 44 0 v50z" fill="#ffd27a" stroke="{INK}" stroke-width="4"/>' for x in range(330, 1600, 90) if not 860 < x < 1060)
    return (f'<defs><linearGradient id="{idp}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d3f7a"/><stop offset="1" stop-color="#e59a7e"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{idp}g)"/>{A.stars(W, H, 25, 9, .3)}'
            f'<rect x="280" y="520" width="1360" height="300" fill="#b5785a" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M260 525 L960 430 L1660 525Z" fill="#5b4a5e" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="870" y="250" width="180" height="570" fill="#a86a4e" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M850 255 L960 150 L1070 255Z" fill="#5b4a5e" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="960" cy="330" r="38" fill="#ffe7b0" stroke="{INK}" stroke-width="6"/><path d="M960 330 v-24 M960 330 h18" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M915 820 v-110 a45 45 0 0 1 90 0 v110z" fill="#3a2a2a" stroke="{INK}" stroke-width="6"/>{win}{win2}'
            f'<rect y="815" width="{W}" height="265" fill="#4f9a55"/><ellipse cx="960" cy="985" rx="700" ry="90" fill="#62b066" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M0 840 H{W}" stroke="#b9ae98" stroke-width="18"/>'
            + "".join(f'<g transform="translate({x},{y})"><rect x="-7" y="-10" width="14" height="70" fill="#5b3d2a"/><circle r="70" cy="-50" fill="#2f7a3c" stroke="{INK}" stroke-width="6"/></g>' for x, y in ((120, 800), (1800, 800), (220, 870), (1700, 880))))


def bg_kensington(idp="kn"):
    """Kensington-style row of colourful Victorian houses, awnings (no store names), string lights, a bike."""
    cols = ["#e8577b", "#4fb3d9", GOLD, "#7bd06e", "#b07be0", CORAL, "#4fd1b8", "#f29a3a"]
    hs = []
    for i in range(8):
        x = -30 + i * 250; c = cols[i % 8]
        hs.append(f'<g><rect x="{x}" y="420" width="250" height="560" fill="{c}" stroke="{INK}" stroke-width="7"/>'
                  f'<path d="M{x - 10} 425 L{x + 125} 290 L{x + 260} 425Z" fill="{c}" stroke="{INK}" stroke-width="7"/>'
                  f'<circle cx="{x + 125}" cy="380" r="30" fill="#ffe7a3" stroke="{INK}" stroke-width="5"/>'
                  f'<rect x="{x + 30}" y="490" width="70" height="100" fill="#ffe7a3" stroke="{INK}" stroke-width="5"/><rect x="{x + 150}" y="490" width="70" height="100" fill="#ffe7a3" stroke="{INK}" stroke-width="5"/>'
                  f'<path d="M{x + 10} 680 h230 l-20 60 h-190z" fill="{["#ffffff", INK][i % 2]}" opacity=".9" stroke="{INK}" stroke-width="5"/>'
                  + "".join(f'<path d="M{x + 18 + k * 46} 680 l0 60" stroke="{c}" stroke-width="18" opacity=".8"/>' for k in range(5))
                  + f'<rect x="{x + 40}" y="760" width="170" height="220" fill="#2a2a3a" stroke="{INK}" stroke-width="6"/></g>')
    bulbs = "".join(f'<circle class="bulb" cx="{x}" cy="{250 + 40 * math.sin(x / 320 * math.pi):.0f}" r="10" fill="{GOLD}"/>' for x in range(20, W, 64))
    return (f'<rect width="{W}" height="{H}" fill="#7fb8e6"/><circle cx="1700" cy="160" r="70" fill="#fff2b0"/>{"".join(hs)}'
            f'<path d="M0 230 Q480 310 960 230 T1920 230" fill="none" stroke="{INK}" stroke-width="4"/>{bulbs}'
            f'<rect y="980" width="{W}" height="100" fill="#8a8f98"/>')


def bg_bluffs(idp="bl"):
    """Scarborough Bluffs: pale cliffs dropping to the lake, beach, sky."""
    return (f'<defs><linearGradient id="{idp}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb3e8"/><stop offset="1" stop-color="#cfe9f7"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{idp}g)"/><circle cx="1650" cy="190" r="80" fill="#fff4c2"/>'
            f'<g id="{idp}Cloud"><ellipse cx="500" cy="180" rx="140" ry="44" fill="#fff"/><ellipse cx="580" cy="160" rx="90" ry="50" fill="#fff"/><ellipse cx="1200" cy="240" rx="120" ry="36" fill="#fff"/></g>'
            f'<rect y="640" width="{W}" height="440" fill="#2e6fb5"/><path d="M0 700 H{W}" stroke="#bfe0ff" stroke-width="5" opacity=".6"/>'
            f'<path d="M0 260 L260 250 L420 330 L600 300 L820 420 L1000 390 L1180 560 L1260 650 L0 700Z" fill="#eadfc4" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M0 260 L260 250 L420 330 L600 300 L820 420" fill="none" stroke="#3f8f4a" stroke-width="22"/>'
            f'<path d="M120 300 l30 200 M300 290 l20 220 M500 340 l24 200 M700 380 l20 170 M930 440 l20 140" stroke="#cdbd96" stroke-width="7"/>'
            f'<path d="M0 700 L1260 650 L1500 700 L0 760Z" fill="#e9d6a6" stroke="{INK}" stroke-width="5"/>'
            f'<g id="{idp}Waves">' + "".join(f'<path d="M{x} 820 q30 -18 60 0 t60 0" fill="none" stroke="#bfe0ff" stroke-width="6"/>' for x in range(1300, 1900, 180)) + '</g>')


def bg_queen(idp="qn"):
    """Queen St with a generic red/white 501 streetcar silhouette (no logo) and overhead wires."""
    shops = "".join(f'<rect x="{x}" y="{y}" width="230" height="{1000 - y}" fill="{c}" stroke="{INK}" stroke-width="6"/>'
                    f'<rect x="{x + 30}" y="{y + 40}" width="70" height="80" fill="#ffe7a3" stroke="{INK}" stroke-width="4"/><rect x="{x + 130}" y="{y + 40}" width="70" height="80" fill="#ffe7a3" stroke="{INK}" stroke-width="4"/>'
                    for x, y, c in zip(range(-20, W, 240), (360, 300, 380, 330, 290, 370, 320, 350, 300), ("#b5785a", "#8a5a7a", "#5a7a8a", "#a8875a", "#7a5a5a", "#5a8a6a", "#9a6a4a", "#6a6a9a", "#b5785a")))
    return (f'<rect width="{W}" height="{H}" fill="#9fd0f2"/>{shops}<rect y="900" width="{W}" height="180" fill="#5a6470"/>'
            f'<path d="M0 990 H{W} M0 1030 H{W}" stroke="#c9ccd2" stroke-width="6"/><path d="M0 230 H{W}" stroke="{INK}" stroke-width="4"/>'
            f'<g id="{idp}Tram">{A.streetcar(900, 650, 1.05, sign="")}</g>')


# ============================================================ figures (panel-local coords, panel 1200x790)
def clock(cx, cy, r, idp, label="20:00"):
    ticks = "".join(f'<path d="M{cx + math.cos(a) * (r - 18):.0f} {cy + math.sin(a) * (r - 18):.0f} L{cx + math.cos(a) * (r - 44):.0f} {cy + math.sin(a) * (r - 44):.0f}" stroke="{INK}" stroke-width="{10 if i % 3 == 0 else 5}" stroke-linecap="round"/>'
                    for i, a in enumerate(math.radians(k * 30 - 90) for k in range(12)))
    return (f'<g id="{idp}"><rect x="{cx - 34}" y="{cy - r - 62}" width="68" height="40" rx="10" fill="{CORAL}" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{cx - 12}" y="{cy - r - 26}" width="24" height="30" fill="#c9ccd2" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 14}" fill="{CORAL}" stroke="{INK}" stroke-width="9"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
            f'<path id="{idp}Arc" d="M{cx} {cy - r + 10} A{r - 10} {r - 10} 0 1 1 {cx - 0.1} {cy - r + 10}" fill="none" stroke="{GREEN}" stroke-width="22" opacity=".85" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0"/>'
            f'{ticks}<g id="{idp}Hand"><path d="M{cx} {cy} L{cx} {cy - r + 50}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="16" fill="{INK}"/>'
            f'<text id="{idp}T" x="{cx}" y="{cy + r * .52:.0f}" text-anchor="middle" font-family="InterBlack" font-size="{int(r * .36)}" fill="{INK}">{label}</text></g>')


def heart(cx, cy, s, idp, fill="#e8455a"):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><g id="{idp}"><path d="M0 70 C-90 10 -110 -60 -55 -80 C-25 -90 -5 -70 0 -50 C5 -70 25 -90 55 -80 C110 -60 90 10 0 70Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/><ellipse cx="-45" cy="-45" rx="18" ry="11" fill="#ffb3bd" transform="rotate(-30 -45 -45)"/></g></g>')


def leaf_icon(cx, cy, s, idp):
    """FLAT abstract leaf icon (explainer card only)."""
    return (f'<g transform="translate({cx},{cy}) scale({s})"><g id="{idp}"><path d="M0 -110 C80 -70 90 40 0 110 C-90 40 -80 -70 0 -110Z" fill="#c69a3e" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M0 -95 V105 M0 -40 L40 -70 M0 0 L48 -26 M0 40 L40 20 M0 -40 L-40 -70 M0 0 L-48 -26 M0 40 L-40 20" stroke="#7a5a1e" stroke-width="6" fill="none" stroke-linecap="round"/></g></g>')


def person(x, y, s, fill, cls="pp"):
    return (f'<g transform="translate({x},{y}) scale({s})"><g class="{cls}"><circle cx="0" cy="-70" r="34" fill="{fill}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M-55 60 Q-55 -25 0 -25 Q55 -25 55 60Z" fill="{fill}" stroke="{INK}" stroke-width="7"/></g></g>')


def ecg_path(x0, y0, w, beats, amp):
    pts = [f"M{x0} {y0}"]; step = w / beats
    for i in range(beats):
        bx = x0 + i * step
        pts.append(f"L{bx + step * .35:.0f} {y0} L{bx + step * .42:.0f} {y0 - amp * .25:.0f} L{bx + step * .48:.0f} {y0 + amp * .2:.0f} "
                   f"L{bx + step * .54:.0f} {y0 - amp:.0f} L{bx + step * .6:.0f} {y0 + amp * .35:.0f} L{bx + step * .66:.0f} {y0} L{bx + step:.0f} {y0}")
    return " ".join(pts)


def gauge(cx, cy, r, idp):
    """semicircle gauge: red (high CO) -> green (normal)."""
    def arc(a0, a1, col):
        p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        return f'<path d="M{p0[0]:.0f} {p0[1]:.0f} A{r} {r} 0 0 1 {p1[0]:.0f} {p1[1]:.0f}" fill="none" stroke="{col}" stroke-width="46"/>'
    return (f'<g id="{idp}"><path d="M{cx - r - 40} {cy + 20} A{r + 40} {r + 40} 0 0 1 {cx + r + 40} {cy + 20}Z" fill="#0c1622" stroke="#2c4d6e" stroke-width="5"/>'
            f'{arc(180, 240, GREEN)}{arc(240, 300, GOLD)}{arc(300, 360, CORAL)}'
            f'<g id="{idp}N"><path d="M{cx} {cy} L{cx + r - 30} {cy}" stroke="{CREAM}" stroke-width="14" stroke-linecap="round"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="22" fill="{CREAM}" stroke="{INK}" stroke-width="6"/></g>')


def brain(cx, cy, s, idp):
    """flat brain side view with receptor sites (class rc, a Y-shape each) on the surface."""
    rnd = random.Random(3)
    folds = ("M-170 -20 Q-120 -60 -80 -20 Q-40 20 0 -30 Q40 -80 90 -30 Q130 10 170 -20 M-150 50 Q-90 20 -40 60 Q20 100 70 50 Q120 10 160 60 "
             "M-60 -120 Q-30 -80 10 -110 Q50 -140 80 -100")
    rec = ""
    for i, a in enumerate(range(200, 345, 18)):
        x = 215 * math.cos(math.radians(a)); y = 150 * math.sin(math.radians(a)) - 10
        ang = a + 90
        rec += (f'<g class="rc" transform="translate({x:.0f},{y:.0f}) rotate({ang})"><path d="M0 0 V-34 M0 -34 L-14 -52 M0 -34 L14 -52" stroke="#6b6f7a" stroke-width="9" stroke-linecap="round" fill="none"/></g>')
    return (f'<g transform="translate({cx},{cy}) scale({s})"><g id="{idp}">'
            f'<path d="M-230 20 C-250 -120 -120 -190 0 -175 C130 -195 250 -120 230 10 C240 100 150 150 60 140 C40 190 -20 200 -30 150 C-150 160 -235 110 -230 20Z" fill="#f4a9bd" stroke="{INK}" stroke-width="9"/>'
            f'<path d="{folds}" fill="none" stroke="#c4708a" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M20 145 C30 190 60 220 60 250" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M20 145 C30 190 60 220 60 250" stroke="#e58aa3" stroke-width="16" stroke-linecap="round"/>'
            f'<g id="{idp}Rec">{rec}</g></g></g>')


def calendar(x, y, w, h, idp, pages=("WEEK 1", "WEEK 2", "WEEK 3")):
    """calendar block; front pages (class pg, ids {idp}P0..) flip up (rotateX) to reveal WEEK 4 under them."""
    def page(lbl, col, pid, cls):
        return (f'<div id="{pid}" class="{cls}" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;transform-origin:50% 0;background:{CREAM};border:8px solid {INK};border-radius:24px;overflow:hidden">'
                f'<div style="height:{h * .3:.0f}px;background:{col};border-bottom:8px solid {INK}"></div>'
                f'<div style="position:absolute;left:0;width:100%;top:{h * .38:.0f}px;text-align:center;font:{int(h * .26)}px InterBlack;color:{INK}">{lbl}</div></div>')
    pg = page("WEEK 4", GREEN, f"{idp}P4", "pg4")
    for i, lbl in reversed(list(enumerate(pages))):
        pg += page(lbl, CORAL, f"{idp}P{i}", "pg")
    rings = "".join(f'<div style="position:absolute;top:-28px;left:{w * f - 14:.0f}px;width:28px;height:56px;border-radius:14px;background:#c9ccd2;border:6px solid {INK};z-index:5"></div>' for f in (.25, .75))
    return f'<div id="{idp}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;perspective:1400px">{pg}{rings}</div>'


def cilia(x0, y0, w, idp, n=16):
    """epithelium strip with cilia (class cl, rotate about base) + mucus blobs (class mu) riding on top."""
    cells = "".join(f'<rect x="{x0 + i * w / 8:.0f}" y="{y0}" width="{w / 8:.0f}" height="120" fill="#f29aa8" stroke="{INK}" stroke-width="6"/>'
                    f'<circle cx="{x0 + i * w / 8 + w / 16:.0f}" cy="{y0 + 66}" r="20" fill="#b06ad0" stroke="{INK}" stroke-width="4"/>' for i in range(8))
    hairs = "".join(f'<g class="cl" data-x="{x0 + 20 + i * (w - 40) / (n - 1):.0f}"><path d="M{x0 + 20 + i * (w - 40) / (n - 1):.0f} {y0} q-10 -50 4 -100" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
                    f'<path d="M{x0 + 20 + i * (w - 40) / (n - 1):.0f} {y0} q-10 -50 4 -100" fill="none" stroke="#ffd0d8" stroke-width="6" stroke-linecap="round"/></g>' for i in range(n))
    mucus = "".join(f'<g class="mu"><ellipse cx="{x0 + 80 + k * 260}" cy="{y0 - 120}" rx="70" ry="30" fill="#c9e07a" stroke="{INK}" stroke-width="5" opacity=".95"/>'
                    + "".join(f'<circle cx="{x0 + 60 + k * 260 + d * 22}" cy="{y0 - 124 + (d % 2) * 10}" r="6" fill="#6b6f4a"/>' for d in range(3)) + '</g>' for k in range(4))
    return f'<g id="{idp}">{cells}{hairs}{mucus}</g>'


def phone_chat(x, y, idp):
    """generic phone, chat UI (no real app)."""
    return (f'<div id="{idp}" style="position:absolute;left:{x}px;top:{y}px;width:360px;height:600px;border-radius:50px;background:#1b2733;border:10px solid {INK};box-shadow:0 14px 30px rgba(0,0,0,.4)">'
            f'<div style="position:absolute;left:24px;right:24px;top:30px;bottom:30px;border-radius:30px;background:#eef3f8;overflow:hidden">'
            f'<div style="height:70px;background:{TEAL};border-bottom:5px solid {INK};font:34px InterBlack;color:{INK};text-align:center;line-height:66px">SQUAD</div>'
            f'<div id="{idp}B1" class="bub" style="top:100px;left:16px;background:#ffffff">day 3 💪</div>'
            f'<div id="{idp}B2" class="bub" style="top:200px;right:16px;background:{GREEN}">proud of u</div>'
            f'<div id="{idp}B3" class="bub" style="top:300px;left:16px;background:#ffffff">walk later?</div>'
            f'<div id="{idp}B4" class="bub" style="top:400px;right:16px;background:{GREEN}">bet 🙌</div></div></div>')


PHONE_CSS = f""".bub {{ position:absolute; padding:12px 20px; border-radius:24px; border:4px solid {INK}; font:34px InterBlack; color:{INK}; white-space:nowrap; }}"""


def pharm_cross(cx, cy, s, idp, fill=GREEN):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><g id="{idp}"><path d="M-35 -100 H35 V-35 H100 V35 H35 V100 H-35 V35 H-100 V-35 H-35Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/></g></g>')


def icon(kind, cx, cy, s=1.0, idp=None):
    """tip-card icons, ~200px box at s=1."""
    g = f'<g transform="translate({cx},{cy}) scale({s})"' + (f' id="{idp}"' if idp else "") + '>'
    if kind == "squad":
        g += person(-60, 30, .8, SKY, "ic") + person(60, 30, .8, PINK, "ic") + person(0, 50, 1.0, GOLD, "ic")
    elif kind == "pharm":
        g += pharm_cross(0, 0, .9, (idp or "ic") + "x")
    elif kind == "pin":
        g += f'<path d="M0 95 C-30 40 -75 10 -75 -30 A75 75 0 0 1 75 -30 C75 10 30 40 0 95Z" fill="{CORAL}" stroke="{INK}" stroke-width="9"/><circle cy="-32" r="28" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
    elif kind == "shoe":
        g += (f'<path d="M-95 40 L-90 -30 Q-60 -40 -40 -10 L10 0 Q80 10 95 40 L95 60 H-95Z" fill="{BLUE}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
              f'<path d="M-95 50 H95" stroke="{CREAM}" stroke-width="14"/><path d="M-30 -10 l10 20 M-10 -6 l10 20 M10 -2 l10 20" stroke="{CREAM}" stroke-width="6"/>')
    elif kind == "reset":
        g += (f'<path d="M60 -50 A78 78 0 1 0 78 10" fill="none" stroke="{GREEN}" stroke-width="22" stroke-linecap="round"/>'
              f'<path d="M30 -90 L80 -60 L40 -20Z" fill="{GREEN}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
              f'<path d="M60 -50 A78 78 0 1 0 78 10" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".5"/>')
    elif kind == "water":
        g += f'<path d="M-50 -80 H50 L38 90 H-38Z" fill="#bfe6ff" stroke="{INK}" stroke-width="9"/><path d="M-44 -10 H44 L36 86 H-36Z" fill="{BLUE}" opacity=".8"/>'
    elif kind == "zzz":
        g += f'<path d="M30 -80 A80 80 0 1 0 80 30 A62 62 0 1 1 30 -80Z" fill="{GOLD}" stroke="{INK}" stroke-width="8"/>'
    elif kind == "angry":
        g += (f'<circle r="80" fill="{CORAL}" stroke="{INK}" stroke-width="9"/><path d="M-50 -30 L-15 -15 M50 -30 L15 -15" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
              f'<circle cx="-30" cy="5" r="9" fill="{INK}"/><circle cx="30" cy="5" r="9" fill="{INK}"/><path d="M-30 45 Q0 25 30 45" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    elif kind == "jitter":
        g += (f'<circle r="80" fill="{GOLD}" stroke="{INK}" stroke-width="9"/><circle cx="-28" cy="-10" r="16" fill="{CREAM}" stroke="{INK}" stroke-width="6"/><circle cx="28" cy="-10" r="16" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>'
              f'<path d="M-35 40 l12 -10 l12 10 l12 -10 l12 10 l12 -10" fill="none" stroke="{INK}" stroke-width="7"/>'
              f'<path d="M-110 -40 l-20 -10 M-110 0 h-24 M110 -40 l20 -10 M110 0 h24" stroke="{CREAM}" stroke-width="8" stroke-linecap="round"/>')
    elif kind == "gum":
        g += f'<rect x="-80" y="-40" width="160" height="80" rx="20" fill="{CREAM}" stroke="{INK}" stroke-width="9"/><path d="M-30 -40 V40 M30 -40 V40" stroke="{SKY}" stroke-width="10"/>'
    elif kind == "patch":
        g += f'<rect x="-80" y="-80" width="160" height="160" rx="34" fill="#e8c9a8" stroke="{INK}" stroke-width="9"/><rect x="-40" y="-40" width="80" height="80" rx="12" fill="#d4a882" stroke="{INK}" stroke-width="5"/>'
    elif kind == "rx":
        g += (f'<rect x="-70" y="-90" width="140" height="180" rx="16" fill="{CREAM}" stroke="{INK}" stroke-width="9"/>'
              f'<text x="0" y="10" text-anchor="middle" font-family="InterBlack" font-size="80" fill="{BLUE}">Rx</text><path d="M-40 50 H40" stroke="{INK}" stroke-width="7"/>')
    g += '</g>'
    return g


def toronto_map(idp="tm"):
    """stylised City of Toronto map (panel 1200x790): lake, Don River, Humber, downtown core, U of T, Bluffs."""
    return (f'<g id="{idp}"><rect width="1200" height="790" fill="#e9e2cf"/>'
            f'<path d="M0 560 Q200 600 380 590 Q560 640 700 610 Q900 560 1200 440 V790 H0Z" fill="#5aa0d8" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M40 640 Q120 600 210 620" fill="none" stroke="#2e6fb5" stroke-width="4"/>'
            f'<path d="M600 610 Q640 470 610 350 Q590 240 650 120 Q680 60 660 0" fill="none" stroke="#4d8fd0" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="M130 600 Q160 420 120 250 Q100 120 150 0" fill="none" stroke="#4d8fd0" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="M0 300 H1200 M0 160 H1200 M300 0 V600 M860 0 V560" stroke="#cfc6ae" stroke-width="10"/>'
            f'<path d="M560 420 Q610 380 640 420" stroke="#cfc6ae" stroke-width="10" fill="none"/>'
            f'<path d="M560 330 Q620 260 690 330" fill="#7fbf74" opacity=".8"/>'
            + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#8aa2bf" stroke="{INK}" stroke-width="4"/>' for x, y, w, h in ((450, 500, 40, 90), (500, 470, 36, 120), (540, 510, 44, 80), (420, 540, 30, 50)))
            + f'<path d="M520 470 L524 380 L528 470Z" fill="#8aa2bf" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M940 430 L1010 400 L1100 360 L1200 330 V420 L1060 470 L960 500Z" fill="#eadfc4" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M640 600 Q700 560 760 590" fill="none" stroke="#2e6fb5" stroke-width="4"/>'
            f'<rect x="360" y="340" width="90" height="70" fill="#b5785a" stroke="{INK}" stroke-width="5"/><rect x="392" y="300" width="26" height="45" fill="#a86a4e" stroke="{INK}" stroke-width="4"/></g>')


def pin(x, y, idp, fill, label_icon=""):
    return (f'<g id="{idp}" transform="translate({x},{y})"><g id="{idp}I"><path d="M0 0 C-22 -40 -56 -62 -56 -96 A56 56 0 0 1 56 -96 C56 -62 22 -40 0 0Z" fill="{fill}" stroke="{INK}" stroke-width="7"/>'
            f'<circle cy="-98" r="34" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>{label_icon}</g></g>')
