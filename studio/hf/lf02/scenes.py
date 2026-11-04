"""LF02 scenes (FIX pass). python3 scenes.py s01 s02 ...  (no args = all). Each scene -> /home/claude/hf/lf02/<name>/index.html
Scene boundaries = CUTS (J-cut: picture cuts 0.15 s after the next scene's first sound). Every dialogue line gets the
speaker camera + listener rules from lib.Scene (talk_camera / listener_looks / close_listener)."""
import sys, json
sys.path.insert(0, "/home/claude/hf/lf02")
from lib import *
import sets as X, math

SC = {}
def scene(f): SC[f.__name__] = f; return f
G = lambda n, w, after=None: gw(n, w, after)


def notif(id_, t, text, x, y, col="#3fc1b0", S=None, d=1.4):
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t:.3f}" data-duration="{d}" style="left:{x}px;top:{y}px;padding:12px 22px;border-radius:18px;background:#fff;border:5px solid #0c1622;font:30px InterBlack;color:#0c1622;box-shadow:0 8px 0 rgba(0,0,0,.3)">'
           f'<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:{col};margin-right:10px"></span>{text}</div>')
    S.j(f'tl.fromTo("#{id_}",{{y:30,scale:.4,opacity:0}},{{y:0,scale:1,opacity:1,duration:.22,ease:"back.out(3)"}},{t:.3f});tl.to("#{id_}",{{y:-40,opacity:0,duration:.25}},{t + d - .25:.3f});')


def buzz(S, t, d=.5):
    S.j(f'tl.to("#cyPhone",{{keyframes:[' + ",".join(f'{{x:{(-1) ** i * 7},duration:.04}}' for i in range(int(d / .04))) + ',{x:0,duration:.04}]},' + f'{t:.3f});')
    S.sfx(t, "buzz", -4)


def alarm_on(S, p, t0, t1, beams=True):
    S.j(f'tl.set("#{p}red",{{opacity:0}},0);tl.to("#{p}red",{{opacity:1,duration:.08}},{t0:.3f});'
        f'tl.fromTo("#{p}red",{{opacity:1}},{{opacity:.35,duration:.35,yoyo:true,repeat:{max(1, int((t1 - t0) / .35) - 1)},ease:"sine.inOut",immediateRender:false}},{t0 + .08:.3f});'
        f'tl.to("#{p}red",{{opacity:0,duration:.2}},{t1:.3f});')
    if beams:
        S.j(f'tl.set("#{p}beamW",{{opacity:0}},0);tl.set("#{p}beamW",{{opacity:1}},{t0:.3f});tl.set("#{p}beamW",{{opacity:0}},{t1:.3f});gsap.set("#{p}beam",{{svgOrigin:"1060 95"}});'
            f'tl.fromTo("#{p}beam",{{rotation:0}},{{rotation:{360 * (t1 - t0) / 1.1:.0f},duration:{t1 - t0:.3f},ease:"none",immediateRender:false}},{t0:.3f});')
    S.j(f'tl.to("#{p}alarmGlass",{{opacity:1,duration:.1}},{t0:.3f});tl.to("#{p}alarmGlass",{{opacity:.35,duration:.1}},{t1:.3f});')


def snowfall(S, sid, T, dy=260):
    S.j(f'tl.fromTo("#{sid}",{{y:-{dy}}},{{y:0,duration:{T:.3f},ease:"none",immediateRender:false}},0);')


# =====================================================================================================
def rooftop(p="rt"):
    sky = (f'<defs><linearGradient id="{p}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1838"/><stop offset="1" stop-color="#4a3a78"/></linearGradient></defs>'
           f'<rect width="1920" height="1080" fill="url(#{p}s)"/><circle cx="1620" cy="170" r="60" fill="#f5f0d8"/>')
    far = f'<g transform="translate(0 40)">{X.skyline(760, "#24305a", "#ffd98a", seed=5)}</g>'
    mid = f'<g transform="translate(-100 120) scale(1.2)">{X.skyline(760, "#3a2a5a", "#ffe9a8", seed=8, cn=False)}</g>'
    roof = ('<path d="M-40 1100 L-40 760 L700 700 L1500 700 L1980 760 L1980 1100Z" fill="#9c5a3c" stroke="#0c1622" stroke-width="10"/>'
            '<path d="M-40 790 L1980 790" stroke="#7a4128" stroke-width="12"/>'
            + "".join(f'<path d="M{x} 700 L{x - 40} 1100" stroke="#7a4128" stroke-width="6"/>' for x in range(100, 1900, 160))
            + '<rect x="1300" y="380" width="260" height="330" fill="#c98f6a" stroke="#0c1622" stroke-width="9"/><path d="M1270 390 L1430 230 L1590 390Z" fill="#5a3a5a" stroke="#0c1622" stroke-width="9"/>'
            + '<path d="M1385 710 V560 A45 45 0 0 1 1475 560 V710Z" fill="#ffd98a" stroke="#0c1622" stroke-width="7"/>'
            + '<g id="rtsiren"><path d="M1400 230 Q1400 180 1430 180 Q1460 180 1460 230Z" fill="#ff3b3b" stroke="#0c1622" stroke-width="6"/></g>')
    return [X.layer(f"{p}L0", sky, 1), X.layer(f"{p}L1", far, 2), X.layer(f"{p}L2", mid, 3), X.layer(f"{p}L3", f'<g transform="translate(0 110)">{roof}</g>' + X.snow(p + "snow", 60, 9), 4)]


def card(S, id_, t0, t1, num, title, art, x=620, y=70, rot=-3):
    """Incident-report card: slams in (whoosh + blip), brief (<= 3 s), then gets torn off with a rip."""
    t1 = min(t1, t0 + 3.0)
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x}px;top:{y}px;width:680px;height:560px;z-index:60;transform:rotate({rot}deg);'
           f'background:#FAF4E8;border:8px solid #0c1622;border-radius:18px;box-shadow:0 18px 0 rgba(0,0,0,.35)">'
           f'<div style="position:absolute;left:0;right:0;top:0;height:86px;background:#1f2b4d;border-radius:8px 8px 0 0"></div>'
           f'<div style="position:absolute;left:28px;top:14px;font:46px InterBlack;color:#FFD166">INCIDENT {num}</div>'
           f'<div style="position:absolute;left:28px;top:458px;right:20px;font:38px/1.1 InterBlack;color:#0c1622">{title}</div>'
           f'<svg style="position:absolute;left:20px;top:100px" width="620" height="360" viewBox="0 0 620 360">{art}</svg></div>')
    S.j(f'tl.fromTo("#{id_}",{{scale:.3,rotation:-30,opacity:0}},{{scale:1,rotation:{rot},opacity:1,duration:.3,ease:"back.out(1.5)"}},{t0:.3f});'
        f'tl.to("#{id_}",{{rotation:{rot + 4},duration:.08,yoyo:true,repeat:1}},{t0 + .34:.3f});'
        f'tl.to("#{id_}",{{scale:.2,rotation:{rot + 25},opacity:0,duration:.25,ease:"power3.in"}},{t1 - .25:.3f});')
    S.covers.append((t0, t1))
    S.sfx(t0, "whoosh", -6); S.sfx(t0 + .25, "blip", -8); S.sfx(t1 - .25, "rip", -8)


ART_EXAM = ('<rect x="170" y="20" width="250" height="320" rx="10" fill="#fff" stroke="#0c1622" stroke-width="7" transform="rotate(-6 295 180)"/>'
            '<rect x="200" y="30" width="250" height="320" rx="10" fill="#fff" stroke="#0c1622" stroke-width="7" transform="rotate(4 325 190)"/>'
            + "".join(f'<circle cx="{250 + (i % 4) * 46}" cy="{90 + (i // 4) * 50}" r="14" fill="{"#0c1622" if (i * 7) % 5 == 1 else "none"}" stroke="#0c1622" stroke-width="4"/>' for i in range(20))
            + '<path d="M470 40 L520 300" stroke="#ffd166" stroke-width="26" stroke-linecap="round"/><path d="M470 40 L520 300" stroke="#0c1622" stroke-width="30" stroke-linecap="round" opacity=".25"/>'
            '<text x="90" y="120" font-family="InterBlack" font-size="80" fill="#e63946">?!</text>')
ART_CHAT = ('<rect x="200" y="0" width="220" height="360" rx="30" fill="#1b1f2a" stroke="#0c1622" stroke-width="7"/><rect x="214" y="20" width="192" height="320" rx="12" fill="#e9f7f4"/>'
            + "".join(f'<rect x="{224 if i % 2 else 260}" y="{40 + i * 52}" width="{140 - (i % 3) * 20}" height="38" rx="14" fill="{"#3fc1b0" if i % 2 else "#fff"}" stroke="#0c1622" stroke-width="3"/>' for i in range(6))
            + '<g transform="translate(440 40)"><rect width="170" height="70" rx="35" fill="#e63946" stroke="#0c1622" stroke-width="5"/><text x="85" y="48" text-anchor="middle" font-family="InterBlack" font-size="34" fill="#fff">43</text></g>'
            '<g transform="translate(10 200)"><rect width="170" height="80" rx="16" fill="#3a9a5a" stroke="#0c1622" stroke-width="5"/><text x="85" y="55" text-anchor="middle" font-family="InterBlack" font-size="40" fill="#fff">$20</text></g>')
ART_TRAIN = ('<rect x="20" y="40" width="580" height="260" rx="40" fill="#d9d4c7" stroke="#0c1622" stroke-width="7"/><rect x="20" y="230" width="580" height="22" fill="#f2c14e"/>'
             + "".join(f'<rect x="{50 + i * 136}" y="70" width="110" height="130" rx="12" fill="#9fd0ea" stroke="#0c1622" stroke-width="5"/>' for i in range(4))
             + "".join(f'<circle cx="{70 + (i % 9) * 56}" cy="{130 + (i // 9) * 40 + (i % 2) * 8}" r="22" fill="{["#3fc1b0", "#ff9f5a", "#7a5cc7", "#f2c6da"][i % 4]}" stroke="#0c1622" stroke-width="4"/>' for i in range(18))
             + '<circle cx="110" cy="320" r="26" fill="#333"/><circle cx="510" cy="320" r="26" fill="#333"/>'
             '<g transform="translate(470 0)"><circle cx="50" cy="40" r="40" fill="#f2c14e" stroke="#0c1622" stroke-width="6"/><text x="50" y="56" text-anchor="middle" font-family="InterBlack" font-size="46" fill="#0c1622">1</text></g>')
ART_AUNTIE = ('<circle cx="190" cy="230" r="120" fill="#c5a3ff" stroke="#0c1622" stroke-width="7"/><path d="M80 170 Q190 40 300 170 Q190 120 80 170Z" fill="#4a2a5a" stroke="#0c1622" stroke-width="6"/>'
              '<circle cx="150" cy="220" r="18" fill="#0c1622"/><circle cx="230" cy="220" r="18" fill="#0c1622"/><path d="M120 190 L175 200 M260 190 L205 200" stroke="#0c1622" stroke-width="8" stroke-linecap="round"/>'
              '<ellipse cx="190" cy="285" rx="22" ry="14" fill="#7a1f2e"/><circle cx="150" cy="300" r="10" fill="#ffd166" stroke="#0c1622" stroke-width="3"/>'
              '<path d="M330 40 H600 V200 H420 L370 250 L380 200 H330Z" fill="#fff" stroke="#0c1622" stroke-width="6" stroke-linejoin="round"/>'
              '<text x="465" y="100" text-anchor="middle" font-family="InterBlack" font-size="34" fill="#0c1622">SO... WHAT</text><text x="465" y="146" text-anchor="middle" font-family="InterBlack" font-size="34" fill="#0c1622">ARE YOU</text><text x="465" y="190" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">DOING??</text>')


BEAR = ('<path d="M40 150 Q30 80 80 70 Q70 30 100 30 Q120 30 125 55 Q160 40 200 55 Q205 30 225 30 Q255 30 245 70 Q290 80 280 150 Q300 230 220 240 L100 240 Q20 230 40 150Z" fill="#7a4b2c" stroke="#0c1622" stroke-width="7"/>'
        '<circle cx="120" cy="130" r="11" fill="#0c1622"/><circle cx="200" cy="130" r="11" fill="#0c1622"/><ellipse cx="160" cy="175" rx="38" ry="28" fill="#c9965f" stroke="#0c1622" stroke-width="5"/><ellipse cx="160" cy="165" rx="14" ry="9" fill="#0c1622"/>')


def bubble(S, id_, t0, t1, inner, x, y, w=340, h=300):
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:55">'
           f'<svg width="{w}" height="{h + 80}" style="overflow:visible"><ellipse cx="{w / 2}" cy="{h / 2}" rx="{w / 2 - 6}" ry="{h / 2 - 6}" fill="#fff" stroke="#0c1622" stroke-width="7"/>'
           f'<circle cx="{w * .2}" cy="{h + 10}" r="18" fill="#fff" stroke="#0c1622" stroke-width="6"/><circle cx="{w * .1}" cy="{h + 50}" r="10" fill="#fff" stroke="#0c1622" stroke-width="5"/>'
           f'<g transform="translate({w / 2 - 160} {h / 2 - 135})">{inner}</g></svg></div>')
    S.j(f'tl.fromTo("#{id_}",{{scale:0,transformOrigin:"20% 100%"}},{{scale:1,duration:.3,ease:"back.out(2)"}},{t0:.3f});')


def src_chip(S, id_, t0, t1, txt, x=40, y=36, right=False):
    """Source chip: reserved zone at the top-RIGHT corner (v3: top-left belongs to the CASE sticker; never on a face)."""
    right = True
    pos = f"right:40px;top:{y}px" if right else f"left:{x}px;top:{y}px"
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="{pos};padding:10px 22px;border-radius:14px;background:#0c1622;border:4px solid #FAF4E8;font:34px InterBlack;color:#FAF4E8;z-index:74">{txt}</div>')
    S.j(f'tl.fromTo("#{id_}",{{y:-40,opacity:0}},{{y:0,opacity:1,duration:.25,ease:"power3.out"}},{t0:.3f});')


def flipsign(S, id_, t, txt0, txt1, x=80, y=60, w=620):
    S.add(f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:120px;z-index:9;perspective:800px">'
          f'<div style="position:absolute;left:{w // 2 - 4}px;top:-80px;width:8px;height:80px;background:#333"></div>'
          f'<div id="{id_}a" style="position:absolute;inset:0;border-radius:14px;background:#151a24;border:6px solid #0c1622;font:50px/108px InterBlack;color:#FFD166;text-align:center"><span class="settxt">{txt0}</span></div>'
          f'<div id="{id_}b" style="position:absolute;inset:0;border-radius:14px;background:#151a24;border:6px solid #0c1622;font:50px/108px InterBlack;color:#ff8a8a;text-align:center;opacity:0"><span class="settxt">{txt1}</span></div></div>')
    S.j(f'tl.to("#{id_}a",{{rotationX:90,duration:.15,ease:"power2.in"}},{t:.3f});tl.set("#{id_}a",{{opacity:0}},{t + .15:.3f});'
        f'tl.fromTo("#{id_}b",{{rotationX:-90,opacity:1}},{{rotationX:0,duration:.25,ease:"back.out(2)",immediateRender:false}},{t + .15:.3f});')
    S.sfx(t, "flip", -6)


BENCH = ('<rect x="1180" y="720" width="620" height="40" rx="10" fill="#7a4b2c" stroke="#0c1622" stroke-width="7"/>'
         '<rect x="1220" y="760" width="26" height="110" fill="#555" stroke="#0c1622" stroke-width="5"/><rect x="1730" y="760" width="26" height="110" fill="#555" stroke="#0c1622" stroke-width="5"/>'
         '<rect x="1180" y="620" width="620" height="30" rx="10" fill="#8a5a36" stroke="#0c1622" stroke-width="6"/>'
         '<rect x="1720" y="660" width="60" height="70" rx="10" fill="#3fc1b0" stroke="#0c1622" stroke-width="6"/>')
CORT = ('<rect x="0" y="40" width="150" height="80" rx="40" fill="#FFD166" stroke="#0c1622" stroke-width="6"/><text x="75" y="92" text-anchor="middle" font-family="InterBlack" font-size="22" fill="#0c1622">CORTISOL</text>'
        '<path d="M150 70 L210 40 L210 120 L150 90Z" fill="#e63946" stroke="#0c1622" stroke-width="5"/>')
IMM = ('<circle cx="90" cy="90" r="80" fill="#8ce2d6" stroke="#0c1622" stroke-width="7"/><circle cx="62" cy="80" r="10" fill="#0c1622"/><circle cx="118" cy="80" r="10" fill="#0c1622"/>'
       '<path d="M70 120 Q90 112 110 120" stroke="#0c1622" stroke-width="6" fill="none" stroke-linecap="round"/>'
       '<g id="hph" opacity="0"><path d="M10 80 Q90 -30 170 80" fill="none" stroke="#222" stroke-width="14"/><rect x="0" y="70" width="28" height="50" rx="10" fill="#e63946" stroke="#0c1622" stroke-width="5"/><rect x="152" y="70" width="28" height="50" rx="10" fill="#e63946" stroke="#0c1622" stroke-width="5"/>'
       '<text x="190" y="40" font-family="InterBlack" font-size="40" fill="#FFD166">♪</text></g>')
FLAME = '<path d="M30 0 Q60 40 50 70 Q70 60 66 40 Q90 70 70 100 Q40 120 14 100 Q-6 80 10 50 Q16 70 26 72 Q14 40 30 0Z" fill="#ff7a29" stroke="#0c1622" stroke-width="5"/><path d="M40 60 Q56 80 46 100 Q30 104 26 90 Q24 76 40 60Z" fill="#FFD166"/>'


def reel(inner):
    return (f'<div style="position:absolute;inset:0;background:#111"><svg width="1920" height="1080">'
            + "".join(f'<rect x="{40 + i * 120}" y="20" width="60" height="40" rx="6" fill="#444"/><rect x="{40 + i * 120}" y="1020" width="60" height="40" rx="6" fill="#444"/>' for i in range(16))
            + f'<rect x="80" y="90" width="1760" height="900" fill="#d6d6d6" stroke="#000" stroke-width="10"/>{inner}</svg></div>')


SCI = lambda x: (f'<g transform="translate({x} 110)"><rect x="-50" y="120" width="100" height="160" rx="30" fill="#fff" stroke="#000" stroke-width="6"/><circle cx="0" cy="80" r="55" fill="#bbb" stroke="#000" stroke-width="6"/>'
                 f'<rect x="-40" y="62" width="80" height="26" rx="12" fill="#333"/><path d="M40 170 L120 210" stroke="#000" stroke-width="16" stroke-linecap="round"/>'
                 f'<g class="drop"><rect x="110" y="190" width="24" height="70" rx="6" fill="#eee" stroke="#000" stroke-width="5"/><circle cx="122" cy="186" r="16" fill="#666" stroke="#000" stroke-width="5"/></g></g>')
VOL = lambda x: (f'<g transform="translate({x} 560)"><circle cx="0" cy="120" r="90" fill="#9a9a9a" stroke="#000" stroke-width="7"/><circle cx="-30" cy="100" r="12" fill="#000"/><circle cx="30" cy="100" r="12" fill="#000"/>'
                 f'<ellipse cx="0" cy="140" rx="16" ry="11" fill="#555"/><path d="M-30 175 Q0 160 30 175" stroke="#000" stroke-width="6" fill="none"/></g>')
TINYRH = '<g><circle r="22" fill="#777" stroke="#000" stroke-width="5"/>' + "".join(f'<circle cx="{30 * math.cos(a / 6 * 6.283):.0f}" cy="{30 * math.sin(a / 6 * 6.283):.0f}" r="7" fill="#aaa" stroke="#000" stroke-width="3"/>' for a in range(6)) + '<rect x="-16" y="-8" width="32" height="10" rx="4" fill="#000"/></g>'


def lever_pull(S, p, t):
    S.j(f'gsap.set("#{p}lever",{{svgOrigin:"1255 545"}});tl.to("#{p}lever",{{rotation:180,duration:.12,ease:"power3.in"}},{t:.3f});tl.to("#{p}lever",{{rotation:0,duration:.3,ease:"back.out(2)"}},{t + .35:.3f});')
    S.sfx(t + .08, "clunk", -6)


def breath_ring(S, t0, tin, tout):
    S.over(f'<div id="ring" class="clip" data-start="{t0:.3f}" data-duration="{tout - t0 + .4:.3f}" style="position:absolute;left:760px;top:140px;width:400px;height:400px;z-index:55">'
           '<svg width="400" height="400"><circle id="ringC" cx="200" cy="200" r="150" fill="rgba(140,226,214,.18)" stroke="#8ce2d6" stroke-width="14"/></svg>'
           '<div id="ringT" style="position:absolute;left:0;right:0;top:170px;text-align:center;font:46px InterBlack;color:#FAF4E8;-webkit-text-stroke:2px #0c1622">IN...</div></div>')
    S.j(f'gsap.set("#ringC",{{transformOrigin:"200px 200px"}});tl.fromTo("#ringC",{{scale:.4}},{{scale:1.15,duration:{tin - t0:.3f},ease:"sine.inOut"}},{t0:.3f});'
        f'tl.to("#ringC",{{scale:.4,duration:{tout - tin:.3f},ease:"sine.inOut"}},{tin:.3f});')


SNEAKER = '<path d="M10 70 L20 30 Q50 40 70 20 L100 50 L150 60 Q160 80 150 90 L10 90Z" fill="#fbfbf6" stroke="#0c1622" stroke-width="6"/><rect x="10" y="84" width="145" height="12" fill="#e63946" stroke="#0c1622" stroke-width="4"/>'
MEDIT = '<circle cx="80" cy="30" r="22" fill="#ff9f5a" stroke="#0c1622" stroke-width="5"/><path d="M30 95 Q80 40 130 95Z" fill="#7a5cc7" stroke="#0c1622" stroke-width="5"/><path d="M40 70 L10 60 M120 70 L150 60" stroke="#0c1622" stroke-width="6" stroke-linecap="round"/>'
WIND = '<path d="M10 40 H110 Q140 40 140 20 Q140 0 120 0 M10 65 H130 Q160 65 160 85 Q160 105 140 105 M10 90 H80" fill="none" stroke="#3fc1b0" stroke-width="10" stroke-linecap="round"/>'


def nps(p="np"):
    arches = ('<path d="M260 520 Q960 120 1660 520" fill="none" stroke="#f6f0e0" stroke-width="30"/><path d="M500 520 Q960 230 1420 520" fill="none" stroke="#f6f0e0" stroke-width="26"/>'
              + "".join(f'<rect x="{x}" y="440" width="26" height="200" fill="#f6f0e0" stroke="#0c1622" stroke-width="4"/>' for x in (300, 520, 1380, 1600)))
    lights = "".join(f'<circle cx="{x}" cy="{360 + 130 * ((x - 960) / 700) ** 2:.0f}" r="9" fill="{["#ffd166", "#ff6b6b", "#8ce2d6"][i % 3]}"/>' for i, x in enumerate(range(300, 1640, 40)))
    rink = '<ellipse cx="960" cy="860" rx="1100" ry="260" fill="#cfe9f7" stroke="#0c1622" stroke-width="8"/><ellipse cx="960" cy="860" rx="900" ry="190" fill="none" stroke="#fff" stroke-width="6"/>'
    hall = '<path d="M60 640 Q200 300 420 300 L420 640Z" fill="#9aa3ab" stroke="#0c1622" stroke-width="6"/><path d="M1860 640 Q1720 260 1480 260 L1480 640Z" fill="#9aa3ab" stroke="#0c1622" stroke-width="6"/><ellipse cx="960" cy="560" rx="150" ry="60" fill="#c9ccd2" stroke="#0c1622" stroke-width="6"/>'
    return [X.layer(f"{p}0", '<rect width="1920" height="1080" fill="#16224a"/>' + X.skyline(640, "#24305a", seed=12), 1), X.layer(f"{p}1", hall + arches + lights, 2), X.layer(f"{p}2", rink, 3)]


def distillery(p="ds"):
    brick = "".join(f'<rect x="{x + (y // 40 % 2) * 40}" y="{y}" width="76" height="36" fill="#a4553a" stroke="#6e3523" stroke-width="4"/>' for y in range(0, 760, 40) for x in range(-80, 1960, 80))
    wins = "".join(f'<rect x="{x}" y="180" width="140" height="220" rx="70" fill="#ffd98a" stroke="#0c1622" stroke-width="6"/>' for x in (180, 620, 1160, 1600))
    strs = "".join(f'<path d="M0 {y} Q960 {y + 120} 1920 {y}" fill="none" stroke="#333" stroke-width="3"/>' + "".join(f'<circle cx="{x}" cy="{y + 120 * (1 - ((x - 960) / 960) ** 2):.0f}" r="10" fill="#ffe08a"/>' for x in range(40, 1900, 70)) for y in (90, 470))
    ground = '<rect y="760" width="1920" height="320" fill="#5a4a40"/>' + "".join(f'<rect x="{x}" y="{y}" width="110" height="50" fill="#6b5a4e" stroke="#4a3c34" stroke-width="4"/>' for y in (780, 840, 900, 960, 1020) for x in range(-50 + (y // 60 % 2) * 55, 1920, 115))
    return [X.layer(f"{p}0", brick + wins, 1), X.layer(f"{p}1", ground + strs, 2)]


def block(p="bk"):
    houses = "".join(f'<g transform="translate({x} 0)"><rect x="0" y="380" width="300" height="380" fill="{c}" stroke="#0c1622" stroke-width="6"/><path d="M-20 390 L150 240 L320 390Z" fill="#5a3a5a" stroke="#0c1622" stroke-width="6"/>'
                     f'<rect x="40" y="460" width="80" height="90" fill="#ffd98a" stroke="#0c1622" stroke-width="5"/><rect x="180" y="560" width="80" height="200" fill="#7a4b2c" stroke="#0c1622" stroke-width="5"/></g>'
                     for x, c in ((-60, "#c98f6a"), (320, "#9fb4c8"), (700, "#c9a3d8"), (1080, "#d9b38a"), (1460, "#a9c9a0")))
    walk = '<rect y="760" width="1920" height="320" fill="#d9dde3"/><rect y="760" width="1920" height="26" fill="#9aa3ab"/>' + "".join(f'<path d="M{x} 786 L{x - 60} 1080" stroke="#bfc5cc" stroke-width="5"/>' for x in range(100, 2000, 220))
    return [X.layer(f"{p}0", '<rect width="1920" height="1080" fill="#9fc3e0"/>' + houses + X.snow(p + "sn", 50, 4), 1), X.layer(f"{p}1", walk, 2)]


BIRD = ('<g id="bird"><ellipse cx="40" cy="40" rx="34" ry="26" fill="#4f86ff" stroke="#0c1622" stroke-width="5"/><circle cx="62" cy="24" r="18" fill="#4f86ff" stroke="#0c1622" stroke-width="5"/>'
        '<circle cx="68" cy="20" r="4" fill="#0c1622"/><path d="M78 24 L94 28 L78 32Z" fill="#ffb02e" stroke="#0c1622" stroke-width="3"/><path d="M10 40 L-8 30 L0 50Z" fill="#3a6ad6" stroke="#0c1622" stroke-width="4"/></g>')


SOURCES = [("Fight-or-flight: standard physiology (textbook)", "Cohen et al., PNAS 2012"),
           ("Cohen, Tyrrell & Smith, NEJM 1991", "Kloner, Prog Cardiovasc Dis 2006"),
           ("Milne, Eur J Epidemiol 2005", "Weerasinghe, Heart 2002"),
           ("Birdee et al., Complement Ther Med 2023", "van der Zwan et al., Appl Psychophysiol Biofeedback 2015"),
           ("Distillery Winter Village (free before 4 pm)", "Nathan Phillips Square skating: City of Toronto")]




# =====================================================================================================  FIX PASS
DOOR = .45      # doors scenes: the picture cuts once the subway doors have closed (beat start + 0.45 s)
def cut_doors(beat): return round(BEATS[beat][0] + DOOR, 3)
CUTS = {
    "s01": (0, cut_doors("title")), "s02": (cut_doors("title"), cut_doors("to_report")),
    "s03": (cut_doors("to_report"), round(BEATS["to_court"][0] + .95, 3)),
    "s04": (round(BEATS["to_court"][0] + .95, 3), round(gw(13, "runs") - .1, 3)), "s05": (round(gw(13, "runs") - .1, 3), cut_line(14)),
    "s06": (cut_line(14), cut_line(18)), "s06d": (cut_line(18), cut_line(19)), "s06b": (cut_line(19), cut_doors("to_bench")),
    "s07": (cut_doors("to_bench"), round(gw(32, "And"), 3)), "s08": (round(gw(32, "And"), 3), cut_line(69)),
    "s08b": (cut_line(69), cut_doors("noir")), "s09": (cut_doors("noir"), cut_doors("to_hq")),
    "s10": (cut_doors("to_hq"), cut_doors("to_heart")), "s11": (cut_doors("to_heart"), cut_doors("to_recap")),
    "s11r": (cut_doors("to_recap"), cut_line(51)), "s12": (cut_line(51), cut_line(53)), "s13": (cut_line(53), cut_doors("to_city")),
    "s14": (cut_doors("to_city"), cut_doors("to_hq3")), "s15": (cut_doors("to_hq3"), cut_beat("chirp")),
    "s16": (cut_beat("chirp"), cut_beat("breakstarts")), "s17": (cut_beat("breakstarts"), TM["T"]),
}
ORDER_SC = list(CUTS)
AMB = {}      # scene -> room-tone kind (mix.py lays a continuous bed under every scene)


def mk(name, music, bg, amb):
    t0, t1 = CUTS[name]; AMB[name] = amb
    S = Scene(name, t0, t1, music=music, bg=bg); S.ambience = amb
    return S


def alarm_shake(S, p, t0, t1):
    """the alarm bell keeps rattling for as long as the siren runs (F)."""
    S.j(f'gsap.set("#{p}alarm",{{svgOrigin:"1060 40"}});tl.fromTo("#{p}alarm",{{rotation:-4}},{{rotation:4,duration:.09,yoyo:true,repeat:{max(1, int((t1 - t0) / .09))},ease:"sine.inOut",immediateRender:false}},{t0:.3f});'
        f'tl.to("#{p}alarm",{{rotation:0,duration:.1}},{t1:.3f});')


@scene
def s01():
    """COLD OPEN (I11): the alarm DROPS in at frame 3, siren + red wash by 0.4 s while Cyto brags over it; the door bursts on
    "I'm him", Neutro storms in; shot/reverse-shot "Code red" / "for what?" / "December." / eyeroll / "...nyeahh"; title slam."""
    S = mk("s01", None, "#47306b", "hq")
    MUSIC.append((0, S.t1, "alarm"))
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq"))
    snowfall(S, "hqsnow", S.T)
    tS = .35; tB = BEATS["title"][0]
    l2, l3, l4, l5 = S.l(2), S.l(3), S.l(4), S.l(5)
    S.prop_in("#hqalarm", .08, "drop", svg="1060 40", sfx="clunk")
    alarm_on(S, "hq", tS, S.T - .02)
    alarm_shake(S, "hq", tS + .55, S.T)
    S.j(f'gsap.set("#hqlamp",{{svgOrigin:"1000 770"}});tl.fromTo("#hqlamp",{{scaleY:1,scaleX:1}},{{keyframes:[{{scaleY:.8,scaleX:1.15,duration:.08}},{{scaleY:1.15,scaleX:.9,duration:.1}},{{scaleY:1,scaleX:1,duration:.2}}],immediateRender:false}},{tS:.3f});')
    S.shake(tS, .45, 14)
    S.sfx(tS - .05, "siren", -4)
    # Rhino pressed to the window (clipped to the arch) during the title
    S.add('<div id="rhClip" class="fill" style="z-index:1;clip-path:path(\'M283 657 V385 A222 222 0 0 1 727 385 V657Z\')">'
          + K.wrap(K.rhino_html("rh", "idle"), "rhW", 380, 700, .62) + '</div>')
    S.j(f'tl.set("#rhW",{{y:0}},0);tl.to("#rhW",{{y:-500,duration:.35,ease:"back.out(1.6)"}},{tB + .05:.3f});tl.to("#rhW",{{x:14,duration:.12,yoyo:true,repeat:3}},{tB + .4:.3f});')
    S.j(K.act_js("rh", 28, 26, poses=[(tB + .35, "wave")], expr=[(tB + .1, 1.2, "smug")], T=S.T, blinks=[]))
    # Cyto: chilling, phone buzzing, unbothered by the siren
    S.cyto(540, 640, .6, phone=True,
           expr=[(S.w(1, "Nah") - .05, .8, "skeptic"), (l5[0] - .05, .2, "squint")],
           x_expr=[(S.w(1, "him"), .5, "smug"), (l2[1] - .02, l3[0] - l2[1] + .5, "deadpan"), (l4[1] + .02, l5[1] - l4[1] + .3, "exhausted"), (tB + .2, .8, "sideeye")],
           sips=[(S.w(1, "I", ) - .05, .9)], tilts=[(S.w(1, "Exams"), .45, -6), (l3[0], .5, 7)], shrugs=[(S.w(1, "Nah"), .55)],
           looks=[(S.w(1, "Group") - .1, -10, 8)])
    for t, txt, x in ((S.w(1, "Exams"), "EXAMS", 760), (S.w(1, "Group"), "GROUP CHAT", 790), (S.w(1, "Holiday"), "SALE ENDS SOON", 760)):
        buzz(S, t - .1); notif(f"n{int(t * 10)}", t - .1, txt, x, 470 - (t - .3) * 30, S=S, d=1.0)
    # the door BURSTS open on "him" and Neutro storms in
    tD = S.w(1, "him") + .1
    S.j(f'gsap.set("#hqdoor",{{svgOrigin:"1530 520"}});tl.to("#hqdoor",{{scaleX:1.04,duration:.06}},{tD - .08:.3f});tl.to("#hqdoor",{{scaleX:.12,duration:.12,ease:"power4.out"}},{tD:.3f});tl.to("#hqdoor",{{scaleX:.22,duration:.45,ease:"elastic.out(1,.35)"}},{tD + .12:.3f});')
    S.sfx(tD, "slam", -3)
    S.char("neutro", "nt", 1410, 300, .74, pose="idle", who="NEUTRO",
           poses=[(tD + .05, "radio"), (l4[0] - .1, "idle"), (l5[0] + .3, "cross")],
           expr=[(tD + .05, l2[1] - tD, "determined"), (l4[0] - .05, .95, "deadpan"), (l4[1] + .05, .7, "sideeye"), (tB + .2, .9, "sideeye")],
           looks=[(l4[1] + .05, 0, -.25)], nods=[l2[0] + .05])
    S.j(f'tl.set("#ntW",{{x:420,opacity:0}},0);tl.set("#ntW",{{opacity:1}},{tD + .02:.3f});tl.to("#ntW",{{x:0,duration:.3,ease:"power3.out"}},{tD + .04:.3f});'
        f'tl.fromTo("#ntW",{{y:-24}},{{y:0,duration:.3,ease:"bounce.out",immediateRender:false}},{tD + .2:.3f});')
    S.sfx(tD + .15, "kick", -6)
    # TITLE SLAM (stays on through the whip into the skyline)
    S.over(f'<div id="title" class="clip" data-start="{tB:.3f}" data-duration="{S.T - tB:.3f}" style="position:absolute;left:780px;right:40px;top:110px;text-align:center;z-index:97">'
           '<div style="font:120px/1 InterBlack;color:#FAF4E8;-webkit-text-stroke:7px #0c1622;paint-order:stroke fill;text-shadow:0 12px 0 rgba(0,0,0,.45)">DECEMBER:</div>'
           '<div style="font:156px/1 InterBlack;color:#ff3b3b;-webkit-text-stroke:8px #0c1622;paint-order:stroke fill;text-shadow:0 14px 0 rgba(0,0,0,.45)">CODE RED</div></div>')
    S.hide_txt(tB, S.T); S.j(f'tl.fromTo("#title",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:.2,ease:"power4.in"}},{tB:.3f});')
    S.shake(tB + .2, .4, 22); S.sfx(tB + .18, "hit", -2)
    S.tr_out("doors", label="YOUR BODY")
    S.captions({"red": "#ff6b6b", "december": "#ff6b6b", "him": "#FFD166"})
    return S


def rooftop2(p="rt"):
    """Rooftop host set in front of the REAL skyline (blurred, darkened photo plate with parallax)."""
    sky = (f'<image href="assets/ph_skyline_bg.jpg" x="-96" y="-120" width="2112" height="1188" preserveAspectRatio="xMidYMid slice"/>'
           f'<rect width="1920" height="1080" fill="#2b1640" opacity=".18"/>')
    roof = ('<path d="M-40 1100 L-40 760 L700 700 L1500 700 L1980 760 L1980 1100Z" fill="#9c5a3c" stroke="#0c1622" stroke-width="10"/>'
            '<path d="M-40 790 L1980 790" stroke="#7a4128" stroke-width="12"/>'
            + "".join(f'<path d="M{x} 700 L{x - 40} 1100" stroke="#7a4128" stroke-width="6"/>' for x in range(100, 1900, 160))
            + '<rect x="1300" y="380" width="260" height="330" fill="#c98f6a" stroke="#0c1622" stroke-width="9"/><path d="M1270 390 L1430 230 L1590 390Z" fill="#5a3a5a" stroke="#0c1622" stroke-width="9"/>'
            + '<path d="M1385 710 V560 A45 45 0 0 1 1475 560 V710Z" fill="#ffd98a" stroke="#0c1622" stroke-width="7"/>'
            + '<g id="rtsiren"><path d="M1400 230 Q1400 180 1430 180 Q1460 180 1460 230Z" fill="#ff3b3b" stroke="#0c1622" stroke-width="6"/></g>')
    return [X.layer(f"{p}L1", sky, 2), X.layer(f"{p}L3", f'<g transform="translate(0 110)">{roof}</g>' + X.snow(p + "snow", 60, 9), 4)]


@scene
def s02():
    """INTRO: real skyline (Ken Burns) "THE BODY = THE 6IX" -> real Queen's Park photo "QUEEN'S PARK HQ" -> Cyto hosts on the
    rooftop in front of the real (blurred) skyline. Text over photos sits on dark panels."""
    S = mk("s02", "intro", "#2b1640", "city")
    S.talk_scale = 0                      # VO over photos, then a single host: manual camera
    tQP = S.w(6, "inside") - .04; tR = S.w(6, "lowkey") - .3
    S.photo("phS", "skyline", 0, tQP + .2, (1.0, 1.1), z=50, ox="62%", oy="40%")
    S.photo("phQ", "queens_park", tQP, tR + .2, (1.03, 1.12), z=51, ox="50%", oy="55%")
    S.tr_in("doors", label="YOUR BODY")
    S.j(f'tl.to("#title",{{scale:.6,opacity:0,duration:.25,ease:"power3.in"}},.75);')
    S.over(f'<div id="title" class="clip" data-start="0" data-duration="1.1" style="position:absolute;left:780px;right:40px;top:110px;text-align:center;z-index:97">'
           '<div style="font:120px/1 InterBlack;color:#FAF4E8;-webkit-text-stroke:7px #0c1622;paint-order:stroke fill;text-shadow:0 12px 0 rgba(0,0,0,.45)">DECEMBER:</div>'
           '<div style="font:156px/1 InterBlack;color:#ff3b3b;-webkit-text-stroke:8px #0c1622;paint-order:stroke fill;text-shadow:0 14px 0 rgba(0,0,0,.45)">CODE RED</div></div>')
    S.panel("pb1", 1.1, tQP - .05, "THE BODY", "= THE 6IX", "#FFD166", 60, 60, 620)
    S.panel("pb2", tQP + .1, tR, "BRAIN =", "QUEEN'S PARK HQ", "#8ce2d6", 60, 60, 760)
    S.sfx(tQP - .04, "whoosh", -8); S.sfx(0, "whoosh", -6)
    # rooftop host shot
    for l in rooftop2("rt"): S.add(l)
    S.parallax([("rtL1", .3), ("rtL3", .8)], tR, S.T, dx=-90)
    snowfall(S, "rtsnow", S.T, 300)
    S.j(f'gsap.set("#rtsiren",{{transformOrigin:"50% 100%"}});tl.fromTo("#rtsiren",{{opacity:1}},{{opacity:.3,duration:.3,yoyo:true,repeat:{int(S.T / .3)},immediateRender:false}},0);')
    S.cyto(700, 700, .62, outfit="outfit_pufferhoodie",
           expr=[(S.w(6, "lowkey"), .9, "squint"), (S.w(6, "bro") - .05, 1.1, "shock"), (S.w(6, "cheat"), .9, "hype")],
           x_expr=[(S.w(6, "Today"), 1.1, "determined"), (S.w(6, "Not"), 1.5, "deadpan")],
           waves=[tR + .4], points=[(S.w(6, "why"), .8), (S.w(6, "cheat"), .8)], sips=[(S.w(6, "just") - .2, 1.0)],
           tilts=[(S.w(6, "panicking"), .7, -7), (S.w(6, "science") - .3, .6, 6)], shrugs=[(S.w(6, "plus"), .6)], looks=[(S.w(6, "why") + .1, 14, -8)])
    S.j(f'tl.set("#cytoLayer",{{opacity:0}},0);tl.set("#cytoLayer",{{opacity:1}},{tR:.3f});'
        f'tl.fromTo("#cytoPos",{{y:"+=320"}},{{y:"-=320",duration:.4,ease:"back.out(1.7)",immediateRender:false}},{tR:.3f});')
    S.sfx(tR + .05, "boing", -10)
    # host camera: a new framing every ~3 s
    for a, b, sc, ox, oy in ((tR, S.w(6, "Today") - .1, 1.0, 700, 600), (S.w(6, "Today") - .1, S.w(6, "plus") - .1, 1.08, 700, 600),
                             (S.w(6, "plus") - .1, S.w(6, "And", after=S.w(6, "plus")) - .1, 1.16, 700, 560),
                             (S.w(6, "And", after=S.w(6, "plus")) - .1, S.w(6, "Not") - .1, 1.05, 900, 560), (S.w(6, "Not") - .1, S.T, 1.1, 700, 600)):
        S.j(f'tl.to("#tk",{{scale:{sc},x:{(1 - sc) * ox:.0f},y:{(1 - sc) * oy:.0f},duration:.3,ease:"power2.inOut",transformOrigin:"0px 0px"}},{a:.3f});')
    # Rhino tiptoes along the roof behind Cyto (sight gag)
    S.char("rhino", "rh", 2000, 590, .45, pose="sneak", z=5, expr=[(S.w(6, "Today"), 4, "smug")], blinks=[])
    S.j(f'tl.fromTo("#rhW",{{x:0}},{{x:-2500,duration:10,ease:"none",immediateRender:false}},{S.w(6, "Today") - .5:.3f});'
        f'tl.to("#rh",{{y:-16,duration:.25,yoyo:true,repeat:19,ease:"sine.inOut"}},{S.w(6, "Today") - .5:.3f});')
    S.sfx(S.w(6, "Today") - .4, "tiptoe", -10)
    S.popup("tz1", S.w(6, "why") - .05, S.w(6, "plus") - .1, "TODAY'S CASE", "WHO KEEPS PULLING THE ALARM?", "#8ce2d6", 1380, 150, 860)
    S.popup("tz2", S.w(6, "plus"), S.w(6, "And", after=S.w(6, "plus")) - .1, "CASE FILE", "ONE STUDY: “BRO, WHAT”", "#ff8a8a", 1380, 150, 860)
    S.popup("tz3", S.w(6, "cheat") - .1, S.w(6, "Not") - .15, "LOADING...", "CHEAT CODES", "#FFD166", 1380, 150, 860)
    S.sfx(S.w(6, "bro") - .05, "sting", -6); S.sfx(S.w(6, "cheat") - .1, "coin", -8)
    S.over(f'<div id="nma" class="clip" data-start="{S.w(6, "Not") - .1:.3f}" data-duration="{S.T - S.w(6, "Not") + .1:.3f}" style="position:absolute;left:1140px;top:180px;width:700px;z-index:70;'
           'padding:26px 30px;border-radius:24px;background:#FAF4E8;border-left:16px solid #e63946;box-shadow:0 14px 0 rgba(0,0,0,.35)">'
           '<div style="font:44px InterBlack;color:#e63946">NOT MEDICAL ADVICE</div><div style="font:36px/1.2 InterSB;color:#0c1622;margin-top:6px">Just your boy + some science. Sources on screen + in the description.</div></div>')
    S.j(f'tl.fromTo("#nma",{{x:80,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"back.out(1.6)"}},{S.w(6, "Not") - .1:.3f});')
    S.tr_out("doors", label="QUEEN'S PARK HQ")
    S.captions({"6ix": "#FFD166", "panicking": "#ff6b6b", "bro": "#ff8a8a", "what": "#ff8a8a"})
    return S


@scene
def s03():
    """ACT 1 - the incident report (HQ). Doors open on the HQ wide + location card; Neutro reads, each card is a brief pop-in
    he flicks away; Cyto takes each one personally. N1: "That's the evidence. Now watch what it does. Follow me." -> CLUE 1
    recap card, Neutro points to the exit and WALKS Cyto out; doors close on NEXT STOP: THE COURT."""
    S = mk("s03", "alarm_low", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    alarm_on(S, "hq", 0, S.T, beams=False); alarm_shake(S, "hq", 0, S.T)
    S.tr_in("doors", label="QUEEN'S PARK HQ")
    S.location("QUEEN'S PARK HQ", "your brain · alarm control", .45, 2.3)
    S.parallax([("hqL0", .2), ("hqL1", .35), ("hqL2", .5), ("hqL3", 1.0)], 0, S.T, dx=-60)
    S.talk_off = {67}                        # N1 plays on the WIDE so both walk out of a full frame
    l = {n: S.l(n) for n in list(range(7, 13)) + [67]}
    cards = [(7, "EXAMS.", ART_EXAM, "ONE"), (8, "SECRET SANTA GROUP CHAT", ART_CHAT, "TWO"), (9, "THE MALL = LINE 1 AT RUSH HOUR", ART_TRAIN, "THREE"), (10, "YOUR AUNTIE.", ART_AUNTIE, "FOUR")]
    flicks = []
    for i, (n, title, art, num) in enumerate(cards):
        a = max(.2, l[n][0] - .05); b = min(l[n][1] + .2, a + 3.0)
        card(S, f"ic{n}", a, b, num, title, art, x=640, y=60, rot=(-3, 2, -2, 3)[i]); flicks.append(b - .3)
    tF = S.w(67, "Follow"); tEnd = S.T - .4
    S.cyto(420, 660, .56, expr=[(l[8][0] + 1.2, 1.0, "skeptic"), (l[10][0] + 1.2, 1.2, "shock"), (l[11][0], 1.0, "skeptic")],
           x_expr=[(l[7][0] + .8, 1.0, "deadpan"), (l[9][0] + 1.0, 1.5, "exhausted"), (l[12][0], 1.0, "worried"), (S.w(67, "watch"), 1.0, "determined")],
           shrugs=[(l[11][0] + .1, .7)], tilts=[(l[10][0] + 2.0, .8, -8)], sips=[(l[9][1] - .8, 1.0)])
    S.char("neutro", "nt", 1340, 300, .74, pose="notepad", who="NEUTRO",
           poses=[(f, "point") for f in flicks] + [(f + .35, "notepad") for f in flicks] + [(l[12][0] + .1, "notepad"), (l[67][0] + .05, "idle"), (tF - .1, "point")],
           expr=[(l[7][0], 1.2, "deadpan"), (l[11][0] + .3, .9, "sideeye"), (l[12][0], 1.1, "smug"), (l[67][0] + .2, 1.6, "determined")],
           nods=[l[12][0] + .4, S.w(67, "watch")], walks=[(tF + .45, tEnd, 760)])
    S.sfx(l[12][0] + .4, "tap", -6)
    # Neutro leads, Cyto hops after him (anticipation squash -> 3 hops on arcs -> out of frame right)
    tc = tF + .75
    S.j(f'tl.to("#cyto",{{scaleY:.86,scaleX:1.08,duration:.12,ease:"power2.in"}},{tc - .12:.3f});tl.to("#cyto",{{scaleY:1,scaleX:1,duration:.18,ease:"back.out(2)"}},{tc:.3f});'
        f'tl.to("#cytoPos",{{x:"+=1450",duration:{tEnd - tc:.3f},ease:"power1.in"}},{tc:.3f});'
        f'tl.fromTo("#cytoJump",{{y:0}},{{y:-70,duration:.16,ease:"power2.out",yoyo:true,repeat:5,immediateRender:false}},{tc:.3f});')
    S.sfx(tc, "boing", -12)
    S.recap(l[67][0] + .05, 1, "STRESS IS REAL — AND EVERYBODY HAS SOME", min(3.4, tF - l[67][0] + .2), y=170)
    S.tr_out("doors", label="THE COURT")
    S.captions({"exams": "#FFD166", "fortythree": "#FFD166", "twenty": "#FFD166", "personal": "#ff8a8a", "evidence": "#FFD166", "follow": "#8ce2d6"})
    return S


@scene
def s04():
    """THE COURT establishing (>= 6 s): doors open on the WIDE, location card, 0.7 s hold, then the camera pushes in while
    Cyto calls the game. Scoreboard drops on a spring, crowd bobs, Mito DRIBBLES (real bounce loop), THE ALARM struts in;
    on "the signal" a red signal line zips out of frame -> straight cut (match on action) to the 3D condos."""
    S = mk("s04", "court", "#5a1430", "court")
    for l in X.court("ct"): S.add(l)
    S.add(X.desk("dk"))
    S.over(X.scoreboard("sb"))
    S.tr_in("doors", label="THE COURT")
    S.location("THE COURT", "inside your body · game time", .45, 2.6)
    S.prop_in("#sb", .55, "drop", origin="50% 0%", sfx="clunk", amp=.7)
    S.j(f'document.querySelectorAll(".ctfan").forEach((f,i)=>tl.to(f,{{y:-10-(i%3)*4,duration:.22+(i%4)*.04,yoyo:true,repeat:{int(S.T / .22)},ease:"sine.inOut"}},(i%9)*.04));')
    S.parallax([("ctL1", .3), ("ctL2", .6)], 0, S.T, dx=-50)
    S.push(S.est + .1, S.T, 1.0, 1.06, 960, 560)
    S.talk_scale = 0                         # one long establishing move instead of speaker re-framing
    S.sfx(.3, "crowd", -12)
    S.cyto(360, 700, .5, z=29, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC,
           expr=[(S.w(13, "Welcome") - .05, 1.0, "hype")], x_expr=[(S.w(13, "stress"), 1.0, "determined")],
           points=[(S.w(13, "alarm") - .2, .8)])
    S.char("mito", "mt", 860, 300, .62, who="MITO", pose="ball", expr=[(.6, 1.2, "hype"), (S.w(13, "brain"), 1.4, "determined")],
           ball=[(0, S.T, "dribble")])
    for k in range(int(S.T / .5)): S.sfx(k * .5 + .22, "bounce", -16)
    S.add(f'<div style="position:absolute;left:0;top:0;z-index:18">' + K.wrap(X.alarm_guy("al", "idle"), "alW", 1300, 300, .78, z=18) + '</div>')
    S.j(f'tl.fromTo("#alW",{{x:900}},{{x:0,duration:.6,ease:"back.out(1.4)"}},{S.w(13, "alarm") - .6:.3f});tl.fromTo("#al",{{rotation:0}},{{rotation:4,duration:.2,yoyo:true,repeat:3,svgOrigin:"250 700"}},{S.w(13, "alarm") - .1:.3f});'
        f'tl.set("#alP_idle",{{opacity:0}},{S.w(13, "alarm"):.3f});tl.set("#alP_flex",{{opacity:1}},{S.w(13, "alarm"):.3f});'
        f'tl.fromTo("#alglow",{{opacity:.2}},{{opacity:.9,duration:.25,yoyo:true,repeat:{int(S.T / .25)},immediateRender:false}},0);')
    S.sfx(S.w(13, "alarm") - .5, "siren_short", -9)
    tz = S.w(13, "signal") - .1
    S.over(f'<div id="zip" class="clip" data-start="{tz:.3f}" data-duration="{S.T - tz:.3f}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:75"><svg width="1920" height="1080"><path id="zipP" d="M1500 360 C1300 600 1700 800 1450 1180" fill="none" stroke="#ff3b3b" stroke-width="22" stroke-linecap="round" stroke-dasharray="1100" stroke-dashoffset="1100"/></svg></div>')
    S.j(f'tl.to("#zipP",{{attr:{{"stroke-dashoffset":0}},duration:{S.T - tz:.3f},ease:"power2.in"}},{tz:.3f});')
    S.sfx(tz, "zap", -6)
    S.captions({"alarm": "#ff6b6b", "signal": "#ff6b6b"})
    return S


@scene
def s05():
    """3D (clean): the alarm signal runs down to the adrenal 'condos' on the kidneys; they fire hormone basketballs. Labels on panels."""
    S = mk("s05", "court", "#2b1640", "body")
    S.talk_scale = 0
    S.three3d("CON", "condos", 0, S.T, f"{{dur:{S.T:.3f},tFire:{S.w(13, 'pumping') - .2:.3f}}}", z=1)
    S.tr_in("cut")
    S.panel("lbA", S.w(13, "adrenal") - .1, S.w(13, "And", after=S.w(13, "adrenal")) - .15, "ADRENAL GLANDS", "= CONDOS ON YOUR KIDNEYS", "#ffa94d", 1000, 60, 860)
    S.panel("lbB", S.w(13, "adrenaline") - .1, S.w(13, "cortisol") - .05, "HORMONE", "ADRENALINE", "#ff8a8a", 1200, 60, 660)
    S.panel("lbC", S.w(13, "cortisol") - .05, S.T, "HORMONE", "CORTISOL", "#FFD166", 1200, 60, 660)
    S.drift = False
    S.add('<div id="pipbg" style="position:absolute;left:40px;top:540px;width:520px;height:340px;z-index:50;border-radius:24px;background:#20283a;box-shadow:0 14px 0 rgba(0,0,0,.35)"></div>')
    S.over('<div id="pip" style="position:absolute;left:40px;top:540px;width:520px;height:340px;z-index:50;border-radius:24px;border:8px solid #FAF4E8">'
           '<div style="position:absolute;left:16px;top:10px;font:24px InterBlack;color:#ff3b3b;z-index:3">● LIVE</div></div>')
    S.cyto(300, 800, .42, z=51, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC,
           expr=[(S.w(13, "condos") - .05, .8, "hype")], x_expr=[(S.w(13, "adrenaline") - .1, 1.0, "shocked")],
           points=[(S.w(13, "kidneys") - .2, .7)], looks=[(S.w(13, "adrenal"), 14, -10)])
    S.j('tl.set("#cytoLayer",{clipPath:"inset(540px 1360px 200px 40px round 24px)"},0);')
    S.j(f'tl.fromTo(["#pip","#pipbg","#cytoLayer"],{{x:-600}},{{x:0,duration:.35,ease:"back.out(1.5)"}},.15);')
    S.sfx(S.w(13, "pumping") - .2, "boing", -8); S.sfx(S.w(13, "adrenaline"), "boing", -8)
    S.tr_out("whip")
    S.captions({"adrenal": "#ffa94d", "condos": "#ffa94d", "adrenaline": "#ff8a8a", "cortisol": "#FFD166"})
    return S


@scene
def s06():
    """MITO vs THE ALARM - play-by-play (lines 14-17): Mito dribbles a real bounce loop (no slide), meters climb, the sugar
    pass lands in the paint. Straight cut ON ACTION into the dunk as Mito drives ("I'm HIM!")."""
    S = mk("s06", "court", "#5a1430", "court")
    for l in X.court("ct"): S.add(l)
    S.add(X.desk("dk")); S.over(X.scoreboard("sb"))
    S.alt_scale = 1.1
    S.j(f'document.querySelectorAll(".ctfan").forEach((f,i)=>tl.to(f,{{y:-10-(i%3)*4,duration:.22+(i%4)*.04,yoyo:true,repeat:{int(S.T / .22)},ease:"sine.inOut"}},(i%9)*.04));')
    l = {n: S.l(n) for n in range(14, 19)}
    S.j(f'tl.to("#sbhr",{{scaleX:.78,duration:.5,ease:"back.out(2)"}},{S.w(15, "UP") - .1:.3f});tl.to("#sbbr",{{scaleX:.8,duration:.5,ease:"back.out(2)"}},{S.w(16, "UP") - .1:.3f});')
    S.j(f'gsap.set("#sbheart",{{transformOrigin:"50% 50%"}});tl.fromTo("#sbheart",{{scale:1.25}},{{scale:1,duration:.5,repeat:{int(S.w(15, "Heart") / .5)},ease:"power2.out",immediateRender:false}},0);'
        f'tl.fromTo("#sbheart",{{scale:1.35}},{{scale:1,duration:.22,repeat:{int((S.T - S.w(15, "Heart")) / .22)},ease:"power2.out",immediateRender:false}},{S.w(15, "Heart"):.3f});')
    for n, w in ((15, "UP"), (16, "UP")):
        S.popup(f"up{n}", S.w(n, w) - .05, l[n][1] + .3, "", "↑ " + ("HEART RATE" if n == 15 else "BREATHING"), "#ff8a8a" if n == 15 else "#8ce2d6", 290, 270, 480)
        S.sfx(S.w(n, w) - .05, "buzzer", -12)
    S.cyto(360, 700, .5, z=29, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC, phone=False,
           expr=[(S.w(15, "Adrenaline"), .8, "hype"), (S.w(17, "Mito") - .1, .8, "hype")],
           points=[(S.w(17, "paint") - .3, .7)], looks=[(S.w(17, "sugar"), 14, -8)])
    tC = S.w(17, "paint")
    S.char("mito", "mt", 820, 290, .62, pose="ball", who="MITO", z=21,
           poses=[(l[14][0], "hype"), (l[15][0] - .1, "ball"), (tC - .05, "dunk"), (tC + .5, "ball")],
           expr=[(l[14][0], 1.5, "hype"), (S.w(16, "Breathing"), 1.0, "determined"), (tC, 1.0, "determined")],
           pops=[(l[14][0] + .1, 1)], ball=[(0, l[14][0], "dribble"), (l[14][0], l[15][0], "hidden"), (l[15][0], tC - .1, "dribble"), (tC - .1, tC + .5, "hidden"), (tC + .5, S.T, "dribble")])
    for k in range(int(S.T / .5)): S.sfx(k * .5 + .22, "bounce", -18)
    S.add(K.wrap(X.alarm_guy("al", "defend"), "alW", 1260, 300, .74, z=19))
    S.j(f'tl.fromTo("#alglow",{{opacity:.2}},{{opacity:.9,duration:.25,yoyo:true,repeat:{int(S.T / .25)},immediateRender:false}},0);'
        f'tl.fromTo("#alW",{{x:0}},{{x:-30,duration:.5,yoyo:true,repeat:{int(S.T / .5)},ease:"sine.inOut",immediateRender:false}},0);')
    # sugar pass: a sugar cube arcs from the blood stream into Mito's hands ON "paint"
    S.add(f'<div id="sugar" class="clip" data-start="{S.w(17, "sugar") - .2:.3f}" data-duration="{tC - S.w(17, "sugar") + .3:.3f}" style="position:absolute;left:0;top:0;width:120px;height:120px;z-index:22">'
          '<svg width="120" height="120"><rect x="10" y="10" width="100" height="100" rx="18" fill="#fff" stroke="#0c1622" stroke-width="7"/><text x="60" y="72" text-anchor="middle" font-family="InterBlack" font-size="26" fill="#0c1622">SUGAR</text></svg></div>')
    S.j(f'tl.fromTo("#sugar",{{x:620,y:470,rotation:0}},{{keyframes:[{{x:860,y:260,rotation:270,duration:{(tC - S.w(17, "sugar") + .1) / 2:.3f},ease:"power1.out"}},{{x:1040,y:430,rotation:540,duration:{(tC - S.w(17, "sugar") + .1) / 2:.3f},ease:"power1.in"}}]}},{S.w(17, "sugar") - .2:.3f});')
    S.sfx(tC, "catch", -6)
    S.captions({"up": "#ff8a8a", "sugar": "#FFD166", "paint": "#FFD166"})
    return S


@scene
def s06d():
    """THE DUNK (3.74 s, rebuilt as one animated sequence, low angle, cut on action both ends).
    approach (dribble, gravity arcs, squash/stretch, ball shadow) -> anticipation crouch (15 % squash, 7 f, arms back) ->
    launch (12 % stretch, parabolic arc, ball cocked back, legs tuck, free arm balances) -> hang (14 f near-still, played at
    40 % speed, face strains) -> slam (arm swings through, ball through the net, rim bends 12 f, net whips, backboard
    shudders, 6 px / 8 f shake, 2-frame white flash, crowd) -> landing (20 % squash, dust puff, ball bounces away,
    fist-pump). Camera: low-angle push in, pull back after the slam. Everything stays in frame with headroom."""
    S = mk("s06d", "court", "#5a1430", "court")
    S.talk_scale = 0; S.drift = False
    T = S.T; FY = 1000                                  # floor line (feet), low camera
    rnd = __import__("random").Random(4)
    fans = "".join(f'<circle class="dkfan" cx="{x + rnd.randint(-6, 6)}" cy="{y}" r="{rnd.randint(15, 21)}" fill="{rnd.choice(["#3fc1b0", "#7a5cc7", "#ffd166", "#f2c6da", "#ff9f5a", "#8ce2d6"])}" stroke="#0c1622" stroke-width="4"/>'
                   for y in (640, 690, 740, 790) for x in range(30, 1910, 48))
    S.add(f'<div id="dkset" class="fill" style="z-index:1"><svg width="1920" height="1080">'
          '<defs><linearGradient id="dksky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a0c22"/><stop offset=".6" stop-color="#8e2a44"/><stop offset="1" stop-color="#d0645e"/></linearGradient></defs>'
          '<rect width="1920" height="1080" fill="url(#dksky)"/>'
          + "".join(f'<rect x="{x}" y="0" width="70" height="620" fill="#2a0a1a" opacity=".35"/>' for x in range(60, 1920, 300))
          + "".join(f'<circle cx="{x}" cy="70" r="26" fill="#ffe9b0" opacity=".9"/><circle cx="{x}" cy="70" r="70" fill="#ffe9b0" opacity=".12"/>' for x in range(200, 1920, 380))
          + f'<rect x="0" y="{FY - 400}" width="1920" height="240" fill="#3a1a2e"/>' + f'<g id="dkfans" transform="translate(0 {FY - 1000})">{fans}</g>'
          + f'<rect x="0" y="{FY - 175}" width="1920" height="22" fill="#1b0a14"/>'
          + f'<path d="M-200 1080 L120 {FY - 170} L1800 {FY - 170} L2120 1080Z" fill="#2f6f8f" stroke="#0c1622" stroke-width="6"/>'
          + f'<path d="M-40 1080 L220 {FY - 150} L1700 {FY - 150} L1960 1080" fill="none" stroke="#f6f0e0" stroke-width="8"/>'
          + f'<path d="M1120 {FY - 150} Q1050 {FY - 40} 1460 {FY + 60}" fill="none" stroke="#ff7a59" stroke-width="10" opacity=".8"/>'
          + '</svg></div>')
    # hoop: pole + arm + backboard (shudders) + rim (bends about its bracket) + net (whips)
    RX, RY, RW = 1590, 360, 100           # rim centre / half-width
    S.add(f'<div id="dkhoop" class="fill" style="z-index:8"><svg width="1920" height="1080" style="overflow:visible">'
          f'<rect x="1790" y="250" width="30" height="{FY - 250}" fill="#555" stroke="#0c1622" stroke-width="6"/>'
          f'<rect x="1710" y="268" width="90" height="22" fill="#666" stroke="#0c1622" stroke-width="5"/>'
          f'<g id="dkBoard"><rect x="1490" y="130" width="230" height="236" rx="8" fill="#dff3ff" fill-opacity=".6" stroke="#fff" stroke-width="10"/>'
          f'<rect x="1490" y="130" width="230" height="236" rx="8" fill="none" stroke="#0c1622" stroke-width="4"/>'
          f'<rect x="1545" y="236" width="120" height="96" fill="none" stroke="#e63946" stroke-width="7"/></g>'
          f'<g id="dkNet"><path d="M{RX - RW + 6} {RY + 4} L{RX - 58} {RY + 112} L{RX + 58} {RY + 112} L{RX + RW - 6} {RY + 4} M{RX - 60} {RY + 6} L{RX - 30} {RY + 110} M{RX - 20} {RY + 8} L{RX} {RY + 112} M{RX + 20} {RY + 8} L{RX} {RY + 112} M{RX + 60} {RY + 6} L{RX + 30} {RY + 110}'
          f' M{RX - 80} {RY + 40} L{RX + 80} {RY + 40} M{RX - 68} {RY + 76} L{RX + 68} {RY + 76}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></g>'
          f'<g id="dkRim"><ellipse cx="{RX}" cy="{RY}" rx="{RW}" ry="17" fill="none" stroke="#0c1622" stroke-width="16"/><ellipse cx="{RX}" cy="{RY}" rx="{RW}" ry="17" fill="none" stroke="#ff6a00" stroke-width="10"/>'
          f'<rect x="{RX + RW - 6}" y="{RY - 9}" width="30" height="18" fill="#ff6a00" stroke="#0c1622" stroke-width="4"/></g></svg></div>')
    # scoreboard (top centre, clear of the CASE sticker)
    S.over('<div id="dksb" style="position:absolute;left:760px;top:26px;width:400px;height:92px;z-index:25;border-radius:18px;background:#151a24;border:6px solid #0c1622;box-shadow:0 8px 0 rgba(0,0,0,.35);text-align:center">'
           '<div style="font:22px InterBlack;color:#FFD166;letter-spacing:.08em;margin-top:6px">MITO vs THE ALARM</div>'
           '<div style="font:40px InterBlack;color:#FAF4E8">MITO <span id="dkpts" style="color:#ffb020">00</span></div></div>')
    # Mito (limb rig) on a procedural wrapper: feet-origin squash & stretch
    s0 = .78
    S.add(f'<div id="mtW" style="position:absolute;left:0;top:0;width:10px;height:10px;z-index:20"><div id="mtD" style="position:absolute;left:0;top:0;width:620px;height:760px;transform-origin:300px 690px">{RG.mito_html("mt")}</div></div>')
    S.add('<div id="dkBall" style="position:absolute;left:0;top:0;width:10px;height:10px;z-index:21"><svg width="10" height="10" style="overflow:visible">'
          f'<g id="dkBshO"><g id="dkBsh"><ellipse cx="0" cy="0" rx="46" ry="11" fill="#000"/></g></g><g id="dkB">{RG.ball_svg("dkb", 40)}</g></svg></div>')
    S.add('<div id="dkDust" style="position:absolute;left:0;top:0;width:10px;height:10px;z-index:22"><svg width="10" height="10" style="overflow:visible">'
          + "".join(f'<circle class="dkd" cx="{dx}" cy="0" r="{r}" fill="#e8dccb" opacity="0"/>' for dx, r in ((-70, 26), (-30, 34), (20, 30), (66, 24), (-100, 16), (100, 18))) + '</svg></div>')
    S.over('<div id="dkFlash" style="position:absolute;inset:0;z-index:90;background:#fff;opacity:0"></div>')
    ws = S.words_of("MITO")
    mouths = close_listener(K.mouth_track(DIALOGUE, ws, [(1.75, .9, "determined"), (2.3, .5, "determined"), (3.38, .36, "hype")], S.t0, S.t1), ws, "MITO", S.name, S.t0)
    S.mouth_tracks["MITO"] = mouths
    S.j(act_js3("mt", 36, 30, mouths=mouths, expr=[(1.72, .55, "determined"), (2.28, .5, "determined"), (3.36, .4, "hype")], T=T, bob=False, lid_n=-.05))
    S.cast["MITO"] = dict(x=700, y=700, kind="mito", idp="mt", s=s0)
    # ---------------- choreography (local s)
    tA1, tG1, tC1, tD1, tE1, tF1, tG2, tL1 = 1.62, 1.72, 1.95, 2.28, 2.74, 2.92, 3.18, 3.42
    X0, XG, XC, XApex, XLand = 300, 1020, 1060, 1330, 1300
    H = FY - (RY + 4) + (400 - 690) * s0       # jump height so the slam hand lands in the rim
    E = MO.ease

    def body(t):
        """feet world x, y, sx, sy"""
        if t < tA1:
            k = t / tA1; x = X0 + (XG - X0) * (k * .85 + .15 * E(k, "io")); per = .27
            ph = (t % per) / per; return x, FY - 10 * abs(math.sin(math.pi * ph)), 1, 1
        if t < tG1: return XG + (XC - XG) * (t - tA1) / (tG1 - tA1) * .5, FY, 1, 1
        if t < tC1:
            k = E((t - tG1) / (tC1 - tG1), "out"); return XG + (XC - XG) * (.5 + .5 * k), FY, 1 + .1 * k, 1 - .15 * k
        if t < tD1:
            k = (t - tC1) / (tD1 - tC1)
            st = math.sin(math.pi * min(1, k / .7)) if k < .7 else 0
            return XC + (XApex - XC) * E(k, "out"), FY - H * (1 - (1 - k) ** 2), 1 - .08 * st, 1 + .12 * st      # parabola (ease-out up)
        if t < tE1:
            k = (t - tD1) / (tE1 - tD1)                 # HANG: same arc, advanced at 40 % speed (slow-mo)
            return XApex + 14 * k, FY - H - 6 * math.sin(math.pi * k) * .4, 1, 1
        if t < tF1: return XApex + 14 + 6 * (t - tE1) / (tF1 - tE1), FY - H + 10 * E((t - tE1) / (tF1 - tE1), "in"), 1, 1
        if t < tG2:
            k = (t - tF1) / (tG2 - tF1); return XApex + 20 + (XLand - XApex - 20) * k, FY - H + 10 + (H - 10) * k * k, .95, 1.06    # ease-in down
        k = (t - tG2) / (tL1 - tG2)
        if k < 1:
            sq = (1 - E(min(1, k / .25), "out")) * .2 if k < .25 else -.06 * math.sin(math.pi * (k - .25) / .75)
            return XLand, FY, 1 + sq * .8, 1 - sq
        return XLand, FY - 6 * abs(math.sin(math.pi * (t - tL1) / .3)) * (t < tL1 + .3), 1, 1

    def arms_at(t, f):
        """canvas targets (P, hand_abs, shape) for L and R."""
        if t < tA1:
            per = .54; ph = (t % per) / per
            hy = 452 + 44 * E(ph / .16, "in") if ph < .16 else (496 - 44 * E((ph - .16) / .34, "out") if ph < .5 else 452)
            sw = math.sin(2 * math.pi * t / .54)
            return ((150 + 26 * sw, 520), None, "relaxed"), ((540, hy), None, "grip" if ph < .16 or ph > .9 else "relaxed")
        if t < tG1: return ((200, 430), -100, "grip"), ((420, 430), 100, "grip")
        if t < tC1: return ((190, 600), None, "grip"), ((410, 600), None, "grip")              # arms swing BACK/down
        if t < tE1: return ((40, 330), 120, "relaxed"), ((516, 206), 165, "grip")              # cocked back + balance arm
        if t < tF1:
            k = E((t - tE1) / (tF1 - tE1), "in"); return ((50, 340), 120, "relaxed"), ((516 + 64 * k, 206 + 224 * k), 165 - 150 * k, "grip" if k < .6 else "relaxed")
        if t < 3.36: return ((110, 470), None, "relaxed"), ((520, 470), None, "relaxed")
        return ((92, 262), 172, "fist"), ((508, 262), -172, "fist")                             # fist-pump

    mvf = {}

    def dunk(mv):
        n = mv.n
        aL = MO.Arm("mtaL", RG.M_SH["L"], RG.M_L1, RG.M_L2, RG.M_REST["L"], 300)
        aR = MO.Arm("mtaR", RG.M_SH["R"], RG.M_L1, RG.M_L2, RG.M_REST["R"], 300)
        ovL, ovR = [], []
        for f in range(n):
            L, Rr = arms_at(f / 30, f); ovL.append(L); ovR.append(Rr)
        rl = mv.arm(aL, ovL); rr = mv.arm(aR, ovR)
        bx_, by_, sx_, sy_, legL, legR, mvx, mvy = [], [], [], [], [], [], [], []
        for f in range(n):
            t = f / 30; x, y, sx, sy = body(t)
            mvx.append(x - 300); mvy.append(y - 690); bx_.append(s0 * sx); by_.append(s0 * sy)
            if t < tA1:
                ph = math.sin(2 * math.pi * t / .54); legL.append(24 * ph); legR.append(-24 * ph)
            elif tC1 <= t < tF1 + .1:
                k = min(1, (t - tC1) / .12); legL.append(-26 * k); legR.append(18 * k)          # legs tuck
            elif t < tG2:
                legL.append(-8); legR.append(6)
            else: legL.append(0); legR.append(0)
        mv.css("mtD", mvx, mvy, 0, bx_, by_)
        mv.rot("mtlegL", *RG.M_HIP["L"], legL); mv.rot("mtlegR", *RG.M_HIP["R"], legR)
        # eyes: on the rim the whole time; no blink in the air
        tg = [(.75, -.35 if f / 30 > tC1 else -.1) for f in range(n)]
        px, py, fx, fy, lid = MO.eye_track(n, 30, tg, [.9, 3.5], -1.4 * 36, .3 * 36, 1.1 * 36)
        mv.tr("mtpgL", px, py); mv.tr("mtpgR", px, py); mv.tr("mtfT", fx, fy); mv.tr("mtbkL", 0, lid); mv.tr("mtbkR", 0, lid)
        # ball: world coords. hand world = feet + (hand - (300,690)) * scale
        def hw(f):
            x, y, sx, sy = body(f / 30); h = rr["hand"][f]
            return x + (h[0] - 300) * s0 * sx, y + (h[1] - 690) * s0 * sy
        BR = 40; floorB = FY - BR
        bx, by, bsx, bsy, brot, shx, shs, sho = [], [], [], [], [], [], [], []
        rel = None; spin = 0
        for f in range(n):
            t = f / 30; habs = rr["A"][f] + rr["B"][f] + rr["H"][f]; d = MO.dvec(habs); hx, hy = hw(f)
            a = b = 1.0
            if t < tA1:
                per = .54; ph = (t % per) / per; top = hy + 44 * s0 + BR
                x = hx + 6
                if ph < .16: y = top
                elif ph < .44:
                    k = (ph - .16) / .28; y = top + (floorB - top) * k * k; b = 1 + .12 * k; a = 1 - .08 * k
                elif ph < .52: y = floorB + BR * .24; a, b = 1.24, .74
                else:
                    k = (ph - .52) / .48; y = floorB - (floorB - top) * (1 - (1 - k) ** 2); b = 1 + .12 * (1 - k); a = 1 - .08 * (1 - k)
                spin += 10
            elif t < 2.86:
                if t < tG1:
                    L_ = rl["hand"][f]; x0, y0, sx0, sy0 = body(t)
                    lx, ly = x0 + (L_[0] - 300) * s0, y0 + (L_[1] - 690) * s0
                    x, y = (hx + lx) / 2, (hy + ly) / 2 + 22
                else:
                    x, y = hx + d[0] * (18 + BR), hy + d[1] * (18 + BR)
                spin += 2
            else:
                if rel is None: rel = (x, y, t)
                tt = t - rel[2]; g = 2600; vy0 = 700
                y = rel[1] + vy0 * tt + .5 * g * tt * tt; x = rel[0] - 40 * tt
                if y > floorB:                                         # bounces away to the left, losing height
                    t_hit = (-vy0 + math.sqrt(vy0 ** 2 + 2 * g * (floorB - rel[1]))) / g
                    tb = tt - t_hit; v = (vy0 + g * t_hit) * .5; per_b = 2 * v / g
                    i_b = 0
                    while tb > per_b and i_b < 4: tb -= per_b; v *= .5; per_b = 2 * v / g; i_b += 1
                    y = floorB - (v * tb - .5 * g * tb * tb)
                    x = rel[0] - 40 * t_hit - 380 * (tt - t_hit)
                    if tb < .045: a, b = 1.2, .78
                spin -= 9
            bx.append(x); by.append(y); bsx.append(a); bsy.append(b); brot.append(spin)
            hgt = max(0, floorB - y); k = max(0, 1 - hgt / 420)
            shx.append(x); shs.append(.35 + .65 * k); sho.append(.1 + .3 * k)
        mv.svgm("dkB", 0, 0, bx, by, 0, bsx, bsy); mv.rot("dkbseam", 0, 0, brot)
        mv.svgm("dkBsh", 0, 0, shx, FY + 2, 0, shs, shs); mv.op("dkBshO", sho)
        # rim bends + 12-frame damped shake, net whip, backboard shudder
        tS = 2.86; rim, net_sy, net_sk, brd = [], [], [], []
        for f in range(n):
            t = f / 30; u = t - tS
            if 0 <= u < .42:
                dmp = math.exp(-u * 9); rim.append(14 * dmp * math.cos(2 * math.pi * u / .14))
                net_sy.append(1 + .35 * dmp * abs(math.cos(2 * math.pi * u / .2))); net_sk.append(16 * dmp * math.sin(2 * math.pi * u / .18))
                brd.append(5 * dmp * math.sin(2 * math.pi * u / .07))
            else: rim.append(0); net_sy.append(1); net_sk.append(0); brd.append(0)
        mv.svgm("dkRim", RX + RW + 10, RY, 0, 0, rim, 1, 1)
        mv.svgm("dkNet", RX, RY, net_sk, 0, 0, 1, net_sy)
        mv.tr("dkBoard", brd, 0)
        # dust puff on landing
        dx_ = [XLand] * n
        mv.ch["dkDust"] = ["c", XLand, FY - 6, 0, 1, 1]
        mvf.update(rl=rl, rr=rr)
    S.mv_extra.append(dunk)
    S.j('document.querySelectorAll(".dkd").forEach((e,i)=>tl.fromTo(e,{opacity:0,scale:.3,x:0,y:0},{opacity:.85,scale:1.3,x:(i%2?1:-1)*(30+i*12),y:-26-(i%3)*10,duration:.3,ease:"power2.out",immediateRender:false},' + f'{tG2 - .02:.3f}));'
        'document.querySelectorAll(".dkd").forEach((e,i)=>tl.to(e,{opacity:0,duration:.25},' + f'{tG2 + .3:.3f}));')
    S.j(f'document.querySelectorAll(".dkfan").forEach((f,i)=>tl.to(f,{{y:-8-(i%3)*3,duration:.24+(i%4)*.04,yoyo:true,repeat:{int(T / .24)},ease:"sine.inOut"}},(i%9)*.03));'
        f'tl.to(".dkfan",{{y:-44,duration:.16,yoyo:true,repeat:5,ease:"power2.out"}},{2.9:.3f});')
    # camera: low-angle push in on the approach, punch at the rim, pull back after the slam
    S.j(f'gsap.set("#cam",{{transformOrigin:"1300px 300px"}});tl.fromTo("#cam",{{scale:1}},{{scale:1.08,duration:{tE1:.3f},ease:"sine.inOut",immediateRender:false}},0);'
        f'tl.to("#cam",{{scale:1,duration:.65,ease:"power2.inOut"}},{tF1 + .05:.3f});')
    S.shake(2.86, 8 / 30, 6)
    S.j('tl.set("#dkFlash",{opacity:.85},2.86);tl.set("#dkFlash",{opacity:.4},2.893);tl.set("#dkFlash",{opacity:0},2.926);'
        'tl.set("#dkpts",{innerHTML:"02"},2.9);tl.fromTo("#dkpts",{scale:1.8},{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false},2.9);')
    for k in range(3): S.sfx(k * .54 + .25, "bounce", -12)
    S.sfx(1.68, "catch", -8); S.sfx(1.93, "kick", -12); S.sfx(2.3, "whoosh", -12)
    S.sfx(2.86, "slam", -2); S.sfx(2.86, "clang", -6); S.sfx(2.88, "rimshake", -8); S.sfx(2.9, "netwhip", -8); S.sfx(2.92, "crowd", -2)
    S.sfx(tG2, "dust", -8); S.sfx(3.3, "bounce", -10); S.sfx(3.55, "bounce", -14)
    S.captions({"him": "#FFD166"})
    return S


@scene
def s06b():
    """After the slam (cut on the landing): fight-or-run commentary, the bear gag, the alarm keeps subbing back in.
    N2 bridge: Neutro WALKS INTO the court (in frame) - "That was one bad day. Now make it a month." - CLUE 2 recap,
    doors close on NEXT STOP: THE BENCH."""
    S = mk("s06b", "court", "#5a1430", "court")
    for l in X.court("ct"): S.add(l)
    S.add(X.desk("dk")); S.over(X.scoreboard("sb"))
    S.alt_scale = 1.1
    S.j(f'document.querySelectorAll(".ctfan").forEach((f,i)=>tl.to(f,{{y:-10-(i%3)*4,duration:.22+(i%4)*.04,yoyo:true,repeat:{int(S.T / .22)},ease:"sine.inOut"}},(i%9)*.04));'
        f'tl.set("#sbhr",{{scaleX:.78}},0);tl.set("#sbbr",{{scaleX:.8}},0);')
    l = {n: S.l(n) for n in list(range(19, 26)) + [68]}
    sb0, sb1 = S.b("subbed"); nw0, nw1 = S.b("n2walk")
    S.cyto(360, 700, .5, z=29, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC, phone=True,
           expr=[(l[25][0], 1.0, "skeptic")],
           x_expr=[(S.w(19, "built"), 1.1, "determined"), (l[21][0], 1.2, "deadpan"), (S.w(23, "Again"), 1.6, "exhausted"), (l[68][0] + .3, 1.6, "worried")],
           points=[(l[25][0], .9)], shrugs=[(S.w(21, "group"), .7)])
    S.char("mito", "mt", 820, 290, .62, pose="hype", who="MITO", z=21,
           poses=[(.9, "idle"), (l[20][0], "point"), (l[22][0], "shrug"), (l[23][0] + 1.0, "ball"), (l[24][0], "shrug"), (l[25][0], "idle")],
           expr=[(0, .9, "hype"), (l[20][0], 1.0, "worried"), (l[22][0] - .3, 1.3, "sideeye"), (sb0, 1.2, "shocked"), (l[24][0], 1.4, "shocked"), (l[25][0], 1.2, "exhausted")],
           ball=[(l[23][0] + 1.0, l[24][0], "dribble")])
    S.add(K.wrap(X.alarm_guy("al", "defend"), "alW", 1260, 300, .74, z=19))
    S.add(K.wrap(X.alarm_guy("al2", "defend"), "al2W", 1470, 330, .7, z=18))
    S.add(K.wrap(X.alarm_guy("al3", "flex"), "al3W", 1000, 340, .68, z=17))
    S.j(f'tl.fromTo(["#alglow","#al2glow","#al3glow"],{{opacity:.2}},{{opacity:.9,duration:.25,yoyo:true,repeat:{int(S.T / .25)},immediateRender:false}},0);'
        f'tl.set("#alW",{{x:900}},0);tl.to("#alW",{{x:0,duration:.6,ease:"power3.out"}},{sb0:.3f});'
        f'tl.set(["#al2W","#al3W"],{{y:-120,opacity:0}},0);tl.to("#al2W",{{y:0,opacity:1,duration:.35,ease:"bounce.out"}},{S.w(23, "Again") - .1:.3f});tl.to("#al3W",{{y:0,opacity:1,duration:.35,ease:"bounce.out"}},{S.w(23, "again", after=S.w(23, "Again") + .1) - .1:.3f});')
    for t in (sb0, S.w(23, "Again") - .1, S.w(23, "again", after=S.w(23, "Again") + .1) - .1):
        S.sfx(t, "siren_short", -10); S.sfx(t, "buzzer", -12)
    for t in (S.w(23, "phone") - .1, S.w(23, "Again") - .3, S.w(23, "again", after=S.w(23, "Again") + .1) - .3):
        buzz(S, t, .3)
    S.popup("sub", sb0 + .05, sb1 + .6, "SUBSTITUTION", "THE ALARM (AGAIN)", "#ff8a8a", 290, 260, 480)
    S.j(f'tl.to("#mtW",{{x:-260,duration:.3,ease:"power3.in"}},{sb0 + .1:.3f});tl.to("#mtW",{{x:0,duration:.45,ease:"power2.out"}},{sb1 + .1:.3f});')
    bubble(S, "bear", S.w(19, "bear") - .1, l[21][1] + .2, BEAR, 520, 270)
    S.over(f'<div id="bearX" class="pop clip" data-start="{S.w(21, "no"):.3f}" data-duration="{l[21][1] - S.w(21, "no") + .2:.3f}" style="left:600px;top:310px;font:220px/1 InterBlack;color:#e63946;-webkit-text-stroke:6px #0c1622">X</div>')
    S.j(f'tl.fromTo("#bearX",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:.18,ease:"power4.in"}},{S.w(21, "no"):.3f});')
    S.sfx(S.w(19, "bear"), "roar", -10)
    # N2: Neutro walks in from the right, IN FRAME, stops between Mito and the Alarm guys, delivers the bridge line
    S.char("neutro", "nt", 1980, 310, .66, pose="idle", who="NEUTRO", z=23,
           poses=[(l[68][0] + .1, "point"), (S.w(68, "month"), "idle")],
           expr=[(nw0, 1.2, "determined"), (S.w(68, "month") - .1, 1.2, "deadpan")],
           walks=[(nw0 - .5, l[68][0] + .05, -560)], nods=[S.w(68, "month")])
    S.cast["NEUTRO"]["x"] -= 560
    S.j(f'tl.to(["#alW","#al2W","#al3W"],{{x:"+=420",opacity:0,duration:.5,ease:"power2.in"}},{nw0 - .4:.3f});')
    S.recap(l[68][0] + .1, 2, "STRESS FLIPS THE ALARM: ADRENALINE + CORTISOL", min(3.6, l[68][1] - l[68][0] + .2), y=270)
    S.tr_out("doors", label="THE BENCH")
    S.captions({"him": "#FFD166", "bear": "#c9965f", "groupchat": "#8ce2d6", "again": "#ff8a8a", "month": "#FFD166"})
    return S


@scene
def s07():
    """IT DRAGS ON - countdown sign drops in, Mito gassed on the bench, the cortisol gag (card top-left, clear of faces), Neutro vs. a crumb."""
    S = mk("s07", "moody", "#2a1030", "court_low")
    for l in X.court("ct"): S.add(l)
    S.add('<div class="fill" style="z-index:5;background:linear-gradient(rgba(20,10,60,.55),rgba(10,5,30,.65))"></div>')
    S.add(X.layer("bench", BENCH, 6))
    S.tr_in("doors", label="THE BENCH")
    S.location("THE BENCH", "weeks of stress later", .45, 2.5)
    S.j(f'document.querySelectorAll(".ctfan").forEach((f,i)=>tl.to(f,{{y:-6-(i%3)*3,duration:.3+(i%4)*.05,yoyo:true,repeat:{int(S.T / .3)},ease:"sine.inOut"}},(i%9)*.05));')
    flipsign(S, "cd", 1.1, "12 DAYS TILL BREAK", "10 DAYS TILL BREAK", 650, 70)
    S.prop_in("#cd", .55, "drop", origin="50% 0%", sfx="clunk", amp=.6)
    S.parallax([("ctL1", .2), ("ctL2", .4), ("bench", .5)], 0, S.T, dx=-60)
    l = {n: S.l(n) for n in range(26, 33)}
    cb0, cb1 = S.b("crumb"); bn0, _ = S.b("bench")
    S.cyto(470, 720, .58, expr=[(S.w(26, "weird") - .2, 1.0, "squint"), (S.w(28, "stop"), 1.0, "sad"), (l[30][0], 1.0, "skeptic")],
           x_expr=[(l[26][0] + .2, 1.3, "smug"), (S.w(28, "Cortisol"), 1.3, "determined"), (S.w(28, "inflammation"), 1.5, "worried"), (cb0, 1.0, "shocked"), (l[32][0] + .1, 1.6, "sideeye")],
           points=[(S.w(28, "Carnegie"), .7), (l[30][0] + .1, .9)], shrugs=[(S.w(26, "days") - .1, .8)], sips=[(l[27][1] + .1, 1.1)],
           tilts=[(S.w(26, "Useful"), .6, 6)])
    S.char("mito", "mt", 1270, 230, .66, pose="slump", gassed=True, who="MITO", z=21,
           expr=[(0, S.T, "exhausted")], shut_at=[(l[27][1] + .6, 2.0)], nods=[l[27][0] + .2], bob=True)
    S.j(f'tl.fromTo("#mtsweat",{{y:0,opacity:1}},{{y:30,opacity:0,duration:1.2,repeat:{int(S.T / 1.2)},ease:"power1.in",immediateRender:false}},0);')
    # cortisol gag card: top-left reserved zone (never over Mito / Cyto), drops in, pinned for <= 3 s per beat
    a0 = S.w(28, "Cortisol") - .1; a1 = min(S.w(28, "inflammation") + 1.0, a0 + 6.0)
    S.over(f'<div id="cg" class="pop clip" data-start="{a0:.3f}" data-duration="{a1 - a0:.3f}" style="left:40px;top:180px;width:900px;height:330px;z-index:50;border-radius:28px;background:#FAF4E8;border:7px solid #0c1622;box-shadow:0 14px 0 rgba(0,0,0,.35);transform:scale(.88);transform-origin:0 0">'
           f'<svg width="900" height="330"><g transform="translate(40 110)">{CORT}</g>'
           f'<g id="cgtxt"><rect x="250" y="40" width="300" height="70" rx="20" fill="#fff" stroke="#0c1622" stroke-width="5"/><text x="400" y="86" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">AIGHT, CALM DOWN</text></g>'
           f'<g transform="translate(600 90)">{IMM}</g><g id="cgfl" opacity="0"><g transform="translate(330 170)">{FLAME}</g><g transform="translate(420 190) scale(.8)">{FLAME}</g><g transform="translate(500 170)">{FLAME}</g></g>'
           f'<text x="450" y="315" text-anchor="middle" font-family="InterBlack" font-size="28" fill="#e63946" id="cglab" opacity="0">INFLAMMATION</text></svg></div>')
    S.j(f'tl.fromTo("#cg",{{y:-600}},{{y:0,duration:.4,ease:"elastic.out(1,.5)"}},{a0:.3f});tl.set("#hph",{{opacity:1}},{S.w(28, "stop"):.3f});'
        f'tl.fromTo("#hph",{{y:-60}},{{y:0,duration:.25,ease:"bounce.out"}},{S.w(28, "stop"):.3f});tl.set("#cgtxt",{{opacity:.25}},{S.w(28, "listening"):.3f});'
        f'tl.set(["#cgfl","#cglab"],{{opacity:1}},{S.w(28, "inflammation"):.3f});tl.fromTo("#cgfl",{{scaleY:.9,transformOrigin:"50% 100%"}},{{scaleY:1.12,duration:.18,yoyo:true,repeat:12,immediateRender:false}},{S.w(28, "inflammation"):.3f});'
        f'tl.to("#cg",{{y:-700,rotation:-8,duration:.3,ease:"power3.in"}},{a1 - .3:.3f});')
    S.sfx(a0 + .1, "clunk", -8); S.sfx(a1 - .3, "whoosh", -10)
    S.over(f'<div id="fl2" class="pop clip" data-start="{S.w(28, "inflammation"):.3f}" data-duration="{l[28][1] - S.w(28, "inflammation") + .4:.3f}" style="left:1300px;top:780px;z-index:23"><svg width="300" height="130" viewBox="0 0 300 130">'
           f'<g transform="translate(0 10)">{FLAME}</g><g transform="translate(100 20) scale(.8)">{FLAME}</g><g transform="translate(190 10)">{FLAME}</g></svg></div>')
    S.j(f'tl.fromTo("#fl2",{{scaleY:.85,transformOrigin:"50% 100%"}},{{scaleY:1.1,duration:.16,yoyo:true,repeat:{int((l[28][1] - S.w(28, "inflammation") + .4) / .16)},immediateRender:false}},{S.w(28, "inflammation"):.3f});')
    src_chip(S, "src1", S.w(28, "Carnegie") - .1, l[28][1], "COHEN ET AL. · PNAS 2012", right=True)
    S.sfx(S.w(28, "stop"), "pop", -8)
    # Neutro: jittery, spins at the crumb, radios for backup (consistent scale; gentle push, no giant zoom)
    S.add('<div id="crumb" style="position:absolute;left:990px;top:840px;z-index:7"><svg width="70" height="50"><path d="M6 44 L20 10 L52 6 L64 38Z" fill="#d9a35b" stroke="#0c1622" stroke-width="4"/></svg></div>')
    S.char("neutro", "nt", 860, 330, .66, pose="idle", who="NEUTRO", z=22,
           poses=[(cb0 + .4, "radio"), (l[31][0], "point"), (l[32][0] + .4, "cross")], looks=[(cb0 - .1, 0, .9, 1.4)],
           expr=[(cb0, l[29][1] - cb0 + .2, "determined"), (l[31][0], 1.3, "sideeye"), (l[32][0], 1.8, "deadpan")])
    S.j(f'tl.set("#ntW",{{x:1200}},0);tl.to("#ntW",{{x:0,duration:.4,ease:"power3.out"}},{cb0 - .45:.3f});'
        f'tl.to("#nt",{{scaleX:-1,duration:.08,svgOrigin:"300 650",yoyo:true,repeat:3}},{cb0:.3f});'
        f'tl.to("#ntW",{{x:60,duration:.07,yoyo:true,repeat:7}},{cb0 + .1:.3f});')
    S.sfx(cb0 - .4, "whoosh", -10); S.sfx(cb0 + .45, "radio", -6)
    S.captions({"cortisol": "#FFD166", "carnegie": "#8ce2d6", "mellon": "#8ce2d6", "cooked": "#ff8a8a", "crumb": "#d9a35b"})
    return S


@scene
def s08():
    """3D (clean: tunnel + lasers + door only): Rhino's heist at the nose front door. Cyto's VO lands during the heist."""
    S = mk("s08", "heist", "#2a0a14", "body")
    S.talk_scale = 0
    S.three3d("LAS", "lasers", 0, S.T, f"{{dur:{S.T:.3f}}}", z=1)
    S.tr_in("cut")
    S.panel("fd", .3, S.T - .2, "MEANWHILE · THE FRONT DOOR", "YOUR NOSE", "#ff8a8a", 60, 60, 760)
    S.char("rhino", "rh", -380, 520, .95, pose="sneak", z=30, expr=[(0, S.T, "smug")], blinks=[],
           poses=[(.8, "duck"), (1.8, "spread"), (2.6, "sneak"), (3.3, "duck")])
    S.j(f'tl.to("#rhW",{{x:1000,duration:{S.T - .5:.3f},ease:"sine.inOut"}},.1);tl.to("#rh",{{y:-20,duration:.3,yoyo:true,repeat:{int(S.T / .3)},ease:"sine.inOut"}},0);'
        f'tl.to("#rh",{{rotation:360,duration:.6,svgOrigin:"200 260",ease:"power2.inOut"}},1.9);tl.set("#rh",{{rotation:0}},2.55);')
    S.sfx(.2, "tiptoe", -8); S.sfx(1.9, "whoosh", -10); S.sfx(S.T - 1.0, "gulp", -8)
    S.captions({"officer": "#ff8a8a"})
    return S


@scene
def s08b():
    """C-bridge (back on the bench, straight cut from the heist): Cyto turns to Neutro - "Wait. Hold up. Has this happened
    before?" - Neutro nods slowly; the doors close on NEXT STOP: COLD CASE 1991, so the noir scene ANSWERS a question."""
    S = mk("s08b", "moody", "#2a1030", "court_low")
    for l in X.court("ct"): S.add(l)
    S.add('<div class="fill" style="z-index:5;background:linear-gradient(rgba(20,10,60,.55),rgba(10,5,30,.65))"></div>')
    S.add(X.layer("bench", BENCH, 6))
    l69 = S.l(69)
    S.cyto(470, 720, .58, expr=[(S.w(69, "Wait") - .05, .7, "shock")], x_expr=[(S.w(69, "Has"), 1.2, "worried")],
           points=[(S.w(69, "before") - .25, .8)], tilts=[(S.w(69, "Has"), .6, 6)])
    S.char("neutro", "nt", 860, 330, .66, pose="cross", who="NEUTRO", z=22, poses=[(S.w(69, "before") + .2, "notepad")],
           expr=[(S.w(69, "Wait"), .8, "sideeye"), (S.w(69, "before"), 1.4, "determined")], nods=[S.w(69, "before") + .3])
    S.char("mito", "mt", 1270, 230, .66, pose="slump", gassed=True, who="MITO", z=21, expr=[(0, S.T, "exhausted")])
    S.tr_out("doors", label="COLD CASE: 1991")
    S.captions({"before": "#FFD166"})
    return S


@scene
def s09():
    """COLD CASE: 1991 - film noir kept B&W to the end (I6). Real Distillery brick through the window (cropped, no signage).
    Title on its own dark band. Animated reenactment. Neutro points at a pull-down wall chart that fills while Cyto reacts."""
    S = mk("s09", "noir", "#111", "rain")
    for l in X.noir("nr"): S.add(l)
    S.tr_in("doors", label="COLD CASE: 1991")
    nb0, nb1 = S.b("noir"); re0, re1 = S.b("reenact"); si0, si1 = S.b("silence"); sm0, sm1 = S.b("smirk")
    l = {n: S.l(n) for n in range(33, 43)}
    S.j('tl.set("#cam",{filter:"grayscale(1) contrast(1.2) brightness(.96)"},0);')
    S.over(f'<div id="grain" class="static clip" data-start="0" data-duration="{S.T:.3f}" style="position:absolute;inset:0;z-index:60;opacity:.07;pointer-events:none"></div>')
    S.j(f'tl.fromTo("#grain",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"53px 29px",duration:.05,repeat:{int(S.T / .05)},ease:"steps(1)",immediateRender:false}},0);')
    S.j(f'tl.fromTo("#nrrain",{{y:-60}},{{y:0,duration:.35,repeat:{int(S.T / .35)},ease:"none",immediateRender:false}},0);')
    S.j(f'gsap.set("#nrlamp",{{svgOrigin:"1540 610"}});tl.fromTo("#nrlamp",{{rotation:-14,y:-200}},{{rotation:0,y:0,duration:.6,ease:"elastic.out(1,.4)",immediateRender:true}},.05);'
        f'tl.fromTo("#nrlamp",{{opacity:1}},{{opacity:.6,duration:.06,yoyo:true,repeat:5,immediateRender:false}},.7);')
    S.sfx(.45, "clunk", -10); S.sfx(0, "sax", -5)
    S.case_from = l[33][1] + .35
    S.est = .95
    S.over(f'<div id="cct" class="clip" data-start="{.05:.3f}" data-duration="{l[33][1] + .3:.3f}" style="position:absolute;left:0;right:0;top:28px;height:150px;z-index:70;background:linear-gradient(rgba(0,0,0,.9),rgba(0,0,0,.75));text-align:center;font:104px/150px InterBlack;color:#f0f0f0">COLD CASE: 1991</div>')
    S.j(f'tl.fromTo("#cct",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.8,ease:"steps(15)"}},.05);tl.to("#cct",{{opacity:0,duration:.2}},{l[33][1] + .05:.3f});')
    S.sfx(.05, "typewriter", -8)
    S.char("neutro", "nt", 760, 210, .78, pose="notepad", who="NEUTRO", z=20, trench=True,
           poses=[(l[34][0], "idle"), (l[38][0] - .2, "point"), (si0, "idle"), (l[41][0], "cross")],
           expr=[(0, 1.4, "deadpan"), (l[36][0], 1.0, "deadpan"), (l[38][0], 1.4, "determined"), (l[41][0], 1.3, "smug")],
           nods=[l[33][1] - .2, l[41][0] + .2])
    S.cyto(360, 760, .66, z=35, expr=[(l[35][0] - .05, .9, "shock"), (S.w(38, "ninety"), .8, "shock"), (si0 + .1, si1 - si0 + l[40][1] - l[40][0] + .2, "shock")],
           x_expr=[(l[34][0] + 1, 1.8, "sideeye"), (S.w(39, "forty") - .1, 1.3, "worried"), (l[42][0] + .1, 2.0, "determined"), (sm0, .9, "worried")],
           tilts=[(l[42][0] + 1.5, .7, 6)], shrugs=[(S.w(42, "Yeah"), .7)])
    S.j(f'tl.fromTo("#nrfile",{{y:0}},{{y:-14,duration:.12,yoyo:true,repeat:1,immediateRender:false}},{l[33][0]:.3f});')
    src_chip(S, "src2", S.w(34, "Scientists"), l[37][1], "COHEN, TYRRELL & SMITH · NEJM 1991", 40, 36)
    # REENACTMENT (animated): droppers drip, tiny Rhinos hop into noses, volunteers sneeze
    ra = S.w(34, "dripped") - .2; rb = l[37][1] + .2
    vols = "".join(f'<g class="vol" transform="translate({x} 560)"><g class="volB">{VOL(0)}</g></g>' for x in (340, 740, 1140, 1540)).replace('translate(0 560)', 'translate(0 0)')
    drops = "".join(f'<circle class="drp" cx="{x + 122}" cy="390" r="12" fill="#444" stroke="#000" stroke-width="3"/>' for x in (340, 740, 1140, 1540))
    hops = "".join(f'<g class="trh" transform="translate({x - 160} 640)">{TINYRH}</g>' for x in (340, 740, 1140, 1540))
    sneeze = "".join(f'<text class="snz" x="{x + 60}" y="610" font-family="InterBlack" font-size="44" fill="#111" opacity="0">ACHOO</text>' for x in (340, 740, 1140, 1540))
    S.hide_txt(ra, rb)
    S.over(f'<div id="reel" class="clip" data-start="{ra:.3f}" data-duration="{rb - ra:.3f}" style="position:absolute;inset:0;z-index:45">'
           + reel("".join(SCI(x) for x in (340, 740, 1140, 1540)) + vols + drops + hops + sneeze
                  + '<text x="1820" y="140" text-anchor="end" font-family="InterBlack" font-size="34" fill="#111">REENACTMENT</text>') + '</div>')
    S.j(f'tl.fromTo("#reel",{{opacity:0,scale:1.04}},{{opacity:1,scale:1,duration:.18,ease:"power3.out"}},{ra:.3f});tl.to("#reel",{{opacity:0,scale:.96,duration:.2}},{rb - .2:.3f});'
        f'document.querySelectorAll("#reel .drp").forEach((e,i)=>tl.fromTo(e,{{y:0,opacity:1}},{{y:270,opacity:.3,duration:.45,ease:"power2.in",repeat:4,repeatDelay:.35,immediateRender:false}},{ra + .3:.3f}+i*.12));'
        f'document.querySelectorAll("#reel .trh").forEach((e,i)=>tl.fromTo(e,{{x:0,y:0,opacity:1,scale:1}},{{keyframes:[{{x:80,y:-120,duration:.25,ease:"power2.out"}},{{x:160,y:-40,scale:.4,duration:.25,ease:"power2.in"}},{{opacity:0,duration:.05}}],immediateRender:false}},{re0 + .1:.3f}+i*.2));'
        f'document.querySelectorAll("#reel .volB").forEach((e,i)=>tl.fromTo(e,{{scaleY:1,scaleX:1}},{{keyframes:[{{scaleY:.85,scaleX:1.12,duration:.1}},{{scaleY:1.1,scaleX:.92,duration:.1}},{{scaleY:1,scaleX:1,duration:.15}}],immediateRender:false}},{re1 + .2:.3f}+i*.25));'
        f'document.querySelectorAll("#reel .snz").forEach((e,i)=>tl.fromTo(e,{{opacity:0,y:0}},{{opacity:1,y:-30,duration:.2,yoyo:true,repeat:1,repeatDelay:.3,immediateRender:false}},{re1 + .2:.3f}+i*.25));')
    for i in range(4): S.sfx(ra + .3 + i * .12, "drip", -10); S.sfx(re1 + .2 + i * .25, "achoo_small", -14)
    for i in range(4): S.sfx(re0 + .1 + i * .2, "boing", -16)
    # the NUMBERS: a chart rolls down over the window like a projector screen; Neutro points, bars fill, Cyto reacts
    b0 = l[38][0] - .35; b1 = si0 + .2
    def bar(id_, lab, v, col, y):
        return (f'<div style="position:absolute;left:30px;top:{y}px;font:32px InterBlack;color:#111">{lab}</div>'
                f'<div style="position:absolute;left:30px;top:{y + 42}px;width:390px;height:44px;background:#bbb;border:4px solid #111"><div id="{id_}" style="width:{v}%;height:100%;background:{col};transform-origin:0 50%;transform:scaleX(0)"></div></div>'
                f'<div id="{id_}n" style="position:absolute;left:440px;top:{y + 40}px;font:42px InterBlack;color:#111;opacity:0">{v}%</div>')
    S.add(f'<div id="ev" class="clip" data-start="{b0:.3f}" data-duration="{b1 - b0:.3f}" style="position:absolute;left:1240px;top:150px;width:540px;height:560px;z-index:8;background:#efefef;border:8px solid #111;box-shadow:0 12px 0 rgba(0,0,0,.4);transform-origin:50% 0">'
          f'<div style="position:absolute;left:30px;top:14px;font:30px InterBlack;color:#555">INFECTED</div>'
          + bar("evA", "LOW STRESS", 74, "#666", 54) + bar("evB", "HIGH STRESS", 90, "#111", 150)
          + '<div style="position:absolute;left:30px;top:270px;font:30px InterBlack;color:#555">ACTUAL COLDS</div>'
          + bar("evC", "LOW STRESS", 27, "#666", 310) + bar("evD", "HIGH STRESS", 47, "#111", 406) + '</div>')
    S.j(f'tl.fromTo("#ev",{{scaleY:0}},{{scaleY:1,duration:.45,ease:"bounce.out"}},{b0:.3f});tl.to("#ev",{{scaleY:0,duration:.25,ease:"power2.in"}},{b1 - .25:.3f});')
    S.sfx(b0, "rip", -10)
    for k, w in (("evA", S.w(38, "seventy")), ("evB", S.w(38, "ninety")), ("evC", S.w(39, "Twenty")), ("evD", S.w(39, "forty"))):
        S.j(f'tl.fromTo("#{k}",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.out",immediateRender:false}},{w - .05:.3f});tl.fromTo("#{k}n",{{opacity:0}},{{opacity:1,duration:.1,immediateRender:false}},{w + .2:.3f});')
        S.sfx(w, "stamp", -8)
    S.shake(si0 + .25, .45, 18); S.snapzoom(si0 + .2, 1.3, si1 - si0 + l[40][1] - l[40][0] - .3, 360, 680, .3)
    S.sfx(si0 + .2, "sting", -6); S.sfx(l[41][0] + .5, "slam", -4)
    S.j(f'tl.to("#nrfile",{{y:-30,duration:.1,yoyo:true,repeat:1}},{l[41][0] + .4:.3f});')
    # Rhino peeks from behind the door frame and smirks (still B&W)
    S.char("rhino", "rh", 1560, 420, .7, pose="idle", z=21, expr=[(sm0, sm1 - sm0 + .3, "smug")], blinks=[])
    S.j(f'tl.set("#rhW",{{x:420}},0);tl.to("#rhW",{{x:0,duration:.3,ease:"back.out(1.6)"}},{sm0:.3f});')
    S.sfx(sm0 + .2, "sting", -6)
    S.recap(l[41][0] + .15, 3, "LONG STRESS → COLDS GET IN EASIER", min(4.0, sm0 - l[41][0]), y=200)
    S.tr_out("doors", label="QUEEN'S PARK HQ")
    S.captions({"purpose": "#ff8a8a", "ninety": "#ff8a8a", "fortyseven": "#ff8a8a", "what": "#ff8a8a"})
    return S


@scene
def s10():
    """THE TWIST - the alarm is still going. Security cam: Cyto's real silhouette (toque pom, cup in hand) yanks the ALARM
    lever every time his phone buzzes. Silent "..." holds, then the confession."""
    S = mk("s10", "alarm_low", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    alarm_on(S, "hq", 0, S.T, beams=False); alarm_shake(S, "hq", 0, S.T)
    S.tr_in("doors", label="QUEEN'S PARK HQ")
    S.location("QUEEN'S PARK HQ", "the alarm is STILL going", .45, 2.2)
    l = {n: S.l(n) for n in range(43, 48)}
    c0, c1 = S.b("seccam")
    S.cyto(560, 650, .6, phone=True, expr=[(l[44][0] - .05, .7, "skeptic"), (c1 - .05, l[45][1] - c1 + .1, "shock")],
           x_expr=[(l[46][0], .9, "worried"), (l[47][0], 2.4, "smug")],
           shrugs=[(l[47][0] + .2, .9)], tilts=[(l[47][0] + 1.3, .8, -8)])
    S.char("neutro", "nt", 1290, 300, .74, pose="radio", who="NEUTRO",
           poses=[(l[43][1], "cross"), (l[46][0], "idle")],
           expr=[(0, l[43][1], "determined"), (l[44][0], 1.0, "sideeye"), (c1, l[46][1] - c1 + .2, "deadpan"), (l[47][0] + .4, 2.0, "smug")],
           nods=[l[47][1] - .4])
    S.j(f'tl.fromTo("#ntW",{{x:0}},{{x:-6,duration:.05,yoyo:true,repeat:{int(l[43][1] / .05)},immediateRender:false}},0);')
    # SECURITY CAM: real Cyto silhouette next to the lever, arm up on every buzz
    pulls = [c0 + .35, c0 + .95, c0 + 1.5]
    cx, cy, cs = 1060, 560, .42
    S.over(f'<div id="cam2" class="clip" data-start="{c0:.3f}" data-duration="{c1 - c0:.3f}" style="position:absolute;inset:0;z-index:72;background:#000;overflow:hidden">'
           f'<div id="camI" style="position:absolute;inset:0;transform-origin:1180px 480px;filter:grayscale(1) sepia(1) hue-rotate(60deg) saturate(1.5) contrast(1.25) brightness(.9)">'
           + "".join(X.hq("sc")[:3]) +
           f'<img id="scDn" src="assets/cy_down.png" style="position:absolute;left:{cx - 600 * cs:.0f}px;top:{cy - 640 * cs:.0f}px;width:{1200 * cs:.0f}px;height:{1300 * cs:.0f}px;z-index:6"/>'
           f'<img id="scUp" src="assets/cy_up.png" style="position:absolute;left:{cx - 600 * cs:.0f}px;top:{cy - 640 * cs:.0f}px;width:{1200 * cs:.0f}px;height:{1300 * cs:.0f}px;z-index:6;opacity:0"/>'
           f'</div>'
           f'<div class="static" id="scN" style="position:absolute;inset:0;opacity:.12"></div>'
           f'<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.25) 0 2px,transparent 2px 5px)"></div>'
           f'<div style="position:absolute;left:60px;top:44px;padding:4px 14px;background:rgba(0,0,0,.6);font:44px InterBlack;color:#e8ffe8">CAM 1 · HQ</div>'
           f'<div id="rec" style="position:absolute;right:60px;top:44px;font:44px InterBlack;color:#ff4d4d">● REC</div>'
           f'<div style="position:absolute;left:60px;top:120px;padding:4px 14px;background:rgba(0,0,0,.6);font:38px InterBlack;color:#e8ffe8">DEC 06 2026 · 06:00</div></div>')
    S.j(f'tl.fromTo("#scN",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"41px 77px",duration:.05,repeat:{int((c1 - c0) / .05)},ease:"steps(1)",immediateRender:false}},{c0:.3f});'
        f'tl.fromTo("#rec",{{opacity:1}},{{opacity:0,duration:.4,yoyo:true,repeat:{int((c1 - c0) / .4)},ease:"steps(1)",immediateRender:false}},{c0:.3f});'
        f'tl.fromTo("#camI",{{scale:1}},{{scale:1.2,duration:{c1 - c0:.3f},ease:"none",immediateRender:false}},{c0:.3f});')
    for t in pulls:
        S.j(f'tl.set("#scUp",{{opacity:1}},{t:.3f});tl.set("#scDn",{{opacity:0}},{t:.3f});tl.set("#scUp",{{opacity:0}},{t + .3:.3f});tl.set("#scDn",{{opacity:1}},{t + .3:.3f});')
        lever_pull(S, "sc", t)
        S.over(f'<div id="bz{int(t * 10)}" class="pop clip" data-start="{t - .22:.3f}" data-duration=".4" style="left:{int(cx - 330)}px;top:400px;z-index:73;font:46px InterBlack;color:#e8ffe8;text-shadow:0 0 8px #000">BZZT</div>')
        S.sfx(t - .22, "buzz", -6)
    S.sfx(c0, "static", -12)
    S.hide_txt(c0 - .05, c1)
    S.snapzoom(c1 + .05, 1.15, l[45][1] - c1, 560, 600, .2)
    S.snapzoom(l[46][0] + .02, 1.15, .8, 1530, 500, .2)
    S.sfx(l[47][0] + .2, "sting", -8)
    S.tr_out("doors", label="DOWNTOWN")
    S.captions({"who": "#FFD166", "me": "#FFD166", "ahlie": "#FFD166"})
    return S


@scene
def s11():
    """SERIOUS BEAT - downtown = the heart. Clean 3D: one beating heart (visible lub-dub squash & stretch + heartbeat SFX), Cyto in
    front on the left, cards in the top band (never on the heart), source chip in the top-left zone."""
    S = mk("s11", "calm", "#1d1838", "body")
    bpm = 66
    S.three3d("HRT", "heart", 0, S.T, f"{{dur:{S.T:.3f},bpm:{bpm}}}", z=1)
    S.tr_in("doors", label="DOWNTOWN")
    S.location("DOWNTOWN", "your heart · real talk", .45, 2.2)
    per = 60 / bpm; k = 0
    while k * per < S.T - .2:
        S.sfx(k * per, "heartbeat", -12); k += 1
    l = {n: S.l(n) for n in range(48, 51)}
    S.add('<div class="fill" style="z-index:2;background:linear-gradient(90deg,rgba(13,18,40,.75),rgba(13,18,40,0) 45%)"></div>')
    S.cyto(380, 700, .62, z=20, expr=[(S.w(48, "Not"), 1.1, "sad")], x_expr=[(l[48][0] + .2, 1.4, "determined"), (S.w(49, "Call") - .1, 1.6, "determined")],
           looks=[(S.w(48, "Christmas"), 14, -10)], points=[(S.w(48, "Some") + .2, .8), (S.w(49, "Call") - .1, 1.0)], tilts=[(S.w(48, "stress"), .6, -5)])
    S.j(C.cup_down(.6, S.T + 1))
    S.popup("hb1", S.w(48, "Some") - .1, S.w(48, "Not") - .1, "SOME STUDIES", "MORE HEART ATTACKS AROUND THE HOLIDAYS", "#ff8a8a", 890, 120, 760)
    S.popup("hb2", S.w(48, "Not"), S.w(48, "But") - .1, "TO BE FAIR", "NOT EVERY STUDY", "#8ce2d6", 890, 120, 700)
    S.popup("hb3", S.w(48, "stress") - .1, l[48][1] + .2, "POSSIBLE REASONS", "STRESS · BIG MEALS · SALT · ALCOHOL · WAITING", "#FFD166", 890, 120, 760)
    S.popup("hb4", S.w(49, "Call") - .15, S.T - .2, "CHEST PAIN?", "DON'T WAIT. CALL 911.", "#ff6b6b", 890, 120, 760)
    src_chip(S, "src3", S.w(48, "Some"), l[48][1], "KLONER 2006 · MILNE 2005 · WEERASINGHE 2002", 40, 36)
    S.char("neutro", "nt", 1300, 300, .7, pose="idle", who="NEUTRO", z=19, expr=[(l[50][0] - .4, 1.6, "determined")], nods=[l[50][0] + .2])
    S.j(f'tl.set("#ntW",{{x:800}},0);tl.to("#ntW",{{x:0,duration:.4,ease:"power3.out"}},{l[50][0] - .6:.3f});')
    S.sfx(l[50][0] - .6, "whoosh", -10)
    S.tr_out("doors", label="QUEEN'S PARK HQ")
    S.captions({"911": "#ff6b6b", "nine": "#ff6b6b", "one": "#ff6b6b"})
    return S


def hq_trio(S, mito_pose="slump", gassed=True, mito_expr=(), neutro_expr=(), mito_kw=None, neutro_kw=None):
    """HQ cast with everyone on the FLOOR (Mito no longer perched on the side table)."""
    S.char("mito", "mt", 760, 480, .52, pose=mito_pose, gassed=gassed, who="MITO", z=19, expr=list(mito_expr), **(mito_kw or {}))
    S.char("neutro", "nt", 1330, 300, .72, pose="cross", who="NEUTRO", z=20, expr=list(neutro_expr), **(neutro_kw or {}))


@scene
def s11r():
    """THE BIG RECAP (C-recap) in HQ: the CASE BOARD. Each clue gets ticked on the word that names it, red string runs to
    the suspect polaroid, which flips to Cyto on "Me." - then "Let's fix that." points at the cheat codes."""
    S = mk("s11r", "alarm_low", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    alarm_on(S, "hq", 0, S.T, beams=False)
    S.tr_in("doors", label="QUEEN'S PARK HQ")
    S.location("QUEEN'S PARK HQ", "the case board", .45, 2.0)
    S.talk_scale = 0
    S.push(S.est + .1, S.T, 1.0, 1.07, 1100, 480)
    t1, t2, t3 = S.w(70, "Stress"), S.w(70, "alarm"), S.w(70, "colds")
    tq, tme, tfix = S.w(70, "one"), S.w(70, "Me"), S.w(70, "fix")
    clue = lambda i, x, title, icon: (f'<g id="bc{i}" transform="translate({x} 130)"><g transform="rotate({(-3, 2, -2)[i - 1]} 110 120)">'
                                      f'<rect x="0" y="0" width="220" height="250" fill="#fff" stroke="#0c1622" stroke-width="6"/><rect x="16" y="16" width="188" height="150" fill="#e9eef3"/>{icon}'
                                      f'<text x="110" y="208" text-anchor="middle" font-family="InterBlack" font-size="25" fill="#0c1622">{title[0]}</text>'
                                      f'<text x="110" y="236" text-anchor="middle" font-family="InterBlack" font-size="25" fill="#0c1622">{title[1]}</text>'
                                      f'<circle cx="110" cy="-6" r="13" fill="#e63946" stroke="#0c1622" stroke-width="4"/>'
                                      f'<g id="bk{i}" opacity="0"><circle cx="186" cy="34" r="36" fill="#3fc1b0" stroke="#0c1622" stroke-width="6"/><path d="M168 34 L182 50 L206 20" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>')
    ic1 = '<g transform="translate(110 92)"><path d="M-40 30 Q-40 -40 0 -40 Q40 -40 40 30Z" fill="#e63946" stroke="#0c1622" stroke-width="6"/><rect x="-50" y="28" width="100" height="16" rx="6" fill="#555" stroke="#0c1622" stroke-width="5"/><path d="M-62 -30 l-16 -10 M62 -30 l16 -10 M0 -58 v-14" stroke="#ffb020" stroke-width="8" stroke-linecap="round"/></g>'
    ic2 = '<g transform="translate(110 92)"><rect x="-58" y="-34" width="44" height="78" rx="12" fill="#ff8a8a" stroke="#0c1622" stroke-width="5"/><rect x="14" y="-34" width="44" height="78" rx="12" fill="#FFD166" stroke="#0c1622" stroke-width="5"/><path d="M-8 -50 L8 -14 L-6 -14 L6 24" fill="none" stroke="#0c1622" stroke-width="7" stroke-linejoin="round"/></g>'
    ic3 = '<g transform="translate(110 92)"><rect x="-56" y="-6" width="112" height="56" rx="8" fill="#9fd0ea" stroke="#0c1622" stroke-width="5"/><path d="M-20 -6 Q0 -50 20 -6" fill="#fff" stroke="#0c1622" stroke-width="5"/><circle cx="40" cy="-30" r="20" fill="#7fd34e" stroke="#0c1622" stroke-width="5"/></g>'
    board = (f'<div id="board" style="position:absolute;left:720px;top:96px;width:900px;height:720px;z-index:9"><svg width="900" height="720" style="overflow:visible">'
             f'<rect x="0" y="0" width="900" height="720" rx="18" fill="#b98a5a" stroke="#0c1622" stroke-width="10"/><rect x="20" y="20" width="860" height="680" rx="8" fill="#c99b68"/>'
             f'<text id="bhead" x="450" y="88" text-anchor="middle" font-family="InterBlack" font-size="44" fill="#0c1622">WHO KEEPS PULLING THE ALARM?</text>'
             f'<path id="bstr" d="M130 380 L450 560 M450 380 L450 560 M770 380 L450 560" stroke="#e63946" stroke-width="7" fill="none" stroke-dasharray="560" stroke-dashoffset="560"/>'
             + clue(1, 40, ("STRESS IS", "REAL"), ic1) + clue(2, 340, ("ALARM", "HORMONES"), ic2) + clue(3, 640, ("TOO LONG =", "MORE COLDS"), ic3)
             + f'<g id="bsus" transform="translate(360 470)"><rect x="0" y="0" width="180" height="200" fill="#fff" stroke="#0c1622" stroke-width="6"/>'
             f'<rect x="14" y="14" width="152" height="130" fill="#2a2f3a"/><text id="bq" x="90" y="110" text-anchor="middle" font-family="InterBlack" font-size="90" fill="#FAF4E8">?</text>'
             f'<image id="bme" href="assets/cy_down.png" x="22" y="10" width="136" height="148" opacity="0"/>'
             f'<text x="90" y="182" text-anchor="middle" font-family="InterBlack" font-size="26" fill="#0c1622">SUSPECT</text></g>'
             f'<g id="bstamp" opacity="0" transform="translate(450 570) rotate(-12)"><rect x="-150" y="-44" width="300" height="88" rx="10" fill="none" stroke="#e63946" stroke-width="10"/>'
             f'<text x="0" y="22" text-anchor="middle" font-family="InterBlack" font-size="60" fill="#e63946">IT’S ME</text></g></svg></div>')
    S.add(board)
    S.prop_in("#board", .3, "drop", origin="50% 0%", sfx="clunk", amp=.25)
    for i, t in ((1, t1), (2, t2), (3, t3)):
        S.j(f'tl.set("#bk{i}",{{opacity:1}},{t:.3f});gsap.set("#bk{i}",{{svgOrigin:"186 34"}});tl.fromTo("#bk{i}",{{scale:2.4}},{{scale:1,duration:.25,ease:"back.out(3)",immediateRender:false}},{t:.3f});'
            '')
        S.sfx(t, "stamp", -8)
    S.j(f'tl.to("#bstr",{{attr:{{"stroke-dashoffset":0}},duration:.5,ease:"power2.out"}},{tq:.3f});'
        f'tl.set("#bq",{{opacity:0}},{tme:.3f});tl.set("#bme",{{opacity:1}},{tme:.3f});gsap.set("#bsus",{{svgOrigin:"450 570"}});'
        f'tl.fromTo("#bsus",{{scaleX:1}},{{keyframes:[{{scaleX:0,duration:.08}},{{scaleX:1,duration:.12}}],immediateRender:false}},{tme - .08:.3f});'
        f'tl.set("#bstamp",{{opacity:1}},{tme + .25:.3f});gsap.set("#bstamp",{{svgOrigin:"450 570"}});tl.fromTo("#bstamp",{{scale:2.5}},{{scale:1,duration:.22,ease:"power4.in",immediateRender:false}},{tme + .25:.3f});'
        f'tl.set("#bhead",{{textContent:"NEXT: CHEAT CODES"}},{tfix:.3f});tl.fromTo("#bhead",{{scale:1.2}},{{scale:1,duration:.25,svgOrigin:"450 70",immediateRender:false}},{tfix:.3f});')
    S.sfx(tq, "rip", -12); S.sfx(tme + .25, "slam", -6); S.sfx(tfix, "coin", -8)
    S.cyto(400, 690, .58, expr=[(tme - .05, .8, "skeptic")], x_expr=[(t1, 1.4, "determined"), (t3, 1.2, "worried"), (tfix, 1.2, "smug")],
           points=[(t1 - .1, .9), (t3 - .1, .9), (tfix - .1, .8)], shrugs=[(tme + .1, .7)])
    S.char("neutro", "nt", 1560, 340, .6, pose="cross", who="NEUTRO", z=19, expr=[(tme, 1.4, "smug")], nods=[tme + .3, t3 + .2])
    S.captions({"stress": "#FFD166", "alarm": "#ff6b6b", "colds": "#8ce2d6", "me": "#FFD166"})
    return S


@scene
def s12():
    """CHEAT CODE 1 - slow breathing. The siren slows with each breath; Neutro breathes extremely seriously; Mito yawns."""
    S = mk("s12", "game", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    S.tr_in("cut")
    l = {n: S.l(n) for n in range(51, 53)}
    b0, b1 = S.b("breathe")
    tin = S.w(52, "in", after=S.w(52, "So", after=S.w(52, "did") - .2)); tout = l[52][1]
    S.j(f'tl.set("#hqred",{{opacity:.8}},0);tl.fromTo("#hqred",{{opacity:.85}},{{opacity:.3,duration:.35,yoyo:true,repeat:{int((tin - .2) / .35)},immediateRender:false}},0);'
        f'tl.fromTo("#hqred",{{opacity:.6}},{{opacity:.2,duration:1.0,yoyo:true,repeat:{int((S.T - tin) / 1.0)},immediateRender:false}},{tin:.3f});'
        f'tl.to("#hqred",{{opacity:.12,duration:.6}},{b0 + .2:.3f});')
    alarm_shake(S, "hq", 0, tin)
    S.cyto(430, 650, .58, expr=[(l[51][0], .8, "squint"), (S.w(52, "Plot") - .05, 1.0, "shock")],
           x_expr=[(S.w(51, "I'm"), 1.3, "determined"), (S.w(52, "slow", after=S.w(52, "part") - .5), 1.0, "smug")],
           points=[(S.w(51, "Cheat"), .8), (S.w(52, "slow") - .1, .7), (S.w(52, "twelve"), .6)], shrugs=[(S.w(52, "didn't"), .8)],
           tilts=[(S.w(52, "anxiety"), .6, -6)], blinks=[])
    S.j(f'tl.to("#cyto",{{scale:1.12,duration:{max(.5, tout - tin - 1.2):.3f},ease:"sine.inOut"}},{tin:.3f});tl.to("#cyto",{{scale:1,duration:1.2,ease:"sine.inOut"}},{tout - 1.0:.3f});'
        f'tl.to(["#lidL","#lidR"],{{y:40,duration:.2}},{tin + .1:.3f});tl.to(["#lidL","#lidR"],{{y:-14,duration:.2}},{b1 - .3:.3f});')
    hq_trio(S, "slump", True, [(0, S.T, "exhausted")], [(tin, b1 - tin, "determined")],
            mito_kw=dict(shut_at=[(b0, 1.0)], nods=[S.w(52, "trial")]), neutro_kw=dict(shut_at=[(tin + .2, max(.3, b1 - tin - .3))], nods=[S.w(51, "mess")]))
    S.j(f'tl.set(["#mtm_rest","#mtm_frown","#mtm_smirk","#mtm_grin","#mtm_flat","#mtm_small","#mtm_a","#mtm_e","#mtm_mbp"],{{opacity:0}},{b0 + .05:.3f});tl.set("#mtm_o",{{opacity:1}},{b0 + .05:.3f});'
        f'gsap.set("#mtm_o",{{transformOrigin:"50% 50%"}});tl.fromTo("#mtm_o",{{scale:1}},{{scale:1.8,duration:.35,yoyo:true,repeat:1}},{b0 + .05:.3f});tl.set("#mtm_o",{{opacity:0}},{b1 - .05:.3f});tl.set("#mtm_frown",{{opacity:1}},{b1 - .05:.3f});')
    S.sfx(b0 + .1, "yawn", -8)
    S.j(f'tl.to("#ntBody",{{scale:1.09,duration:{max(.5, tout - tin - .3):.3f},ease:"sine.inOut"}},{tin:.3f});tl.to("#ntBody",{{scale:1,duration:1.0,ease:"sine.inOut"}},{tout - .3:.3f});')
    S.popup("cc0", S.w(51, "Cheat") - .1, l[52][0] - .1, "PRESS START", "CHEAT CODES", "#FFD166", 1040, 120, 700)
    S.popup("cc1", S.w(52, "Cheat") - .1, S.w(52, "A") - .1, "CHEAT CODE 1 UNLOCKED", "SLOW YOUR BREATHING", "#8ce2d6", 1040, 120, 900)
    S.popup("cc1b", S.w(52, "A"), S.w(52, "Plot") - .15, "12-WEEK TRIAL", "SLOW BREATHING → ANXIETY ↓", "#8ce2d6", 1040, 120, 1040)
    S.popup("cc1c", S.w(52, "Plot") - .05, S.w(52, "So", after=S.w(52, "did") - .2) - .1, "PLOT TWIST", "LONGER EXHALE? NOPE. SLOW = THE KEY", "#FFD166", 1040, 120, 980)
    src_chip(S, "src4", S.w(52, "A"), S.w(52, "So", after=S.w(52, "did") - .2), "BIRDEE ET AL. 2023", 40, 36)
    breath_ring(S, tin - .1, S.w(52, "and", after=tin) - .1, tout + .2)
    S.j('tl.set("#ring",{left:"40px",top:"40px"},0);')
    S.j(f'tl.set("#ringT",{{innerHTML:"OUT..."}},{S.w(52, "and", after=tin) - .1:.3f});')
    S.sfx(S.w(51, "Cheat") - .1, "coin", -6); S.sfx(S.w(52, "Cheat") - .1, "levelup", -6); S.sfx(tin, "inhale", -10)
    S.tr_out("whip")
    S.captions({"cheat": "#FFD166", "codes": "#FFD166", "slow": "#8ce2d6"})
    return S


@scene
def s13():
    """CHEAT CODE 2 - pick your side quest (trial card clear of faces), Mito wants hoops, 'Bet.'"""
    S = mk("s13", "game", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    snowfall(S, "hqsnow", S.T)
    S.add('<div class="fill" style="z-index:30;background:rgba(255,40,40,.08)"></div>')
    S.tr_in("whip")
    l = {n: S.l(n) for n in range(53, 56)}
    S.cyto(430, 650, .58, x_expr=[(S.w(53, "All"), 1.4, "smug"), (l[55][0] - .1, .9, "hype")], expr=[(l[54][0] + .2, .6, "skeptic")],
           points=[(S.w(53, "Cheat"), .8), (S.w(53, "pick", after=S.w(53, "So", after=S.w(53, "same")) - .1) - .1, .8)],
           tilts=[(S.w(53, "meditation"), .6, 6)], shrugs=[(S.w(53, "actually"), .6)])
    hq_trio(S, "slump", False, [(0, l[54][0] - .3, "exhausted"), (l[54][0] - .2, 1.2, "hype"), (l[55][0], S.T - l[55][0], "hype")], [(0, S.T, "deadpan")],
            mito_kw=dict(poses=[(l[54][0] - .2, "ball"), (l[55][0] + .1, "hype")], pops=[(l[54][0] - .1, 1), (l[55][0] + .15, 1.3)]),
            neutro_kw=dict(nods=[S.w(53, "same")], poses=[(S.w(53, "exercise"), "notepad"), (S.w(53, "So", after=S.w(53, "same")), "cross")]))
    S.popup("cc2", S.w(53, "Cheat") - .1, S.w(53, "Another") - .1, "CHEAT CODE 2 UNLOCKED", "PICK YOUR SIDE QUEST", "#FFD166", 1000, 110, 900)
    tc0 = S.w(53, "Another") - .05; tc1 = min(tc0 + 3.0, S.w(53, "So", after=S.w(53, "same")) + .2)
    S.over(f'<div id="tri" class="pop clip" data-start="{tc0:.3f}" data-duration="{tc1 - tc0:.3f}" style="left:520px;top:96px;width:1000px;height:330px;z-index:55;border-radius:26px;background:#FAF4E8;border:7px solid #0c1622;box-shadow:0 14px 0 rgba(0,0,0,.35);transform:scale(.9);transform-origin:50% 0">'
           f'<div style="position:absolute;left:0;right:0;top:16px;text-align:center;font:36px InterBlack;color:#0c1622">5-WEEK TRIAL: ALL 3 LOWERED STRESS</div>'
           f'<svg style="position:absolute;left:40px;top:80px" width="920" height="240"><g transform="translate(20 20)">{SNEAKER}</g><text x="240" y="90" font-family="InterBlack" font-size="80" fill="#e63946">=</text>'
           f'<g transform="translate(340 10)">{MEDIT}</g><text x="560" y="90" font-family="InterBlack" font-size="80" fill="#e63946">=</text><g transform="translate(660 20)">{WIND}</g>'
           f'<text x="90" y="200" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">EXERCISE</text><text x="420" y="200" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">MEDITATION</text><text x="740" y="200" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">SLOW BREATHING</text></svg></div>')
    S.j(f'tl.fromTo("#tri",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(1.4)"}},{tc0:.3f});')
    S.hide_txt(tc0, tc1)
    src_chip(S, "src5", tc0 + .3, tc1, "VAN DER ZWAN ET AL. 2015", 40, 36)
    S.popup("pk", tc1 + .05, l[53][1] + .3, "", "PICK WHAT YOU'LL ACTUALLY DO", "#8ce2d6", 1000, 110, 760)
    S.sfx(S.w(53, "Cheat") - .1, "levelup", -6); S.sfx(l[55][0], "coin", -6)
    S.tr_out("doors", label="THE CITY")
    S.captions({"side": "#FFD166", "quest": "#FFD166", "same": "#8ce2d6"})
    return S


@scene
def s14():
    """SIDE-QUEST MONTAGE on REAL Toronto photos (I9/H): skyline (brick outside), Nathan Phillips Square rink (kept wide),
    Distillery brick (warm grade, cropped - no signage), the block. Cyto stays 2D in front with a light rim + drop shadow."""
    S = mk("s14", "game", "#16224a", "city")
    S.talk_scale = 0
    S.tr_in("doors", label="THE CITY")
    S.location("THE CITY", "real Toronto · side quests", .45, 2.0)
    tA = S.w(56, "Skate") - .15; tB = S.w(56, "walk") - .1; tC = S.w(56, "or") - .1; sq0, sq1 = S.b("sidequest")
    segs = [("p0", 0, tA, "skyline", ("55%", "45%")), ("p1", tA, tB, "nathan_phillips", ("50%", "60%")), ("p2", tB, tC, "distillery_warm", ("45%", "40%")), ("p3", tC, S.T, "skyline_block", ("40%", "60%"))]
    for i, (p, a, b, ph, (ox, oy)) in enumerate(segs):
        S.photo(p, ph, a, b + (.25 if i < 3 else 0), (1.0, 1.08), z=1 + i, ox=ox, oy=oy)
        if i:
            S.j(f'tl.fromTo("#{p}",{{x:1920}},{{x:0,duration:.25,ease:"power3.out",immediateRender:false}},{a:.3f});'); S.sfx(a, "whoosh", -10)
    S.add(X.layer("snw", X.snow("sqsnow", 70, 4), 6))
    S.j(f'tl.fromTo("#sqsnow",{{y:-300}},{{y:0,duration:{S.T:.3f},ease:"none"}},0);')
    S.add('<div class="fill" style="z-index:7;background:linear-gradient(rgba(13,24,56,0) 55%,rgba(13,24,56,.55))"></div>')
    S.cyto(760, 720, .58, z=20, x_expr=[(0, tA, "worried"), (tA, tB - tA, "hype"), (tB, tC - tB, "smug"), (tC, S.T - tC, "smug")],
           waves=[tA + .4], points=[(tB + .3, .7)], tilts=[(tC + .3, .6, 6)], blinks=None, toque_extra="")
    S.style(f"#cytoLayer{{{RIM}}}")
    S.j(f'tl.to("#cyto",{{x:6,duration:.05,yoyo:true,repeat:{max(2, int(tA / .05) - 2)}}},0);')
    S.j(f'tl.fromTo("#cytoPos",{{x:"-=520"}},{{x:"+=940",duration:{tB - tA:.3f},ease:"sine.inOut",immediateRender:false}},{tA:.3f});tl.to("#cyto",{{rotation:-8,duration:.4,yoyo:true,repeat:3}},{tA:.3f});'
        f'tl.to("#cytoPos",{{x:"-=420",duration:.01}},{tB:.3f});')
    S.over(f'<div id="hp" class="clip" data-start="{tC:.3f}" data-duration="{S.T - tC:.3f}" style="position:absolute;left:0;top:0;z-index:21"><svg width="1920" height="1080">'
           f'<g transform="translate({760 - 300 * .58 - 40:.0f} {720 - 230:.0f}) scale(.97)"><path d="M40 120 Q180 -40 400 120" fill="none" stroke="#222" stroke-width="20"/><rect x="10" y="100" width="56" height="90" rx="20" fill="#e63946" stroke="#0c1622" stroke-width="6"/><rect x="376" y="100" width="56" height="90" rx="20" fill="#e63946" stroke="#0c1622" stroke-width="6"/></g></svg></div>')
    S.prop_in("#hp", tC, "drop", origin="50% 50%", sfx="pop", amp=.5)
    S.panel("q0", .1, tA - .1, "SIDE QUEST", "IT'S BRICK OUTSIDE: BUNDLE UP", "#8ce2d6", 60, 60, 900)
    S.panel("q1", tA + .1, tB - .1, "SIDE QUEST", "SKATE AT NATHAN PHILLIPS SQUARE", "#8ce2d6", 60, 60, 1000)
    S.panel("q2", tB + .1, tC - .1, "SIDE QUEST", "DISTILLERY WINTER VILLAGE: FREE BEFORE 4 PM", "#8ce2d6", 60, 60, 1260)
    S.panel("q3", tC + .1, sq0, "SIDE QUEST", "WALK THE BLOCK, HEADPHONES IN", "#8ce2d6", 60, 60, 960)
    S.popup("sqc", sq0, S.T, "★ ★ ★", "SIDE QUEST COMPLETE", "#FFD166", 1300, 300, 860)
    S.sfx(sq0, "levelup", -4); S.sfx(tA + .2, "skate", -8)
    S.tr_out("doors", label="QUEEN'S PARK HQ")
    S.captions({"brick": "#8ce2d6", "nathan": "#FFD166", "phillips": "#FFD166", "distillery": "#FFD166"})
    return S


@scene
def s15():
    """CHEAT CODE 3 - mute the group chat. Cyto pushes the lever back UP (it stays), the alarm powers down and goes quiet."""
    S = mk("s15", "game", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    S.j('tl.set("#hqred",{opacity:.25},0);')
    S.tr_in("doors", label="QUEEN'S PARK HQ")
    S.location("QUEEN'S PARK HQ", "cheat code 3", .45, 2.0)
    l57 = S.l(57); m0, m1 = S.b("mute")
    alarm_shake(S, "hq", 0, m0)
    S.cyto(430, 650, .58, phone=True, x_expr=[(S.w(57, "Say"), 1.1, "determined"), (m0, S.T - m0, "smug")], points=[(S.w(57, "Protect") - .1, .8)],
           sips=[(m0 + .15, 1.0)], tilts=[(S.w(57, "sleep"), .5, -6)])
    hq_trio(S, "idle", False, [(m0, S.T - m0, "hype")], [(0, m0, "deadpan"), (m0, S.T - m0, "smug")],
            mito_kw=dict(pops=[(m0 + .2, .8)]), neutro_kw=dict(nods=[m0 + .3]))
    S.popup("cc3", S.w(57, "Cheat") - .1, S.w(57, "Say") - .1, "CHEAT CODE 3 UNLOCKED", "MUTE THE GROUP CHAT", "#ff8a8a", 1000, 110, 900)
    S.popup("cc3b", S.w(57, "Say"), S.w(57, "Protect") - .1, "BONUS", "SAY NO TO ONE THING", "#8ce2d6", 1000, 110, 760)
    S.popup("cc3c", S.w(57, "Protect"), m0 + .05, "BONUS", "PROTECT YOUR SLEEP", "#c4b0ff", 1000, 110, 760)
    S.j(f'tl.set("#cyNotif",{{opacity:0}},{S.w(57, "mute"):.3f});')
    S.over(f'<div id="mute" class="pop clip" data-start="{S.w(57, "mute"):.3f}" data-duration="{S.T - S.w(57, "mute"):.3f}" style="left:640px;top:520px;z-index:60"><svg width="120" height="120"><circle cx="60" cy="60" r="54" fill="#e63946" stroke="#0c1622" stroke-width="6"/>'
           '<path d="M34 48 H50 L70 30 V90 L50 72 H34Z" fill="#fff"/><path d="M80 44 L100 76 M100 44 L80 76" stroke="#fff" stroke-width="8" stroke-linecap="round"/></svg></div>')
    S.prop_in("#mute", S.w(57, "mute"), "pop", origin="50% 50%", sfx="click")
    S.j(f'tl.to("#hqred",{{opacity:0,duration:.6}},{m0:.3f});tl.to("#hqalarmGlass",{{opacity:0,duration:.3}},{m0:.3f});'
        f'gsap.set("#hqalarm",{{svgOrigin:"1060 40"}});tl.to("#hqalarm",{{keyframes:[{{scaleY:.8,duration:.12}},{{scaleY:1.06,duration:.12}},{{scaleY:1,duration:.15}}]}},{m0 + .05:.3f});')
    S.popup("alq", m0 + .1, S.T, "", "ALARM: QUIET", "#8ce2d6", 1000, 110, 560)
    S.sfx(m0, "powerdown", -6)
    S.tr_out("cut")
    S.captions({"mute": "#ff8a8a", "sleep": "#c4b0ff"})
    return S


@scene
def s16():
    """CLIMAX (E/10): silence, a bird chirps. 'Exactly.' Neutro spots Rhino frozen mid-sneak, writes him up and SLAPS the ticket on.
    Hard cut on the slap to the nose door: ACHOO impact (shake + 6-frame snap zoom + 2-frame white flash), Rhino flicked out in a
    big on-screen arc across the whole frame, 'ACHOO!' pops 0.4 s. Hard cut on "He got BOOKED!" to all three in frame, Mito hype."""
    S = mk("s16", "quiet", "#47306b", "hq_quiet")
    for l in X.hq("hq"): S.add(l)
    snowfall(S, "hqsnow", S.T)
    S.tr_in("cut")
    ch0, ch1 = S.b("chirp"); sp0, sp1 = S.b("spot"); ac0, ac1 = S.b("achoo")
    l = {n: S.l(n) for n in range(58, 64)}
    t62 = l[62][0]
    S.add(f'<div style="position:absolute;left:600px;top:572px;z-index:3"><svg width="120" height="90" style="overflow:visible">{BIRD}</svg></div>')
    S.j(f'gsap.set("#bird",{{transformOrigin:"50% 100%"}});tl.fromTo("#bird",{{y:-300,rotation:-30}},{{y:0,rotation:0,duration:.35,ease:"back.out(1.6)",immediateRender:true}},.05);'
        f'tl.to("#bird",{{rotation:-12,y:-6,duration:.12,yoyo:true,repeat:5}},{.45:.3f});')
    for i, t in enumerate((.45, .95)):
        S.over(f'<div id="nt{i}x" class="pop clip" data-start="{t:.3f}" data-duration=".9" style="left:{700 + i * 40}px;top:{500 - i * 30}px;font:60px InterBlack;color:#FFD166;-webkit-text-stroke:2px #0c1622">♪</div>')
        S.j(f'tl.fromTo("#nt{i}x",{{y:0,opacity:1}},{{y:-60,opacity:0,duration:.9}},{t:.3f});')
        S.sfx(t, "chirp", -4)
    S.cyto(430, 650, .58, expr=[(ac0 - .1, .6, "shock"), (t62, .7, "hype")], x_expr=[(l[58][0] - .3, 1.3, "sideeye"), (l[60][0], 1.2, "smug"), (l[63][0], 1.0, "smug")],
           looks=[(.45, 10, -8)], sips=[(l[60][1] + .1, .7)])
    S.char("mito", "mt", 760, 480, .52, pose="idle", who="MITO", z=19, poses=[(t62 - .05, "hype")],
           expr=[(0, sp0, "deadpan"), (sp0, 1.1, "shocked"), (t62 - .05, S.T - t62 + .05, "hype")], pops=[(t62 + .02, 1.6)])
    S.j(f'tl.to("#mtW",{{y:-60,duration:.18,ease:"power2.out",yoyo:true,repeat:1}},{t62 + .05:.3f});')
    # Rhino frozen mid-sneak behind the plant
    S.char("rhino", "rh", 1180, 560, .55, pose="sneak", z=18, expr=[(sp0, S.T - sp0, "shocked")], blinks=[], bob=False)
    S.j(f'tl.fromTo("#rhW",{{x:-260}},{{x:0,duration:{sp0:.3f},ease:"none",immediateRender:false}},0);tl.to("#rh",{{y:-12,duration:.3,yoyo:true,repeat:{max(1, int(sp0 / .3) - 1)},ease:"sine.inOut"}},0);'
        f'tl.set("#rhW",{{opacity:0}},{ac0:.3f});')
    S.char("neutro", "nt", 1450, 300, .72, pose="cross", who="NEUTRO", z=20,
           poses=[(sp0 + .25, "point"), (l[61][0], "notepad"), (l[61][1] - .15, "ticket")],
           expr=[(0, sp0, "deadpan"), (sp0, .8, "shocked"), (l[61][0], S.T - l[61][0], "smug")], nods=[l[59][0] + .1])
    S.j(f'tl.to("#nt",{{scaleX:-1,duration:.1,svgOrigin:"300 650"}},{sp0:.3f});tl.to("#nt",{{scaleX:1,duration:.1,svgOrigin:"300 650"}},{sp0 + .25:.3f});'
        f'tl.to("#ntW",{{x:-150,duration:.25,ease:"power2.out"}},{l[61][1] - .35:.3f});')
    S.snapzoom(sp0 + .25, 1.2, sp1 - sp0, 1300, 640, .3)
    S.sfx(sp0 + .25, "sting", -6); S.sfx(l[61][1] - .3, "rip", -4)
    # the ticket SLAP (ticket sticks to Rhino with a squash), then hard cut on the slap
    S.over(f'<div id="tkt" class="pop clip" data-start="{l[61][1] - .12:.3f}" data-duration="{ac0 - l[61][1] + .12:.3f}" style="left:1250px;top:560px;z-index:60;transform:rotate(-12deg)"><svg width="120" height="140"><rect x="6" y="6" width="108" height="128" rx="8" fill="#fff6c8" stroke="#0c1622" stroke-width="6"/><path d="M22 34 H96 M22 60 H96 M22 86 H70" stroke="#c0392b" stroke-width="7"/></svg></div>')
    S.j(f'tl.fromTo("#tkt",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:.1,ease:"power4.in"}},{l[61][1] - .12:.3f});'
        f'tl.fromTo("#rh",{{scaleY:1,scaleX:1}},{{scaleY:.82,scaleX:1.14,duration:.06,yoyo:true,repeat:1,svgOrigin:"200 400",immediateRender:false}},{l[61][1] - .02:.3f});')
    S.sfx(l[61][1] - .02, "slap", 0)
    S.hide_txt(ac0 - .05, t62 + .05)
    # ---- ACHOO cutaway (inside the camera so the shake / snap zoom hit it)
    nd = "".join(X.nose_door("nd"))
    S.add(f'<div id="ach" class="clip" data-start="{ac0:.3f}" data-duration="{t62 - ac0:.3f}" style="position:absolute;inset:0;z-index:60;overflow:hidden">{nd}'
          f'<div style="position:absolute;inset:0;z-index:5">{K.wrap(K.rhino_html("rz", "spread"), "rzW", 0, 0, .8)}</div>'
          f'<div id="rzTk" style="position:absolute;left:0;top:0;z-index:6;width:10px;height:10px"><svg width="90" height="104" style="position:absolute;left:-45px;top:-52px"><rect x="5" y="5" width="80" height="94" rx="6" fill="#fff6c8" stroke="#0c1622" stroke-width="5"/><path d="M16 26 H72 M16 46 H72 M16 66 H52" stroke="#c0392b" stroke-width="6"/></svg></div>'
          f'<div id="achF" style="position:absolute;inset:0;z-index:8;background:#fff;opacity:0"></div></div>')
    S.over(f'<div id="achT" class="clip" data-start="{ac0 + .12:.3f}" data-duration=".42" style="position:absolute;left:0;right:0;top:250px;text-align:center;z-index:76;font:220px InterBlack;color:#FFD166;-webkit-text-stroke:9px #0c1622;paint-order:stroke fill">ACHOO!</div>')
    ti = ac0 + .12
    # Rhino path: out of the door, big arc across the WHOLE frame (stays on screen, large), exits left
    path = [(800, 560, .7, 0), (1250, 230, .95, 200), (900, 60, 1.1, 420), (420, 120, 1.15, 600), (60, 380, 1.15, 760), (-500, 640, 1.2, 900)]
    kf = ",".join(f'{{x:{x},y:{y},scale:{s},rotation:{r},duration:{(ac1 + .1 - ti) / (len(path) - 1):.3f},ease:"none"}}' for x, y, s, r in path[1:])
    x0, y0, s0, r0 = path[0]
    S.j(f'gsap.set("#rzW",{{transformOrigin:"0 0"}});tl.set("#rzW",{{x:{x0},y:{y0},scale:{s0},rotation:{r0}}},{ac0:.3f});tl.to("#rzW",{{keyframes:[{kf}]}},{ti:.3f});'
        f'tl.set("#rzTk",{{x:{x0 + 160},y:{y0 + 150}}},{ac0:.3f});tl.to("#rzTk",{{keyframes:[' + ",".join(f'{{x:{x + 160 * s},y:{y + 150 * s},rotation:{r},duration:{(ac1 + .1 - ti) / (len(path) - 1):.3f},ease:"none"}}' for x, y, s, r in path[1:]) + f']}},{ti:.3f});'
        f'tl.fromTo("#rzW",{{scaleY:.7}},{{scaleY:{s0},duration:.08,immediateRender:false}},{ac0 + .04:.3f});'
        f'tl.fromTo("#achF",{{opacity:.75}},{{opacity:0,duration:.067,ease:"steps(1)",immediateRender:false}},{ti:.3f});'
        f'tl.fromTo("#achT",{{scale:.2}},{{keyframes:[{{scale:1.25,duration:.12,ease:"power3.out"}},{{scale:1,duration:.1}},{{scale:1.05,duration:.12}},{{scale:0,duration:.08,ease:"power3.in"}}],immediateRender:false}},{ti:.3f});')
    S.j(K.act_js("rz", 28, 26, expr=[(ac0, S.T - ac0, "shocked")], T=S.T, blinks=[], bob=False))
    S.snapzoom(ti, 1.25, .2, 960, 560, .25)
    S.shake(ti, .6, 30)
    S.sfx(ac0 + .02, "achoo", 2); S.sfx(ti + .05, "slam", -2); S.sfx(ti + .2, "whoosh", -4)
    # back in HQ on the punchline: a tiny Rhino sails past the window (callback), crowd cheer
    S.add(f'<div id="rhOut" class="clip" data-start="{t62:.3f}" data-duration="1.0" style="position:absolute;left:0;top:0;z-index:1">{K.wrap(K.rhino_html("ro", "spread"), "roW", 300, 240, .16)}</div>')
    S.j(f'tl.fromTo("#roW",{{x:0,y:0,rotation:0}},{{x:500,y:120,rotation:540,duration:.9,ease:"power1.in"}},{t62:.3f});')
    S.sfx(t62, "cheer", -8); S.sfx(t62, "hit", -6)
    S.tr_out("whip")
    S.captions({"exactly": "#FFD166", "booked": "#FFD166", "nasal": "#ff8a8a"})
    return S


PHOTO_CREDIT = ("Photos: Unsplash", "Ronin · Richard Burlton · Chris Stewart · Zia Syed")


@scene
def s17():
    """OUTRO (I10): BREAK STARTS. Neutro, Mito and Cyto together on the left 2/3; Rhino in a jar on the shelf, cuffed (callback).
    Sources in their own band on the right (34 px+), NOT MEDICAL ADVICE in solid colour. Phone buzzes, alarm flickers... loop."""
    S = mk("s17", "outro", "#47306b", "hq")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    S.tr_in("whip")
    l = {n: S.l(n) for n in range(64, 67)}
    e0, e1 = S.b("end")
    flipsign(S, "cd", .45, "1 DAY TILL BREAK", "BREAK STARTS", 290, 40, 520)
    S.prop_in("#cd", .02, "drop", origin="50% 0%", sfx="clunk", amp=.5)
    S.j(f'tl.to("#cd",{{y:-260,duration:.3,ease:"power2.in"}},{l[64][0] - .2:.3f});')
    S.sfx(.5, "cheer", -10)
    # Rhino in a jar on the shelf, cuffed
    S.add(f'<div id="jar" style="position:absolute;left:40px;top:200px;z-index:9"><svg width="230" height="230" style="overflow:visible">'
          f'<rect x="0" y="196" width="230" height="22" rx="6" fill="#7a4b2c" stroke="#0c1622" stroke-width="6"/>'
          f'<rect x="40" y="40" width="150" height="156" rx="26" fill="#cfe9f7" fill-opacity=".45" stroke="#0c1622" stroke-width="6"/><rect x="34" y="22" width="162" height="28" rx="8" fill="#e63946" stroke="#0c1622" stroke-width="6"/>'
          f'<g transform="translate(58 66) scale(.28)">{K.rhino_html("rj", "idle")}</g>'
          f'<g fill="none" stroke="#c9ccd2" stroke-width="7"><circle cx="98" cy="170" r="12"/><circle cx="128" cy="170" r="12"/><path d="M110 170 H116"/></g>'
          f'<path d="M150 60 Q160 120 150 180" stroke="#fff" stroke-width="8" opacity=".6" fill="none" stroke-linecap="round"/></svg></div>')
    S.prop_in("#jar", .25, "drop", origin="50% 100%", sfx="clunk", amp=.6)
    S.j(f'tl.to("#rjBody",{{y:-6,duration:.4,yoyo:true,repeat:{int(S.T / .4)},ease:"sine.inOut"}},.8);')
    S.cyto(360, 690, .54, phone=True, expr=[(l[65][0], .8, "skeptic"), (e0 + .45, 1.0, "shock")],
           x_expr=[(S.w(66, "Comment"), 1.6, "hype"), (S.w(66, "Not"), 1.2, "deadpan"), (S.w(66, "breathe") - .2, 1.0, "smug")],
           waves=[S.w(66, "Like")], points=[(S.w(66, "sources") - .1, .8)], sips=[(S.w(66, "December's") - .3, .9)])
    S.char("mito", "mt", 560, 500, .48, pose="idle", who="MITO", z=19, poses=[(l[64][0], "hype"), (l[65][0] + .5, "slump")],
           expr=[(.3, 1, "hype"), (l[64][0], l[64][1] - l[64][0], "hype"), (l[65][0] + .3, 2, "exhausted")], shut_at=[(S.w(64, "mans"), 1.2)])
    S.j(f'tl.to("#mtBody",{{y:-14,duration:.3,yoyo:true,repeat:5,ease:"sine.inOut"}},{l[64][0] + .2:.3f});')
    S.over(f'<div id="smell" class="clip" data-start="{l[64][0]:.3f}" data-duration="{l[64][1] - l[64][0] + .5:.3f}" style="position:absolute;left:640px;top:330px;z-index:30"><svg width="260" height="200">'
           + "".join(f'<path d="M{20 + i * 70} 190 q30 -40 0 -80 t0 -80" fill="none" stroke="#FAF4E8" stroke-width="10" stroke-linecap="round" opacity=".8"/>' for i in range(3)) + '</svg></div>')
    S.j(f'tl.fromTo("#smell",{{y:30,opacity:0}},{{y:-20,opacity:1,duration:1.2,repeat:2}},{l[64][0]:.3f});')
    S.sfx(S.w(64, "Is"), "sniff", -6)
    S.char("neutro", "nt", 860, 330, .6, pose="cross", who="NEUTRO", z=20, expr=[(0, S.T, "deadpan")], nods=[.6, S.w(66, "Not")],
           poses=[(S.w(66, "sources") - .1, "point"), (S.w(66, "sources") + 1.0, "cross")])
    # sources band (right, own zone), NOT MEDICAL ADVICE, then the photo credit
    s0 = l[64][0]; items = SOURCES + [PHOTO_CREDIT]; per = (e0 - s0) / len(items)
    S.hide_txt(s0 - .2, S.T)
    S.over(f'<div id="srcband" class="clip" data-start="{s0 - .15:.3f}" data-duration="{e0 - s0 + .15:.3f}" style="position:absolute;left:1260px;top:150px;width:620px;height:720px;z-index:61;border-radius:26px;background:rgba(12,22,34,.9);border:6px solid #FAF4E8"></div>')
    S.j(f'tl.fromTo("#srcband",{{x:700}},{{x:0,duration:.3,ease:"back.out(1.4)"}},{s0 - .15:.3f});')
    for i, (a, b) in enumerate(items):
        ta = s0 + i * per
        hdr = "PHOTOS" if i == len(items) - 1 else f"SOURCES {i + 1}/{len(SOURCES)}"
        S.over(f'<div id="src{i}" class="pop clip" data-start="{ta:.3f}" data-duration="{per:.3f}" style="left:1290px;top:190px;width:560px;z-index:62">'
               f'<div style="font:30px InterBlack;color:#FFD166;letter-spacing:.08em">{hdr}</div>'
               f'<div style="font:36px/1.2 InterBlack;color:#FAF4E8;margin-top:16px">{a}</div><div style="font:36px/1.2 InterBlack;color:#FAF4E8;margin-top:18px">{b}</div></div>')
        S.j(f'tl.fromTo("#src{i}",{{x:40,opacity:0}},{{x:0,opacity:1,duration:.22}},{ta:.3f});')
    S.over(f'<div id="nma2" class="clip" data-start="{s0:.3f}" data-duration="{e0 - s0:.3f}" style="position:absolute;left:1300px;top:760px;width:540px;z-index:63;text-align:center;padding:12px 0;border-radius:16px;background:#e63946;font:40px InterBlack;color:#fff">NOT MEDICAL ADVICE</div>')
    S.popup("cta", S.w(66, "Comment") - .1, S.w(66, "Like") - .1, "COMMENT", "WHAT'S STRESSING YOU OUT?", "#FFD166", 560, 110, 900)
    S.popup("cta2", S.w(66, "Like") - .05, S.w(66, "sources") - .1, "", "LIKE + SUBSCRIBE", "#ff8a8a", 560, 110, 700)
    buzz(S, e0 + .15, .4)
    S.j(f'tl.set("#hqred",{{opacity:0}},0);tl.to("#hqred",{{opacity:.7,duration:.05}},{e0 + .55:.3f});tl.to("#hqred",{{opacity:0,duration:.05}},{e0 + .7:.3f});tl.to("#hqred",{{opacity:.6,duration:.05}},{e0 + .9:.3f});tl.to("#hqred",{{opacity:0,duration:.08}},{e0 + 1.05:.3f});'
        f'tl.to("#hqalarmGlass",{{opacity:1,duration:.05}},{e0 + .55:.3f});tl.to("#hqalarmGlass",{{opacity:.35,duration:.05}},{e0 + 1.1:.3f});')
    alarm_shake(S, "hq", e0 + .55, S.T)
    S.snapzoom(e0 + .5, 1.2, e1 - e0, 400, 600, .01)
    S.sfx(e0 + .55, "blip", -6)
    S.captions({"comment": "#FFD166", "breathe": "#8ce2d6", "christmas": "#ff8a8a", "marved": "#FFD166"})
    return S


if __name__ == "__main__":
    names = sys.argv[1:] or list(SC)
    for n in names:
        s = SC[n](); d = s.build() if not os.environ.get("NOBUILD") else None
        print("built", n, f"{s.t0:.2f}-{s.t1:.2f} ({s.T:.2f}s)", "mouth fixes:", sum(1 for m in MOUTH_LOG if m[0] == n))
    ev_f = "/home/claude/lf02/events.json"
    ev = json.load(open(ev_f)) if os.path.exists(ev_f) else {}
    for n in names:
        s0, s1 = CUTS[n]
        ev[n] = {"sfx": [x for x in SFX if s0 - .2 <= x[0] < s1 + .01], "music": [m for m in MUSIC if s0 - .01 <= m[0] < s1 + .01],
                 "amb": [s0, s1, AMB.get(n, "hq")]}
    ev = {k: v for k, v in ev.items() if k in CUTS}
    json.dump(ev, open(ev_f, "w"), indent=0)
    json.dump(MOUTH_LOG, open("/home/claude/lf02/mouth_log.json", "w"))
