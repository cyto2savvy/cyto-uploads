"""EP12 — Movember: Does Checking Yourself Save Lives? (6ixty Seconds of Science / Cyto vs Disease).
Started from hf/template/build.py (v2 layout + v3 rig); scene structure follows hf/ep11/build.py.
Test upgrades: U1 word times from ElevenLabs Scribe (timing.json via ep12/make_segs.py), U2 syllable visemes + acting on
stressed words, U3 ElevenLabs SFX (whoosh/pop/hit/chime) mixed ~-18 dB under the voice + quiet synth bed, U4 overshoot/
secondary motion/push-ins.   python3 build.py -> index.html + assets/audio.wav"""
import json, sys, os, subprocess, random, shutil, re
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import numpy as np
import cytohf as C, cyto3 as R, art as A
from engine import tone, noise, hp, lp, add, load_mono, SR

P = "/home/claude/hf/ep12"; os.chdir(P)
V = "/home/claude/ep12"
TM = json.load(open(f"{V}/timing.json")); WORDS = TM["words"]
W, H = 1080, 1920


def wt(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and re.sub(r"[^a-z0-9%']", "", w["w"].lower()) == re.sub(r"[^a-z0-9%']", "", word.lower()):
            return round(w["t0"], 3)
    raise KeyError(word)


# ------------------------------------------------------------------ word beats (exact-word match, Scribe times)
tMov, tReal, tBro = wt("Movember"), wt("Real"), wt("bro")
tYo, tCyto, tLive, t6ix, tInside = wt("Yo"), wt("Cyto"), wt("live"), wt("6ix"), wt("inside")
tTest, tMost, tGuys, t15, t45 = wt("Testicular"), wt("most"), wt("guys"), wt("15"), wt("45")
tGood, tNews, t95, tAlive, tYears = wt("good"), wt("news"), wt("95%"), wt("alive"), wt("years")
tNow, tTwist, tDoes, tEvery, tMonth, tSave, tLives = wt("Now"), wt("twist"), wt("Does"), wt("every"), wt("month"), wt("save"), wt("lives")
tNobody, tProven, tUS, tDoesnt, tRec, tRoutine = wt("Nobody's"), wt("proven"), wt("US"), wt("doesn't"), wt("recommend"), wt("routine")
tEvid, tStrong, tEither, tStyll = wt("evidence"), wt("strong"), wt("either"), wt("styll")
tBut2, tIgnore, tBody2, tKnow, tNormal = wt("But", 25), wt("ignore"), wt("body", 26), wt("Know"), wt("normal")
tLump, tSwell, tSomething, tOff, tDont, tWait, tSee, tDoctor, tFam = wt("lump"), wt("swelling"), wt("something"), wt("off"), wt("Don't"), wt("wait"), wt("See"), wt("doctor"), wt("fam")
tGrow, tStache, t6ix2, tBook, tCheckup, tNot, tAdvice = wt("Grow"), wt("'stache"), wt("6ix", 34), wt("book"), wt("checkup"), wt("Not"), wt("advice")
tLike, tSub, tTake, tYourself = wt("Like"), wt("subscribe"), wt("take"), wt("yourself")
END_V = WORDS[-1]["t1"]

C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 = 2.45, 6.58, 10.82, 14.80, 18.80, 22.63, 25.66, 29.03, 33.40, 37.30
SIPS = [(round(END_V + 0.08, 2), 0.62)]
C11 = round(SIPS[0][0] + SIPS[0][1] + 0.05, 2)
T = round(C11 + 0.55, 2)
CUTS = (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10)

# ------------------------------------------------------------------ assets
LOTS = ["shield-2.json", "steth-1.json", "heart-beat.json"]
C.copy_assets_v2(P, lotties=LOTS)


# ------------------------------------------------------------------ audio (U3): quiet calm bed + ElevenLabs SFX at ~-18 dB under the voice
def load_sfx(name, max_len):
    x = load_mono(f"{V}/sfx/{name}.wav", SR)
    env = np.abs(x); thr = env.max() * 0.004
    nz = np.where(env > thr)[0]
    x = x[nz[0]: min(len(x), nz[0] + int(max_len * SR))] if len(nz) else x[: int(max_len * SR)]
    f = min(len(x), int(0.08 * SR)); x[-f:] *= np.linspace(1, 0, f)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)          # unit RMS; gain set at mix time


def pad(m, dur, g=0.035):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.8).clip(0, 1)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3.01 * f * t)) * env * g


def make_audio(sfx_events):
    n = int((T + 0.3) * SR); music = np.zeros(n, np.float32)
    BAR = 60 / 80 * 4
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]   # Am7 Fmaj7 Cmaj7 G7 — calm
    t = 0.0; i = 0
    while t < T + 0.3:
        for m in chords[i % 4]: add(music, pad(m, BAR + 0.9), t)
        add(music, pad(chords[i % 4][0] - 12, BAR + 0.5, 0.05), t)
        t += BAR; i += 1
    kick = tone(110, 45, 0.3, 0.1) * 0.5
    hat = hp(noise(0.03, 2), 0.6) * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.008) * 0.07
    BEAT = 60 / 80; t = C1; s = 0
    while t < T + 0.3:
        serious = (C7 - 0.05 <= t < C9 - 0.05)          # cup-down beat: drums drop out
        if not serious:
            if s % 4 == 0: add(music, kick, t)
            add(music, hat, t + BEAT / 2)
        t += BEAT; s += 1
    music = lp(music, 0.3)
    v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    vrms = np.sqrt(np.mean(vv[np.abs(vv) > 0.02] ** 2))
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.6 * np.clip(env * 3, 0, 1))
    music *= vrms * 10 ** (-24 / 20) / (np.sqrt(np.mean(music ** 2)) + 1e-9)       # bed ~-24 dB under the voice
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


SFX = [("pop", tMov), ("hit", tReal), ("pop", tCyto), ("hit", t6ix), ("pop", tInside),
       ("pop", tTest), ("pop", t15), ("pop", t45), ("chime", t95 + 0.25), ("pop", tAlive),
       ("hit", tTwist), ("pop", tDoes + 0.1), ("hit", tLives), ("hit", tProven), ("pop", tUS), ("pop", tDoesnt + 0.2),
       ("pop", tEither), ("pop", tStyll), ("pop", tKnow), ("pop", tLump), ("pop", tSwell), ("pop", tSomething),
       ("hit", tDont), ("pop", tDoctor), ("pop", tStache), ("chime", tBook + 0.15), ("pop", tNot), ("pop", tLike),
       ("pop", tSub + 0.15), ("chime", tTake)]
SFX += [("whoosh", c - 0.22) for c in CUTS]
make_audio(SFX)

# ------------------------------------------------------------------ Cyto: outfit, positions, acting (U2)
STACHE = f'<g id="stacheW"><g id="stache">{A.handlebar(591, 703, 150)}</g></g>'
RIBBON = f'<g id="ribbonPin">{A.awareness_ribbon(800, 520, 0.85)}</g>'
POS_HOOK, POS_BIG, POS_V2 = C.place(330, 1335, 0.60), C.place(330, 1300, 0.64), C.CYTO_V2
mouth = R.viseme_track(f"{V}/voice.wav", WORDS)
if mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
blinks = [(t, 0.1) for t in (1.6, 4.4, 7.4, 10.4, 13.1, 16.6, 19.8, 22.3, 25.2, 28.2, 31.0, 33.0, 35.9, 38.4)]
gest = dict(sips=SIPS, raises=[(tCyto, 0.6), (t95 - 0.05, 0.7), (tStache - 0.05, 0.7)], waves=[tYo, tTake - 0.05],
            points=[(t15 - 0.05, 0.9), (tAlive - 0.05, 0.7), (tProven - 0.05, 0.6), (tDoctor - 0.08, 0.7)],
            tilts=[(tBro, 0.5, -7), (tStyll, 0.7, 8), (tFam, 0.6, -7), (t6ix2, 0.5, 7), (tNormal, 0.6, 5)],
            shrugs=[(tNobody, 0.6), (tEither, 0.6)])
expr = [(tMov - 0.02, 0.6, "hype"), (tReal - 0.05, 1.0, "squint"), (tCyto - 0.05, 0.5, "hype"), (t6ix, 0.5, "hype"),
        (tTest - 0.05, 1.2, "skeptic"), (tGood - 0.05, 0.6, "hype"), (t95 - 0.05, 0.7, "hype"),
        (tTwist - 0.05, 0.7, "shock"), (tLives - 0.05, 0.7, "skeptic"), (tNobody - 0.05, 0.8, "skeptic"), (tUS - 0.02, 1.0, "squint"),
        (tStrong - 0.05, 0.8, "skeptic"), (tStyll, 0.6, "squint"), (tBut2 - 0.05, 1.4, "sad"), (tKnow - 0.05, 0.8, "squint"),
        (tLump - 0.05, 0.9, "squint"), (tDont - 0.05, 0.6, "shock"), (tDoctor - 0.05, 0.5, "hype"),
        (tStache - 0.05, 0.7, "hype"), (tBook - 0.05, 0.5, "hype"), (tNot - 0.05, 0.9, "squint"), (tLike - 0.05, 0.5, "hype"), (tTake - 0.05, 0.6, "hype")]
looks = [(C2 + 0.3, 6, -6), (C3 + 0.6, 6, -6), (C4 + 1.4, 6, -6), (C5 + 0.4, 6, -5), (C6 + 0.3, 6, -6), (C7 + 1.5, 6, -6), (C8 + 0.4, 6, -6)]
rig_js = R.rig3_js(mouth, T, blinks=blinks, mute=[(s[0], 0) for s in SIPS], expr=expr, looks=looks, **gest)
R.mix_sips("assets/base.wav", [s[0] for s in SIPS], "assets/audio.wav")

# ------------------------------------------------------------------ captions + transitions
KEYS = {"bro": "#3fc1b0", "cyto": "#3fc1b0", "testicular": "#9fc3e8", "cancer": "#9fc3e8", "common": "#FFD166", "15": "#FFD166", "45": "#FFD166",
        "good": "#5AE68C", "news": "#5AE68C", "95": "#5AE68C", "alive": "#5AE68C", "twist": "#FF7A59", "checking": "#FFD166", "month": "#FFD166",
        "lives": "#FF7A59", "nobodys": "#FF7A59", "proven": "#FF7A59", "us": "#9fc3e8", "routine": "#9fc3e8", "evidence": "#c4b0ff",
        "strong": "#c4b0ff", "styll": "#3fc1b0", "ignore": "#FF7A59", "normal": "#5AE68C", "lump": "#FFD166", "swelling": "#FFD166",
        "off": "#FFD166", "wait": "#FF7A59", "doctor": "#5AE68C", "fam": "#3fc1b0", "stache": "#c4b0ff", "6ix": "#FFD166",
        "checkup": "#5AE68C", "subscribe": "#FF7A59"}
CAPW = [w for w in WORDS if not (w["t0"] < 0.5) and not (tLive - 0.01 <= w["t0"] < C2)]
cap_html, cap_js = C.captions(CAPW, KEYS, y=C.CAP_Y_V2)
last_cap = cap_html.count('"cap clip"') - 1
cap_js += f'\ntl.set("#cap{last_cap}",{{opacity:0}},{C11});'
_m = [m for m in re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'CYTO,' in m.group(2)][0]
cap_js += f'\ntl.set("#{_m.group(1)}",{{opacity:1}},0);tl.set("#{_m.group(1)}",{{opacity:0}},{tLive - 0.03});'
TRS = [C.transition(k, t) for k, t in (("zoom", C1), ("whip", C2), ("doors", C3), ("membrane", C4), ("whip", C5), ("zoom", C6),
                                        ("membrane", C7), ("whip", C8), ("doors", C9), ("zoom", C10))]
tr_html = "\n".join(h for h, _ in TRS); tr_js = "\n".join(j for _, j in TRS)


# ------------------------------------------------------------------ helpers
def chip(id_, text, left, top, bg="#FFD166", fg=A.INK, size=40, extra=""):
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


def svg(inner, w=W, h=H, style="position:absolute;left:0;top:0;overflow:visible"):
    return f'<svg width="{w}" height="{h}" style="{style}">{inner}</svg>'


def guy(x, y, s=1.0, cls="guy"):
    """Generic person icon (head + shoulders + toque)."""
    return (f'<g transform="translate({x},{y}) scale({s})"><g class="{cls}"><path d="M-46 110 Q-46 40 0 40 Q46 40 46 110Z" fill="#4a5d7d" stroke="{A.INK}" stroke-width="6"/>'
            f'<circle cx="0" cy="0" r="34" fill="#f2c9a0" stroke="{A.INK}" stroke-width="6"/>'
            f'<path d="M-34 -6 Q-34 -46 0 -46 Q34 -46 34 -6Z" fill="#1e56ac" stroke="{A.INK}" stroke-width="6"/></g></g>')


# ------------------------------------------------------------------ scenes
def hook_bg(idp):
    """University Ave 'hospital row' at dawn, Queen's Park closing the avenue (Toronto background plan: hook)."""
    return f'''<div class="bgfill" style="background:linear-gradient(#27305e 0%,#6a4a86 38%,#d97a7a 62%,#ffbe8a 76%)"></div>
{svg(f'<g id="{idp}Sky">{A.stars(W, H, 18, 12, .2)}</g><g id="{idp}Ave">{A.univ_ave(W, 1000, idp)}</g>')}'''


S1 = hook_bg("h1") + '''
<div id="t1" class="big" style="top:250px;font-size:124px;color:#FFD166;opacity:1">MOVEMBER</div>'''

S2 = f'''<div class="bgfill" style="background:linear-gradient(#0a1024 0%,#1b2650 70%,#3a3f6b 85%)"></div>
{svg(f'{A.stars(W, H, 50, 21, .45)}<g id="h2City">{A.skyline(W, H, 1000, 1.05, seed=23, lit=.45, cn=760)}</g>')}
<div id="t2a" class="big" style="top:250px;font-size:170px;color:#FFD166"><span style="font-size:74px;color:#FAF4E8">LIVE FROM</span><br>THE 6IX</div>
{chip("t2c", "...INSIDE YOUR BODY", 300, 640, bg="#3fc1b0", size=42)}'''

guys = "".join(guy(110 + k * 110, 400, 1.15, f"guy g{k}") for k in range(7))
S3 = f'''<div class="navy"></div><div id="dots3" class="dots"></div>
<div id="pn3" class="panel"><div class="ptitle">MOST COMMON CANCER IN YOUNG GUYS</div>
 {svg(f"""<rect id="band3" x="150" y="300" width="560" height="270" rx="26" fill="#3fc1b0" opacity=".28"/>
  <path d="M60 600 H820" stroke="#96b0c4" stroke-width="8" stroke-linecap="round"/>
  {''.join(f'<path d="M{x} 588 V612" stroke="#96b0c4" stroke-width="6"/>' for x in range(60, 830, 55))}
  <g id="rb3" opacity="0">{A.awareness_ribbon(830, 290, 0.9)}</g>
  {guys}""", 880, 650)}
 <div id="p15" class="pin" style="left:150px;top:590px">15</div>
 <div id="p45" class="pin" style="left:710px;top:590px">45</div>
 <div id="t3" class="big" style="top:110px;font-size:120px;color:#FFD166;width:880px">AGE 15 TO 45</div>
</div>
<div id="cd3" class="card"><h3>THOMAS 2026 · REVIEW</h3><p>Most common cancer in men aged 15 to 45.</p></div>'''

PLAT = svg(f'<g id="plat">{A.subway_platform(W, H, "bp")}</g>')
RING_R = 190; RING_L = 2 * 3.14159 * RING_R
S4 = f'''{PLAT}
<div id="pn4" class="panel" style="top:300px;height:540px;background:rgba(15,34,54,.95)"><div class="ptitle">5 YEARS AFTER DIAGNOSIS</div>
 {svg(f"""<g transform="translate(270,290) rotate(-90)"><circle r="{RING_R}" fill="none" stroke="#24425f" stroke-width="48"/>
  <circle id="ring4" r="{RING_R}" fill="none" stroke="#5AE68C" stroke-width="48" stroke-linecap="round" stroke-dasharray="{RING_L:.1f}" stroke-dashoffset="{RING_L:.1f}"/></g>""", 880, 540)}
 <div id="t4" class="pct">95%</div>
 <div id="sh4" class="lot" style="left:560px;top:80px;width:260px;height:300px"></div>
 {chip("c4", "ALIVE", 600, 410, bg="#5AE68C", size=46)}
</div>
<div id="cd4" class="card"><h3>THOMAS 2026</h3><p>5-year survival is over 95%, all stages.</p></div>'''

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
cal = "".join(f'<g class="mo" transform="translate({60 + (k % 4) * 128},{110 + (k // 4) * 120})"><rect width="112" height="104" rx="14" fill="#FAF4E8" stroke="{A.INK}" stroke-width="5"/>'
              f'<rect width="112" height="30" rx="10" fill="{"#4f86ff" if k != 10 else "#FF7A59"}" stroke="{A.INK}" stroke-width="5"/>'
              f'<text x="56" y="24" text-anchor="middle" font-family="InterBlack" font-size="22" fill="#fff">{m}</text>'
              f'<path class="ck" d="M30 66 L50 86 L84 48" fill="none" stroke="#3fc1b0" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="80" stroke-dashoffset="80"/></g>'
              for k, m in enumerate(MONTHS))
S5 = f'''{svg(f'<g id="plat5">{A.subway_platform(W, H, "bq")}</g>')}
<div id="pn5" class="panel" style="top:300px;height:540px;background:rgba(15,34,54,.95)"><div class="ptitle">SELF-CHECK EVERY MONTH</div>
 {svg(f'<g id="cal5">{cal}</g>', 880, 540)}
 <div id="q5" class="big" style="top:70px;left:560px;width:300px;font-size:330px;color:#FF7A59">?</div>
</div>
<div id="tw5" class="stamp" style="left:250px;top:430px">TWIST</div>'''

S6 = f'''<div class="navy"></div><div id="dots6" class="dots"></div>
<div id="pn6" class="panel"><div class="ptitle">THE PROOF</div>
 {svg(f"""<g id="doc6"><rect x="260" y="110" width="360" height="460" rx="20" fill="#FAF4E8" stroke="{A.INK}" stroke-width="7"/>
   {''.join(f'<rect x="300" y="{y}" width="{w}" height="18" rx="9" fill="#cfd5dc"/>' for y, w in ((170, 260), (220, 220), (270, 250), (320, 180), (370, 240), (420, 200), (470, 150)))}
   <g id="mag6"><circle cx="0" cy="0" r="70" fill="#9fc3e8" fill-opacity=".35" stroke="{A.INK}" stroke-width="14"/><path d="M50 50 L120 120" stroke="{A.INK}" stroke-width="26" stroke-linecap="round"/></g></g>
  <g id="clip6" opacity="0"><rect x="210" y="100" width="460" height="500" rx="24" fill="#c9a36a" stroke="{A.INK}" stroke-width="7"/>
   <rect x="240" y="150" width="400" height="430" rx="10" fill="#FAF4E8" stroke="{A.INK}" stroke-width="5"/>
   <rect x="350" y="80" width="180" height="60" rx="14" fill="#9aa3ab" stroke="{A.INK}" stroke-width="6"/>
   <text x="440" y="215" text-anchor="middle" font-family="InterBlack" font-size="40" fill="#1e56ac">US TASK FORCE</text>
   <rect x="270" y="300" width="60" height="60" rx="8" fill="#fff" stroke="{A.INK}" stroke-width="6"/>
   <text x="345" y="343" font-family="InterBlack" font-size="31" fill="{A.INK}">ROUTINE CHECKS</text>
   <path id="x6" d="M280 310 L320 350 M320 310 L280 350" stroke="#FF7A59" stroke-width="12" stroke-linecap="round" stroke-dasharray="120" stroke-dashoffset="120"/>
   {''.join(f'<rect x="275" y="{y}" width="{w}" height="16" rx="8" fill="#cfd5dc"/>' for y, w in ((410, 320), (450, 280), (490, 300)))}</g>""", 880, 650)}
</div>
<div id="np6" class="stamp" style="left:130px;top:430px;font-size:108px">NOT PROVEN</div>
<div id="cd6" class="card"><h3>USPSTF (US, NOT CANADA)</h3><p>Advises against routine screening if no symptoms.</p></div>'''

S7 = f'''<div class="navy"></div><div id="dots7" class="dots"></div>
<div id="pn7" class="panel"><div class="ptitle">HOW STRONG IS THE EVIDENCE?</div>
 {svg(f"""<path d="M440 250 V560" stroke="{A.INK}" stroke-width="18"/><path d="M440 250 V560" stroke="#9aa3ab" stroke-width="10"/>
  <path d="M340 580 H540 L500 548 H380Z" fill="#9aa3ab" stroke="{A.INK}" stroke-width="6"/><circle cx="440" cy="250" r="20" fill="{A.GOLD}" stroke="{A.INK}" stroke-width="6"/>
  <g id="beam7"><path d="M160 250 H720" stroke="{A.INK}" stroke-width="16" stroke-linecap="round"/><path d="M160 250 H720" stroke="#cfd5dc" stroke-width="8" stroke-linecap="round"/>
   <g id="panL"><path d="M160 250 L100 400 M160 250 L220 400" stroke="{A.INK}" stroke-width="5"/><path d="M80 400 H240 Q160 460 80 400Z" fill="#3fc1b0" stroke="{A.INK}" stroke-width="6"/></g>
   <g id="panR"><path d="M720 250 L660 400 M720 250 L780 400" stroke="{A.INK}" stroke-width="5"/><path d="M640 400 H800 Q720 460 640 400Z" fill="#FF7A59" stroke="{A.INK}" stroke-width="6"/></g></g>""", 880, 650)}
 <div id="lf7" class="slab" style="left:85px;top:300px;color:#3fc1b0">FOR</div>
 <div id="la7" class="slab" style="left:610px;top:300px;color:#FF7A59">AGAINST</div>
</div>
<div id="ew7" class="stamp" style="left:230px;top:300px;font-size:80px;color:#c4b0ff;border-color:#c4b0ff">EITHER WAY</div>
<div id="cd7" class="card" style="border-left-color:#c4b0ff"><h3 style="color:#7a5cc7">THOMAS 2026</h3><p>Not strong enough to say yes or no.</p></div>'''


def ecg(n=24, per=110):
    d = "M0 160"
    for i in range(n):
        x = i * per
        d += f" L{x + 25} 160 L{x + 32} 150 L{x + 39} 160 L{x + 50} 160 L{x + 55} 170 L{x + 61} 70 L{x + 67} 190 L{x + 73} 160 L{x + 88} 160 L{x + 96} 140 L{x + 104} 160"
    return d


S8 = f'''<div class="bgfill" style="background:linear-gradient(#1c2a45,#14203a)"></div><div id="dots8" class="dots"></div>
<div id="pn8" class="panel"><div class="ptitle">YOUR BASELINE</div>
 <div id="hb8" class="lot" style="left:10px;top:230px;width:330px;height:260px"></div>
 {svg(f"""<rect id="band8" x="300" y="300" width="560" height="120" rx="20" fill="#5AE68C" opacity=".18"/>
  <g clip-path="url(#ec8)"><clipPath id="ec8"><rect x="300" y="240" width="560" height="240"/></clipPath>
  <g transform="translate(300,200)"><path id="ecg8" d="{ecg()}" fill="none" stroke="#5AE68C" stroke-width="7" stroke-linejoin="round" stroke-dasharray="3000" stroke-dashoffset="3000"/></g></g>""", 880, 650)}
 {chip("c8", "NORMAL FOR YOU", 420, 470, bg="#5AE68C", size=40)}
 <div id="t8" class="big" style="top:80px;width:880px;font-size:104px;color:#5AE68C">KNOW YOUR<br>NORMAL</div>
</div>'''

S9 = f'''<div class="bgfill" style="background:linear-gradient(#5b6b8a 0%,#9fb0c8 60%,#cdd6e2 100%)"></div>
{svg(f'<g id="st9">{A.clinic_street(W, H, "cs")}</g><g id="tram9" transform="translate(1200,0)">{A.streetcar(0, 1070, .62, sign="506 MAIN ST")}</g>')}
<div class="snowW" style="position:absolute;inset:0;overflow:hidden">{snow("s9", 46, 9, 0, 1600, (6, 13))}</div>
{chip("c9a", "A LUMP", 90, 250, bg="#FFD166", size=46)}
{chip("c9b", "SWELLING", 90, 345, bg="#FFD166", size=46)}
{chip("c9c", "SOMETHING OFF?", 90, 440, bg="#FFD166", size=46)}
<div id="dw9" class="stamp" style="left:180px;top:330px;font-size:104px">DON'T WAIT</div>
<div id="sd9" class="big" style="top:250px;left:60px;width:560px;font-size:100px;color:#5AE68C">SEE A<br>DOCTOR</div>
<div id="stl9" class="lot" style="left:620px;top:210px;width:300px;height:300px"></div>'''

S10 = f'''<div class="bgfill" style="background:linear-gradient(#ff9f7a 0%,#f2c48a 30%,#9fc3e8 62%)"></div>
{svg(f'<g id="fv10">{A.ferry_view(W, H, "fv")}</g>')}
<div id="mus10" class="lot" style="left:600px;top:420px;width:200px;height:100px">{svg(f'<g id="mz10">{A.handlebar(100, 50, 190, fill="#7a5cc7", sticker=False)}</g>', 200, 100, "position:absolute;left:0;top:0;overflow:visible")}</div>
<div id="g10" class="big" style="top:640px;font-size:96px;color:#FAF4E8"><span style="color:#c4b0ff">GROW</span> THE 'STACHE</div>
<div id="bk10" class="big" style="top:640px;font-size:96px;color:#5AE68C">BOOK THE<br>CHECKUP</div>
<div id="cal10" style="position:absolute;left:150px;top:300px;opacity:0">{svg(f"""<rect x="10" y="20" width="200" height="190" rx="22" fill="#FAF4E8" stroke="{A.INK}" stroke-width="7"/>
  <rect x="10" y="20" width="200" height="56" rx="18" fill="#4f86ff" stroke="{A.INK}" stroke-width="7"/><path d="M60 6 V44 M160 6 V44" stroke="{A.INK}" stroke-width="12" stroke-linecap="round"/>
  <path id="ck10" d="M60 140 L95 175 L160 105" fill="none" stroke="#3fc1b0" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="160" stroke-dashoffset="160"/>""", 230, 230)}</div>
<div id="cd10" class="card" style="border-left-color:#3fc1b0"><h3 style="color:#188076">HEADS UP</h3><p>Not medical advice. Lump, swelling or pain? See a doctor.</p></div>'''

S11 = f'''<div class="bgfill" style="background:linear-gradient(#ff9f7a 0%,#f2c48a 30%,#9fc3e8 62%)"></div>
{svg(f'<g id="fv11">{A.ferry_view(W, H, "fw")}</g>')}
<div id="pn11" class="panel" style="top:220px;height:600px;background:rgba(15,34,54,.95)">
 <div id="sub11" class="subbtn" style="background:#FF7A59;color:#0c1622">SUBSCRIBE</div>
 <div id="subd11" class="subbtn" style="background:#3a4a5e;color:#FAF4E8;opacity:0;font-size:60px">SUBSCRIBED ✓</div>
 <div id="like11" style="position:absolute;left:760px;top:80px;font:100px InterBlack;opacity:0">👍</div>
 <div style="position:absolute;left:40px;top:262px;font:34px InterBlack;color:#FFD166;letter-spacing:.05em">SOURCES</div>
 <div id="src11" style="position:absolute;left:40px;top:318px;width:800px;font:36px/1.4 InterSB;color:#cfe0ff">
  Thomas 2026 · Bashi 2026<br><span style="color:#96b0c4;font-size:34px">Links in the description<br>Not medical advice</span></div>
</div>
<div id="tc11" class="big" style="top:1090px;left:470px;width:520px;font-size:84px;color:#FFD166">TAKE<br>CARE</div>'''

S12 = hook_bg("h12") + '<div id="t12" class="big" style="top:250px;font-size:124px;color:#FFD166;opacity:1">MOVEMBER</div>'

scenes = [("s1", 0, C1, S1), ("s2", C1, C2, S2), ("s3", C2, C3, S3), ("s4", C3, C4, S4), ("s5", C4, C5, S5), ("s6", C5, C6, S6),
          ("s7", C6, C7, S7), ("s8", C7, C8, S8), ("s9", C8, C9, S9), ("s10", C9, C10, S10), ("s11", C10, C11, S11), ("s12", C11, T, S12)]
scene_html = "\n".join(f'<div id="{i}" class="scene clip" data-start="{a}" data-duration="{round(b - a, 3)}">{h}</div>' for i, a, b, h in scenes)

# ------------------------------------------------------------------ timeline beats
J = []
def j(s): J.append(s)
# camera: slow push-in per scene, punch on punchlines (U4)
for _, a, b, _h in scenes[:-1]:
    j(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:{b - a - 0.05:.3f},ease:"sine.inOut",immediateRender:false}},{a + 0.01:.3f});')
j(f'tl.set("#cam",{{scale:1}},{C11});')
j('const punch=(t,s=1.07)=>{tl.to("#shaker",{scale:s,duration:0.08,ease:"power2.out"},t);tl.to("#shaker",{scale:1,duration:0.35,ease:"back.out(2)"},t+0.08);};')
j('const pop=(s,t,from=0)=>tl.fromTo(s,{scale:from,opacity:0},{scale:1,opacity:1,duration:0.34,ease:"back.out(2.8)"},t);')
j('const out=(s,t)=>tl.to(s,{opacity:0,scale:0.7,duration:0.15,ease:"power2.in"},t);')
j('const stamp=(s,t,r=-8)=>tl.fromTo(s,{scale:3,opacity:0,rotation:r-6},{scale:1,opacity:1,rotation:r,duration:0.24,ease:"back.out(1.6)"},t);')
j('const slideIn=(s,t)=>tl.fromTo(s,{x:600,opacity:1},{x:0,opacity:1,duration:0.4,ease:"back.out(1.5)",immediateRender:false},t);')
for t in (tReal, t6ix, t95, tTwist, tProven, tDont, tStache, tBook): j(f"punch({t:.3f});")
j('tl.set("#shaker",{x:0,y:0,scale:1},0);')
for b, a, d in (("#dots3", C2, C3 - C2), ("#dots6", C5, C6 - C5), ("#dots7", C6, C7 - C6), ("#dots8", C7, C8 - C7)):
    j(f'tl.fromTo("{b}",{{x:0,y:0}},{{x:70,y:140,duration:{d:.3f},ease:"none"}},{a});')
for t, pos in ((0, POS_HOOK), (C1, POS_BIG), (C2, POS_V2), (C11, POS_HOOK)):
    j(f'tl.set("#cytoPos",{json.dumps(pos)},{t});')
j(f'tl.set("#cytoPos",{json.dumps(POS_HOOK)},{T - 0.01});')
# moustache sticker: always on (loop frame = hook frame); slaps on with an elastic squash on "Movember", wiggles on "'stache"
j('gsap.set("#stache",{svgOrigin:"591 703"});gsap.set("#ribbonPin",{svgOrigin:"800 520"});')
j(f'tl.fromTo("#stache",{{scaleX:1.45,scaleY:0.6,rotation:-8}},{{scaleX:1,scaleY:1,rotation:0,duration:0.7,ease:"elastic.out(1.2,0.3)",immediateRender:false}},{tMov + 0.02});')
j(f'tl.fromTo("#stache",{{rotation:0}},{{rotation:7,duration:0.09,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{tStache});')
j(f'tl.fromTo("#ribbonPin",{{rotation:0}},{{rotation:10,duration:0.5,yoyo:true,repeat:{int(T / 0.5)},ease:"sine.inOut",immediateRender:false}},0.4);')
# cup down for the serious beat (Brief: 'cup set down'), picked back up for the payoff
j(f'tl.set("#cupTable",{{opacity:0}},0);tl.set("#cup",{{opacity:0}},{tBut2 - 0.05});tl.fromTo("#cupTable",{{opacity:1,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"bounce.out",immediateRender:false}},{tBut2 - 0.05});'
  f'tl.set("#cup",{{opacity:1}},{C9 + 0.05});tl.set("#cupTable",{{opacity:0}},{C9 + 0.05});')

# ---- S1 hook: max 3 movers (MOVEMBER punch, caption, Cyto); background still except the camera push
j(f'tl.fromTo("#t1",{{scale:1}},{{scale:1.12,duration:0.1,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{tMov + 0.02});')
j(f'tl.to("#t1",{{y:-30,opacity:0,duration:0.2,ease:"power2.in"}},{C1 - 0.25});')
# ---- S2 catchphrase
j(f'document.querySelectorAll("#h2City .win").forEach((w,i)=>{{ if(i%4==0) tl.to(w,{{opacity:.2,duration:0.3,repeat:7,yoyo:true}},{C1}+(i%9)*0.2); }});')
j(f'tl.fromTo("#h2City",{{y:80}},{{y:0,duration:{C2 - C1:.3f},ease:"power2.out"}},{C1});')
j(f'tl.set("#t2a",{{opacity:0}},0);tl.fromTo("#t2a",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(1.7)"}},{tLive - 0.05});')
j(f'tl.set("#t2c",{{opacity:0}},0);tl.fromTo("#t2c",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.34,ease:"back.out(2.4)"}},{tInside});')
j(f'tl.to(["#t2a","#t2c"],{{opacity:0,duration:0.15}},{C2 - 0.2});')
# ---- S3 age range figure
j(f'tl.fromTo("#pn3",{{y:900}},{{y:0,duration:0.45,ease:"back.out(1.1)"}},{C2});')
j(f'document.querySelectorAll("#pn3 .guy").forEach((g,i)=>tl.fromTo(g,{{y:120,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(2.2)"}},{C2 + 0.2}+i*0.07));')
j(f'tl.set("#rb3",{{opacity:1}},{tTest});tl.fromTo("#rb3",{{scale:0,svgOrigin:"830 290"}},{{scale:1,svgOrigin:"830 290",duration:0.4,ease:"back.out(2.6)"}},{tTest});'
  f'tl.fromTo("#rb3",{{rotation:-8,svgOrigin:"830 290"}},{{rotation:8,svgOrigin:"830 290",duration:0.6,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{tTest + 0.4});')
j(f'tl.set(["#p15","#p45","#t3"],{{opacity:0}},0);pop("#p15",{t15 - 0.05});pop("#p45",{t45 - 0.05});')
j(f'tl.fromTo("#band3",{{scaleX:0,svgOrigin:"150 400"}},{{scaleX:1,svgOrigin:"150 400",duration:{t45 - t15 + 0.3:.2f},ease:"power2.inOut"}},{t15});')
j(f'["#pn3 .g1","#pn3 .g2","#pn3 .g3","#pn3 .g4","#pn3 .g5","#pn3 .g6"].forEach((g,i)=>tl.to(g,{{y:-14,duration:0.14,yoyo:true,repeat:1,ease:"power2.out"}},{t15 + 0.1}+i*0.1));')
j(f'pop("#t3",{tGuys - 0.05});')
j(f'tl.set("#cd3",{{opacity:0}},0);slideIn("#cd3",{tMost});')
# ---- S4 platform: train pulls out, 95% ring fills, shield
j(f'tl.fromTo("#bpTrain",{{x:0}},{{x:-1900,duration:{C4 - C3:.2f},ease:"power2.in"}},{C3});')
j(f'tl.fromTo("#bpMin",{{opacity:1}},{{opacity:.35,duration:0.3,repeat:{int((C4 - C3) / 0.3)},yoyo:true}},{C3});')
j(f'tl.fromTo("#pn4",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{tGood - 0.1});')
j(f'tl.fromTo("#ring4",{{attr:{{"stroke-dashoffset":{RING_L:.1f}}}}},{{attr:{{"stroke-dashoffset":{RING_L * 0.05:.1f}}},duration:{t95 - tNews + 0.25:.2f},ease:"power2.inOut"}},{tNews});')
j(f'tl.set("#t4",{{opacity:0}},0);tl.fromTo("#t4",{{scale:1.8,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2.6)"}},{t95 + 0.1});')
j(lot("sh4", "shield-2.json", tAlive - 0.2, C4, loops=1))
j(f'tl.set("#sh4",{{opacity:0}},0);tl.set("#sh4",{{opacity:1}},{tAlive - 0.2});')
j(f'tl.set("#c4",{{opacity:0}},0);pop("#c4",{tAlive - 0.05});')
j(f'tl.set("#cd4",{{opacity:0}},0);slideIn("#cd4",{tYears - 0.2});')
# ---- S5 twist: calendar checks month by month, then the big ?
j(f'tl.fromTo("#bqTrain",{{x:1900}},{{x:0,duration:1.8,ease:"power2.out"}},{C4});')
j(f'tl.set("#tw5",{{opacity:0}},0);stamp("#tw5",{tTwist - 0.03});out("#tw5",{tDoes - 0.22});')
j(f'tl.fromTo("#pn5",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.8)"}},{tDoes - 0.2});')
j(f'document.querySelectorAll("#cal5 .mo").forEach((m,i)=>tl.fromTo(m,{{scale:0,opacity:0,transformOrigin:"56px 52px"}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2.6)"}},{tDoes}+i*0.04));')
j(f'document.querySelectorAll("#cal5 .ck").forEach((c,i)=>tl.to(c,{{strokeDashoffset:0,duration:0.14,ease:"power2.out"}},{tEvery}+i*0.085));')
j(f'tl.set("#q5",{{opacity:0}},0);tl.fromTo("#q5",{{scale:3,opacity:0,rotation:-20}},{{scale:1,opacity:1,rotation:0,duration:0.3,ease:"back.out(2)"}},{tSave - 0.05});'
  f'tl.to("#q5",{{rotation:10,duration:0.12,yoyo:true,repeat:3}},{tLives + 0.2});')
# ---- S6 proof search -> NOT PROVEN -> US task force clipboard
j(f'tl.fromTo("#pn6",{{scale:1.15,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"power3.out"}},{C5});')
j(f'tl.fromTo("#mag6",{{x:300,y:200}},{{keyframes:[{{x:520,y:220,duration:0.45}},{{x:330,y:380,duration:0.45}},{{x:540,y:430,duration:0.4}}],ease:"sine.inOut"}},{C5 + 0.1});')
j(f'tl.set("#np6",{{opacity:0}},0);stamp("#np6",{tProven - 0.03});out("#np6",{tUS - 0.25});')
j(f'tl.to("#doc6",{{opacity:0,duration:0.15}},{tUS - 0.2});tl.fromTo("#clip6",{{opacity:0,y:200}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{tUS - 0.1});')
j(f'tl.to("#x6",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{tDoesnt + 0.15});')
j(f'tl.set("#cd6",{{opacity:0}},0);slideIn("#cd6",{tRec});')
# ---- S7 balance: teeters both ways, settles level on "either way"
j(f'tl.fromTo("#pn7",{{y:900}},{{y:0,duration:0.42,ease:"back.out(1.1)"}},{C6});')
j('gsap.set("#beam7",{svgOrigin:"440 250"});gsap.set("#panL",{svgOrigin:"160 250"});gsap.set("#panR",{svgOrigin:"720 250"});')
j(f'tl.fromTo("#beam7",{{rotation:0}},{{keyframes:[{{rotation:-12,duration:0.5}},{{rotation:10,duration:0.55}},{{rotation:-7,duration:0.45}},{{rotation:5,duration:0.4}},{{rotation:0,duration:0.5,ease:"elastic.out(1,0.4)"}}],ease:"sine.inOut"}},{C6 + 0.2});')
j(f'tl.fromTo(["#panL","#panR"],{{rotation:0}},{{keyframes:[{{rotation:12,duration:0.5}},{{rotation:-10,duration:0.55}},{{rotation:7,duration:0.45}},{{rotation:-5,duration:0.4}},{{rotation:0,duration:0.5}}],ease:"sine.inOut"}},{C6 + 0.2});')
j(f'tl.fromTo("#lf7",{{y:0}},{{keyframes:[{{y:-55,duration:0.5}},{{y:46,duration:0.55}},{{y:-32,duration:0.45}},{{y:22,duration:0.4}},{{y:0,duration:0.5}}],ease:"sine.inOut"}},{C6 + 0.2});')
j(f'tl.fromTo("#la7",{{y:0}},{{keyframes:[{{y:55,duration:0.5}},{{y:-46,duration:0.55}},{{y:32,duration:0.45}},{{y:-22,duration:0.4}},{{y:0,duration:0.5}}],ease:"sine.inOut"}},{C6 + 0.2});')
j(f'tl.set(["#lf7","#la7"],{{opacity:0}},0);pop("#lf7",{C6 + 0.25});pop("#la7",{C6 + 0.4});')
j(f'tl.to(["#lf7","#la7"],{{opacity:0,duration:0.15}},{tEither - 0.25});')
j(f'tl.set("#ew7",{{opacity:0}},0);stamp("#ew7",{tEither - 0.03},-3);tl.to("#ew7",{{rotation:2,duration:0.12,yoyo:true,repeat:1}},{tStyll});')
j(f'tl.set("#cd7",{{opacity:0}},0);slideIn("#cd7",{tEvid});')
# ---- S8 cup down: baseline heartbeat, 'know your normal'
j(f'tl.fromTo("#pn8",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{C7});')
j(lot("hb8", "heart-beat.json", C7, C8, loops=6))
j(f'tl.to("#ecg8",{{strokeDashoffset:0,duration:{C8 - C7:.2f},ease:"none"}},{C7});')
j(f'tl.fromTo("#band8",{{opacity:0}},{{opacity:.22,duration:0.3}},{tKnow});')
j(f'tl.set(["#t8","#c8"],{{opacity:0}},0);pop("#t8",{tKnow - 0.05});pop("#c8",{tNormal + 0.1});')
# ---- S9 Danforth-style street: streetcar, snow, symptom chips, don't wait, see a doctor
j(snow_js("s9", C8, C9, 1800))
j(f'tl.fromTo("#tram9",{{x:1200}},{{x:-1000,duration:3.4,ease:"none"}},{C8});')
j(f'document.querySelectorAll("#tram9 .wheel").forEach(w=>tl.fromTo(w,{{rotation:0,transformOrigin:"50% 50%"}},{{rotation:-720,duration:3.4,ease:"none"}},{C8}));')
j(f'tl.set(["#c9a","#c9b","#c9c"],{{opacity:0}},0);' + "".join(f'tl.fromTo("{s}",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:0.34,ease:"back.out(1.9)"}},{t - 0.05});' for s, t in (("#c9a", tLump), ("#c9b", tSwell), ("#c9c", tSomething))))
j(f'tl.to(["#c9a","#c9b","#c9c"],{{x:-500,opacity:0,duration:0.18,ease:"power2.in",stagger:0.04}},{tDont - 0.28});')
j(f'tl.set(["#dw9","#sd9"],{{opacity:0}},0);stamp("#dw9",{tDont - 0.03},-5);out("#dw9",{tSee - 0.2});pop("#sd9",{tSee - 0.03});')
j(f'tl.fromTo("#csDoor",{{scaleX:1,transformOrigin:"610px 0px"}},{{scaleX:0.15,duration:0.35,ease:"power2.out"}},{tDoctor});')
j(lot("stl9", "steth-1.json", tSee - 0.1, C9, loops=1))
j(f'tl.set("#stl9",{{opacity:0}},0);tl.fromTo("#stl9",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{tSee - 0.1});')
# ---- S10 ferry: moustache on the CN Tower, book the checkup
j(f'document.querySelectorAll("#fvRip .rip").forEach((r,i)=>tl.fromTo(r,{{x:-30}},{{x:30,duration:0.9+0.1*(i%3),yoyo:true,repeat:6,ease:"sine.inOut"}},{C9}));')
j(f'tl.fromTo("#fv10",{{y:0}},{{keyframes:[{{y:8,duration:0.8}},{{y:-6,duration:0.8}},{{y:6,duration:0.8}},{{y:-4,duration:0.8}},{{y:0,duration:0.7}}],ease:"sine.inOut"}},{C9});')
j(f'tl.fromTo("#mz10",{{rotation:-6,svgOrigin:"100 50"}},{{rotation:6,svgOrigin:"100 50",duration:0.25,yoyo:true,repeat:{int((C10 - tStache) / 0.25)},ease:"sine.inOut",immediateRender:false}},{tStache + 0.3});')
j(f'tl.set("#mus10",{{opacity:0}},0);tl.fromTo("#mus10",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{tStache - 0.1});')
j(f'tl.set(["#g10","#bk10"],{{opacity:0}},0);pop("#g10",{tGrow - 0.05});out("#g10",{tBook - 0.25});pop("#bk10",{tBook - 0.05});out("#bk10",{C10 - 0.2});')
j(f'tl.set("#cal10",{{opacity:0}},0);tl.fromTo("#cal10",{{opacity:0,y:-80,scale:.5}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2.2)"}},{tBook - 0.05});tl.to("#ck10",{{strokeDashoffset:0,duration:0.3}},{tCheckup + 0.1});')
j(f'tl.set("#cd10",{{opacity:0}},0);slideIn("#cd10",{tNot - 0.05});')
# ---- S11 outro
j(f'document.querySelectorAll("#fwRip .rip").forEach((r,i)=>tl.fromTo(r,{{x:-30}},{{x:30,duration:0.9+0.1*(i%3),yoyo:true,repeat:4,ease:"sine.inOut"}},{C10}));')
j(f'tl.fromTo("#pn11",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:0.38,ease:"back.out(1.8)"}},{C10 + 0.05});')
j(f'tl.fromTo("#like11",{{scale:0,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.32,ease:"back.out(3)"}},{tLike});')
j(f'tl.fromTo("#sub11",{{scale:1}},{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},{tSub + 0.15});'
  f'tl.set("#subd11",{{opacity:0}},0);tl.set("#subd11",{{opacity:1}},{tSub + 0.25});tl.set("#sub11",{{opacity:0}},{tSub + 0.25});')
j(f'tl.fromTo("#src11",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{C10 + 0.2});')
j(f'tl.set("#tc11",{{opacity:0}},0);pop("#tc11",{tTake - 0.05});')
# ---- S12 loop frame = hook frame
j(f'tl.fromTo("#s12",{{opacity:0}},{{opacity:1,duration:0.18}},{C11});')

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
  background:rgba(12,22,34,.88); transform:rotate(-8deg); opacity:0; letter-spacing:.02em; z-index:40; white-space:nowrap; }}
.pin {{ position:absolute; transform:translate(-50%,0); font:52px InterBlack; color:#0c1622; background:#FFD166; border:5px solid #0c1622; border-radius:18px; padding:2px 16px; }}
.pct {{ position:absolute; left:110px; top:215px; width:320px; text-align:center; font:120px InterBlack; color:#5AE68C; paint-order:stroke fill; -webkit-text-stroke:10px #0c1622; letter-spacing:-3px; }}
.slab {{ position:absolute; width:190px; text-align:center; font:40px InterBlack; paint-order:stroke fill; -webkit-text-stroke:8px #0c1622; }}
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
  <div id="cytoLayer">{R.rig3_html(None, "cup_red", face_extra=STACHE, toque_extra=RIBBON)}</div>
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
json.dump({"name": "ep12"}, open("meta.json", "w"))
print("built", len(html), "bytes; T", T, "C11", C11, "words", len(WORDS), "voice", round(TM["total"], 2))
