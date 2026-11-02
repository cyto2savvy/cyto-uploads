"""EP09 — Is winter killing your vitamin D? (6ix Seconds of Science). v2 layout + v3 rig + art.py 2D + three3d.js 3D.
python3 build.py -> index.html + assets/audio.wav"""
import json, sys, os, subprocess, math, random, shutil
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import numpy as np
import cytohf as C, cyto3 as R, art as A
from engine import tone, noise, hp, lp, add, load_mono, SR

P = "/home/claude/hf/ep09"; os.chdir(P)
V = "/home/claude/ep9"
TM = json.load(open(f"{V}/timing.json")); WORDS = TM["words"]
T = 40.3
C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11 = 4.45, 8.72, 11.82, 16.08, 18.03, 21.73, 26.12, 28.73, 30.75, 37.15, 39.62
W, H = 1080, 1920


def wt(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and w["w"].lower().strip(".,?!:").startswith(word.lower()):
            return round(w["t0"], 3)
    raise KeyError(word)


# ------------------------------------------------------------------ assets
LOTS = ["sunset-2.json", "sunset-3.json", "capsule-1.json", "bulb-2.json", "trophy-1.json"]
C.copy_assets_v2(P, lotties=LOTS)
for f in ("outfit_puffer.png",):
    shutil.copy(f"/home/claude/cyto2/rig/{f}", "assets/")
shutil.copy("/home/claude/hf/node_modules/three/build/three.min.js", "assets/")
shutil.copy("/home/claude/hf/three3d.js", "assets/")

# ------------------------------------------------------------------ word beats
tBro, tDark, tFive, tWinter, tVit, tD1 = wt("Bro"), wt("dark"), wt("five"), wt("winter"), wt("vitamin"), wt("D", 4.0)
tYo, tCyto, tLive, t6ix, tInside = wt("Yo"), wt("Cyto"), wt("live"), wt("6ix"), wt("inside")
tSun, tClocks, tD2, tCrash, tAhlie = wt("Sun"), wt("clocks"), wt("D", 10), wt("crashes"), wt("ahlie")
tNah, tCan, tDip, tSmall, tWhat, tMore = wt("Nah"), wt("Canadian"), wt("dip"), wt("small"), wt("What"), wt("more")
tSupp, tAnc, tSouth, tLow, tAll, tStyll = wt("Supplements"), wt("ancestry"), wt("South"), wt("low"), wt("all"), wt("styll")
tBut, tMood, tSome, tSeas, tDep = wt("But"), wt("mood"), wt("some"), wt("seasonal"), wt("depression")
tAnd2, tYear, tReview, tSeven, tTrials = wt("And", 26), wt("2025"), wt("review"), wt("seventeen"), wt("trials")
tBright, tWhite, tLight, tCame, tTop = wt("Bright"), wt("white"), wt("light", 29), wt("came"), wt("top")
tSo, tBlame, tTTC, tVibe, tCheck, tGet, tSay, tLess, tNot = wt("So", 30), wt("blame"), wt("TTC"), wt("vibe"), wt("check"), wt("get"), wt("say"), wt("less"), wt("Not")
tLike, tSub, tSee, tFive2 = wt("Like"), wt("subscribe"), wt("see"), wt("five", 38)

# ------------------------------------------------------------------ audio: lo-fi winter beat; mood section muffled, opens up on "Bright"
def rhodes(m, dur):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.02) * np.exp(-t / 1.5)
    trem = 1 + 0.16 * np.sin(2 * np.pi * 4.0 * t)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t / .3)) * env * trem * 0.06


def bell(f0, dur=1.2, g=0.12):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f0 * t) + .5 * np.sin(2 * np.pi * f0 * 2.76 * t) * np.exp(-t / .2)) * np.exp(-t / .5) * g


def make_audio(sfx_events):
    n = int((T + 0.3) * SR); music = np.zeros(n, np.float32); drums = np.zeros(n, np.float32)
    BEAT = 60 / 88; BAR = BEAT * 4
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]   # Am7 Fmaj7 Cmaj7 G6
    t = 0.0; i = 0
    while t < T + 0.3:
        for k, m in enumerate(chords[i % 4]): add(music, rhodes(m, BAR + 0.4), t + k * 0.014)
        add(music, rhodes(chords[i % 4][0] - 12, BAR) * 1.5, t)
        t += BAR; i += 1
    kick = tone(120, 45, 0.35, 0.12) * 0.9
    snare = lp(hp(noise(0.18, 1)), 0.5) * np.exp(-np.arange(int(0.18 * SR)) / SR / 0.05) * 0.36
    hat = hp(noise(0.04, 2), 0.6) * np.exp(-np.arange(int(0.04 * SR)) / SR / 0.01) * 0.15
    t = C1; s = 0
    while t < T + 0.3:
        quiet = (C6 - 0.1 <= t < C8 - 0.05) or (tNot - 0.1 <= t < C10 - 0.05)
        if not quiet:
            p = s % 8
            if p in (0, 3, 5): add(drums, kick, t)
            if p in (2, 6): add(drums, snare, t)
            add(drums, hat, t + (0.06 if s % 2 else 0), 0.9 if s % 2 == 0 else 0.55)
        t += BEAT / 2; s += 1
    rnd = np.random.default_rng(9); crackle = np.zeros(n, np.float32)
    for p_ in rnd.integers(0, n - 200, 900): crackle[p_:p_ + 60] += rnd.uniform(-1, 1) * np.exp(-np.arange(60) / 10) * 0.05
    music = lp(music, 0.35) + crackle * 0.6
    a = int(C1 * SR); music[:a] = lp(music[:a], 0.08) * 1.8
    a, b = int((C6 - 0.1) * SR), int((C8 - 0.05) * SR); music[a:b] = lp(music[a:b], 0.06) * 1.9       # the dark: muffled
    a, b = int((tNot - 0.1) * SR), int((C10 - 0.05) * SR); music[a:b] = lp(music[a:b], 0.12) * 1.5
    music += drums
    v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.55 * np.clip(env * 3, 0, 1)); music *= 0.42
    S = {
        "whoosh": lp(noise(0.4, 3), 0.25) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))) ** 2 * 0.45,
        "boom": tone(90, 35, 0.9, 0.35) * 0.8,
        "pop": tone(1200, 380, 0.08, 0.03) * 0.3,
        "plink": tone(1900, 1500, 0.07, 0.03) * 0.22,
        "ding": (tone(1760, 1760, 0.6, 0.18) + 0.5 * tone(2640, 2640, 0.6, 0.12)) * 0.2,
        "crunch": np.round(noise(0.35, 6) * 3) / 3 * 0.13 * np.linspace(1, 0, int(0.35 * SR)),
        "rise": np.sin(2 * np.pi * np.cumsum(np.linspace(300, 900, int(0.6 * SR))) / SR) * np.linspace(0, 1, int(0.6 * SR)) * 0.06,
        "fall": np.sin(2 * np.pi * np.cumsum(np.linspace(900, 250, int(0.5 * SR))) / SR) * np.linspace(1, 0, int(0.5 * SR)) * 0.07,
        "click": tone(2200, 900, 0.05, 0.015) * 0.35,
        "sparkle": sum(bell(f, 1.0, 0.07) * 1 for f in (1568, 2093, 2637)),
        "tram": np.concatenate([bell(1046, 0.35, 0.16)[:int(.22 * SR)], bell(1046, 0.9, 0.16)]),
        "switch": tone(3000, 1200, 0.03, 0.01) * 0.5,
    }
    sfx = np.zeros(n, np.float32)
    for kind, tt in sfx_events: add(sfx, S[kind], tt)
    mix = music + sfx; mix[:m] += v[:m]
    mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[: int(T * SR)]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/raw_mix.wav"],
                   input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/raw_mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "assets/base.wav"], check=True)


SFX = [("boom", tBro), ("ding", tFive), ("pop", tVit), ("boom", C1), ("pop", tLive), ("boom", t6ix), ("pop", tInside),
       ("fall", tClocks), ("crunch", tCrash), ("pop", tAhlie), ("boom", tNah), ("rise", tCan + 0.3), ("ding", tSmall), ("fall", tWhat + 0.2),
       ("pop", tSupp), ("pop", tAnc), ("pop", tSouth), ("boom", tAll), ("pop", tSeas), ("pop", tReview), ("ding", tTrials - 0.1),
       ("switch", tBright - 0.05), ("sparkle", tBright), ("boom", tTop), ("tram", C9 + 0.5), ("pop", tTTC), ("ding", tCheck), ("ding", tGet),
       ("boom", tSay), ("pop", tNot), ("pop", tLike), ("click", tSub + 0.15)]
SFX += [("plink", C4 + 0.15 + i * 0.09 + 0.43) for i in range(7)]
SFX += [("pop", tSeven + 0.04 * i) for i in range(0, 17, 4)]
SFX += [("whoosh", c - 0.18) for c in (C2, C3, C4, C5, C6, C7, C8, C9, C10)]
make_audio(SFX)

# ------------------------------------------------------------------ Cyto: positions + acting
POS_HOOK, POS_BIG, POS_V2 = C.place(330, 1335, 0.60), C.place(540, 1300, 0.66), C.CYTO_V2
SIPS = [(39.45, 0.7)]
mouth = R.viseme_track(f"{V}/voice.wav", WORDS)
if mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
blinks = [(t, 0.1) for t in (2.9, 6.6, 9.6, 13.0, 15.6, 18.9, 23.0, 25.7, 29.0, 32.4, 34.8, 37.9)]
gest = dict(sips=SIPS, raises=[(tCyto, 0.6), (tTop - 0.1, 0.8)], waves=[tYo, tSee - 0.1],
            points=[(tSmall - 0.05, 0.8), (tSeven - 0.05, 0.8), (tCheck - 0.05, 0.7)],
            tilts=[(tAhlie, 0.6, 8), (tStyll, 0.7, -8), (tTTC, 0.6, 7), (tLess, 0.5, -6)],
            shrugs=[(tNah, 0.6), (tWhat, 0.6)])
expr = [(tBro - 0.04, 0.7, "shock"), (tDark, 1.0, "shock"), (tVit - 0.05, 0.6, "skeptic"), (tCyto - 0.05, 0.5, "hype"), (t6ix, 0.5, "hype"),
        (tSun, 1.4, "skeptic"), (tCrash, 0.6, "squint"), (tNah - 0.05, 0.5, "hype"), (tSmall - 0.05, 0.6, "shock"),
        (tSupp, 0.5, "hype"), (tAll, 0.7, "shock"), (tBut, 3.4, "sad"), (tSeven - 0.05, 0.6, "shock"),
        (tBright - 0.05, 0.4, "shock"), (tCame - 0.05, 0.9, "hype"), (tBlame - 0.05, 0.7, "skeptic"), (tSay - 0.05, 0.6, "hype"),
        (tNot - 0.05, 1.0, "squint")]
looks = [(C2 + 0.25, 12, -18), (C3 + 0.3, 12, -16), (C4 + 0.2, 14, -16), (C5 + 0.2, 12, -14), (C6 + 0.3, 14, -10),
         (C7 + 0.2, 12, -16), (C8 + 0.1, 16, -6), (C9 + 0.3, 12, -14), (C10 + 0.2, 0, -10), (C11 - 0.2, 0, 0)]
rig_js = R.rig3_js(mouth, T, blinks=blinks, mute=[(s[0], 0) for s in SIPS], expr=expr, looks=looks, **gest)
R.mix_sips("assets/base.wav", [s[0] for s in SIPS], "assets/audio.wav")

# ------------------------------------------------------------------ captions + transitions
KEYS = {"five": "#FFD166", "vitamin": "#FFD166", "d": "#FFD166", "winter": "#9fc3e8", "nah": "#FF7A59", "small": "#5AE68C",
        "supplements": "#FFD166", "ancestry": "#3fc1b0", "year": "#FF7A59", "ahlie": "#3fc1b0", "styll": "#3fc1b0", "mood": "#c4b0ff",
        "seasonal": "#c4b0ff", "depression": "#c4b0ff", "2025": "#FFD166", "seventeen": "#FFD166", "bright": "#FFD166", "light": "#FFD166",
        "top": "#5AE68C", "ttc": "#E2394B", "say": "#3fc1b0", "less": "#3fc1b0", "subscribe": "#FF7A59", "dark": "#9fc3e8"}
CAPW = [w for w in WORDS if not (tLive - 0.01 <= w["t0"] < C2)]
cap_html, cap_js = C.captions(CAPW, KEYS, y=C.CAP_Y_V2)
last_cap = cap_html.count('"cap clip"') - 1
cap_js += f'\ntl.set("#cap{last_cap}",{{opacity:0}},{C11});'
TRS = [C.transition(k, t) for k, t in (("zoom", C1), ("membrane", C2), ("whip", C3), ("zoom", C4), ("whip", C5), ("membrane", C6),
                                        ("whip", C7), ("zoom", C8), ("doors", C9), ("whip", C10))]
tr_html = "\n".join(h for h, _ in TRS); tr_js = "\n".join(j for _, j in TRS)


# ------------------------------------------------------------------ helpers
def chip(id_, text, left, top, bg="#FFD166", fg=A.INK, size=34, extra=""):
    return (f'<div id="{id_}" class="chip" style="left:{left}px;top:{top}px;background:{bg};color:{fg};font-size:{size}px;{extra}">{text}</div>')


def snow(idp, n=46, seed=1, top=0, height=1500, size=(6, 14)):
    rnd = random.Random(seed)
    flakes = [(rnd.uniform(0, W), rnd.uniform(-height, 0), rnd.uniform(*size), rnd.uniform(.4, .95), rnd.uniform(2.6, 5.0)) for _ in range(n)]
    html = "".join(f'<div class="flake {idp}" data-v="{v:.2f}" style="left:{x:.0f}px;top:{top + y:.0f}px;width:{s:.0f}px;height:{s:.0f}px;opacity:{o:.2f}"></div>' for x, y, s, o, v in flakes)
    return html


def snow_js(idp, t0, t1, height=1700):
    return (f'document.querySelectorAll(".{idp}").forEach((f,i)=>{{const v=+f.dataset.v;'
            f'tl.fromTo(f,{{y:0,x:0}},{{y:{height},x:(i%2?40:-40),duration:v,ease:"none",repeat:Math.ceil({t1 - t0:.2f}/v)}},{t0:.2f});}});')


def lot(id_, file, t0, t1, loops=1, offset=0, ease="none"):
    """Lottie driven by the timeline, optional start-frame offset (skip blank intros)."""
    data = open(f"{P}/assets/{file}").read(); v = id_.replace("-", "_")
    return (f'const L_{v}=lottie.loadAnimation({{container:document.getElementById("{id_}"),renderer:"svg",loop:false,autoplay:false,animationData:{data}}});'
            f'const P_{v}={{f:0}};tl.fromTo(P_{v},{{f:0}},{{f:L_{v}.totalFrames*{loops}-0.01,duration:{t1 - t0:.3f},ease:"{ease}",'
            f'onUpdate:()=>L_{v}.goToAndStop(({offset}+P_{v}.f) % L_{v}.totalFrames,true)}},{t0:.3f});')


def three(var, factory, canvas_id, t0, t1, opts="{}"):
    return (f'const {var}=C3D.{factory}(document.getElementById("{canvas_id}"),{opts});const P{var}={{t:0}};{var}.render(0);'
            f'tl.fromTo(P{var},{{t:0}},{{t:{t1 - t0:.3f},duration:{t1 - t0:.3f},ease:"none",onUpdate:()=>{var}.render(P{var}.t)}},{t0:.3f});')


GLOBAL_DEFS = f'<svg width="0" height="0" style="position:absolute"><defs>{A.PHONE_DEFS}</defs></svg>'

# ------------------------------------------------------------------ scenes
def dusk(idp):
    """Hook backdrop: dusk sky (animatable), sinking sun, skyline whose windows switch on."""
    return f'''<div id="{idp}Sky" class="bgfill" style="background:linear-gradient(#24365e 0%,#f28b5b 62%,#ffcf7a 78%)"></div>
<div id="{idp}Night" class="bgfill" style="background:linear-gradient(#070d1a 0%,#14274a 70%,#2a3f6b 85%);opacity:0"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">
 <g id="{idp}Stars" opacity="0">{A.stars(W, H, 50, 21, .45)}</g>
 <g id="{idp}SunG"><circle cx="760" cy="700" r="150" fill="#FFD166" opacity=".25"/><circle id="{idp}Sun" cx="760" cy="700" r="92" fill="#FFD166" stroke="{A.INK}" stroke-width="8"/></g>
 <g id="{idp}City">{A.skyline(W, H, 1010, .92, seed=7, lit=.42, cn=300, ground="#0c1622")}</g>
</svg>'''


S1 = dusk("h1") + f'''
<div id="clk1" class="chip" style="left:520px;top:205px;font-size:44px;background:#0c1622;color:#FFD166;border-color:#FFD166">☀︎ SUNSET ≈ 5:00</div>
<div id="t1a" class="big" style="top:330px;font-size:150px;color:#FFD166">VITAMIN D</div>
<div id="t1b" class="big" style="top:470px;font-size:84px;color:#FAF4E8">GONE?!</div>'''

S2 = dusk("h2") + f'''<div class="snowL">{snow("sn2", 40, 2)}</div>
<div id="t2a" class="big" style="top:250px;font-size:74px;color:#FAF4E8">LIVE FROM</div>
<div id="t2b" class="big" style="top:330px;font-size:210px;color:#FFD166">THE 6IX</div>
{chip("t2c", "...INSIDE YOUR BODY", 270, 590, bg="#FF7A59", size=40)}'''

S3 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 30%, #13254a 0%, #050a14 70%)"></div>
<div style="position:absolute;left:0;top:150px;width:1080px;height:740px">
 <canvas id="cvE" width="1080" height="740" style="position:absolute;left:0;top:0"></canvas>
 <div id="pinLab" class="pin">TORONTO</div></div>
{chip("dDown", "D ↓↓↓", 700, 640, bg="#FF7A59", size=56)}
<div id="cd3" class="card"><div id="lSun" style="position:absolute;right:10px;top:-90px;width:130px;height:130px"></div><h3>THE MYTH</h3><p>Sun clocks out → your vitamin D crashes?</p></div>'''

S4 = f'''<div class="navy"></div><div id="dots4" class="dots"></div>
<div id="pn4" class="panel"><div class="ptitle">VITAMIN D IN YOUR BLOOD</div>
 <canvas id="cvB" width="880" height="650" style="position:absolute;left:0;top:0"></canvas>
 <div id="lbS" class="blab" style="color:#FFD166">SUMMER</div><div id="lbW" class="blab" style="color:#9fc3e8">WINTER</div>
 <div id="gap" class="gap"><span>ONLY ≈12 nmol/L</span></div>
 <div id="lSun2" style="position:absolute;left:640px;top:20px;width:150px;height:150px"></div>
 <div id="q4" class="big" style="top:160px;font-size:240px;color:#FFD166">?</div>
</div>
<div id="nah" class="stamp" style="left:520px;top:540px">NAH.</div>
<div id="cd4" class="card"><h3>LI 2011 · VANCOUVER</h3><p>Summer was only ~12 nmol/L higher than winter.</p></div>'''

S5 = f'''<div class="navy"></div><div id="dots5" class="dots"></div>
<div id="pn5" class="panel"><div class="ptitle">WHAT MATTERED WAY MORE</div>
 <canvas id="cvC" width="880" height="650" style="position:absolute;left:0;top:0"></canvas>
 {chip("cSupp", "SUPPLEMENTS", 40, 90, size=40)}
 {chip("cAnc", "ANCESTRY", 560, 90, bg="#3fc1b0", size=40)}
</div>
<div id="cd5" class="card"><div id="lCap" style="position:absolute;right:6px;top:-110px;width:130px;height:130px"></div><h3>NAGASAKA 2018</h3><p>Health Canada study: supplements + ancestry beat season.</p></div>'''

SEAS = [("WINTER", "❄", "#9fc3e8"), ("SPRING", "✿", "#c4b0ff"), ("SUMMER", "☀", "#FFD166"), ("FALL", "❦", "#FF7A59")]
tiles = "".join(f'''<div class="tile" id="tile{i}" style="left:{40 + i * 205}px"><div class="tic" style="color:{c}">{ic}</div><div class="tname">{n}</div>
 <svg width="160" height="96" style="position:absolute;left:12px;top:150px"><path d="M14 86 A66 66 0 0 1 146 86" fill="none" stroke="#2a4866" stroke-width="18"/>
 <path d="M14 86 A66 66 0 0 1 146 86" fill="none" stroke="#FF7A59" stroke-width="18" stroke-dasharray="208" stroke-dashoffset="208" class="garc" id="garc{i}"/>
 <g id="gnd{i}" style="transform-origin:80px 86px"><path d="M80 86 L80 30" stroke="#FAF4E8" stroke-width="7" stroke-linecap="round"/></g><circle cx="80" cy="86" r="10" fill="#FAF4E8"/></svg>
 <div class="tlow">LOW</div></div>''' for i, (n, ic, c) in enumerate(SEAS))
S6 = f'''<div class="navy"></div><div id="dots6" class="dots"></div>
<div id="pn6" class="panel"><div class="ptitle">SOUTH ASIAN CANADIANS · HEALTH CANADA STUDY</div>
 <div id="h6" style="position:absolute;left:40px;top:80px;font:52px/1.05 InterBlack;color:#FAF4E8">LOW D WAS <span style="color:#FF7A59">MORE COMMON</span></div>
 {tiles}
 <div id="ay" class="stamp" style="left:230px;top:505px;font-size:84px">ALL YEAR</div>
</div>
<div id="cd6" class="card"><h3>NAGASAKA 2018</h3><p>vs European-ancestry Canadians, in every season tested.</p></div>'''


def room(idp, lampOn=False):
    return f'''<div id="{idp}Wall" class="bgfill" style="background:linear-gradient(#18233d,#0e1628)"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">
 {A.window(560, 230, 400, 470, idp=idp + "W")}
 <g clip-path="url(#{idp}Clip)"><clipPath id="{idp}Clip"><rect x="560" y="230" width="400" height="470"/></clipPath>
  {A.moon(860, 320, 40, "#0b1630")}{A.stars(W, H, 25, 31, .4)}</g>
 <rect x="-20" y="1040" width="1120" height="900" fill="#0b1220"/>
 {A.lamp(270, 1040, idp=idp + "L")}
</svg>
<div class="snowW" style="position:absolute;left:560px;top:230px;width:400px;height:470px;overflow:hidden">{snow(idp + "s", 26, 5, 0, 600, (5, 10))}</div>
<div id="{idp}Dim" class="bgfill" style="background:#05080f;opacity:0"></div>'''


S7 = room("r7") + f'''
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible"><g transform="translate(-60,180)"><g id="cloud7" opacity="0">
 <path d="M300 880 Q250 880 255 835 Q258 790 310 795 Q325 745 385 755 Q430 720 470 765 Q525 760 525 815 Q560 830 545 870 Q535 885 500 885 Z" fill="#6b7a90" stroke="#0c1622" stroke-width="8"/>
 <g id="rain7">{"".join(f'<path class="drop" d="M{x} {y} l-8 26" stroke="#9fc3e8" stroke-width="6" stroke-linecap="round"/>' for x, y in ((310, 905), (360, 925), (410, 905), (460, 925), (500, 905)))}</g></g></g></svg>
{chip("sad7", "SEASONAL AFFECTIVE DISORDER", 90, 250, bg="#c4b0ff", size=34)}
{chip("some7", "FOR SOME PEOPLE", 90, 330, bg="#FAF4E8", size=30)}
<div id="cd7" class="card" style="border-left-color:#c4b0ff"><h3 style="color:#7a5cc7">REAL TALK</h3><p>Seasonal depression is a real condition.</p></div>'''

papers = "".join(f'<div class="paper" id="pp{i}" style="left:{70 + (i % 6) * 128}px;top:{150 + (i // 6) * 150}px"><div></div><div></div><div></div></div>' for i in range(17))
S8 = f'''<div class="navy"></div><div id="dots8" class="dots"></div>
<div id="pn8" class="panel"><div class="ptitle">2025 REVIEW · LIGHT THERAPY FOR SAD</div>
 {papers}
 <div id="cnt8" style="position:absolute;right:46px;top:400px;font:130px InterBlack;color:#FFD166;text-align:right">0</div>
 <div style="position:absolute;right:50px;top:560px;font:30px InterXB;color:#96b0c4">TRIALS · 773 PATIENTS</div>
</div>
<div id="cd8" class="card"><h3>WAN 2025 · MEDICINE</h3><p>17 randomized trials compared light colours.</p></div>'''

S9 = room("r9") + f'''
<div id="lBulb" style="position:absolute;left:600px;top:760px;width:160px;height:160px;opacity:0"></div>
<div id="tro" style="position:absolute;left:640px;top:250px;width:300px;height:300px;filter:hue-rotate(-75deg) saturate(3) brightness(1.4);opacity:0"></div>
<div id="win9" class="big" style="top:560px;left:540px;width:520px;font-size:66px;color:#FFD166">#1 BRIGHT<br>WHITE LIGHT</div>'''

S10 = f'''<div class="bgfill" style="background:linear-gradient(#1b2d52 0%,#3a3f6b 45%,#c46a5a 80%,#e8956a 92%)"></div>
<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">{A.stars(W, H, 20, 41, .3)}
 {A.skyline(W, H, 560, .62, seed=19, lit=.45, cn=860, ground="#1a2236")}
 <rect x="-20" y="555" width="1120" height="240" fill="#2a3346"/>
 <path d="M0 735 H1080 M0 760 H1080" stroke="#7a8496" stroke-width="7"/>
 <g id="tramW">{A.streetcar(80, 450, 1.0)}</g>
 {A.stop_pole(980, 790, 300)}
 <rect x="-20" y="790" width="1120" height="1200" fill="#0f1626"/></svg>
<div class="snowL">{snow("sn10", 46, 7)}</div>
{chip("ttc10", "BLAME THE TTC?", 70, 250, bg="#E2394B", fg="#fff", size=44)}
{chip("ck1", "✓ CHECK YOUR D", 510, 1045, bg="#FFD166", size=36)}
{chip("ck2", "✓ GET SOME LIGHT", 510, 1135, bg="#FAF4E8", size=36)}
<div id="sl10" class="stamp" style="left:520px;top:1235px;font-size:64px">SAY LESS</div>
<div id="cd10" class="card" style="border-left-color:#3fc1b0;top:1250px"><h3 style="color:#188076">HEADS UP</h3><p>Not medical advice. Ask a doctor or pharmacist.</p></div>'''

S11 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 30%, #1d3a66 0%, #0c1622 70%)"></div>
<div id="pn11" class="panel">
 <div id="sub11" class="subbtn" style="background:#FF7A59;color:#0c1622">SUBSCRIBE</div>
 <div id="subd11" class="subbtn" style="background:#3a4a5e;color:#FAF4E8;opacity:0;font-size:60px">SUBSCRIBED ✓</div>
 <div id="like11" style="position:absolute;left:760px;top:70px;font:110px InterBlack;opacity:0">👍</div>
 <div style="position:absolute;left:40px;top:270px;font:30px InterBlack;color:#FFD166;letter-spacing:.05em">SOURCES</div>
 <div id="src11" style="position:absolute;left:40px;top:320px;width:800px;font:25px/1.45 InterSB;color:#cfe0ff">
  Li et al. 2011 · Can J Public Health<br>Nagasaka et al. 2018 · PLoS One (Health Canada)<br>Wan et al. 2025 · Medicine<br>
  <span style="color:#96b0c4">Links in the description · Not medical advice</span></div>
</div>'''

S12 = dusk("h12") + f'''
<div class="chip" style="left:520px;top:205px;font-size:44px;background:#0c1622;color:#FFD166;border-color:#FFD166;opacity:0">☀︎ SUNSET ≈ 5:00</div>'''

scenes = [("s1", 0, C1, S1), ("s2", C1, C2, S2), ("s3", C2, C3, S3), ("s4", C3, C4, S4), ("s5", C4, C5, S5), ("s6", C5, C6, S6),
          ("s7", C6, C7, S7), ("s8", C7, C8, S8), ("s9", C8, C9, S9), ("s10", C9, C10, S10), ("s11", C10, C11, S11), ("s12", C11, T, S12)]
scene_html = "\n".join(f'<div id="{i}" class="scene clip" data-start="{a}" data-duration="{round(b - a, 3)}">{h}</div>' for i, a, b, h in scenes)

# ------------------------------------------------------------------ timeline beats
J = []
def j(s): J.append(s)
for _, a, b, _h in scenes:
    j(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.045,duration:{b - a - 0.05:.3f},ease:"none",immediateRender:false}},{a + 0.01:.3f});')
j('const punch=(t,s=1.08)=>{tl.to("#shaker",{scale:s,duration:0.08,ease:"power2.out"},t);tl.to("#shaker",{scale:1,duration:0.3,ease:"power2.inOut"},t+0.08);};')
j('const shake=(t,d=0.5,a=14)=>{tl.fromTo("#shaker",{x:-a},{x:a,duration:0.05,repeat:Math.round(d/0.05),yoyo:true,ease:"none",immediateRender:false},t);tl.to("#shaker",{x:0,duration:0.05},t+d);};')
j('const pop=(s,t,from=0)=>tl.fromTo(s,{scale:from,opacity:0},{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"},t);')
for t in (tBro, tVit, t6ix, tNah, tSmall, tAll, tTop, tSay): j(f"punch({t:.3f});")
for t, d in ((tDark, 0.4), (tCrash, 0.35), (tNah, 0.3)): j(f"shake({t:.3f},{d});")
j('tl.set("#shaker",{x:0,y:0,scale:1},0);')
for b, a, d in (("#dots4", C3, C4 - C3), ("#dots5", C4, C5 - C4), ("#dots6", C5, C6 - C5), ("#dots8", C7, C8 - C7)):
    j(f'tl.fromTo("{b}",{{x:0,y:0}},{{x:70,y:140,duration:{d:.3f},ease:"none"}},{a});')
for t, pos in ((0, POS_HOOK), (C1, POS_BIG), (C2, POS_V2), (C6, POS_V2), (C10, POS_V2), (C11, POS_HOOK)):
    j(f'tl.set("#cytoPos",{json.dumps(pos)},{t});')
j(f'tl.set("#cytoPos",{json.dumps(POS_HOOK)},{T - 0.01});')

# --- S1 hook: sun sinks, sky goes night, windows switch on
def dusk_js(idp, t0, dur, start_k=0.0):
    return (f'tl.fromTo("#{idp}Sun",{{attr:{{cy:700}}}},{{attr:{{cy:1080}},duration:{dur},ease:"power1.in"}},{t0});'
            f'tl.fromTo("#{idp}SunG",{{opacity:1}},{{opacity:0.0,duration:{dur},ease:"power2.in"}},{t0});'
            f'tl.fromTo("#{idp}Night",{{opacity:{start_k}}},{{opacity:1,duration:{dur},ease:"power1.inOut"}},{t0});'
            f'tl.fromTo("#{idp}Stars",{{opacity:0}},{{opacity:1,duration:{dur},ease:"power2.in"}},{t0});'
            f'document.querySelectorAll("#{idp}City .win").forEach((w,i)=>tl.fromTo(w,{{opacity:0}},{{opacity:.9,duration:0.08}},{t0}+({dur}*0.25)+(i%13)*{dur * 0.05:.3f}));')
j(dusk_js("h1", 0.0, 2.6))
j(f'pop("#clk1",{tFive - 0.05});tl.fromTo("#clk1",{{rotation:-6}},{{rotation:0,duration:0.4,ease:"elastic.out(1,0.4)"}},{tFive});')
j(f'tl.fromTo("#t1a",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.26,ease:"power4.out"}},{tVit - 0.03});')
j(f'tl.fromTo("#t1b",{{y:-80,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"bounce.out"}},{tD1});')
j(f'tl.to("#t1a",{{color:"#FF7A59",duration:0.12,repeat:3,yoyo:true}},{tD1 + 0.2});')
# --- S2 intro (night city, snow)
j(f'tl.set("#h2Night",{{opacity:1}},0);tl.set("#h2Stars",{{opacity:1}},0);tl.set("#h2SunG",{{opacity:0}},0);'
  f'document.querySelectorAll("#h2City .win").forEach((w,i)=>{{ if(i%4==0) tl.to(w,{{opacity:.15,duration:0.2,repeat:6,yoyo:true}},{C1}+(i%9)*0.31); }});')
j(snow_js("sn2", C1, C2))
j(f'tl.fromTo("#t2a",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"}},{tLive - 0.05});')
j(f'tl.fromTo("#t2b",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.28,ease:"power4.out"}},{t6ix - 0.03});')
j(f'tl.fromTo("#t2c",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{tInside});')
j(f'tl.fromTo("#h2City",{{y:60}},{{y:0,duration:{C2 - C1:.3f},ease:"power1.out"}},{C1});')
# --- S3 3D Earth
j(three("E3", "earth", "cvE", C2, C3, f'{{dur:{C3 - C2:.3f},rot0:-1.05,rot1:0.6,label:document.getElementById("pinLab")}}'))
j(lot("lSun", "sunset-2.json", C2, C3, loops=1))
j(f'tl.fromTo("#cd3",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{C2 + 0.2});')
j(f'pop("#dDown",{tCrash - 0.05});tl.fromTo("#dDown",{{y:0}},{{y:30,duration:0.12,repeat:5,yoyo:true}},{tCrash + 0.25});')
# --- S4 3D bars
j(three("B4", "bars", "cvB", C3, C4,
        f'{{dur:{C4 - C3:.3f},tGrow:{tCan - C3 + 0.1:.3f},tSink:{tWhat - C3 + 0.25:.3f},zoomAt:{tSmall - C3 - 0.3:.3f},'
        f'bars:[{{h:.95,color:0xffb703}},{{h:.79,color:0x4f86ff}}],labels:[document.getElementById("lbS"),document.getElementById("lbW")],gap:document.getElementById("gap")}}'))
j(f'tl.fromTo("#pn4",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C3 + 0.05});')
j(f'tl.fromTo("#nah",{{scale:3,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-8,duration:0.22,ease:"power4.out"}},{tNah - 0.03});tl.to("#nah",{{opacity:0,scale:.6,duration:0.2}},{tCan});')
j(f'tl.fromTo(["#lbS","#lbW"],{{opacity:0}},{{opacity:1,duration:0.25}},{tCan + 0.5});')
j(f'tl.set("#gap",{{opacity:0}},0);pop("#gap",{tSmall - 0.05});tl.to(["#lbS","#lbW","#gap"],{{opacity:0,duration:0.2}},{tWhat + 0.2});')
j(lot("lSun2", "sunset-3.json", C3, C4, loops=1))
j(f'tl.fromTo("#cd4",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tCan});')
j(f'tl.set("#q4",{{opacity:0}},0);tl.fromTo("#q4",{{scale:0,opacity:0,rotation:-20}},{{scale:1,opacity:1,rotation:0,duration:0.35,ease:"back.out(2.6)"}},{tMore - 0.05});')
# --- S5 3D capsules -> DNA
j(three("K5", "capsulesDna", "cvC", C4, C5, f'{{tDrop:0.12,tDna:{tAnc - C4 - 0.1:.3f}}}'))
j(f'tl.fromTo("#pn5",{{scale:1.15,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"power3.out"}},{C4});')
j(f'tl.set(["#cSupp","#cAnc"],{{opacity:0}},0);pop("#cSupp",{tSupp});pop("#cAnc",{tAnc});tl.to("#cSupp",{{opacity:.35,duration:0.2}},{tAnc});')
j(lot("lCap", "capsule-1.json", C4, C5, loops=1))
j(f'tl.fromTo("#cd5",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{C4 + 0.2});')
# --- S6 all-year gauges
j(f'tl.fromTo("#pn6",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C5});')
j(f'tl.fromTo("#h6",{{x:-400,opacity:0}},{{x:0,opacity:1,duration:0.35,ease:"back.out(1.6)"}},{tSouth});')
for i in range(4):
    t0 = tLow + i * 0.22
    j(f'tl.fromTo("#tile{i}",{{y:300,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(1.8)"}},{C5 + 0.2 + i * 0.12:.3f});')
    j(f'tl.fromTo("#gnd{i}",{{rotation:-90}},{{rotation:-55,duration:0.5,ease:"back.out(2)"}},{t0:.3f});'
      f'tl.fromTo("#garc{i}",{{attr:{{"stroke-dashoffset":208}}}},{{attr:{{"stroke-dashoffset":168}},duration:0.5}},{t0:.3f});')
    j(f'tl.fromTo("#tile{i} .tlow",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(3)"}},{t0 + 0.3:.3f});')
j(f'tl.set("#ay",{{opacity:0}},0);tl.fromTo("#ay",{{scale:3,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-6,duration:0.22,ease:"power4.out"}},{tAll - 0.03});')
j(f'tl.fromTo("#cd6",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tSouth + 0.3});')
# --- S7 mood room
j(snow_js("r7s", C6, C7, 700))
j(f'tl.fromTo("#r7Dim",{{opacity:.2}},{{opacity:.55,duration:1.2}},{C6});')
j(f'tl.fromTo("#cloud7",{{opacity:0,y:-80,scale:.6,transformOrigin:"400px 820px"}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},{tMood - 0.15});')
j(f'document.querySelectorAll("#rain7 .drop").forEach((d,i)=>tl.fromTo(d,{{y:-10,opacity:0}},{{y:120,opacity:1,duration:0.45,ease:"none",repeat:7,delay:(i%3)*0.13}},{tMood}));')
j(f'tl.fromTo("#cloud7",{{x:-6}},{{x:6,duration:0.6,repeat:5,yoyo:true,ease:"sine.inOut"}},{tMood + 0.3});')
j(f'tl.set(["#sad7","#some7"],{{opacity:0}},0);pop("#some7",{tSome});pop("#sad7",{tSeas});')
j(f'tl.fromTo("#cd7",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tSeas + 0.2});')
# --- S8 17 trials
j(f'tl.fromTo("#pn8",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C7});')
j(f'document.querySelectorAll("#s8 .paper").forEach((p,i)=>tl.fromTo(p,{{scale:0,opacity:0,rotation:(i%2?12:-12)}},{{scale:1,opacity:1,rotation:0,duration:0.22,ease:"back.out(3)"}},{tSeven - 0.25}+i*0.045));')
j(f'tl.fromTo("#cnt8",{{innerText:0}},{{innerText:17,snap:{{innerText:1}},duration:0.8,ease:"power1.out"}},{tSeven - 0.25});'
  f'tl.fromTo("#cnt8",{{scale:1.5}},{{scale:1,duration:0.3,ease:"back.out(3)"}},{tTrials});')
j(f'tl.fromTo("#cd8",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tReview});')
# --- S9 lamp on, the win
j(snow_js("r9s", C8, C9, 700))
j(f'tl.fromTo("#r9Dim",{{opacity:.55}},{{opacity:.55,duration:0.05,immediateRender:false}},{C8});tl.to("#r9Dim",{{opacity:0,duration:0.25}},{tBright});')
j(f'tl.to("#r9LPanel",{{attr:{{fill:"#fffdf2"}},duration:0.06}},{tBright});tl.to("#r9LBeam",{{opacity:.55,duration:0.15}},{tBright});'
  f'tl.fromTo("#r9LBeam",{{opacity:.55}},{{opacity:.38,duration:0.25,repeat:3,yoyo:true}},{tBright + 0.2});')
j(f'tl.to("#r9Wall",{{background:"linear-gradient(#3a4a6e,#26334f)",duration:0.2}},{tBright});')
j(f'tl.set("#lBulb",{{opacity:1}},{tBright - 0.1});' + lot("lBulb", "bulb-2.json", tBright - 0.1, C9, loops=1))
j(f'tl.set("#tro",{{opacity:0}},0);pop("#tro",{tCame - 0.05});' + lot("tro", "trophy-1.json", tCame - 0.05, C9, loops=1))
j(f'tl.set("#win9",{{opacity:0}},0);tl.fromTo("#win9",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"power4.out"}},{tTop - 0.05});')
# --- S10 streetcar stop, payoff
j(snow_js("sn10", C9, C10))
j(f'tl.fromTo("#tramW",{{x:1100}},{{x:0,duration:0.9,ease:"power3.out"}},{C9 + 0.05});')
j(f'document.querySelectorAll("#s10 .wheel").forEach(w=>tl.fromTo(w,{{rotation:0}},{{rotation:-720,transformOrigin:"50% 50%",duration:0.9,ease:"power3.out"}},{C9 + 0.05}));')
j(f'tl.fromTo("#tram",{{rotation:0}},{{rotation:-1,svgOrigin:"510 700",duration:0.12,yoyo:true,repeat:1}},{C9 + 0.85});')
j(f'document.querySelectorAll("#s10 .tw").forEach((w,i)=>tl.to(w,{{fill:"#fff4c8",duration:0.2,repeat:3,yoyo:true}},{C9 + 1.2}+i*0.1));')
j(f'tl.set(["#ttc10","#ck1","#ck2","#sl10"],{{opacity:0}},0);pop("#ttc10",{tTTC - 0.05});tl.to("#ttc10",{{x:12,duration:0.05,repeat:5,yoyo:true}},{tVibe});')
j(f'tl.fromTo("#ck1",{{x:500,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"back.out(1.8)"}},{tCheck - 0.05});')
j(f'tl.fromTo("#ck2",{{x:500,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"back.out(1.8)"}},{tGet - 0.05});')
j(f'tl.fromTo("#sl10",{{scale:3,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-6,duration:0.22,ease:"power4.out"}},{tSay - 0.03});')
j(f'tl.set("#cd10",{{opacity:0}},0);tl.fromTo("#cd10",{{opacity:1,x:600}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{tNot - 0.05});'
  f'tl.to(["#ck1","#ck2","#sl10"],{{opacity:0,duration:0.2}},{tNot - 0.1});')
# cup set down for the serious line
j(f'tl.set("#cupTable",{{opacity:0}},0);tl.set("#cup",{{opacity:0}},{tNot - 0.05});tl.set("#cupTable",{{opacity:1}},{tNot - 0.05});tl.set("#cup",{{opacity:1}},{C10});tl.set("#cupTable",{{opacity:0}},{C10});')
# --- S11 outro
j(f'tl.fromTo("#pn11",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C10});')
j(f'tl.fromTo("#like11",{{scale:0,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.3,ease:"back.out(3)"}},{tLike});')
j(f'tl.fromTo("#sub11",{{scale:1}},{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},{tSub + 0.15});'
  f'tl.set("#subd11",{{opacity:0}},0);tl.set("#subd11",{{opacity:1}},{tSub + 0.25});tl.set("#sub11",{{opacity:0}},{tSub + 0.25});')
j(f'tl.fromTo("#src11",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{C10 + 0.2});')
# --- S12 loop frame = hook frame 0
j(f'tl.fromTo("#s12",{{opacity:0}},{{opacity:1,duration:0.18}},{C11});')
j(f'document.querySelectorAll("#h12City .win").forEach(w=>tl.set(w,{{opacity:0}},{C11 - 0.01}));')

CSS = f"""
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
.chip {{ position:absolute; font-family:InterBlack; letter-spacing:.03em; padding:10px 22px; border-radius:30px; border:5px solid #0c1622;
  box-shadow:0 6px 0 #0c1622; white-space:nowrap; opacity:0; color:#0c1622; }}
.stamp {{ position:absolute; font:120px InterBlack; color:#FF7A59; padding:6px 30px; border:12px solid #FF7A59; border-radius:24px;
  background:rgba(12,22,34,.85); transform:rotate(-8deg); opacity:0; letter-spacing:.02em; z-index:40; }}
.pin {{ position:absolute; transform:translate(-50%,-150%); background:#FF7A59; color:#0c1622; font:30px InterBlack; padding:6px 16px;
  border-radius:20px; border:5px solid #0c1622; box-shadow:0 5px 0 #0c1622; white-space:nowrap; }}
.blab {{ position:absolute; transform:translate(-50%,-120%); font:40px InterBlack; paint-order:stroke fill; -webkit-text-stroke:8px #0c1622; opacity:0; }}
.gap {{ position:absolute; transform:translate(-50%,-50%); }}
.gap span {{ display:block; background:#5AE68C; color:#0c1622; font:34px InterBlack; padding:8px 18px; border-radius:24px; border:5px solid #0c1622; box-shadow:0 5px 0 #0c1622; white-space:nowrap; }}
.flake {{ position:absolute; border-radius:50%; background:#FAF4E8; }}
.snowL {{ position:absolute; inset:0; pointer-events:none; }}
.tile {{ position:absolute; top:170px; width:185px; height:310px; border-radius:24px; background:#132b45; border:4px solid #24425f; opacity:0; }}
.tic {{ position:absolute; top:18px; width:100%; text-align:center; font:64px InterBlack; }}
.tname {{ position:absolute; top:100px; width:100%; text-align:center; font:28px InterBlack; color:#FAF4E8; }}
.tlow {{ position:absolute; top:252px; width:100%; text-align:center; font:30px InterBlack; color:#FF7A59; opacity:0; }}
.paper {{ position:absolute; width:96px; height:120px; border-radius:12px; background:#FAF4E8; border:5px solid #0c1622; box-shadow:0 6px 0 #0c1622; opacity:0; }}
.paper div {{ height:9px; margin:16px 14px 0; border-radius:5px; background:#9fb3c8; }}
.subbtn {{ position:absolute; left:150px; top:70px; width:580px; height:140px; border-radius:70px; border:7px solid #0c1622; box-shadow:0 10px 0 #0c1622;
  font:64px InterBlack; text-align:center; line-height:126px; }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-200px; width:400px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
{R.rig3_css()}
{C.CAP_CSS}
{C.V2_CSS}
{C.TR_CSS}
#cytoLayer {{ position:absolute; inset:0; z-index:20; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<script src="assets/lottie_svg.min.js"></script>
<script src="assets/three.min.js"></script>
<script src="assets/three3d.js"></script>
<style>{CSS}</style>
</head>
<body>
{GLOBAL_DEFS}
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="shaker" class="clip" data-start="0" data-duration="{T}"><div id="cam">
{scene_html}
  <div id="cytoLayer">{R.rig3_html("outfit_puffer", "cup_red")}</div>
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
    if not os.path.exists(f): shutil.copy(f"/home/claude/hf/template/{f}", f)
if not os.path.exists("node_modules"): os.symlink("../node_modules", "node_modules")
print("built", len(html), "bytes; T", T, "words", len(WORDS), "voice", round(TM["total"], 2))
