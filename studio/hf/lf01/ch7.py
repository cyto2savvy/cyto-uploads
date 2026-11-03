"""LF01 ch7: Outro. Toronto map tour (Lungs = Don Valley, Heart = downtown, Brain = U of T); comment question; 6 source screens
(2 per screen, >=2.5 s each, 34px+); Not medical advice end card; final line loops back to the hook frame (ch0 frame 0)."""
from lf import *
import lfart as L

c = Ch(7); wt = c.wt; T = c.T
tQuit, tTour, tSix, tLungs, tDon, tBreath, tHeart, tDown, tPump, tBrain, tU, tSleep = (wt("Quitting"), wt("tour"), wt("6ix."), wt("Lungs,"), wt("Don"),
    wt("breathing"), wt("Heart,"), wt("downtown,"), wt("pumping"), wt("Brain,"), wt("U"), wt("sleeping"))
tQ, tHard, tHabit, tCrav, tRead, tIf, tLike, tSub, tSrc, tDesc, tNot, tAnd, tTwenty, tThats, tStart, tYo, tCyto, tLive, tEnd6 = (wt("Question"), wt("hardest"), wt("habit"),
    wt("craving?"), wt("read"), wt("If"), wt("like"), wt("subscribe."), wt("Sources"), wt("description."), wt("Not"), wt("And", 22), wt("twenty"), wt("That's"), wt("start."),
    wt("Yo,"), wt("Cyto,"), wt("live"), wt("6ix…"))
SA, SB, SL = 0, tQ - 0.15, tTwenty - 0.25

c.bg("bgN", 0, SL, L.bg_downtown("bd7"), kb=(1.0, 1.07))
c.bg("bgH", SL, T, L.bg_night("bn"), kb=(1.0, 1.0))

# ---- A: map tour
lung_i = '<g transform="translate(0,-98) scale(.13)">' + A.lungs(0, 0, 1, "ml") + '</g>'
heart_i = L.heart(0, -98, .3, "mh")
brain_i = L.brain(0, -96, .11, "mb")
PINS = [("pL", 625, 300, GREEN, lung_i, tLungs, "LUNGS = DON VALLEY", "BREATHING EASY"),
        ("pH", 500, 470, CORAL, heart_i, tHeart, "HEART = DOWNTOWN", "PUMPING SMOOTHER"),
        ("pB", 405, 300, BLUE, brain_i, tBrain, "BRAIN = U OF T", "SLEEPING RIGHT")]
sA = (svg(f'<g id="mapZ">{L.toronto_map("tm")}' + "".join(L.pin(x, y, idp, col, ic) for idp, x, y, col, ic, *_ in PINS) + '</g>')
      + f'<div id="tt" class="chip" style="left:60px;top:40px;background:{GOLD};font-size:48px">A TOUR OF THE 6IX</div>'
      + "".join(f'<div id="{idp}C" class="chip" style="left:60px;top:650px;background:{col};font-size:46px">{a} <span style="color:#0c1622;opacity:.75">· {b}</span></div>'
                for idp, x, y, col, ic, t, a, b in PINS))
c.slide("sA", SA, SB, sA, panel=True)
c.pop("#tt", tTour - 0.1)
c.j('gsap.set("#mapZ",{svgOrigin:"600 395"});')
nxt = [tHeart, tBrain, tQ]
for i, (idp, x, y, col, ic, t, a, b) in enumerate(PINS):
    c.j(f'tl.set("#{idp}",{{opacity:0}},0);gsap.set("#{idp}",{{opacity:0}});tl.to("#{idp}",{{opacity:1,duration:0.1}},{t - 0.1:.3f});tl.fromTo("#{idp}I",{{y:-80}},{{y:0,duration:0.45,ease:"bounce.out",immediateRender:false}},{t - 0.1:.3f});')
    c.j(f'tl.to("#mapZ",{{scale:1.7,x:{(600 - x) * 1.7:.0f},y:{(395 - y) * 1.7 - 120:.0f},duration:0.7,ease:"power2.inOut"}},{t - 0.2:.3f});')
    c.beat(t); c.fx("pop", t)
    c.pop(f"#{idp}C", t + 0.2, None)
    c.j(f'tl.fromTo("#{idp}I",{{scale:1}},{{scale:1.18,duration:0.3,yoyo:true,repeat:3,svgOrigin:"0 -98",immediateRender:false}},{t + 0.6:.3f});')
    if i < 2: c.out(f"#{idp}C", nxt[i] - 0.25)
c.out("#tt", tLungs - 0.3)
c.j(f'tl.to("#mapZ",{{scale:1,x:0,y:0,duration:0.6,ease:"power2.inOut"}},{tSleep + 0.2:.3f});'); c.beat(tSleep + 0.2)

# ---- B: 6 source screens (2 each, 34px+), comment question + like/sub + end card in the bubble above Cyto
SRC = [("JHA 2013 · NEJM", "Smoking, quitting & years of life", "TASHKIN 2013 · ANNALS ATS", "Marijuana smoking & the lung"),
       ("BONNET 2017 · SUBST ABUSE REHABIL", "Cannabis withdrawal syndrome", "LAPPERRE 2007 · RESPIR RES", "Airway lining after quitting (COPD)"),
       ("FAIRMAN 2023 · DRUG ALCOHOL DEPEND", "Nicotine from blunts", "WALTERS 2023 · ADDICT BEHAV", "Cannabis & smoking in young adults"),
       ("HARTMANN-BOYCE 2021 · COCHRANE", "Behavioural support for quitting", "THEODOULOU 2023 · COCHRANE", "Nicotine replacement: combos & doses"),
       ("LIVINGSTONE-BANKS 2023 · COCHRANE", "Varenicline & receptor partial agonists", "HEALTH CANADA · CCS 2024", "Canadian Cannabis Survey"),
       ("CDC · SURGEON GENERAL 2004", "Within 20 minutes of quitting", "WHO", "Health benefits of smoking cessation")]
n = len(SRC); span = (tAnd - 0.1) - SB; d = span / n
cols = [CORAL, SKY, "#7a5cc7", BLUE, "#c8102e", GREEN]
html = ""
for i, (a1, b1, a2, b2) in enumerate(SRC):
    t0 = SB + i * d
    html += (f'<div id="sr{i}" class="clip" data-start="{t0:.3f}" data-duration="{d:.3f}" style="position:absolute;inset:0">'
             f'<div class="ptitle">SOURCES {i + 1} OF 6 · LINKS IN THE DESCRIPTION</div>'
             f'<div class="card" style="left:60px;top:150px;width:1080px;border-left-color:{cols[i]}"><h3 style="color:{cols[i]};font-size:44px">{a1}</h3><p style="font-size:38px">{b1}</p></div>'
             f'<div class="card" style="left:60px;top:420px;width:1080px;border-left-color:{cols[(i + 3) % 6]}"><h3 style="color:{cols[(i + 3) % 6]};font-size:44px">{a2}</h3><p style="font-size:38px">{b2}</p></div></div>')
    c.j(f'tl.fromTo("#sr{i} .card",{{x:120,opacity:0}},{{x:0,opacity:1,duration:0.35,stagger:0.12,ease:"back.out(1.6)",immediateRender:false}},{t0 + 0.02:.3f});')
    c.beat(t0); c.fx("pop", t0 + 0.05)
c.slide("sB", SB, SL, html)
c.css += "#sB .ptitle{color:#FFD166}"
# bubble above Cyto (left third, y 70-290): question -> like/subscribe -> NOT MEDICAL ADVICE
bub = (f'<div id="bub" class="clip tip" data-start="{SB:.3f}" data-duration="{SL - SB:.3f}" style="position:absolute;left:60px;top:70px;width:540px;height:220px;border-radius:36px;background:{CREAM};border:7px solid {INK};z-index:35;box-shadow:0 10px 0 {INK}">'
       f'<div id="bq" style="position:absolute;inset:0;padding:26px 30px;text-align:center;font:44px/1.12 InterBlack;color:{INK}">WHAT\'S HARDER:<br><span style="color:{CORAL}">THE HABIT</span> OR<br><span style="color:{BLUE}">THE CRAVING?</span></div>'
       f'<div id="bl" style="position:absolute;inset:0;padding:40px 30px;text-align:center;font:52px/1.15 InterBlack;color:{INK}">👍 LIKE +<br><span style="color:{CORAL}">SUBSCRIBE</span></div>'
       f'<div id="bm" style="position:absolute;inset:0;padding:40px 30px;text-align:center;font:52px/1.15 InterBlack;color:{CORAL}">NOT MEDICAL<br>ADVICE</div></div>')
c.overlay(bub)
c.j(f'tl.fromTo("#bub",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2)",immediateRender:false}},{SB + 0.05:.3f});tl.set(["#bl","#bm"],{{opacity:0}},0);'); c.fx("pop", SB + 0.05)
c.j(f'tl.to("#bq",{{opacity:0,duration:0.15}},{tIf - 0.2:.3f});tl.fromTo("#bl",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",immediateRender:false}},{tLike - 0.1:.3f});')
c.j(f'tl.to("#bl",{{opacity:0,duration:0.15}},{tNot - 0.2:.3f});tl.fromTo("#bm",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",immediateRender:false}},{tNot - 0.05:.3f});')
c.fx("pop", tLike); c.fx("chime", tSub); c.fx("hit", tNot)

# ---- loop: identical to the hook frame (ch0 frame 0): night bg, clock '20 MIN', hand back at 12
loop = svg(L.clock(330, 400, 250, "ck", "20 MIN"))
c.slide("sL", SL, T, loop, s="whoosh")
c.j('gsap.set("#ckHand",{svgOrigin:"330 400"});')
c.j(f'tl.fromTo("#ckHand",{{rotation:-720}},{{rotation:0,duration:{T - SL:.2f},ease:"power1.out",immediateRender:false}},{SL:.3f});')
c.j(f'tl.fromTo("#ckArc",{{strokeDashoffset:100}},{{strokeDashoffset:0,duration:{T - SL - 0.3:.2f},ease:"power1.out",immediateRender:false}},{SL:.3f});')
c.j(f'tl.to("#ck",{{scale:1.04,duration:0.15,yoyo:true,repeat:1,svgOrigin:"330 400"}},{tTwenty:.3f});'); c.beat(tTwenty); c.beat(tStart); c.beat(tYo)
c.fx("hit", tTwenty)

c.build(cyto_js_kw=dict(points=[(tLungs - 0.1, 0.6), (tHeart - 0.1, 0.6), (tBrain - 0.1, 0.6), (tSrc - 0.1, 0.7)], waves=[tYo],
                        raises=[(tTour, 0.6), (tSub, 0.6)], tilts=[(tHabit, 0.5, 6), (tCrav, 0.5, -6), (tNot, 0.5, 6)],
                        expr=[(tTour - 0.05, 0.6, "hype"), (tBreath - 0.05, 0.6, "hype"), (tHard - 0.05, 0.8, "squint"), (tLike - 0.05, 0.6, "hype"),
                              (tNot - 0.05, 0.7, "squint"), (tTwenty - 0.05, 0.6, "hype"), (tCyto - 0.05, 0.5, "hype")]),
        cap_keys={"6ix": GOLD, "lungs": GREEN, "don": GREEN, "valley": GREEN, "heart": CORAL, "downtown": CORAL, "brain": SKY, "campus": SKY,
                  "habit": CORAL, "craving": BLUE, "subscribe": CORAL, "sources": GOLD, "medical": CORAL, "twenty": GOLD, "minutes": GOLD, "cyto": TEAL})
