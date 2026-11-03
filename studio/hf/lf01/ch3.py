"""LF01 ch3: The first week. U of T (the 'Brain') bg. Mood icons; weed withdrawal meter (Bonnet 2017); brain receptor-reset diagram; water/movement/people."""
from lf import *
import lfart as L

c = Ch(3); wt = c.wt; T = c.T
tFirst, tLoud, tIrr, tRest, tSleep, tWeird = wt("first"), wt("loud"), wt("Irritable,"), wt("restless,"), wt("sleep"), wt("weird.")
tFor, tReview, tSub, tReg, tReal, tWith, tMostly, tMood, tSleep2, tLight, tMod = (wt("For"), wt("review"), wt("Substance"), wt("regular"), wt("real"), wt("withdrawal."),
    wt("Mostly"), wt("mood"), wt("sleep", 12), wt("light"), wt("moderate."))
tYour, tBrain, tCann, tRec, tReset, tWithin, tTwo, tDays = wt("Your"), wt("brain's"), wt("cannabinoid"), wt("receptors"), wt("resetting"), wt("within"), wt("two"), wt("days.", 15)
tNot, tDang, tAnn, tWater, tMove, tPeople = wt("Not"), wt("dangerous"), wt("annoying."), wt("Water,"), wt("movement,"), wt("people.", 20)
SA, SB, SC, SD = 0, tFor - 0.15, tYour - 0.15, tNot - 0.15

c.bg("bgU", 0, T, L.bg_uoft("ut"), kb=(1.0, 1.07))

# ---- A: the loud part
MOOD = [("angry", "IRRITABLE", tIrr, CORAL), ("jitter", "RESTLESS", tRest, GOLD), ("zzz", "SLEEP GETS WEIRD", tSleep, SKY)]
XA = [200, 600, 970]
sA = (f'<div id="lp" class="stamp" style="left:300px;top:60px;font-size:80px;color:{GOLD};border-color:{GOLD}">THE LOUD PART</div>'
      + svg("".join(f'<g id="mi{i}">{L.icon(k, XA[i], 400, 1.3)}</g>' for i, (k, _l, _t, _c) in enumerate(MOOD)))
      + "".join(f'<div id="ml{i}" class="lbl" style="left:{XA[i] - 210}px;width:420px;text-align:center;top:540px;font-size:40px;color:{col}">{lbl}</div>' for i, (_k, lbl, _t, col) in enumerate(MOOD)))
c.slide("sA", SA, SB, sA)
c.stamp("#lp", tLoud - 0.05, r=-3)
for i, (_k, _l, t, _c) in enumerate(MOOD):
    c.pop(f"#mi{i}", t - 0.1); c.j(f'gsap.set("#mi{i}",{{svgOrigin:"{XA[i]} 400"}});'); c.rise(f"#ml{i}", t + 0.1)
c.j(f'tl.fromTo("#mi1",{{x:-6}},{{x:6,duration:0.05,yoyo:true,repeat:15,immediateRender:false}},{tRest + 0.2:.3f});')

# ---- B: real withdrawal, mostly mood + sleep, light to moderate (Bonnet 2017)
sB = (f'<div id="rw" class="stamp" style="left:60px;top:60px;font-size:72px">REAL WITHDRAWAL</div>'
      + src_card("cBo", "BONNET 2017", "Subst Abuse Rehabil (review)", "#7a5cc7", left=660, top=640, width=500)
      + f'<div id="fw" class="chip" style="left:120px;top:200px;background:{GREEN};font-size:50px">FOR WEED</div>'
      + f'<div id="ru" class="chip" style="left:470px;top:200px;background:{CREAM};font-size:50px">REGULAR USERS</div>'
      + f'<div id="cm" class="chip" style="left:120px;top:260px;background:{CORAL};font-size:50px">MOOD</div>'
      + f'<div id="cs" class="chip" style="left:380px;top:260px;background:{SKY};font-size:50px">SLEEP</div>'
      + svg(f'<defs><linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{CORAL}"/></linearGradient></defs>'
            f'<rect id="mbar" x="100" y="470" width="1000" height="56" rx="28" fill="url(#mg)" stroke="{INK}" stroke-width="7"/>'
            f'<g id="knob"><circle cx="100" cy="498" r="44" fill="{CREAM}" stroke="{INK}" stroke-width="8"/></g>')
      + f'<div id="ml" class="lbl" style="left:100px;top:560px;font-size:44px;color:{GREEN}">LIGHT</div>'
      + f'<div id="mm" class="lbl" style="left:500px;top:560px;font-size:44px;color:{GOLD}">MODERATE</div>'
      + f'<div id="mh" class="lbl" style="left:960px;top:560px;font-size:44px;color:#7d8a99">SEVERE</div>')
c.slide("sB", SB, SC, sB)
c.pop("#fw", tFor); c.slide_in("#cBo", tSub - 0.1); c.pop("#ru", tReg - 0.05); c.out("#fw", tReal - 0.25); c.out("#ru", tReal - 0.25); c.stamp("#rw", tReal - 0.05, r=-3)
c.pop("#cm", tMood - 0.05); c.pop("#cs", tSleep2 - 0.05)
c.j(f'gsap.set("#mbar",{{svgOrigin:"100 498"}});tl.set("#mbar",{{scaleX:0}},0);tl.to("#mbar",{{scaleX:1,duration:0.5,ease:"power2.out"}},{tLight - 0.4:.3f});')
c.pop("#ml", tLight - 0.05, None); c.pop("#mh", tLight - 0.05, None)
c.j(f'tl.set("#knob",{{opacity:0}},0);tl.set("#knob",{{opacity:1}},{tLight:.3f});tl.fromTo("#knob",{{x:0}},{{x:500,duration:0.8,ease:"back.out(1.6)",immediateRender:false}},{tMod - 0.3:.3f});')
c.pop("#mm", tMod - 0.05)

# ---- C: brain receptor reset
sC = (svg(L.brain(430, 380, 1.25, "br"))
      + f'<div id="cr" class="lbl" style="left:60px;top:40px;font-size:44px;color:{GOLD}">CANNABINOID RECEPTORS</div>'
      + f'<div id="rs" class="chip" style="left:800px;top:220px;background:{GREEN};font-size:48px">RESETTING</div>'
      + f'<div id="w2" class="stamp" style="left:640px;top:400px;font-size:60px;color:{GREEN};border-color:{GREEN}">WITHIN 2 DAYS</div>')
c.slide("sC", SC, SD, sC)
c.pop("#cr", tCann - 0.05)
c.j(f'tl.fromTo("#brRec .rc",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.3,stagger:0.05,ease:"back.out(2)",immediateRender:false}},{tRec - 0.1:.3f});tl.set("#brRec .rc",{{opacity:0}},0);'); c.beat(tRec)
c.pop("#rs", tReset - 0.05)
c.j(f'document.querySelectorAll("#brRec .rc path").forEach((p,i)=>{{ if(i%2==0) tl.to(p,{{stroke:"{GREEN}",duration:0.2}},{tReset + 0.2:.3f}+i*0.12); }});'); c.beat(tReset + 0.6)
c.stamp("#w2", tTwo - 0.1, r=-3)

# ---- D: not dangerous, just annoying; water, movement, your people
HELP = [("water", "WATER", tWater, SKY), ("shoe", "MOVEMENT", tMove, BLUE), ("squad", "YOUR PEOPLE", tPeople - 0.4, GOLD)]
sD = (f'<div id="nd" class="big" style="left:0;width:{PW}px;top:60px;font-size:70px;color:{CREAM}">NOT DANGEROUS FOR MOST,<br><span style="color:{GOLD}">JUST ANNOYING</span></div>'
      + svg(f'<g id="an">{L.icon("jitter", 600, 470, 1.3)}</g>') + svg("".join(f'<g id="hi{i}">{L.icon(k, XA[i], 470, 1.2)}</g>' for i, (k, _l, _t, _c) in enumerate(HELP)))
      + "".join(f'<div id="hl{i}" class="chip" style="left:{XA[i] - [95, 135, 165][i]}px;top:620px;background:{col};font-size:42px">{lbl}</div>' for i, (_k, lbl, _t, col) in enumerate(HELP)))
c.slide("sD", SD, T, sD)
c.pop("#nd", tDang - 0.1); c.pop("#an", tAnn - 0.3, None); c.out("#an", tWater - 0.25)
for i, (_k, _l, t, _c) in enumerate(HELP):
    c.pop(f"#hi{i}", t - 0.1, None); c.pop(f"#hl{i}", t)

c.build(cyto_js_kw=dict(points=[(tIrr - 0.1, 0.5), (tSub - 0.1, 0.6), (tBrain - 0.1, 0.6), (tWater - 0.1, 0.5)], tilts=[(tWeird, 0.6, 7), (tAnn, 0.6, -6)],
                        shrugs=[(tAnn - 0.2, 0.6)], raises=[(tWater, 0.6)],
                        expr=[(tLoud - 0.05, 0.6, "shock"), (tIrr - 0.05, 0.7, "skeptic"), (tWeird - 0.05, 0.6, "squint"), (tReal - 0.05, 0.7, "squint"),
                              (tReset - 0.05, 0.7, "hype"), (tAnn - 0.05, 0.7, "skeptic"), (tPeople - 0.4, 0.6, "hype")]),
        cap_keys={"loud": GOLD, "irritable": CORAL, "restless": GOLD, "weird": SKY, "withdrawal": CORAL, "mood": CORAL, "light": GREEN, "moderate": GOLD,
                  "cannabinoid": GOLD, "receptors": GOLD, "resetting": GREEN, "two": GREEN, "water": SKY, "movement": BLUE, "people": GOLD})
