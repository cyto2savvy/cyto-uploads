"""LF02 sets (1920x1080, flat-ink, multi-plane). Each set returns layer html; every layer is a full-frame div
with an id so scenes can parallax them (S.parallax). Toronto refs = generic shapes only (no logos/brands)."""
import math, random

INK = "#0c1622"
W, H = 1920, 1080


def layer(id_, svg, z=1, extra=""):
    return f'<div id="{id_}" class="fill" style="z-index:{z};{extra}"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;overflow:visible">{svg}</svg></div>'


def skyline(y0=640, col="#1a2440", win="#ffd98a", seed=4, cn=True, x0=-40, x1=1960):
    """Toronto-ish skyline: generic towers + CN-tower silhouette."""
    rnd = random.Random(seed); s = ""; x = x0
    while x < x1:
        w = rnd.randint(50, 120); h = rnd.randint(80, 300)
        s += f'<rect x="{x}" y="{y0 - h}" width="{w}" height="{h + 400}" fill="{col}"/>'
        for wy in range(y0 - h + 14, y0 - 10, 26):
            for wx in range(x + 10, x + w - 14, 22):
                if rnd.random() < .35: s += f'<rect x="{wx}" y="{wy}" width="9" height="12" fill="{win}" opacity=".8"/>'
        x += w + rnd.randint(4, 20)
    if cn:
        cx = (x0 + x1) // 2 + 180
        s += (f'<path d="M{cx - 9} {y0 + 10} L{cx - 5} {y0 - 330} L{cx + 5} {y0 - 330} L{cx + 9} {y0 + 10}Z" fill="{col}"/>'
              f'<ellipse cx="{cx}" cy="{y0 - 300}" rx="26" ry="14" fill="{col}"/><rect x="{cx - 2}" y="{y0 - 430}" width="4" height="110" fill="{col}"/>'
              f'<circle cx="{cx}" cy="{y0 - 432}" r="4" fill="#ff5050"/>')
    return s


def snow(id_, n=70, seed=2, x0=0, x1=W, y0=0, y1=H, r=(2, 5), col="#ffffff"):
    rnd = random.Random(seed)
    return f'<g id="{id_}">' + "".join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.uniform(*r):.1f}" fill="{col}" opacity="{rnd.uniform(.5, .95):.2f}"/>' for _ in range(n)) + '</g>'


# ------------------------------------------------------------------ HQ (brain = Queen's Park)
def hq(p="hq", window_x=270, door=True):
    wx, wy, ww, wh = window_x, 150, 470, 520
    sky = (f'<defs><linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1838"/><stop offset="1" stop-color="#3b3f78"/></linearGradient>'
           f'<clipPath id="{p}win"><path d="M{wx} {wy + wh} V{wy + ww / 2} A{ww / 2} {ww / 2} 0 0 1 {wx + ww} {wy + ww / 2} V{wy + wh}Z"/></clipPath>'
           f'<pattern id="{p}gyri" width="160" height="90" patternUnits="userSpaceOnUse"><path d="M0 45 q20 -30 40 0 t40 0 t40 0 t40 0" fill="none" stroke="#5b3f7d" stroke-width="5" opacity=".55"/></pattern></defs>')
    wall = (f'<rect width="{W}" height="{H}" fill="#47306b"/><rect width="{W}" height="{H}" fill="url(#{p}gyri)"/>'
            f'<rect y="0" width="{W}" height="60" fill="#33224f"/><rect y="770" width="{W}" height="22" fill="#2b1d44"/>'
            + "".join(f'<rect x="{x}" y="60" width="34" height="710" fill="#3d2960"/>' for x in (180, 820, 1420)))
    winp = (f'<g clip-path="url(#{p}win)"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#{p}sky)"/>'
            f'<circle cx="{wx + 360}" cy="{wy + 120}" r="34" fill="#f5f0d8"/>'
            f'<image id="{p}winph" href="assets/ph_skyline_bg.jpg" x="{wx - 120}" y="{wy - 20}" width="{ww + 240}" height="{wh + 40}" preserveAspectRatio="xMidYMid slice"/>'
            f'<g id="{p}rhinoSlot"></g>'
            f'{snow(p + "snow", 40, 3, wx, wx + ww, wy - 200, wy + wh)}</g>'
            f'<path d="M{wx} {wy + wh} V{wy + ww / 2} A{ww / 2} {ww / 2} 0 0 1 {wx + ww} {wy + ww / 2} V{wy + wh}Z" fill="none" stroke="#c7b28a" stroke-width="26"/>'
            f'<path d="M{wx + ww / 2} {wy} V{wy + wh} M{wx} {wy + ww / 2 + 30} H{wx + ww} M{wx} {wy + wh - 150} H{wx + ww}" stroke="#c7b28a" stroke-width="12"/>'
            f'<rect x="{wx - 30}" y="{wy + wh}" width="{ww + 60}" height="30" rx="6" fill="#a8916a" stroke="{INK}" stroke-width="5"/>')
    plaque = (f'<rect x="830" y="92" width="420" height="80" rx="14" fill="#c7a24e" stroke="{INK}" stroke-width="6"/>'
              f'<text class="settxt" x="1040" y="146" text-anchor="middle" font-family="InterBlack" font-size="38" fill="#2b1d44">QUEEN\'S PARK HQ</text>')
    lever = (f'<g id="{p}leverBox"><rect x="1180" y="330" width="150" height="250" rx="16" fill="#d9d4c7" stroke="{INK}" stroke-width="7"/>'
             f'<rect x="1196" y="346" width="118" height="40" rx="6" fill="#c0392b"/><text class="settxt" x="1255" y="376" text-anchor="middle" font-family="InterBlack" font-size="26" fill="#fff">ALARM</text>'
             f'<rect x="1245" y="400" width="20" height="150" rx="10" fill="#555"/>'
             f'<g id="{p}lever"><rect x="1245" y="400" width="20" height="90" rx="8" fill="#9aa3ab" stroke="{INK}" stroke-width="5"/><rect x="1215" y="380" width="80" height="40" rx="18" fill="#e63946" stroke="{INK}" stroke-width="6"/></g></g>')
    door_g = ""
    if door:
        door_g = (f'<rect x="1530" y="250" width="290" height="545" fill="#1e1430"/>'
                  f'<g id="{p}door"><rect x="1530" y="250" width="290" height="545" rx="6" fill="#7a4b2c" stroke="{INK}" stroke-width="8"/>'
                  f'<rect x="1565" y="290" width="220" height="200" rx="8" fill="none" stroke="#5c361d" stroke-width="10"/><rect x="1565" y="530" width="220" height="220" rx="8" fill="none" stroke="#5c361d" stroke-width="10"/>'
                  f'<circle cx="1790" cy="530" r="16" fill="#e8c35a" stroke="{INK}" stroke-width="5"/></g>'
                  f'<rect x="1520" y="240" width="310" height="20" fill="#5c361d" stroke="{INK}" stroke-width="5"/>')
    alarm = (f'<g id="{p}alarm"><rect x="1040" y="40" width="40" height="40" fill="#555"/>'
             f'<path d="M1010 110 Q1010 60 1060 60 Q1110 60 1110 110Z" fill="#7a1010" stroke="{INK}" stroke-width="6"/>'
             f'<path id="{p}alarmGlass" d="M1016 108 Q1016 66 1060 66 Q1104 66 1104 108Z" fill="#ff3b3b" opacity=".35"/><rect x="1000" y="106" width="120" height="16" rx="6" fill="#333" stroke="{INK}" stroke-width="5"/></g>')
    floor = (f'<rect y="792" width="{W}" height="300" fill="#6b4630"/>'
             + "".join(f'<path d="M0 {y} H{W}" stroke="#583824" stroke-width="5"/>' for y in (850, 920, 1000))
             + f'<ellipse cx="760" cy="900" rx="560" ry="110" fill="#2f6f8f" stroke="{INK}" stroke-width="6"/><ellipse cx="760" cy="900" rx="470" ry="80" fill="none" stroke="#f6f0e0" stroke-width="8" opacity=".6"/>')
    bean = (f'<path d="M290 880 Q250 700 420 690 Q560 640 690 720 Q790 790 740 890 Q520 950 290 880Z" fill="#e2394b" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M340 860 Q360 760 450 740" fill="none" stroke="#ff7a8a" stroke-width="14" stroke-linecap="round" opacity=".6"/>')
    table = (f'<rect x="900" y="770" width="200" height="22" rx="8" fill="#a06a3f" stroke="{INK}" stroke-width="6"/><rect x="980" y="790" width="40" height="90" fill="#7a4b2c" stroke="{INK}" stroke-width="5"/>'
             f'<g id="{p}lamp"><path d="M960 770 L975 690 L1025 690 L1040 770Z" fill="#ffd166" stroke="{INK}" stroke-width="5"/></g>')
    plant = (f'<rect x="1380" y="700" width="90" height="100" rx="10" fill="#c96b3b" stroke="{INK}" stroke-width="6"/>'
             + "".join(f'<path d="M1425 705 Q{1425 + dx} {640 - abs(dx) // 3} {1425 + dx * 1.4:.0f} {600 + abs(dx) // 2}" fill="none" stroke="#3a9a5a" stroke-width="16" stroke-linecap="round"/>' for dx in (-60, -25, 10, 45)))
    fg = (f'<path d="M-40 1100 L-40 900 Q60 860 180 900 L230 1100Z" fill="#2c1f45" stroke="{INK}" stroke-width="8"/>'
          f'<path d="M1720 1100 Q1760 960 1880 950 Q1960 950 1980 1100Z" fill="#2c1f45" stroke="{INK}" stroke-width="8"/>')
    return [layer(f"{p}L0", sky + wall + winp + plaque + lever + door_g + alarm, 1),
            layer(f"{p}L1", floor + plant + table, 2),
            layer(f"{p}L2", bean, 3),
            layer(f"{p}L3", fg, 40)]


def alarm_fx(p="hq"):
    """Red alarm wash + rotating beams (toggle #{p}red opacity)."""
    return (f'<div id="{p}red" class="fill" style="z-index:30;opacity:0;pointer-events:none;background:radial-gradient(ellipse at 1060px 90px, rgba(255,40,40,.55), rgba(160,0,20,.35) 55%, rgba(80,0,10,.25))"></div>'
            f'<div id="{p}beamW" class="fill" style="z-index:31;opacity:0;overflow:hidden"><svg width="{W}" height="{H}"><g id="{p}beam">'
            f'<path d="M1060 95 L-200 -100 L-200 380Z" fill="#ff6060" opacity=".28"/><path d="M1060 95 L2300 300 L2300 900Z" fill="#ff6060" opacity=".28"/></g></svg></div>')


# ------------------------------------------------------------------ COURT (streetball inside the body)
def court(p="ct"):
    sky = (f'<defs><linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a1430"/><stop offset=".7" stop-color="#c04b5a"/><stop offset="1" stop-color="#f29a7a"/></linearGradient></defs>'
           f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>'
           + "".join(f'<path d="M{x} 700 Q{x + 60} {300 + (i % 3) * 60} {x + 200} {200 + (i % 2) * 90} T{x + 420} 60" fill="none" stroke="#8e1f3a" stroke-width="{26 - (i % 3) * 6}" stroke-linecap="round" opacity=".7"/>' for i, x in enumerate(range(-100, 1900, 260)))
           + f'<g opacity=".55">{skyline(560, "#6d1a36", "#ffb3a1", seed=9)}</g>')
    rnd = random.Random(5)
    fans = "".join(f'<circle class="{p}fan" cx="{x + rnd.randint(-8, 8)}" cy="{y}" r="{rnd.randint(16, 22)}" fill="{rnd.choice(["#3fc1b0", "#7a5cc7", "#ffd166", "#f2c6da", "#ff9f5a", "#8ce2d6"])}" stroke="{INK}" stroke-width="4"/>'
                   for y in (470, 520, 570) for x in range(40, 1900, 52))
    stands = (f'<rect x="0" y="440" width="{W}" height="170" fill="#3a1a2e"/>'
              + "".join(f'<rect x="0" y="{y}" width="{W}" height="10" fill="#2a1022"/>' for y in (495, 545, 595)) + f'<g id="{p}fans">{fans}</g>')
    fence = (f'<defs><pattern id="{p}chain" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="34" height="34" fill="none" stroke="#c9ccd2" stroke-width="3" opacity=".55"/></pattern></defs>'
             f'<rect x="0" y="380" width="{W}" height="250" fill="url(#{p}chain)"/>' + "".join(f'<rect x="{x}" y="370" width="12" height="270" fill="#9aa0a8" stroke="{INK}" stroke-width="3"/>' for x in range(0, 1960, 320)))
    floor = (f'<path d="M-200 1080 L260 610 L1660 610 L2120 1080Z" fill="#2f6f8f" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-60 1080 L330 650 L1590 650 L1980 1080" fill="none" stroke="#f6f0e0" stroke-width="8"/>'
             f'<path d="M960 650 L960 1080" stroke="#f6f0e0" stroke-width="8"/><ellipse cx="960" cy="830" rx="190" ry="70" fill="none" stroke="#f6f0e0" stroke-width="8"/>'
             f'<path d="M1180 650 Q1060 780 1500 900" fill="none" stroke="#ff7a59" stroke-width="10" opacity=".8"/>')
    hoop = (f'<g id="{p}hoop"><rect x="1700" y="300" width="22" height="420" fill="#555" stroke="{INK}" stroke-width="5"/>'
            f'<g id="{p}board"><rect x="1560" y="250" width="220" height="150" rx="6" fill="#dff3ff" fill-opacity=".55" stroke="#fff" stroke-width="8"/><rect x="1625" y="300" width="90" height="70" fill="none" stroke="#e63946" stroke-width="6"/></g>'
            f'<g id="{p}shards" opacity="0">' + "".join(f'<path class="{p}shard" d="M{1600 + (i % 5) * 36} {270 + (i // 5) * 40} l{18 + i % 3 * 6} {8} l-{10} {22}Z" fill="#dff3ff" stroke="#fff" stroke-width="3"/>' for i in range(15)) + '</g>'
            f'<ellipse cx="1640" cy="400" rx="58" ry="12" fill="none" stroke="#ff6a00" stroke-width="9"/>'
            f'<path d="M1585 405 L1605 470 L1675 470 L1695 405 M1610 410 L1630 468 M1670 410 L1650 468" fill="none" stroke="#fff" stroke-width="4"/></g>')
    return [layer(f"{p}L0", sky, 1), layer(f"{p}L1", stands + fence, 2), layer(f"{p}L2", floor + hoop, 3)]


def scoreboard(p="sb"):
    """Top-centre scoreboard: two meters (heart rate, breathing) — bars only, no invented numbers."""
    return (f'<div id="{p}" style="position:absolute;left:560px;top:40px;width:800px;height:200px;z-index:25;border-radius:22px;background:#151a24;border:6px solid {INK};box-shadow:0 10px 0 rgba(0,0,0,.35)">'
            f'<div style="position:absolute;left:0;right:0;top:12px;text-align:center;font:34px InterBlack;color:#FFD166;letter-spacing:.06em">MITO vs THE ALARM</div>'
            f'<div style="position:absolute;left:40px;top:76px;font:26px InterBlack;color:#ff8a8a">HEART RATE</div>'
            f'<div style="position:absolute;left:40px;top:116px;width:330px;height:40px;border-radius:12px;background:#2a3140;overflow:hidden"><div id="{p}hr" style="width:100%;height:100%;background:linear-gradient(90deg,#ffb4a2,#e63946);transform-origin:0 50%;transform:scaleX(.3)"></div></div>'
            f'<svg id="{p}heart" style="position:absolute;left:300px;top:66px;overflow:visible" width="44" height="40"><path d="M22 38 L4 18 A10 10 0 0 1 22 8 A10 10 0 0 1 40 18Z" fill="#e63946" stroke="#fff" stroke-width="3"/></svg>'
            f'<div style="position:absolute;left:430px;top:76px;font:26px InterBlack;color:#8ce2d6">BREATHING</div>'
            f'<div style="position:absolute;left:430px;top:116px;width:330px;height:40px;border-radius:12px;background:#2a3140;overflow:hidden"><div id="{p}br" style="width:100%;height:100%;background:linear-gradient(90deg,#c2fff5,#3fc1b0);transform-origin:0 50%;transform:scaleX(.3)"></div></div>'
            f'</div>')


def desk(p="dk"):
    return layer(f"{p}", f'<path d="M40 860 L660 860 L700 1100 L0 1100Z" fill="#20283a" stroke="{INK}" stroke-width="8"/>'
                         f'<rect x="20" y="840" width="700" height="34" rx="8" fill="#39445c" stroke="{INK}" stroke-width="6"/>'
                         f'<rect x="170" y="878" width="400" height="44" rx="10" fill="#e63946" stroke="{INK}" stroke-width="5"/>'
                         f'<text class="settxt" x="370" y="911" text-anchor="middle" font-family="InterBlack" font-size="28" fill="#fff">PLAY-BY-PLAY</text>'
                         f'<rect x="540" y="770" width="16" height="74" fill="#333"/><ellipse cx="548" cy="768" rx="22" ry="30" fill="#222" stroke="{INK}" stroke-width="5"/>', 30)


HEADSET = ('<path d="M372 300 Q600 130 828 300" fill="none" stroke="#222" stroke-width="26" stroke-linecap="round"/>'
           '<rect x="344" y="300" width="56" height="96" rx="22" fill="#e63946" stroke="#0c1622" stroke-width="7"/>'
           '<rect x="800" y="300" width="56" height="96" rx="22" fill="#e63946" stroke="#0c1622" stroke-width="7"/>')
HEADSET_MIC = '<path d="M372 380 Q380 520 520 560" fill="none" stroke="#222" stroke-width="10" stroke-linecap="round"/><circle cx="526" cy="562" r="16" fill="#333" stroke="#0c1622" stroke-width="4"/>'


def alarm_guy(idp="al", pose="idle"):
    """THE ALARM: big red siren-headed baller (no voice, siren SFX only)."""
    limb = lambda d: f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#b81d2b" stroke-width="48" stroke-linecap="round"/>'
    poses = {"idle": limb("M120 330 Q70 420 90 500") + limb("M380 330 Q430 420 410 500"),
             "defend": limb("M120 330 Q20 300 -20 220") + limb("M380 330 Q480 300 520 220"),
             "flex": limb("M120 330 Q60 260 110 190") + limb("M380 330 Q440 260 390 190")}
    pg = "".join(f'<g id="{idp}P_{k}" opacity="{1 if k == pose else 0}">{v}</g>' for k, v in poses.items())
    return f"""<svg viewBox="0 0 500 720" width="500" height="720" style="position:absolute;left:0;top:0;overflow:visible"><g id="{idp}">
<ellipse cx="250" cy="702" rx="150" ry="18" fill="#000" opacity=".3"/>
<rect x="160" y="560" width="60" height="120" rx="20" fill="#7a0f18" stroke="{INK}" stroke-width="7"/><rect x="280" y="560" width="60" height="120" rx="20" fill="#7a0f18" stroke="{INK}" stroke-width="7"/>
<path d="M140 690 h100 v-28 h-90Z M260 690 h100 v-28 h-90Z" fill="#111" stroke="{INK}" stroke-width="5"/>
<g id="{idp}Body"><rect x="100" y="270" width="300" height="320" rx="70" fill="#e63946" stroke="{INK}" stroke-width="9"/>
<rect x="100" y="420" width="300" height="20" fill="#111"/><text x="250" y="400" text-anchor="middle" font-family="InterBlack" font-size="64" fill="#fff" stroke="{INK}" stroke-width="4" paint-order="stroke">ALARM</text>
<rect x="190" y="230" width="120" height="50" rx="10" fill="#333" stroke="{INK}" stroke-width="7"/>
<path d="M150 236 Q150 60 250 60 Q350 60 350 236Z" fill="#ff3b3b" stroke="{INK}" stroke-width="9"/>
<path id="{idp}glow" d="M170 230 Q170 84 250 84 Q330 84 330 230Z" fill="#ffd1d1" opacity=".4"/>
<g id="{idp}eyes"><ellipse cx="215" cy="160" rx="22" ry="26" fill="#fff" stroke="{INK}" stroke-width="5"/><ellipse cx="285" cy="160" rx="22" ry="26" fill="#fff" stroke="{INK}" stroke-width="5"/>
<circle cx="219" cy="166" r="11" fill="{INK}"/><circle cx="281" cy="166" r="11" fill="{INK}"/><path d="M190 128 L238 142 M310 128 L262 142" stroke="{INK}" stroke-width="10" stroke-linecap="round"/></g>
{pg}</g></g></svg>"""


# ------------------------------------------------------------------ NOIR office
def noir(p="nr"):
    blinds = "".join(f'<rect x="1120" y="{y}" width="640" height="10" fill="#cfcfcf" opacity=".55"/>' for y in range(170, 700, 56))
    rain = "".join(f'<path class="{p}drop" d="M{1130 + (i * 53) % 620} {160 + (i * 97) % 520} l-6 34" stroke="#e8e8e8" stroke-width="3" opacity=".7"/>' for i in range(60))
    room = (f'<rect width="{W}" height="{H}" fill="#2a2a2a"/>'
            f'<rect x="1100" y="150" width="680" height="570" fill="#101010" stroke="#000" stroke-width="10"/>'
            f'<image href="assets/ph_distillery_noir.jpg" x="1100" y="150" width="680" height="570" preserveAspectRatio="xMidYMid slice" opacity=".8"/>'
            f'<rect x="1100" y="150" width="680" height="570" fill="#000" opacity=".25"/><g id="{p}rain">{rain}</g>{blinds}'
            f'<path d="M1100 150 L1780 150 L1780 720 L1100 720Z" fill="none" stroke="#000" stroke-width="14"/>'
            f'<path d="M0 0 L760 0 L560 1080 L0 1080Z" fill="#000" opacity=".25"/>'
            f'<rect x="80" y="160" width="520" height="380" rx="8" fill="#6e6e6e" stroke="#000" stroke-width="8"/>'
            f'<text class="settxt" x="340" y="220" text-anchor="middle" font-family="InterBlack" font-size="40" fill="#1a1a1a">COLD CASES</text>'
            + "".join(f'<rect x="{110 + i * 165}" y="250" width="140" height="170" fill="#d8d8d8" stroke="#000" stroke-width="5" transform="rotate({(-1) ** i * 4} {180 + i * 165} 335)"/>' for i in range(3)))
    desk = (f'<rect x="0" y="760" width="{W}" height="330" fill="#3b3b3b"/><rect x="0" y="740" width="{W}" height="36" fill="#555" stroke="#000" stroke-width="6"/>'
            f'<g id="{p}lamp"><path d="M1460 740 L1500 610 L1580 610 L1620 740Z" fill="#8a8a8a" stroke="#000" stroke-width="6"/><path d="M1500 740 L1300 1080 L1820 1080 L1600 740Z" fill="#fff" opacity=".08"/></g>'
            f'<g id="{p}file"><rect x="760" y="700" width="380" height="60" rx="6" fill="#a8a8a8" stroke="#000" stroke-width="6"/>'
            f'<text class="settxt" x="950" y="744" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#111">CASE FILE · 1991</text></g>')
    return [layer(f"{p}L0", room, 1), layer(f"{p}L1", desk, 30)]


# ------------------------------------------------------------------ nose "front door"
def nose_door(p="nd"):
    return [layer(f"{p}L0",
        f'<defs><radialGradient id="{p}g" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#ffb7a8"/><stop offset="1" stop-color="#b34a5a"/></radialGradient></defs>'
        f'<rect width="{W}" height="{H}" fill="url(#{p}g)"/>'
        + "".join(f'<path d="M{x} 0 Q{x + 40} 540 {x - 20} 1080" fill="none" stroke="#c4566a" stroke-width="10" opacity=".5"/>' for x in range(80, 1920, 180))
        + f'<path d="M560 980 Q560 300 960 260 Q1360 300 1360 980Z" fill="#5a1626" stroke="{INK}" stroke-width="12"/>'
        f'<path d="M620 980 Q620 360 960 330 Q1300 360 1300 980Z" fill="#2a0a14"/>'
        + "".join(f'<path d="M{x} 980 q{8 * (-1) ** k} -40 0 -80" stroke="#e6a0aa" stroke-width="10" stroke-linecap="round" fill="none"/>' for k, x in enumerate(range(640, 1300, 40)))
        + f'<rect x="760" y="190" width="400" height="70" rx="12" fill="#ffd166" stroke="{INK}" stroke-width="6"/><text class="settxt" x="960" y="240" text-anchor="middle" font-family="InterBlack" font-size="38" fill="{INK}">FRONT DOOR</text>'
        f'<rect y="980" width="{W}" height="100" fill="#8e2f43"/>', 1)]
