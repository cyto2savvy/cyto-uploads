"""LF01 ch2: The first hours. Downtown (the 'Heart') bg. Heart-rate line, CO gauge (12 h), clock, 2 wk-9 mo recovery bars; cravings = receptors + waves."""
from lf import *
import lfart as L

c = Ch(2); wt = c.wt; T = c.T
tOk, tCount, tTw, tHeart, tDrop = wt("Okay,"), wt("countdown."), wt("Twenty"), wt("heart"), wt("dropping.")
tTwelve, tCarbon, tMon, tBlood, tNormal, tOxy, tMusc, tBrain = wt("Twelve"), wt("carbon"), wt("monoxide"), wt("blood"), wt("normal,"), wt("oxygen"), wt("muscles"), wt("brain.")
tTwo, tWeeks, tCirc, tLung, tImpr, tOne, tNine, tCough, tBreath, tDrop2 = wt("Two"), wt("weeks"), wt("circulation"), wt("lung"), wt("improving."), wt("One"), wt("nine"), wt("coughing"), wt("breathlessness"), wt("drop.")
tThen, tCrav, tNic, tRec, tRefill, tTot, tThey, tWaves, tEvery, tPasses = wt("Then"), wt("cravings."), wt("nicotine"), wt("receptors"), wt("refill."), wt("Totally"), wt("They"), wt("waves,"), wt("every"), wt("passes.")
SA, SB = 0, tThen - 0.15

c.bg("bgD", 0, T, L.bg_downtown("bd"), kb=(1.0, 1.08))
c.j(f'document.querySelectorAll("#bdCity .win").forEach((w,i)=>{{ if(i%4==0) tl.fromTo(w,{{opacity:.9}},{{opacity:.2,duration:0.6,repeat:{int(T / 0.6)},yoyo:true,immediateRender:false}},(i%7)*0.2); }});')

# ---- A: the countdown timeline
ST = [("20 MIN", tTw, CORAL), ("12 HRS", tTwelve, GOLD), ("2 WKS TO 3 MOS", tTwo, GREEN), ("1 TO 9 MOS", tOne, SKY)]
XS = [40, 250, 450, 830]
row = "".join(f'<div id="st{i}" class="chip" style="left:{XS[i]}px;top:660px;background:#3a4a5e;color:{CREAM};font-size:40px">{lbl}</div>' for i, (lbl, _, _c) in enumerate(ST))
ecg_fast = L.ecg_path(80, 330, 560, 6, 120); ecg_slow = L.ecg_path(80, 330, 560, 3, 120)
f1 = (f'<div id="f1" style="position:absolute;inset:0">' + svg(L.heart(820, 300, 1.5, "hrt") +
      f'<path id="eF" d="{ecg_fast}" fill="none" stroke="{CORAL}" stroke-width="10" stroke-linejoin="round" {DRAW}/>'
      f'<path id="eS" d="{ecg_slow}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linejoin="round" {DRAW} transform="translate(0,0)"/>'
      f'<g id="ar1"><path d="M1060 200 V350" stroke="{GREEN}" stroke-width="24" stroke-linecap="round"/><path d="M1015 315 L1060 370 L1105 315" fill="none" stroke="{GREEN}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/></g>')
      + f'<div id="hrl" class="lbl" style="left:80px;top:470px;font-size:48px;color:{GREEN}">HEART RATE DROPS</div></div>')
o2 = "".join(f'<g class="o2" data-x="{dx}" data-y="{dy}"><circle cx="700" cy="330" r="22" fill="{SKY}" stroke="{INK}" stroke-width="5"/><text x="700" y="340" text-anchor="middle" font-family="InterBlack" font-size="22" fill="{INK}">O2</text></g>'
             for dx, dy in ((120, -150), (140, 120), (90, -60), (150, 40), (110, 160), (140, -110)))
f2 = (f'<div id="f2" style="position:absolute;inset:0">' + svg(L.gauge(330, 400, 210, "gg") + o2)
      + f'<div id="col" class="lbl" style="left:120px;top:440px;font-size:44px;color:{CREAM}">CARBON MONOXIDE</div>'
      + f'<div id="nml" class="chip" style="left:170px;top:520px;background:{GREEN};font-size:46px">BACK TO NORMAL</div>'
      + f'<div id="mu" class="chip" style="left:925px;top:180px;background:{CORAL};font-size:42px">MUSCLES</div>'
      + f'<div id="bri" class="chip" style="left:950px;top:420px;background:{PINK};font-size:42px">BRAIN</div></div>')
f3 = (f'<div id="f3" style="position:absolute;inset:0">'
      + svg(f'<rect x="60" y="230" width="1080" height="70" rx="35" fill="#24384f" stroke="{INK}" stroke-width="6"/><rect id="rb1" x="60" y="230" width="1080" height="70" rx="35" fill="{GREEN}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="60" y="470" width="1080" height="70" rx="35" fill="#24384f" stroke="{INK}" stroke-width="6"/><rect id="rb2" x="60" y="470" width="1080" height="70" rx="35" fill="{SKY}" stroke="{INK}" stroke-width="6"/>')
      + f'<div id="r1l" class="lbl" style="left:70px;top:150px;font-size:46px;color:{GREEN}">CIRCULATION + LUNG FUNCTION ↑</div>'
      + f'<div id="r2l" class="lbl" style="left:70px;top:390px;font-size:46px;color:{SKY}">COUGHING + BREATHLESSNESS ↓</div></div>')
sA = f1 + f2 + f3 + row + src_card("cCW", "CDC · WHO", None, CORAL, left=760, top=30, width=400)
c.slide("sA", SA, SB, sA)
c.j('tl.set(["#f2","#f3"],{opacity:0},0);')
for i, (_, t, col) in enumerate(ST):
    c.pop(f"#st{i}", t - 0.1)
    c.j(f'tl.to("#st{i}",{{backgroundColor:"{col}",color:"#0c1622",duration:0.2}},{t:.3f});')
    if i: c.j(f'tl.to("#st{i - 1}",{{backgroundColor:"#3a4a5e",color:"{CREAM}",duration:0.2}},{t:.3f});')
c.slide_in("#cCW", tTw + 0.3)
c.pop("#hrt", tHeart - 0.1, None); c.j('gsap.set("#hrt",{svgOrigin:"0 0"});tl.fromTo("#hrt",{scale:1},{scale:1.12,duration:0.25,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false},%.3f);' % tHeart)
c.draw("#eF", tTw + 0.2, 0.8); c.j(f'tl.to("#eF",{{opacity:0,duration:0.2}},{tDrop - 0.1:.3f});'); c.draw("#eS", tDrop, 0.8)
c.pop("#ar1", tDrop, "pop"); c.rise("#hrl", tDrop + 0.2)
c.j(f'tl.to("#f1",{{opacity:0,duration:0.2}},{tTwelve - 0.25:.3f});tl.to("#f2",{{opacity:1,duration:0.25}},{tTwelve - 0.05:.3f});'); c.beat(tTwelve)
c.j('gsap.set("#ggN",{svgOrigin:"330 400"});')
c.j(f'tl.set("#ggN",{{rotation:-20}},0);tl.to("#ggN",{{rotation:-175,duration:1.0,ease:"elastic.out(1,0.5)"}},{tNormal - 0.3:.3f});'); c.beat(tNormal)
c.rise("#col", tCarbon); c.pop("#nml", tNormal); c.out("#col", tOxy - 0.2)
c.j(f'tl.set("#sA .o2",{{opacity:0}},0);document.querySelectorAll("#sA .o2").forEach((o,i)=>tl.fromTo(o,{{x:0,y:0,opacity:0}},{{x:+o.dataset.x,y:+o.dataset.y,opacity:1,duration:0.8,ease:"power2.out",immediateRender:false}},{tOxy:.3f}+i*0.1));'); c.beat(tOxy)
c.pop("#mu", tMusc - 0.05); c.pop("#bri", tBrain - 0.05)
c.j(f'tl.to("#f2",{{opacity:0,duration:0.2}},{tTwo - 0.25:.3f});tl.to("#f3",{{opacity:1,duration:0.25}},{tTwo - 0.05:.3f});'); c.beat(tTwo)
c.j(f'gsap.set(["#rb1","#rb2"],{{svgOrigin:"60 0"}});tl.set(["#rb1","#rb2"],{{scaleX:0.02}},0);'
    f'tl.to("#rb1",{{scaleX:1,duration:{tImpr - tCirc + 0.4:.2f},ease:"power1.inOut"}},{tCirc - 0.2:.3f});tl.to("#rb2",{{scaleX:1,duration:{tDrop2 - tCough + 0.4:.2f},ease:"power1.inOut"}},{tCough - 0.2:.3f});')
c.rise("#r1l", tCirc - 0.1); c.rise("#r2l", tCough - 0.1)
c.beat(tLung); c.beat(tBreath)

# ---- B: cravings = receptors asking for a refill; waves pass
recs = "".join(f'<g transform="translate({120 + i * 140},330)"><g class="rcp"><path d="M0 0 V-60 M0 -60 L-24 -92 M0 -60 L24 -92" stroke="{GOLD}" stroke-width="14" stroke-linecap="round" fill="none"/></g></g>' for i, _ in enumerate(range(8)))
wave = "M0 0 " + " ".join(f"Q{60 + k * 240} {-(150 - k * 16)} {120 + k * 240} 0 T{240 + k * 240} 0" for k in range(9))
sB = (svg(f'<rect x="40" y="330" width="1120" height="40" rx="20" fill="{PINK}" stroke="{INK}" stroke-width="6"/>{recs}'
          f'<g transform="translate(0,620)"><g id="wv"><path d="{wave}" fill="none" stroke="{SKY}" stroke-width="14" stroke-linecap="round"/></g></g>')
      + f'<div id="nrl" class="lbl" style="left:60px;top:390px;font-size:44px;color:{GOLD}">NICOTINE RECEPTORS</div>'
      + f'<div id="rf" style="position:absolute;left:560px;top:60px;padding:16px 34px;border-radius:40px;background:{CREAM};border:6px solid {INK};font:64px InterBlack;color:{INK}">REFILL?</div>'
      + f'<div id="tn" class="chip" style="left:640px;top:390px;background:{GREEN};font-size:44px">TOTALLY NORMAL</div>'
      + f'<div id="ewp" class="stamp" style="left:220px;top:80px;font-size:76px;color:{SKY};border-color:{SKY}">EVERY WAVE PASSES</div>')
c.slide("sB", SB, T, sB)
c.pop("#nrl", tNic - 0.05, None); c.beat(tNic)
c.j(f'document.querySelectorAll("#sB .rcp").forEach((r,i)=>tl.fromTo(r,{{rotation:-12}},{{rotation:12,duration:0.18,yoyo:true,repeat:7,transformOrigin:"50% 100%",ease:"sine.inOut",immediateRender:false}},{tRec:.3f}+i*0.04));'); c.beat(tRec)
c.pop("#rf", tRefill - 0.1, "pop"); c.out("#rf", tThey - 0.2)
c.pop("#tn", tTot - 0.05)
c.j(f'tl.set("#wv",{{opacity:0}},0);tl.fromTo("#wv",{{x:-200,opacity:1}},{{x:-1400,duration:{T - tThey + 0.3:.2f},ease:"none",immediateRender:false}},{tThey - 0.1:.3f});'); c.beat(tWaves)
c.stamp("#ewp", tEvery - 0.05, r=-3)

c.build(cyto_js_kw=dict(points=[(tOk, 0.6), (tTwo - 0.1, 0.6), (tRefill - 0.1, 0.6)], tilts=[(tNormal, 0.5, 6), (tTot - 0.05, 0.6, -6)],
                        raises=[(tPasses, 0.6)], shrugs=[(tCrav, 0.6)],
                        expr=[(tDrop - 0.05, 0.6, "hype"), (tNormal - 0.05, 0.6, "hype"), (tCrav - 0.05, 0.8, "skeptic"), (tRefill - 0.05, 0.6, "squint"), (tPasses - 0.05, 0.6, "hype")]),
        cap_keys={"countdown": GOLD, "twenty": CORAL, "heart": "#ff8095", "twelve": GOLD, "carbon": CREAM, "monoxide": CREAM, "normal": GREEN, "oxygen": SKY,
                  "circulation": GREEN, "lung": GREEN, "coughing": SKY, "breathlessness": SKY, "cravings": CORAL, "refill": GOLD, "waves": SKY, "passes": SKY})
