"""LF01 ch6: Cyto's tips, 6ix edition. Five tip cards (icon each), helpline card, generic text-message UI, pharmacy cross,
trigger spots, Toronto ritual swaps (Bluffs / Kensington / 501), slips happen."""
from lf import *
import lfart as L

c = Ch(6); wt = c.wt; T = c.T
tSetup, tWill = wt("setup."), wt("willpower,")
t1 = wt("Tip"); t2 = wt("Tip", t1 + 1); t3 = wt("Tip", t2 + 1); t4 = wt("Tip", t3 + 1); t5 = wt("Tip", t4 + 1)
tSquad, tCoch, tTrials, tCouns, tOdds, tPct = wt("squad."), wt("Cochrane"), wt("trials"), wt("counselling"), wt("odds"), wt("forty-four")
tCall, tHelp, tFree, t247, tPhone, tIQ, tTell, tGroup, tRoom, tText, tHelpful, tDont = (wt("Call"), wt("Helpline,"), wt("free"), wt("24/7:"), wt("one,", 15),
    wt("iQuit"), wt("Tell"), wt("group"), wt("roommate."), wt("Text-message"), wt("helpful"), wt("Don't"))
tPharm, tTobs, tCigs, tHook, tCoch2, tPatch, tGum, tLoz, tBeats, tPresc, tVar, tSingle, tAny, tNo, tShame = (wt("pharmacist."), wt("tobacco's"), wt("cigs"), wt("hook."),
    wt("Cochrane", t2), wt("patch"), wt("gum"), wt("lozenge"), wt("beats"), wt("prescription"), wt("varenicline"), wt("single"), wt("Any"), wt("No", t2), wt("shame."))
tProm, tTrig, tSpots, tStudy, tYoung, tCann, tSmoke, tDrink, tNext, tSmall, tPatt, tRule, tLink, tPatio, tAfter, tPlan, tBring, tLeave, tLine, tNah, tGood = (
    wt("promised:"), wt("trigger", t3), wt("spots."), wt("study", t3), wt("young"), wt("cannabis,"), wt("smoke", t3), wt("drinking"), wt("next"), wt("Small"),
    wt("pattern,"), wt("rule."), wt("link-up,"), wt("patio,"), wt("after-party"), wt("plan"), wt("Bring"), wt("Leave"), wt("line"), wt('"nah,'), wt("good", t3))
tRepl, tRit, tCrav, tFew, tPass, tWalk, tBluffs, tKens, tFood, tRide, t501, tHead, tBeat, tWave = (wt("replace"), wt("ritual."), wt("craving"), wt("few"), wt("passes."),
    wt("Walk"), wt("Bluffs,"), wt("Kensington"), wt("food,"), wt("ride"), wt("501"), wt("headphones"), wt("Beat"), wt("wave."))
tSlips, tOneS, tRel, tReset, tClock, tKeep = wt("slips"), wt("One", t5), wt("relapse."), wt("Reset"), wt("clock"), wt("keep", t5)

# ---------------- backgrounds
c.bg("b0", 0, t2 - 0.15, L.bg_night("bn6", seed=17), kb=(1.0, 1.06))
c.bg("b1", t2 - 0.15, t4 - 0.15, L.bg_downtown("bd6"), kb=(1.06, 1.0))
c.bg("b2", t4 - 0.15, tKens - 0.2, L.bg_bluffs("bl6"), kb=(1.0, 1.08))
c.bg("b3", tKens - 0.2, tRide - 0.2, L.bg_kensington("kn6"), kb=(1.06, 1.0))
c.bg("b4", tRide - 0.2, t5 - 0.15, L.bg_queen("qn6"), kb=(1.0, 1.05))
c.bg("b5", t5 - 0.15, T, L.bg_night("bn7", seed=29), kb=(1.0, 1.06))
c.j(f'tl.fromTo("#qn6Tram",{{x:900}},{{x:-1300,duration:{t5 - tRide + 0.2:.2f},ease:"power1.out",immediateRender:false}},{tRide - 0.2:.3f});')


def header(n, idp, icon, title, col):
    return (f'<div id="{idp}" style="position:absolute;inset:0">' + svg(L.icon(icon, 300, 380, 1.6, idp + "I"))
            + f'<div class="lbl" style="left:540px;top:230px;font-size:64px;color:{col}">TIP {n}</div>'
            f'<div class="lbl" style="left:540px;top:320px;width:600px;white-space:normal;line-height:1.05;font-size:68px;color:{CREAM}">{title}</div></div>')


def tip_intro(idp, t_on, t_off):
    c.pop(f"#{idp}", t_on, "hit"); c.j(f'gsap.set("#{idp}I",{{svgOrigin:"300 380"}});tl.fromTo("#{idp}I",{{rotation:-10}},{{rotation:10,duration:0.3,yoyo:true,repeat:3,immediateRender:false}},{t_on + 0.3:.3f});')
    c.out(f"#{idp}", t_off)


# ---------------- intro: setup > willpower
s0 = (f'<div id="sw" class="big" style="left:0;width:{PW}px;top:200px;font-size:120px;color:{GOLD}">SETUP<br><span style="color:{CREAM};font-size:80px">BEATS WILLPOWER</span></div>')
c.slide("s0", 0, t1 - 0.15, s0)
c.stamp("#sw", tWill - 0.2, r=0, s="hit"); c.punch(tSetup)

# ---------------- TIP 1: get a squad
sq_a = (f'<div id="q1a" style="position:absolute;inset:0;opacity:0">'
        + f'<div id="tr3" class="chip" style="left:60px;top:90px;background:{CREAM};font-size:46px">300+ TRIALS</div>'
        + svg(f'<rect id="ob1" x="330" y="300" width="400" height="80" rx="16" fill="#5d6f84" stroke="{INK}" stroke-width="6"/>'
              f'<rect id="ob2" x="330" y="440" width="576" height="80" rx="16" fill="{GREEN}" stroke="{INK}" stroke-width="6"/>')
        + f'<div class="lbl" style="left:60px;top:315px;font-size:40px;color:{CREAM}">ON YOUR OWN</div>'
        + f'<div class="lbl" style="left:60px;top:455px;font-size:40px;color:{GREEN}">COUNSELLING</div>'
        + f'<div id="p44" class="stamp" style="left:700px;top:150px;font-size:70px;color:{GREEN};border-color:{GREEN}">+44% ODDS</div>'
        + src_card("cHB", "HARTMANN-BOYCE 2021", "Cochrane", BLUE, left=60, top=620, width=560) + '</div>')
sq_b = (f'<div id="q1b" style="position:absolute;left:150px;top:90px;width:900px;height:520px;border-radius:34px;background:{CREAM};border:8px solid {INK};opacity:0;text-align:center">'
        f'<div style="margin-top:34px;font:50px InterBlack;color:{CORAL}">SMOKERS\' HELPLINE</div>'
        f'<div style="margin-top:22px;font:96px InterBlack;color:{INK}">1-877-513-5333</div>'
        f'<div style="margin-top:22px;font:54px InterBlack;color:{BLUE}">TEXT iQuit TO 123456</div>'
        f'<div style="margin-top:26px;font:46px InterBlack;color:#1f7a45">FREE · 24/7</div></div>')
sq_c = (f'<div id="q1c" style="position:absolute;inset:0;opacity:0">' + L.phone_chat(90, 60, "pc")
        + f'<div id="gc" class="chip" style="left:560px;top:120px;background:{TEAL};font-size:46px">TELL YOUR GROUP CHAT</div>'
        + f'<div id="rm" class="chip" style="left:560px;top:230px;background:{PINK};font-size:46px">+ YOUR ROOMMATE</div>'
        + f'<div id="tsh" class="chip" style="left:560px;top:340px;background:{GREEN};font-size:44px">TEXT SUPPORT HELPS</div>'
        + f'<div id="dst" class="stamp" style="left:480px;top:500px;font-size:62px">DON\'T SOLO THIS</div></div>')
c.slide("s1", t1 - 0.15, t2 - 0.15, header(1, "h1", "squad", "GET A SQUAD", GOLD) + sq_a + sq_b + sq_c, title="TIP 1 · GET A SQUAD")
tip_intro("h1", t1 - 0.05, tCoch - 0.3)
c.j(f'tl.to("#q1a",{{opacity:1,duration:0.25}},{tCoch - 0.15:.3f});'); c.beat(tCoch)
c.pop("#tr3", tTrials - 0.1); c.slide_in("#cHB", tCoch + 0.2, s=None)
c.j(f'gsap.set(["#ob1","#ob2"],{{svgOrigin:"330 0"}});tl.set(["#ob1","#ob2"],{{scaleX:0}},0);tl.to("#ob1",{{scaleX:1,duration:0.5,ease:"power2.out"}},{tCouns - 0.3:.3f});tl.to("#ob2",{{scaleX:1,duration:0.8,ease:"back.out(1.4)"}},{tOdds - 0.1:.3f});')
c.beat(tCouns); c.beat(tOdds); c.stamp("#p44", tPct - 0.05, r=-4)
c.j(f'tl.to("#q1a",{{opacity:0,duration:0.2}},{tCall - 0.25:.3f});tl.fromTo("#q1b",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)",immediateRender:false}},{tCall - 0.05:.3f});')
c.beat(tCall); c.fx("hit", tCall)
for t in (tHelp, tFree, tPhone, tIQ):
    c.j(f'tl.to("#q1b",{{scale:1.04,duration:0.12,yoyo:true,repeat:1}},{t:.3f});'); c.beat(t)
c.fx("pop", tPhone); c.fx("pop", tIQ)
c.j(f'tl.to("#q1b",{{opacity:0,duration:0.2}},{tTell - 0.25:.3f});tl.to("#q1c",{{opacity:1,duration:0.25}},{tTell - 0.05:.3f});'); c.beat(tTell)
for k, t in enumerate((tTell + 0.1, tGroup + 0.3, tText, tHelpful)):
    c.pop(f"#pcB{k + 1}", t, "pop")
c.pop("#gc", tGroup - 0.05, None); c.pop("#rm", tRoom - 0.05, None); c.pop("#tsh", tText + 0.1, None)
c.stamp("#dst", tDont - 0.05, r=-4)

# ---------------- TIP 2: ask a pharmacist
ph_a = (f'<div id="q2a" style="position:absolute;inset:0;opacity:0">'
        + f'<div id="nh" class="chip" style="left:60px;top:90px;background:{GOLD};font-size:48px">NICOTINE\'S THE HOOK</div>'
        + svg(f'<g id="ip">{L.icon("patch", 170, 330, 1.0)}</g><g id="ig">{L.icon("gum", 430, 330, 1.0)}</g><g id="ix">{L.icon("rx", 170, 330, 1.0)}</g>')
        + f'<div id="pl" class="lbl" style="left:280px;top:290px;font-size:70px;color:{CREAM}">+</div>'
        + f'<div id="gt1" class="lbl" style="left:600px;top:280px;font-size:58px;color:{GREEN}">BEATS JUST ONE</div>'
        + f'<div id="lb1" class="lbl" style="left:60px;top:440px;font-size:38px;color:{CREAM}">PATCH + GUM OR LOZENGE</div>'
        + f'<div id="gt2" class="lbl" style="left:340px;top:280px;font-size:50px;color:{GREEN}">BEATS ONE FORM OF NRT</div>'
        + f'<div id="lb2" class="lbl" style="left:60px;top:440px;font-size:38px;color:{CREAM}">VARENICLINE (PRESCRIPTION)</div>'
        + src_card("cTh", "THEODOULOU 2023", "Cochrane", BLUE, left=60, top=620, width=480)
        + src_card("cLB", "LIVINGSTONE-BANKS 2023", "Cochrane", BLUE, left=560, top=620, width=600) + '</div>')
ph_b = (f'<div id="q2b" style="position:absolute;inset:0;opacity:0">' + svg(L.pharm_cross(600, 300, 1.4, "pcx"))
        + f'<div id="ap" class="chip" style="left:330px;top:500px;background:{CREAM};font-size:50px">ANY PHARMACY</div>'
        + f'<div id="ns" class="stamp" style="left:330px;top:470px;font-size:70px;color:{GREEN};border-color:{GREEN}">NO SHAME</div></div>')
c.slide("s2", t2 - 0.15, t3 - 0.15, header(2, "h2", "pharm", "ASK A PHARMACIST", GREEN) + ph_a + ph_b, title="TIP 2 · ASK A PHARMACIST")
tip_intro("h2", t2 - 0.05, tTobs - 0.3)
c.j(f'tl.to("#q2a",{{opacity:1,duration:0.25}},{tTobs - 0.15:.3f});tl.set(["#ix","#gt2","#lb2"],{{opacity:0}},0);'); c.beat(tTobs)
c.pop("#nh", tHook - 0.3)
c.pop("#ip", tPatch - 0.05); c.pop("#pl", tGum - 0.2, None); c.pop("#ig", tGum - 0.05, None); c.pop("#lb1", tLoz - 0.1, None)
c.pop("#gt1", tBeats - 0.05, "chime"); c.slide_in("#cTh", tCoch2 - 0.05, s=None)
c.j(f'tl.to(["#ip","#ig","#pl","#gt1","#lb1"],{{opacity:0,duration:0.2}},{tPresc - 0.25:.3f});'); c.beat(tPresc - 0.25)
c.pop("#ix", tPresc - 0.05); c.pop("#lb2", tVar - 0.05, None); c.pop("#gt2", tSingle - 0.1, "chime"); c.slide_in("#cLB", tVar + 0.2, s=None)
c.j(f'tl.to("#q2a",{{opacity:0,duration:0.2}},{tAny - 0.25:.3f});tl.to("#q2b",{{opacity:1,duration:0.25}},{tAny - 0.05:.3f});'); c.beat(tAny)
c.j('gsap.set("#pcx",{svgOrigin:"0 0"});'); c.j(f'tl.fromTo("#pcx",{{scale:.6}},{{scale:1,duration:0.4,ease:"back.out(2.4)",immediateRender:false}},{tAny:.3f});')
c.pop("#ap", tAny + 0.2, None); c.out("#ap", tNo - 0.2); c.stamp("#ns", tNo, r=-4)

# ---------------- TIP 3: trigger spots (the open loop)
tr_a = (f'<div id="q3a" style="position:absolute;inset:0;opacity:0">'
        + f'<div id="cd1" class="card" style="left:60px;top:100px;width:500px;border-left-color:{GREEN}"><h3 style="color:#1f7a45">CANNABIS DAYS</h3><p>far more likely to smoke too</p></div>'
        + f'<div id="cd2" class="card" style="left:640px;top:100px;width:500px;border-left-color:{GOLD}"><h3 style="color:#a8741a">DRINKING</h3><p>predicted smoking the next day</p></div>'
        + f'<div id="ptn" class="stamp" style="left:120px;top:360px;font-size:58px;color:{SKY};border-color:{SKY}">A PATTERN, NOT A RULE</div>'
        + src_card("cWa", "WALTERS 2023", "young adults, small study", SKY, left=60, top=620, width=560) + '</div>')
tr_b = (f'<div id="q3b" style="position:absolute;inset:0;opacity:0">'
        + "".join(f'<div id="tg{i}" class="chip" style="left:{[40, 370, 680][i]}px;top:100px;background:{col};font-size:42px">{lbl}</div>'
                  for i, (lbl, col) in enumerate((("THE LINK-UP", CORAL), ("THE PATIO", GOLD), ("THE AFTER-PARTY", PINK))))
        + f'<div id="pf" class="lbl" style="left:60px;top:230px;font-size:56px;color:{CREAM}">PLAN FOR IT:</div>'
        + f'<div id="bg1" class="chip" style="left:60px;top:330px;background:{GREEN};font-size:46px">✓ BRING GUM</div>'
        + f'<div id="le1" class="chip" style="left:420px;top:330px;background:{GREEN};font-size:46px">✓ LEAVE EARLY</div>'
        + f'<div id="nah" style="position:absolute;left:300px;top:470px;padding:20px 40px;border-radius:44px;background:{CREAM};border:7px solid {INK};font:58px InterBlack;color:{INK}">"NAH, I\'M GOOD TONIGHT."</div></div>')
c.slide("s3", t3 - 0.15, t4 - 0.15, header(3, "h3", "pin", "KNOW YOUR TRIGGER SPOTS", CORAL) + tr_a + tr_b, title="TIP 3 · TRIGGER SPOTS")
tip_intro("h3", t3 - 0.05, tStudy - 0.3)
c.j(f'tl.to("#q3a",{{opacity:1,duration:0.25}},{tStudy - 0.15:.3f});'); c.beat(tStudy)
c.slide_in("#cWa", tYoung - 0.1, s=None); c.slide_in("#cd1", tCann - 0.1); c.slide_in("#cd2", tDrink - 0.1)
c.stamp("#ptn", tPatt - 0.05, r=-3)
c.j(f'tl.to("#q3a",{{opacity:0,duration:0.2}},{tLink - 0.3:.3f});tl.to("#q3b",{{opacity:1,duration:0.25}},{tLink - 0.1:.3f});'); c.beat(tLink - 0.1)
for i, t in enumerate((tLink, tPatio, tAfter)): c.pop(f"#tg{i}", t - 0.05)
c.rise("#pf", tPlan - 0.05); c.pop("#bg1", tBring - 0.05); c.pop("#le1", tLeave - 0.05); c.pop("#nah", tNah - 0.1, "chime")

# ---------------- TIP 4: replace the ritual (Toronto swaps)
rt = (f'<div id="q4a" style="position:absolute;inset:0;opacity:0">'
      + svg(f'<g transform="translate(0,420)"><g id="cw"><path d="M60 0 C200 -260 300 -260 420 0 S640 120 760 0 S980 -40 1140 0" fill="none" stroke="{CORAL}" stroke-width="16" stroke-linecap="round" {DRAW}/></g></g>')
      + f'<div id="fm" class="chip" style="left:150px;top:520px;background:{GOLD};font-size:46px">A CRAVING: A FEW MINUTES</div>'
      + f'<div id="itp" class="chip" style="left:640px;top:300px;background:{GREEN};font-size:46px">THEN IT PASSES</div></div>')
c.slide("s4", t4 - 0.15, tWalk - 0.15, header(4, "h4", "shoe", "REPLACE THE RITUAL", BLUE) + rt, title="TIP 4 · REPLACE THE RITUAL")
tip_intro("h4", t4 - 0.05, tCrav - 0.3)
c.j(f'tl.to("#q4a",{{opacity:1,duration:0.25}},{tCrav - 0.15:.3f});'); c.beat(tCrav)
c.j(f'tl.fromTo("#cw path",{{strokeDashoffset:100}},{{strokeDashoffset:0,duration:{tPass - tCrav + 0.3:.2f},ease:"none",immediateRender:false}},{tCrav:.3f});')
c.pop("#fm", tFew - 0.1); c.pop("#itp", tPass - 0.1)
SW = [("WALK THE BLUFFS", tWalk - 0.15, tKens - 0.2, GREEN), ("HIT KENSINGTON FOR FOOD", tKens - 0.2, tRide - 0.2, GOLD), ("RIDE THE 501, HEADPHONES ON", tRide - 0.2, t5 - 0.15, CORAL)]
for i, (lbl, a, b, col) in enumerate(SW):
    inner = f'<div id="rw{i}" class="chip" style="left:{[260, 150, 110][i]}px;top:60px;background:{col};font-size:58px">{lbl}</div>'
    if i == 2: inner += f'<div id="btw" class="stamp" style="left:230px;top:250px;font-size:80px;color:{SKY};border-color:{SKY}">BEAT THE WAVE</div>'
    c.slide(f"s4{i}", a, b, inner, panel=False)
    c.pop(f"#rw{i}", a + 0.15, None)
c.stamp("#btw", tBeat - 0.05, r=-4)

# ---------------- TIP 5: slips happen
s5 = (svg(L.clock(300, 380, 210, "rk", "RESET"))
      + f'<div id="osr" class="stamp" style="left:470px;top:120px;font-size:56px">1 SLIP ≠ RELAPSE</div>'
      + f'<div id="kgo" class="chip" style="left:640px;top:420px;background:{GREEN};font-size:56px">KEEP GOING</div>')
c.slide("s5", t5 - 0.15, T, header(5, "h5", "reset", "SLIPS HAPPEN", GREEN) + f'<div id="q5" style="position:absolute;inset:0;opacity:0">{s5}</div>', title="TIP 5 · SLIPS HAPPEN")
tip_intro("h5", t5 - 0.05, tOneS - 0.3)
c.j(f'tl.to("#q5",{{opacity:1,duration:0.25}},{tOneS - 0.15:.3f});'); c.beat(tOneS)
c.stamp("#osr", tRel - 0.3, r=-3)
c.j(f'gsap.set("#rkHand",{{svgOrigin:"300 380"}});tl.fromTo("#rkHand",{{rotation:250}},{{rotation:-360,duration:0.9,ease:"power3.inOut",immediateRender:false}},{tReset:.3f});'
    f'tl.fromTo("#rkArc",{{strokeDashoffset:70}},{{strokeDashoffset:0,duration:0.9,ease:"power3.inOut",immediateRender:false}},{tReset:.3f});'); c.beat(tReset); c.fx("whoosh", tReset)
c.pop("#kgo", tKeep - 0.05, "chime")

c.build(cyto_js_kw=dict(
    points=[(tSquad - 0.1, 0.6), (tCall - 0.1, 0.7), (tPharm - 0.1, 0.6), (tPresc - 0.1, 0.6), (tSpots - 0.1, 0.6), (tLink - 0.1, 0.6), (tWalk - 0.1, 0.6), (tReset - 0.1, 0.6)],
    waves=[tNah - 0.1], raises=[(tSetup, 0.6), (tShame, 0.6), (tWave, 0.6), (tKeep, 0.6)],
    tilts=[(tWill, 0.5, -6), (tRoom, 0.5, 6), (tHook, 0.5, -6), (tRule, 0.5, 6), (tFood, 0.5, -6), (tRel, 0.5, 6)], shrugs=[(tSmall, 0.6), (tSlips, 0.6)],
    expr=[(tWill - 0.05, 0.6, "skeptic"), (tSetup - 0.05, 0.6, "hype"), (tSquad - 0.05, 0.6, "hype"), (tPct - 0.05, 0.7, "shock"), (tFree - 0.05, 0.6, "hype"),
          (tDont - 0.05, 0.6, "squint"), (tHook - 0.05, 0.6, "squint"), (tShame - 0.05, 0.6, "hype"), (tProm - 0.05, 0.6, "squint"), (tSmall - 0.05, 0.7, "skeptic"),
          (tNah - 0.05, 0.9, "hype"), (tPass - 0.05, 0.6, "hype"), (tBluffs - 0.05, 0.6, "hype"), (tWave - 0.05, 0.6, "hype"), (tRel - 0.05, 0.7, "squint"), (tKeep - 0.05, 0.6, "hype")],
    looks=[(tCoch, 6, -5)]), extra_css=L.PHONE_CSS,
    cap_keys={"setup": GOLD, "willpower": CORAL, "squad": GOLD, "300": CREAM, "44%": GREEN, "helpline": CORAL, "free": GREEN, "247": GREEN,
              "18775135333": GOLD, "iquit": SKY, "123456": SKY, "pharmacist": GREEN, "nicotines": GOLD, "patch": CREAM, "varenicline": SKY, "shame": GREEN,
              "trigger": CORAL, "spots": CORAL, "cannabis": GREEN, "drinking": GOLD, "pattern": SKY, "gum": GREEN, "early": GREEN, "ritual": BLUE,
              "bluffs": GREEN, "kensington": GOLD, "501": CORAL, "wave": SKY, "slips": GREEN, "relapse": CORAL, "clock": GREEN, "going": GREEN})
