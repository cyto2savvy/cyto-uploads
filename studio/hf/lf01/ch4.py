"""LF01 ch4: Weeks 2-4. Kensington bg. Punch: calendar flips to WEEK 4 + 'IT FLIPS' stamp + shake; receptors back to normal;
Neutro gets a break; cilia sweeping animation; cleanup, not failure."""
from lf import *
import lfart as L

c = Ch(4); wt = c.wt; T = c.T
tWeek, tFour, tFlips, tThose, tCann, tBack, tNormal, tPer, tCrav, tFade, tSleep, tComes = (wt("Week"), wt("four"), wt("flips."), wt("Those"), wt("cannabinoid"),
    wt("back"), wt("normal"), wt("per"), wt("Cravings"), wt("fade."), wt("Sleep"), wt("comes"))
tIn, tLungs, tNeutro, tBreak, tCilia, tTiny, tSweep, tStart, tMoving, tCough, tFirst, tCleanup, tFail, tKeep = (wt("In"), wt("Lungs,"), wt("Neutro"), wt("break."),
    wt("cilia,"), wt("tiny"), wt("sweepers,"), wt("start"), wt("moving"), wt("cough"), wt("first."), wt("cleanup,"), wt("failure."), wt("Keep"))
SA, SB = 0, tIn - 0.15

c.bg("bgK", 0, T, L.bg_kensington("kn"), kb=(1.0, 1.08))
c.j(f'document.querySelectorAll("#bgK .bulb").forEach((b,i)=>tl.fromTo(b,{{opacity:1}},{{opacity:.3,duration:0.4,yoyo:true,repeat:{int(T / 0.4)},immediateRender:false}},(i%3)*0.13));')

# ---- A: the flip (punch moment) + receptors back to normal
sA = (L.calendar(70, 150, 440, 420, "cal")
      + f'<div id="itf" class="stamp" style="left:580px;top:200px;font-size:96px;color:{GREEN};border-color:{GREEN}">IT FLIPS</div>'
      + svg(f'<g id="bm">{L.brain(860, 250, .62, "b4")}</g>')
      + f'<div id="btn" class="chip" style="left:620px;top:440px;background:{GREEN};font-size:46px">BACK TO NORMAL</div>'
      + f'<div id="cf" class="chip" style="left:620px;top:440px;background:{GOLD};font-size:46px">CRAVINGS FADE</div>'
      + f'<div id="sc" class="chip" style="left:620px;top:540px;background:{SKY};font-size:46px">SLEEP COMES BACK</div>'
      + src_card("cBo4", "BONNET 2017", "same review", "#7a5cc7", left=640, top=640, width=520))
c.slide("sA", SA, SB, sA)
# flips start as the title card leaves (title 0.1-1.65)
c.rise("#cal", 1.62, 40)
for i in range(3):
    c.j(f'tl.to("#calP{i}",{{rotationX:-100,opacity:0,duration:0.2,ease:"power2.in"}},{1.9 + i * 0.2:.3f});')
c.fx("whoosh", 1.9); c.beat(1.9); c.beat(2.2)
c.stamp("#itf", 2.5, r=-5)
c.j('tl.fromTo("#cal",{rotation:0},{rotation:-4,duration:0.08,yoyo:true,repeat:5,immediateRender:false},2.5);'
    'tl.fromTo("#punch",{x:0},{x:14,duration:0.05,yoyo:true,repeat:7,immediateRender:false},2.53);tl.set("#punch",{x:0},3.0);')
c.out("#itf", tNormal - 0.45)
c.pop("#bm", tNormal - 0.3, None); c.j(f'tl.set("#b4Rec .rc path",{{stroke:"{GREEN}"}},0);')
c.j(f'tl.fromTo("#b4Rec .rc",{{scale:0.3}},{{scale:1,duration:0.25,stagger:0.05,ease:"back.out(2)",immediateRender:false}},{tNormal - 0.1:.3f});')
c.pop("#btn", tNormal - 0.05); c.slide_in("#cBo4", tPer - 0.1)
c.out("#btn", tCrav - 0.25); c.pop("#cf", tCrav - 0.05); c.pop("#sc", tSleep - 0.05, "chime")

# ---- B: Neutro's break, then the cilia sweep
sB = (f'<div id="g1" style="position:absolute;inset:0">' + svg(A.lungs(260, 360, 1.0, "l4"))
      + NT("n4", 560, 90, .55, "idle")
      + f'<div id="brk" class="chip" style="left:600px;top:560px;background:{PINK};font-size:50px">NEUTRO\'S BREAK</div></div>'
      + f'<div id="g2" style="position:absolute;inset:0">' + svg(L.cilia(60, 520, 1080, "cil"))
      + f'<div id="cll" class="lbl" style="left:60px;top:60px;font-size:54px;color:{CREAM}">CILIA = TINY SWEEPERS</div>'
      + f'<div id="cm" class="chip" style="left:60px;top:170px;background:{GOLD};font-size:44px">YOU MIGHT COUGH MORE AT FIRST</div>'
      + f'<div id="cnf" class="stamp" style="left:120px;top:150px;font-size:76px;color:{GREEN};border-color:{GREEN}">CLEANUP, NOT FAILURE</div>'
      + f'<div id="kg" class="chip" style="left:720px;top:60px;background:{GREEN};font-size:46px">KEEP GOING →</div></div>')
c.slide("sB", SB, T, sB)
c.j('tl.set("#g2",{opacity:0},0);')
c.pop("#n4W", tNeutro - 0.15, None); c.j('tl.set("#n4W",{scale:.55},0);')
c.j(neutro_js("n4", poses=[(tBreak - 0.05, "idle")], mouths=[(tFinally := wt("finally"), "smirk")], brows=[(tBreak, "flat")], blinks=[tBreak + 0.1], nods=[tBreak]))
c.j(f'tl.to("#n4M",{{rotation:-8,svgOrigin:"300 700",duration:0.4,ease:"sine.inOut"}},{tBreak:.3f});')
c.pop("#brk", tBreak - 0.1)
c.j(f'tl.to("#g1",{{opacity:0,duration:0.2}},{tCilia - 0.2:.3f});tl.to("#g2",{{opacity:1,duration:0.25}},{tCilia - 0.05:.3f});'); c.beat(tCilia)
c.rise("#cll", tTiny - 0.1)
# cilia beat (wave of strokes) + mucus slides right once they 'start moving'
c.j('document.querySelectorAll("#cil .cl").forEach((h,i)=>{ gsap.set(h,{svgOrigin:h.dataset.x+" 520"}); tl.fromTo(h,{rotation:-4},{rotation:28,duration:0.32,yoyo:true,repeat:%d,ease:"sine.inOut",immediateRender:false},%.3f+i*0.04); });'
    % (int((T - tStart) / 0.32), tStart - 0.3))
c.j(f'tl.fromTo("#cil .mu",{{x:0}},{{x:420,duration:{T - tStart:.2f},ease:"none",immediateRender:false}},{tStart:.3f});'); c.beat(tMoving)
c.out("#cll", tCough - 0.3); c.pop("#cm", tCough - 0.1)
c.out("#cm", tCleanup - 0.25); c.stamp("#cnf", tCleanup - 0.05, r=-3)
c.pop("#kg", tKeep - 0.05, "chime")

c.build(cyto_js_kw=dict(raises=[(tFlips, 0.7)], points=[(tThose - 0.1, 0.6), (tCilia - 0.1, 0.6)], tilts=[(tFade, 0.5, 6), (tFirst, 0.6, -6)],
                        shrugs=[(tCough - 0.1, 0.6)],
                        expr=[(tWeek - 0.0, 1.0, "hype"), (tFlips - 0.05, 0.7, "shock"), (tNormal - 0.05, 0.6, "hype"), (tBreak - 0.05, 0.6, "hype"),
                              (tCough - 0.05, 0.7, "skeptic"), (tCleanup - 0.05, 0.7, "hype"), (tKeep - 0.05, 0.6, "hype")]),
        cap_keys={"four": GREEN, "flips": GREEN, "normal": GREEN, "cravings": GOLD, "fade": GOLD, "sleep": SKY, "lungs": "#ff8095", "neutro": PINK,
                  "break": PINK, "cilia": GOLD, "sweepers": GOLD, "cough": CORAL, "cleanup": GREEN, "failure": CORAL, "going": GREEN})
