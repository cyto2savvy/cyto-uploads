"""LF01 ch1: What's in the smoke. Don Valley bg. Lungs + Neutro patrolling; weed vs tobacco split; tobacco leaf = nicotine card; 1 in 4."""
from lf import *
import lfart as L

c = Ch(1); wt = c.wt; T = c.T
tQuick, tAny, tHeat, tPart, tLungs = wt("Quick"), wt("Any"), wt("heat"), wt("particles"), wt("lungs.")
tNeut, tSec, tPat, tAir, tDon, tAll, tWears, tOut = wt("Neutro's"), wt("security"), wt("patrolling"), wt("airways"), wt("Don"), wt("All"), wt("wears"), wt("out.")
tWeed, tTob, tSame, tAnnals, tReg, tBron, tEase, tFar, tRisk = wt("Weed"), wt("tobacco"), wt("same."), wt("Annals"), wt("regular"), wt("bronchitis"), wt("ease"), wt("far"), wt("risk")
tBut, tLeaf, tBlunts, tGrab, tThats, tRes, tDeliv, tNic, tEven, tSo, tHooked, tReal = (wt("But"), wt("tobacco-leaf"), wt("blunts"), wt("grabba?"), wt("That's", 25),
    wt("Research"), wt("deliver"), wt("nicotine,"), wt("even"), wt("So"), wt("hooked"), wt("realizing."))
tAnd, tNiche, tAbout, tFour, tCan, tHC, tKeep, tNum, tYears, tBack = wt("And", 37), wt("niche."), wt("About"), wt("four"), wt("Canadians"), wt("Health"), wt("Keep"), wt("number"), wt("years"), wt("back.")
SA, SB, SC, SD, SE = 0, tWeed - 0.15, tBut - 0.15, tAnd - 0.15, tKeep - 0.15

c.bg("bgDV", 0, T, L.bg_don_valley("dv"), kb=(1.0, 1.07))
c.j(f'tl.fromTo("#dvCars",{{x:-400}},{{x:600,duration:{T:.2f},ease:"none",immediateRender:false}},0);')

# ---- A: lungs + particles + Neutro on patrol
import random
rnd = random.Random(11)
parts = "".join(f'<circle class="pt" cx="{rnd.uniform(240, 600):.0f}" cy="{rnd.uniform(-120, -20):.0f}" r="{rnd.uniform(6, 12):.0f}" fill="{rnd.choice(["#9aa0a8", "#c9b37a", "#7d838c"])}" data-y="{rnd.uniform(330, 520):.0f}"/>' for _ in range(40))
sweat = '<g id="sw"><path d="M0 0 q-14 22 0 30 q14 -8 0 -30Z" fill="#9fd3ff" stroke="#0c1622" stroke-width="4"/></g>'
sA = (svg(f'<g id="lgW">{A.lungs(420, 420, 1.25, "lg")}</g><g id="pts">{parts}</g>'
          f'<g id="sweatG" transform="translate(1010,250)">{sweat}</g>')
      + f'<div id="hc" class="chip" style="left:60px;top:110px;background:{CORAL}">HEAT</div>'
      + f'<div id="pc" class="chip" style="left:250px;top:110px;background:#c9ccd2">+ TINY PARTICLES</div>'
      + NT("nA", 760, 210, .62, "cross")
      + f'<div id="sg" class="chip" style="left:700px;top:110px;background:{PINK}">SECURITY GUARD</div>'
      + f'<div id="dvc" class="chip" style="left:330px;top:660px;background:{GREEN}">THE DON VALLEY OF THE BODY</div>'
      + f'<div id="wo" class="chip" style="left:780px;top:110px;background:{GOLD}">WORN OUT</div>')
c.slide("sA", SA, SB, sA, title=None)
c.pop("#hc", tHeat - 0.05); c.pop("#pc", tPart - 0.05)
c.j(f'document.querySelectorAll("#pts .pt").forEach((p,i)=>tl.fromTo(p,{{y:0,opacity:0}},{{y:+p.dataset.y,opacity:1,duration:1.6,ease:"power1.in",immediateRender:false}},{tPart:.3f}+(i%10)*0.12));')
c.j(f'tl.to("#lgL,#lgR",{{fill:"#d98a96",duration:0.6}},{tLungs:.3f});'); c.beat(tLungs)
c.rise("#nAW", tNeut - 0.1, 80, "pop")
c.j(f'tl.fromTo("#nAW",{{x:0}},{{x:180,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:3,immediateRender:false}},{tPat - 0.2:.3f});')
c.pop("#sg", tSec - 0.05); c.out("#sg", tPat + 0.9)
c.pop("#dvc", tDon - 0.05)
c.j(neutro_js("nA", poses=[(tSec, "flex"), (tPat, "cross"), (tWears, "idle")], brows=[(tNeut, "up"), (tWears, "down")],
              mouths=[(tSec, "smirk"), (tWears, "frown")], nods=[tSec + 0.3], blinks=[tAir, tOut + 0.4]))
c.j(f'tl.to("#nAM",{{y:30,duration:0.5,ease:"power2.out"}},{tWears:.3f});')
c.pop("#wo", tWears, "hit"); c.out("#dvc", tAll - 0.1)
c.pop("#sweatG", tOut - 0.1, None); c.j(f'tl.fromTo("#sw",{{y:0}},{{y:40,duration:0.6,repeat:1,ease:"power1.in",immediateRender:false}},{tOut:.3f});')
c.j(f'tl.set("#sweatG",{{opacity:0}},0);')

# ---- B: weed smoke vs tobacco smoke (Tashkin 2013)
sB = (f'<div id="hW" class="chip" style="left:90px;top:60px;background:{GREEN};font-size:50px">WEED SMOKE</div>'
      f'<div id="hT" class="chip" style="left:650px;top:60px;background:{CORAL};font-size:50px">TOBACCO SMOKE</div>'
      f'<div id="ne" class="lbl" style="left:565px;top:50px;font-size:90px;color:{GOLD}">≠</div>'
      + svg(f'<path d="M600 170 V600" stroke="#2c4d6e" stroke-width="6" stroke-dasharray="16 14"/>'
            f'<g id="bars"><rect x="120" y="560" width="220" height="0" fill="{GREEN}" stroke="{INK}" stroke-width="6" id="bW"/>'
            f'<rect x="760" y="560" width="220" height="0" fill="{CORAL}" stroke="{INK}" stroke-width="6" id="bT"/>'
            f'<path d="M80 562 H1120" stroke="{CREAM}" stroke-width="6"/></g>'
            f'<g id="lgw" opacity=".35">{A.lungs(230, 420, .55, "lgw")}</g><g id="lgt" opacity=".35">{A.lungs(870, 420, .55, "lgt")}</g>')
      + f'<div id="br" class="card" style="left:60px;top:190px;width:500px;border-left-color:{GREEN}"><h3 style="color:#1f7a45">BRONCHITIS SYMPTOMS</h3><p>ease after you stop</p></div>'
      + f'<div id="lr" class="lbl" style="left:400px;top:600px;font-size:44px;color:{GOLD}">LUNG RISK</div>'
      + f'<div id="lr2" class="lbl" style="left:110px;top:600px;font-size:38px;color:{GREEN}">FAR LOWER</div>'
      + src_card("cTa", "TASHKIN 2013", "Annals of the ATS (review)", BLUE, left=600, top=190, width=540))
c.slide("sB", SB, SC, sB)
c.pop("#hW", tWeed - 0.05); c.pop("#hT", tTob - 0.05); c.pop("#ne", tSame - 0.1, "hit")
c.slide_in("#cTa", tAnnals - 0.1)
c.out("#cTa", tReg + 0.2); c.slide_in("#br", tBron - 0.1)
c.j(f'tl.to("#bW",{{attr:{{y:470,height:90}},duration:0.6,ease:"back.out(1.6)"}},{tFar:.3f});tl.to("#bT",{{attr:{{y:250,height:310}},duration:0.7,ease:"back.out(1.4)"}},{tRisk:.3f});')
c.beat(tFar); c.beat(tRisk); c.fx("pop", tFar); c.fx("pop", tRisk)
c.out("#br", tFar - 0.3)
c.pop("#lr", tRisk + 0.1, None); c.pop("#lr2", tFar + 0.3, None)

# ---- C: tobacco-leaf wraps = tobacco = nicotine (flat icon card only)
hook_p = f'<path id="hk" d="M960 170 V330 Q960 400 900 400 Q840 400 840 345" fill="none" stroke="{CREAM}" stroke-width="18" stroke-linecap="round" {DRAW}/>'
sC = (f'<div class="ptitle">EXPLAINER</div>'
      + svg(L.leaf_icon(250, 330, 1.25, "lf") + hook_p)
      + f'<div id="eq1" class="lbl" style="left:430px;top:270px;font-size:110px;color:{GOLD}">=</div>'
      + f'<div id="nicC" class="chip" style="left:540px;top:290px;background:{GOLD};font-size:64px">NICOTINE</div>'
      + f'<div id="bw" class="chip" style="left:90px;top:520px;background:{CREAM};font-size:44px">BLUNT WRAPS</div>'
      + f'<div id="gb" class="chip" style="left:440px;top:520px;background:{CREAM};font-size:44px">GRABBA</div>'
      + f'<div id="ist" class="stamp" style="left:680px;top:500px;font-size:62px;color:{GOLD};border-color:{GOLD}">= TOBACCO</div>'
      + f'<div id="hkd" class="chip" style="left:360px;top:440px;background:{CORAL};font-size:46px">HOOKED WITHOUT REALIZING</div>'
      + src_card("cFa", "FAIRMAN 2023", "Blunts deliver real nicotine", SKY, left=60, top=640, width=620))
c.slide("sC", SC, SD, sC)
c.pop("#lf", tLeaf - 0.05); c.j('gsap.set("#lf",{svgOrigin:"0 0"});')
c.pop("#bw", tBlunts - 0.05); c.pop("#gb", tGrab - 0.05); c.stamp("#ist", tThats, r=-4)
c.out("#ist", tRes - 0.2); c.out("#bw", tRes - 0.2); c.out("#gb", tRes - 0.2)
c.pop("#eq1", tDeliv - 0.1, None); c.pop("#nicC", tNic - 0.1)
c.slide_in("#cFa", tRes + 0.2)
c.draw("#hk", tHooked - 0.1, 0.6, "pop"); c.pop("#hkd", tHooked + 0.2, None)

# ---- D: 1 in 4 Canadians (Health Canada CCS 2024)
ppl = "".join(L.person(200 + i * 260, 420, 1.5, GREEN if i == 0 else "#5d6f84", f"pp p{i}") for i in range(4))
sD = (f'<div id="nn" class="stamp" style="left:300px;top:60px;font-size:70px;color:{SKY};border-color:{SKY}">NOT NICHE</div>'
      + svg(ppl)
      + f'<div id="oif" class="big" style="left:0;width:{PW}px;top:520px;font-size:96px;color:{GREEN}">1 IN 4 CANADIANS</div>'
      + src_card("cHC", "HEALTH CANADA", "Canadian Cannabis Survey 2024", "#c8102e", left=640, top=60, width=520))
c.slide("sD", SD, SE, sD)
c.stamp("#nn", tNiche - 0.15, r=-3); c.out("#nn", tAbout - 0.1)
c.j(f'document.querySelectorAll("#sD .pp").forEach((p,i)=>tl.fromTo(p,{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)",immediateRender:false}},{tAbout:.3f}+i*0.12));'
    f'tl.set("#sD .pp",{{opacity:0}},0);'); c.beat(tAbout)
c.j(f'tl.fromTo("#sD .p0",{{scale:1}},{{scale:1.15,duration:0.3,yoyo:true,repeat:1,transformOrigin:"50% 100%",immediateRender:false}},{tFour:.3f});')
c.pop("#oif", tFour - 0.1, "hit"); c.slide_in("#cHC", tHC - 0.1)

# ---- E: open loop B
sE = (f'<div style="position:absolute;left:250px;top:110px;width:700px;height:470px;border-radius:30px;background:#1b2b40;border:6px dashed {GOLD};text-align:center">'
      f'<div id="qq" style="font:170px InterBlack;color:{GOLD};margin-top:30px;white-space:nowrap">?? YRS</div><div id="qt" style="font:52px InterBlack;color:{CREAM}">YOU CAN GET BACK</div></div>'
      f'<div id="ate" class="chip" style="left:420px;top:620px;background:{CORAL};font-size:46px">AT THE END</div>')
c.slide("sE", SE, T, sE)
c.pop("#qq", tNum - 0.05, "hit"); c.pop("#qt", tYears - 0.05, None); c.pop("#ate", tBack - 0.2)
c.j(f'tl.fromTo("#qq",{{rotation:0}},{{rotation:4,duration:0.07,yoyo:true,repeat:7,immediateRender:false}},{tYears:.3f});')

c.build(cyto_js_kw=dict(
    points=[(tLungs - 0.1, 0.6), (tNeut - 0.1, 0.7), (tAnnals - 0.1, 0.6), (tRes - 0.1, 0.6), (tAbout - 0.1, 0.6), (tNum - 0.1, 0.6)],
    tilts=[(tSame - 0.1, 0.5, 6), (tThats - 0.1, 0.6, -7), (tNiche - 0.1, 0.5, 6)], shrugs=[(tEven, 0.7)],
    expr=[(tQuick - 0.05, 0.6, "hype"), (tAll, 1.0, "sad"), (tSame - 0.05, 0.7, "squint"), (tFar - 0.05, 0.6, "hype"), (tBut - 0.05, 0.9, "skeptic"),
          (tHooked - 0.05, 0.9, "shock"), (tFour - 0.05, 0.6, "hype"), (tNum - 0.05, 0.8, "squint")],
    looks=[(tTob, 6, -5)]),
    cap_keys={"neutros": PINK, "lungs": "#ff8095", "don": GREEN, "valley": GREEN, "weed": GREEN, "tobacco": CORAL, "bronchitis": SKY, "lower": GREEN,
              "nicotine": GOLD, "blunts": GOLD, "grabba": GOLD, "hooked": CORAL, "four": GREEN, "canadians": GREEN, "number": GOLD, "years": GOLD})
