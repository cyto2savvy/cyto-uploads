"""EP08 — Why you wake up at 3am (6ix Seconds of Science). v2 layout + v3 rig + art.py set pieces.
python3 build.py -> index.html + assets/audio.wav"""
import json, sys, os, subprocess, math
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import numpy as np
import cytohf as C, cyto3 as R, art as A
from engine import tone, noise, hp, lp, add, load_mono, SR

P = "/home/claude/hf/ep08"; os.chdir(P)
V = "/home/claude/ep8"
TM = json.load(open(f"{V}/timing.json")); WORDS = TM["words"]
T = 30.5
C1, C2, C3, C4, C5, C6, C7, C8 = 3.24, 6.95, 16.02, 20.0, 23.43, 24.95, 28.3, 30.22


def wt(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and w["w"].lower().strip(".,?!:").startswith(word.lower()):
            return round(w["t0"], 3)
    raise KeyError(word)


# ------------------------------------------------------------------ assets
C.copy_assets_v2(P, lotties=["zzz-a.json", "siren.json"])
for f in ("outfit_pj.png", "acc_sleepmask.png"):
    subprocess.run(["cp", f"/home/claude/cyto2/rig/{f}", "assets/"])

# ------------------------------------------------------------------ audio: lo-fi night beat + SFX, ducked under the voice
def rhodes(m, dur):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.02) * np.exp(-t / 1.4)
    trem = 1 + 0.18 * np.sin(2 * np.pi * 4.2 * t)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t / .3)) * env * trem * 0.06


def make_audio(sfx_events):
    n = int((T + 0.3) * SR); music = np.zeros(n, np.float32); drums = np.zeros(n, np.float32)
    BEAT = 60 / 90; BAR = BEAT * 4
    chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]   # Fmaj7 Em7 Dm7 Cmaj7
    t = 0.0; i = 0
    while t < T + 0.3:
        for k, m in enumerate(chords[i % 4]): add(music, rhodes(m, BAR + 0.4), t + k * 0.012)
        add(music, rhodes(chords[i % 4][0] - 12, BAR) * 1.4, t)
        t += BAR; i += 1
    kick = tone(120, 45, 0.35, 0.12) * 0.9
    snare = lp(hp(noise(0.18, 1)), 0.5) * np.exp(-np.arange(int(0.18 * SR)) / SR / 0.05) * 0.38
    hat = hp(noise(0.04, 2), 0.6) * np.exp(-np.arange(int(0.04 * SR)) / SR / 0.01) * 0.16
    t = C1; s = 0
    while t < T + 0.3:
        quiet = C6 - 0.1 <= t < C7 - 0.05
        if not quiet:
            p = s % 8
            if p in (0, 3, 5): add(drums, kick, t)
            if p in (2, 6): add(drums, snare, t)
            add(drums, hat, t + (0.06 if s % 2 else 0), 0.9 if s % 2 == 0 else 0.55)
        t += BEAT / 2; s += 1
    crackle = np.zeros(n, np.float32); rnd = np.random.default_rng(7)
    for p in rnd.integers(0, n - 200, 900): crackle[p:p + 60] += rnd.uniform(-1, 1) * np.exp(-np.arange(60) / 10) * 0.05
    music = lp(music, 0.35) + crackle * 0.6
    music[: int(C1 * SR)] = lp(music[: int(C1 * SR)], 0.08) * 1.8          # muffled until the drop
    a, b = int((C6 - 0.1) * SR), int((C7 - 0.05) * SR); music[a:b] = lp(music[a:b], 0.12) * 1.5   # serious bit: soft
    music += drums
    v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.55 * np.clip(env * 3, 0, 1)); music *= 0.42
    S = {
        "whoosh": lp(noise(0.4, 3), 0.25) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))) ** 2 * 0.45,
        "boom": tone(90, 35, 0.9, 0.35) * 0.8,
        "pop": tone(1200, 380, 0.08, 0.03) * 0.3,
        "ding": (tone(1760, 1760, 0.6, 0.18) + 0.5 * tone(2640, 2640, 0.6, 0.12)) * 0.2,
        "buzz": np.concatenate([np.sign(np.sin(2 * np.pi * 170 * np.arange(int(.32 * SR)) / SR)) * 0.07, np.zeros(int(.12 * SR)),
                                np.sign(np.sin(2 * np.pi * 170 * np.arange(int(.32 * SR)) / SR)) * 0.07]),
        "crunch": np.round(noise(0.35, 6) * 3) / 3 * 0.13 * np.linspace(1, 0, int(0.35 * SR)),
        "hiss": hp(noise(0.7, 9), 0.7) * np.exp(-np.arange(int(0.7 * SR)) / SR / 0.25) * 0.22,
        "woop": np.sin(2 * np.pi * np.cumsum(np.linspace(650, 980, int(0.5 * SR))) / SR) * np.sin(np.linspace(0, np.pi, int(0.5 * SR))) * 0.07,
        "click": tone(2200, 900, 0.05, 0.015) * 0.35,
        "rewind": np.sin(2 * np.pi * np.cumsum(np.linspace(1400, 300, int(0.45 * SR))) / SR) * np.linspace(.6, 0, int(0.45 * SR)) * 0.08,
    }
    sfx = np.zeros(n, np.float32)
    for kind, tt in sfx_events: add(sfx, S[kind], tt)
    mix = music + sfx; mix[:m] += v[:m]
    mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[: int(T * SR)]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/raw_mix.wav"],
                   input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/raw_mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "assets/base.wav"], check=True)


# ------------------------------------------------------------------ word beats
tBro, tWhy, tAlarm = wt("Bro"), wt("why"), wt("alarm")
tYo, tCyto, tLive, t6ix, tInside = wt("Yo"), wt("Cyto"), wt("live"), wt("6ix"), wt("inside")
t90, tDeep, t3am, tLight, tDreamy, tEasy, tWake = wt("90"), wt("deep"), wt("3AM", 9), wt("light"), wt("dreamy"), wt("Easy"), wt("wake", 12)
tCort, tClimb, tMorning = wt("cortisol"), wt("climbing"), wt("morning")
tStress, tCity, tHall, tHigh, tAlert, tDream, tBreaks = wt("Stressed"), wt("City"), wt("Hall"), wt("high"), wt("alert"), wt("dream", 18), wt("breaks")
tClocks, tFell, t3, tPhone, t4, tBody2 = wt("clocks"), wt("fell"), wt("3", 21), wt("phone"), wt("4"), wt("body", 22.5)
tBlue, tBus, tAhlie = wt("Blue"), wt("bus"), wt("ahlie")
tEvery, tWrecked, tTalk, tDoctor, tNot = wt("Every"), wt("wrecked"), wt("Talk"), wt("doctor"), wt("Not")
tLike, tSub, tOut = wt("Like"), wt("subscribe"), wt("out")

SFX = [("buzz", 0.0), ("boom", tBro), ("buzz", tAlarm - 0.1), ("pop", tAlarm + 0.1),
       ("boom", C1), ("pop", tLive), ("boom", t6ix), ("pop", tInside),
       ("pop", t90), ("pop", tDeep), ("ding", t3am), ("pop", tLight), ("pop", tEasy + 0.3), ("pop", tCort), ("ding", tMorning),
       ("pop", tCity), ("pop", tHall), ("boom", tHigh), ("woop", tHigh), ("woop", tHigh + 0.55), ("pop", tDream), ("crunch", tBreaks),
       ("rewind", tFell - 0.1), ("pop", t3), ("ding", t4), ("hiss", C5 + 0.55), ("pop", tBlue), ("boom", tAhlie),
       ("pop", tEvery), ("pop", tWrecked), ("pop", tDoctor), ("pop", tNot), ("pop", tLike), ("click", tSub + 0.15)]
SFX += [("whoosh", c - 0.18) for c in (C2, C3, C4, C5, C6, C7)]
make_audio(SFX)

# ------------------------------------------------------------------ Cyto: positions, acting
POS_HOOK, POS_BIG, POS_V2 = C.place(330, 1335, 0.60), C.place(540, 1300, 0.66), C.CYTO_V2
SIPS = [(29.72, 0.8)]
mouth = R.viseme_track(f"{V}/voice.wav", WORDS)
if mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
blinks = [(t, 0.1) for t in (4.0, 6.4, 9.3, 12.0, 14.8, 17.2, 21.9, 24.2, 26.8, 28.9)]
gest = dict(sips=SIPS, raises=[(tCyto, 0.6), (tAhlie, 0.7)], waves=[tYo, tOut - 0.2],
            points=[(tCort, 0.9), (t4 - 0.05, 0.9)], tilts=[(tWake, 0.6, 7), (tFell, 0.6, -6), (tAhlie, 0.6, 8)],
            shrugs=[(tStress, 0.5)])
expr = [(tWhy - 0.04, 1.3, "shock"), (tCyto - 0.05, 0.5, "hype"), (t6ix, 0.5, "hype"),
        (tDreamy, 0.7, "squint"), (tMorning - 0.05, 0.45, "hype"),
        (tStress, 0.6, "skeptic"), (tHigh - 0.05, 0.8, "shock"), (tBreaks - 0.05, 0.6, "squint"),
        (t3 - 0.05, 0.7, "skeptic"), (t4 - 0.05, 0.6, "shock"), (tAhlie - 0.05, 0.5, "hype"),
        (C6 + 0.1, 3.0, "sad")]
looks = [(C2 + 0.25, 12, -16), (tCort + 0.1, 14, -18), (C3 + 0.2, 10, -16), (tDream, 6, -20), (C4 + 0.2, 14, -12),
         (C5 + 0.4, 12, -6), (C6 + 0.3, 6, -10), (C7 + 0.1, 0, 0)]
rig_js = R.rig3_js(mouth, T, blinks=blinks, mute=[(s[0], 0) for s in SIPS], expr=expr, looks=looks, **gest)
R.mix_sips("assets/base.wav", [s[0] for s in SIPS], "assets/audio.wav")

# ------------------------------------------------------------------ captions + transitions
KEYS = {"3am": "#FFD166", "3am,": "#FFD166", "90minute": "#4f86ff", "deep": "#4f86ff", "light": "#cfe0ff", "dreamy": "#c4b0ff",
        "cortisol": "#FF7A59", "morning": "#FFD166", "stressed": "#FF7A59", "city": "#FFD166", "hall": "#FFD166", "alert": "#FF7A59",
        "dream": "#c4b0ff", "3": "#FFD166", "4": "#FFD166", "blue": "#4f86ff", "doctor": "#3fc1b0", "subscribe": "#FF7A59", "6ix": "#FFD166"}
CAPW = [w for w in WORDS if not (tLive - 0.01 <= w["t0"] < C2)]
cap_html, cap_js = C.captions(CAPW, KEYS, y=C.CAP_Y_V2)
cap_js += f'\ntl.set("#cap{cap_html.count(chr(34)+"cap clip"+chr(34)) - 1}",{{opacity:0}},{C8});'
TRS = [C.transition(k, t) for k, t in (("zoom", C1), ("membrane", C2), ("whip", C3), ("doors", C4), ("whip", C5), ("membrane", C6), ("whip", C7))]
tr_html = "\n".join(h for h, _ in TRS); tr_js = "\n".join(j for _, j in TRS)

# ------------------------------------------------------------------ art
W, H = 1080, 1920
hy_svg, HY = A.hypnogram(150, 150, 680, 330)
x3 = HY["x_of"](3.85); y3 = HY["y_of"](2); xw = HY["x_of"](4.02); yw = HY["y_of"](0)


def cloud(cx, cy, s=1.0):
    return (f'<g id="dreamB"><path d="M{cx - 220 * s:.0f} {cy + 60 * s:.0f} Q{cx - 280 * s:.0f} {cy - 20 * s:.0f} {cx - 190 * s:.0f} {cy - 60 * s:.0f} '
            f'Q{cx - 160 * s:.0f} {cy - 150 * s:.0f} {cx - 50 * s:.0f} {cy - 120 * s:.0f} Q{cx + 20 * s:.0f} {cy - 190 * s:.0f} {cx + 110 * s:.0f} {cy - 120 * s:.0f} '
            f'Q{cx + 230 * s:.0f} {cy - 140 * s:.0f} {cx + 220 * s:.0f} {cy - 30 * s:.0f} Q{cx + 290 * s:.0f} {cy + 40 * s:.0f} {cx + 200 * s:.0f} {cy + 80 * s:.0f} Z" '
            f'fill="#c4b0ff" stroke="{A.INK}" stroke-width="9"/>'
            f'<text x="{cx}" y="{cy + 10 * s:.0f}" text-anchor="middle" font-family="InterBlack" font-size="{56 * s:.0f}" fill="{A.INK}">DREAM SLEEP</text>'
            f'<path d="M{cx - 150 * s:.0f} {cy - 60 * s:.0f} l8 16 18 3 -13 12 3 18 -16 -9 -16 9 3 -18 -13 -12 18 -3Z" fill="#FFD166" stroke="{A.INK}" stroke-width="4"/>'
            f'<g id="crack" opacity="0"><path d="M{cx - 20 * s:.0f} {cy - 140 * s:.0f} l30 60 -40 40 50 50 -20 60" fill="none" stroke="{A.INK}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M{cx + 10 * s:.0f} {cy - 40 * s:.0f} l70 -20 40 30" fill="none" stroke="{A.INK}" stroke-width="8"/></g></g>')


def chip(id_, text, left, top, bg="#FFD166", fg=A.INK, size=34, extra=""):
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;background:{bg};color:{fg};font:{size}px InterBlack;'
            f'letter-spacing:.03em;padding:10px 22px;border-radius:30px;border:5px solid {A.INK};box-shadow:0 6px 0 {A.INK};white-space:nowrap;opacity:0;{extra}">{text}</div>')


GLOBAL_DEFS = f'<svg width="0" height="0" style="position:absolute"><defs>{A.PHONE_DEFS}</defs></svg>'
sky = lambda seed, n=45: A.stars(W, H, n, seed, .5)

S1 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 28%, #16295a 0%, #070d17 62%)"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{sky(11, 30)}
 <g id="ph1w">{A.phone(360, 210, 360, 655, idp="ph1")}</g></svg>
<div id="zzz" style="position:absolute;left:560px;top:930px;width:230px;height:230px;filter:brightness(2.2) sepia(.3)"></div>'''

S2 = f'''<div class="bgfill" style="background:linear-gradient(#0f2236,#22487a 70%,#2d5a8f)"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{sky(5, 60)}{A.moon(190, 730, 50, "#1d3d66")}
 <g id="sky2">{A.skyline(W, H, 1500, .95, seed=4, lit=.32, cn=780)}</g></svg>
<div id="t2a" class="big" style="top:250px;font-size:74px;color:#FAF4E8">LIVE FROM</div>
<div id="t2b" class="big" style="top:330px;font-size:210px;color:#FFD166">THE 6IX</div>
{chip("t2c", "...INSIDE YOUR BODY", 270, 590, bg="#FF7A59", size=40)}'''

S3 = f'''<div class="navy"></div><div id="dots3" class="dots"></div>
<div id="pn3" class="panel"><div class="ptitle">ONE NIGHT OF SLEEP</div>
 <svg width="880" height="650" style="position:absolute;left:0;top:0;overflow:visible">
  <g id="hyAll">{hy_svg}
  <g id="brk" opacity="0"><path d="M{HY["x_of"](0):.0f} 140 V124 H{HY["x_of"](1.5):.0f} V140" fill="none" stroke="#4f86ff" stroke-width="6"/></g>
  <path id="m3" d="M{HY["x_of"](3.85):.0f} 140 V490" stroke="#FFD166" stroke-width="6" stroke-dasharray="14 10" opacity="0"/>
  <circle id="dot3" cx="{x3:.0f}" cy="{y3:.0f}" r="20" fill="#FFD166" stroke="{A.INK}" stroke-width="6" opacity="0"/>
  <g id="sun" opacity="0"><circle cx="{HY["x_of"](8):.0f}" cy="112" r="30" fill="#FFD166" stroke="{A.INK}" stroke-width="5"/>
   {"".join(f'<path d="M{HY["x_of"](8) + math.cos(math.radians(a)) * 42:.0f} {112 + math.sin(math.radians(a)) * 42:.0f} L{HY["x_of"](8) + math.cos(math.radians(a)) * 58:.0f} {112 + math.sin(math.radians(a)) * 58:.0f}" stroke="#FFD166" stroke-width="7" stroke-linecap="round"/>' for a in range(0, 360, 45))}</g>
  </g></svg>
 {chip("c90", "90 MIN", 205, 70, bg="#4f86ff", fg="#fff", size=30)}
 {chip("cDeep", "DEEP = EARLY", 175, 560, bg="#4f86ff", fg="#fff", size=28)}
 {chip("c3am", "3AM", int(x3) - 52, 74, size=30)}
 {chip("cLight", "LIGHT + DREAMY", int(x3) - 150, int(y3) + 38, bg="#cfe0ff", size=28)}
 {chip("cWake", "EASY TO WAKE!", int(xw) + 34, 120, bg="#FF7A59", size=28)}
 {chip("cCort", "CORTISOL ↑ WAKE-UP HORMONE", 330, 560, bg="#FF7A59", size=28)}
</div>
<div id="cd3a" class="card"><h3>BUCKLEY 2005</h3><p>Deep sleep comes early. Later cycles run lighter.</p></div>
<div id="cd3b" class="card" style="opacity:0"><h3>CORTISOL RHYTHM</h3><p>It starts rising in the 2nd half of the night.</p></div>'''

S4 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 30%, #1b3257 0%, #0a1322 70%)"></div>
<div id="red4" class="bgfill" style="background:radial-gradient(ellipse at 60% 25%, rgba(255,59,59,.55) 0%, rgba(255,59,59,0) 60%);opacity:0"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">{sky(8, 45)}{A.moon(900, 330, 50, "#14284a")}
 <g id="ch">{A.city_hall(600, 830, 0.95)}</g>
 <rect x="-20" y="860" width="1120" height="1100" fill="#0a1322"/>
 <g id="cloudW" transform="translate(0,0)">{cloud(560, 640, 0.95)}</g></svg>
<div id="sir" style="position:absolute;left:650px;top:150px;width:150px;height:150px;opacity:0"></div>
<div id="t4a" class="big" style="top:245px;left:70px;width:auto;text-align:left;font-size:96px;color:#FFD166">CITY HALL</div>
<div id="t4b" class="big" style="top:345px;left:74px;width:auto;text-align:left;font-size:54px;color:#FAF4E8">= YOUR BRAIN</div>
<div id="cd4" class="card"><h3>RIEMANN 2024</h3><p>Stress makes dream sleep the easiest to break.</p></div>'''

S5 = f'''<div class="navy"></div><div id="dots5" class="dots"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">
 <g id="ph5w">{A.phone(120, 300, 300, 545, time="4:00", day="SUNDAY", note=False, idp="ph5")}
  <text id="ph5T3" x="270" y="505" text-anchor="middle" font-family="InterBlack" font-size="134" fill="#fff" letter-spacing="-4" opacity="0">3:00</text></g>
 <g id="bc5w">{A.body_clock(725, 560, 195)}</g></svg>
{chip("l5a", "YOUR PHONE", 120, 210, bg="#cfe0ff", size=32)}
{chip("l5b", "YOUR BODY", 600, 245, bg="#3fc1b0", size=32)}
{chip("rw5", "⟲ −1 HOUR", 330, 640, bg="#FF7A59", size=36)}
{chip("f5", "FEELS LIKE 4:00", 560, 790, bg="#FFD166", size=32)}'''

S6 = f'''<div class="bgfill" style="background:linear-gradient(#11263f,#0c1622 70%)"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{A.skyline(W, H, 800, .72, seed=12, lit=.3, cn=860)}</svg>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">
 <rect x="-20" y="795" width="1120" height="64" fill="#1b2733"/><path d="M0 827 H1080" stroke="#FFD166" stroke-width="6" stroke-dasharray="40 30"/>
 <g id="busW">{A.night_bus(230, 525, 0.95)}</g></svg>
{chip("b6", "BLUE NIGHT HOURS", 80, 235, bg="#4f86ff", fg="#fff", size=46)}'''

S7 = f'''<div class="bgfill" style="background:linear-gradient(#152a44,#0c1622 75%)"></div>
<div class="panel" id="pn7" style="background:#12263c"><div class="ptitle">REAL TALK</div>
 <div id="r7a" class="row"><span class="ic" style="background:#c4b0ff">☾</span>UP AT 3AM EVERY NIGHT?</div>
 <div id="r7b" class="row" style="top:250px"><span class="ic" style="background:#FF7A59">!</span>WRECKED ALL DAY?</div>
 <div id="r7c" class="row" style="top:400px;font-size:60px;color:#3fc1b0"><span class="ic" style="background:#3fc1b0;color:#0c1622">+</span>TALK TO A DOCTOR</div>
</div>
<div id="cd7" class="card" style="border-left-color:#3fc1b0"><h3 style="color:#188076">HEADS UP</h3><p>Not medical advice.</p></div>'''

S8 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 30%, #1d3a66 0%, #0c1622 70%)"></div>
<div id="pn8" class="panel">
 <div id="sub8" style="position:absolute;left:150px;top:70px;width:580px;height:140px;border-radius:70px;background:#FF7A59;border:7px solid #0c1622;box-shadow:0 10px 0 #0c1622;
   font:64px InterBlack;color:#0c1622;text-align:center;line-height:126px">SUBSCRIBE</div>
 <div id="subd8" style="position:absolute;left:150px;top:70px;width:580px;height:140px;border-radius:70px;background:#3a4a5e;border:7px solid #0c1622;box-shadow:0 10px 0 #0c1622;
   font:60px InterBlack;color:#FAF4E8;text-align:center;line-height:126px;opacity:0">SUBSCRIBED ✓</div>
 <div id="like8" style="position:absolute;left:740px;top:70px;font:110px InterBlack;color:#FFD166;opacity:0">👍</div>
 <div style="position:absolute;left:40px;top:270px;font:30px InterBlack;color:#FFD166;letter-spacing:.05em">SOURCES</div>
 <div id="src8" style="position:absolute;left:40px;top:320px;width:800px;font:25px/1.45 InterSB;color:#cfe0ff">
  Buckley &amp; Schatzberg 2005 · J Clin Endocrinol Metab<br>Liyanarachchi et al. 2017 · Best Pract Res Clin Endocrinol Metab<br>Riemann et al. 2024 · J Sleep Res<br>
  <span style="color:#96b0c4">Links in the description · Not medical advice</span></div>
</div>'''

S9 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 28%, #16295a 0%, #070d17 62%)"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{sky(11, 30)}{A.phone(360, 210, 360, 655, note=False, idp="ph9")}</svg>'''

scenes = [("s1", 0, C1, S1), ("s2", C1, C2, S2), ("s3", C2, C3, S3), ("s4", C3, C4, S4), ("s5", C4, C5, S5),
          ("s6", C5, C6, S6), ("s7", C6, C7, S7), ("s8", C7, C8, S8), ("s9", C8, T, S9)]
scene_html = "\n".join(f'<div id="{i}" class="scene clip" data-start="{a}" data-duration="{round(b - a, 3)}">{h}</div>' for i, a, b, h in scenes)

# ------------------------------------------------------------------ timeline (scene beats)
J = []
def j(s): J.append(s)
# camera: slow push every scene, punches on hooks/punchlines
for _, a, b, _h in scenes:
    j(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.045,duration:{b - a - 0.05:.3f},ease:"none",immediateRender:false}},{a + 0.01:.3f});')
j('const punch=(t,s=1.08)=>{tl.to("#shaker",{scale:s,duration:0.08,ease:"power2.out"},t);tl.to("#shaker",{scale:1,duration:0.3,ease:"power2.inOut"},t+0.08);};')
j('const shake=(t,d=0.5,a=14)=>{tl.fromTo("#shaker",{x:-a},{x:a,duration:0.05,repeat:Math.round(d/0.05),yoyo:true,ease:"none",immediateRender:false},t);tl.to("#shaker",{x:0,duration:0.05},t+d);};')
for t in (tBro, tAlarm, t6ix, t3am, tHigh, t4, tAhlie): j(f"punch({t});")
for t, d in ((tAlarm, 0.45), (tHigh, 0.7), (tBreaks, 0.3)): j(f"shake({t},{d});")
j('tl.set("#shaker",{x:0,y:0,scale:1},0);')
for b, a, d in (("#dots3", C2, C3 - C2), ("#dots5", C4, C5 - C4)):
    j(f'tl.fromTo("{b}",{{x:0,y:0}},{{x:70,y:140,duration:{d:.3f},ease:"none"}},{a});')
# Cyto positions per scene (moves hidden under the transitions)
for t, pos in ((0, POS_HOOK), (C1, POS_BIG), (C2, POS_V2), (C7, POS_HOOK)):
    j(f'tl.set("#cytoPos",{json.dumps(pos)},{t});')
j(f'tl.set("#cytoPos",{json.dumps(POS_HOOK)},{T - 0.01});')
# --- S1 hook: phone lit on frame 1 (loop), buzzing; Cyto asleep -> shock
j('tl.set(["#eyeL","#eyeR"],{opacity:0},0);tl.set(["#ecL","#ecR"],{opacity:1},0);')
j(f'tl.set(["#eyeL","#eyeR"],{{opacity:1}},{tWhy - 0.06});tl.set(["#ecL","#ecR"],{{opacity:0}},{tWhy - 0.06});')
j(f'tl.fromTo("#ph1w",{{x:-7}},{{x:7,duration:0.045,repeat:12,yoyo:true,ease:"none"}},0);tl.set("#ph1w",{{x:0}},0.6);')
j(f'tl.fromTo("#ph1w",{{x:-7}},{{x:7,duration:0.045,repeat:12,yoyo:true,ease:"none",immediateRender:false}},{tAlarm - 0.1});tl.set("#ph1w",{{x:0}},{tAlarm + 0.5});')
j(f'tl.fromTo("#ph1Glow",{{opacity:.95}},{{opacity:.45,duration:0.6,repeat:4,yoyo:true,ease:"sine.inOut"}},0);')
j(f'tl.fromTo("#ph1Note",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{tAlarm + 0.1});')
j(f'tl.fromTo("#ph1w",{{scale:1}},{{scale:1.06,duration:{C1},ease:"none",svgOrigin:"540 540"}},0);')
j('const Lz=lottie.loadAnimation({container:document.getElementById("zzz"),renderer:"svg",loop:false,autoplay:false,animationData:' + open(f"{P}/assets/zzz-a.json").read() + '});'
  f'const Pz={{f:70}};tl.fromTo(Pz,{{f:70}},{{f:70+{tWhy * 50:.0f},duration:{tWhy},ease:"none",onUpdate:()=>Lz.goToAndStop(Pz.f%Lz.totalFrames,true)}},0);')
j(f'tl.to("#zzz",{{opacity:0,y:-60,duration:0.15}},{tWhy - 0.05});')
# --- S2 intro
j(f'tl.fromTo("#t2a",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"}},{tLive - 0.05});')
j(f'tl.fromTo("#t2b",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.28,ease:"power4.out"}},{t6ix - 0.03});')
j(f'tl.fromTo("#t2c",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{tInside});')
j(f'tl.fromTo("#sky2",{{y:60}},{{y:0,duration:{C2 - C1:.3f},ease:"power1.out"}},{C1});')
j(f'document.querySelectorAll("#s2 .win").forEach((w,i)=>{{ if(i%4==0) tl.to(w,{{opacity:.15,duration:0.2,repeat:6,yoyo:true}},{C1}+(i%9)*0.31); }});')
j(f'tl.to("#s2 .tip",{{opacity:.1,duration:0.25,repeat:7,yoyo:true}},{C1});')
# --- S3 hypnogram + cortisol
j(f'tl.fromTo("#pn3",{{y:900}},{{y:0,duration:0.45,ease:"power3.out"}},{C2});')
j(f'(()=>{{const l=document.querySelector("#hyLine");const L=l.getTotalLength();l.style.strokeDasharray=L;'
  f'tl.fromTo(l,{{strokeDashoffset:L}},{{strokeDashoffset:0,duration:{tLight - wt("Sleep"):.3f},ease:"none",immediateRender:true}},{wt("Sleep")});'
  f'const c=document.querySelector("#hyCort");const K=c.getTotalLength();c.style.strokeDasharray=K;'
  f'tl.fromTo(c,{{strokeDashoffset:K}},{{strokeDashoffset:0,duration:{tMorning - tCort:.3f},ease:"power1.in",immediateRender:true}},{tCort});}})();')
j(f'tl.set("#hyCort",{{opacity:0}},0);tl.set("#hyCort",{{opacity:1}},{tCort});tl.fromTo("#hyAxis",{{opacity:0}},{{opacity:1,duration:0.3}},{C2 + 0.2});')
j(f'tl.to("#brk",{{opacity:1,duration:0.2}},{t90});tl.fromTo("#c90",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"}},{t90});')
j(f'tl.to("#hyDeep",{{opacity:1,duration:0.25}},{tDeep});tl.fromTo("#hyDeep",{{scale:1}},{{scale:1.06,transformOrigin:"50% 80%",duration:0.3,repeat:3,yoyo:true}},{tDeep});')
j(f'tl.fromTo("#cDeep",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"}},{tDeep + 0.15});')
j(f'tl.to(["#c90","#brk"],{{opacity:0,duration:0.2}},{t3am - 0.3});')
j(f'tl.fromTo("#m3",{{opacity:0,attr:{{"stroke-dashoffset":400}}}},{{opacity:1,attr:{{"stroke-dashoffset":0}},duration:0.35}},{t3am});')
j(f'tl.fromTo("#c3am",{{y:-40,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"bounce.out"}},{t3am});')
j(f'tl.fromTo("#dot3",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(3)"}},{t3am + 0.15});')
j(f'tl.fromTo("#cLight",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"}},{tLight});')
j(f'tl.to("#dot3",{{attr:{{cx:{xw:.0f},cy:{yw:.0f}}},duration:0.35,ease:"power3.out"}},{tEasy + 0.25});')
j(f'tl.to("#c3am",{{opacity:0,duration:0.15}},{tEasy + 0.25});tl.fromTo("#cWake",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"}},{tEasy + 0.35});')
j(f'tl.to(["#cDeep","#cLight","#cWake","#c3am","#m3"],{{opacity:0,duration:0.2}},{tCort - 0.15});tl.to(["#hyLine","#dot3","#hyDeep"],{{opacity:.28,duration:0.3}},{tCort - 0.15});')
j(f'tl.fromTo("#cCort",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"}},{tCort + 0.1});')
j(f'tl.fromTo("#sun",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(2)"}},{tMorning});')
j(f'tl.fromTo("#hyAll",{{scale:1.06,transformOrigin:"50% 50%"}},{{scale:1,duration:{C3 - C2:.3f},ease:"none"}},{C2});')
j(f'tl.fromTo("#cd3a",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{wt("Sleep") + 0.3});')
j(f'tl.to("#cd3a",{{x:600,duration:0.2,ease:"power2.in"}},{tCort - 0.25});tl.set("#cd3b",{{opacity:0}},0);'
  f'tl.fromTo("#cd3b",{{opacity:1,x:600}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.6)",immediateRender:false}},{tCort - 0.02});')
# --- S4 City Hall
j(f'tl.fromTo("#ch",{{y:120,scale:.92,transformOrigin:"600px 830px"}},{{y:0,scale:1,duration:0.6,ease:"power3.out"}},{C3});')
j(f'tl.set("#beacon",{{opacity:0}},0);')
j(f'tl.fromTo("#t4a",{{x:-500,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"back.out(1.6)"}},{tCity - 0.05});')
j(f'tl.fromTo("#t4b",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"}},{tHall});')
j(f'document.querySelectorAll("#ch .chw").forEach((w,i)=>{{tl.to(w,{{fill:(i%2?"#FF7A59":"#ff3b3b"),opacity:1,duration:0.06}},{tHigh}+(i%7)*0.02);'
  f'tl.to(w,{{opacity:.35,duration:0.12,repeat:6,yoyo:true}},{tHigh + 0.15}+(i%5)*0.03);}});')
j(f'tl.to("#red4",{{opacity:1,duration:0.15,repeat:5,yoyo:true}},{tHigh});tl.set("#red4",{{opacity:.5}},{tHigh + 0.95});')
j(f'tl.to("#sir",{{opacity:1,duration:0.1}},{tHigh - 0.05});')
j(C.lottie_js("sir", f"{P}/assets/siren.json", tHigh - 0.05, C4, loops=5))
j(f'tl.set("#dreamB",{{opacity:0}},0);tl.fromTo("#dreamB",{{opacity:0,scale:0,transformOrigin:"560px 640px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{tDream - 0.1});')
j(f'tl.to("#dreamB",{{y:-14,duration:0.4,repeat:1,yoyo:true,ease:"sine.inOut"}},{tDream + 0.25});')
j(f'tl.set("#crack",{{opacity:1}},{tBreaks});tl.fromTo("#dreamB",{{rotation:0}},{{rotation:-4,transformOrigin:"560px 640px",duration:0.06,repeat:5,yoyo:true}},{tBreaks});')
j(f'tl.to("#dreamB",{{y:420,rotation:18,opacity:0,duration:0.5,ease:"power2.in"}},{tBreaks + 0.45});')
j(f'tl.fromTo("#cd4",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tDream - 0.2});')
# --- S5 phone vs body clock
j(f'tl.fromTo(["#l5a","#l5b"],{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)",stagger:0.12}},{C4 + 0.25});')
j(f'tl.fromTo("#ph5w",{{x:-500}},{{x:0,duration:0.4,ease:"power3.out"}},{C4 + 0.05});tl.fromTo("#bc5w",{{x:500}},{{x:0,duration:0.4,ease:"power3.out"}},{C4 + 0.1});')
j('tl.set("#bcH",{svgOrigin:"725 560",rotation:120},0);tl.set("#bcM",{svgOrigin:"725 560",rotation:0},0);')
j(f'tl.fromTo("#rw5",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2.4)"}},{tFell - 0.05});tl.to("#rw5",{{opacity:0,duration:0.2}},{t3 + 0.3});')
j(f'tl.to("#ph5Time",{{scaleY:0,transformOrigin:"50% 50%",duration:0.1}},{tFell + 0.05});'
  f'tl.set("#ph5Time",{{opacity:0}},{tFell + 0.15});tl.set("#ph5T3",{{opacity:1,scaleY:0,transformOrigin:"50% 50%"}},{tFell + 0.15});'
  f'tl.to("#ph5T3",{{scaleY:1,duration:0.14,ease:"back.out(3)"}},{tFell + 0.16});')
j(f'tl.fromTo("#ph5w",{{scale:1}},{{scale:1.08,svgOrigin:"270 572",duration:0.2,yoyo:true,repeat:1}},{t3});')
j(f'tl.fromTo("#bc5w",{{scale:1}},{{scale:1.1,svgOrigin:"725 560",duration:0.2,yoyo:true,repeat:1}},{t4});tl.fromTo("#bcH",{{rotation:60}},{{rotation:120,duration:0.4,ease:"back.out(3)",svgOrigin:"725 560"}},{t4 - 0.1});')
j(f'tl.fromTo("#f5",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"}},{t4 + 0.1});')
# --- S6 night bus
j(f'tl.fromTo("#busW",{{x:900}},{{x:0,duration:0.6,ease:"power3.out"}},{C5});tl.fromTo("#busW",{{rotation:0}},{{rotation:-1.5,svgOrigin:"560 815",duration:0.12,yoyo:true,repeat:1}},{C5 + 0.55});')
j(f'document.querySelectorAll("#s6 .wheel").forEach(w=>tl.fromTo(w,{{rotation:0}},{{rotation:-540,transformOrigin:"50% 50%",duration:0.6,ease:"power3.out"}},{C5}));')
j(f'tl.fromTo("#b6",{{y:-80,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"bounce.out"}},{tBlue - 0.05});')
j(f'tl.fromTo("#b6",{{scale:1}},{{scale:1.12,duration:0.15,yoyo:true,repeat:1}},{tAhlie});')
# --- S7 serious: cup set down on the table, rows build, calm
j(f'tl.set("#cup",{{opacity:0}},{C6 + 0.05});tl.set("#cupTable",{{opacity:1}},{C6 + 0.05});tl.set("#cup",{{opacity:1}},{C7});tl.set("#cupTable",{{opacity:0}},{C7});tl.set("#cupTable",{{opacity:0}},0);')
j(f'tl.fromTo("#pn7",{{y:900}},{{y:0,duration:0.45,ease:"power3.out"}},{C6});')
for rid, tt in (("#r7a", tEvery), ("#r7b", tWrecked), ("#r7c", tTalk)):
    j(f'tl.fromTo("{rid}",{{x:-300,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"back.out(1.6)"}},{tt - 0.05});')
j(f'tl.fromTo("#cd7",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tNot - 0.05});')
# --- S8 outro
j(f'tl.fromTo("#pn8",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C7});')
j(f'tl.fromTo("#like8",{{scale:0,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.3,ease:"back.out(3)"}},{tLike});')
j(f'tl.fromTo("#sub8",{{scale:1}},{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},{tSub + 0.15});'
  f'tl.set("#subd8",{{opacity:0}},0);tl.set("#subd8",{{opacity:1}},{tSub + 0.25});tl.set("#sub8",{{opacity:0}},{tSub + 0.25});')
j(f'tl.fromTo("#src8",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{C7 + 0.2});')
# --- S9 loop frame (= hook frame 1): phone lit; Cyto eyes closed (sip) like the opening
j(f'tl.fromTo("#s9",{{opacity:0}},{{opacity:1,duration:0.2}},{C8});')
j(f'tl.set(["#eyeL","#eyeR"],{{opacity:0}},{T - 0.1});tl.set(["#ecL","#ecR"],{{opacity:1}},{T - 0.1});')

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<script src="assets/lottie_svg.min.js"></script>
<style>
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:InterXB; }}
#cam, #shaker {{ position:absolute; inset:0; transform-origin:540px 960px; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.bgfill {{ position:absolute; inset:0; }}
.navy {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #17304d 0%, #0c1622 70%); }}
.dots {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; background-image:radial-gradient(rgba(120,170,220,.10) 3px, transparent 4px); background-size:70px 70px; }}
.big {{ position:absolute; left:0; width:1080px; text-align:center; font-family:InterBlack; line-height:.95; letter-spacing:-2px;
  paint-order:stroke fill; -webkit-text-stroke:14px #0c1622; text-shadow:0 10px 0 #0c1622; opacity:0; }}
.row {{ position:absolute; left:40px; top:100px; font:50px InterBlack; color:#FAF4E8; display:flex; align-items:center; gap:24px; opacity:0; }}
.ic {{ display:inline-flex; width:84px; height:84px; border-radius:50%; border:5px solid #0c1622; align-items:center; justify-content:center; font:48px InterBlack; color:#0c1622; }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-200px; width:400px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
{R.rig3_css()}
{C.CAP_CSS}
{C.V2_CSS}
{C.TR_CSS}
#cytoLayer {{ position:absolute; inset:0; z-index:20; }}
</style>
</head>
<body>
{GLOBAL_DEFS}
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="shaker" class="clip" data-start="0" data-duration="{T}"><div id="cam">
{scene_html}
  <div id="cytoLayer">{R.rig3_html("outfit_pj", "cup_red", "acc_sleepmask")}</div>
</div></div>
<div id="pill" class="clip" data-start="0" data-duration="{T}">6IX SECONDS OF SCIENCE</div>
{cap_html}
{tr_html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const T = {T};
{rig_js}
{chr(10).join(J)}
{tr_js}
{cap_js}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
for f in ("hyperframes.json", "package.json"):
    if not os.path.exists(f): subprocess.run(["cp", f"/home/claude/hf/template/{f}", f])
json.dump({"name": "ep08"}, open("meta.json", "w"))
print("built", len(html), "bytes; T", T, "words", len(WORDS))
