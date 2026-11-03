"""EP13 — Meet Neutro: Your Flu Season Bouncer (6ixty Seconds of Science / Cyto vs Disease).
Base: hf/ep12/build.py (v2 layout + v3 rig + Ep 12 upgrades: Scribe word timing, visemes, acting on stressed words, ElevenLabs SFX
under the voice, synth bed, overshoot/push-ins, a transition on every cut). New: Neutro (studio/rig/neutro/neutro.py), hoodie outfit.
python3 build.py -> index.html + assets/audio.wav"""
import json, sys, os, subprocess, random, re
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import numpy as np
import cytohf as C, cyto3 as R, art as A
from neutro import neutro_html, neutro_js
from engine import tone, noise, hp, lp, add, load_mono, SR

P = "/home/claude/hf/ep13"; os.chdir(P)
V = "/home/claude/ep13"
TM = json.load(open(f"{V}/timing.json")); WORDS = TM["words"]
W, H = 1080, 1920


def wt(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and re.sub(r"[^a-z0-9%']", "", w["w"].lower()) == re.sub(r"[^a-z0-9%']", "", word.lower()):
            return round(w["t0"], 3)
    raise KeyError(word)


# ------------------------------------------------------------------ word beats (Scribe times; after= for repeated/short words)
tFlus, tComing, tSix, tWho, tPulls, tFirst, tNeutro = wt("Flu's"), wt("coming"), wt("6ix"), wt("Who"), wt("pulls"), wt("first"), wt("Neutro")
tYo, tCyto, tLive, tSix2, tInside = wt("Yo"), wt("Cyto"), wt("live"), wt("6ix", 4), wt("inside")
tWhen, tHits, tAir, tNphil, tFirst2, tImmune, tScene = wt("When"), wt("hits"), wt("airways"), wt("neutrophils"), wt("first", 9), wt("immune"), wt("scene")
tBouncer, tEnergy, tDun, tKnow = wt("Bouncer"), wt("energy"), wt("dun"), wt("know")
tThey, tEat, tGerms, tRelease, tToxic, tChem, tEven, tThrow, tSticky, tNets = wt("They"), wt("eat"), wt("germs"), wt("release"), wt("toxic"), wt("chemicals"), wt("even"), wt("throw"), wt("sticky"), wt("nets")
tBut, tMcM, tThin, tLine, tHelpful, tHarmful = wt("But"), wt("McMaster"), wt("thin"), wt("line"), wt("helpful"), wt("harmful")
tIn, tSevere, tSame, tMoves, tHurt, tLungs = wt("In", 20), wt("severe"), wt("same"), wt("moves"), wt("hurt"), wt("lungs")
tNeutros, tBouncer2, tAmazing, tSwings, tToo, tHard = wt("Neutro's"), wt("bouncer", 24), wt("amazing"), wt("swings"), wt("too", 24), wt("hard")
tYour, tBest, tDefence, tYearly, tShot, tFam, tNot, tAdvice = wt("Your", 26), wt("best"), wt("defence"), wt("yearly"), wt("shot"), wt("fam"), wt("Not"), wt("advice")
tLike, tSub, tTell, tNeutro3, tWagwan = wt("Like"), wt("subscribe"), wt("tell"), wt("Neutro", 30), wt("wagwan")
END_V = WORDS[-1]["t1"]

C1, C2, C3, C4, C5, C6, C7, C8 = (round(x, 2) for x in (tYo - 0.15, tWhen - 0.15, tThey - 0.1, tBut - 0.1, tIn - 0.1, tNeutros - 0.08, tYour - 0.1, tLike - 0.1))
SIPS = [(round(END_V + 0.08, 2), 0.62)]
C9 = round(SIPS[0][0] + SIPS[0][1] + 0.05, 2)
T = round(C9 + 0.55, 2)
CUTS = (C1, C2, C3, C4, C5, C6, C7, C8, C9)

# ------------------------------------------------------------------ assets
C.copy_assets_v2(P, lotties=["shield-2.json"])


# ------------------------------------------------------------------ audio: synth bed (drums out for the serious beat) + Ep 12 ElevenLabs SFX
def load_sfx(name, max_len):
    x = load_mono(f"{V}/sfx/{name}.wav", SR)
    env = np.abs(x); thr = env.max() * 0.004
    nz = np.where(env > thr)[0]
    x = x[nz[0]: min(len(x), nz[0] + int(max_len * SR))] if len(nz) else x[: int(max_len * SR)]
    f = min(len(x), int(0.08 * SR)); x[-f:] *= np.linspace(1, 0, f)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)


def pad(m, dur, g=0.035):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.7).clip(0, 1)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3.01 * f * t)) * env * g


def make_audio(sfx_events):
    n = int((T + 0.3) * SR); music = np.zeros(n, np.float32)
    BPM = 92; BAR = 60 / BPM * 4
    chords = [[50, 57, 60, 65], [46, 53, 57, 62], [43, 50, 55, 58], [45, 52, 57, 61]]   # Dm7 Bbmaj7 Gm7 A — wintry, a bit of swagger
    t = 0.0; i = 0
    while t < T + 0.3:
        for m in chords[i % 4]: add(music, pad(m + 12, BAR + 0.8), t)
        add(music, pad(chords[i % 4][0], BAR + 0.4, 0.05), t)
        t += BAR; i += 1
    kick = tone(100, 42, 0.3, 0.1) * 0.55
    snare = hp(noise(0.12, 5), 0.25) * np.exp(-np.arange(int(0.12 * SR)) / SR / 0.04) * 0.12
    hat = hp(noise(0.03, 2), 0.6) * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.008) * 0.07
    BEAT = 60 / BPM; t = C1; s = 0
    while t < T + 0.3:
        if not (C5 - 0.05 <= t < C6 - 0.05):                 # serious beat: drums drop out
            if s % 4 in (0, 2): add(music, kick, t)
            if s % 4 in (1, 3): add(music, snare, t)
            add(music, hat, t + BEAT / 2)
        t += BEAT; s += 1
    music = lp(music, 0.3)
    v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    vrms = np.sqrt(np.mean(vv[np.abs(vv) > 0.02] ** 2))
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.6 * np.clip(env * 3, 0, 1))
    music *= vrms * 10 ** (-24 / 20) / (np.sqrt(np.mean(music ** 2)) + 1e-9)
    S = {"whoosh": load_sfx("whoosh", 0.9), "pop": load_sfx("pop", 0.35), "hit": load_sfx("hit", 1.4), "chime": load_sfx("chime", 1.5)}
    GAIN = {"whoosh": -18, "pop": -18, "hit": -15, "chime": -17}
    sfx = np.zeros(n, np.float32)
    for kind, tt in sfx_events: add(sfx, S[kind] * vrms * 10 ** (GAIN[kind] / 20), max(0, tt))
    mix = music + sfx; mix[:m] += v[:m]
    mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[: int(T * SR)]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/raw_mix.wav"],
                   input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/raw_mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "assets/base.wav"], check=True)


SFX = [("hit", tNeutro), ("pop", tCyto), ("hit", tSix2), ("pop", tInside),
       ("pop", tAir), ("pop", tNphil), ("hit", tFirst2), ("hit", tBouncer), ("pop", tDun),
       ("pop", tEat), ("pop", tGerms), ("pop", tToxic), ("pop", tChem), ("pop", tSticky), ("pop", tNets),
       ("pop", tMcM), ("pop", tHelpful), ("hit", tHarmful), ("pop", tSame), ("hit", tHurt),
       ("pop", tAmazing), ("hit", tSwings + 0.1), ("pop", tDefence), ("chime", tShot), ("pop", tNot),
       ("pop", tLike), ("pop", tSub + 0.15), ("chime", tWagwan)]
SFX += [("whoosh", c - 0.22) for c in CUTS]
make_audio(SFX)

# ------------------------------------------------------------------ Cyto: hoodie + toque, acting
POS_HOOK, POS_BIG, POS_V2 = C.place(300, 1335, 0.60), C.place(330, 1300, 0.64), C.CYTO_V2
mouth = R.viseme_track(f"{V}/voice.wav", WORDS)
if mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
blinks = [(t, 0.1) for t in (1.7, 4.6, 7.6, 10.5, 13.3, 16.4, 19.6, 22.6, 25.4, 28.4, 31.2, 33.4)]
gest = dict(sips=SIPS, raises=[(tCyto, 0.6), (tShot - 0.1, 0.7)], waves=[tYo, tWagwan - 0.05],
            points=[(tNphil - 0.05, 0.8), (tEat - 0.05, 0.5), (tToxic - 0.05, 0.5), (tSticky - 0.05, 0.6), (tMcM - 0.05, 0.6), (tAmazing - 0.05, 0.6)],
            tilts=[(tFirst - 0.1, 0.5, 7), (tDun, 0.6, -7), (tHarmful, 0.6, 6), (tFam, 0.6, -7), (tSix2, 0.5, 7)],
            shrugs=[(tThin - 0.05, 0.6)])
expr = [(tFlus, 0.8, "shock"), (tWho - 0.05, 0.7, "squint"), (tNeutro - 0.05, 0.6, "hype"), (tCyto - 0.05, 0.5, "hype"), (tSix2, 0.5, "hype"),
        (tAir - 0.05, 0.8, "squint"), (tFirst2 - 0.05, 0.7, "hype"), (tBouncer - 0.05, 0.8, "hype"), (tToxic - 0.05, 0.7, "shock"),
        (tSticky - 0.05, 0.7, "hype"), (tBut - 0.05, 1.2, "skeptic"), (tHarmful - 0.05, 0.8, "skeptic"), (tSevere - 0.05, 1.0, "sad"),
        (tHurt - 0.05, 1.0, "sad"), (tAmazing - 0.05, 0.6, "hype"), (tSwings - 0.05, 0.7, "shock"), (tBest - 0.05, 0.6, "squint"),
        (tShot - 0.05, 0.6, "hype"), (tNot - 0.05, 0.9, "squint"), (tLike - 0.05, 0.5, "hype"), (tWagwan - 0.05, 0.6, "hype")]
looks = [(C2 + 0.3, 6, -6), (C3 + 0.4, 6, -6), (C4 + 0.3, 6, -5), (C5 + 0.4, 6, -6), (C6 + 0.3, 6, -5), (C7 + 0.4, 6, -6), (C8 + 0.4, 6, -6)]
rig_js = R.rig3_js(mouth, T, blinks=blinks, mute=[(s[0], 0) for s in SIPS], expr=expr, looks=looks, **gest)
R.mix_sips("assets/base.wav", [s[0] for s in SIPS], "assets/audio.wav")

# ------------------------------------------------------------------ captions (real spellings) + transitions
PINK = "#f6a6c8"
KEYS = {"flus": "#FF7A59", "flu": "#FF7A59", "6ix": "#FFD166", "neutro": PINK, "neutros": PINK, "first": "#FFD166",
        "cyto": "#3fc1b0", "airways": "#9fc3e8", "bouncer": "#FFD166", "dun": "#3fc1b0", "eat": "#5AE68C", "germs": "#5AE68C",
        "toxic": "#5AE68C", "chemicals": "#5AE68C", "sticky": "#5AE68C", "nets": "#5AE68C", "mcmaster": "#9fc3e8", "helpful": "#5AE68C",
        "harmful": "#FF7A59", "severe": "#FF7A59", "lungs": "#FF7A59", "amazing": "#5AE68C", "hard": "#FF7A59", "defence": "#5AE68C",
        "shot": "#5AE68C", "fam": "#3fc1b0", "subscribe": "#FF7A59", "wagwan": "#FFD166"}
CAPW = [w for w in WORDS if not (tLive - 0.01 <= w["t0"] < C2)]
cap_html, cap_js = C.captions(CAPW, KEYS, y=C.CAP_Y_V2)
last_cap = cap_html.count('"cap clip"') - 1
cap_js += f'\ntl.set("#cap{last_cap}",{{opacity:0}},{C9});'
_m = [m for m in re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'CYTO,' in m.group(2)][0]
cap_js += f'\ntl.set("#{_m.group(1)}",{{opacity:1}},0);tl.set("#{_m.group(1)}",{{opacity:0}},{tLive - 0.03});'
TRS = [C.transition(k, t) for k, t in (("zoom", C1), ("doors", C2), ("membrane", C3), ("whip", C4), ("membrane", C5), ("zoom", C6),
                                        ("whip", C7), ("doors", C8), ("zoom", C9))]
tr_html = "\n".join(h for h, _ in TRS)
tr_js = "\n".join(j for _, j in TRS).replace('{scale:1.0,duration:0.35,', '{scale:1.0,immediateRender:false,duration:0.35,').replace('{x:-60,duration:0.18,', '{x:-60,immediateRender:false,duration:0.18,')


# ------------------------------------------------------------------ helpers
def chip(id_, text, left, top, bg="#FFD166", fg=A.INK, size=40, extra=""):
    return f'<div id="{id_}" class="chip" style="left:{left}px;top:{top}px;background:{bg};color:{fg};font-size:{size}px;{extra}">{text}</div>'


def svg(inner, w=W, h=H, style="position:absolute;left:0;top:0;overflow:visible"):
    return f'<svg width="{w}" height="{h}" style="{style}">{inner}</svg>'


def NT(idp, left, top, s, pose="cross"):
    """Neutro, placed by an outer div (#{idp}W, for slides); the rig animates the inner svg group #{idp}."""
    return (f'<div id="{idp}W" class="ntw" style="left:{left}px;top:{top}px;transform:scale({s})">'
            f'{neutro_html(idp, pose)}</div>')


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


def head(x, y, s, c, cls):
    """Rider head + shoulders seen through a train window."""
    return (f'<g transform="translate({x},{y}) scale({s})"><g class="{cls}"><path d="M-40 70 Q-40 26 0 26 Q40 26 40 70Z" fill="{c}" stroke="{A.INK}" stroke-width="5"/>'
            f'<circle cx="0" cy="0" r="27" fill="#e8b98f" stroke="{A.INK}" stroke-width="5"/><path d="M-27 -4 Q-27 -36 0 -36 Q27 -36 27 -4Z" fill="{c}" stroke="{A.INK}" stroke-width="5"/></g></g>')


# ------------------------------------------------------------------ scenes
def hook(idp):
    """Union Station front at dusk = the 'airway entrance'; Neutro works the door (Toronto plan: hook)."""
    return f'''<div class="bgfill" style="background:linear-gradient(#1d2650 0%,#4a3f78 40%,#c9707a 70%,#f2a77a 86%)"></div>
{svg(f'{A.stars(W, H, 14, 13, .18)}<g>{A.skyline(W, H, 760, .9, seed=13, lit=.35, cn=990)}</g><g>{A.union_station(W, 1500, idp + "us")}</g>')}
<div id="{idp}t" class="big" style="top:250px;left:60px;width:880px;font-size:124px;color:#FFD166;opacity:1">FLU SEASON</div>
{NT(idp + "n", 600, 967, .82, "cross")}'''


S1 = hook("h1")

S2 = f'''<div class="bgfill" style="background:linear-gradient(#0a1024 0%,#1b2650 70%,#3a3f6b 85%)"></div>
{svg(f'{A.stars(W, H, 50, 21, .45)}<g id="h2City">{A.skyline(W, H, 1000, 1.05, seed=23, lit=.45, cn=760)}</g>')}
<div id="t2a" class="big" style="top:250px;font-size:170px;color:#FFD166"><span style="font-size:74px;color:#FAF4E8">LIVE FROM</span><br>THE 6IX</div>
{chip("t2c", "...INSIDE YOUR BODY", 300, 640, bg="#3fc1b0", size=42)}'''

RIDER_C = ["#4a5d7d", "#7a3b4a", "#2f6b5a", "#6b5a2f", "#3b4a7a", "#5a3b6b"]
riders = "".join(head(105 + k * 230 + dx, 830, .9, RIDER_C[(k * 2 + j) % 6], f"rid r{k}") for k in range(5) for j, dx in enumerate((-28, 28)))
SNEEZE = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9be08a" opacity=".55"/>' for x, y, r in ((0, 0, 46), (40, -20, 36), (-36, -14, 30), (20, 26, 30))) + \
         A.virus(-10, -6, 15, cls="sv") + A.virus(34, 16, 12, cls="sv") + A.virus(28, -26, 11, cls="sv")
S3 = f'''{svg(f"""<g id="bp3">{A.subway_platform(W, H, "bp")}</g>
 <g id="rid3">{riders}</g>
 <g id="sn3" transform="translate(-120,790)"><g id="sn3i">{SNEEZE}</g></g>
 {A.raccoon(905, 172, .5, "rc3")}""")}
{chip("c3", "AIRWAYS", 400, 340, bg="#9fc3e8", size=50)}
<div id="st3" class="stamp" style="left:140px;top:330px;font-size:84px">FIRST ON SCENE</div>
<div id="b3" class="big" style="top:330px;left:60px;width:880px;font-size:88px;color:#FFD166">BOUNCER ENERGY</div>
{NT("n3", 640, 1030, .68, "cross")}'''

COLS = (150, 440, 730)
eat = (f'<g transform="translate({COLS[0]},280) scale(1.3)"><circle r="92" fill="{PINK}" stroke="{A.INK}" stroke-width="7"/>'
       f'<circle cx="-30" cy="-40" r="16" fill="#6f45a3" stroke="{A.INK}" stroke-width="4"/><circle cx="0" cy="-52" r="18" fill="#6f45a3" stroke="{A.INK}" stroke-width="4"/>'
       f'<circle cx="30" cy="-40" r="16" fill="#6f45a3" stroke="{A.INK}" stroke-width="4"/>'
       f'<g id="jaw4"><path d="M0 10 L96 -22 L96 42Z" fill="#0f2236" stroke="{A.INK}" stroke-width="6" stroke-linejoin="round"/></g></g>'
       + "".join(f'<g class="eg">{A.virus(COLS[0] + 170 + k * 50, 290 + (k % 2) * 34 - 17, 21, cls="ev")}</g>' for k in range(3)))
spray = (f'<g transform="translate({COLS[1]},280) scale(1.3)">'
         + "".join(f'<g class="dr"><circle cx="{math_c * 0}" cy="0" r="15" fill="#d6f03a" stroke="{A.INK}" stroke-width="4" '
                   f'data-a="{a}"/></g>' for a, math_c in [(k * 45, 0) for k in range(8)])
         + f'<circle r="88" fill="{PINK}" stroke="{A.INK}" stroke-width="7"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#d49ac0"/>' for x, y in ((-40, 20), (30, 40), (-10, -30), (44, -10), (-50, -20), (10, 10)))
         + f'<circle cx="-20" cy="-48" r="18" fill="#6f45a3" stroke="{A.INK}" stroke-width="4"/><circle cx="18" cy="-48" r="18" fill="#6f45a3" stroke="{A.INK}" stroke-width="4"/></g>')
NET_D = "M600 110 L860 450 M860 110 L600 450 M730 90 V470 M590 280 H870 M620 160 Q730 230 840 160 M620 400 Q730 330 840 400"
net = (f'<path id="net4" d="{NET_D}" fill="none" stroke="#f2f0ff" stroke-width="7" stroke-linecap="round" stroke-dasharray="2400" stroke-dashoffset="2400"/>'
       + "".join(f'<g class="nv">{A.virus(x, y, 18, cls="nvi")}</g>' for x, y in ((655, 180), (810, 220), (690, 390), (815, 395))))
S4 = f'''<div class="navy"></div><div id="dots4" class="dots"></div>
<div id="pn4" class="panel"><div class="ptitle">NEUTRO'S 3 MOVES</div>
 {svg(f'{eat}{spray}{net}', 880, 650)}
 {chip("l4a", "EAT", COLS[0] - 58, 505, bg="#5AE68C", size=46)}
 {chip("l4b", "SPRAY", COLS[1] - 88, 505, bg="#d6f03a", size=46)}
 {chip("l4c", "NET", COLS[2] - 58, 505, bg="#f2f0ff", size=46)}
</div>
<div id="cd4" class="card" style="border-left-color:{PINK}"><h3 style="color:#b0457a">GEORGE 2021 · REVIEW</h3><p>Eat germs, toxic sprays, sticky NETs.</p></div>'''

SLX0, SLX1, SLY = 150, 930, 640
S5 = f'''{svg(f"""<g transform="translate(0,-150)"><g id="qs5">{A.queen_snow(W, H + 300, "qs")}</g></g>
 <rect x="60" y="430" width="960" height="320" rx="32" fill="#0f2236" opacity=".88" stroke="#24425f" stroke-width="4"/>
 <defs><linearGradient id="sl5" x1="0" x2="1"><stop offset="0" stop-color="#5AE68C"/><stop offset=".5" stop-color="#FFD166"/><stop offset="1" stop-color="#FF7A59"/></linearGradient></defs>
 <rect id="bar5" x="{SLX0}" y="{SLY - 20}" width="{SLX1 - SLX0}" height="40" rx="20" fill="url(#sl5)" stroke="{A.INK}" stroke-width="6"/>
 <path id="rail5" d="M{SLX0} {SLY - 34} H{SLX1} M{SLX0} {SLY + 34} H{SLX1}" stroke="#a7afbd" stroke-width="6" stroke-dasharray="900" stroke-dashoffset="900"/>""")}
<div id="hp5" class="slab" style="left:90px;top:470px;width:300px;color:#5AE68C">HELPFUL</div>
<div id="hm5" class="slab" style="left:690px;top:470px;width:300px;color:#FF7A59">HARMFUL</div>
<div id="kn5W" class="ntw" style="left:{SLX0 - 78}px;top:{SLY - 150}px;transform:scale(.26)">{neutro_html("kn5", "idle")}</div>
<div class="snowW" style="position:absolute;inset:0;overflow:hidden">{snow("s5", 40, 5, 0, 1600, (6, 13))}</div>
<div id="cd5" class="card" style="border-left-color:#9fc3e8"><h3 style="color:#1e56ac">GEORGE 2021 · McMASTER</h3><p>A thin line: helpful vs harmful.</p></div>'''

rnd6 = random.Random(6)
swarm = "".join(f'<g class="sw" data-x="{x:.0f}" data-y="{y:.0f}"><g transform="translate({tx:.0f},{ty:.0f})"><circle r="23" fill="{PINK}" stroke="{A.INK}" stroke-width="5"/>'
                f'<circle cx="-7" cy="-5" r="7" fill="#6f45a3"/><circle cx="7" cy="-5" r="7" fill="#6f45a3"/></g></g>'
                for x, y, tx, ty in [(rnd6.choice((-420, 420)), rnd6.uniform(-200, 200), rnd6.choice((270, 330, 390, 490, 550, 610)) , rnd6.uniform(250, 560)) for _ in range(12)])
S6 = f'''<div class="navy"></div><div id="dots6" class="dots"></div>
<div id="pn6" class="panel"><div class="ptitle">IN SEVERE FLU</div>
 {svg(f'{A.lungs(440, 370, 1.22, "lg6")}<g id="sw6">{swarm}</g>', 880, 650)}
 {chip("c6", "SAME MOVES", 560, 110, bg=PINK, size=42)}
</div>
<div id="cd6" class="card" style="border-left-color:#FF7A59"><h3>LAMICHHANE 2019</h3><p>Same cells: protection or damage.</p></div>'''

S7 = f'''{svg(f'<g id="ph7">{A.pharmacy_nps(W, H, "pq", shop=False)}</g>')}
<div class="bgfill" style="background:rgba(12,22,34,.25)"></div>
{NT("n7", 290, 230, .82, "cross")}
{chip("c7", "AMAZING", 80, 300, bg="#5AE68C", size=50)}
<div id="st7" class="stamp" style="left:110px;top:640px;font-size:96px">TOO HARD</div>'''

S8 = f'''{svg(f'<g id="ph8">{A.pharmacy_nps(W, H, "ph", py=200)}</g>')}
<div id="t8" class="big" style="top:228px;left:60px;width:880px;font-size:84px;color:#5AE68C">YEARLY FLU SHOT</div>
<div id="sh8" class="lot" style="left:420px;top:390px;width:240px;height:280px"></div>
{NT("n8", 700, 470, .5, "cross")}
<div id="cd8" class="card" style="border-left-color:#2fa36b"><h3 style="color:#1f7a45">GEORGE 2021</h3><p>Yearly flu shot = best defence. Not medical advice.</p></div>'''

S9 = f'''<div class="bgfill" style="background:linear-gradient(#1d2650 0%,#4a3f78 40%,#c9707a 70%,#f2a77a 86%)"></div>
{svg(f'<g>{A.skyline(W, H, 760, .9, seed=13, lit=.35, cn=990)}</g><g>{A.union_station(W, 1500, "o9us")}</g>')}
<div id="pn9" class="panel" style="top:220px;height:600px;background:rgba(15,34,54,.95)">
 <div id="sub9" class="subbtn" style="background:#FF7A59;color:#0c1622">SUBSCRIBE</div>
 <div id="subd9" class="subbtn" style="background:#3a4a5e;color:#FAF4E8;opacity:0;font-size:60px">SUBSCRIBED ✓</div>
 <div id="like9" style="position:absolute;left:760px;top:80px;font:100px InterBlack;opacity:0">👍</div>
 <div style="position:absolute;left:40px;top:262px;font:34px InterBlack;color:#FFD166;letter-spacing:.05em">SOURCES</div>
 <div id="src9" style="position:absolute;left:40px;top:318px;width:800px;font:38px/1.4 InterSB;color:#cfe0ff">
  George 2021 · Lamichhane 2019<br><span style="color:#96b0c4;font-size:34px">Links in the description<br>Not medical advice</span></div>
</div>
{NT("n9", 600, 967, .82, "cross")}'''

S10 = hook("h10")

scenes = [("s1", 0, C1, S1), ("s2", C1, C2, S2), ("s3", C2, C3, S3), ("s4", C3, C4, S4), ("s5", C4, C5, S5), ("s6", C5, C6, S6),
          ("s7", C6, C7, S7), ("s8", C7, C8, S8), ("s9", C8, C9, S9), ("s10", C9, T, S10)]
scene_html = "\n".join(f'<div id="{i}" class="scene clip" data-start="{a}" data-duration="{round(b - a, 3)}">{h}</div>' for i, a, b, h in scenes)

# ------------------------------------------------------------------ timeline beats
J = []
def j(s): J.append(s)
for _, a, b, _h in scenes[:-1]:
    j(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:{b - a - 0.05:.3f},ease:"sine.inOut",immediateRender:false}},{a + 0.01:.3f});')
j(f'tl.set("#cam",{{scale:1}},{C9});')
j('const punch=(t,s=1.07)=>{tl.to("#shaker",{scale:s,duration:0.08,ease:"power2.out"},t);tl.to("#shaker",{scale:1,duration:0.35,ease:"back.out(2)"},t+0.08);};')
j('const pop=(s,t,from=0)=>tl.fromTo(s,{scale:from,opacity:0},{scale:1,opacity:1,duration:0.34,ease:"back.out(2.8)"},t);')
j('const out=(s,t)=>tl.to(s,{opacity:0,scale:0.7,duration:0.15,ease:"power2.in"},t);')
j('const stamp=(s,t,r=-8)=>tl.fromTo(s,{scale:3,opacity:0,rotation:r-6},{scale:1,opacity:1,rotation:r,duration:0.24,ease:"back.out(1.6)"},t);')
j('const slideIn=(s,t)=>tl.fromTo(s,{x:90,opacity:0},{x:0,opacity:1,duration:0.35,ease:"back.out(1.8)",immediateRender:false},t);')
for t in (tNeutro, tSix2, tFirst2, tBouncer, tHarmful, tHurt, tSwings + 0.1, tShot):
    j(f"punch({t:.3f});")
j('tl.set("#shaker",{x:0,y:0,scale:1},0);')
for b, a, d in (("#dots4", C3, C4 - C3), ("#dots6", C5, C6 - C5)):
    j(f'tl.fromTo("{b}",{{x:0,y:0}},{{x:70,y:140,duration:{d:.3f},ease:"none"}},{a});')
for t, pos in ((0, POS_HOOK), (C1, POS_BIG), (C2, POS_V2), (C9, POS_HOOK)):
    j(f'tl.set("#cytoPos",{json.dumps(pos)},{t});')
j(f'tl.set("#cytoPos",{json.dumps(POS_HOOK)},{T - 0.01});')
j(f'gsap.set("#cytoPos",{json.dumps(POS_HOOK)});gsap.set("#shaker",{{x:0,y:0,scale:1}});')
# cup down for the serious lungs beat, back up for the payoff
j(f'tl.set("#cupTable",{{opacity:0}},0);tl.set("#cup",{{opacity:0}},{C5 + 0.05});tl.fromTo("#cupTable",{{opacity:1,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"bounce.out",immediateRender:false}},{C5 + 0.05});'
  f'tl.set("#cup",{{opacity:1}},{C6 + 0.05});tl.set("#cupTable",{{opacity:0}},{C6 + 0.05});')

# ---- S1 hook: 3 movers max (caption, Cyto, Neutro). Neutro stands at the door from frame 0; nods + brows up on his name
j(neutro_js("h1n", brows=[(tNeutro - 0.05, "up"), (tNeutro + 0.5, "down")], nods=[tNeutro], blinks=[1.2]))
j(f'tl.to("#h1t",{{y:-30,opacity:0,duration:0.2,ease:"power2.in"}},{C1 - 0.25});')
# ---- S2 catchphrase
j(f'document.querySelectorAll("#h2City .win").forEach((w,i)=>{{ if(i%4==0) tl.to(w,{{opacity:.2,duration:0.3,repeat:7,yoyo:true}},{C1}+(i%9)*0.2); }});')
j(f'tl.fromTo("#h2City",{{y:80}},{{y:0,duration:{C2 - C1:.3f},ease:"power2.out"}},{C1});')
j(f'tl.set("#t2a",{{opacity:0}},0);tl.fromTo("#t2a",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(1.7)"}},{tLive - 0.05});')
j(f'tl.set("#t2c",{{opacity:0}},0);tl.fromTo("#t2c",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.34,ease:"back.out(2.4)"}},{tInside});')
j(f'tl.to(["#t2a","#t2c"],{{opacity:0,duration:0.15}},{C2 - 0.2});')
# ---- S3 rush-hour Line 1: sneeze cloud passes rider to rider; Neutro slides in, first on the scene, bouncer flex
j(f'tl.fromTo("#bpTrain",{{x:900}},{{x:0,duration:0.9,ease:"power3.out"}},{C2});')
j(f'tl.fromTo("#rid3",{{x:900}},{{x:0,duration:0.9,ease:"power3.out"}},{C2});')
j(f'tl.fromTo("#sn3",{{x:-120}},{{x:1180,duration:{tFirst2 - C2 - 0.6:.2f},ease:"none"}},{C2 + 0.6});')
j(f'tl.fromTo("#sn3i",{{scale:.6}},{{scale:1.15,duration:0.5,yoyo:true,repeat:{int((tFirst2 - C2) / 0.5)},ease:"sine.inOut",svgOrigin:"0 0"}},{C2 + 0.6});')
j(f'document.querySelectorAll("#rid3 .rid").forEach((r,i)=>tl.to(r,{{y:-14,rotation:-6,duration:0.12,yoyo:true,repeat:1,transformOrigin:"50% 100%"}},{C2 + 0.75}+i*{(tFirst2 - C2 - 0.8) / 10:.3f}));')
j(f'tl.to("#sn3i",{{scale:0,opacity:0,duration:0.25,ease:"back.in(2)",svgOrigin:"0 0"}},{tFirst2 - 0.05});')
j(f'tl.fromTo("#rc3Tail",{{rotation:-10,svgOrigin:"-40 -30"}},{{rotation:12,svgOrigin:"-40 -30",duration:0.45,yoyo:true,repeat:{int((C3 - C2) / 0.45)},ease:"sine.inOut",immediateRender:false}},{C2});')
j(f'tl.fromTo("#bpMin",{{opacity:1}},{{opacity:.35,duration:0.3,repeat:{int((C3 - C2) / 0.3)},yoyo:true}},{C2});')
j(f'tl.set("#c3",{{opacity:0}},0);pop("#c3",{tAir - 0.05});out("#c3",{tFirst2 - 0.25});')
j(f'tl.set("#n3W",{{opacity:0}},0);tl.fromTo("#n3W",{{x:700,opacity:1}},{{x:0,opacity:1,duration:0.45,ease:"back.out(1.6)",immediateRender:false}},{tNphil - 0.1});')
j(neutro_js("n3", poses=[(tBouncer - 0.05, "flex"), (tKnow, "cross")], brows=[(tNphil + 0.4, "down"), (tBouncer - 0.05, "up"), (tKnow, "down")],
            mouths=[(tBouncer - 0.05, "open"), (tEnergy + 0.3, "smirk")], nods=[tDun, tKnow + 0.1], looks=[(tNphil + 0.5, -7, 0)], blinks=[tScene]))
j(f'tl.set("#st3",{{opacity:0}},0);stamp("#st3",{tFirst2 - 0.03},-5);out("#st3",{tBouncer - 0.22});')
j(f'tl.set("#b3",{{opacity:0}},0);pop("#b3",{tBouncer - 0.03});out("#b3",{C3 - 0.2});')
# ---- S4 three moves: eat (chomp), spray (granules burst), net (strands draw on, viruses stick)
j(f'tl.fromTo("#pn4",{{y:900}},{{y:0,duration:0.45,ease:"back.out(1.1)"}},{C3});')
j(f'gsap.set("#jaw4",{{svgOrigin:"0 10"}});tl.fromTo("#jaw4",{{scaleY:1}},{{scaleY:0.1,duration:0.12,yoyo:true,repeat:7,ease:"power2.inOut"}},{tEat - 0.05});')
j(f'document.querySelectorAll("#pn4 .eg").forEach((g,i)=>tl.to(g,{{x:-{170}-i*50,opacity:0,duration:0.3,ease:"power2.in"}},{tEat}+i*0.18));')
j(f'document.querySelectorAll("#pn4 .dr circle").forEach((c,i)=>{{const a=(+c.dataset.a)*Math.PI/180;tl.fromTo(c,{{attr:{{cx:0,cy:0}},opacity:0}},{{attr:{{cx:Math.cos(a)*118,cy:Math.sin(a)*118}},opacity:1,duration:0.4,ease:"back.out(2)"}},{tToxic});'
  f'tl.to(c,{{attr:{{cx:Math.cos(a)*104,cy:Math.sin(a)*104}},duration:0.4,yoyo:true,repeat:3,ease:"sine.inOut"}},{tToxic + 0.4});}});')
j(f'tl.to("#net4",{{strokeDashoffset:0,duration:0.7,ease:"power2.out"}},{tSticky - 0.1});')
j(f'document.querySelectorAll("#pn4 .nv").forEach((g,i)=>tl.fromTo(g,{{opacity:0,y:-140}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},{tNets - 0.1}+i*0.07));')
j(f'tl.set(["#l4a","#l4b","#l4c"],{{opacity:0}},0);pop("#l4a",{tEat - 0.05});pop("#l4b",{tToxic - 0.05});pop("#l4c",{tSticky - 0.05});')
j(f'tl.set("#cd4",{{opacity:0}},0);slideIn("#cd4",{tGerms + 0.1});')
# ---- S5 thin line over snowy Queen St: GO train crosses behind, mini-Neutro knob slides helpful -> harmful
j(snow_js("s5", C4, C5, 1800))
j(f'tl.fromTo("#qsGo",{{x:1100}},{{x:-2700,duration:{C5 - C4 + 1:.2f},ease:"none"}},{C4});')
j(f'tl.to("#rail5",{{strokeDashoffset:0,duration:0.6,ease:"power2.out"}},{C4 + 0.1});')
j(f'tl.fromTo("#bar5",{{scaleX:0,svgOrigin:"{SLX0} {SLY}"}},{{scaleX:1,svgOrigin:"{SLX0} {SLY}",duration:0.6,ease:"power2.out"}},{C4 + 0.1});')
j(f'tl.set(["#hp5","#hm5"],{{opacity:0}},0);pop("#hp5",{tHelpful - 0.05});pop("#hm5",{tHarmful - 0.05});')
j(f'tl.set("#kn5W",{{opacity:0}},0);tl.fromTo("#kn5W",{{scale:0,opacity:0}},{{scale:.26,opacity:1,duration:0.34,ease:"back.out(2.8)"}},{tThin - 0.1});')
j(f'tl.fromTo("#kn5W",{{x:0}},{{keyframes:[{{x:{(SLX1 - SLX0) * .45:.0f},duration:0.6}},{{x:{(SLX1 - SLX0) * .2:.0f},duration:0.35}},{{x:{(SLX1 - SLX0) * .5:.0f},duration:0.5}}],ease:"sine.inOut",immediateRender:false}},{tThin});'
  f'tl.to("#kn5W",{{x:{(SLX1 - SLX0) * .86:.0f},duration:0.45,ease:"back.out(1.6)"}},{tHarmful - 0.05});')
j(neutro_js("kn5", mouths=[(tHarmful, "open")], brows=[(tHarmful, "up")]))
j(f'tl.set("#cd5",{{opacity:0}},0);slideIn("#cd5",{tMcM});')
# ---- S6 lungs: neutrophils swarm in, then the damage (cup down, drums out)
j(f'tl.fromTo("#pn6",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{C5});')
j(f'document.querySelectorAll("#sw6 .sw").forEach((g,i)=>tl.fromTo(g,{{x:+g.dataset.x,y:+g.dataset.y,opacity:0}},{{x:0,y:0,opacity:1,duration:0.5,ease:"back.out(1.4)"}},{tSame - 0.1}+i*0.05));')
j(f'tl.to(["#lg6L","#lg6R"],{{fill:"#d9485f",duration:0.4}},{tHurt});')
j(f'document.querySelectorAll("#lg6Hurt .crk").forEach((c,i)=>tl.to(c,{{strokeDashoffset:0,duration:0.3}},{tHurt}+i*0.08));')
j(f'tl.fromTo("#lg6",{{x:0}},{{x:8,duration:0.06,yoyo:true,repeat:7}},{tHurt + 0.05});')
j(f'tl.set("#c6",{{opacity:0}},0);pop("#c6",{tSame - 0.05});')
j(f'tl.set("#cd6",{{opacity:0}},0);slideIn("#cd6",{tSevere + 0.1});')
# ---- S7 Nathan Phillips Square: Neutro flexes on "amazing", swings too hard, skaters topple
j(f'document.querySelectorAll("#pqSkaters .sk").forEach((s,i)=>tl.fromTo(s,{{x:0}},{{x:(i%2?-60:60),duration:1.2,yoyo:true,repeat:2,ease:"sine.inOut"}},{C6}));')
j(neutro_js("n7", poses=[(tAmazing - 0.05, "flex"), (tSwings - 0.05, "idle"), (tHard + 0.3, "cross")], mouths=[(tAmazing, "open"), (tAmazing + 0.5, "smirk"), (tSwings, "open"), (tHard + 0.4, "frown")],
            brows=[(tAmazing - 0.05, "up"), (tSwings - 0.05, "down")], blinks=[C6 + 0.3]))
j(f'tl.to("#n7",{{rotation:-14,svgOrigin:"300 650",duration:0.12,ease:"power2.in"}},{tSwings});tl.to("#n7",{{rotation:9,duration:0.18,ease:"power3.out"}},{tSwings + 0.12});tl.to("#n7",{{rotation:0,duration:0.4,ease:"elastic.out(1,0.4)"}},{tSwings + 0.3});')
j(f'document.querySelectorAll("#pqSkaters .sk").forEach((s,i)=>tl.to(s,{{rotation:(i%2?80:-80),y:10,transformOrigin:"50% 100%",duration:0.3,ease:"bounce.out"}},{tSwings + 0.15}+i*0.06));')
j(f'tl.set("#c7",{{opacity:0}},0);pop("#c7",{tAmazing - 0.05});out("#c7",{tSwings - 0.22});')
j(f'tl.set("#st7",{{opacity:0}},0);stamp("#st7",{tToo - 0.05},-6);')
# ---- S8 pharmacy + NPS rink: yearly flu shot, shield, Neutro nods
j(f'document.querySelectorAll("#phSkaters .sk").forEach((s,i)=>tl.fromTo(s,{{x:0}},{{x:(i%2?-50:50),duration:1.1,yoyo:true,repeat:2,ease:"sine.inOut"}},{C7}));')
j(f'tl.fromTo("#phSign",{{scale:1,svgOrigin:"200 655"}},{{scale:1.12,svgOrigin:"200 655",duration:0.18,yoyo:true,repeat:3,ease:"sine.inOut"}},{tShot - 0.1});')
j(f'tl.set("#t8",{{opacity:0}},0);pop("#t8",{tYearly - 0.05});')
j(lot("sh8", "shield-2.json", tDefence - 0.1, C8, loops=1))
j(f'tl.set("#sh8",{{opacity:0}},0);tl.fromTo("#sh8",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{tDefence - 0.1});')
j(neutro_js("n8", nods=[tShot, tFam], brows=[(tShot - 0.05, "up")], mouths=[(tShot - 0.05, "smirk")], blinks=[C7 + 0.5]))
j(f'tl.set("#cd8",{{opacity:0}},0);slideIn("#cd8",{tNot - 0.15});')
# ---- S9 outro
j(f'tl.fromTo("#pn9",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:0.38,ease:"back.out(1.8)"}},{C8 + 0.05});')
j(f'tl.fromTo("#like9",{{scale:0,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.32,ease:"back.out(3)"}},{tLike});')
j(f'tl.fromTo("#sub9",{{scale:1}},{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},{tSub + 0.15});'
  f'tl.set("#subd9",{{opacity:0}},0);tl.set("#subd9",{{opacity:1}},{tSub + 0.25});tl.set("#sub9",{{opacity:0}},{tSub + 0.25});')
j(f'tl.fromTo("#src9",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{C8 + 0.2});')
j(neutro_js("n9", poses=[(tWagwan - 0.05, "flex"), (C9 - 0.15, "cross")], mouths=[(tNeutro3, "open"), (tNeutro3 + 0.4, "smirk"), (tWagwan, "open")],
            brows=[(tNeutro3 - 0.05, "up")], nods=[tTell]))
# ---- S10 loop frame = hook frame
j(neutro_js("h10n"))
j(f'tl.fromTo("#s10",{{opacity:0}},{{opacity:1,duration:0.18}},{C9});')

CSS = f"""
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:InterXB; }}
#cam, #shaker {{ position:absolute; inset:0; transform-origin:540px 960px; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.bgfill {{ position:absolute; inset:0; }}
.lot {{ position:absolute; }}
.ntw {{ position:absolute; width:600px; height:720px; transform-origin:0 0; z-index:15; }}
.navy {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #17304d 0%, #0c1622 70%); }}
.dots {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; background-image:radial-gradient(rgba(120,170,220,.10) 3px, transparent 4px); background-size:70px 70px; }}
.big {{ position:absolute; left:0; width:1080px; text-align:center; font-family:InterBlack; line-height:.95; letter-spacing:-2px;
  paint-order:stroke fill; -webkit-text-stroke:14px #0c1622; text-shadow:0 10px 0 #0c1622; opacity:0; z-index:30; }}
.chip {{ position:absolute; font-family:InterBlack; letter-spacing:.03em; padding:10px 22px; border-radius:30px; border:5px solid #0c1622;
  box-shadow:0 6px 0 #0c1622; white-space:nowrap; opacity:0; color:#0c1622; z-index:30; }}
.stamp {{ position:absolute; font:120px InterBlack; color:#FF7A59; padding:6px 30px; border:12px solid #FF7A59; border-radius:24px;
  background:rgba(12,22,34,.88); transform:rotate(-8deg); opacity:0; letter-spacing:.02em; z-index:40; white-space:nowrap; }}
.slab {{ position:absolute; text-align:center; font:52px InterBlack; paint-order:stroke fill; -webkit-text-stroke:8px #0c1622; z-index:30; }}
.flake {{ position:absolute; border-radius:50%; background:#FAF4E8; }}
.subbtn {{ position:absolute; left:150px; top:70px; width:580px; height:140px; border-radius:70px; border:7px solid #0c1622; box-shadow:0 10px 0 #0c1622;
  font:64px InterBlack; text-align:center; line-height:126px; }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-210px; width:420px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
{R.rig3_css()}
{C.CAP_CSS}
{C.V2_CSS}
.card p {{ font-size:34px; }}
{C.TR_CSS}
#cytoLayer {{ position:absolute; inset:0; z-index:20; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<script src="assets/lottie_svg.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<audio id="mix" class="clip" src="assets/audio.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="shaker" class="clip" data-start="0" data-duration="{T}"><div id="cam">
{scene_html}
  <div id="cytoLayer">{R.rig3_html("outfit_hoodie", "cup_red")}</div>
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
json.dump({"name": "ep13"}, open("meta.json", "w"))
print("built", len(html), "bytes; T", T, "cuts", CUTS, "words", len(WORDS), "voice", round(TM["total"], 2))
