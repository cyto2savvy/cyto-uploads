"""EP14 v3 — What Two Minutes of Silence Does to Your Body (6ixty Seconds of Science, Remembrance Day).
FIRST HOOK-FIRST TEST: Cyto talks on frame 1 (voice at 0.00s), huge claim + heart-rate trace visible on frame 1, catchphrase AFTER the hook,
<= 34 s, loop frame = hook frame. Respectful: slow push-ins, soft cross-fades only (no whip/shake/punch), cup set down all video,
v3 (Nov 9): CANON v2 rig (cyto2d.js RIG=1 + cyto_rig_runtime.js), solemn face, hoodie + plain poppy-shape pin, cup set down on a ledge.
Re-hook at ~4.1s ("And it wasn't just the heart."), quiet follow chip mid-video, loop frame = hook frame.
python3 build.py -> index.html + assets/audio.wav"""
import json, sys, os, subprocess, random, re, math, shutil
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import numpy as np
import cytohf as C, cytorig as K, art as A
from engine import tone, noise, hp, lp, add, load_mono, SR

P = "/home/claude/hf/ep14v3"; os.chdir(P)
V = "/home/claude/ep14v3"
TM = json.load(open(f"{V}/timing.json")); WORDS = TM["words"]
W, H = 1080, 1920
NAVY, INK, GOLD, CORAL, TEAL, CREAM, RED = "#0c1622", A.INK, "#FFD166", "#FF7A59", "#3fc1b0", "#FAF4E8", "#d7262e"


def wt(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and re.sub(r"[^a-z0-9%']", "", w["w"].lower()) == re.sub(r"[^a-z0-9%']", "", word.lower()):
            return round(w["t0"], 3)
    raise KeyError(word)


def we(word, after=0.0):
    for w in WORDS:
        if w["t0"] >= after and re.sub(r"[^a-z0-9%']", "", w["w"].lower()) == re.sub(r"[^a-z0-9%']", "", word.lower()):
            return round(w["t1"], 3)
    raise KeyError(word)


# ------------------------------------------------------------------ word beats (after= for repeated / short words)
tIn, tSilence1, tSlowed, tHeart1, tRate1 = wt("In"), wt("silence"), wt("slowed"), wt("heart"), wt("rate")
tAnd, tWasnt, tJust, tHeartR = wt("And"), wt("wasn't"), wt("just"), wt("heart", 4.5)
tYo, tCyto, tLive, tSix, tInside = wt("Yo", 3.8), wt("Cyto"), wt("live"), wt("6ix"), wt("inside")
tResearchers, tMusic, tTwoMin, tPauses, tTracked, tHeart2, tBlood, tBreathing = (wt("Researchers"), wt("music"), wt("two-minute"), wt("pauses"),
                                                                                 wt("tracked"), wt("heart", 12), wt("blood"), wt("breathing"))
tIn2, tPauses2, tAll, tDropped, tBelow, tStarted = wt("In", 13), wt("pauses", 13), wt("all"), wt("dropped"), wt("below"), wt("started")
tSilence2, tEmpty, tFam, tYour, tSlows, tDown = wt("Silence", 17), wt("empty"), wt("fam"), wt("Your", 19), wt("slows"), wt("down")
tSo, tCity, tQuiet1, tEleven, tQuiet2, tToo = wt("So", 21), wt("city"), wt("quiet"), wt("eleven"), wt("quiet", 24), wt("too")
tLest, tForget, eForget, tNot = wt("Lest"), wt("forget"), we("forget"), wt("Not", 27)
tLike, tSub, tTake, tMoment = wt("Like"), wt("subscribe"), wt("take"), wt("moment")
END_V = WORDS[-1]["t1"]

C1, C2, C3, C4, C5, C6, C7 = (round(x, 2) for x in (tYo - 0.15, tResearchers - 0.15, tIn2 - 0.12, tSilence2 - 0.12, tSo - 0.12, tLest - 0.12, tLike - 0.12))
C8 = round(END_V + 0.18, 2)
T = round(C8 + 0.5, 2)
CUTS = (C1, C2, C3, C4, C5, C6, C7, C8)
XF = 0.45                       # soft cross-fade length (centred on each cut)
assert T <= 34.0, T

# ------------------------------------------------------------------ assets
C.copy_assets_v2(P, lotties=["soundwave-1.json", "notes-1.json", "heart-beat.json", "candle-2.json"])

# ------------------------------------------------------------------ hook ECG trace (frame 1 = trace already running; it slows and dips below the start line)
ECG_X0, ECG_X1, ECG_Y = 110, 890, 690
def ecg_points():
    beats = [(x, 1.0, 0) for x in range(150, 470, 80)]                        # music: steady, quick
    x, gap, amp, dip = 470, 120, 0.85, 0
    while x < ECG_X1 - 40:                                                    # silence: slower, smaller, sinking
        beats.append((x, amp, dip)); x += gap; gap += 34; amp *= 0.86; dip = min(46, dip + 14)
    pts, peaks = [(ECG_X0, ECG_Y)], []
    for bx, a, d in beats:
        b = ECG_Y + d
        for dx, dy in ((-22, 0), (-12, -7 * a), (-5, 9 * a), (0, -78 * a), (6, 26 * a), (13, 0), (30, -14 * a), (42, 0)):
            pts.append((bx + dx, b + dy))
        peaks.append((bx, b - 78 * a))
    pts.append((ECG_X1, ECG_Y + beats[-1][2]))
    return pts, peaks
ECG_PTS, ECG_PEAKS = ecg_points()
seg = [math.dist(ECG_PTS[i], ECG_PTS[i + 1]) for i in range(len(ECG_PTS) - 1)]
ECG_LEN = sum(seg)
def len_at_x(x):
    acc = 0
    for (a, b), s in zip(zip(ECG_PTS, ECG_PTS[1:]), seg):
        if b[0] >= x: return acc + s * max(0, min(1, (x - a[0]) / max(1e-6, b[0] - a[0])))
        acc += s
    return acc
L0 = len_at_x(455)              # revealed on frame 1 (the 'music' part)
ECG_DUR = 3.55                  # head reaches the end just before the hook line ends
BEAT_T = [round((len_at_x(px) - L0) / (ECG_LEN - L0) * ECG_DUR, 3) for px, _ in ECG_PEAKS if len_at_x(px) > L0]
ECG_D = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ECG_PTS)

# heart lottie beats in S5: slowing down
HB_T = []; t_, g_ = C4 + 0.35, 0.72
while t_ < C5 - 0.45:
    HB_T.append(round(t_, 3)); t_ += g_; g_ *= 1.16


# ------------------------------------------------------------------ audio: quiet pads, heartbeat thumps, one soft bell at 'eleven', near-silence after 'Lest we forget'
def pad(m, dur, g=0.03):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 1.0).clip(0, 1)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) + 0.08 * np.sin(2 * np.pi * 3.01 * f * t)) * env * g


def thump(gain=1.0):
    t = np.arange(int(0.42 * SR)) / SR
    lub = np.sin(2 * np.pi * (58 - 20 * t) * t) * np.exp(-t / 0.05)
    dub = np.zeros_like(t); k = int(0.19 * SR); dub[k:] = np.sin(2 * np.pi * 66 * t[: len(t) - k]) * np.exp(-t[: len(t) - k] / 0.04) * 0.7
    return lp(lub + dub, 0.08) * gain


def bell(f0=392.0, dur=3.2):
    t = np.arange(int(dur * SR)) / SR
    return sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d) for r, a, d in ((1, 1, 1.4), (2.0, .45, .8), (2.76, .3, .5), (5.4, .12, .25)))


def make_audio():
    n = int((T + 0.3) * SR); music = np.zeros(n, np.float32)
    BAR = 4.0
    chords = [[50, 57, 62, 65], [46, 53, 58, 62], [53, 57, 60, 65], [48, 55, 60, 64]]    # Dm Bb F C — slow, stately
    t = -1.0; i = 0
    while t < T + 0.3:
        for mm in chords[i % 4]: add(music, pad(mm, BAR + 1.6), max(0, t))
        add(music, pad(chords[i % 4][0] - 12, BAR + 1.0, 0.04), max(0, t))
        t += BAR; i += 1
    music = lp(music, 0.12)
    v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
    vrms = np.sqrt(np.mean(vv[np.abs(vv) > 0.02] ** 2))
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.5 * np.clip(env * 3, 0, 1))
    music *= vrms * 10 ** (-26 / 20) / (np.sqrt(np.mean(music ** 2)) + 1e-9)
    # the held moment after "Lest we forget": music dips to near-silence, comes back softly for the outro
    tt = np.arange(n) / SR
    g = np.ones(n)
    a0, a1, b0, b1 = eForget - 0.1, eForget + 0.5, tNot - 0.1, tNot + 0.8
    g = np.where((tt >= a0) & (tt < a1), 1 - 0.95 * (tt - a0) / (a1 - a0), g)
    g = np.where((tt >= a1) & (tt < b0), 0.05, g)
    g = np.where((tt >= b0) & (tt < b1), 0.05 + 0.95 * (tt - b0) / (b1 - b0), g)
    music *= g
    music[: int(0.25 * SR)] *= np.linspace(0.3, 1, int(0.25 * SR))
    sfx = np.zeros(n, np.float32)
    th = thump(); th /= np.sqrt(np.mean(th ** 2)) + 1e-9
    for k, bt in enumerate(BEAT_T): add(sfx, th * vrms * 10 ** (-21 / 20) * (0.95 ** k), max(0, bt))
    for k, bt in enumerate(HB_T): add(sfx, th * vrms * 10 ** (-22 / 20) * (0.93 ** k), bt + 0.05)
    bl = bell(); bl /= np.sqrt(np.mean(bl ** 2)) + 1e-9
    add(sfx, bl * vrms * 10 ** (-24 / 20), tEleven)
    mix = music + sfx; mix[:m] += v[:m]
    mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[: int(T * SR)]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "assets/raw_mix.wav"],
                   input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/raw_mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "assets/audio.wav"], check=True)


make_audio()

# ------------------------------------------------------------------ Cyto (canon v2 rig): hoodie + poppy-shape pin, solemn face, cup set down on a ledge all video
POS_HOOK, POS_BIG, POS_V2 = C.place(400, 1345, 0.58), C.place(400, 1315, 0.62), C.place(350, 1310, 0.53)
mouth = K.mouth_track(f"{V}/voice.wav", WORDS)
HOLD = (round(eForget + 0.15, 2), round(tNot - 0.25, 2))          # eyes gently closed for the held moment after "Lest we forget"
blinks = K.blink_times(T, seed=14, avoid=[HOLD])
rig_js = K.rig_js(mouth, T, blinks)
rig_js = rig_js.replace('"blinks"', '"closed":%s,"blinks"' % json.dumps([list(HOLD)]))

# ------------------------------------------------------------------ captions (real spellings; hidden while the same words are a big title)
KEYS = {"silence": "#c4b0ff", "slowed": GOLD, "heart": CORAL, "6ix": GOLD, "music": "#9fc3e8", "twominute": "#9fc3e8", "pauses": "#9fc3e8",
        "dropped": GOLD, "below": GOLD, "empty": "#c4b0ff", "fam": TEAL, "slows": GOLD, "eleven": GOLD, "quiet": "#c4b0ff",
        "advice": TEAL, "subscribe": CORAL, "moment": GOLD}
HIDE = [(tAnd - 0.01, tYo - 0.01), (tLive - 0.01, C2), (tSilence2 - 0.01, tFam - 0.01), (tLest - 0.01, eForget + 0.05)]
CAPW = [w for w in WORDS if not any(a <= w["t0"] < b for a, b in HIDE)]
cap_html, cap_js = C.captions(CAPW, KEYS, y=C.CAP_Y_V2)
cap_html = re.sub(r'data-start="-[0-9.]+"', 'data-start="0.000"', cap_html)
cap_js = re.sub(r'\},-0\.0[0-9]+\);', '},0);', cap_js)
last_cap = cap_html.count('"cap clip"') - 1
cap_js += f'\ntl.set("#cap{last_cap}",{{opacity:0}},{C8});'
_q = [m for m in re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'TOO.' in m.group(2)][0]
cap_js += f'\ntl.set("#{_q.group(1)}",{{opacity:0}},{tLest - 0.05});'
_q2 = [m for m in re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'STARTED.' in m.group(2)][0]
cap_js += f'\ntl.set("#{_q2.group(1)}",{{opacity:0}},{tSilence2 - 0.05});'
_m = [m for m in re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'CYTO,' in m.group(2)][0]
cap_js += f'\ntl.set("#{_m.group(1)}",{{opacity:1}},0);tl.set("#{_m.group(1)}",{{opacity:0}},{tLive - 0.03});'
_r = [m for m in re.finditer(r'<div id="(cap\d+)"[^>]*>(.*?)</div>', cap_html) if 'RATE.' in m.group(2)][0]
cap_js += f'\ntl.set("#{_r.group(1)}",{{opacity:0}},{tAnd - 0.05});'
# first words visible on frame 1 (hook-first): no fade-in on the opening caption chunk
for i, w in enumerate(WORDS[:4]):
    cap_js = re.sub(rf'tl\.fromTo\("#w{i}",\{{[^}}]*\}},\{{[^}}]*\}},[0-9.]+\);', f'tl.set("#w{i}",{{opacity:1,scale:1,y:0}},0);' if w["t0"] < 0.3 else r'\g<0>', cap_js, count=1)


# ------------------------------------------------------------------ helpers
def chip(id_, text, left, top, bg=GOLD, fg=INK, size=40, extra=""):
    return f'<div id="{id_}" class="chip" style="left:{left}px;top:{top}px;background:{bg};color:{fg};font-size:{size}px;{extra}">{text}</div>'


def svg(inner, w=W, h=H, style="position:absolute;left:0;top:0;overflow:visible"):
    return f'<svg width="{w}" height="{h}" style="{style}">{inner}</svg>'


def snow(idp, n=40, seed=1, top=0, height=1500, size=(6, 13), op=(.35, .85)):
    rnd = random.Random(seed)
    return "".join(f'<div class="flake {idp}" data-v="{rnd.uniform(3.5, 6.0):.2f}" style="left:{rnd.uniform(0, W):.0f}px;top:{top + rnd.uniform(-height, 0):.0f}px;'
                   f'width:{(s := rnd.uniform(*size)):.0f}px;height:{s:.0f}px;opacity:{rnd.uniform(*op):.2f}"></div>' for _ in range(n))


def snow_js(idp, t0, t1, height=1800, t_slow=None, slow=0.2):
    """Snow falls; after t_slow it slows to `slow` of its speed (the city goes quiet). Seek-safe (plain tweens)."""
    if t_slow is None:
        return (f'document.querySelectorAll(".{idp}").forEach((f,i)=>{{const v=+f.dataset.v;'
                f'tl.fromTo(f,{{y:0,x:0}},{{y:{height},x:(i%2?30:-30),duration:v,ease:"none",repeat:Math.ceil({t1 - t0:.2f}/v)}},{t0:.2f});}});')
    a, b = t_slow - t0, t1 - t_slow
    return (f'document.querySelectorAll(".{idp}").forEach((f,i)=>{{const v=+f.dataset.v,sp={height}/v;'
            f'tl.fromTo(f,{{y:0,x:0}},{{y:sp*{a:.2f},x:(i%2?12:-12),duration:{a:.2f},ease:"none"}},{t0:.2f});'
            f'tl.fromTo(f,{{y:sp*{a:.2f}}},{{y:sp*{a:.2f}+sp*{b:.2f}*{slow},duration:{b:.2f},ease:"power2.out",immediateRender:false}},{t_slow:.2f});}});')


def lot(id_, file, t0, t1, loops=1, offset=0, ease="none"):
    data = open(f"{P}/assets/{file}").read(); v = id_.replace("-", "_")
    return (f'const L_{v}=lottie.loadAnimation({{container:document.getElementById("{id_}"),renderer:"svg",loop:false,autoplay:false,animationData:{data}}});'
            f'const P_{v}={{f:0}};tl.fromTo(P_{v},{{f:0}},{{f:L_{v}.totalFrames*{loops}-0.01,duration:{t1 - t0:.3f},ease:"{ease}",'
            f'onUpdate:()=>L_{v}.goToAndStop(({offset}+P_{v}.f) % L_{v}.totalFrames,true)}},{t0:.3f});L_{v}.goToAndStop({offset},true);')


# ------------------------------------------------------------------ scenes
heart_d = "M0 40 C-90 -20 -70 -95 -20 -80 C-5 -76 0 -62 0 -52 C0 -62 5 -76 20 -80 C70 -95 90 -20 0 40Z"
def hook(idp):
    """Frame 1: huge claim + a live heart-rate trace that slows and sinks below its start line, over a dim pre-dawn Old City Hall."""
    head_x, head_y = ECG_PTS[0]
    return f'''<div class="bgfill" style="background:linear-gradient(#070d1a 0%,#14254a 55%,#3b4670 82%,#6a6587 100%)"></div>
{svg(f'{A.stars(W, H, 26, 31, .3)}<g opacity=".55">{A.skyline(W, H, 1500, .7, seed=9, lit=.12, cn=950)}</g><g opacity=".6">{A.old_city_hall(560, 1640, .72, idp + "och")}</g>')}
<div class="bgfill" style="background:linear-gradient(rgba(7,13,26,.35),rgba(7,13,26,.15) 60%,rgba(7,13,26,.55))"></div>
<div id="{idp}t" class="big" style="top:205px;left:60px;width:880px;font-size:106px;color:{CREAM};opacity:1"><span>SILENCE</span> <span style="color:{GOLD}">SLOWS</span><br><span>YOUR</span> <span style="color:{CORAL}">HEART</span></div>
{svg(f"""<rect x="70" y="510" width="860" height="320" rx="34" fill="#071322" opacity=".92" stroke="#24425f" stroke-width="4"/>
 <rect x="480" y="530" width="430" height="280" rx="20" fill="#c4b0ff" opacity=".08"/>
 <path d="M{ECG_X0} {ECG_Y} H{ECG_X1}" stroke="#96b0c4" stroke-width="3" stroke-dasharray="10 12" opacity=".7"/>
 <text x="110" y="565" font-family="InterBlack" font-size="26" fill="#9fc3e8" letter-spacing="2">MUSIC</text>
 <text x="500" y="565" font-family="InterBlack" font-size="26" fill="#c4b0ff" letter-spacing="2">SILENCE</text>
 <path id="{idp}eg" d="{ECG_D}" fill="none" stroke="{CORAL}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round" opacity=".25"
   style="stroke-dasharray:{ECG_LEN:.1f};stroke-dashoffset:{ECG_LEN - L0:.1f}"/>
 <path id="{idp}ecg" d="{ECG_D}" fill="none" stroke="{CORAL}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"
   style="stroke-dasharray:{ECG_LEN:.1f};stroke-dashoffset:{ECG_LEN - L0:.1f}"/>
 <circle id="{idp}hd" cx="{455}" cy="{ECG_Y}" r="13" fill="{CREAM}" stroke="{CORAL}" stroke-width="6"/>
 <g id="{idp}hr" opacity="0" transform="translate(872,592)"><g id="{idp}hri"><path d="{heart_d}" transform="scale(.42)" fill="{CORAL}" stroke="{INK}" stroke-width="7"/></g></g>
 <g id="{idp}rh" opacity="0">
  <path id="{idp}bp" d="M490 618 C560 612 600 626 650 630 S760 652 900 660" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"/>
  <path id="{idp}br" d="M490 772 Q520 752 550 772 T610 776 T670 784 T730 792 T790 798 T850 804 T900 806" fill="none" stroke="{TEAL}" stroke-width="7" stroke-linecap="round" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"/>
  <text x="836" y="604" text-anchor="end" font-family="InterBlack" font-size="27" fill="{GOLD}" letter-spacing="1">BLOOD PRESSURE ?</text>
  <text x="900" y="822" text-anchor="end" font-family="InterBlack" font-size="27" fill="{TEAL}" letter-spacing="1">BREATHING ?</text>
 </g>""")}
<div id="{idp}t2" class="big" style="top:205px;left:60px;width:880px;font-size:96px;color:{CREAM};opacity:0"><span>IT</span> <span>WASN'T</span> <span>JUST</span><br><span>THE</span> <span style="color:{CORAL}">HEART</span></div>'''


S1 = hook("h1")

S2 = f'''<div class="bgfill" style="background:linear-gradient(#0d1a33 0%,#2b3c66 55%,#6f6a8f 82%,#b48f8a 100%)"></div>
{svg(f'{A.stars(W, H, 30, 21, .35)}<g id="h2City">{A.skyline(W, H, 1010, 1.0, seed=23, lit=.3, cn=760)}</g>')}
<div class="snowL" style="position:absolute;inset:0;overflow:hidden">{snow("s2", 32, 2)}</div>
<div id="t2a" class="big" style="top:250px;left:60px;width:880px;font-size:170px;color:{GOLD}"><span style="font-size:74px;color:{CREAM}">LIVE FROM</span><br>THE 6IX</div>
{chip("t2c", "...INSIDE YOUR BODY", 300, 640, bg=TEAL, size=42)}'''

notes = "".join(f'<g transform="translate({x},{y})"><g class="nt"><ellipse cx="0" cy="0" rx="15" ry="11" transform="rotate(-20)" fill="{CREAM}"/>'
                f'<path d="M13 -3 V-52" stroke="{CREAM}" stroke-width="5"/></g></g>'
                for x, y in ((80, 170), (140, 150), (200, 180), (260, 140), (330, 160), (390, 130), (690, 160), (750, 140), (810, 170)))
staff = "".join(f'<path d="M40 {110 + k * 20} H840" stroke="#3a5a7a" stroke-width="3"/>' for k in range(5))
gauge = (f'<g transform="translate(440,380)"><path d="M-95 20 A95 95 0 0 1 95 20" fill="none" stroke="#24425f" stroke-width="22"/>'
         f'<path d="M-95 20 A95 95 0 0 1 95 20" fill="none" stroke="{GOLD}" stroke-width="22" stroke-dasharray="300" stroke-dashoffset="120"/>'
         f'<g id="nd3"><path d="M0 20 L0 -70" stroke="{CREAM}" stroke-width="9" stroke-linecap="round"/></g><circle cx="0" cy="20" r="14" fill="{CREAM}" stroke="{INK}" stroke-width="5"/></g>')
S3 = f'''<div class="navy"></div><div id="dots3" class="dots"></div>
<div id="pn3" class="panel"><div class="ptitle">THE STUDY · A LAB</div>
 {svg(f"""{staff}<g id="nts3">{notes}</g>
  <g id="pz3"><rect x="455" y="92" width="200" height="116" rx="16" fill="#c4b0ff" opacity=".16" stroke="#c4b0ff" stroke-width="4" stroke-dasharray="12 10"/>
   <path d="M470 150 H640" stroke="#c4b0ff" stroke-width="6" stroke-linecap="round"/></g>
  <g transform="translate(150,380)"><g id="sh3"><g id="sh3i"><path d="{heart_d}" transform="scale(1.25)" fill="{CORAL}" stroke="{INK}" stroke-width="6"/></g></g></g>
  <g id="sg3">{gauge}</g>
  <g id="sl3">{A.lungs(730, 385, .48, "lg3")}</g>""", 880, 650)}
 {chip("pzc3", "2-MIN PAUSE", 448, 222, bg="#c4b0ff", size=30)}
 <div id="la3" class="slab" style="left:40px;top:500px;width:220px;color:{CORAL}">HEART<br>RATE</div>
 <div id="lb3" class="slab" style="left:330px;top:500px;width:220px;color:{GOLD}">BLOOD<br>PRESSURE</div>
 <div id="lc3" class="slab" style="left:620px;top:500px;width:220px;color:{TEAL}">BREATHING</div>
</div>
<div id="cd3" class="card" style="border-left-color:#9fc3e8"><h3 style="color:#1e56ac">BERNARDI 2006 · HEART</h3><p>24 people in a lab: music with 2-min pauses.</p></div>'''

# S4: three lines wiggle around the start line during music, then all dip below it in the pause
GX0, GX1, GXP, GY = 70, 830, 440, 250
def gline(seed, amp, dip, off):
    rnd = random.Random(seed); pts = []
    for k in range(0, 61):
        x = GX0 + (GX1 - GX0) * k / 60
        if x < GXP: y = GY + off + amp * math.sin(k * 1.3 + seed) + rnd.uniform(-amp * .3, amp * .3)
        else:
            u = min(1, (x - GXP) / 160)
            y = GY + off * (1 - u) + dip * (1 - math.cos(math.pi * u)) / 2 + amp * .35 * math.sin(k * 1.3 + seed)
        pts.append(f"{x:.1f} {y:.1f}")
    return "M" + " L".join(pts)
LINES = [("hr4", CORAL, gline(1, 16, 92, -10)), ("bp4", GOLD, gline(2, 11, 70, 4)), ("br4", TEAL, gline(3, 20, 116, 12))]
S4 = f'''<div class="navy"></div><div id="dots4" class="dots"></div>
<div id="pn4" class="panel"><div class="ptitle">IN THE PAUSES</div>
 {svg(f"""<rect id="pr4" x="{GXP}" y="80" width="{GX1 - GXP + 20}" height="400" rx="18" fill="#c4b0ff" opacity=".1"/>
  <path id="bl4" d="M{GX0} {GY} H{GX1 + 10}" stroke="#96b0c4" stroke-width="4" stroke-dasharray="12 12"/>
  {"".join(f'<path id="{i}" d="{d}" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/>' for i, c, d in LINES)}
  <g id="ar4" opacity="0"><path d="M690 300 V420" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/><path d="M660 392 L690 432 L720 392" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>""", 880, 650)}
 <div class="slab" style="left:{GX0 - 10}px;top:{GY - 62}px;width:170px;font-size:24px;color:#96b0c4;text-align:left">START</div>
 <div class="slab" style="left:{GXP + 20}px;top:92px;width:220px;font-size:26px;color:#c4b0ff;text-align:left">PAUSE</div>
 <div class="slab" style="left:{GX0}px;top:92px;width:220px;font-size:26px;color:#9fc3e8;text-align:left">MUSIC</div>
 {chip("bw4", "BELOW START", 470, 450, bg=GOLD, size=32)}
 {chip("k4a", "HEART RATE", 40, 548, bg=CORAL, size=28)}
 {chip("k4b", "BLOOD PRESSURE", 290, 548, bg=GOLD, size=28)}
 {chip("k4c", "BREATHING", 630, 548, bg=TEAL, size=28)}
</div>
<div id="cd4" class="card" style="border-left-color:{GOLD}"><h3 style="color:#a8780a">BERNARDI 2006</h3><p>All three fell below where they started.</p></div>'''

S5 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 40%, #2a2350 0%, #141a33 55%, #0a1020 100%)"></div>
<div id="ptc5" style="position:absolute;inset:0">{"".join(f'<div class="ptc" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"></div>' for x, y, s in [(random.Random(k).uniform(80, 920), random.Random(k + 50).uniform(480, 860), random.Random(k + 90).uniform(10, 22)) for k in range(16)])}</div>
<div id="t5" class="big" style="top:225px;left:60px;width:880px;font-size:112px;color:{CREAM}"><span>SILENCE</span><br><span style="color:#c4b0ff">ISN'T EMPTY</span></div>
{svg(f'<circle id="rg5" cx="540" cy="680" r="150" fill="none" stroke="#c4b0ff" stroke-width="6" opacity="0"/>')}
<div id="hb5" class="lot" style="left:380px;top:560px;width:320px;height:244px"></div>'''

S6 = f'''<div class="bgfill" style="background:linear-gradient(#55698a 0%,#8597b4 45%,#b9c4d6 75%,#d8dde6 100%)"></div>
{svg(f"""<g opacity=".5">{A.skyline(W, H, 1250, .62, seed=31, lit=.0, cn=120, ground="#8a95a8")}</g>
 <g id="och6">{A.old_city_hall(600, 1300, .78, "och6")}</g>
 <rect x="-20" y="1296" width="1120" height="700" fill="#6b7383"/>
 <path d="M-20 1300 H1100" stroke="{INK}" stroke-width="6"/>
 {A.cenotaph(830, 1350, .78, "cen6")}
 <circle id="glow6" cx="600" cy="{1300 - 720 * .78:.0f}" r="70" fill="none" stroke="{GOLD}" stroke-width="8" opacity="0"/>""")}
<div class="snowL" style="position:absolute;inset:0;overflow:hidden">{snow("s6", 44, 6)}</div>
{chip("loc6", "OLD CITY HALL · 11:00", 70, 236, bg=CREAM, size=32)}'''

S7 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 45% 35%, #1d2a4a 0%, #0c1426 60%, #070c18 100%)"></div>
{svg(f'<g id="pp7w">{A.poppy(470, 600, 165, "pp7", 10)}</g>')}
<div id="cn7" class="lot" style="left:720px;top:470px;width:200px;height:320px"></div>
<div id="t7" class="big" style="top:250px;left:60px;width:880px;font-size:92px;color:{CREAM}">LEST WE FORGET</div>
<div id="cd7" class="card" style="border-left-color:{TEAL}"><h3 style="color:#188076">HEADS UP</h3><p>Lab study, 24 people, music with pauses. Not a ceremony.</p></div>'''

S8 = f'''<div class="bgfill" style="background:radial-gradient(ellipse at 50% 30%, #1d3a66 0%, #0c1622 70%)"></div>
<div id="pn8" class="panel" style="top:220px;height:600px;background:rgba(15,34,54,.96)">
 <div id="sub8" class="subbtn" style="background:{CORAL};color:{INK}">SUBSCRIBE</div>
 <div id="subd8" class="subbtn" style="background:#3a4a5e;color:{CREAM};opacity:0;font-size:60px">SUBSCRIBED ✓</div>
 {svg(A.poppy(800, 140, 48, "pp8", 6), 880, 600)}
 <div style="position:absolute;left:40px;top:262px;font:34px InterBlack;color:{GOLD};letter-spacing:.05em">SOURCE</div>
 <div id="src8" style="position:absolute;left:40px;top:318px;width:800px;font:40px/1.35 InterSB;color:#cfe0ff">
  Bernardi 2006 · Heart<br><span style="color:#96b0c4;font-size:34px">Lab study, 24 people<br>Links in the description</span></div>
</div>'''

S9 = hook("h9")

scenes = [("s1", 0, C1, S1), ("s2", C1, C2, S2), ("s3", C2, C3, S3), ("s4", C3, C4, S4), ("s5", C4, C5, S5), ("s6", C5, C6, S6),
          ("s7", C6, C7, S7), ("s8", C7, C8, S8), ("s9", C8, T, S9)]
def span(i, a, b):
    s0 = 0 if i == 0 else a - XF / 2
    s1 = T if i == len(scenes) - 1 else b + XF / 2
    return round(s0, 3), round(s1 - s0, 3)
scene_html = "\n".join(f'<div id="{sid}" class="scene clip" data-start="{span(k, a, b)[0]}" data-duration="{span(k, a, b)[1]}">{h}</div>'
                       for k, (sid, a, b, h) in enumerate(scenes))

# ------------------------------------------------------------------ timeline beats
J = []
def j(s): J.append(s)
j('const pop=(s,t)=>tl.fromTo(s,{scale:0.85,opacity:0},{scale:1,opacity:1,duration:0.4,ease:"power2.out"},t);')
j('const out=(s,t)=>tl.to(s,{opacity:0,duration:0.25,ease:"power1.in"},t);')
j('const slideIn=(s,t)=>tl.fromTo(s,{x:60,opacity:0},{x:0,opacity:1,duration:0.5,ease:"power2.out",immediateRender:false},t);')
# soft cross-fades + a slow push-in on every scene (no shake / whip / punch)
for k, (sid, a, b, _h) in enumerate(scenes):
    s0, d = span(k, a, b)
    if k > 0: j(f'tl.fromTo("#{sid}",{{opacity:0}},{{opacity:1,duration:{XF},ease:"sine.inOut",immediateRender:false}},{s0});')
    if k < len(scenes) - 1:   # the loop scene stays at scale 1 so the last frame = the hook frame
        j(f'tl.fromTo("#{sid}",{{scale:1}},{{scale:1.045,duration:{d:.3f},ease:"none",transformOrigin:"540px 760px",immediateRender:false}},{s0});')
j(f'gsap.set("#s1",{{scale:1,opacity:1}});')
# Cyto glides between marks under the cross-fades
POSES = [(0, POS_HOOK), (C1, POS_BIG), (C2, POS_V2), (C7, POS_HOOK)]
j(f'gsap.set("#cytoPos",{json.dumps(POS_HOOK)});')
for t, pos in POSES[1:]:
    j(f'tl.to("#cytoPos",{dict(pos, duration=XF, ease="sine.inOut")!r},{t - XF / 2:.3f});'.replace("'", '"'))
j(f'tl.set("#cytoPos",{json.dumps(POS_HOOK)},0);')
# cup set down the WHOLE video (respect): the held cup is hidden, the table cup is shown
# eyes closed for the held moment after "Lest we forget"
# (cup set down + eyes-closed hold live in the rig runtime)


def hook_js(idp, t0, live=True):
    """ECG head sweeps from the 'music' part through the slowing 'silence' part (seek-safe: onUpdate positions the head)."""
    if not live:
        return ''
    return (f'(()=>{{const p=document.querySelector("#{idp}ecg"),g=document.querySelector("#{idp}eg"),h=document.querySelector("#{idp}hd");const L={ECG_LEN:.1f},L0={L0:.1f};'
            f'const S={{v:L0}};const upd=()=>{{p.style.strokeDashoffset=L-S.v;g.style.strokeDashoffset=L-S.v;const q=p.getPointAtLength(S.v);h.setAttribute("cx",q.x);h.setAttribute("cy",q.y);}};'
            f'tl.fromTo(S,{{v:L0}},{{v:L,duration:{ECG_DUR},ease:"none",onUpdate:upd,immediateRender:false}},{t0});'
            f'tl.fromTo("#{idp}hd",{{attr:{{r:13}}}},{{attr:{{r:18}},duration:0.16,yoyo:true,repeat:1,immediateRender:false}},{t0});}})();'
            + "".join(f'tl.fromTo("#{idp}hd",{{attr:{{r:13}}}},{{attr:{{r:20}},duration:0.14,yoyo:true,repeat:1,immediateRender:false}},{t0 + bt:.3f});' for bt in BEAT_T)
            + f'tl.fromTo("#{idp}t",{{scale:1}},{{scale:1.03,duration:{C1:.2f},ease:"none",transformOrigin:"50% 50%",immediateRender:false}},{t0});')


# ---- S1 hook (3 movers: trace head, caption, Cyto). Claim + trace already on screen at 0.00 s.
j(hook_js("h1", 0.0))
j(f'tl.set("#h1hr",{{opacity:0}},0);tl.fromTo("#h1hr",{{opacity:0,scale:.6,svgOrigin:"0 0"}},{{opacity:1,scale:1,svgOrigin:"0 0",duration:0.3,ease:"power2.out",immediateRender:false}},{tHeart1 - 0.06});'
  + "".join(f'tl.fromTo("#h1hri",{{scale:1}},{{scale:1.18,svgOrigin:"0 0",duration:0.13,yoyo:true,repeat:1,immediateRender:false}},{bt:.3f});' for bt in (tRate1, tRate1 + 1.15, tRate1 + 2.45)))
j(f'tl.to("#h1t",{{opacity:0,duration:0.22,ease:"sine.in"}},{tAnd - 0.12:.3f});'
  f'tl.set("#h1t2",{{opacity:0}},0);tl.fromTo("#h1t2",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.3,ease:"power2.out",immediateRender:false}},{tAnd - 0.02:.3f});'
  f'tl.set("#h1rh",{{opacity:0}},0);tl.to("#h1rh",{{opacity:1,duration:0.25}},{tWasnt - 0.05:.3f});'
  f'tl.fromTo("#h1bp",{{attr:{{"stroke-dashoffset":110}}}},{{attr:{{"stroke-dashoffset":0}},duration:0.8,ease:"sine.inOut",immediateRender:false}},{tWasnt - 0.05:.3f});'
  f'tl.fromTo("#h1br",{{attr:{{"stroke-dashoffset":110}}}},{{attr:{{"stroke-dashoffset":0}},duration:0.8,ease:"sine.inOut",immediateRender:false}},{tJust:.3f});'
  f'tl.to("#h1t2",{{opacity:0,duration:0.25}},{C1 - 0.42:.3f});')
# ---- S2 catchphrase: quiet dawn skyline, gentle snow
j(snow_js("s2", C1 - XF / 2, C2 + XF / 2))
j(f'document.querySelectorAll("#h2City .win").forEach((w,i)=>{{ if(i%5==0) tl.to(w,{{opacity:.25,duration:0.6,repeat:3,yoyo:true}},{C1}+(i%7)*0.25); }});')
j(f'tl.fromTo("#h2City",{{y:40}},{{y:0,duration:{C2 - C1:.3f},ease:"sine.out"}},{C1 - XF / 2:.3f});')
j(f'tl.set("#t2a",{{opacity:0}},0);tl.fromTo("#t2a",{{y:20,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"power2.out",immediateRender:false}},{tLive - 0.08});')
j(f'tl.set("#t2c",{{opacity:0}},0);tl.fromTo("#t2c",{{y:20,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"power2.out",immediateRender:false}},{tInside - 0.05});')
j(f'tl.to(["#t2a","#t2c"],{{opacity:0,duration:0.25}},{C2 - 0.42:.3f});')
# ---- S3 the study: music on a staff, the 2-min pause, three things measured
j(f'tl.fromTo("#pn3",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power2.out",immediateRender:false}},{C2 - XF / 2:.3f});')
j(f'document.querySelectorAll("#nts3 .nt").forEach((n,i)=>tl.fromTo(n,{{y:0}},{{y:-10,duration:0.42,yoyo:true,repeat:{int((C3 - C2) / 0.42)},ease:"sine.inOut",delay:(i%3)*0.14,immediateRender:false}},{C2}));')
j(f'tl.fromTo("#pz3",{{opacity:0}},{{opacity:1,duration:0.35}},{tTwoMin - 0.05});tl.set("#pz3",{{opacity:0}},0);')
j(f'tl.set("#pzc3",{{opacity:0}},0);pop("#pzc3",{tPauses - 0.05});')
for gid, lab, t in (("#sh3", "#la3", tHeart2), ("#sg3", "#lb3", tBlood), ("#sl3", "#lc3", tBreathing)):
    j(f'tl.set("{lab}",{{opacity:0}},0);tl.set("{gid}",{{opacity:0.18}},0);tl.fromTo("{gid}",{{opacity:0.18,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out",immediateRender:false}},{t - 0.08});'
      f'tl.fromTo("{lab}",{{opacity:0}},{{opacity:1,duration:0.35,immediateRender:false}},{t - 0.02});')
j(f'gsap.set("#sh3i",{{svgOrigin:"0 0"}});tl.fromTo("#sh3i",{{scale:1}},{{scale:1.12,duration:0.18,yoyo:true,repeat:{int((C3 - tHeart2) / 0.36) * 2 - 1},ease:"sine.inOut",svgOrigin:"0 0",repeatDelay:0.25,immediateRender:false}},{tHeart2});')
j(f'tl.fromTo("#nd3",{{rotation:-30,svgOrigin:"0 20"}},{{rotation:24,svgOrigin:"0 20",duration:0.5,ease:"power2.out",immediateRender:false}},{tBlood});'
  f'tl.to("#nd3",{{rotation:14,svgOrigin:"0 20",duration:0.6,yoyo:true,repeat:2,ease:"sine.inOut"}},{tBlood + 0.5});')
j(f'tl.fromTo("#lg3",{{scale:1}},{{scale:1.08,svgOrigin:"0 0",duration:0.7,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{tBreathing});')
j(f'tl.set("#cd3",{{opacity:0}},0);slideIn("#cd3",{tMusic + 0.1});')
# ---- S4 the three lines dip below the start line
j(f'tl.fromTo("#pn4",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power2.out",immediateRender:false}},{C3 - XF / 2:.3f});')
for k, (i, c, d) in enumerate(LINES):
    j(f'tl.set("#{i}",{{opacity:0}},0);tl.set("#{i}",{{opacity:1}},{C3 + 0.05 + k * 0.05:.3f});')
    j(f'tl.fromTo("#{i}",{{attr:{{"stroke-dashoffset":1000}}}},{{attr:{{"stroke-dashoffset":520}},duration:{tPauses2 + 0.4 - C3:.2f},ease:"none",immediateRender:false}},{C3 + 0.05 + k * 0.05:.3f});'
      f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:{tDropped + 0.5 - tPauses2 - 0.4:.2f},ease:"power1.inOut"}},{tPauses2 + 0.45 + k * 0.05:.3f});')
j(f'tl.fromTo("#pr4",{{opacity:0}},{{opacity:.1,duration:0.4,immediateRender:false}},{tPauses2 - 0.1});tl.set("#pr4",{{opacity:0}},0);')
j(f'tl.to("#bl4",{{stroke:"{GOLD}",duration:0.3,yoyo:true,repeat:3}},{tBelow - 0.05});')
j(f'tl.fromTo("#ar4",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out",immediateRender:false}},{tBelow - 0.05});')
j(f'tl.set("#bw4",{{opacity:0}},0);pop("#bw4",{tBelow});')
j(f'tl.set(["#k4a","#k4b","#k4c"],{{opacity:0}},0);' + "".join(f'pop("#{k}",{C3 + 0.25 + n * 0.12:.2f});' for n, k in enumerate(("k4a", "k4b", "k4c"))))
j(f'tl.set("#cd4",{{opacity:0}},0);slideIn("#cd4",{tAll});')
# ---- S5 silence isn't empty: the heart beats slower and slower, particles drift to a stop
j(f'tl.set("#t5",{{opacity:0}},0);tl.fromTo("#t5",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"power2.out",immediateRender:false}},{tSilence2 - 0.05});')
j(f'document.querySelectorAll("#ptc5 .ptc").forEach((p,i)=>tl.fromTo(p,{{y:0,x:0}},{{y:(i%2?-50:50),x:(i%3-1)*30,duration:{C5 - C4 + XF:.2f},ease:"power3.out",immediateRender:false}},{C4 - XF / 2:.3f}));')
hb = ('const L_hb5=lottie.loadAnimation({container:document.getElementById("hb5"),renderer:"svg",loop:false,autoplay:false,animationData:'
      + open(f"{P}/assets/heart-beat.json").read() + '});L_hb5.goToAndStop(0,true);')
for k, bt in enumerate(HB_T):
    hb += (f'(()=>{{const P={{f:0}};tl.fromTo(P,{{f:0}},{{f:L_hb5.totalFrames-1,duration:{0.42 + k * 0.04:.2f},ease:"none",immediateRender:false,'
           f'onUpdate:()=>L_hb5.goToAndStop(P.f,true)}},{bt});}})();')
    hb += f'tl.fromTo("#rg5",{{attr:{{r:140}},opacity:.7}},{{attr:{{r:{230 - k * 10}}},opacity:0,duration:{0.9 + k * 0.1:.2f},ease:"sine.out",immediateRender:false}},{bt});'
j(hb)
# ---- S6 Old City Hall: the clock reaches 11:00, a soft bell, snow slows almost to a stop
CCX, CCY = 600, round(1300 - 720 * .78, 1)
j(f'tl.fromTo("#och6M",{{rotation:-40,svgOrigin:"{CCX} {CCY}"}},{{rotation:0,svgOrigin:"{CCX} {CCY}",duration:{tEleven - C5 + XF / 2:.2f},ease:"sine.inOut",immediateRender:false}},{C5 - XF / 2:.3f});')
j(f'tl.fromTo("#och6H",{{rotation:326.7,svgOrigin:"{CCX} {CCY}"}},{{rotation:330,svgOrigin:"{CCX} {CCY}",duration:{tEleven - C5 + XF / 2:.2f},ease:"sine.inOut",immediateRender:false}},{C5 - XF / 2:.3f});')
j(f'tl.set("#glow6",{{opacity:0}},0);tl.fromTo("#glow6",{{attr:{{r:70}},opacity:.9}},{{attr:{{r:150}},opacity:0,duration:1.6,ease:"sine.out",immediateRender:false}},{tEleven});')
j(snow_js("s6", C5 - XF / 2, C6 + XF / 2, 1800, t_slow=tQuiet2 - 0.3, slow=0.08))
j(f'tl.set("#loc6",{{opacity:0}},0);tl.fromTo("#loc6",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.45,ease:"power2.out",immediateRender:false}},{C5 + 0.1});')
j(f'tl.to("#loc6",{{opacity:0,duration:0.25}},{C6 - 0.42:.3f});')
# ---- S7 Lest we forget: the poppy opens, a candle, the held moment, then the caveat card
j(f'tl.fromTo("#pp7",{{scale:0.7,opacity:0,svgOrigin:"470 600"}},{{scale:1,opacity:1,svgOrigin:"470 600",duration:1.1,ease:"sine.out",immediateRender:false}},{C6 - 0.05:.2f});')
j(f'tl.fromTo("#pp7w",{{rotation:0,svgOrigin:"470 600"}},{{rotation:5,svgOrigin:"470 600",duration:{C7 - C6:.2f},ease:"none",immediateRender:false}},{C6});')
j(lot("cn7", "candle-2.json", C6 - XF / 2, C7 + XF / 2, loops=2))
j(f'tl.set("#t7",{{opacity:0}},0);tl.fromTo("#t7",{{opacity:0,y:15}},{{opacity:1,y:0,duration:0.7,ease:"power2.out",immediateRender:false}},{tLest - 0.05});')
j(f'tl.set("#cd7",{{opacity:0}},0);slideIn("#cd7",{tNot - 0.15});')
j(f'tl.to("#t7",{{opacity:0,duration:0.3}},{C7 - 0.45:.3f});')
# ---- S8 outro: subscribe + source (gentle)
j(f'tl.fromTo("#pn8",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:"power2.out",immediateRender:false}},{C7 - XF / 2:.3f});')
j(f'tl.fromTo("#sub8",{{scale:1}},{{scale:0.96,duration:0.1,yoyo:true,repeat:1}},{tSub + 0.15});'
  f'tl.set("#subd8",{{opacity:0}},0);tl.set("#subd8",{{opacity:1}},{tSub + 0.3});tl.set("#sub8",{{opacity:0}},{tSub + 0.3});')
j(f'tl.to("#pn8",{{opacity:0,duration:0.25}},{C8 - 0.42:.3f});')
j(f'tl.fromTo("#src8",{{opacity:0,y:15}},{{opacity:1,y:0,duration:0.4,immediateRender:false}},{C7 + 0.2});')
FOLLOW = (round(T * 0.42, 2), round(T * 0.56, 2))
j(f'tl.set("#follow",{{opacity:0}},0);tl.fromTo("#follow",{{opacity:0,y:12}},{{opacity:.95,y:0,duration:0.5,ease:"sine.out",immediateRender:false}},{FOLLOW[0]});tl.to("#follow",{{opacity:0,duration:0.5,ease:"sine.in"}},{FOLLOW[1]});')
# ---- S9 loop frame = hook frame (static frame-1 state)

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
.dots {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; background-image:radial-gradient(rgba(120,170,220,.08) 3px, transparent 4px); background-size:70px 70px; }}
.big {{ position:absolute; left:0; width:1080px; text-align:center; font-family:InterBlack; line-height:.98; letter-spacing:-2px;
  paint-order:stroke fill; -webkit-text-stroke:14px #0c1622; text-shadow:0 10px 0 #0c1622; opacity:0; z-index:30; }}
.chip {{ position:absolute; font-family:InterBlack; letter-spacing:.03em; padding:10px 22px; border-radius:30px; border:5px solid #0c1622;
  box-shadow:0 6px 0 #0c1622; white-space:nowrap; opacity:0; color:#0c1622; z-index:30; }}
.slab {{ position:absolute; text-align:center; font:32px/1.05 InterBlack; paint-order:stroke fill; -webkit-text-stroke:6px #0c1622; z-index:30; }}
.flake {{ position:absolute; border-radius:50%; background:#FAF4E8; }}
.ptc {{ position:absolute; border-radius:50%; background:#c4b0ff; opacity:.35; }}
.subbtn {{ position:absolute; left:150px; top:70px; width:580px; height:140px; border-radius:70px; border:7px solid #0c1622; box-shadow:0 10px 0 #0c1622;
  font:64px InterBlack; text-align:center; line-height:126px; }}
#pill {{ position:absolute; top:110px; left:50%; margin-left:-210px; width:420px; text-align:center; background:#FFD166; color:#0c1622; font:23px InterBlack; letter-spacing:.06em; padding:12px 0; border-radius:40px; z-index:60; }}
{K.rig_css()}
{C.CAP_CSS}
{C.V2_CSS}
.card p {{ font-size:34px; }}
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
  <div id="cytoLayer">{K.rig_html("hoodie", "solemn", 3)}</div>
</div></div>
<div id="follow" class="chip" style="left:560px;top:1400px;font-size:30px;background:#16263c;color:{CREAM};border-color:#2c4766;box-shadow:none;z-index:40">+ FOLLOW FOR MORE</div>
<div id="pill" class="clip" data-start="0" data-duration="{T}">6IXTY SECONDS OF SCIENCE</div>
{cap_html}
</div>
<script>{K.runtime_js()}</script>
<script>
const tl = gsap.timeline({{ paused: true }});
const T = {T};
{rig_js}
{chr(10).join(J)}
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
json.dump({"name": "ep14v3"}, open("meta.json", "w"))
print("built", len(html), "bytes; T", T, "cuts", CUTS, "words", len(WORDS), "voice", round(TM["total"], 2), "beats", BEAT_T, "hb", HB_T)
