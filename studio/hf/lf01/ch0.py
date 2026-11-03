"""LF01 ch0: Hook (countdown clock) + intro (catchphrase, 3 kinds of smoke, 1-month anniversary, Not medical advice)."""
import random
from lf import *
import lfart as L

c = Ch(0); wt = c.wt
tTwenty, tThats, tHeart, tDrop, tStick = 0.0, wt("That's"), wt("heart"), wt("dropping."), wt("Stick")
tTwelve, tWeek, tOne, tFifteen, tPlus, tTrig, tSlip = wt("twelve,"), wt("week"), wt("one,"), wt("fifteen."), wt("Plus"), wt("trigger"), wt("slip.")
tYo, tCyto, tLive, tSix, tInside, tToday, tCount, tStops = wt("Yo,"), wt("Cyto,"), wt("live"), wt("6ix…"), wt("inside"), wt("Today's"), wt("countdown:"), wt("stops.")
tCig, tWeed, tGrab, tNo, tJudg, tFam, tShout, tAnniv = wt("Cigarettes,"), wt("weed,"), wt("grabba."), wt("No"), wt("judgment,"), wt("fam."), wt("shout-out:"), wt("anniversary.")
tOneM, tSix2, tBig, tLove, tWatch, tNot, tTalk, tDoc = wt("One", 28.5), wt("6ix,", 25), wt("Big"), wt("love"), wt("watching."), wt("Not"), wt("talk"), wt("doctor.")
T = c.T
S1, S2, S3, S4, S5 = 0, tYo - 0.1, tCig - 0.15, tShout - 0.1, tNot - 0.12

# ---------------- backgrounds
c.bg("bgA", 0, S3, L.bg_night("bn"), kb=(1.0, 1.08))
c.bg("bgB", S3, T, L.bg_downtown("bd"), kb=(1.04, 1.0))
c.j(f'document.querySelectorAll("#bnCity .win").forEach((w,i)=>{{ if(i%5==0) tl.fromTo(w,{{opacity:.9}},{{opacity:.15,duration:0.5,repeat:{int(S3 / 0.5)},yoyo:true,immediateRender:false}},(i%11)*0.17); }});')

# ---------------- S1 hook: countdown clock (frame 0 = loop target). Movers in 0-3 s: clock hand, caption, Cyto.
MIL = [("12 HRS", tTwelve, CORAL), ("WEEK 4", tWeek + 0.1, GOLD), ("YEAR 1", tOne, GREEN), ("YEAR 15", tFifteen, SKY)]
s1 = (svg(L.clock(330, 400, 250, "ck", "20 MIN") + L.heart(860, 250, 1.1, "hh") +
          f'<path id="ecg" d="{L.ecg_path(700, 470, 420, 3, 110)}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linejoin="round" {DRAW}/>'
          f'<g id="arrow"><path d="M1090 200 V330" stroke="{GREEN}" stroke-width="22" stroke-linecap="round"/><path d="M1050 300 L1090 350 L1130 300" fill="none" stroke="{GREEN}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/></g>')
      + "".join(f'<div id="m{i}" class="chip" style="left:700px;top:{120 + i * 130}px;background:{col};font-size:56px">{lbl}</div>' for i, (lbl, _, col) in enumerate(MIL))
      + f'<div id="myst" style="position:absolute;left:640px;top:170px;width:500px;height:420px;border-radius:30px;background:#1b2b40;border:6px dashed {GOLD};text-align:center">'
        f'<div style="font:180px InterBlack;color:{GOLD};margin-top:20px">?</div><div style="font:46px InterBlack;color:{CREAM};line-height:1.1">THE #1 TRIGGER</div></div>')
c.slide("s1", S1, S2, s1)
c.j('gsap.set("#ckHand",{svgOrigin:"330 400"});')
c.j(f'tl.fromTo("#ckHand",{{rotation:0}},{{rotation:360*4,duration:{S2:.2f},ease:"none",immediateRender:false}},0);')
c.j(f'tl.fromTo("#ckArc",{{strokeDashoffset:0}},{{strokeDashoffset:92,duration:{S2:.2f},ease:"none",immediateRender:false}},0);')
c.pop("#hh", tHeart - 0.05); c.j('gsap.set("#hh",{svgOrigin:"0 0"});')
c.j(f'tl.to("#hh",{{scale:1.12,duration:0.18,yoyo:true,repeat:5,ease:"sine.inOut"}},{tHeart + 0.35:.3f});')
c.draw("#ecg", tHeart + 0.1, 0.9)
c.pop("#arrow", tDrop, "pop"); c.j(f'tl.fromTo("#arrow",{{y:-30}},{{y:20,duration:0.5,ease:"power2.in",immediateRender:false}},{tDrop:.3f});')
c.j(f'tl.to(["#hh","#ecg","#arrow"],{{opacity:0,duration:0.2}},{tTwelve - 0.3:.3f});')
for i, (lbl, t, col) in enumerate(MIL): c.pop(f"#m{i}", t - 0.05)
c.j(f'tl.to(["#m0","#m1","#m2","#m3"],{{opacity:0,x:60,duration:0.2,stagger:0.04}},{tPlus - 0.1:.3f});')
c.pop("#myst", tTrig - 0.2, "hit")
c.j(f'tl.fromTo("#myst",{{rotation:0}},{{rotation:3,duration:0.06,yoyo:true,repeat:5}},{tSlip:.3f});')

# ---------------- S2 catchphrase (no panel: big text over the night city)
s2 = (f'<div id="t2a" class="big" style="left:0;width:{PW}px;top:150px;font-size:150px;color:{GOLD}"><span style="font-size:70px;color:{CREAM}">LIVE FROM</span><br>THE 6IX</div>'
      f'<div id="t2b" class="chip" style="left:330px;top:500px;background:{TEAL};font-size:52px">...INSIDE YOUR BODY</div>'
      f'<div id="t2c" class="big" style="left:0;width:{PW}px;top:170px;font-size:120px;color:{CREAM}"><span style="font-size:64px;color:{GOLD}">TODAY\'S COUNTDOWN</span><br>WHEN THE<br>SMOKE STOPS</div>')
c.slide("s2", S2, S3, s2, panel=False)
c.stamp("#t2a", tLive - 0.05, r=0); c.slide_in("#t2b", tInside)
c.out("#t2a", tToday - 0.3); c.out("#t2b", tToday - 0.3)
c.pop("#t2c", tCount)
c.j(f'tl.to("#t2c",{{scale:1.06,duration:0.2,yoyo:true,repeat:1}},{tStops:.3f});'); c.beat(tStops)

# ---------------- S3 three kinds of smoke (word chips only, no products)
KIND = [("CIGARETTES", tCig, CORAL), ("WEED", tWeed, GREEN), ("GRABBA", tGrab, GOLD)]
s3 = ('<div class="ptitle">TODAY: ALL THREE</div>'
      + "".join(f'<div id="k{i}" class="chip" style="left:{[60, 520, 800][i]}px;top:230px;background:{col};font-size:54px">{lbl}</div>' for i, (lbl, _, col) in enumerate(KIND))
      + "".join(f'<div id="kd{i}" class="lbl" style="left:{[90, 545, 800][i]}px;top:340px;font-size:38px;color:{SKY}">{d}</div>' for i, d in enumerate(("= TOBACCO", "= CANNABIS", "= TOBACCO LEAF")))
      + f'<div id="nj" class="stamp" style="left:300px;top:450px;color:{GREEN};border-color:{GREEN}">NO JUDGMENT</div>')
c.slide("s3", S3, S4, s3)
for i, (_, t, _c) in enumerate(KIND): c.pop(f"#k{i}", t - 0.05); c.rise(f"#kd{i}", t + 0.3)
c.stamp("#nj", tJudg, r=-4)

# ---------------- S4 one-month anniversary
rnd = random.Random(4)
conf = "".join(f'<rect class="cf" x="590" y="330" width="{rnd.randint(14, 24)}" height="{rnd.randint(24, 40)}" rx="4" fill="{rnd.choice([CORAL, GOLD, GREEN, SKY, PINK])}" '
               f'data-x="{rnd.uniform(-560, 560):.0f}" data-y="{rnd.uniform(-300, 380):.0f}" data-r="{rnd.uniform(-400, 400):.0f}"/>' for _ in range(46))
s4 = (svg(conf + f'<g id="badge"><circle cx="600" cy="320" r="190" fill="{GOLD}" stroke="{INK}" stroke-width="10"/>'
          f'<circle cx="600" cy="320" r="160" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="14 12"/>'
          f'<text x="600" y="345" text-anchor="middle" font-family="InterBlack" font-size="170" fill="{INK}">1</text>'
          f'<text x="600" y="420" text-anchor="middle" font-family="InterBlack" font-size="52" fill="{INK}">MONTH</text></g>'
          + L.heart(990, 210, .8, "lv") + L.heart(200, 230, .55, "lv2", PINK))
      + f'<div id="an" class="chip" style="left:395px;top:560px;background:{CORAL};font-size:52px">ANNIVERSARY</div>'
      + f'<div id="an2" class="chip" style="left:310px;top:560px;background:{TEAL};font-size:52px">THANK YOU, FAM</div>')
c.slide("s4", S4, S5, s4)
c.pop("#badge", tShout + 0.1, "hit"); c.j('gsap.set("#badge",{svgOrigin:"600 320"});')
c.j(f'tl.fromTo("#badge",{{rotation:-8}},{{rotation:8,duration:0.8,yoyo:true,repeat:{int((S5 - tShout) / 0.8)},ease:"sine.inOut",immediateRender:false}},{tShout + 0.4:.3f});')
c.pop("#an", tAnniv - 0.05, "chime")
c.j(f'document.querySelectorAll("#s4 .cf").forEach((e,i)=>tl.fromTo(e,{{x:0,y:0,rotation:0,opacity:1}},{{x:+e.dataset.x,y:+e.dataset.y+200,rotation:+e.dataset.r,opacity:0,duration:2.2,ease:"power2.out",immediateRender:false}},{tAnniv:.3f}));')
c.j('tl.set("#s4 .cf",{opacity:0},0);'); c.punch(tAnniv)
c.out("#an", tBig - 0.25); c.pop("#an2", tBig)
c.pop("#lv", tLove - 0.05); c.pop("#lv2", tLove + 0.25, None)
c.j(f'tl.to(["#lv","#lv2"],{{y:-30,duration:0.4,yoyo:true,repeat:3,ease:"sine.inOut"}},{tLove + 0.4:.3f});')

# ---------------- S5 start card: Not medical advice
s5 = (f'<div class="ptitle">BEFORE WE START</div>'
      f'<div id="nma" class="stamp" style="left:150px;top:180px;font-size:84px;color:{CORAL}">NOT MEDICAL ADVICE</div>'
      + svg(f'<g id="doc">{L.icon("rx", 360, 560, 1.0)}</g>')
      + f'<div id="tdoc" class="chip" style="left:440px;top:500px;background:{SKY};font-size:52px">TALK TO YOUR DOCTOR</div>')
c.slide("s5", S5, T, s5)
c.stamp("#nma", wt("medical") - 0.1, r=-3)
c.pop("#doc", tTalk - 0.1, None); c.pop("#tdoc", tTalk)

# ---------------- Cyto acting
c.build(cyto_js_kw=dict(
    waves=[tYo], raises=[(tAnniv, 0.8)], points=[(0.3, 0.9), (tTwelve - 0.1, 0.6), (tCig - 0.1, 0.6)],
    tilts=[(tSix, 0.5, 7), (tFam, 0.6, -7), (tDoc, 0.5, 6)], shrugs=[(tTrig, 0.7)],
    expr=[(0.0, 1.0, "squint"), (tDrop - 0.05, 0.7, "shock"), (tTrig - 0.05, 0.8, "skeptic"), (tCyto - 0.05, 0.5, "hype"), (tSix - 0.05, 0.6, "hype"),
          (tJudg - 0.05, 0.7, "hype"), (tAnniv - 0.05, 0.9, "hype"), (tLove - 0.05, 0.7, "hype"), (tNot - 0.05, 0.9, "squint")],
    looks=[(tToday, 6, -5)]),
    cap_keys={"twenty": GOLD, "minutes": GOLD, "heart": "#ff8095", "twelve": CORAL, "four": GOLD, "fifteen": SKY, "trigger": CORAL, "slip": CORAL,
              "cyto": TEAL, "6ix": GOLD, "countdown": GOLD, "cigarettes": CORAL, "weed": GREEN, "grabba": GOLD, "fam": TEAL, "anniversary": CORAL,
              "love": PINK, "medical": CORAL, "doctor": SKY},
    extra_css=f"#myst{{opacity:0}}")
