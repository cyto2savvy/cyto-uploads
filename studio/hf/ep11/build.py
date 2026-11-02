"""EP11 — Is Your Diwali Food Coma Actually the Sweets? (6ixty Seconds of Science). Scarborough-led.
v2 layout + v3 rig + art.py 2D + three3d.js 3D.  python3 build.py -> index.html + assets/audio.wav"""
import json, sys, os, subprocess, random, shutil
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import numpy as np
import cytohf as C, cyto3 as R, art as A
from engine import tone, noise, hp, lp, add, load_mono, SR

P = "/home/claude/hf/ep11"; os.chdir(P)
V = "/home/claude/ep11"
TM = json.load(open(f"{V}/timing.json")); WORDS = TM["words"]
W, H = 1080, 1920


def wt(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and w["w"].lower().strip(".,?!:").startswith(word.lower()):
            return round(w["t0"], 3)
    raise KeyError(word)


# ------------------------------------------------------------------ word beats
tDiwali, tFeast, tDead, tCouch, tBlame, tMithai, tNah = wt("Diwali"), wt("feast"), wt("dead"), wt("couch"), wt("Blame"), wt("mithai"), wt("Nah")
tYo, tCyto, tLive, t6ix, tInside = wt("Yo", 4), wt("Cyto"), wt("live"), wt("6ix"), wt("inside")
tEvery, tCarbs, tKnock, tAhlie = wt("Everyone"), wt("carbs"), wt("knock"), wt("ahlie")
tSleep, tLab, tFat, tCarb, tMixed, tMeals = wt("sleep"), wt("lab"), wt("high-fat"), wt("high-carb"), wt("mixed"), wt("meals")
tNo, tDiff, tFell, tWhat, tMatter = wt("No"), wt("difference"), wt("fell"), wt("What"), wt("matter")
tEating, tSolid, tMeal, tComp, tWater = wt("Eating"), wt("solid"), wt("meal", 18), wt("compared"), wt("water")
tAnd, tImmune, tMess, tIL1, tTired, tBig, tStyll = wt("And", 21), wt("immune"), wt("messenger"), wt("IL-1"), wt("tired"), wt("big"), wt("styll")
tSo, tBlame2, tMithai2, tFull, tStom, tPlus, tBare, tSig = wt("So", 26.9), wt("blame", 26), wt("mithai", 26), wt("full"), wt("stomach"), wt("plus"), wt("bare"), wt("signals")
tThe, tCouch2, tNap, tEarned, tSay, tLess, tNot = wt("The", 30.5), wt("couch", 30), wt("nap"), wt("earned"), wt("say", 32), wt("less"), wt("Not")
tLike, tSub, tHappy, tFam = wt("Like"), wt("subscribe"), wt("happy"), wt("fam")
END_V = WORDS[-1]["t1"]

C1, C2, C3, C4, C5, C6 = 2.55, 4.18, 8.42, 10.80, 14.36, 17.58
C7, C8, C9, C10, C11 = 21.28, 23.80, 26.86, 30.98, 34.45
SIPS = [(round(END_V + 0.05, 2), 0.62)]
C12 = round(SIPS[0][0] + SIPS[0][1] + 0.05, 2)
T = round(C12 + 0.55, 2)

# ------------------------------------------------------------------ assets
LOTS = ["fireworks-1.json", "fireworks-2.json", "diya-1.json", "diya-2.json", "zzz-a.json", "rangoli-1.json"]
C.copy_assets_v2(P, lotties=LOTS)
for f in ("outfit_kurta.png",):
    shutil.copy(f"/home/claude/cyto2/rig/{f}", "assets/")
shutil.copy("/home/claude/hf/node_modules/three/build/three.min.js", "assets/")
shutil.copy("/home/claude/hf/three3d.js", "assets/")


# ------------------------------------------------------------------ audio: warm festive lo-fi; bells on the Diwali beats
def rhodes(m, dur):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.02) * np.exp(-t / 1.5)
    trem = 1 + 0.14 * np.sin(2 * np.pi * 4.0 * t)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t / .3)) * env * trem * 0.06


def bell(f0, dur=1.2, g=0.12):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f0 * t) + .5 * np.sin(2 * np.pi * f0 * 2.76 * t) * np.exp(-t / .2)) * np.exp(-t / .5) * g


def tabla(f0=180, g=0.5):   # pitched membrane hit (generic, synthesized)
    t = np.arange(int(0.35 * SR)) / SR
    f = f0 * (1 + 0.6 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12) * g


def make_audio(sfx_events):
    n = int((T + 0.3) * SR); music = np.zeros(n, np.float32); drums = np.zeros(n, np.float32)
    BEAT = 60 / 92; BAR = BEAT * 4
    chords = [[62, 65, 69, 72], [58, 62, 65, 69], [60, 64, 67, 70], [57, 60, 64, 67]]   # Dm7 Bbmaj7 C7 Am7
    t = 0.0; i = 0
    while t < T + 0.3:
        for k, m in enumerate(chords[i % 4]): add(music, rhodes(m, BAR + 0.4), t + k * 0.014)
        add(music, rhodes(chords[i % 4][0] - 12, BAR) * 1.5, t)
        t += BAR; i += 1
    kick = tone(120, 45, 0.35, 0.12) * 0.8
    hat = hp(noise(0.04, 2), 0.6) * np.exp(-np.arange(int(0.04 * SR)) / SR / 0.01) * 0.13
    ta, tb = tabla(190, .32), tabla(320, .22)
    t = C2; s = 0
    while t < T + 0.3:
        quiet = (tNot - 0.1 <= t < C11 - 0.05)
        if not quiet:
            p = s % 8
            if p in (0, 5): add(drums, kick, t)
            if p in (2, 6): add(drums, ta, t)
            if p in (3, 7): add(drums, tb, t + 0.04)
            add(drums, hat, t + (0.06 if s % 2 else 0), 0.9 if s % 2 == 0 else 0.5)
        t += BEAT / 2; s += 1
    rnd = np.random.default_rng(11); crackle = np.zeros(n, np.float32)
    for p_ in rnd.integers(0, n - 200, 800): crackle[p_:p_ + 60] += rnd.uniform(-1, 1) * np.exp(-np.arange(60) / 10) * 0.05
    music = lp(music, 0.35) + crackle * 0.6
    a = int(C2 * SR); music[:a] = lp(music[:a], 0.1) * 1.7
    a, b = int(C10 * SR), int(C11 * SR); music[a:b] = lp(music[a:b], 0.08) * 1.7          # couch nap: sleepy, muffled
    music += drums
    v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.55 * np.clip(env * 3, 0, 1)); music *= 0.42
    S = {
        "whoosh": lp(noise(0.4, 3), 0.25) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))) ** 2 * 0.45,
        "boom": tone(90, 35, 0.9, 0.35) * 0.8,
        "pop": tone(1200, 380, 0.08, 0.03) * 0.3,
        "ding": (tone(1760, 1760, 0.6, 0.18) + 0.5 * tone(2640, 2640, 0.6, 0.12)) * 0.2,
        "rise": np.sin(2 * np.pi * np.cumsum(np.linspace(300, 900, int(0.6 * SR))) / SR) * np.linspace(0, 1, int(0.6 * SR)) * 0.06,
        "fall": np.sin(2 * np.pi * np.cumsum(np.linspace(900, 250, int(0.5 * SR))) / SR) * np.linspace(1, 0, int(0.5 * SR)) * 0.07,
        "click": tone(2200, 900, 0.05, 0.015) * 0.35,
        "sparkle": sum(bell(f, 1.0, 0.07) for f in (1568, 2093, 2637)),
        "firework": lp(noise(0.8, 4), 0.5) * np.exp(-np.arange(int(0.8 * SR)) / SR / 0.25) * 0.18,
        "ding2": bell(1320, 0.9, 0.14),
        "flop": tone(160, 70, 0.3, 0.12) * 0.7,
        "elev": bell(988, 0.9, 0.16),
        "slot": tone(700, 300, 0.12, 0.04) * 0.4,
    }
    sfx = np.zeros(n, np.float32)
    for kind, tt in sfx_events: add(sfx, S[kind], tt)
    mix = music + sfx; mix[:m] += v[:m]
    mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[: int(T * SR)]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/raw_mix.wav"],
                   input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/raw_mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "assets/base.wav"], check=True)


SFX = [("sparkle", tDiwali), ("firework", 0.6), ("flop", tDead + 0.05), ("boom", tCouch), ("pop", tMithai), ("boom", tNah),
       ("firework", C2 + 0.3), ("pop", tLive), ("boom", t6ix), ("pop", tInside), ("pop", tCarbs), ("boom", tKnock + 0.1), ("pop", tAhlie),
       ("pop", tFat), ("pop", tCarb), ("pop", tMixed), ("ding", tDiff), ("fall", tWhat + 0.1), ("pop", tSolid), ("ding", tWater),
       ("elev", C7 + 0.12), ("pop", tMess), ("boom", tIL1), ("slot", C8 + 1.35), ("rise", tTired), ("pop", tStyll),
       ("pop", tStom), ("pop", tSig), ("boom", tSig + 0.3), ("flop", C10 + 0.1), ("boom", tEarned), ("ding", tSay), ("pop", tNot),
       ("pop", tLike), ("click", tSub + 0.15), ("sparkle", tHappy), ("firework", tHappy + 0.2), ("ding2", C12)]
SFX += [("whoosh", c - 0.18) for c in (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11)]
make_audio(SFX)

# ------------------------------------------------------------------ Cyto: positions + acting
POS_HOOK, POS_BIG, POS_V2 = C.place(330, 1335, 0.60), C.place(330, 1300, 0.64), C.CYTO_V2
POS_COUCH = C.place(330, 1230, 0.60)
mouth = R.viseme_track(f"{V}/voice.wav", WORDS)
if mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
blinks = [(t, 0.1) for t in (2.0, 5.6, 9.0, 12.4, 15.9, 19.2, 22.6, 25.2, 28.0, 33.0, 35.6)]
gest = dict(sips=SIPS, raises=[(tCyto, 0.6), (tEarned - 0.1, 0.7)], waves=[tYo, tHappy - 0.05],
            points=[(tFat - 0.05, 0.7), (tSolid - 0.05, 0.8), (tIL1 - 0.05, 0.8), (tStom - 0.05, 0.7)],
            tilts=[(tAhlie, 0.6, 8), (tStyll, 0.7, -8), (tLess, 0.5, -6)],
            shrugs=[(tNah, 0.5), (tWhat, 0.6)])
expr = [(tDead - 0.05, 0.9, "shock"), (tBlame - 0.05, 0.5, "skeptic"), (tNah - 0.05, 0.5, "hype"), (tCyto - 0.05, 0.5, "hype"), (t6ix, 0.5, "hype"),
        (tEvery, 1.6, "skeptic"), (tSleep, 0.8, "squint"), (tDiff - 0.05, 0.8, "shock"), (tSolid - 0.05, 0.7, "hype"),
        (tIL1 - 0.05, 0.7, "shock"), (tTired, 1.2, "squint"), (tBlame2 - 0.05, 0.6, "skeptic"), (tSig - 0.05, 0.5, "hype"),
        (C10 + 0.05, 0.9, "squint"), (tEarned - 0.05, 0.6, "hype"), (tNot - 0.05, 1.0, "squint"), (tHappy - 0.05, 0.9, "hype")]
looks = [(C4 + 0.3, 6, -6), (C5 + 0.3, 6, -6), (C7 + 0.3, 6, -5), (C9 + 0.4, 6, -6)]
rig_js = R.rig3_js(mouth, T, blinks=blinks, mute=[(s[0], 0) for s in SIPS], expr=expr, looks=looks, **gest)
R.mix_sips("assets/base.wav", [s[0] for s in SIPS], "assets/audio.wav")

# ------------------------------------------------------------------ captions + transitions
KEYS = {"diwali": "#FFD166", "feast": "#FFD166", "dead": "#FF7A59", "couch": "#c4b0ff", "mithai": "#f5a524", "nah": "#FF7A59",
        "carbs": "#f5a524", "ahlie": "#3fc1b0", "sleep": "#c4b0ff", "highfat": "#FFD166", "highcarb": "#f5a524", "mixed": "#3fc1b0",
        "difference": "#FF7A59", "solid": "#5AE68C", "meal": "#5AE68C", "water": "#9fc3e8", "immune": "#c4b0ff", "messenger": "#c4b0ff",
        "il1": "#FF7A59", "tired": "#c4b0ff", "styll": "#3fc1b0", "stomach": "#f5a524", "signals": "#c4b0ff", "earned": "#5AE68C",
        "say": "#3fc1b0", "less": "#3fc1b0", "subscribe": "#FF7A59", "fam": "#FFD166"}
CAPW = [w for w in WORDS if not (tLive - 0.01 <= w["t0"] < C3)]
cap_html, cap_js = C.captions(CAPW, KEYS, y=C.CAP_Y_V2)
last_cap = cap_html.count('"cap clip"') - 1
cap_js += f'\ntl.set("#cap{last_cap}",{{opacity:0}},{C12});'
import re as _re
_m = [m for m in _re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'CYTO,' in m.group(2)][0]
cap_js += f'\ntl.set("#{_m.group(1)}",{{opacity:1}},0);tl.set("#{_m.group(1)}",{{opacity:0}},{tLive - 0.03});'
TRS = [C.transition(k, t) for k, t in (("whip", C1), ("zoom", C2), ("membrane", C3), ("doors", C4), ("zoom", C5), ("whip", C6),
                                        ("doors", C7), ("whip", C8), ("membrane", C9), ("zoom", C10), ("whip", C11))]
tr_html = "\n".join(h for h, _ in TRS); tr_js = "\n".join(j for _, j in TRS)


# ------------------------------------------------------------------ helpers
def chip(id_, text, left, top, bg="#FFD166", fg=A.INK, size=34, extra=""):
    return f'<div id="{id_}" class="chip" style="left:{left}px;top:{top}px;background:{bg};color:{fg};font-size:{size}px;{extra}">{text}</div>'


def snow(idp, n=40, seed=1, top=0, height=1500, size=(6, 14)):
    rnd = random.Random(seed)
    return "".join(f'<div class="flake {idp}" data-v="{rnd.uniform(2.6, 5.0):.2f}" style="left:{rnd.uniform(0, W):.0f}px;top:{top + rnd.uniform(-height, 0):.0f}px;'
                   f'width:{(s := rnd.uniform(*size)):.0f}px;height:{s:.0f}px;opacity:{rnd.uniform(.4, .95):.2f}"></div>' for _ in range(n))


def snow_js(idp, t0, t1, height=1700):
    return (f'document.querySelectorAll(".{idp}").forEach((f,i)=>{{const v=+f.dataset.v;'
            f'tl.fromTo(f,{{y:0,x:0}},{{y:{height},x:(i%2?40:-40),duration:v,ease:"none",repeat:Math.ceil({t1 - t0:.2f}/v)}},{t0:.2f});}});')


def lot(id_, file, t0, t1, loops=1, offset=0, ease="none"):
    data = open(f"{P}/assets/{file}").read(); v = id_.replace("-", "_")
    return (f'const L_{v}=lottie.loadAnimation({{container:document.getElementById("{id_}"),renderer:"svg",loop:false,autoplay:false,animationData:{data}}});'
            f'const P_{v}={{f:0}};tl.fromTo(P_{v},{{f:0}},{{f:L_{v}.totalFrames*{loops}-0.01,duration:{t1 - t0:.3f},ease:"{ease}",'
            f'onUpdate:()=>L_{v}.goToAndStop(({offset}+P_{v}.f) % L_{v}.totalFrames,true)}},{t0:.3f});')


def zzz(id_, left, top, size=240):
    """Native SVG 'Z z Z' (the zzz Lottie's PNG layers don't survive the HyperFrames render)."""
    zs = "".join(f'<text class="zq" x="{x}" y="{y}" font-family="InterBlack" font-size="{fs}" fill="#c4b0ff" stroke="#0c1622" stroke-width="{fs * .12:.0f}" paint-order="stroke">Z</text>'
                 for x, y, fs in ((20, 220, 70), (90, 150, 95), (170, 80, 125)))
    return f'<div id="{id_}" class="lot" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px"><svg viewBox="0 0 260 260" width="{size}" height="{size}" style="overflow:visible">{zs}</svg></div>'


def zzz_js(id_, t0, t1):
    n = max(1, int((t1 - t0) / 1.2) + 1)
    return (f'document.querySelectorAll("#{id_} .zq").forEach((z,i)=>tl.fromTo(z,{{y:30,opacity:0,scale:.6,transformOrigin:"50% 50%"}},'
            f'{{keyframes:[{{y:0,opacity:1,scale:1,duration:0.35}},{{y:-30,opacity:0,duration:0.6,delay:0.2}}],repeat:{n},repeatDelay:0.05,ease:"sine.out"}},{t0:.3f}+i*0.22));')


def burst(id_, left, top, size=320, cols=("#FFD166", "#FF7A59", "#c4b0ff")):
    """Native SVG firework bursts (three staggered rings of sparks)."""
    import math as _m
    rings = []
    for k, (cx, cy, r, c) in enumerate(((130, 120, 90, cols[0]), (230, 210, 70, cols[1]), (70, 230, 60, cols[2]))):
        sp = "".join(f'<path d="M{cx + r * .35 * _m.cos(a):.0f} {cy + r * .35 * _m.sin(a):.0f} L{cx + r * _m.cos(a):.0f} {cy + r * _m.sin(a):.0f}" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
                     for a in [2 * _m.pi * i / 14 for i in range(14)])
        rings.append(f'<g class="fwr" style="transform-origin:{cx}px {cy}px">{sp}<circle cx="{cx}" cy="{cy}" r="9" fill="{c}"/></g>')
    return f'<div id="{id_}" class="lot" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px"><svg viewBox="0 0 300 300" width="{size}" height="{size}" style="overflow:visible">{"".join(rings)}</svg></div>'


def burst_js(id_, t0, t1, still=False):
    if still:
        return f'document.querySelectorAll("#{id_} .fwr").forEach((g,i)=>tl.set(g,{{scale:[.9,.5,.3][i],opacity:[.9,.6,.4][i]}},0));'
    n = max(1, int((t1 - t0) / 1.0))
    return (f'document.querySelectorAll("#{id_} .fwr").forEach((g,i)=>tl.fromTo(g,{{scale:0.1,opacity:1}},'
            f'{{scale:1.15,opacity:0,duration:0.95,ease:"power2.out",repeat:{n},repeatDelay:0.05}},{t0:.3f}+i*0.33));')


def three(var, factory, canvas_id, t0, t1, opts="{}"):
    return (f'const {var}=C3D.{factory}(document.getElementById("{canvas_id}"),{opts});const P{var}={{t:0}};{var}.render(0);'
            f'tl.fromTo(P{var},{{t:0}},{{t:{t1 - t0:.3f},duration:{t1 - t0:.3f},ease:"none",onUpdate:()=>{var}.render(P{var}.t)}},{t0:.3f});')


def svg(inner):
    return f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">{inner}</svg>'


# ------------------------------------------------------------------ scenes
def hook_bg(idp):
    """Scarborough condo towers at dusk (STC area), TTC-style bus on an arterial, balcony of diyas (+ raccoon)."""
    return f'''<div class="bgfill" style="background:linear-gradient(#1d2a55 0%,#6a3f7a 40%,#e0785a 66%,#ffc27a 78%)"></div>
{svg(f"""<g id="{idp}Stars">{A.stars(W, H, 30, 12, .3)}</g>
 <g id="{idp}City">{A.scarb_skyline(W, 900, 1.0, seed=11, lit=.45, ground="#141c30")}</g>
 <rect x="-20" y="905" width="1120" height="70" fill="#2a3346"/><path d="M0 940 H1080" stroke="#e8e0cc" stroke-width="5" stroke-dasharray="40 30"/>
 <g id="{idp}Bus" transform="translate(1200,0)">{A.night_bus(0, 735, .62, sign="KENNEDY STN")}</g>
 <rect x="-20" y="975" width="1120" height="1000" fill="#141c30"/>
 <g transform="translate(0,90)">{A.balcony(20, 1040, 1040, n_diya=6, raccoon=True)}</g>""")}
{burst(idp + "Fw", 620, 520, 340)}'''


S1 = hook_bg("h1") + '''
<div id="t1a" class="big" style="top:220px;font-size:132px;color:#FFD166">DIWALI<br>FEAST</div>
<div id="t1b" class="big" style="top:230px;font-size:150px;color:#c4b0ff">FOOD<br>COMA</div>'''

S1B = f'''<div class="bgfill" style="background:linear-gradient(#3a2a4a,#24182e)"></div>
{svg(f"""{A.bluffs_view(110, 230, 860, 520, "bv1")}
 <rect x="110" y="230" width="860" height="520" fill="none" stroke="#f4f4ef" stroke-width="22"/><path d="M540 230 V750" stroke="#f4f4ef" stroke-width="16"/>
 <rect x="80" y="750" width="920" height="26" rx="8" fill="#e7e2d6" stroke="{A.INK}" stroke-width="6"/>
 <rect x="-20" y="990" width="1120" height="940" fill="#4a2f3a"/><rect x="-20" y="990" width="1120" height="22" fill="#6b4450"/>""")}
<div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px">{svg(A.mithai_plate(770, 1090, 1.0, "mp1"))}</div>
<div id="dy1" class="lot" style="left:800px;top:1200px;width:180px;height:180px"></div>
<div id="q1" class="big" style="top:300px;font-size:200px;color:#f5a524">?</div>
<div id="nah1" class="stamp" style="left:300px;top:330px">NAH.</div>'''

S2 = f'''<div class="bgfill" style="background:linear-gradient(#0a1024 0%,#1b2650 70%,#3a3f6b 85%)"></div>
{svg(f"""{A.stars(W, H, 50, 21, .45)}<g id="h2City">{A.scarb_skyline(W, 1000, 1.05, seed=23, lit=.5, ground="#0c1622")}</g>
 {A.balcony(570, 1060, 380, n_diya=3, raccoon=True)}""")}
{burst("fw2", 240, 200, 600)}
{burst("fw2b", 60, 690, 220, ("#3fc1b0", "#FFD166", "#e0457b"))}
<div id="t2a" class="big" style="top:230px;font-size:180px;color:#FFD166"><span style="font-size:74px;color:#FAF4E8">LIVE FROM</span><br>THE 6IX</div>
{chip("t2c", "...INSIDE YOUR BODY", 300, 600, bg="#FF7A59", size=40)}'''

S3 = f'''<div class="navy"></div><div id="dots3" class="dots"></div>
<div id="pn3" class="panel"><div class="ptitle">THE MYTH</div>
 {svg(f"""<g transform="translate(220,470)"><g id="rice3"><path d="M-150 0 Q0 190 150 0Z" fill="#cfd5dc" stroke="{A.INK}" stroke-width="8"/>
  {''.join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="9" fill="#FAF4E8" stroke="#c9c2b0" stroke-width="2"/>' for x, y in ((-110, -6), (-80, -22), (-50, -8), (-20, -28), (10, -10), (40, -26), (70, -8), (100, -18), (-65, -42), (-5, -48), (55, -40)))}
  <path d="M-160 0 H160" stroke="{A.INK}" stroke-width="8"/></g></g>
  <g transform="translate(300,540)"><g id="naan3"><ellipse cx="0" cy="0" rx="120" ry="56" fill="#f2c27a" stroke="{A.INK}" stroke-width="7" transform="rotate(-18)"/>
  {''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#b9772e"/>' for x, y in ((-50, 6), (-10, -18), (30, -6), (60, -30), (-30, -30)))}</g></g>""")}
 {zzz("z3", 60, 70, 260)}
</div>
<div id="t3" class="big" style="top:330px;left:470px;width:480px;font-size:110px;color:#f5a524">CARBS<br>= KO?</div>
<div id="cd3" class="card"><h3>THE MYTH</h3><p>Carbs are what knock you out.</p></div>'''

S4 = f'''<div class="bgfill" style="background:linear-gradient(#22324a,#182436)"></div>
{svg(f"""{A.platform_view(560, 220, 400, 420, "pv4")}
 <rect x="560" y="220" width="400" height="420" fill="none" stroke="#e8edf2" stroke-width="20"/>
 <g id="bus4" transform="translate(-700,0)">{A.night_bus(560, 545, .34, sign="KENNEDY STN")}</g>
 <rect x="530" y="640" width="460" height="22" rx="8" fill="#e8edf2" stroke="{A.INK}" stroke-width="6"/>
 <rect x="-20" y="1000" width="1120" height="940" fill="#2a3a52"/>
 <g id="bed4"><rect x="40" y="560" width="440" height="140" rx="30" fill="#e8edf2" stroke="{A.INK}" stroke-width="8"/>
  <rect x="60" y="520" width="140" height="70" rx="26" fill="#FAF4E8" stroke="{A.INK}" stroke-width="6"/>
  <rect x="40" y="700" width="20" height="120" fill="#9aa3ab"/><rect x="460" y="700" width="20" height="120" fill="#9aa3ab"/>
  <g id="eeg4" transform="translate(330,262) scale(.42)"><rect x="60" y="250" width="400" height="200" rx="20" fill="#0f2236" stroke="{A.INK}" stroke-width="7"/>
  <path id="eegL" d="M80 350 l20 -30 l20 50 l20 -60 l20 70 l20 -40 l20 20 l20 -30 l20 50 l20 -60 l20 70 l20 -40 l20 20 l20 -30 l20 50 l20 -30 l20 20 l20 -10" fill="none" stroke="#5AE68C" stroke-width="6"/></g></g>""")}
<div id="t4" class="big" style="top:290px;left:40px;width:340px;font-size:84px;color:#c4b0ff;opacity:0">SLEEP<br>LAB</div>
{chip("c4a", "HIGH-FAT", 70, 250, bg="#FFD166", size=40)}
{chip("c4b", "HIGH-CARB", 70, 345, bg="#f5a524", size=40)}
{chip("c4c", "MIXED", 70, 440, bg="#3fc1b0", size=40)}
<div id="cd4" class="card"><h3>ORR 1997 · SLEEP LAB</h3><p>10 healthy men per test, nap after lunch.</p></div>'''

S5 = f'''<div class="navy"></div><div id="dots5" class="dots"></div>
<div id="pn5" class="panel"><div class="ptitle">HOW FAST THEY FELL ASLEEP</div>
 <canvas id="cvB5" width="880" height="650" style="position:absolute;left:0;top:0"></canvas>
 <div id="lb5a" class="blab" style="color:#FFD166">FAT</div><div id="lb5b" class="blab" style="color:#f5a524">CARB</div><div id="lb5c" class="blab" style="color:#3fc1b0">MIXED</div>
 <div id="eq5" class="big" style="top:110px;width:880px;font-size:130px;color:#FF7A59">=&nbsp;=</div>
 <div id="q5" class="big" style="top:150px;width:880px;font-size:240px;color:#FFD166">?</div>
</div>
<div id="same5" class="stamp" style="left:330px;top:600px;font-size:96px">SAME</div>
<div id="cd5" class="card"><h3>ORR 1997</h3><p>Fat vs carb vs mixed: no real difference.</p></div>'''

S6 = f'''<div class="navy"></div><div id="dots6" class="dots"></div>
<div id="pn6" class="panel"><div class="ptitle">TIME TO FALL ASLEEP</div>
 <canvas id="cvB6" width="880" height="650" style="position:absolute;left:0;top:0"></canvas>
 <div id="lb6a" class="blab" style="color:#5AE68C">SOLID MEAL</div><div id="lb6b" class="blab" style="color:#9fc3e8">WATER</div>
 <div id="gap6" class="gap"><span>MEAL = ASLEEP FASTER</span></div>
 <div id="cupW" style="position:absolute;left:690px;top:80px">{svg('<path d="M10 10 h110 l-14 150 h-82z" fill="#9fc3e8" opacity=".6" stroke="#0c1622" stroke-width="7"/><path d="M14 50 h102" stroke="#cfe0ff" stroke-width="6"/>').replace(f'width="{W}" height="{H}"', 'width="140" height="180"')}</div>
</div>
<div id="cd6" class="card"><h3>ORR 1997</h3><p>A solid meal beat the same amount of water.</p></div>'''

HALL = A.hallway(W, 1000, "hw")
cells = "".join(A.il1_cell(0, 0, .9, f"m{k}") for k in range(3))
S7 = f'''<div class="bgfill" style="background:#c9b99a"></div>
{svg(f'<g id="hall7" transform="translate(0,-170)">{HALL}</g><g id="cells7">{cells}</g>')}
<div id="t7" class="big" style="top:200px;left:440px;width:640px;left:0;font-size:150px;color:#FF7A59">IL-1</div>
<div id="cd7" class="card"><h3>LEHRSKOV 2018</h3><p>IL-1: an immune messenger molecule.</p></div>'''

cells8 = "".join(A.il1_cell(0, 0, .9, f"n{k}") for k in range(3))
S8 = f'''<div class="bgfill" style="background:#c9b99a"></div>
{svg(f'<g id="hall8" transform="translate(-560,-420) scale(1.55)">{A.hallway(W, 1000, "hx")}</g><g id="cells8">{cells8}</g>'
     f'<g id="env8"><rect x="-60" y="-36" width="120" height="72" rx="8" fill="#FAF4E8" stroke="{A.INK}" stroke-width="6"/><path d="M-60 -36 L0 6 L60 -36" fill="none" stroke="{A.INK}" stroke-width="5"/>'
     f'<text x="0" y="28" text-anchor="middle" font-family="InterBlack" font-size="26" fill="#7a5cc7">zzz</text></g>')}
<div id="meter8" style="position:absolute;left:80px;top:250px;width:290px;height:120px">
 <div style="position:absolute;left:0;top:0;font:38px InterBlack;color:#0c1622">TIRED</div>
 <div style="position:absolute;left:0;top:56px;width:280px;height:46px;border-radius:24px;background:#FAF4E8;border:6px solid #0c1622;overflow:hidden">
  <div id="meterF" style="position:absolute;left:0;top:0;height:100%;width:100%;background:linear-gradient(90deg,#c4b0ff,#7a5cc7);transform-origin:0 50%;transform:scaleX(0.1)"></div></div></div>
<div id="cd8" class="card"><h3>LEHRSKOV 2018 · RCT</h3><p>Blocking IL-1 cut post-meal tiredness (8 lean + 8 obese men).</p></div>'''

S9 = f'''<div class="bgfill" style="background:linear-gradient(#3a2a4a,#24182e)"></div>
{svg(f"""{A.bluffs_view(110, 230, 860, 520, "bv9")}
 <rect x="110" y="230" width="860" height="520" fill="none" stroke="#f4f4ef" stroke-width="22"/><path d="M540 230 V750" stroke="#f4f4ef" stroke-width="16"/>
 <rect x="80" y="750" width="920" height="26" rx="8" fill="#e7e2d6" stroke="{A.INK}" stroke-width="6"/>
 <rect x="-20" y="990" width="1120" height="940" fill="#4a2f3a"/>""")}
<div id="pn9" class="panel" style="background:rgba(15,34,54,.94)"><div class="ptitle">THE REAL COMBO</div>
 {svg(f'''<g id="mp9w" transform="translate(-170,-650)">{A.mithai_plate(440, 1000, .8, "mp9")}</g>
  <g id="x9" opacity="0"><path d="M150 230 L380 430 M380 230 L150 430" stroke="#FF7A59" stroke-width="30" stroke-linecap="round"/></g>
  <g id="st9w" opacity="0">{A.stomach(150, 330, 1.0, "st9")}</g>
  <text id="pl9" x="330" y="370" text-anchor="middle" font-family="InterBlack" font-size="110" fill="#FAF4E8" opacity="0">+</text>
  <g id="ce9w" opacity="0">{A.il1_cell(470, 360, 1.25, "q9")}</g>
  <text id="eq9" x="610" y="370" text-anchor="middle" font-family="InterBlack" font-size="110" fill="#FAF4E8" opacity="0">=</text>''')}
 <div id="z9w" style="position:absolute;left:0;top:0;opacity:0">{zzz("z9", 650, 210, 200)}</div>
 <div id="lbS9" class="chip" style="left:60px;top:520px;font-size:30px;background:#f5a524">FULL STOMACH</div>
 <div id="lbI9" class="chip" style="left:380px;top:520px;font-size:30px;background:#c4b0ff">IMMUNE SIGNALS</div>
</div>
<div id="cd9" class="card"><h3>BOTH STUDIES</h3><p>A big meal + IL-1 signals, not the sugar.</p></div>'''

S10 = f'''<div class="bgfill" style="background:linear-gradient(#1c2340,#121a2e)"></div>
{svg(f"""<rect x="560" y="220" width="400" height="460" fill="#0b1630"/>
 <g clip-path="url(#wc10)"><clipPath id="wc10"><rect x="560" y="220" width="400" height="460"/></clipPath>
 <g transform="translate(470,10) scale(.55)">{A.scarb_skyline(1000, 1200, 1.0, seed=31, lit=.6, ground="#e8eef5", mall=False)}</g></g>
 <rect x="560" y="220" width="400" height="460" fill="none" stroke="#f4f4ef" stroke-width="20"/><path d="M760 220 V680" stroke="#f4f4ef" stroke-width="14"/>
 <rect x="530" y="680" width="460" height="22" rx="8" fill="#e7e2d6" stroke="{A.INK}" stroke-width="6"/>
 {A.diya(620, 676, .8)}{A.diya(900, 676, .8)}
 <rect x="-20" y="1080" width="1120" height="900" fill="#3a2a3a"/>
 <g transform="translate(540,1250) scale(1,.42) translate(-540,-1250)">{A.rangoli(540, 1250, 330, "rg10")}</g>
 {A.couch(130, 900, 820, "cc10")}""")}
<div class="snowW" style="position:absolute;left:560px;top:220px;width:400px;height:460px;overflow:hidden">{snow("s10", 26, 5, 0, 600, (5, 10))}</div>
{zzz("z10", 330, 560, 260)}
<div id="rgL" class="lot" style="left:760px;top:1240px;width:200px;height:200px"></div>
<div id="er10" class="stamp" style="left:90px;top:320px;font-size:100px;color:#5AE68C;border-color:#5AE68C">EARNED</div>
<div id="sl10" class="stamp" style="left:90px;top:320px;font-size:100px">SAY LESS</div>
<div id="cd10" class="card" style="border-left-color:#3fc1b0"><h3 style="color:#188076">HEADS UP</h3><p>Not medical advice. Ask a doctor or pharmacist.</p></div>'''

shops = "".join(f'<rect x="{x}" y="640" width="{w}" height="360" fill="{c}" stroke="{A.INK}" stroke-width="6"/>'
                f'<path d="M{x} 640 h{w} l-20 60 h{-(w - 40)}z" fill="{aw}" stroke="{A.INK}" stroke-width="5"/>'
                f'<rect x="{x + 30}" y="760" width="{w - 60}" height="160" fill="#ffe7a3" opacity=".75" stroke="{A.INK}" stroke-width="5"/>'
                for x, w, c, aw in ((-20, 300, "#7a3b5a", "#f57c1f"), (280, 260, "#3b5a7a", "#e0457b"), (540, 280, "#5a7a3b", "#FFD166"), (820, 300, "#7a5a3b", "#3fc1b0")))
S11 = f'''<div class="bgfill" style="background:linear-gradient(#0a1024 0%,#1d2a55 60%,#3a3f6b 100%)"></div>
{svg(f"""{A.stars(W, H, 40, 41, .3)}{shops}
 {A.string_lights(W, 600, 18, 50, "slA", 5)}{A.string_lights(W, 520, 16, 40, "slB", 9)}
 <rect x="-20" y="1000" width="1120" height="940" fill="#1a2236"/><path d="M0 1080 H1080" stroke="#e8e0cc" stroke-width="5" stroke-dasharray="40 30"/>""")}
{burst("fw11", 660, 1300, 280)}
<div id="pn11" class="panel" style="top:220px;height:600px">
 <div id="sub11" class="subbtn" style="background:#FF7A59;color:#0c1622">SUBSCRIBE</div>
 <div id="subd11" class="subbtn" style="background:#3a4a5e;color:#FAF4E8;opacity:0;font-size:60px">SUBSCRIBED ✓</div>
 <div id="like11" style="position:absolute;left:760px;top:70px;font:110px InterBlack;opacity:0">👍</div>
 <div style="position:absolute;left:40px;top:270px;font:30px InterBlack;color:#FFD166;letter-spacing:.05em">SOURCES</div>
 <div id="src11" style="position:absolute;left:40px;top:320px;width:800px;font:25px/1.45 InterSB;color:#cfe0ff">
  Orr et al. 1997 · Physiol Behav<br>Lehrskov et al. 2018 · Mol Metab<br>
  <span style="color:#96b0c4">Links in the description · Not medical advice</span></div>
</div>
<div id="hd11" class="big" style="top:1090px;left:470px;width:520px;font-size:84px;color:#FFD166">HAPPY<br>DIWALI</div>'''

S12 = hook_bg("h12")

scenes = [("s1", 0, C1, S1), ("s1b", C1, C2, S1B), ("s2", C2, C3, S2), ("s3", C3, C4, S3), ("s4", C4, C5, S4), ("s5", C5, C6, S5),
          ("s6", C6, C7, S6), ("s7", C7, C8, S7), ("s8", C8, C9, S8), ("s9", C9, C10, S9), ("s10", C10, C11, S10), ("s11", C11, C12, S11), ("s12", C12, T, S12)]
scene_html = "\n".join(f'<div id="{i}" class="scene clip" data-start="{a}" data-duration="{round(b - a, 3)}">{h}</div>' for i, a, b, h in scenes)

# ------------------------------------------------------------------ timeline beats
J = []
def j(s): J.append(s)
j(f'tl.set("#cam",{{scale:1}},{C12});')
for _, a, b, _h in scenes[:-1]:
    j(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.045,duration:{b - a - 0.05:.3f},ease:"none",immediateRender:false}},{a + 0.01:.3f});')
j('const punch=(t,s=1.08)=>{tl.to("#shaker",{scale:s,duration:0.08,ease:"power2.out"},t);tl.to("#shaker",{scale:1,duration:0.3,ease:"power2.inOut"},t+0.08);};')
j('const shake=(t,d=0.5,a=14)=>{tl.fromTo("#shaker",{x:-a},{x:a,duration:0.05,repeat:Math.round(d/0.05),yoyo:true,ease:"none",immediateRender:false},t);tl.to("#shaker",{x:0,duration:0.05},t+d);};')
j('const pop=(s,t,from=0)=>tl.fromTo(s,{scale:from,opacity:0},{scale:1,opacity:1,duration:0.3,ease:"back.out(2.6)"},t);')
j('const out=(s,t)=>tl.to(s,{opacity:0,scale:0.7,duration:0.15,ease:"power2.in"},t);')
j('const stamp=(s,t,r=-8)=>tl.fromTo(s,{scale:3,opacity:0,rotation:r-6},{scale:1,opacity:1,rotation:r,duration:0.22,ease:"power4.out"},t);')
for t in (tDiwali, tNah, t6ix, tKnock, tDiff, tSolid, tIL1, tSig, tEarned, tHappy): j(f"punch({t:.3f});")
for t, d in ((tDead, 0.35), (tNah, 0.25)): j(f"shake({t:.3f},{d});")
j('tl.set("#shaker",{x:0,y:0,scale:1},0);')
for b, a, d in (("#dots3", C3, C4 - C3), ("#dots5", C5, C6 - C5), ("#dots6", C6, C7 - C6)):
    j(f'tl.fromTo("{b}",{{x:0,y:0}},{{x:70,y:140,duration:{d:.3f},ease:"none"}},{a});')
for t, pos in ((0, POS_HOOK), (C1, POS_BIG), (C2, POS_BIG), (C3, POS_V2), (C10, POS_COUCH), (C11, POS_V2), (C12, POS_HOOK)):
    j(f'tl.set("#cytoPos",{json.dumps(pos)},{t});')
j(f'tl.set("#cytoPos",{json.dumps(POS_HOOK)},{T - 0.01});')
# couch flop: lean back on the couch, sit up again for the outro
j(f'tl.set("#cytoJump",{{rotation:0,transformOrigin:"600px 960px"}},0);tl.fromTo("#cytoJump",{{rotation:0}},{{rotation:-14,duration:0.35,ease:"bounce.out",transformOrigin:"600px 960px",immediateRender:false}},{C10 + 0.05});'
  f'tl.set("#cytoJump",{{rotation:0}},{C11});')
# hook slump on "dead on the couch"
j(f'tl.fromTo("#cytoJump",{{rotation:0}},{{rotation:-10,duration:0.25,ease:"power2.out",transformOrigin:"600px 960px",immediateRender:false}},{tDead});tl.to("#cytoJump",{{rotation:0,duration:0.25,transformOrigin:"600px 960px"}},{C1 - 0.3});')


def hook_js(idp, t0, t1, anim=True):
    s = (f'document.querySelectorAll("#{idp}City .win").forEach((w,i)=>{{ if(i%5==0) tl.to(w,{{opacity:.2,duration:0.25,repeat:5,yoyo:true}},{t0}+(i%7)*0.27); }});'
         f'document.querySelectorAll("#s{idp[1:]} .diyaF").forEach((f,i)=>tl.fromTo(f,{{scaleY:1,scaleX:1}},{{scaleY:1.25,scaleX:.85,duration:0.18+0.03*(i%3),repeat:Math.ceil({t1 - t0:.2f}/0.2),yoyo:true,ease:"sine.inOut"}},{t0}));')
    if anim:
        s += (f'tl.fromTo("#{idp}Bus",{{x:1200}},{{x:-800,duration:{t1 - t0 + 1.2:.2f},ease:"none"}},{t0});'
              '')
    return s


j(hook_js("h1", 0, C1))
j(burst_js("h1Fw", 0.02, C1)); j(burst_js("h1Fw", 0, 0, still=True))
j(f'tl.set(["#t1a","#t1b"],{{opacity:0}},0);tl.fromTo("#t1a",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.26,ease:"power4.out"}},{max(0.05, tDiwali - 0.05)});out("#t1a",{tDead - 0.2});')
j(f'stamp("#t1b",{tDead},0);tl.to("#t1b",{{y:20,rotation:-6,duration:0.4,ease:"power2.in"}},{tCouch});')
# S1b: mithai plate, "?" then NAH stamp
j(f'document.querySelectorAll("#mp1 .sweet").forEach((s,i)=>tl.fromTo(s,{{y:-120,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"bounce.out"}},{C1 + 0.05}+i*0.05));')
j(f'tl.fromTo("#mp1",{{scale:1}},{{scale:1.05,transformOrigin:"770px 1090px",duration:0.2,yoyo:true,repeat:1}},{tMithai});')
j(lot("dy1", "diya-1.json", C1, C2, loops=1))
j(f'tl.set(["#q1","#nah1"],{{opacity:0}},0);pop("#q1",{tMithai - 0.05});tl.to("#q1",{{rotation:12,duration:0.12,yoyo:true,repeat:2}},{tMithai + 0.3});out("#q1",{tNah - 0.2});stamp("#nah1",{tNah - 0.03});')
# S2 intro
j(hook_js("h2", C2, C3, anim=False))
j(burst_js("fw2", C2 + 0.05, tLive));j(f'tl.set("#fw2",{{opacity:1}},0);tl.to("#fw2",{{opacity:0,duration:0.12}},{tLive - 0.2});')
j(burst_js("fw2b", tLive, C3))
j(f'tl.set("#t2a",{{opacity:0}},0);tl.fromTo("#t2a",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.28,ease:"power4.out"}},{tLive - 0.05});')
j(f'tl.set("#t2c",{{opacity:0}},0);tl.fromTo("#t2c",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{tInside});')
j(f'tl.fromTo("#h2City",{{y:60}},{{y:0,duration:{C3 - C2:.3f},ease:"power1.out"}},{C2});')
# S3 myth
j(f'tl.fromTo("#pn3",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C3});')
j(f'tl.fromTo("#rice3",{{y:-200,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"bounce.out"}},{C3 + 0.15});tl.fromTo("#naan3",{{x:-300,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{tCarbs});')
j(f'tl.set("#t3",{{opacity:0}},0);tl.fromTo("#t3",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:0.26,ease:"power4.out"}},{tCarbs - 0.05});')
j(f'tl.to("#t3",{{x:10,duration:0.05,repeat:5,yoyo:true}},{tKnock + 0.1});')
j(zzz_js("z3", tKnock, C4))
j(f'tl.set("#cd3",{{opacity:0}},0);tl.fromTo("#cd3",{{x:600,opacity:1}},{{x:0,opacity:1,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{tCarbs + 0.15});')
# S4 sleep lab
j(f'tl.fromTo("#eegL",{{x:0}},{{x:-60,duration:0.6,repeat:5,ease:"none"}},{C4});')
j(f'tl.fromTo("#pv4Train",{{x:0}},{{x:-260,duration:{C5 - C4:.2f},ease:"power1.inOut"}},{C4});tl.fromTo("#bus4",{{x:-700}},{{x:0,duration:1.4,ease:"power2.out"}},{C4 + 0.8});')
j(f'pop("#t4",{tSleep - 0.05});out("#t4",{tFat - 0.25});')
j(f'tl.set(["#c4a","#c4b","#c4c"],{{opacity:0}},0);' + "".join(f'tl.fromTo("{s}",{{x:-400,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"back.out(1.8)"}},{t - 0.05});' for s, t in (("#c4a", tFat), ("#c4b", tCarb), ("#c4c", tMixed))))
j(f'tl.fromTo("#cd4",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tSleep});')
# S5 3 equal bars
j(three("B5", "bars", "cvB5", C5, C6,
        f'{{dur:{C6 - C5:.3f},tGrow:0.15,floorW:7.2,bars:[{{h:.62,color:0xffd166}},{{h:.62,color:0xf5a524}},{{h:.62,color:0x3fc1b0}}],'
        f'labels:[document.getElementById("lb5a"),document.getElementById("lb5b"),document.getElementById("lb5c")]}}'))
j(f'tl.fromTo("#pn5",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C5 + 0.02});')
j(f'tl.fromTo(["#lb5a","#lb5b","#lb5c"],{{opacity:0}},{{opacity:1,duration:0.25}},{C5 + 0.9});')
j(f'tl.set(["#eq5","#same5","#q5"],{{opacity:0}},0);stamp("#same5",{tDiff - 0.03});out("#same5",{tWhat - 0.25});')
j(f'pop("#q5",{tWhat - 0.05});tl.to(["#lb5a","#lb5b","#lb5c"],{{opacity:0,duration:0.15}},{tWhat - 0.1});')
j(f'tl.fromTo("#cd5",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tNo + 0.1});')
# S6 meal vs water
j(three("B6", "bars", "cvB6", C6, C7,
        f'{{dur:{C7 - C6:.3f},tGrow:{tSolid - C6 - 0.3:.3f},zoomAt:{tWater - C6 + 0.2:.3f},bars:[{{h:.38,color:0x5ae68c}},{{h:.9,color:0x9fc3e8}}],'
        f'labels:[document.getElementById("lb6a"),document.getElementById("lb6b")],gap:document.getElementById("gap6")}}'))
j(f'tl.fromTo("#pn6",{{scale:1.15,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"power3.out"}},{C6});')
j(f'tl.set(["#lb6a","#lb6b","#gap6"],{{opacity:0}},0);tl.to("#lb6a",{{opacity:1,duration:0.2}},{tSolid + 0.3});tl.to("#lb6b",{{opacity:1,duration:0.2}},{tComp});pop("#gap6",{tComp + 0.45});')
j(f'tl.set("#cupW",{{opacity:0}},0);tl.fromTo("#cupW",{{y:-200,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"bounce.out"}},{tComp});')
j(f'tl.fromTo("#cd6",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{tEating});')
# S7 elevator opens, IL-1 messengers march out
j(f'tl.fromTo("#hwDL",{{x:0}},{{x:-180,duration:0.5,ease:"power2.inOut"}},{C7 + 0.25});tl.fromTo("#hwDR",{{x:0}},{{x:180,duration:0.5,ease:"power2.inOut"}},{C7 + 0.25});')
j(f'tl.fromTo("#hwArrow",{{opacity:1}},{{opacity:.2,duration:0.15,repeat:5,yoyo:true}},{C7});')
for k in range(3):
    j(f'tl.fromTo("#m{k}",{{x:{290 + (k - 1) * 70},y:{600 - k * 10},scale:.3,opacity:0}},{{x:{230 + k * 190},y:{690 + (k % 2) * 30},scale:.9,opacity:1,duration:0.7,ease:"back.out(1.6)"}},{tMess - 0.35 + k * 0.15:.3f});')
    j(f'tl.fromTo("#m{k}Flag",{{rotation:-12,svgOrigin:"34 -10"}},{{rotation:12,svgOrigin:"34 -10",duration:0.3,repeat:5,yoyo:true,ease:"sine.inOut"}},{tMess + k * 0.1:.3f});')
j(f'tl.set("#t7",{{opacity:0}},0);tl.fromTo("#t7",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.26,ease:"power4.out"}},{tIL1 - 0.05});')
j(f'tl.set("#cd7",{{opacity:0}},0);tl.fromTo("#cd7",{{x:600,opacity:1}},{{x:0,opacity:1,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{tImmune});')
# S8 messengers post a zzz envelope through the mail slot, tired meter fills
for k in range(3):
    j(f'tl.fromTo("#n{k}",{{x:{80 + k * 140},y:{740 + (k % 2) * 30},scale:.9}},{{x:{240 + k * 140},y:{740 + (k % 2) * 30},scale:.9,duration:1.1,ease:"power1.inOut"}},{C8:.3f});')
    j(f'tl.fromTo("#n{k}Flag",{{rotation:-12,svgOrigin:"34 -10"}},{{rotation:12,svgOrigin:"34 -10",duration:0.3,repeat:7,yoyo:true,ease:"sine.inOut"}},{C8 + k * 0.1:.3f});')
j(f'tl.fromTo("#env8",{{x:520,y:560,rotation:-10,opacity:1,scale:1}},{{x:726,y:686,rotation:0,duration:0.6,ease:"power2.inOut"}},{C8 + 0.4});'
  f'tl.to("#env8",{{x:726,y:686,scaleX:.2,opacity:0,duration:0.3,ease:"power2.in"}},{C8 + 1.2});')
j(f'tl.set("#meter8",{{opacity:0}},0);pop("#meter8",{tTired - 0.3});tl.fromTo("#meterF",{{scaleX:.1}},{{scaleX:.92,duration:1.4,ease:"power2.out"}},{tTired});')
j(f'tl.fromTo("#cd8",{{x:600}},{{x:0,duration:0.35,ease:"back.out(1.4)"}},{C8 + 0.3});')
# S9 not the mithai -> full stomach + immune signals = zzz
j(f'tl.fromTo("#pn9",{{y:900}},{{y:0,duration:0.4,ease:"power3.out"}},{C9});')
j(f'tl.fromTo("#x9",{{opacity:0,scale:2,transformOrigin:"265px 330px"}},{{opacity:1,scale:1,duration:0.25,ease:"power4.out"}},{tMithai2});')
j(f'tl.to(["#mp9w","#x9"],{{opacity:0,duration:0.2}},{tFull - 0.2});')
j(f'tl.fromTo("#st9w",{{opacity:0,scale:.3,transformOrigin:"150px 330px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{tFull - 0.05});'
  f'tl.fromTo("#st9Fill",{{y:300}},{{y:60,duration:0.9,ease:"power2.out"}},{tStom});')
j(f'tl.fromTo("#pl9",{{opacity:0}},{{opacity:1,duration:0.2}},{tPlus});tl.fromTo("#ce9w",{{opacity:0,scale:.3,transformOrigin:"470px 360px"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{tBare});')
j(f'tl.fromTo("#q9Flag",{{rotation:-12,svgOrigin:"34 -10"}},{{rotation:12,svgOrigin:"34 -10",duration:0.3,repeat:4,yoyo:true}},{tBare + 0.2});')
j(f'tl.fromTo("#eq9",{{opacity:0}},{{opacity:1,duration:0.2}},{tSig + 0.3});tl.set("#z9w",{{opacity:0}},0);tl.set("#z9w",{{opacity:1}},{tSig + 0.35});' + zzz_js("z9", tSig + 0.35, C10))
j(f'tl.set(["#lbS9","#lbI9"],{{opacity:0}},0);pop("#lbS9",{tStom});pop("#lbI9",{tSig - 0.1});')
j(f'tl.set("#cd9",{{opacity:0}},0);tl.fromTo("#cd9",{{x:600,opacity:1}},{{x:0,opacity:1,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{tFull + 0.2});')
# S10 couch nap
j(snow_js("s10", C10, C11, 700))
j(f'document.querySelectorAll("#s10 .diyaF").forEach((f,i)=>tl.fromTo(f,{{scaleY:1}},{{scaleY:1.25,duration:0.2,repeat:16,yoyo:true}},{C10}));')
j(f'document.querySelectorAll("#rg10 .rring").forEach((r,i)=>tl.fromTo(r,{{rotation:0}},{{rotation:(i%2?-40:40),duration:{C11 - C10:.2f},ease:"none"}},{C10}));')
j(zzz_js("z10", C10 + 0.2, C11))
j(lot("rgL", "rangoli-1.json", C10, C11, loops=1))
j(f'tl.set(["#er10","#sl10"],{{opacity:0}},0);stamp("#er10",{tEarned - 0.03},-6);out("#er10",{tSay - 0.18});stamp("#sl10",{tSay - 0.02},-6);out("#sl10",{tNot - 0.2});')
j(f'tl.set("#cd10",{{opacity:0}},0);tl.fromTo("#cd10",{{opacity:1,x:600}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{tNot - 0.05});')
j(f'tl.set("#cupTable",{{opacity:0}},0);tl.set("#cup",{{opacity:0}},{tNot - 0.05});tl.set("#cupTable",{{opacity:1}},{tNot - 0.05});tl.set("#cup",{{opacity:1}},{C11});tl.set("#cupTable",{{opacity:0}},{C11});')
# S11 outro: string-lit street (Gerrard-style), subscribe, sources, happy Diwali
j(burst_js("fw11", tHappy - 0.1, C12))
j(f'document.querySelectorAll("#s11 .bulb").forEach((b,i)=>tl.to(b,{{opacity:.35,duration:0.25,repeat:9,yoyo:true}},{C11}+(i%4)*0.12));')
j(f'tl.fromTo("#pn11",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(1.6)"}},{C11 + 0.05});')
j(f'tl.fromTo("#like11",{{scale:0,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.3,ease:"back.out(3)"}},{tLike});')
j(f'tl.fromTo("#sub11",{{scale:1}},{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},{tSub + 0.15});'
  f'tl.set("#subd11",{{opacity:0}},0);tl.set("#subd11",{{opacity:1}},{tSub + 0.25});tl.set("#sub11",{{opacity:0}},{tSub + 0.25});')
j(f'tl.fromTo("#src11",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{C11 + 0.2});')
j(f'tl.set("#hd11",{{opacity:0}},0);tl.fromTo("#hd11",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.26,ease:"power4.out"}},{tHappy - 0.05});')
# S12 loop frame = hook frame 0
j(f'tl.fromTo("#s12",{{opacity:0}},{{opacity:1,duration:0.18}},{C12});')
j(f'document.querySelectorAll("#h12Fw .fwr").forEach((g,i)=>tl.set(g,{{scale:[.9,.5,.3][i],opacity:[.9,.6,.4][i]}},0));')
j(f'tl.set("#h12Bus",{{x:1200}},0);tl.fromTo("#h12Bus",{{x:1200}},{{x:1200,duration:0.01}},{C12});')

CSS = f"""
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:InterXB; }}
#cam, #shaker {{ position:absolute; inset:0; transform-origin:540px 960px; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.bgfill {{ position:absolute; inset:0; }}
.lot {{ position:absolute; }}
.navy {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #17304d 0%, #0c1622 70%); }}
.dots {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; background-image:radial-gradient(rgba(120,170,220,.10) 3px, transparent 4px); background-size:70px 70px; }}
.big {{ position:absolute; left:0; width:1080px; text-align:center; font-family:InterBlack; line-height:.95; letter-spacing:-2px;
  paint-order:stroke fill; -webkit-text-stroke:14px #0c1622; text-shadow:0 10px 0 #0c1622; opacity:0; }}
.chip {{ position:absolute; font-family:InterBlack; letter-spacing:.03em; padding:10px 22px; border-radius:30px; border:5px solid #0c1622;
  box-shadow:0 6px 0 #0c1622; white-space:nowrap; opacity:0; color:#0c1622; }}
.stamp {{ position:absolute; font:120px InterBlack; color:#FF7A59; padding:6px 30px; border:12px solid #FF7A59; border-radius:24px;
  background:rgba(12,22,34,.85); transform:rotate(-8deg); opacity:0; letter-spacing:.02em; z-index:40; white-space:nowrap; }}
.blab {{ position:absolute; transform:translate(-50%,-120%); font:38px InterBlack; paint-order:stroke fill; -webkit-text-stroke:8px #0c1622; opacity:0; white-space:nowrap; }}
.gap {{ position:absolute; transform:translate(-50%,-50%); }}
.gap span {{ display:block; background:#5AE68C; color:#0c1622; font:34px InterBlack; padding:8px 18px; border-radius:24px; border:5px solid #0c1622; box-shadow:0 5px 0 #0c1622; white-space:nowrap; }}
.flake {{ position:absolute; border-radius:50%; background:#FAF4E8; }}
.subbtn {{ position:absolute; left:150px; top:70px; width:580px; height:140px; border-radius:70px; border:7px solid #0c1622; box-shadow:0 10px 0 #0c1622;
  font:64px InterBlack; text-align:center; line-height:126px; }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-210px; width:420px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
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
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="shaker" class="clip" data-start="0" data-duration="{T}"><div id="cam">
{scene_html}
  <div id="cytoLayer">{R.rig3_html("outfit_kurta", "cup_red")}</div>
</div></div>
<div id="pill" class="clip" data-start="0" data-duration="{T}">6IXTY SECONDS OF SCIENCE</div>
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
print("built", len(html), "bytes; T", T, "C12", C12, "words", len(WORDS), "voice", round(TM["total"], 2))
