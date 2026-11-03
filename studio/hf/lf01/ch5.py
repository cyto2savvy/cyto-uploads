"""LF01 ch5: Months to years. Scarborough Bluffs bg. Heart-risk timeline (1 yr half, 15 yr = never smoked); airway lining (Lapperre 2007);
the number (Jha 2013, Toronto CGHR): years-gained bar chart 25-34 ~10 / 35-44 ~9 / 45-54 ~6; quit before 40 = ~90% ring."""
from lf import *
import lfart as L

c = Ch(5); wt = c.wt; T = c.T
tBy, tYear, tHeart, tRisk, tHalf, tBy2, tFif, tMatch, tNever, tSmoked = (wt("By"), wt("year,"), wt("heart"), wt("risk"), wt("half."), wt("By", 4), wt("fifteen"),
    wt("matches"), wt("never"), wt("smoked."))
tAir, tHeal, tCOPD, tLining, tBetter, tMostly, tThree, tQuitting, tReal, tOver = (wt("Airways"), wt("healing"), wt("COPD"), wt("lining"), wt("better"), wt("mostly"),
    wt("three"), wt("quitting."), wt("Real"), wt("overnight."))
tNow, tNum, tProm, tToronto, tCentre, tNEJM, tLose, tDecade = wt("Now"), wt("number"), wt("promised."), wt("Toronto's"), wt("Centre"), wt("New"), wt("lose"), wt("decade")
tQ1, tTen, tQ2, tNine, tQ3, tSix = wt("Quit"), wt("ten"), wt("Thirty-five"), wt("nine."), wt("Forty-five"), wt("six.")
tQ4, tForty, tCut, tNinety, tNeverTL, tSooner = wt("Quit", 38), wt("forty,"), wt("cut"), wt("ninety"), wt("Never", 42), wt("sooner")
SA, SB, SC, SD = 0, tAir - 0.15, tNow - 0.15, tQ1 - 0.15

c.bg("bgL", 0, T, L.bg_bluffs("bl"), kb=(1.0, 1.08))
c.j(f'tl.fromTo("#blCloud",{{x:0}},{{x:260,duration:{T:.2f},ease:"none",immediateRender:false}},0);tl.fromTo("#blWaves",{{x:0}},{{x:-60,duration:1.5,yoyo:true,repeat:{int(T / 1.5)},ease:"sine.inOut",immediateRender:false}},0);')

# ---- A: heart-risk line
sA = (svg(L.heart(120, 150, .6, "h5")
          + f'<path d="M110 620 H1140" stroke="#5d6f84" stroke-width="6"/>'
          f'<path d="M110 600 H1140" stroke="{GREEN}" stroke-width="6" stroke-dasharray="18 14"/>'
          f'<path id="rl" d="M110 220 C300 240 380 400 470 410 C700 440 900 580 1060 600" fill="none" stroke="{CORAL}" stroke-width="14" stroke-linecap="round" {DRAW}/>'
          f'<g id="d1"><circle cx="470" cy="410" r="22" fill="{GOLD}" stroke="{INK}" stroke-width="6"/></g>'
          f'<g id="d2"><circle cx="1060" cy="600" r="22" fill="{GREEN}" stroke="{INK}" stroke-width="6"/></g>')
      + f'<div id="exr" class="lbl" style="left:200px;top:110px;font-size:46px;color:{CORAL}">EXTRA HEART DISEASE RISK</div>'
      + f'<div id="l1" class="chip" style="left:330px;top:300px;background:{GOLD};font-size:42px">1 YR: ABOUT HALF</div>'
      + f'<div id="l2" class="chip" style="left:560px;top:470px;background:{GREEN};font-size:42px">15 YRS: = NEVER SMOKED</div>'
      + src_card("cWh", "WHO · CDC", None, CORAL, left=110, top=650, width=330))
c.slide("sA", SA, SB, sA)
c.pop("#h5", tHeart - 0.1, None); c.rise("#exr", tHeart - 0.05)
c.beat(tYear); c.j(f'tl.set("#rl",{{strokeDashoffset:100}},0);tl.to("#rl",{{keyframes:[{{strokeDashoffset:62,duration:0.8}},{{strokeDashoffset:62,duration:{tSmoked - 1.6 - tYear - 0.6:.2f}}},{{strokeDashoffset:0,duration:2.0}}],ease:"none"}},{tYear - 0.2:.3f});')
c.pop("#d1", tHalf - 0.15, None); c.pop("#l1", tHalf - 0.1); c.slide_in("#cWh", tBy + 0.5)
c.pop("#d2", tNever - 0.1, None); c.pop("#l2", tMatch - 0.05, "chime")

# ---- B: airway lining heals (Lapperre 2007)
import math
def ring(r_out, r_in, bump, n=26):
    pts = []
    for k in range(n * 2 + 1):
        a = math.pi * 2 * k / (n * 2); r = r_in + (bump if k % 2 else 0)
        pts.append(f"{300 + r * math.cos(a):.0f} {360 + r * math.sin(a):.0f}")
    return "M" + " L".join(pts) + "Z"
sB = (svg(f'<circle cx="300" cy="360" r="250" fill="#f29aa8" stroke="{INK}" stroke-width="9"/>'
          f'<path id="rough" d="{ring(250, 120, 34)}" fill="#c43a52" stroke="{INK}" stroke-width="6"/>'
          f'<circle id="smooth" cx="300" cy="360" r="170" fill="#f7c4cc" stroke="{INK}" stroke-width="6"/>'
          f'<circle cx="300" cy="360" r="{110}" fill="#0f2236" stroke="{INK}" stroke-width="6" id="lumen"/>')
      + f'<div id="al" class="lbl" style="left:620px;top:80px;font-size:48px;color:{CREAM}">AIRWAY LINING</div>'
      + f'<div id="cp" class="chip" style="left:620px;top:170px;background:{SKY};font-size:42px">IN EX-SMOKERS (COPD)</div>'
      + f'<div id="tp" class="stamp" style="left:620px;top:290px;font-size:72px;color:{GREEN};border-color:{GREEN}">3½+ YEARS</div>'
      + f'<div id="no" class="lbl" style="left:620px;top:440px;font-size:46px;color:{GOLD}">REAL HEALING,<br>NOT OVERNIGHT</div>'
      + src_card("cLa", "LAPPERRE 2007", "Respiratory Research", SKY, left=620, top=620, width=520))
c.slide("sB", SB, SC, sB)
c.j('tl.set("#smooth",{opacity:0},0);'); c.rise("#al", tAir); c.pop("#cp", tCOPD - 0.1); c.slide_in("#cLa", tCOPD + 0.4)
c.j(f'tl.to("#rough",{{opacity:0,duration:1.2,ease:"power1.inOut"}},{tBetter - 0.2:.3f});tl.to("#smooth",{{opacity:1,duration:1.2,ease:"power1.inOut"}},{tBetter - 0.2:.3f});'
    f'tl.fromTo("#lumen",{{attr:{{r:80}}}},{{attr:{{r:120}},duration:1.2,ease:"power1.inOut",immediateRender:false}},{tBetter - 0.2:.3f});'); c.beat(tBetter)
c.out("#cp", tMostly - 0.2); c.stamp("#tp", tThree - 0.05, r=-3); c.pop("#no", tReal - 0.05)

# ---- C: the number (Jha 2013, NEJM; Toronto's Centre for Global Health Research) -- callback to ch1's ?? YRS
sC = (f'<div id="bx" style="position:absolute;left:220px;top:90px;width:760px;height:420px;border-radius:30px;background:#1b2b40;border:6px dashed {GOLD};text-align:center">'
      f'<div id="qy" style="position:absolute;left:0;width:100%;top:60px;font:170px InterBlack;color:{GOLD};white-space:nowrap">?? YRS</div>'
      f'<div id="dc" style="position:absolute;left:0;width:100%;top:60px;font:150px InterBlack;color:{CORAL};white-space:nowrap">~10 YRS</div>'
      f'<div id="dcl" style="position:absolute;left:0;width:100%;top:260px;font:50px InterBlack;color:{CREAM}">OF LIFE LOST TO SMOKING</div></div>'
      + f'<div id="tor" class="chip" style="left:100px;top:560px;background:{CREAM};font-size:40px">TORONTO RESEARCH</div>'
      + src_card("cJh", "JHA 2013 · NEJM", None, CORAL, left=620, top=560, width=460))
c.slide("sC", SC, SD, sC)
c.j('tl.set(["#dc","#dcl"],{opacity:0},0);'); c.pop("#bx", tNum - 0.1)
c.j(f'tl.fromTo("#qy",{{rotation:0}},{{rotation:4,duration:0.07,yoyo:true,repeat:5,immediateRender:false}},{tProm:.3f});'); c.beat(tProm)
c.pop("#tor", tToronto - 0.05); c.slide_in("#cJh", tNEJM - 0.1)
c.j(f'tl.to("#qy",{{rotationX:90,opacity:0,duration:0.2}},{tDecade - 0.3:.3f});'); c.pop("#dc", tDecade - 0.1, "hit"); c.punch(tDecade); c.rise("#dcl", tDecade + 0.3)

# ---- D: years gained by quit age + 90% ring
BARS = [("25 TO 34", "~10 YRS", 10, tTen, tQ1), ("35 TO 44", "~9 YRS", 9, tNine, tQ2), ("45 TO 54", "~6 YRS", 6, tSix, tQ3)]
bx = [120, 340, 560]; base = 600; unit = 40
bars = "".join(f'<rect id="bar{i}" x="{bx[i]}" y="{base - v * unit}" width="170" height="{v * unit}" rx="12" fill="{[GREEN, GOLD, SKY][i]}" stroke="{INK}" stroke-width="7"/>' for i, (_a, _b, v, _t, _q) in enumerate(BARS))
sD = (f'<div class="ptitle">YEARS YOU GET BACK, BY QUIT AGE</div>'
      + svg(f'<path d="M80 {base} H780" stroke="{CREAM}" stroke-width="6"/>{bars}'
            f'<circle cx="980" cy="330" r="150" fill="none" stroke="#24384f" stroke-width="44"/>'
            f'<circle id="rg" cx="980" cy="330" r="150" fill="none" stroke="{GREEN}" stroke-width="44" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" transform="rotate(-90 980 330)"/>')
      + "".join(f'<div id="bv{i}" class="lbl" style="left:{bx[i] - 10}px;width:190px;text-align:center;top:{base - v * unit - 64}px;font-size:40px;color:{CREAM}">{val}</div>'
                f'<div id="ba{i}" class="lbl" style="left:{bx[i] - 10}px;width:190px;text-align:center;top:{base + 16}px;font-size:36px;color:{[GREEN, GOLD, SKY][i]}">{age}</div>'
                for i, (age, val, v, _t, _q) in enumerate(BARS))
      + f'<div id="rgv" class="lbl" style="left:880px;width:200px;text-align:center;top:290px;font-size:64px;color:{GREEN}">90%</div>'
      + f'<div id="rgl" class="lbl" style="left:770px;width:420px;text-align:center;top:510px;font-size:34px;color:{CREAM}">LESS EXTRA RISK<br>IF YOU QUIT BEFORE 40</div>'
      + f'<div id="ntl" class="stamp" style="left:250px;top:250px;font-size:68px;color:{GOLD};border-color:{GOLD}">NEVER TOO LATE</div>')
c.slide("sD", SD, T, sD)
for i, (_a, _b, v, t, q) in enumerate(BARS):
    c.j(f'gsap.set("#bar{i}",{{svgOrigin:"{bx[i] + 85} {base}"}});tl.set("#bar{i}",{{scaleY:0}},0);tl.to("#bar{i}",{{scaleY:1,duration:0.6,ease:"back.out(1.4)"}},{q:.3f});')
    c.beat(q); c.fx("pop", q); c.pop(f"#ba{i}", q - 0.05, None); c.pop(f"#bv{i}", t - 0.05)
c.beat(tForty)
c.j(f'tl.fromTo("#rg",{{strokeDashoffset:100}},{{strokeDashoffset:10,duration:1.4,ease:"power2.out",immediateRender:false}},{tForty - 0.2:.3f});')
c.pop("#rgl", tForty - 0.1, None); c.pop("#rgv", tNinety - 0.05, "hit")
c.j(f'tl.to(["#bv0","#bv1","#bv2"],{{opacity:0,duration:0.15}},{tNeverTL - 0.2:.3f});'); c.stamp("#ntl", tNeverTL - 0.05, r=-4)

c.build(cyto_js_kw=dict(points=[(tYear - 0.1, 0.6), (tFif - 0.1, 0.6), (tLining - 0.1, 0.6), (tQ1 - 0.1, 0.6), (tForty - 0.1, 0.6)],
                        raises=[(tDecade - 0.2, 0.6), (tSooner, 0.7)], tilts=[(tHalf, 0.5, 6), (tOver, 0.6, -6), (tNine, 0.4, 6)], shrugs=[(tNeverTL - 0.1, 0.6)],
                        expr=[(tHalf - 0.05, 0.6, "hype"), (tSmoked - 0.05, 0.6, "hype"), (tOver - 0.05, 0.7, "squint"), (tNum - 0.05, 0.8, "squint"),
                              (tDecade - 0.05, 0.9, "shock"), (tTen - 0.05, 0.6, "hype"), (tNinety - 0.05, 0.7, "hype"), (tSooner - 0.05, 0.7, "hype")]),
        cap_keys={"half": GOLD, "fifteen": GREEN, "never": GREEN, "smoked": GREEN, "healing": GREEN, "copd": SKY, "better": GREEN, "quitting": GREEN,
                  "overnight": GOLD, "number": GOLD, "torontos": CREAM, "decade": CORAL, "25to34": GREEN, "10": GREEN, "35to44": GOLD, "9": GOLD,
                  "45to54": SKY, "6": SKY, "40": GREEN, "90%": GREEN, "sooner": GOLD})
