"""LF02 scenes. python3 scenes.py s01 s02 ...  (no args = all). Each scene -> /home/claude/hf/lf02/<name>/index.html"""
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
@scene
def s01():
    """COLD OPEN — Queen's Park HQ. Cyto chill on the beanbag; alarm; Neutro kicks the door in; Rhino at the window; title slam."""
    S = Scene("s01", 0, BEATS["title"][1], bg="#47306b")
    MUSIC.append((0, BEATS["alarm"][0], "cozy")); MUSIC.append((BEATS["alarm"][0], S.t1, "alarm"))
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq"))
    snowfall(S, "hqsnow", S.T)
    tA = BEATS["alarm"][0]; tB = BEATS["title"][0]
    l2, l3, l4, l5 = S.l(2), S.l(3), S.l(4), S.l(5)
    # Rhino pressed to the window (clipped to the arch), waves, ducks
    S.add('<div id="rhClip" class="fill" style="z-index:1;clip-path:path(\'M283 657 V385 A222 222 0 0 1 727 385 V657Z\')">'
          + K.wrap(K.rhino_html("rh", "idle"), "rhW", 380, 700, .62) + '</div>')
    S.j(f'tl.set("#rhW",{{y:0}},0);tl.to("#rhW",{{y:-500,duration:.35,ease:"back.out(1.6)"}},{tB + .1:.3f});tl.to("#rhW",{{y:0,duration:.3,ease:"power3.in"}},{tB + 2.05:.3f});')
    S.j(K.act_js("rh", 28, 26, poses=[(tB + .5, "wave"), (tB + 1.6, "duck")], expr=[(tB + .2, 1.8, "smug")], T=S.T, blinks=[]))
    S.j(f'tl.to("#rhW",{{x:14,duration:.12,yoyo:true,repeat:5}},{tB + .55:.3f});')
    # Cyto on the beanbag, phone in hand
    S.cyto(540, 640, .6, phone=True,
           expr=[(S.w(1, "Nah") - .05, .9, "skeptic"), (tA + .05, 1.3, "shock"), (l3[0], .9, "skeptic")],
           x_expr=[(S.w(1, "him"), .9, "smug"), (l5[0] - .1, 1.6, "exhausted"), (tB + .2, 2.2, "sideeye")],
           sips=[(S.w(1, "I", ) - .05, 1.1)], tilts=[(S.w(1, "Exams"), .5, -6), (l3[0], .6, 7)], shrugs=[(S.w(1, "Nah"), .6)],
           looks=[(S.w(1, "Group") - .1, -10, 8), (l2[0], 14, -2), (tB + .3, -14, -8)])
    for t, txt, x in ((S.w(1, "Exams"), "EXAMS", 760), (S.w(1, "Group"), "GROUP CHAT", 790), (S.w(1, "Holiday"), "SALE ENDS SOON", 760)):
        buzz(S, t - .1); notif(f"n{int(t * 10)}", t - .1, txt, x, 520 - (t - 1) * 40, S=S, d=1.2)
    buzz(S, tA - .25, .4)
    alarm_on(S, "hq", tA, S.T - .05)
    S.shake(tA, .6, 16); S.punch(tA, 1.1)
    S.sfx(tA, "siren", -6); S.sfx(tB + .15, "hit", -2); S.sfx(tB + .3, "gulp", -8)
    # Neutro kicks the door open, steps in with a hand on his radio
    S.j(f'gsap.set("#hqdoor",{{svgOrigin:"1530 520"}});tl.to("#hqdoor",{{scaleX:.12,duration:.16,ease:"power4.out"}},{tA + .7:.3f});tl.to("#hqdoor",{{scaleX:.2,duration:.4,ease:"elastic.out(1,.4)"}},{tA + .86:.3f});')
    S.sfx(tA + .7, "kick", -2)
    S.char("neutro", "nt", 1530, 300, .74, pose="idle", who="NEUTRO",
           poses=[(tA + .8, "radio"), (l4[0] - .1, "idle"), (l5[0] + .3, "cross")],
           expr=[(tA + .8, 1.1, "determined"), (l4[0] - .05, 1.4, "deadpan"), (l5[0], 1.2, "deadpan"), (tB + .4, 2.0, "sideeye")],
           looks=[(l3[0] + .2, -.3, 0), (tB + .5, -.3, -.2)], nods=[l2[0] + .1, l4[0] + .3])
    S.j(f'tl.set("#ntW",{{x:260,opacity:0}},0);tl.set("#ntW",{{opacity:1}},{tA + .72:.3f});tl.to("#ntW",{{x:-120,duration:.35,ease:"power3.out"}},{tA + .74:.3f});'
        f'tl.fromTo("#ntW",{{y:-30}},{{y:0,duration:.35,ease:"bounce.out",immediateRender:false}},{tA + .9:.3f});')
    S.punch(l4[0], 1.18, .5, 1350, 520)            # "December." snap on Neutro
    S.snapzoom(l5[0] - .1, 1.12, 1.0, 520, 640)       # slow push on Cyto's "...nyeahh"
    # TITLE SLAM
    S.over(f'<div id="title" class="clip" data-start="{tB + .05:.3f}" data-duration="{S.T - tB:.3f}" style="position:absolute;left:760px;right:60px;top:80px;text-align:center;z-index:85">'
           '<div style="font:130px/1 InterBlack;color:#FAF4E8;-webkit-text-stroke:7px #0c1622;paint-order:stroke fill;text-shadow:0 12px 0 rgba(0,0,0,.45)">DECEMBER:</div>'
           '<div style="font:160px/1 InterBlack;color:#ff3b3b;-webkit-text-stroke:8px #0c1622;paint-order:stroke fill;text-shadow:0 14px 0 rgba(0,0,0,.45)">CODE RED</div></div>')
    S.j(f'tl.to(".settxt",{{opacity:0,duration:.1}},{tB:.3f});')
    S.j(f'tl.fromTo("#title",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:.22,ease:"power4.in"}},{tB + .05:.3f});')
    S.shake(tB + .27, .45, 22)
    S.tr_out("zoom", .35)
    S.captions({"red": "#ff6b6b", "december": "#ff6b6b", "him": "#FFD166"})
    return S


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


@scene
def s02():
    """INTRO — 3D fly-through of the body-city into Queen's Park, then Cyto hosting from the HQ rooftop."""
    t0 = BEATS["title"][1]; t1 = BEATS["to_report"][1]
    S = Scene("s02", t0, t1, music="intro", bg="#2b1640")
    tFly = S.w(6, "And") - .1      # 3D until "...inside your body."
    S.three3d("CITY", "bodycity", 0, tFly + .4, f"{{dur:{tFly + .4:.3f}}}", z=50)
    S.tr_in("zoom", .35)
    # body-city labels over the 3D (one at a time)
    for i, (txt, a, b, x) in enumerate((("THE BODY = THE 6IX", .5, 2.6, 960), ("HEART = DOWNTOWN", 2.8, 4.2, 1340), ("BRAIN = QUEEN'S PARK", 4.4, tFly, 960))):
        S.over(f'<div id="lab{i}" class="pop clip" data-start="{a:.3f}" data-duration="{b - a:.3f}" style="left:{x - 380}px;width:760px;top:150px;text-align:center;font:54px InterBlack;color:#FFD166;-webkit-text-stroke:3px #0c1622;paint-order:stroke fill">{txt}</div>')
        S.j(f'tl.fromTo("#lab{i}",{{y:-30,opacity:0}},{{y:0,opacity:1,duration:.25,ease:"back.out(2)"}},{a:.3f});')
    S.sfx(0, "whoosh", -4)
    # rooftop host shot
    for l in rooftop("rt"): S.add(l)
    S.parallax([("rtL1", .15), ("rtL2", .35), ("rtL3", .7)], tFly, S.T, dx=-120)
    snowfall(S, "rtsnow", S.T, 300)
    S.j(f'gsap.set("#rtsiren",{{transformOrigin:"50% 100%"}});tl.fromTo("#rtsiren",{{opacity:1}},{{opacity:.3,duration:.3,yoyo:true,repeat:{int(S.T / .3)},immediateRender:false}},0);')
    S.cyto(700, 700, .62, outfit="outfit_pufferhoodie",
           expr=[(S.w(6, "lowkey"), .9, "squint"), (S.w(6, "bro") - .05, 1.3, "shock"), (S.w(6, "cheat"), .9, "hype")],
           x_expr=[(S.w(6, "Today"), 1.2, "determined"), (S.w(6, "Not"), 1.6, "deadpan")],
           waves=[S.w(6, "Yo")], points=[(S.w(6, "why"), .8), (S.w(6, "cheat"), .8)], sips=[(S.w(6, "just") - .2, 1.1)],
           tilts=[(S.w(6, "panicking"), .7, -7)], looks=[(S.w(6, "why") + .1, 14, -8)])
    S.j(f'tl.set("#cytoLayer",{{opacity:0}},0);tl.set("#cytoLayer",{{opacity:1}},{tFly + .3:.3f});')
    S.j(f'tl.fromTo("#cytoPos",{{y:"+=300"}},{{y:"-=300",duration:.4,ease:"back.out(1.7)",immediateRender:false}},{tFly + .3:.3f});')
    # Rhino tiptoes along the roof behind Cyto (sight gag), Mito jogs by far below? keep it to one gag
    S.char("rhino", "rh", 2000, 590, .45, pose="sneak", z=5, expr=[(S.w(6, "Today"), 4, "smug")], blinks=[])
    S.j(f'tl.fromTo("#rhW",{{x:0}},{{x:-2500,duration:10,ease:"none",immediateRender:false}},{S.w(6, "Today") - .5:.3f});'
        f'tl.to("#rh",{{y:-16,duration:.25,yoyo:true,repeat:19,ease:"sine.inOut"}},{S.w(6, "Today") - .5:.3f});')
    S.sfx(S.w(6, "Today") - .4, "tiptoe", -10)
    # teaser beats: WHY / WHAT IT DOES / "BRO, WHAT" / CHEAT CODES, then the NOT MEDICAL ADVICE card
    S.popup("tz1", S.w(6, "why") - .05, S.w(6, "plus") - .1, "TODAY", "WHY + WHAT IT DOES TO YOU", "#8ce2d6", 1330, 170, 900)
    S.popup("tz2", S.w(6, "plus"), S.w(6, "And", after=S.w(6, "plus")) - .1, "CASE FILE", "ONE STUDY: “BRO, WHAT”", "#ff8a8a", 1330, 170, 900)
    S.popup("tz3", S.w(6, "cheat") - .1, S.w(6, "Not") - .15, "LOADING...", "CHEAT CODES", "#FFD166", 1330, 170, 900)
    S.snapzoom(S.w(6, "bro") - .05, 1.16, .9, 700, 560)
    S.sfx(S.w(6, "bro") - .05, "sting", -6); S.sfx(S.w(6, "cheat") - .1, "coin", -8)
    S.over(f'<div id="nma" class="clip" data-start="{S.w(6, "Not") - .1:.3f}" data-duration="{S.T - S.w(6, "Not") + .1:.3f}" style="position:absolute;left:1120px;top:200px;width:700px;z-index:70;'
           'padding:26px 30px;border-radius:24px;background:#FAF4E8;border-left:16px solid #e63946;box-shadow:0 14px 0 rgba(0,0,0,.35)">'
           '<div style="font:44px InterBlack;color:#e63946">NOT MEDICAL ADVICE</div><div style="font:36px/1.2 InterSB;color:#0c1622;margin-top:6px">Just your boy + some science. Sources on screen + in the description.</div></div>')
    S.j(f'tl.fromTo("#nma",{{x:80,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"back.out(1.6)"}},{S.w(6, "Not") - .1:.3f});')
    S.tr_out("whip", .3)
    S.captions({"6ix": "#FFD166", "panicking": "#ff6b6b", "bro": "#ff8a8a", "what": "#ff8a8a"})
    return S



def card(S, id_, t0, t1, num, title, art, x=620, y=70, rot=-3):
    """Incident-report card: slams in with a whoosh + alarm blip."""
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x}px;top:{y}px;width:680px;height:560px;z-index:60;transform:rotate({rot}deg);'
           f'background:#FAF4E8;border:8px solid #0c1622;border-radius:18px;box-shadow:0 18px 0 rgba(0,0,0,.35)">'
           f'<div style="position:absolute;left:0;right:0;top:0;height:86px;background:#1f2b4d;border-radius:8px 8px 0 0"></div>'
           f'<div style="position:absolute;left:28px;top:14px;font:46px InterBlack;color:#FFD166">INCIDENT {num}</div>'
           f'<div style="position:absolute;left:28px;top:458px;right:20px;font:38px/1.1 InterBlack;color:#0c1622">{title}</div>'
           f'<svg style="position:absolute;left:20px;top:100px" width="620" height="360" viewBox="0 0 620 360">{art}</svg></div>')
    S.j(f'tl.fromTo("#{id_}",{{x:-900,rotation:-30}},{{x:0,rotation:{rot},duration:.32,ease:"back.out(1.5)"}},{t0:.3f});tl.to("#{id_}",{{x:1500,rotation:20,duration:.25,ease:"power3.in"}},{t1 - .25:.3f});')
    S.sfx(t0, "whoosh", -6); S.sfx(t0 + .25, "blip", -8)


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


@scene
def s03():
    """ACT 1 — the incident report. Neutro reads off his notepad, cards slam in, Cyto takes each one personally."""
    t0 = BEATS["to_report"][1]; t1 = BEATS["to_condos"][0] + .6
    S = Scene("s03", t0, t1, music="alarm_low", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    alarm_on(S, "hq", 0, S.T, beams=False)
    S.tr_in("whip", .3)
    S.parallax([("hqL0", .2), ("hqL1", .35), ("hqL2", .5), ("hqL3", 1.0)], 0, S.T, dx=-60)
    l = {n: S.l(n) for n in range(7, 13)}
    S.j('tl.to(".settxt",{opacity:0,duration:.2},.31);')   # the cards cover the wall signs all scene
    cards = [(7, "EXAMS.", ART_EXAM, "ONE"), (8, "SECRET SANTA GROUP CHAT", ART_CHAT, "TWO"), (9, "THE MALL = LINE 1 AT RUSH HOUR", ART_TRAIN, "THREE"), (10, "YOUR AUNTIE.", ART_AUNTIE, "FOUR")]
    for i, (n, title, art, num) in enumerate(cards):
        a = l[n][0] - .05; b = (l[n + 1][0] - .1) if n < 10 else l[12][1] + .3
        card(S, f"ic{n}", a, b, num, title, art, x=640, y=60, rot=(-3, 2, -2, 3)[i])
    S.cyto(420, 660, .56, expr=[(l[8][0] + 1.2, 1.0, "skeptic"), (l[10][0] + 1.2, 1.4, "shock"), (l[11][0], 1.2, "skeptic")],
           x_expr=[(l[7][0] + .8, 1.0, "deadpan"), (l[9][0] + 1.0, 1.6, "exhausted"), (l[12][0], 1.1, "worried")],
           looks=[(l[7][0] + .1, 12, -8), (l[9][0] + .1, 12, -8), (l[12][0] + .1, 14, 0)],
           shrugs=[(l[11][0] + .1, .8)], tilts=[(l[10][0] + 2.0, .9, -8)], sips=[(l[9][1] - .9, 1.1)])
    S.char("neutro", "nt", 1340, 300, .74, pose="notepad", who="NEUTRO",
           poses=[(l[11][0] + .5, "point"), (l[12][0] + .2, "notepad")],
           expr=[(l[7][0], l[10][1] - l[7][0], "deadpan"), (l[11][0] + .3, .9, "sideeye"), (l[12][0], 1.4, "smug")],
           nods=[l[7][1] - .3, l[8][1] - .3, l[9][1] - .3, l[10][1] - .3, l[12][0] + .5], looks=[(l[11][0] + .2, -.3, 0)])
    S.punch(l[11][0], 1.12, .45, 420, 600)          # "Bro, that's personal."
    S.snapzoom(l[12][0] + .05, 1.1, .9, 1560, 500)   # "It's in the report."
    S.sfx(l[12][0] + .4, "tap", -6)
    # the alarm signal zips out of HQ (to the adrenal condos)
    tz = BEATS["to_condos"][0] - t0
    S.over(f'<div id="zip" class="clip" data-start="{tz:.3f}" data-duration="{S.T - tz:.3f}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:75"><svg width="1920" height="1080"><path id="zipP" d="M1060 110 C1300 300 700 600 1000 1180" fill="none" stroke="#ff3b3b" stroke-width="22" stroke-linecap="round" stroke-dasharray="1600" stroke-dashoffset="1600"/></svg></div>')
    S.j(f'tl.to("#zipP",{{attr:{{"stroke-dashoffset":0}},duration:.45,ease:"power2.in"}},{tz:.3f});')
    S.sfx(tz, "zap", -6)
    S.tr_out("whip", .25)
    S.captions({"exams": "#FFD166", "fortythree": "#FFD166", "twenty": "#FFD166", "personal": "#ff8a8a"})
    return S


def mito_court_char(S, **kw):
    S.char("mito", "mt", kw.pop("x"), kw.pop("y"), kw.pop("s", .62), who="MITO", **kw)


@scene
def s04():
    """Streetball court establishing: scoreboard drops, crowd bobs, Mito warms up, THE ALARM checks in. Cyto on the mic."""
    t0 = BEATS["to_condos"][0] + .6; t1 = gw(13, "signal") - .4
    S = Scene("s04", t0, t1, music="court", bg="#5a1430")
    S.cap_lr = (720, 120)
    for l in X.court("ct"): S.add(l)
    S.add(X.desk("dk"))
    S.over(X.scoreboard("sb"))
    S.tr_in("whip", .25)
    S.j(f'tl.fromTo("#sb",{{y:-40,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"back.out(2)"}},.2);')
    S.j(f'document.querySelectorAll(".ctfan").forEach((f,i)=>tl.to(f,{{y:-10-(i%3)*4,duration:.22+(i%4)*.04,yoyo:true,repeat:{int(S.T / .22)},ease:"sine.inOut"}},(i%9)*.04));')
    S.parallax([("ctL1", .3), ("ctL2", .6)], 0, S.T, dx=-50)
    S.sfx(.2, "crowd", -10)
    S.cyto(360, 700, .5, z=29, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC,
           expr=[(S.w(13, "Welcome") - .05, 1.0, "hype")], x_expr=[(S.w(13, "stress"), 1.1, "determined")],
           points=[(S.w(13, "alarm") - .2, .8)], looks=[(S.w(13, "brain"), 14, -6)])
    mito_court_char(S, x=860, y=270, s=.66, pose="ball", expr=[(.3, 1.4, "hype"), (S.w(13, "brain"), 1.6, "determined")],
                    poses=[(1.2, "hype"), (S.w(13, "Welcome"), "ball")], pops=[(1.2, 1)], looks=[(S.w(13, "alarm"), .3, 0)])
    S.add(f'<div style="position:absolute;left:0;top:0;z-index:18">' + K.wrap(X.alarm_guy("al", "idle"), "alW", 1300, 300, .78, z=18) + '</div>')
    S.j(f'tl.fromTo("#alW",{{x:900}},{{x:0,duration:.8,ease:"power3.out"}},.6);tl.fromTo("#al",{{rotation:0}},{{rotation:4,duration:.2,yoyo:true,repeat:3,svgOrigin:"250 700"}},.6);'
        f'tl.set("#alP_idle",{{opacity:0}},{S.w(13, "alarm"):.3f});tl.set("#alP_flex",{{opacity:1}},{S.w(13, "alarm"):.3f});'
        f'tl.fromTo("#alglow",{{opacity:.2}},{{opacity:.9,duration:.25,yoyo:true,repeat:{int(S.T / .25)},immediateRender:false}},0);')
    S.sfx(.7, "siren", -9)
    S.punch(S.w(13, "alarm"), 1.08, .4, 1500, 500)
    S.tr_out("flash", .2)
    S.captions({"alarm": "#ff6b6b"})
    return S


@scene
def s05():
    """3D: the alarm signal runs down to the adrenal 'condos' on the kidneys; they fire hormone basketballs. Cyto calls it (PiP)."""
    t0 = gw(13, "signal") - .4; t1 = LINES[13]["t1"] + .15
    S = Scene("s05", t0, t1, music="court", bg="#3a1028")
    S.three3d("CON", "condos", 0, S.T, f"{{dur:{S.T:.3f},tFire:{S.w(13, 'pumping') - .2:.3f}}}", z=1)
    S.tr_in("flash", .2)
    S.popup("lbA", S.w(13, "adrenal") - .1, S.w(13, "they") - .15, "ADRENAL GLANDS", "= CONDOS ON YOUR KIDNEYS", "#ffa94d", 1240, 90, 1040)
    S.popup("lbB", S.w(13, "adrenaline") - .1, S.w(13, "cortisol") - .05, "HORMONE", "ADRENALINE", "#ff8a8a", 1240, 90, 760)
    S.popup("lbC", S.w(13, "cortisol") - .05, S.T - .05, "HORMONE", "CORTISOL", "#FFD166", 1240, 90, 760)
    S.over('<div id="pip" style="position:absolute;left:40px;top:560px;width:520px;height:340px;z-index:50;border-radius:24px;overflow:hidden;border:8px solid #FAF4E8;background:#20283a;box-shadow:0 14px 0 rgba(0,0,0,.35)">'
           '<div style="position:absolute;left:16px;top:10px;font:24px InterBlack;color:#ff3b3b;z-index:3">● LIVE</div></div>')
    S.cyto(300, 820, .42, z=51, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC,
           expr=[(S.w(13, "condos") - .05, .8, "hype")], x_expr=[(S.w(13, "adrenaline") - .1, 1.2, "shocked")],
           points=[(S.w(13, "kidneys") - .2, .7)], looks=[(S.w(13, "adrenal"), 14, -10)])
    S.j('tl.set("#cytoLayer",{clipPath:"inset(560px 1380px 180px 40px round 24px)"},0);')
    S.sfx(S.w(13, "pumping") - .2, "boing", -8); S.sfx(S.w(13, "adrenaline"), "boing", -8)
    S.tr_out("flash", .15)
    S.captions({"adrenal": "#ffa94d", "condos": "#ffa94d", "adrenaline": "#ff8a8a", "cortisol": "#FFD166"})
    return S



BEAR = ('<path d="M40 150 Q30 80 80 70 Q70 30 100 30 Q120 30 125 55 Q160 40 200 55 Q205 30 225 30 Q255 30 245 70 Q290 80 280 150 Q300 230 220 240 L100 240 Q20 230 40 150Z" fill="#7a4b2c" stroke="#0c1622" stroke-width="7"/>'
        '<circle cx="120" cy="130" r="11" fill="#0c1622"/><circle cx="200" cy="130" r="11" fill="#0c1622"/><ellipse cx="160" cy="175" rx="38" ry="28" fill="#c9965f" stroke="#0c1622" stroke-width="5"/><ellipse cx="160" cy="165" rx="14" ry="9" fill="#0c1622"/>')


def bubble(S, id_, t0, t1, inner, x, y, w=340, h=300):
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:55">'
           f'<svg width="{w}" height="{h + 80}" style="overflow:visible"><ellipse cx="{w / 2}" cy="{h / 2}" rx="{w / 2 - 6}" ry="{h / 2 - 6}" fill="#fff" stroke="#0c1622" stroke-width="7"/>'
           f'<circle cx="{w * .2}" cy="{h + 10}" r="18" fill="#fff" stroke="#0c1622" stroke-width="6"/><circle cx="{w * .1}" cy="{h + 50}" r="10" fill="#fff" stroke="#0c1622" stroke-width="5"/>'
           f'<g transform="translate({w / 2 - 160} {h / 2 - 135})">{inner}</g></svg></div>')
    S.j(f'tl.fromTo("#{id_}",{{scale:0,transformOrigin:"20% 100%"}},{{scale:1,duration:.3,ease:"back.out(2)"}},{t0:.3f});')


@scene
def s06():
    """MITO vs THE ALARM — play-by-play. Adrenaline, heart rate + breathing meters, sugar pass, the dunk, the bear, the subs."""
    t0 = LINES[13]["t1"] + .15; t1 = BEATS["countdown"][0]
    S = Scene("s06", t0, t1, music="court", bg="#5a1430")
    S.cap_lr = (720, 120)
    for l in X.court("ct"): S.add(l)
    S.add(X.desk("dk")); S.over(X.scoreboard("sb"))
    S.tr_in("flash", .15)
    S.j(f'document.querySelectorAll(".ctfan").forEach((f,i)=>tl.to(f,{{y:-10-(i%3)*4,duration:.22+(i%4)*.04,yoyo:true,repeat:{int(S.T / .22)},ease:"sine.inOut"}},(i%9)*.04));')
    l = {n: S.l(n) for n in range(14, 26)}
    dk0, dk1 = S.b("dunk"); sb0, sb1 = S.b("subbed")
    # meters (bars only)
    S.j(f'tl.to("#sbhr",{{scaleX:.78,duration:.5,ease:"back.out(2)"}},{S.w(15, "UP") - .1:.3f});tl.to("#sbbr",{{scaleX:.8,duration:.5,ease:"back.out(2)"}},{S.w(16, "UP") - .1:.3f});'
        f'tl.to("#sbhr",{{scaleX:.95,duration:.4}},{sb0:.3f});tl.to("#sbbr",{{scaleX:.95,duration:.4}},{sb0:.3f});')
    S.j(f'gsap.set("#sbheart",{{transformOrigin:"50% 50%"}});tl.fromTo("#sbheart",{{scale:1.25}},{{scale:1,duration:.5,repeat:{int(S.w(15, "Heart") / .5)},ease:"power2.out",immediateRender:false}},0);'
        f'tl.fromTo("#sbheart",{{scale:1.35}},{{scale:1,duration:.22,repeat:{int((S.T - S.w(15, "Heart")) / .22)},ease:"power2.out",immediateRender:false}},{S.w(15, "Heart"):.3f});')
    for n, w in ((15, "UP"), (16, "UP")):
        S.popup(f"up{n}", S.w(n, w) - .05, l[n][1] + .3, "", "↑ " + ("HEART RATE" if n == 15 else "BREATHING"), "#ff8a8a" if n == 15 else "#8ce2d6", 290, 270, 480)
        S.sfx(S.w(n, w) - .05, "buzzer", -12)
    # Cyto: play-by-play desk
    S.cyto(360, 700, .5, z=29, toque_extra=X.HEADSET, face_extra=X.HEADSET_MIC, phone=True,
           expr=[(S.w(15, "Adrenaline"), .8, "hype"), (S.w(17, "Mito") - .1, .8, "hype"), (dk0 + .2, 1.2, "shock"), (l[25][0], 1.1, "skeptic")],
           x_expr=[(S.w(19, "built"), 1.2, "determined"), (l[21][0], l[21][1] - l[21][0] + .4, "deadpan"), (S.w(23, "Again"), 2.0, "exhausted")],
           points=[(S.w(17, "paint") - .3, .7), (l[25][0], 1.0)], looks=[(S.w(17, "sugar"), 14, -8), (l[20][0] + .2, 14, -4)])
    # Mito
    S.char("mito", "mt", 820, 250, .66, pose="ball", who="MITO", z=21,
           poses=[(l[14][0], "hype"), (S.w(17, "Mito") + .2, "ball"), (dk0 - .1, "dunk"), (dk1 - .3, "idle"), (l[20][0], "point"),
                  (l[22][0], "idle"), (l[24][0], "shrug"), (l[25][0], "idle")],
           expr=[(l[14][0], l[14][1] - l[14][0] + .3, "hype"), (S.w(16, "Breathing"), 1.0, "determined"), (l[18][0], dk1 - l[18][0], "hype"),
                 (l[19][0] + 1, 1.6, "determined"), (l[20][0], 1.2, "worried"), (l[22][0] - .5, l[22][1] - l[22][0] + .8, "sideeye"),
                 (sb0, 1.4, "shocked"), (l[24][0], l[24][1] - l[24][0] + .4, "shocked"), (l[25][0], 1, "exhausted")],
           pops=[(l[14][0] + .1, 1), (dk0 + .05, 1.4)],
           looks=[(l[20][0] + .1, -.3, 0), (l[20][0] + .5, .3, 0), (l[20][0] + .9, -.3, -.2), (l[24][0] + .3, -.3, 0)])
    # the dunk: rise to the rim, backboard shatters, slow-mo, crowd
    S.j(f'tl.to("#mtW",{{x:560,y:-230,duration:.45,ease:"power2.out"}},{dk0:.3f});tl.to("#mtW",{{x:575,y:-205,duration:1.6,ease:"none"}},{dk0 + .45:.3f});'
        f'tl.to("#mtW",{{x:0,y:0,duration:.5,ease:"power2.inOut"}},{dk1 - .55:.3f});')
    S.j(f'tl.set("#ctshards",{{opacity:1}},{dk0 + .5:.3f});tl.set("#ctboard",{{opacity:0}},{dk0 + .5:.3f});'
        f'document.querySelectorAll(".ctshard").forEach((e,i)=>tl.fromTo(e,{{x:0,y:0,rotation:0}},{{x:(i%5-2)*90,y:200+(i%3)*120,rotation:(i%2?1:-1)*200,duration:1.8,ease:"power1.in",immediateRender:false}},{dk0 + .5:.3f}));'
        f'tl.set("#ctshards",{{opacity:0}},{dk1 + .5:.3f});tl.set("#ctboard",{{opacity:1}},{dk1 + .5:.3f});')
    S.j(f'tl.to(".ctfan",{{y:-46,duration:.18,yoyo:true,repeat:5,ease:"power2.out"}},{dk0 + .55:.3f});')
    S.over(f'<div id="lbx" class="clip" data-start="{dk0:.3f}" data-duration="{dk1 - dk0:.3f}" style="position:absolute;inset:0;z-index:66;pointer-events:none;box-shadow:inset 0 120px 0 #000, inset 0 -120px 0 #000"></div>'
           f'<div id="slomo" class="pop clip" data-start="{dk0 + .3:.3f}" data-duration="{dk1 - dk0 - .5:.3f}" style="left:1480px;top:30px;font:54px InterBlack;color:#FFD166;z-index:67">SLOW-MO</div>')
    S.snapzoom(dk0 + .45, 1.3, dk1 - dk0 - .8, 1600, 330, .4)
    S.sfx(dk0 + .5, "shatter", -2); S.sfx(dk0 + .6, "crowd", -4); S.sfx(dk0 + .45, "slam", -2)
    # THE ALARM + its subs
    S.add(K.wrap(X.alarm_guy("al", "defend"), "alW", 1320, 300, .74, z=19))
    S.add(K.wrap(X.alarm_guy("al2", "defend"), "al2W", 1520, 330, .7, z=18))
    S.add(K.wrap(X.alarm_guy("al3", "flex"), "al3W", 1080, 340, .68, z=17))
    S.j(f'tl.fromTo(["#alglow","#al2glow","#al3glow"],{{opacity:.2}},{{opacity:.9,duration:.25,yoyo:true,repeat:{int(S.T / .25)},immediateRender:false}},0);'
        f'tl.to("#alW",{{x:900,duration:.4,ease:"power2.in"}},{dk0:.3f});tl.to("#alW",{{x:0,duration:.6,ease:"power3.out"}},{sb0:.3f});'
        f'tl.set(["#al2W","#al3W"],{{x:300,opacity:0}},0);tl.to("#al2W",{{x:0,opacity:1,duration:.35,ease:"back.out(1.4)"}},{S.w(23, "Again") - .1:.3f});tl.to("#al3W",{{x:0,opacity:1,duration:.35,ease:"back.out(1.4)"}},{S.w(23, "again", after=S.w(23, "Again") + .1) - .1:.3f});')
    for t in (sb0, S.w(23, "Again") - .1, S.w(23, "again", after=S.w(23, "Again") + .1) - .1):
        S.sfx(t, "siren_short", -10); S.sfx(t, "buzzer", -12)
    for t in (S.w(23, "phone") - .1, S.w(23, "Again") - .3, S.w(23, "again", after=S.w(23, "Again") + .1) - .3):
        buzz(S, t, .3)
    S.popup("sub", sb0 + .1, sb0 + 1.4, "SUBSTITUTION", "THE ALARM (AGAIN)", "#ff8a8a", 290, 260, 480)
    S.j(f'tl.to("#mtW",{{x:-260,duration:.35,ease:"power3.in"}},{sb0 + .2:.3f});tl.to("#mtW",{{x:0,duration:.5,ease:"power2.out"}},{sb1 + .2:.3f});')
    # sugar pass
    S.add(f'<div id="sugar" class="clip" data-start="{S.w(17, "sugar") - .2:.3f}" data-duration="{S.w(18, "I") - S.w(17, "sugar") + .2:.3f}" style="position:absolute;left:0;top:0;width:120px;height:120px;z-index:22">'
          '<svg width="120" height="120"><rect x="10" y="10" width="100" height="100" rx="18" fill="#fff" stroke="#0c1622" stroke-width="7"/><text x="60" y="72" text-anchor="middle" font-family="InterBlack" font-size="26" fill="#0c1622">SUGAR</text></svg></div>')
    S.j(f'tl.fromTo("#sugar",{{x:400,y:120,rotation:0}},{{x:1150,y:330,rotation:540,duration:{S.w(17, "paint") - S.w(17, "sugar") + .1:.3f},ease:"power1.in"}},{S.w(17, "sugar") - .2:.3f});')
    S.sfx(S.w(17, "paint"), "catch", -6)
    # the bear (thought bubble) + the group chat reveal
    bubble(S, "bear", S.w(19, "bear") - .1, l[21][1] + .2, BEAR, 520, 270)
    S.over(f'<div id="bearX" class="pop clip" data-start="{S.w(21, "no"):.3f}" data-duration="{l[21][1] - S.w(21, "no") + .2:.3f}" style="left:600px;top:310px;font:220px/1 InterBlack;color:#e63946;-webkit-text-stroke:6px #0c1622">X</div>')
    S.j(f'tl.fromTo("#bearX",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:.18,ease:"power4.in"}},{S.w(21, "no"):.3f});')
    S.snapzoom(S.w(21, "group") - .05, 1.3, .9, 520, 640)
    S.sfx(S.w(19, "bear"), "roar", -10)
    S.punch(l[24][0], 1.12, .45, 1100, 500)
    S.tr_out("whip", .3)
    S.captions({"up": "#ff8a8a", "him": "#FFD166", "bear": "#c9965f", "groupchat": "#8ce2d6", "again": "#ff8a8a"})
    return S



def src_chip(S, id_, t0, t1, txt, x=60, y=60):
    S.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x}px;top:{y}px;padding:12px 22px;border-radius:14px;background:#0c1622;border:4px solid #FAF4E8;font:34px InterBlack;color:#FAF4E8">{txt}</div>')
    S.j(f'tl.fromTo("#{id_}",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.25,ease:"power3.out"}},{t0:.3f});')


def flipsign(S, id_, t, txt0, txt1, x=80, y=60, w=620):
    S.add(f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:120px;z-index:9;perspective:800px">'
          f'<div style="position:absolute;left:{w // 2 - 4}px;top:-80px;width:8px;height:80px;background:#333"></div>'
          f'<div id="{id_}a" style="position:absolute;inset:0;border-radius:14px;background:#151a24;border:6px solid #0c1622;font:50px/108px InterBlack;color:#FFD166;text-align:center">{txt0}</div>'
          f'<div id="{id_}b" style="position:absolute;inset:0;border-radius:14px;background:#151a24;border:6px solid #0c1622;font:50px/108px InterBlack;color:#ff8a8a;text-align:center;opacity:0">{txt1}</div></div>')
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


@scene
def s07():
    """IT DRAGS ON — countdown sign, Mito gassed on the bench, the cortisol gag, Neutro vs. a crumb."""
    t0 = BEATS["countdown"][0]; t1 = gw(32, "And")
    S = Scene("s07", t0, t1, music="moody", bg="#2a1030")
    for l in X.court("ct"): S.add(l)
    S.add('<div class="fill" style="z-index:5;background:linear-gradient(rgba(20,10,60,.55),rgba(10,5,30,.65))"></div>')
    S.add(X.layer("bench", BENCH, 6))
    S.tr_in("whip", .3)
    flipsign(S, "cd", .5, "12 DAYS TILL BREAK", "10 DAYS TILL BREAK", 80, 120)
    S.parallax([("ctL1", .2), ("ctL2", .4), ("bench", .5)], 0, S.T, dx=-60)
    l = {n: S.l(n) for n in range(26, 33)}
    cb0, cb1 = S.b("crumb"); bn0, _ = S.b("bench")
    S.cyto(560, 650, .62, expr=[(l[26][0] + 3.4, 1.1, "squint"), (S.w(28, "stop"), 1.0, "sad"), (l[30][0], 1.1, "skeptic")],
           x_expr=[(l[26][0] + .2, 1.4, "smug"), (S.w(28, "Cortisol"), 1.4, "determined"), (S.w(28, "inflammation"), 1.6, "worried"), (cb0, 1.1, "shocked"), (l[32][0], 2.0, "sideeye")],
           points=[(S.w(28, "Carnegie"), .7), (l[30][0] + .1, .9)], shrugs=[(S.w(26, "days") - .1, .8)], sips=[(l[27][1] + .1, 1.2)],
           looks=[(bn0, 14, 0), (cb0 + .1, 14, 6), (l[32][0] + 1.3, -10, 0)])
    S.char("mito", "mt", 1270, 190, .66, pose="slump", gassed=True, who="MITO", z=21,
           expr=[(0, S.T, "exhausted")], shut_at=[(l[27][1] + .6, 2.0)], nods=[l[27][0] + .2], bob=True)
    S.j(f'tl.fromTo("#mtsweat",{{y:0,opacity:1}},{{y:30,opacity:0,duration:1.2,repeat:{int(S.T / 1.2)},ease:"power1.in",immediateRender:false}},0);')
    # cortisol gag (quick, with Cyto reacting): megaphone -> immune cell puts headphones on -> flames won't go out
    a0 = S.w(28, "Cortisol") - .1; a1 = S.w(28, "But", after=a0) - 1.9
    S.over(f'<div id="cg" class="pop clip" data-start="{a0:.3f}" data-duration="{a1 - a0 + 2.6:.3f}" style="left:900px;top:150px;width:900px;height:330px;z-index:50;border-radius:28px;background:#FAF4E8;border:7px solid #0c1622;box-shadow:0 14px 0 rgba(0,0,0,.35)">'
           f'<svg width="900" height="330"><g transform="translate(40 110)">{CORT}</g>'
           f'<g id="cgtxt"><rect x="250" y="40" width="300" height="70" rx="20" fill="#fff" stroke="#0c1622" stroke-width="5"/><text x="400" y="86" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">AIGHT, CALM DOWN</text></g>'
           f'<g transform="translate(600 90)">{IMM}</g><g id="cgfl" opacity="0"><g transform="translate(330 170)">{FLAME}</g><g transform="translate(420 190) scale(.8)">{FLAME}</g><g transform="translate(500 170)">{FLAME}</g></g>'
           f'<text x="450" y="315" text-anchor="middle" font-family="InterBlack" font-size="28" fill="#e63946" id="cglab" opacity="0">INFLAMMATION</text></svg></div>')
    S.j(f'tl.fromTo("#cg",{{y:-500}},{{y:0,duration:.35,ease:"back.out(1.5)"}},{a0:.3f});tl.set("#hph",{{opacity:1}},{S.w(28, "stop"):.3f});'
        f'tl.fromTo("#hph",{{y:-60}},{{y:0,duration:.25,ease:"bounce.out"}},{S.w(28, "stop"):.3f});tl.set("#cgtxt",{{opacity:.25}},{S.w(28, "listening"):.3f});'
        f'tl.set(["#cgfl","#cglab"],{{opacity:1}},{S.w(28, "inflammation"):.3f});tl.fromTo("#cgfl",{{scaleY:.9,transformOrigin:"50% 100%"}},{{scaleY:1.12,duration:.18,yoyo:true,repeat:30,immediateRender:false}},{S.w(28, "inflammation"):.3f});'
        f'tl.to("#cg",{{y:-600,duration:.3,ease:"power3.in"}},{a1 + 1.6:.3f});')
    # sight gags after the card: the immune cell (headphones on) pops next to Cyto, flames at Mito's feet won't go out
    g0 = S.w(28, "immune", after=a1) - .2; g1 = l[28][1] + .4
    S.over(f'<div id="imm2" class="pop clip" data-start="{g0:.3f}" data-duration="{g1 - g0:.3f}" style="left:880px;top:330px;z-index:50"><svg width="260" height="200" viewBox="-10 -40 240 220">{IMM.replace('id="hph"', 'id="hph2"')}</svg></div>'
           f'<div id="fl2" class="pop clip" data-start="{S.w(28, "inflammation"):.3f}" data-duration="{g1 - S.w(28, "inflammation"):.3f}" style="left:1300px;top:780px;z-index:23"><svg width="300" height="130" viewBox="0 0 300 130">'
           f'<g transform="translate(0 10)">{FLAME}</g><g transform="translate(100 20) scale(.8)">{FLAME}</g><g transform="translate(190 10)">{FLAME}</g></svg></div>')
    S.j(f'tl.fromTo("#imm2",{{scale:0}},{{scale:1,duration:.3,ease:"back.out(2)"}},{g0:.3f});tl.set("#hph2",{{opacity:0}},0);tl.set("#hph2",{{opacity:1}},{S.w(28, "stop"):.3f});'
        f'tl.fromTo("#hph2",{{y:-60}},{{y:0,duration:.25,ease:"bounce.out",immediateRender:false}},{S.w(28, "stop"):.3f});'
        f'tl.fromTo("#fl2",{{scaleY:.85,transformOrigin:"50% 100%"}},{{scaleY:1.1,duration:.16,yoyo:true,repeat:{int((g1 - S.w(28, "inflammation")) / .16)},immediateRender:false}},{S.w(28, "inflammation"):.3f});')
    src_chip(S, "src1", S.w(28, "Carnegie") - .1, l[28][1], "COHEN ET AL. · PNAS 2012", 1180, 140)
    S.sfx(S.w(28, "stop"), "pop", -8)
    # Neutro: jittery, spins at the crumb, radios for backup
    S.add('<div id="crumb" style="position:absolute;left:990px;top:840px;z-index:7"><svg width="70" height="50"><path d="M6 44 L20 10 L52 6 L64 38Z" fill="#d9a35b" stroke="#0c1622" stroke-width="4"/></svg></div>')
    S.char("neutro", "nt", 2000, 330, .7, pose="idle", who="NEUTRO", z=22,
           poses=[(cb0 + .5, "radio"), (l[31][0], "point"), (l[32][0] + .4, "cross")],
           expr=[(cb0, cb1 - cb0 + l[29][1] - l[29][0] + .2, "determined"), (l[31][0], 1.6, "sideeye"), (l[32][0], 2.4, "deadpan")],
           looks=[(cb0 + .3, -.3, .2), (l[30][0] + .3, -.3, 0)])
    S.j(f'tl.to("#ntW",{{x:-1100,duration:.4,ease:"power3.out"}},{cb0 - .5:.3f});'
        f'tl.to("#nt",{{scaleX:-1,duration:.08,svgOrigin:"300 650",yoyo:true,repeat:3}},{cb0:.3f});'
        f'tl.to("#ntW",{{x:-1040,duration:.07,yoyo:true,repeat:9}},{cb0 + .1:.3f});')
    S.sfx(cb0, "whoosh", -10); S.sfx(cb0 + .5, "radio", -6)
    S.snapzoom(cb0 + .3, 1.5, cb1 - cb0, 1030, 760, .35)
    S.punch(l[30][0], 1.12, .45, 560, 600)
    S.tr_out("iris", .3)
    S.captions({"cortisol": "#FFD166", "carnegie": "#8ce2d6", "mellon": "#8ce2d6", "cooked": "#ff8a8a", "crumb": "#d9a35b"})
    return S


@scene
def s08():
    """3D: Rhino's heist at the nose (front door): ducking under laser beams. Silent villain, heist music."""
    t0 = gw(32, "And"); t1 = BEATS["heist"][1]
    S = Scene("s08", t0, t1, music="heist", bg="#2a0a14")
    S.three3d("LAS", "lasers", 0, S.T, "{}", z=1)
    S.tr_in("iris", .3)
    S.popup("fd", .4, S.T - .3, "LOCATION", "FRONT DOOR = YOUR NOSE", "#ff8a8a", 960, 60, 860)
    S.char("rhino", "rh", -380, 520, .95, pose="sneak", z=30, expr=[(0, S.T, "smug")], blinks=[],
           poses=[(1.0, "duck"), (2.2, "spread"), (3.2, "sneak"), (4.4, "duck"), (5.6, "wave")])
    S.j(f'tl.to("#rhW",{{x:900,duration:{S.T - 1:.3f},ease:"sine.inOut"}},.2);tl.to("#rh",{{y:-20,duration:.3,yoyo:true,repeat:{int(S.T / .3)},ease:"sine.inOut"}},0);'
        f'tl.to("#rh",{{rotation:360,duration:.6,svgOrigin:"200 260",ease:"power2.inOut"}},2.4);tl.set("#rh",{{rotation:0}},3.05);')
    S.sfx(.2, "tiptoe", -8); S.sfx(2.4, "whoosh", -10); S.sfx(S.T - 1.2, "gulp", -8)
    S.tr_out("flash", .3)
    S.captions({"officer": "#ff8a8a"})
    return S


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


@scene
def s09():
    """COLD CASE: 1991 — film-noir. Neutro in a trench coat reads the case file; reenactment; the numbers; "Bro, WHAT."; colour snaps back."""
    import math as _m
    t0 = BEATS["heist"][1]; t1 = BEATS["smirk"][1]
    S = Scene("s09", t0, t1, music="noir", bg="#111")
    for l in X.noir("nr"): S.add(l)
    S.tr_in("flash", .3)
    nb0, nb1 = S.b("noir"); re0, re1 = S.b("reenact"); si0, si1 = S.b("silence"); sm0, sm1 = S.b("smirk")
    l = {n: S.l(n) for n in range(33, 43)}
    tc = l[42][0] - .1                       # colour snaps back
    S.j(f'tl.set("#cam",{{filter:"grayscale(1) contrast(1.25) brightness(.95)"}},0);tl.set("#cam",{{filter:"none"}},{tc:.3f});')
    S.over(f'<div id="grain" class="static clip" data-start="0" data-duration="{tc:.3f}" style="position:absolute;inset:0;z-index:60;opacity:.07;pointer-events:none"></div>')
    S.j(f'tl.fromTo("#grain",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"53px 29px",duration:.05,repeat:{int(tc / .05)},ease:"steps(1)",immediateRender:false}},0);')
    S.j(f'tl.fromTo("#nrrain",{{y:-60}},{{y:0,duration:.35,repeat:{int(S.T / .35)},ease:"none",immediateRender:false}},0);')
    S.j(f'tl.fromTo("#nrlamp",{{opacity:1}},{{opacity:.6,duration:.06,yoyo:true,repeat:5,immediateRender:false}},{nb0 + .2:.3f});')
    S.sfx(0, "rain", -12); S.sfx(nb0 + .1, "sax", -4)
    S.over(f'<div id="cct" class="clip" data-start="{nb0 + .1:.3f}" data-duration="{l[33][1] + .2:.3f}" style="position:absolute;left:0;right:0;top:330px;text-align:center;z-index:70;font:120px InterBlack;color:#f0f0f0;-webkit-text-stroke:5px #000;paint-order:stroke fill">COLD CASE: 1991</div>')
    S.j(f'tl.fromTo("#cct",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.9,ease:"steps(15)"}},{nb0 + .1:.3f});')
    S.sfx(nb0 + .1, "typewriter", -8)
    # cast: Neutro (trench) behind the desk, Cyto across from him
    S.char("neutro", "nt", 760, 210, .78, pose="notepad", who="NEUTRO", z=20, trench=True,
           poses=[(l[34][0], "idle"), (l[38][0], "point"), (l[41][0], "cross")],
           expr=[(0, l[35][0], "deadpan"), (l[36][0], 1.2, "deadpan"), (l[38][0], l[39][1] - l[38][0], "determined"), (l[41][0], 1.6, "smug")],
           nods=[l[33][1] - .2, l[36][0] + .3, l[41][0] + .2], looks=[(l[35][0] + .1, -.3, 0)])
    S.cyto(360, 760, .66, z=35, expr=[(l[35][0] - .05, 1.0, "shock"), (si0 + .1, si1 - si0 + l[40][1] - l[40][0] + .3, "shock")],
           x_expr=[(l[34][0] + 1, 2.5, "sideeye"), (l[38][0] + 1.0, 2.5, "worried"), (l[42][0] + .1, 2.5, "determined"), (sm0, 1.2, "worried")],
           looks=[(l[33][0], 12, -4), (l[38][0] + .3, 14, -10), (sm0 + .1, -14, 0)], tilts=[(l[42][0] + 1.5, .7, 6)], shrugs=[(S.w(42, "Yeah"), .7)])
    S.j(f'tl.fromTo("#nrfile",{{y:0}},{{y:-14,duration:.12,yoyo:true,repeat:1,immediateRender:false}},{l[33][0]:.3f});')
    # case photos (grainy) slide onto the board while he talks
    S.over(f'<div id="ph1" class="pop clip" data-start="{S.w(34, "volunteers") - .2:.3f}" data-duration="{l[35][0] - S.w(34, "volunteers") + .1:.3f}" style="left:1120px;top:150px;width:660px;height:430px;z-index:40;background:#e8e8e8;border:10px solid #fff;box-shadow:0 12px 0 rgba(0,0,0,.4);transform:rotate(3deg)">'
           f'<svg width="640" height="410" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice"><rect width="1920" height="1080" fill="#cfcfcf"/>'
           + "".join(f'<path d="M0 {y} H1920" stroke="#999" stroke-width="6"/>' for y in range(200, 1000, 120)) + "".join(VOL(x) for x in (300, 700, 1100, 1500)).replace('560)', '300)') + '</svg>'
           f'<div style="position:absolute;left:0;right:0;bottom:-58px;text-align:center;font:34px InterBlack;color:#111;background:#fff">~400 VOLUNTEERS</div></div>')
    S.j(f'tl.fromTo("#ph1",{{x:900,rotation:20}},{{x:0,rotation:3,duration:.35,ease:"back.out(1.4)"}},{S.w(34, "volunteers") - .2:.3f});')
    S.sfx(S.w(34, "volunteers") - .1, "click", -6)
    src_chip(S, "src2", S.w(34, "Scientists"), l[37][1], "COHEN, TYRRELL & SMITH · NEJM 1991", 60, 60)
    S.punch(l[35][0], 1.18, .5, 360, 640)
    # reenactment reel: scientists with eye-droppers, volunteers, tiny Rhinos dropping in
    drops = "".join(f'<g class="trh" transform="translate({340 + i * 400} 380)">{TINYRH}</g>' for i in range(4))
    S.over(f'<div id="reel" class="clip" data-start="{S.w(34, "dripped") - .2:.3f}" data-duration="{l[37][1] - S.w(34, "dripped") + .4:.3f}" style="position:absolute;inset:0;z-index:45">'
           + reel("".join(SCI(x) for x in (340, 740, 1140, 1540)) + drops + "".join(VOL(x) for x in (340, 740, 1140, 1540))
                  + '<text x="1820" y="130" text-anchor="end" font-family="InterBlack" font-size="34" fill="#111">REENACTMENT</text>') + '</div>')
    S.j(f'document.querySelectorAll(".trh").forEach((e,i)=>tl.fromTo(e,{{y:0,opacity:0}},{{y:260,opacity:1,duration:.6,ease:"power2.in",repeat:3,repeatDelay:.25,immediateRender:false}},{re0:.3f}+i*.15));'
        f'tl.fromTo("#reel",{{scale:1.05}},{{scale:1,duration:.3}},{S.w(34, "dripped") - .2:.3f});')
    S.sfx(re0 + .1, "drip", -6); S.sfx(re0 + .9, "drip", -6)
    # the numbers (one quick 'evidence' board, Neutro pointing, Cyto reacting)
    b0 = l[38][0] - .1; b1 = si0 + .1
    def bar(id_, lab, v, col, y):
        return (f'<div style="position:absolute;left:30px;top:{y}px;font:34px InterBlack;color:#111">{lab}</div>'
                f'<div style="position:absolute;left:30px;top:{y + 44}px;width:560px;height:46px;background:#bbb;border:4px solid #111"><div id="{id_}" style="width:{v}%;height:100%;background:{col};transform-origin:0 50%"></div></div>'
                f'<div id="{id_}n" style="position:absolute;left:600px;top:{y + 44}px;font:42px InterBlack;color:#111">{v}%</div>')
    S.over(f'<div id="ev" class="pop clip" data-start="{b0:.3f}" data-duration="{b1 - b0:.3f}" style="left:1100px;top:130px;width:720px;height:520px;z-index:40;background:#efefef;border:8px solid #111;box-shadow:0 12px 0 rgba(0,0,0,.4)">'
           f'<div style="position:absolute;left:30px;top:16px;font:30px InterBlack;color:#555">INFECTED</div>'
           + bar("evA", "LOW STRESS", 74, "#666", 56) + bar("evB", "HIGH STRESS", 90, "#111", 156)
           + '<div style="position:absolute;left:30px;top:270px;font:30px InterBlack;color:#555">ACTUAL COLDS</div>'
           + bar("evC", "LOW STRESS", 27, "#666", 310) + bar("evD", "HIGH STRESS", 47, "#111", 410) + '</div>')
    S.j(f'tl.fromTo("#ev",{{y:-700}},{{y:0,duration:.35,ease:"back.out(1.3)"}},{b0:.3f});')
    for i, (k, w) in enumerate((("evA", S.w(38, "seventy")), ("evB", S.w(38, "ninety")), ("evC", S.w(39, "Twenty")), ("evD", S.w(39, "forty")))):
        S.j(f'tl.fromTo("#{k}",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.out"}},{w - .05:.3f});tl.fromTo("#{k}n",{{opacity:0}},{{opacity:1,duration:.1}},{w + .2:.3f});')
        S.sfx(w, "stamp", -8)
    # silence -> shake + snap zoom -> "Bro, WHAT."
    S.j(f'tl.to(".settxt",{{opacity:0,duration:.05}},{si0 + .8:.3f});tl.to(".settxt",{{opacity:1,duration:.1}},{l[41][0] + .1:.3f});')
    S.shake(si0 + .9, .5, 18); S.snapzoom(si0 + .85, 1.45, si1 - si0 + l[40][1] - l[40][0] - .5, 360, 640, .3)
    S.sfx(l[41][0] + .5, "slam", -4)
    S.j(f'tl.to("#nrfile",{{y:-30,duration:.1,yoyo:true,repeat:1}},{l[41][0] + .4:.3f});')
    # colour snaps back; Rhino peeks from behind the door frame and smirks
    S.sfx(tc, "whoosh", -8)
    S.char("rhino", "rh", 1560, 420, .7, pose="idle", z=21, expr=[(sm0, sm1 - sm0, "smug")], blinks=[])
    S.j(f'tl.set("#rhW",{{x:420}},0);tl.to("#rhW",{{x:0,duration:.35,ease:"back.out(1.6)"}},{sm0:.3f});')
    S.sfx(sm0 + .3, "sting", -6)
    S.tr_out("whip", .3)
    S.captions({"purpose": "#ff8a8a", "seventyfour": "#FAF4E8", "ninety": "#ff8a8a", "fortyseven": "#ff8a8a", "what": "#ff8a8a"})
    return S



def lever_pull(S, p, t):
    S.j(f'gsap.set("#{p}lever",{{svgOrigin:"1255 545"}});tl.to("#{p}lever",{{rotation:180,duration:.12,ease:"power3.in"}},{t:.3f});tl.to("#{p}lever",{{rotation:0,duration:.3,ease:"back.out(2)"}},{t + .35:.3f});')
    S.sfx(t + .08, "clunk", -6)


@scene
def s10():
    """THE TWIST — the alarm is still going. Security-cam footage: Cyto yanks the lever every time his phone buzzes."""
    t0 = BEATS["smirk"][1]; t1 = BEATS["to_heart"][0] + .8
    S = Scene("s10", t0, t1, music="alarm_low", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    alarm_on(S, "hq", 0, S.T, beams=False)
    S.tr_in("whip", .3)
    l = {n: S.l(n) for n in range(43, 48)}
    c0, c1 = S.b("seccam")
    S.cyto(560, 650, .6, phone=True, expr=[(l[44][0] - .05, .8, "skeptic"), (c1 - .1, l[45][1] - c1 + .1, "shock")],
           x_expr=[(l[46][0], .9, "worried"), (l[47][0], 2.8, "smug")], looks=[(l[43][0] + .3, 14, -2), (c1 + .3, 14, 0), (c1 + .7, -10, -6), (l[46][0] + .2, 14, -2)],
           shrugs=[(l[47][0] + .2, 1.0)], tilts=[(l[47][0] + 1.4, .9, -8)])
    S.char("neutro", "nt", 1290, 300, .74, pose="radio", who="NEUTRO",
           poses=[(l[43][1], "cross"), (l[46][0], "idle")],
           expr=[(0, l[43][1], "determined"), (l[44][0], 1.2, "sideeye"), (c1, l[46][1] - c1 + .2, "deadpan"), (l[47][0] + .4, 2.2, "smug")],
           looks=[(l[43][1], -.3, 0), (l[46][0] + .1, -.3, 0)], nods=[l[47][1] - .4])
    S.j(f'tl.fromTo("#ntW",{{x:0}},{{x:-6,duration:.05,yoyo:true,repeat:{int(l[43][1] / .05)},immediateRender:false}},0);')    # jumpy
    # security-cam cutaway (grainy, green, timestamp, REC) — Cyto on the beanbag pulling the lever without looking
    pulls = [c0 + .6, c0 + 1.5, c0 + 2.4]
    S.over(f'<div id="cam2" class="clip" data-start="{c0:.3f}" data-duration="{c1 - c0:.3f}" style="position:absolute;inset:0;z-index:72;background:#000;overflow:hidden">'
           f'<div id="camI" style="position:absolute;inset:0;transform-origin:960px 540px;filter:grayscale(1) sepia(1) hue-rotate(60deg) saturate(1.6) contrast(1.3) brightness(.85)">'
           + "".join(X.hq("sc")[:3]) +
           f'<div style="position:absolute;inset:0;z-index:5">{K.wrap(K.rhino_html("zz", "idle"), "zzW", -900, 0, .1)}</div>'
           f'<div id="scCy" style="position:absolute;left:0;top:0;z-index:6"><svg viewBox="0 0 1200 1200" width="1200" height="1200" style="position:absolute;left:{1000 - 600 * .5:.0f}px;top:{640 - 640 * .5:.0f}px;transform:scale(.5);transform-origin:0 0;overflow:visible">'
           f'<circle cx="600" cy="640" r="300" fill="#3fc1b0" stroke="#0c1622" stroke-width="8"/><ellipse cx="600" cy="300" rx="290" ry="140" fill="#1e56ac" stroke="#0c1622" stroke-width="8"/>'
           f'<ellipse cx="520" cy="640" rx="40" ry="26" fill="#fff" stroke="#0c1622" stroke-width="6"/><ellipse cx="660" cy="640" rx="40" ry="26" fill="#fff" stroke="#0c1622" stroke-width="6"/><circle cx="520" cy="652" r="16" fill="#0c1622"/><circle cx="660" cy="652" r="16" fill="#0c1622"/>'
           f'<rect x="440" y="760" width="110" height="180" rx="16" fill="#1b1f2a" stroke="#0c1622" stroke-width="7"/><rect x="452" y="776" width="86" height="148" rx="6" fill="#8ce2d6"/>'
           f'<g id="scArm"><path d="M840 650 Q980 560 1010 420" fill="none" stroke="#0c1622" stroke-width="78" stroke-linecap="round"/><path d="M840 650 Q980 560 1010 420" fill="none" stroke="#188076" stroke-width="62" stroke-linecap="round"/><circle cx="1010" cy="410" r="50" fill="#3fc1b0" stroke="#0c1622" stroke-width="7"/></g></svg></div>'
           f'</div>'
           f'<div class="static" id="scN" style="position:absolute;inset:0;opacity:.12"></div>'
           f'<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.25) 0 2px,transparent 2px 5px)"></div>'
           f'<div style="position:absolute;left:60px;top:44px;font:44px InterBlack;color:#e8ffe8;text-shadow:0 0 8px #000">CAM 1 · HQ</div>'
           f'<div id="rec" style="position:absolute;left:1600px;top:44px;font:44px InterBlack;color:#ff4d4d">● REC</div>'
           f'<div style="position:absolute;left:60px;top:120px;font:38px InterBlack;color:#e8ffe8;text-shadow:0 0 8px #000">DEC 06 2026 · 06:00</div></div>')
    S.j(f'tl.fromTo("#scN",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"41px 77px",duration:.05,repeat:{int((c1 - c0) / .05)},ease:"steps(1)",immediateRender:false}},{c0:.3f});'
        f'tl.fromTo("#rec",{{opacity:1}},{{opacity:0,duration:.4,yoyo:true,repeat:{int((c1 - c0) / .4)},ease:"steps(1)",immediateRender:false}},{c0:.3f});'
        f'tl.fromTo("#camI",{{scale:1}},{{scale:1.18,duration:{c1 - c0:.3f},ease:"none",immediateRender:false}},{c0:.3f});'
        f'gsap.set("#scArm",{{svgOrigin:"840 650"}});')
    for t in pulls:
        S.j(f'tl.to("#scArm",{{rotation:40,duration:.12,ease:"power3.in"}},{t:.3f});tl.to("#scArm",{{rotation:0,duration:.3,ease:"power2.out"}},{t + .3:.3f});')
        lever_pull(S, "sc", t)
        S.over(f'<div id="bz{int(t * 10)}" class="pop clip" data-start="{t - .25:.3f}" data-duration=".5" style="left:800px;top:280px;z-index:73;font:50px InterBlack;color:#e8ffe8">BZZT</div>')
        S.sfx(t - .25, "buzz", -6)
    S.sfx(c0, "static", -10)
    S.j(f'tl.to(".settxt",{{opacity:0,duration:.05}},{c0 - .05:.3f});tl.to(".settxt",{{opacity:1,duration:.1}},{c1:.3f});')
    # the twist reaction: silent holds, then the confession
    S.snapzoom(c1 + .05, 1.15, l[45][1] - c1, 560, 600, .2)
    S.snapzoom(l[46][0] + .02, 1.15, .85, 1530, 500, .2)
    S.punch(l[47][0], 1.1, .5, 560, 600)
    S.sfx(l[47][0] + .2, "sting", -8)
    S.tr_out("iris", .4)
    S.captions({"who": "#FFD166", "me": "#FFD166", "ahlie": "#FFD166"})
    return S


@scene
def s11():
    """SERIOUS BEAT — downtown (the heart), 3D, calm. Cup down."""
    t0 = BEATS["to_heart"][0] + .8; t1 = BEATS["to_cheats"][0] + .4
    S = Scene("s11", t0, t1, music="calm", bg="#1d2240")
    S.three3d("HRT", "heart", 0, S.T, "{}", z=1)
    S.tr_in("iris", .4)
    l = {n: S.l(n) for n in range(48, 51)}
    S.add('<div class="fill" style="z-index:2;background:linear-gradient(90deg,rgba(13,18,40,.75),rgba(13,18,40,0) 45%)"></div>')
    S.cyto(380, 700, .62, z=20, expr=[(S.w(48, "Not"), 1.2, "sad")], x_expr=[(l[48][0] + .2, 1.6, "determined"), (S.w(49, "Call") - .1, 1.8, "determined")],
           looks=[(S.w(48, "Christmas"), 14, -10)], points=[(S.w(49, "Call") - .1, 1.0)])
    S.j(C.cup_down(.6, S.T + 1))
    S.popup("hb1", S.w(48, "Some") - .1, S.w(48, "Not") - .1, "SOME STUDIES", "MORE HEART ATTACKS AROUND THE HOLIDAYS", "#ff8a8a", 1260, 90, 1000)
    S.popup("hb2", S.w(48, "Not"), S.w(48, "But") - .1, "TO BE FAIR", "NOT EVERY STUDY", "#8ce2d6", 1260, 90, 760)
    S.popup("hb3", S.w(48, "stress") - .1, l[48][1] + .2, "POSSIBLE REASONS", "STRESS · BIG MEALS · SALT · ALCOHOL · WAITING TOO LONG", "#FFD166", 1260, 90, 1040)
    S.popup("hb4", S.w(49, "Call") - .15, S.T - .2, "CHEST PAIN?", "DON'T WAIT. CALL 911.", "#ff6b6b", 1260, 90, 860)
    src_chip(S, "src3", S.w(48, "Some"), l[48][1], "KLONER 2006 · MILNE 2005 · WEERASINGHE 2002", 1000, 360)
    S.char("neutro", "nt", 2000, 300, .7, pose="idle", who="NEUTRO", z=19, expr=[(l[50][0] - .4, 2, "determined")], nods=[l[50][0] + .2])
    S.j(f'tl.to("#ntW",{{x:-560,duration:.4,ease:"power3.out"}},{l[50][0] - .6:.3f});')
    S.tr_out("whip", .3)
    S.captions({"911": "#ff6b6b", "nine": "#ff6b6b", "one": "#ff6b6b"})
    return S



def hq_cast(S, cy=(430, 650, .58), mito=None, neutro=None):
    pass


def breath_ring(S, t0, tin, tout):
    S.over(f'<div id="ring" class="clip" data-start="{t0:.3f}" data-duration="{tout - t0 + .4:.3f}" style="position:absolute;left:760px;top:140px;width:400px;height:400px;z-index:55">'
           '<svg width="400" height="400"><circle id="ringC" cx="200" cy="200" r="150" fill="rgba(140,226,214,.18)" stroke="#8ce2d6" stroke-width="14"/></svg>'
           '<div id="ringT" style="position:absolute;left:0;right:0;top:170px;text-align:center;font:46px InterBlack;color:#FAF4E8;-webkit-text-stroke:2px #0c1622">IN...</div></div>')
    S.j(f'gsap.set("#ringC",{{transformOrigin:"200px 200px"}});tl.fromTo("#ringC",{{scale:.4}},{{scale:1.15,duration:{tin - t0:.3f},ease:"sine.inOut"}},{t0:.3f});'
        f'tl.to("#ringC",{{scale:.4,duration:{tout - tin:.3f},ease:"sine.inOut"}},{tin:.3f});')


@scene
def s12():
    """CHEAT CODE 1 — slow breathing. The siren slows; Neutro breathes extremely seriously; Mito yawns."""
    t0 = BEATS["to_cheats"][0] + .4; t1 = BEATS["breathe"][1]
    S = Scene("s12", t0, t1, music="game", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    S.tr_in("whip", .3)
    l = {n: S.l(n) for n in range(51, 53)}
    b0, b1 = S.b("breathe")
    tin = S.w(52, "in", after=S.w(52, "So", after=S.w(52, "did") - .2)); tout = l[52][1]
    # alarm: pulsing, then slower and dimmer with each breath
    S.j(f'tl.set("#hqred",{{opacity:.8}},0);tl.fromTo("#hqred",{{opacity:.85}},{{opacity:.3,duration:.35,yoyo:true,repeat:{int((tin - .2) / .35)},immediateRender:false}},0);'
        f'tl.fromTo("#hqred",{{opacity:.6}},{{opacity:.2,duration:1.0,yoyo:true,repeat:{int((S.T - tin) / 1.0)},immediateRender:false}},{tin:.3f});'
        f'tl.to("#hqred",{{opacity:.12,duration:.6}},{b0 + .4:.3f});')
    S.cyto(430, 650, .58, expr=[(l[51][0], .9, "squint"), (S.w(52, "Plot") - .05, 1.1, "shock")],
           x_expr=[(S.w(51, "I'm"), 1.6, "determined"), (S.w(52, "slow", after=S.w(52, "part") - .5), 1.0, "smug")],
           points=[(S.w(51, "Cheat"), .8), (S.w(52, "slow") - .1, .7)], shrugs=[(S.w(52, "didn't"), .8)], blinks=[])
    S.j(f'tl.to("#cyto",{{scale:1.12,duration:{tout - tin - 1.2:.3f},ease:"sine.inOut"}},{tin:.3f});tl.to("#cyto",{{scale:1,duration:1.3,ease:"sine.inOut"}},{tout - 1.2:.3f});'
        f'tl.to(["#lidL","#lidR"],{{y:40,duration:.2}},{tin + .1:.3f});tl.to(["#lidL","#lidR"],{{y:-14,duration:.2}},{b1 - .4:.3f});')
    S.char("mito", "mt", 860, 330, .56, pose="slump", gassed=True, who="MITO", z=19, expr=[(0, S.T, "exhausted")], shut_at=[(b0 + .2, 1.4)])
    S.j(f'tl.set(["#mtm_rest","#mtm_frown","#mtm_smirk","#mtm_grin","#mtm_flat","#mtm_small","#mtm_a","#mtm_e","#mtm_mbp"],{{opacity:0}},{b0 + .2:.3f});tl.set("#mtm_o",{{opacity:1}},{b0 + .2:.3f});'
        f'gsap.set("#mtm_o",{{transformOrigin:"50% 50%"}});tl.fromTo("#mtm_o",{{scale:1}},{{scale:1.8,duration:.5,yoyo:true,repeat:1}},{b0 + .2:.3f});tl.set("#mtm_o",{{opacity:0}},{b1 - .1:.3f});tl.set("#mtm_frown",{{opacity:1}},{b1 - .1:.3f});')
    S.sfx(b0 + .3, "yawn", -8)
    S.char("neutro", "nt", 1330, 300, .72, pose="cross", who="NEUTRO", z=20, expr=[(tin, b1 - tin, "determined")], shut_at=[(tin + .2, b1 - tin - .3)])
    S.j(f'tl.to("#ntBody",{{scale:1.09,duration:{tout - tin - .3:.3f},ease:"sine.inOut"}},{tin:.3f});tl.to("#ntBody",{{scale:1,duration:1.2,ease:"sine.inOut"}},{tout - .4:.3f});'
        f'tl.to("#ntBody",{{scale:1.1,duration:.8,ease:"sine.inOut",yoyo:true,repeat:1}},{b0 + .1:.3f});')
    S.popup("cc0", S.w(51, "Cheat") - .1, l[52][0] - .1, "PRESS START", "CHEAT CODES", "#FFD166", 1040, 120, 700)
    S.popup("cc1", S.w(52, "Cheat") - .1, S.w(52, "A") - .1, "CHEAT CODE 1 UNLOCKED", "SLOW YOUR BREATHING", "#8ce2d6", 1040, 120, 900)
    S.popup("cc1b", S.w(52, "A"), S.w(52, "Plot") - .15, "12-WEEK TRIAL", "SLOW BREATHING → ANXIETY ↓", "#8ce2d6", 1040, 120, 900)
    S.popup("cc1c", S.w(52, "Plot") - .05, S.w(52, "So", after=S.w(52, "did") - .2) - .1, "PLOT TWIST", "LONGER EXHALE? NOPE. SLOW = THE KEY", "#FFD166", 1040, 120, 980)
    src_chip(S, "src4", S.w(52, "A"), S.w(52, "So", after=S.w(52, "did") - .2), "BIRDEE ET AL. 2023", 600, 560)
    breath_ring(S, tin - .1, S.w(52, "and", after=tin) - .1, tout + .2)
    S.j(f'tl.set("#ringT",{{innerHTML:"OUT..."}},{S.w(52, "and", after=tin) - .1:.3f});')
    S.sfx(S.w(51, "Cheat") - .1, "coin", -6); S.sfx(S.w(52, "Cheat") - .1, "levelup", -6); S.sfx(tin, "inhale", -10)
    S.tr_out("whip", .3)
    S.captions({"cheat": "#FFD166", "codes": "#FFD166", "slow": "#8ce2d6"})
    return S


SNEAKER = '<path d="M10 70 L20 30 Q50 40 70 20 L100 50 L150 60 Q160 80 150 90 L10 90Z" fill="#fbfbf6" stroke="#0c1622" stroke-width="6"/><rect x="10" y="84" width="145" height="12" fill="#e63946" stroke="#0c1622" stroke-width="4"/>'
MEDIT = '<circle cx="80" cy="30" r="22" fill="#ff9f5a" stroke="#0c1622" stroke-width="5"/><path d="M30 95 Q80 40 130 95Z" fill="#7a5cc7" stroke="#0c1622" stroke-width="5"/><path d="M40 70 L10 60 M120 70 L150 60" stroke="#0c1622" stroke-width="6" stroke-linecap="round"/>'
WIND = '<path d="M10 40 H110 Q140 40 140 20 Q140 0 120 0 M10 65 H130 Q160 65 160 85 Q160 105 140 105 M10 90 H80" fill="none" stroke="#3fc1b0" stroke-width="10" stroke-linecap="round"/>'


@scene
def s13():
    """CHEAT CODE 2 — pick your side quest (trial card), Mito wants hoops, 'Bet.'"""
    t0 = BEATS["breathe"][1]; t1 = LINES[55]["t1"] + .3
    S = Scene("s13", t0, t1, music="game", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    snowfall(S, "hqsnow", S.T)
    S.add('<div class="fill" style="z-index:30;background:rgba(255,40,40,.1)"></div>')
    S.tr_in("whip", .3)
    l = {n: S.l(n) for n in range(53, 56)}
    S.cyto(430, 650, .58, x_expr=[(S.w(53, "All"), 1.6, "smug"), (l[55][0] - .1, 1.0, "hype")], expr=[(l[54][0] + .3, .7, "skeptic")],
           points=[(S.w(53, "Cheat"), .8), (S.w(53, "pick", after=S.w(53, "So", after=S.w(53, "same")) - .1) - .1, .8)], looks=[(S.w(53, "Another"), 14, -10), (l[54][0], 14, 0)])
    S.char("mito", "mt", 860, 300, .58, pose="slump", who="MITO", z=19, poses=[(l[54][0] - .2, "ball"), (l[55][0] + .1, "hype")],
           expr=[(0, l[54][0] - .3, "exhausted"), (l[54][0] - .2, 1.3, "hype"), (l[55][0], S.T - l[55][0], "hype")], pops=[(l[54][0] - .1, 1), (l[55][0] + .15, 1.3)])
    S.char("neutro", "nt", 1330, 300, .72, pose="cross", who="NEUTRO", z=20, expr=[(0, S.T, "deadpan")], nods=[S.w(53, "same")])
    S.popup("cc2", S.w(53, "Cheat") - .1, S.w(53, "Another") - .1, "CHEAT CODE 2 UNLOCKED", "PICK YOUR SIDE QUEST", "#FFD166", 1040, 120, 900)
    tc0 = S.w(53, "Another") - .05; tc1 = min(tc0 + 3.9, S.w(53, "So", after=S.w(53, "same")) + .2)
    S.over(f'<div id="tri" class="pop clip" data-start="{tc0:.3f}" data-duration="{tc1 - tc0:.3f}" style="left:620px;top:110px;width:1000px;height:330px;z-index:55;border-radius:26px;background:#FAF4E8;border:7px solid #0c1622;box-shadow:0 14px 0 rgba(0,0,0,.35)">'
           f'<div style="position:absolute;left:0;right:0;top:16px;text-align:center;font:36px InterBlack;color:#0c1622">5-WEEK TRIAL: ALL 3 LOWERED STRESS</div>'
           f'<svg style="position:absolute;left:40px;top:80px" width="920" height="240"><g transform="translate(20 20)">{SNEAKER}</g><text x="240" y="90" font-family="InterBlack" font-size="80" fill="#e63946">=</text>'
           f'<g transform="translate(340 10)">{MEDIT}</g><text x="560" y="90" font-family="InterBlack" font-size="80" fill="#e63946">=</text><g transform="translate(660 20)">{WIND}</g>'
           f'<text x="90" y="200" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">EXERCISE</text><text x="420" y="200" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">MEDITATION</text><text x="740" y="200" text-anchor="middle" font-family="InterBlack" font-size="30" fill="#0c1622">SLOW BREATHING</text></svg></div>')
    S.j(f'tl.fromTo("#tri",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(1.4)"}},{tc0:.3f});tl.to(".settxt",{{opacity:0,duration:.1}},{tc0:.3f});tl.to(".settxt",{{opacity:1,duration:.1}},{tc1:.3f});')
    src_chip(S, "src5", tc0 + .3, tc1, "VAN DER ZWAN ET AL. 2015", 1140, 470)
    S.popup("pk", tc1 + .05, l[53][1] + .3, "", "PICK WHAT YOU'LL ACTUALLY DO", "#8ce2d6", 1100, 120, 760)
    S.sfx(S.w(53, "Cheat") - .1, "levelup", -6); S.sfx(l[55][0], "coin", -6)
    S.punch(l[55][0], 1.1, .4, 430, 600)
    S.tr_out("zoom", .3)
    S.captions({"side": "#FFD166", "quest": "#FFD166", "same": "#8ce2d6"})
    return S


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


@scene
def s14():
    """SIDE-QUEST MONTAGE — brick outside, skate at Nathan Phillips Square, Distillery lights, walk the block. SIDE QUEST COMPLETE."""
    t0 = LINES[55]["t1"] + .3; t1 = BEATS["sidequest"][1]
    S = Scene("s14", t0, t1, music="game", bg="#16224a")
    S.tr_in("zoom", .3)
    tA = S.w(56, "Skate") - .15; tB = S.w(56, "walk") - .1; tC = S.w(56, "or") - .1; sq0, sq1 = S.b("sidequest")
    segs = [("bk", 0, tA, block("bk")), ("np", tA, tB, nps("np")), ("ds", tB, tC, distillery("ds")), ("bk2", tC, S.T, block("bk2"))]
    for i, (p, a, b, layers) in enumerate(segs):
        S.add(f'<div id="seg{i}" class="clip" data-start="{a:.3f}" data-duration="{b - a:.3f}" style="position:absolute;inset:0">' + "".join(layers) + '</div>')
        S.parallax([(f"{p}0", .3), (f"{p}1", .7)] + ([(f"{p}2", 1.0)] if p == "np" else []), a, b, dx=-120)
        if i: S.j(f'tl.fromTo("#seg{i}",{{x:1920}},{{x:0,duration:.25,ease:"power3.out"}},{a:.3f});'); S.sfx(a, "whoosh", -10)
    S.j('tl.fromTo("#bksn",{y:-200},{y:0,duration:3,ease:"none"},0);')
    S.cyto(760, 700, .6, z=20, x_expr=[(0, tA, "worried"), (tA, tB - tA, "hype"), (tB, tC - tB, "smug"), (tC, S.T - tC, "smug")],
           waves=[tA + .4], blinks=None, toque_extra="")
    S.j(f'tl.to("#cyto",{{x:6,duration:.05,yoyo:true,repeat:{int(tA / .05) - 2}}},0);')                       # shivering
    S.j(f'tl.fromTo("#cytoPos",{{x:"-=500"}},{{x:"+=900",duration:{tB - tA:.3f},ease:"sine.inOut",immediateRender:false}},{tA:.3f});tl.to("#cyto",{{rotation:-8,duration:.4,yoyo:true,repeat:3}},{tA:.3f});'
        f'tl.to("#cytoPos",{{x:"-=400",duration:.01}},{tB:.3f});')
    S.over(f'<div id="hp" class="clip" data-start="{tC:.3f}" data-duration="{S.T - tC:.3f}" style="position:absolute;left:0;top:0;z-index:21"><svg width="1920" height="1080">'
           f'<g transform="translate({760 - 300 * .6 - 40:.0f} {700 - 220:.0f})"><path d="M40 120 Q180 -40 400 120" fill="none" stroke="#222" stroke-width="20"/><rect x="10" y="100" width="56" height="90" rx="20" fill="#e63946" stroke="#0c1622" stroke-width="6"/><rect x="376" y="100" width="56" height="90" rx="20" fill="#e63946" stroke="#0c1622" stroke-width="6"/></g></svg></div>')
    S.popup("q0", .1, tA - .1, "SIDE QUEST", "IT'S BRICK OUTSIDE: BUNDLE UP", "#8ce2d6", 960, 70, 900)
    S.popup("q1", tA + .1, tB - .1, "SIDE QUEST", "SKATE AT NATHAN PHILLIPS SQUARE", "#8ce2d6", 960, 70, 980)
    S.popup("q2", tB + .1, tC - .1, "SIDE QUEST", "DISTILLERY WINTER VILLAGE: FREE BEFORE 4 PM", "#8ce2d6", 960, 70, 1100)
    S.popup("q3", tC + .1, sq0, "SIDE QUEST", "WALK THE BLOCK, HEADPHONES IN", "#8ce2d6", 960, 70, 980)
    S.popup("sqc", sq0, S.T, "★ ★ ★", "SIDE QUEST COMPLETE", "#FFD166", 960, 380, 900)
    S.sfx(sq0, "levelup", -4); S.sfx(tA + .2, "skate", -8)
    S.tr_out("whip", .3)
    S.captions({"brick": "#8ce2d6", "nathan": "#FFD166", "phillips": "#FFD166", "distillery": "#FFD166"})
    return S


@scene
def s15():
    """CHEAT CODE 3 — mute the group chat. The lever finally stays up. The alarm goes quiet."""
    t0 = BEATS["sidequest"][1]; t1 = BEATS["mute"][1]
    S = Scene("s15", t0, t1, music="game", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    S.j('tl.set("#hqred",{opacity:.25},0);')
    S.tr_in("whip", .3)
    l57 = S.l(57); m0, m1 = S.b("mute")
    S.cyto(430, 650, .58, phone=True, x_expr=[(S.w(57, "Say"), 1.2, "determined"), (m0, S.T - m0, "smug")], points=[(S.w(57, "Protect") - .1, .8)], sips=[(m0 + .1, 1.1)])
    S.char("mito", "mt", 860, 330, .56, pose="idle", who="MITO", z=19, expr=[(m0, S.T - m0, "hype")])
    S.char("neutro", "nt", 1330, 300, .72, pose="cross", who="NEUTRO", z=20, expr=[(0, m0, "deadpan"), (m0, S.T - m0, "smug")], nods=[m0 + .3])
    S.popup("cc3", S.w(57, "Cheat") - .1, S.w(57, "Say") - .1, "CHEAT CODE 3 UNLOCKED", "MUTE THE GROUP CHAT", "#ff8a8a", 1040, 120, 900)
    S.popup("cc3b", S.w(57, "Say"), S.w(57, "Protect") - .1, "BONUS", "SAY NO TO ONE THING", "#8ce2d6", 1040, 120, 760)
    S.popup("cc3c", S.w(57, "Protect"), m1, "BONUS", "PROTECT YOUR SLEEP", "#c4b0ff", 1040, 120, 760)
    S.j(f'tl.set("#cyNotif",{{opacity:0}},{S.w(57, "mute"):.3f});')
    S.over(f'<div id="mute" class="pop clip" data-start="{S.w(57, "mute"):.3f}" data-duration="{S.T - S.w(57, "mute"):.3f}" style="left:700px;top:560px;z-index:60"><svg width="120" height="120"><circle cx="60" cy="60" r="54" fill="#e63946" stroke="#0c1622" stroke-width="6"/>'
           '<path d="M34 48 H50 L70 30 V90 L50 72 H34Z" fill="#fff"/><path d="M80 44 L100 76 M100 44 L80 76" stroke="#fff" stroke-width="8" stroke-linecap="round"/></svg></div>')
    S.j(f'tl.fromTo("#mute",{{scale:0}},{{scale:1,duration:.3,ease:"back.out(3)"}},{S.w(57, "mute"):.3f});')
    S.j(f'tl.to("#hqred",{{opacity:0,duration:.6}},{m0:.3f});tl.to("#hqalarmGlass",{{opacity:0,duration:.3}},{m0:.3f});')
    S.popup("alq", m0 + .1, S.T, "", "ALARM: QUIET", "#8ce2d6", 1255, 300, 520)
    S.sfx(S.w(57, "mute"), "click", -6); S.sfx(m0, "powerdown", -6)
    S.tr_out("flash", .25)
    S.captions({"mute": "#ff8a8a", "sleep": "#c4b0ff"})
    return S



BIRD = ('<g id="bird"><ellipse cx="40" cy="40" rx="34" ry="26" fill="#4f86ff" stroke="#0c1622" stroke-width="5"/><circle cx="62" cy="24" r="18" fill="#4f86ff" stroke="#0c1622" stroke-width="5"/>'
        '<circle cx="68" cy="20" r="4" fill="#0c1622"/><path d="M78 24 L94 28 L78 32Z" fill="#ffb02e" stroke="#0c1622" stroke-width="3"/><path d="M10 40 L-8 30 L0 50Z" fill="#3a6ad6" stroke="#0c1622" stroke-width="4"/></g>')


@scene
def s16():
    """CLIMAX — silence, a bird chirps. 'Exactly.' Neutro spots Rhino frozen mid-sneak, tickets him; ACHOO out the front door."""
    t0 = BEATS["mute"][1]; t1 = BEATS["breakstarts"][0]
    S = Scene("s16", t0, t1, music="quiet", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    snowfall(S, "hqsnow", S.T)
    S.tr_in("flash", .25)
    ch0, ch1 = S.b("chirp"); sp0, sp1 = S.b("spot"); ac0, ac1 = S.b("achoo")
    l = {n: S.l(n) for n in range(58, 64)}
    S.add(f'<div style="position:absolute;left:600px;top:572px;z-index:3"><svg width="120" height="90" style="overflow:visible">{BIRD}</svg></div>')
    S.j(f'gsap.set("#bird",{{transformOrigin:"50% 100%"}});tl.to("#bird",{{rotation:-12,y:-6,duration:.12,yoyo:true,repeat:5}},{ch0 + .4:.3f});')
    for i, t in enumerate((ch0 + .4, ch0 + 1.0)):
        S.over(f'<div id="nt{i}x" class="pop clip" data-start="{t:.3f}" data-duration=".9" style="left:{700 + i * 40}px;top:{500 - i * 30}px;font:60px InterBlack;color:#FFD166;-webkit-text-stroke:2px #0c1622">♪</div>')
        S.j(f'tl.fromTo("#nt{i}x",{{y:0,opacity:1}},{{y:-60,opacity:0,duration:.9}},{t:.3f});')
        S.sfx(t, "chirp", -4)
    S.cyto(430, 650, .58, expr=[(ac0 - .2, .9, "shock")], x_expr=[(l[58][0] - .3, 1.6, "sideeye"), (l[60][0], 1.6, "smug"), (l[63][0], 1.4, "smug")],
           looks=[(ch0 + .4, 10, -8), (l[59][0] + .1, 14, 0)], sips=[(l[60][1] + .1, 1.0)])
    S.char("mito", "mt", 860, 330, .56, pose="idle", who="MITO", z=19, poses=[(l[62][0] - .1, "hype")],
           expr=[(0, ch1, "deadpan"), (sp0, 1.3, "shocked"), (l[62][0] - .1, S.T - l[62][0] + .1, "hype")], pops=[(l[62][0], 1.3)])
    # Rhino frozen mid-sneak behind the plant (mannequin-challenge freeze)
    S.char("rhino", "rh", 1290, 520, .62, pose="sneak", z=18, expr=[(sp0, S.T - sp0, "shocked")], blinks=[], bob=False)
    S.j(f'tl.fromTo("#rhW",{{x:-260}},{{x:0,duration:{sp0:.3f},ease:"none",immediateRender:false}},0);tl.to("#rh",{{y:-12,duration:.3,yoyo:true,repeat:{int(sp0 / .3) - 1},ease:"sine.inOut"}},0);')
    S.char("neutro", "nt", 1500, 300, .72, pose="cross", who="NEUTRO", z=20,
           poses=[(sp0 + .3, "point"), (l[61][0], "notepad"), (l[61][1] - .1, "ticket")],
           expr=[(0, sp0, "deadpan"), (sp0, .9, "shocked"), (l[61][0], S.T - l[61][0], "smug")], looks=[(sp0 + .1, -.3, .1)], nods=[l[59][0] + .1])
    S.j(f'tl.to("#nt",{{scaleX:-1,duration:.1,svgOrigin:"300 650"}},{sp0:.3f});tl.to("#nt",{{scaleX:1,duration:.1,svgOrigin:"300 650"}},{sp0 + .25:.3f});')
    S.snapzoom(sp0 + .3, 1.35, sp1 - sp0, 1420, 640, .3)
    S.sfx(sp0 + .3, "sting", -6); S.sfx(l[61][1] - .1, "rip", -4); S.sfx(l[61][1] + .15, "slap", -2)
    S.over(f'<div id="tkt" class="pop clip" data-start="{l[61][1] + .1:.3f}" data-duration="{ac0 - l[61][1]:.3f}" style="left:1360px;top:560px;z-index:60;transform:rotate(-12deg)"><svg width="120" height="140"><rect x="6" y="6" width="108" height="128" rx="8" fill="#fff6c8" stroke="#0c1622" stroke-width="6"/><path d="M22 34 H96 M22 60 H96 M22 86 H70" stroke="#c0392b" stroke-width="7"/></svg></div>')
    S.j(f'tl.fromTo("#tkt",{{scale:2.5,opacity:0}},{{scale:1,opacity:1,duration:.15,ease:"power4.in"}},{l[61][1] + .1:.3f});')
    # ACHOO: cut to the nose front door, Rhino launched out
    nd = "".join(X.nose_door("nd"))
    S.over(f'<div id="ach" class="clip" data-start="{ac0:.3f}" data-duration="{S.T - ac0:.3f}" style="position:absolute;inset:0;z-index:70;overflow:hidden">{nd}'
           f'<div style="position:absolute;inset:0;z-index:5">{K.wrap(K.rhino_html("rz", "spread"), "rzW", 760, 520, .7)}</div>'
           f'<div id="achT" style="position:absolute;left:0;right:0;top:300px;text-align:center;z-index:6;font:230px InterBlack;color:#FFD166;-webkit-text-stroke:9px #0c1622;paint-order:stroke fill">ACHOO!</div>'
           f'<div style="position:absolute;inset:0;z-index:7">{K.wrap(K.mito_html("mz", "hype"), "mzW", 1420, 330, .62)}</div></div>')
    S.j(f'tl.fromTo("#rzW",{{x:0,y:0,scale:1,rotation:0}},{{x:-260,y:-900,scale:.15,rotation:720,duration:1.1,ease:"power2.in"}},{ac0 + .25:.3f});'
        f'tl.fromTo("#achT",{{scale:.2,opacity:0}},{{scale:1,opacity:1,duration:.18,ease:"back.out(3)"}},{ac0 + .2:.3f});tl.to("#achT",{{scale:1.15,opacity:0,duration:.3}},{ac1 - .3:.3f});'
        f'tl.set("#mzW",{{y:900}},0);tl.fromTo("#mzW",{{y:900}},{{y:0,duration:.35,ease:"back.out(1.6)"}},{l[62][0] - .3:.3f});')
    S.j(K.act_js("mz", 38, 32, mouths=K.mouth_track(DIALOGUE, S.words_of("MITO"), [(0, S.T, "hype")], S.t0, S.t1), expr=[(ac0, S.T - ac0, "hype")], T=S.T, blinks=[]))
    S.j(K.act_js("rz", 28, 26, expr=[(ac0, S.T - ac0, "shocked")], T=S.T, blinks=[], bob=False))
    S.shake(ac0 + .2, .7, 26)
    S.j(f'tl.to(".settxt",{{opacity:0,duration:.05}},{ac0 - .05:.3f});')
    S.sfx(ac0 + .15, "achoo", 0); S.sfx(ac0 + .5, "whoosh", -6); S.sfx(l[62][0], "crowd", -10)
    S.tr_out("whip", .3)
    S.captions({"exactly": "#FFD166", "booked": "#FFD166", "nasal": "#ff8a8a"})
    return S


SOURCES = [("Fight-or-flight: standard physiology (textbook)", "Cohen et al., PNAS 2012"),
           ("Cohen, Tyrrell & Smith, NEJM 1991", "Kloner, Prog Cardiovasc Dis 2006"),
           ("Milne, Eur J Epidemiol 2005", "Weerasinghe, Heart 2002"),
           ("Birdee et al., Complement Ther Med 2023", "van der Zwan et al., Appl Psychophysiol Biofeedback 2015"),
           ("Distillery Winter Village (free before 4 pm)", "Nathan Phillips Square skating: City of Toronto")]


@scene
def s17():
    """OUTRO — BREAK STARTS, Mito smells holiday food, sources, CTA. Phone buzzes once, the alarm flickers... hard cut = loop."""
    t0 = BEATS["breakstarts"][0]; t1 = BEATS["end"][1]
    S = Scene("s17", t0, t1, music="outro", bg="#47306b")
    for l in X.hq("hq"): S.add(l)
    S.add(X.alarm_fx("hq")); snowfall(S, "hqsnow", S.T)
    S.tr_in("whip", .3)
    l = {n: S.l(n) for n in range(64, 67)}
    e0, e1 = S.b("end")
    flipsign(S, "cd", .3, "1 DAY TILL BREAK", "BREAK STARTS", 1240, 120, 560)
    S.sfx(.4, "cheer", -10)
    S.cyto(540, 640, .6, phone=True, expr=[(l[65][0], .8, "skeptic"), (e0 + .45, 1.2, "shock")],
           x_expr=[(S.w(66, "Comment"), 2.0, "hype"), (S.w(66, "Not"), 1.4, "deadpan"), (S.w(66, "breathe") - .2, 1.2, "smug")],
           waves=[S.w(66, "Like")], points=[(S.w(66, "sources") - .1, .8)], sips=[(S.w(66, "December's") - .3, 1.0)],
           looks=[(l[64][0] + .3, 14, -4), (e0 + .5, 0, 0)])
    S.char("mito", "mt", 730, 330, .56, pose="idle", who="MITO", z=19, poses=[(l[64][0], "hype"), (l[65][0] + .5, "slump")],
           expr=[(.3, 1, "hype"), (l[64][0], l[64][1] - l[64][0], "hype"), (l[65][0] + .3, 2, "exhausted")], shut_at=[(S.w(64, "mans"), 1.4)])
    S.j(f'tl.to("#mtBody",{{y:-14,duration:.3,yoyo:true,repeat:5,ease:"sine.inOut"}},{l[64][0] + .2:.3f});')
    S.over(f'<div id="smell" class="clip" data-start="{l[64][0]:.3f}" data-duration="{l[64][1] - l[64][0] + .5:.3f}" style="position:absolute;left:950px;top:300px;z-index:30"><svg width="260" height="200">'
           + "".join(f'<path d="M{20 + i * 70} 190 q30 -40 0 -80 t0 -80" fill="none" stroke="#FAF4E8" stroke-width="10" stroke-linecap="round" opacity=".8"/>' for i in range(3)) + '</svg></div>')
    S.j(f'tl.fromTo("#smell",{{y:30,opacity:0}},{{y:-20,opacity:1,duration:1.2,repeat:2}},{l[64][0]:.3f});')
    S.sfx(S.w(64, "Is"), "sniff", -6)
    S.char("neutro", "nt", 1500, 300, .7, pose="cross", who="NEUTRO", z=20, expr=[(0, S.T, "deadpan")], nods=[.6])
    S.j(f'tl.to("#ntW",{{x:700,duration:.5,ease:"power2.in"}},{l[64][0] - .6:.3f});')
    # sources (2 per screen, >=34px), CTA, not medical advice
    s0 = l[64][0]; per = (e0 - s0) / len(SOURCES)
    S.j(f'tl.to(".settxt",{{opacity:0,duration:.1}},{s0 - .1:.3f});')
    for i, (a, b) in enumerate(SOURCES):
        ta = s0 + i * per
        S.over(f'<div id="src{i}" class="pop clip" data-start="{ta:.3f}" data-duration="{per:.3f}" style="left:1060px;top:300px;width:820px;z-index:62;padding:26px 30px;border-radius:24px;background:#0c1622;border:6px solid #FAF4E8">'
               f'<div style="font:28px InterBlack;color:#FFD166;letter-spacing:.08em">SOURCES {i + 1}/{len(SOURCES)}</div>'
               f'<div style="font:36px/1.2 InterBlack;color:#FAF4E8;margin-top:14px">{a}</div><div style="font:36px/1.2 InterBlack;color:#FAF4E8;margin-top:16px">{b}</div></div>')
        S.j(f'tl.fromTo("#src{i}",{{x:60,opacity:0}},{{x:0,opacity:1,duration:.25}},{ta:.3f});')
    S.over(f'<div id="nma2" class="clip" data-start="{s0:.3f}" data-duration="{e0 - s0:.3f}" style="position:absolute;left:1060px;top:700px;width:820px;z-index:62;text-align:center;font:40px InterBlack;color:#ff8a8a;-webkit-text-stroke:2px #0c1622">NOT MEDICAL ADVICE</div>')
    S.popup("cta", S.w(66, "Comment") - .1, S.w(66, "Like") - .1, "COMMENT", "WHAT'S STRESSING YOU OUT?", "#FFD166", 540, 120, 900)
    S.popup("cta2", S.w(66, "Like") - .05, S.w(66, "sources") - .1, "", "LIKE + SUBSCRIBE", "#ff8a8a", 540, 120, 700)
    S.j(f'tl.set(".settxt",{{opacity:0}},{S.w(66, "Like") - .04:.3f});tl.set(".settxt",{{opacity:0}},{S.w(66, "sources"):.3f});tl.set(".settxt",{{opacity:0}},{S.w(66, "Comment") - .09:.3f});')
    # the loop: phone buzzes once, the alarm light flickers, Cyto looks at camera -> hard cut to the cold open
    buzz(S, e0 + .15, .4)
    S.j(f'tl.set("#hqred",{{opacity:0}},0);tl.to("#hqred",{{opacity:.7,duration:.05}},{e0 + .55:.3f});tl.to("#hqred",{{opacity:0,duration:.05}},{e0 + .7:.3f});tl.to("#hqred",{{opacity:.6,duration:.05}},{e0 + .9:.3f});tl.to("#hqred",{{opacity:0,duration:.08}},{e0 + 1.05:.3f});'
        f'tl.to("#hqalarmGlass",{{opacity:1,duration:.05}},{e0 + .55:.3f});tl.to("#hqalarmGlass",{{opacity:.35,duration:.05}},{e0 + 1.1:.3f});')
    S.snapzoom(e0 + .5, 1.2, e1 - e0, 540, 600, .01)
    S.sfx(e0 + .55, "blip", -6)
    S.captions({"comment": "#FFD166", "breathe": "#8ce2d6", "christmas": "#ff8a8a", "marved": "#FFD166"})
    return S


if __name__ == "__main__":
    names = sys.argv[1:] or list(SC)
    for n in names:
        s = SC[n](); d = s.build() if not os.environ.get("NOBUILD") else None; print("built", n, f"{s.t0:.2f}-{s.t1:.2f} ({s.T:.2f}s)")
    ev_f = "/home/claude/lf02/events.json"
    ev = json.load(open(ev_f)) if os.path.exists(ev_f) else {}
    for n in names:
        s0, s1 = json.load(open(f"{P}/{n}/meta.json"))["t0"], json.load(open(f"{P}/{n}/meta.json"))["t1"]
        ev[n] = {"sfx": [x for x in SFX if s0 - .01 <= x[0] < s1 + .01], "music": [m for m in MUSIC if s0 - .01 <= m[0] < s1 + .01]}
    json.dump(ev, open(ev_f, "w"), indent=0)
