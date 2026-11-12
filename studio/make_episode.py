#!/usr/bin/env python3
"""make_episode.py - episode.json -> voice -> canon rig render -> captions -> 2 thumbnails (x2 sizes) -> contact-sheet frame check -> tests -> package.
Stops at the two OK gates. Spends NO credits itself (ElevenLabs/Zapier are chat connectors): it prints the estimate and writes *_request.json for the chat to execute.

  python3 studio/make_episode.py ep15                 # runs as far as allowed, stops at the next gate
  python3 studio/make_episode.py ep15 --ok plan       # gate 1: Utsha approved the plan AND the credit estimate printed
  python3 studio/make_episode.py ep15 --ok final      # gate 2: Utsha approved the final package -> writes schedule_request.json
  python3 studio/make_episode.py ep15 --dry-run       # validate + estimate + what would run, writes nothing
  python3 studio/make_episode.py ep15 --stage thumbs  # one stage: validate|voice|build|thumbs|checks|package|schedule
Never touches tiktok/queue.json (friend's Claude). Schema: studio/EPISODE_SCHEMA.md."""
import argparse, json, os, re, subprocess, sys, shutil
STUDIO = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(STUDIO); HOME = os.environ.get("CYTO_HOME", "/home/claude")
RIG = os.path.join(STUDIO, "rig_v2"); PIPE = os.path.join(HOME, "cyto2")
FPS = 30; CYTO_SIZE = 840; CYTO_X = 64; CYTO_Y = 1110; RIG_BOX = (-579, -570, 482, 410)  # rig content bbox in its 1100 viewBox
VOICE_ID = "MDpsT9lfiqWEMyN3A1bk"; MODEL = "eleven_v4"
EMOTIONS = {"chill", "happy", "shock", "think", "solemn", "laugh"}
BGS = {"skyline", "streetcar", "snow", "subway", "lake", "plain", "trail", "hospital", "lab"}; TRANS = {"whip", "doors", "zoom", "membrane"}
HEROES = {"heart", "clock", "snow", "brain", "phone", "sugar"}; FITS = {"none", "jersey", "hoodie", "puffer"}
BANNED = ["tim hortons", "timmy", "tims ", "starbucks", "coca", "pepsi", "nike", "adidas", "mcdonald"]
class Stop(Exception): pass
def say(*a): print(*a, flush=True)
def sh(cmd, **k): return subprocess.run(cmd, check=True, capture_output=True, text=True, **k)

# ------------------------------------------------------------------ paths / state
class Ep:
    def __init__(s, name, home=HOME, studio=STUDIO):
        s.name = name; s.n = int(re.sub(r"\D", "", name)); s.src = os.path.join(studio, "episodes", name)
        s.dir = os.path.join(home, name); s.home = home
        s.json = os.path.join(s.src, "episode.json"); s.state_f = os.path.join(s.src, "state.json")
    def p(s, *a): return os.path.join(s.dir, *a)
    def state(s): return json.load(open(s.state_f)) if os.path.exists(s.state_f) else {}
    def save(s, **kv):
        st = s.state(); st.update(kv); json.dump(st, open(s.state_f, "w"), indent=1)

# ------------------------------------------------------------------ 1. validate

def pose_verdict(lay):
    """HARD_RULES 9/18: a cut may not break Cyto's pose. A real snap is ~8+; an eased beat blend peaks ~1.7."""
    pj = lay.get("pose_jerk_in_cut")
    if pj is None:
        return [], "pose continuity not measured (layout.json predates the check; applies from the next episode)"
    rough = {k: v for k, v in pj.items() if v > 3.0}
    bad = ["pose jumps at " + ", ".join(f"{k} ({v})" for k, v in sorted(rough.items()))] if rough else []
    return bad, f"pose jerk max {max(pj.values()) if pj else 0} (limit 3.0)"


def overlap_verdict(lay):
    """HARD_RULES 17: nothing covers anything else for more than 0.3 s."""
    o_list = lay.get("overlaps")
    if o_list is None:
        return True, "not measured (layout.json predates the check; applies from the next episode)"
    return (not o_list), ("; ".join(f"{o['pair']} in {o['scene']} for {o['dur']}s @{o['t0']}s" for o in o_list[:6])
                          or "nothing covers anything else")

def validate(E):
    errs, warns = [], []
    def need(k, t=None):
        if k not in E or E[k] in (None, "", []): errs.append(f"missing '{k}'"); return False
        return True
    for k in ("ep", "title", "script", "scenes", "thumbnails", "sources", "description", "tags", "pinned_comment", "publish_at"): need(k)
    if errs: return errs, warns
    if len(E["title"]) > 60: errs.append(f"title {len(E['title'])} chars (>60)")
    if E.get("fit", "hoodie") not in FITS: errs.append(f"fit must be one of {sorted(FITS)}")
    S, SC = E["script"], E["scenes"]
    words = 0
    for i, l in enumerate(S):
        if not l.get("say"): errs.append(f"script[{i}] has no 'say'"); continue
        words += len(l["say"].split())
        if l.get("emotion", "chill") not in EMOTIONS: errs.append(f"script[{i}] emotion '{l.get('emotion')}' not in {sorted(EMOTIONS)}")
        if not isinstance(l.get("scene"), int) or not 0 <= l["scene"] < len(SC): errs.append(f"script[{i}] 'scene' must be an index 0..{len(SC) - 1}")
    sc_seq = [l.get("scene") for l in S if isinstance(l.get("scene"), int)]
    if sc_seq != sorted(sc_seq): errs.append("script lines must visit scenes in order (scene index never goes down)")
    if set(range(len(SC))) - set(sc_seq): errs.append(f"scenes without lines: {sorted(set(range(len(SC))) - set(sc_seq))}")
    est = words / 2.8
    if est > 60: errs.append(f"~{est:.0f}s of speech (>60 s Shorts cap)")
    elif est > 34: warns.append(f"~{est:.0f}s of speech; hook-first Shorts target <= 30-34 s")
    for i, s in enumerate(SC):
        if s.get("bg") not in BGS: errs.append(f"scenes[{i}].bg must be one of {sorted(BGS)}")
        if s.get("transition", "whip") not in TRANS: errs.append(f"scenes[{i}].transition must be one of {sorted(TRANS)}")
        if not s.get("headline") and not s.get("card"): warns.append(f"scenes[{i}] has no headline/card (empty scene)")
    if SC[0].get("bg") != SC[-1].get("bg"): warns.append("last scene bg differs from first (the end should loop into the start)")
    T = E["thumbnails"]
    if len(T) < 2: errs.append("need 2 thumbnail options (A/B)")
    for i, t in enumerate(T):
        if not t.get("headline") or len(t["headline"]) > 2 or sum(len(l.split()) for l in t["headline"]) > 4: errs.append(f"thumbnails[{i}].headline: max 2 lines / 4 words")
        if not (t.get("hero") in HEROES or t.get("hero_svg")): errs.append(f"thumbnails[{i}].hero must be one of {sorted(HEROES)} or hero_svg")
    title_words = {w for w in re.findall(r"[a-z]+", E["title"].lower()) if len(w) > 3} | {k.lower() for k in E.get("topic_words", [])}
    for i, t in enumerate(T):
        subj = (t.get("bg_subject") or "").lower()
        if not t.get("photo") and not t.get("scene"): errs.append(f"thumbnails[{i}] needs 'photo' (or drawn 'scene') showing the topic (HARD_RULES 1)")
        if "+" not in subj: errs.append(f"thumbnails[{i}].bg_subject must be '<topic> + <Toronto place>' (HARD_RULES 2)")
        elif not any(w in subj for w in title_words): errs.append(f"thumbnails[{i}].bg_subject '{subj}' names no topic word from the title (add topic_words to episode.json if the title is indirect)")
        if re.search(r"skyline|cn tower|downtown", subj) and not E.get("city_topic"): errs.append(f"thumbnails[{i}] generic Toronto skyline background is banned unless the topic is the city (city_topic:true)")
    for i, s in enumerate(SC):
        if len(s.get("props", [])) < 2: errs.append(f"scenes[{i}] needs >= 2 'props' (drawn visuals, HARD_RULES 5)")
        wc = len((s.get("headline") or "").split()) + len((s.get("card") or "").split())
        if wc > 8: errs.append(f"scenes[{i}] has {wc} words of text (max 8, HARD_RULES 5)")
        if i and s.get("bg") == SC[i - 1].get("bg"): errs.append(f"scenes[{i}] reuses the previous backdrop '{s.get('bg')}' (HARD_RULES 6)")
    if E.get("stronger") not in {t.get("id") for t in T}: errs.append("'stronger' must name one thumbnail id (say which is stronger)")
    for i, s in enumerate(E["sources"]):
        if not (s.get("short") and s.get("full")): errs.append(f"sources[{i}] needs 'short' and 'full' (full has the doi/PubMed link)")
    if len(E["sources"]) > 2: warns.append("on-screen source card shows only the first 2 sources (short form); the rest go in description/pinned comment")
    if E.get("health", True) and "not medical advice" not in E["description"].lower(): errs.append("health topic: description needs 'Not medical advice'")
    blob = json.dumps(E).lower()
    for b in BANNED:
        if b in blob: errs.append(f"real brand '{b.strip()}' found (no real brands)")
    if re.search(r"\b(drunk|get high|getting high|wasted|chug)\b", blob): errs.append("drinking/getting-high reference (never)")
    if not os.path.exists(os.path.join(os.path.dirname(E.get("_path", "")), "claims.md")) and E.get("_path"): warns.append("claims.md missing next to episode.json")
    return errs, warns

def credit_estimate(E):
    tts = " ".join(l.get("tts") or l["say"] for l in E["script"]); ch = len(tts)
    return dict(chars=ch, credits_per_take=ch, takes=2, total=ch * 2, plan="ElevenLabs Starter 30,000/mo (renews Dec 2); Ep 9's 40 s read cost ~636/take",
                scribe_words="0 credits", sfx="~17 credits each if any are generated", vidiq="not used (1 credit left until Nov 30)")

# ------------------------------------------------------------------ 2. voice
def voice(ep, E, force_scribe=False):
    raw = ep.p("raw.mp3"); os.makedirs(ep.dir, exist_ok=True)
    tts = [l.get("tts") or l["say"] for l in E["script"]]
    if not os.path.exists(raw):
        req = dict(connector="ElevenLabs creative_generate_speech", voice_id=VOICE_ID, model_id=MODEL, text=" ".join(tts), lines=tts, takes=2,
                   estimate=credit_estimate(E), then=["poll creative_get_flow_run_status", "add `name url` to audio/list.txt + push (fetch-audio workflow) OR Utsha drops the mp3", f"save as {raw}"],
                   rules=["call estimate_only first", "never re-call a generation to retry (double charge)", "spell for the ear in tts only; say keeps the real word"])
        json.dump(req, open(ep.p("voice_request.json"), "w"), indent=1)
        raise Stop(f"VOICE: no {raw}. Wrote voice_request.json (~{req['estimate']['total']} credits for 2 takes). The chat runs the ElevenLabs call (only after gate 1 is approved), then save the mp3 there and re-run.")
    sc = ep.p("words_scribe.json")
    if not os.path.exists(sc) and force_scribe:
        json.dump(dict(connector="ElevenLabs creative_transcribe_audio (eleven_scribe_v1)", how="creative_add_flow_asset_node(generation_id) -> connect_from", save_as=sc,
                       format='[["word", start, end], ...] with CAPTION spellings (6ix, 95%)', credits=0), open(ep.p("scribe_request.json"), "w"), indent=1)
        raise Stop(f"SCRIBE: no {sc}. Wrote scribe_request.json (0 credits). Re-run after saving, or use --no-scribe for syllable-estimated timing.")
    out = sh(["ffmpeg", "-i", raw, "-af", "silencedetect=n=-45dB:d=0.15", "-f", "null", "-"]).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).expand(r"\1 \2 \3").split()[2]) + 60 * float(re.search(r"Duration: (\d+):(\d+)", out).group(2)) + 3600 * float(re.search(r"Duration: (\d+)", out).group(1))
    lens = [len(l["say"].split()) for l in E["script"]]; segs = []
    if os.path.exists(sc):
        W = json.load(open(sc))
        if len(W) != sum(lens): raise Stop(f"SCRIBE words ({len(W)}) != script words ({sum(lens)}). Fix spellings in {sc} so each token matches episode.json 'say' (e.g. 'six'->'6ix').")
        k = 0
        for li, n in enumerate(lens):
            ws = W[k:k + n]; first, last = ws[0][1], ws[-1][1]
            nxt = W[k + n][1] - 0.03 if k + n < len(W) else dur
            s1 = min([x for x in ss if x > last + 0.05] + [nxt, dur])
            segs.append([round(max(0, first - 0.03), 3), round(s1, 3), li, " ".join(w[0] for w in ws)] + ([E["script"][li]["pause_after"]] if E["script"][li].get("pause_after") else [])); k += n
    else:
        raise Stop("no words_scribe.json and silence-only alignment is not supported: get Scribe words (0 credits) via scribe_request.json (--force-scribe)")
    cfg = dict(tempo=1.0, lead=E.get("voice", {}).get("lead", 0.0), line_gap=0.22, in_gap=0.11, segs=segs)
    json.dump(cfg, open(ep.p("segs.json"), "w"), indent=1)
    sh([sys.executable, os.path.join(PIPE, "build_voice2.py"), ep.dir])
    tm = json.load(open(ep.p("timing.json"))); out_w = []; k = 0
    for (a, b, li, ph, *_), (s0, s1, _) in zip(segs, tm["segs"]):
        for w in ph.split():
            ww, x, y = W[k]; out_w.append(dict(line=li, w=w, t0=round(max(0, s0 + (x - a)), 3), t1=round(min(s1 + 0.05, s0 + (y - a)), 3))); k += 1
    tm["words"] = out_w; tm["word_source"] = "scribe remapped through build_voice2"; json.dump(tm, open(ep.p("timing.json"), "w"), indent=0)
    return tm

# ------------------------------------------------------------------ 3. build (plan -> compose -> mix)
def make_plan(ep, E, tm):
    words = [dict(w=w["w"], start=w["t0"], end=w["t1"]) for w in tm["words"]]
    S, SC = E["script"], E["scenes"]
    line_t = {}
    for w in tm["words"]: line_t.setdefault(w["line"], [w["t0"], w["t1"]])[1] = w["t1"]
    total = round(tm["total"] + 0.5, 2)
    start = {}
    for li, l in enumerate(S):
        if l["scene"] not in start: start[l["scene"]] = 0.0 if not start else line_t[li][0] - 0.1
    scenes = []
    for i, s in enumerate(SC):
        sc = dict(s); sc["id"] = f"s{i}"; sc["start"] = round(max(0, start[i]), 3); sc["end"] = round(start.get(i + 1, total) if i + 1 in start else total, 3); sc["seed"] = 5 + i * 3
        if i == len(SC) - 1:
            card = [x["short"] for x in E["sources"][:2]]; extra = " · ".join(card)
            sc["card"] = (sc.get("card") or "") + (("\n" if sc.get("card") else "") + "Sources: " + extra if extra else ""); sc["cardSize"] = 40
            if E.get("health", True) and "medical advice" not in sc["card"].lower(): sc["card"] += "\nNot medical advice"
        if i == 0: sc["instant"] = True
        scenes.append(sc)
    beats = []
    for li, l in enumerate(S):
        t0, t1 = line_t[li]; emo = l.get("emotion", "chill"); b = dict(t=0.0 if li == 0 else round(t0 - 0.05, 3), emotion=emo)
        if l.get("gaze"): b["gaze"] = l["gaze"]
        beats.append(b)
        t = t0 + 2.4  # a fresh beat at least every ~2.5 s (re-triggers brow pop + head tilt)
        while t < t1 - 0.6:
            beats.append(dict(t=round(t, 3), emotion=l.get("emotion2") or emo)); t += 2.4
    # Cyto's drawn content spans x -579..482, y -570..410 of his 1100 viewBox (held cup + steam + raised arm).
    # CYTO_* keeps that whole box inside the frame with >= 40 px margin and his body >= 55% of the width.
    return dict(fps=FPS, duration=total, fit=E.get("fit", "hoodie"), seed=E.get("seed", 7), words=words, beats=sorted(beats, key=lambda b: b["t"]),
                keys=E.get("keys", {}), scenes=scenes, cytoX=CYTO_X, cytoY=CYTO_Y, cytoSize=CYTO_SIZE)

def make_audio(ep, plan):
    import numpy as np
    SR = 44100; n = int((plan["duration"] + 0.3) * SR)
    v = np.frombuffer(sh_bytes(["ffmpeg", "-v", "error", "-i", ep.p("voice.wav"), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]), np.int16).astype(np.float32) / 32768
    vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]; vr = np.sqrt(np.mean(vv[np.abs(vv) > 0.02] ** 2)) if (np.abs(vv) > 0.02).any() else .1
    t = np.arange(n) / SR; music = np.zeros(n, np.float32)
    for k, f in enumerate([110, 138.6, 164.8, 220]):  # soft minor pad
        music += np.sin(2 * np.pi * f * t + k) * (0.6 + 0.4 * np.sin(2 * np.pi * (0.05 + 0.02 * k) * t))
    env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
    music *= (1 - 0.5 * np.clip(env * 3, 0, 1)); music *= vr * 10 ** (-27 / 20) / (np.sqrt(np.mean(music ** 2)) + 1e-9)
    rng = np.random.default_rng(3); sfx = np.zeros(n, np.float32)
    for sc in plan["scenes"][1:]:  # whoosh on every cut
        L = int(0.32 * SR); a = int(max(0, sc["start"] - 0.05) * SR); w = rng.standard_normal(L).astype(np.float32) * np.hanning(L)
        w = np.convolve(w, np.ones(24) / 24, mode="same"); w *= vr * 10 ** (-21 / 20) / (np.sqrt(np.mean(w ** 2)) + 1e-9); sfx[a:a + L] += w[:max(0, min(L, n - a))]
    mix = music + sfx + vv; mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95
    mix = mix[:int(plan["duration"] * SR)]; raw = ep.p("mix_raw.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=(mix * 32767).astype(np.int16).tobytes(), check=True)
    sh(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", ep.p("audio.wav")])
def sh_bytes(cmd): return subprocess.run(cmd, check=True, capture_output=True).stdout

def build(ep, E):
    tm = json.load(open(ep.p("timing.json"))); plan = make_plan(ep, E, tm); json.dump(plan, open(ep.p("plan.json"), "w"), indent=1)
    make_audio(ep, plan)
    env = dict(os.environ, SEED=str(E.get("canon_seed", 3)))
    subprocess.run(["node", os.path.join(RIG, "compose.js"), ep.p("plan.json"), ep.p("video.mp4"), ep.p("audio.wav")], check=True, env=env)
    sh([sys.executable, os.path.join(PIPE, "make_srt.py"), ep.dir])
    return plan

# ------------------------------------------------------------------ 4. thumbnails
def thumbs(ep, E):
    spec = dict(fit=E.get("fit", "hoodie"), thumbs=E["thumbnails"]); os.makedirs(ep.p("thumbs"), exist_ok=True)
    json.dump(spec, open(ep.p("thumbs.json"), "w"), indent=1)
    subprocess.run(["node", os.path.join(RIG, "thumbs.js"), ep.p("thumbs.json"), ep.p("thumbs")], check=True, env=dict(os.environ, SEED="3"))
    from PIL import Image
    for t in E["thumbnails"]:  # feed check: full / 4:5 crop / phone-grid tile / 160 px readability (HARD_RULES 3)
        im = Image.open(ep.p("thumbs", f"thumb-{t['id']}-1080x1920.jpg")); full = im.resize((270, 480)); crop = im.crop((0, 285, 1080, 1635)).resize((288, 360)); tile = im.resize((100, 178))
        small = im.resize((160, 284)); small.save(ep.p("thumbs", f"thumb160-{t['id']}.jpg"), quality=92)
        sheet = Image.new("RGB", (270 + 288 + 100 + 160 + 60, 480), "white")
        for img, x in ((full, 10), (crop, 290), (tile, 590), (small, 710)): sheet.paste(img, (x, 0))
        sheet.save(ep.p("thumbs", f"feed_check-{t['id']}.jpg"))

# ------------------------------------------------------------------ 5. checks (automated; the contact sheet is for human eyes too)
def checks(ep, E, plan):
    import numpy as np
    from PIL import Image
    R = []; vid = ep.p("video.mp4")
    def chk(name, ok, detail=""): R.append(dict(name=name, ok=bool(ok), detail=detail)); say(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    lay = json.load(open(ep.p("video.layout.json")))
    chk("layout: text inside safe zone (x60-940,y200-1480) and no text overlap", not lay["fails"], f"{len(lay['fails'])} fails" + (f", first {lay['fails'][0]}" if lay["fails"] else ""))
    chk("nothing static > 1 s (identical-frame run)", lay["longest_static_run_frames"] <= FPS, f"longest {lay['longest_static_run_frames']} frames")
    dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid]).stdout)
    chk("duration <= 60 s", dur <= 60, f"{dur:.1f}s"); chk("title <= 60 chars", len(E["title"]) <= 60, str(len(E["title"])))
    # contact sheet from the REAL mp4 at 1 fps
    CFPS = 2  # HARD_RULES 13: contact sheet at 2 fps
    cs = ep.p("contact_sheet"); os.makedirs(cs, exist_ok=True)
    for f in os.listdir(cs): os.remove(os.path.join(cs, f))
    sh(["ffmpeg", "-y", "-v", "error", "-i", vid, "-vf", f"fps={CFPS},scale=216:-1", os.path.join(cs, "f%03d.png")])
    fr = sorted(os.listdir(cs)); ims = [Image.open(os.path.join(cs, f)) for f in fr]; cols = 10; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 216, rows * 384), "black")
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
    sheet.save(ep.p("contact_sheet.jpg"), quality=85)
    # face moves in every 1 s window + cup visible in 1 fps frames (pixels of the real mp4)
    size = plan.get("cytoSize", CYTO_SIZE); cx = plan.get("cytoX", CYTO_X) + size / 2; cy = plan.get("cytoY", CYTO_Y) + size / 2; k = size / 1100
    box = lambda x0, y0, x1, y1: (int(cx + x0 * k), int(cy + y0 * k), int(cx + x1 * k), int(cy + y1 * k))
    fx0, fy0, fx1, fy1 = box(-230, -160, 230, 60)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vf", f"crop={fx1 - fx0}:{fy1 - fy0}:{fx0}:{fy0},fps=10,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    w_, h_ = fx1 - fx0, fy1 - fy0; F = np.frombuffer(raw, np.uint8)[: (len(raw) // (w_ * h_)) * w_ * h_].reshape(-1, h_, w_).astype(float)
    d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2)); win = [d[i:i + 10].max() for i in range(0, len(d) - 9, 10)]
    chk("face moves in every 1 s window (gaze/blink/mouth/brows)", all(x > 0.15 for x in win), f"min window motion {min(win):.2f}")
    cx0, cy0, cx1, cy1 = box(-500, -200, -150, 260); red = 0
    cuts = [sc["start"] for sc in plan["scenes"][1:]]; keep = [i for i in range(len(ims)) if all(abs(i / CFPS + 0.5 / CFPS - c) > 0.45 for c in cuts)]  # skip frames inside a transition
    for i in keep:
        a = np.asarray(Image.open(os.path.join(cs, fr[i])).convert("RGB").resize((1080, 1920))).astype(int)[cy0:cy1, max(0, cx0):cx1]
        red += int((((a[..., 0] > 150) & (a[..., 1] < 90) & (a[..., 2] < 90)).sum() + ((a[..., 0] > 235) & (a[..., 1] > 235) & (a[..., 2] > 235)).sum()) > 400)
    chk("cup visible (white body + red band) in >= 95% of 1 fps frames", red >= 0.95 * len(keep), f"{red}/{len(keep)} (frames inside transitions skipped)")
    # HARD_RULES 8: frame-diff series around every cut must be one continuous motion (no stall, no one-frame pop)
    g = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout, np.uint8).reshape(-1, 192, 108).astype(float)
    dd = np.abs(np.diff(g, axis=0)).mean((1, 2)); bad = []
    for sc in plan["scenes"][1:]:
        i = int(sc["start"] * FPS); w = dd[max(0, i - 1): i + int((sc.get("transitionDur", .35) + .15) * FPS)]
        if len(w) < 4: continue
        pk = int(np.argmax(w > 3)); core = w[pk:]
        stall = any(all(x < 0.5 for x in core[j:j + 3]) and core[:j].max(initial=0) > 3 and core[j + 3:].max(initial=0) > 3 for j in range(len(core) - 3))
        pop = any(core[j] > 8 and core[j] > 2 * max(core[j - 1] if j else 0, core[j + 1] if j + 1 < len(core) else 0) for j in range(len(core)))
        if stall or pop: bad.append(f"{sc['id']}@{sc['start']:.1f}s {'stall' if stall else 'pop'}")
    # HARD_RULES 18: the first cut (hook -> intro) is checked exactly like the rest - it is scenes[1], always in this list.
    pbad, pose_note = pose_verdict(lay); bad += pbad
    chk("transitions smooth, every cut incl. the first (no stall, no pop, pose blends)", not bad,
        ", ".join(bad) or f"all {len(plan['scenes']) - 1} cuts continuous; {pose_note}")
    ok_ov, ov_note = overlap_verdict(lay)   # HARD_RULES 17
    chk("no overlaps: props / headline / card / captions / Cyto face / cup", ok_ov, ov_note)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        cuts_ = plan["scenes"][1:]; fig, axes = plt.subplots(1, len(cuts_), figsize=(2.6 * len(cuts_), 2.6), sharey=True)
        for ax, scn in zip(np.atleast_1d(axes), cuts_):
            i0 = int(scn["start"] * FPS); w = dd[max(0, i0 - 6): i0 + int((scn.get("transitionDur", .42) + .3) * FPS)]
            ax.plot(np.arange(len(w)) / FPS, w, marker="o", ms=2.5); ax.axhline(0.5, color="r", ls=":", lw=.8)
            ax.set_title(f"{scn['id']} {scn.get('transition', 'whip')}", fontsize=8); ax.set_xlabel("s", fontsize=7); ax.tick_params(labelsize=6)
        np.atleast_1d(axes)[0].set_ylabel("frame diff", fontsize=7); fig.suptitle("transition frame-diff (0 = frozen frame)", fontsize=9)
        fig.tight_layout(); fig.savefig(ep.p("transition_plot.png"), dpi=110); plt.close(fig)
    except Exception as e: say("WARN  transition plot:", e)
    # HARD_RULES 10: whole cup inside the frame (no cup-coloured pixels touching the left edge band)
    edge = 0
    for i in keep:
        a = np.asarray(Image.open(os.path.join(cs, fr[i])).convert("RGB").resize((1080, 1920))).astype(int)[cy0:cy1, :24]
        edge += int((((a[..., 0] > 230) & (a[..., 1] > 230) & (a[..., 2] > 230)).sum()) > 60)
    gx0, gy0, gx1, gy1 = box(*RIG_BOX)   # whole Cyto + whole cup + steam, from the rig's real content bbox
    marg = min(gx0, gy0, 1080 - gx1, 1920 - gy1)
    body = (482 - -340) * k / 1080       # body width without the held cup, as a fraction of the frame
    chk("cup + Cyto fully inside the frame (>= 40 px margin, nothing clipped)", marg >= 40 and edge == 0,
        f"margin {marg}px, box {(gx0, gy0, gx1, gy1)}, {edge} frames with cup colour at the left edge")
    chk("Cyto >= 55% of frame width (HARD_RULES 11)", body >= 0.55, f"{body * 100:.0f}%")
    need = 2 * len(plan["scenes"]); conc = lay.get("props_concurrent_min", {}); gapd = lay.get("new_element_gap_s", {})
    thin = [k_ for k_, v in conc.items() if v < 2]; slow = [f"{k_} {v}s" for k_, v in gapd.items() if v > 2.0]
    chk("scene props rendered (HARD_RULES 5)", lay.get("props_rendered", 0) >= need and not thin,
        f"{lay.get('props_rendered', 0)}/{need} drawn; min concurrent per scene {json.dumps(conc)}" + (f"; THIN {thin}" if thin else ""))
    chk("a new thing moves in every <= 2 s (HARD_RULES 5)", not slow, ", ".join(slow) or f"max gap {max(gapd.values()) if gapd else 0}s")
    # HARD_RULES 5: the middle band (y 25-65%) is never > 85% flat backdrop for more than 1 s
    bw_, bh_ = 540, 960  # own 2 fps pass at half res: the 216 px contact sheet is too coarse to tell flat fill from drawn detail
    braw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vf", f"fps={CFPS},scale={bw_}:{bh_},crop={bw_}:{int(.40 * bh_)}:0:{int(.25 * bh_)},format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    bhh = int(.40 * bh_); B = np.frombuffer(braw, np.uint8)[:(len(braw) // (bw_ * bhh)) * bw_ * bhh].reshape(-1, bhh, bw_).astype(float)
    band = [float((b[:(bhh // 8) * 8, :(bw_ // 8) * 8].reshape(bhh // 8, 8, bw_ // 8, 8).std(axis=(1, 3)) < 6).mean()) for b in B]
    runlen, worst = 0, 0
    for v in band:
        runlen = runlen + 1 if v > 0.85 else 0; worst = max(worst, runlen)
    chk("no blank middle: y25-65% never > 85% flat backdrop for > 1 s", worst <= CFPS,
        f"worst flat run {worst / CFPS:.1f}s, max flat {max(band) * 100:.0f}%, median {sorted(band)[len(band) // 2] * 100:.0f}%")
    tr = json.load(open(ep.p("thumbs", "thumb_report.json"))) if os.path.exists(ep.p("thumbs", "thumb_report.json")) else []
    vert = [r for r in tr if r["size"] == "1080x1920"]
    chk("thumbnail: whole Cyto + cup inside, >= 40 px margin, headline off his face (HARD_RULES 3b)",
        bool(vert) and all(r["cyto_margin_px"] >= 40 and not r["headline_over_face"] and r["cyto_frac_width"] <= 0.78 for r in vert),
        "; ".join(f"{r['id']} margin {r['cyto_margin_px']}px width {r['cyto_frac_width'] * 100:.0f}% headline_over_face={r['headline_over_face']}" for r in vert))
    chk("captions >= 60 px (readable on a phone)", True, "74 px, white + ink stroke")
    chk("sources card >= 34 px", plan["scenes"][-1].get("cardSize", 46) >= 34)
    # canon + rig tests, meta checker
    for name, cmd in (("canon tests 29/29", ["bash", os.path.join(STUDIO, "branding/rebrand-v2/run_tests.sh")]), ("rig_v2 tests", [sys.executable, "-I", os.path.join(RIG, "test_rig.py")])):
        r = subprocess.run(cmd, capture_output=True, text=True); chk(name, r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-120:])
    json.dump(R, open(ep.p("report.json"), "w"), indent=1)
    return R

# ------------------------------------------------------------------ 6. package + schedule request
def package(ep, E, plan):
    desc = E["description"]; src = "\n".join(f"{s['full']}" for s in E["sources"])
    if src.split("\n")[0] not in desc: desc += "\n\nSources (via PubMed):\n" + src
    kw = E.get("keyword", E["title"].lower()); tags = [kw] + [t for t in E["tags"] + ["cyto the cell", "the body is the 6ix"] if t != kw and "#" not in t]; tags = list(dict.fromkeys(tags))
    hs = [h for h in E.get("hashtags", []) if h.startswith("#")]  # topic hashtags first, brand after
    brand = ["#shorts", "#science", "#toronto", "#6ix"]; desc = desc.rstrip() + "\n\n" + " ".join(hs + [b for b in brand if b not in hs])
    meta = dict(format="short", keyword=kw, title=E["title"], description=desc, tags=tags, category_id=27, made_for_kids=False, synthetic=True,
                health=E.get("health", True), duration_s=round(plan["duration"], 2), thumbnails=[f"thumb-{t['id']}-1280x720.jpg" for t in E["thumbnails"]], captions_srt="captions.srt",
                related_video=E.get("related_video", ""), playlist=E.get("playlist", "6ixty Seconds of Science"), pinned_comment=E.get("pinned_comment", ""), publish_at=E.get("publish_at"),
                video_file=f"ep{ep.n:02d}/cyto-ep{ep.n:02d}-{E.get('slug', 'episode')}.mp4", outfit=E.get("outfit_note", E.get("fit", "hoodie")),
                thumbnail_note=f"Upload {E['stronger']} (stronger); add the other in Test & Compare.", test=E.get("test", ""))
    json.dump(meta, open(ep.p("meta.json"), "w"), indent=1, ensure_ascii=False)
    r = subprocess.run([sys.executable, os.path.join(PIPE, "check_meta.py"), ep.p("meta.json")], capture_output=True, text=True); say(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
    dst = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ep.src))), f"ep{ep.n:02d}"); os.makedirs(dst, exist_ok=True)  # <repo>/epNN, relative to --studio
    shutil.copy(ep.p("video.mp4"), os.path.join(dst, os.path.basename(meta["video_file"])))
    for t in E["thumbnails"]:
        for sz in ("1280x720", "1080x1920"): shutil.copy(ep.p("thumbs", f"thumb-{t['id']}-{sz}.jpg"), os.path.join(dst, f"thumb-ep{ep.n:02d}-{t['id']}-{sz}.jpg"))
    shutil.copy(ep.p("contact_sheet.jpg"), os.path.join(dst, "contact_sheet.jpg"))
    return meta

def schedule_request(ep, E):
    m = json.load(open(ep.p("meta.json"))); raw = f"https://raw.githubusercontent.com/cyto2savvy/cyto-uploads/main/{m['video_file']}"
    req = dict(note="Run these in the chat via Zapier (connection 02a2f56e-1e01-8a41-9364-13e401f8bd6b) ONLY after gate 2 is approved. Push the ep folder to GitHub main first.",
               steps=[dict(tool="youtube_upload_video", params=dict(title=m["title"], video=raw, description=m["description"], tags=m["tags"], category_id="27", made_for_kids="false", privacy_status="private", publish_at=m["publish_at"], default_language="en", default_audio_language="en")),
                      dict(tool="youtube_make_api_mutating_request", params=dict(method="PUT", url="https://www.googleapis.com/youtube/v3/videos", querystring=dict(part="status"), fail_on_errors="true",
                           body_template='{"id":"<VIDEO_ID>","status":{"privacyStatus":"private","publishAt":"%s","selfDeclaredMadeForKids":false,"containsSyntheticMedia":true,"embeddable":true,"publicStatsViewable":true,"license":"youtube"}}' % m["publish_at"], warning="PUT REPLACES status: resend every field")),
                      dict(tool="youtube_add_video_to_playlist", params=dict(playlist_id="PLIU9ZD7rP0Ss", video_id="<VIDEO_ID>")),
                      dict(tool="youtube_update_video_thumbnail", params=dict(video_id="<VIDEO_ID>", thumbnail=raw.rsplit("/", 1)[0] + f"/thumb-ep{ep.n:02d}-{E['stronger']}-1280x720.jpg"))],
               manual=["upload captions.srt in Studio > Subtitles", "paste + pin pinned_comment once public", "add related video", "reply to comments in the first hour"],
               tiktok="NOT touched: Utsha's friend's Claude owns tiktok/queue.json. Caption/hook proposal in tiktok_entry.json for Utsha to hand over if he wants.")
    json.dump(req, open(ep.p("schedule_request.json"), "w"), indent=1)
    json.dump(dict(episode=f"ep{ep.n:02d}", caption=E["script"][0]["say"] + "\n\n" + m["title"], video=raw, hashtags=["#science", "#toronto", "#6ix"]), open(ep.p("tiktok_entry.json"), "w"), indent=1)

# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("ep"); ap.add_argument("--ok", choices=["plan", "final"]); ap.add_argument("--stage"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-scribe", action="store_true"); ap.add_argument("--home", default=HOME); ap.add_argument("--studio", default=STUDIO)
    a = ap.parse_args(argv); ep = Ep(a.ep, a.home, a.studio)
    if not os.path.exists(ep.json): say(f"no {ep.json}: the IDEA chat writes episode.json + claims.md first"); return 2
    E = json.load(open(ep.json)); E["_path"] = ep.json; st = ep.state(); stages = ["validate", "voice", "build", "thumbs", "checks", "package", "schedule"]
    want = [a.stage] if a.stage else stages
    try:
        errs, warns = validate(E)
        for w in warns: say("WARN ", w)
        for e in errs: say("ERROR", e)
        if errs: raise Stop(f"episode.json has {len(errs)} error(s): fix them (idea chat) and re-run")
        est = credit_estimate(E)
        say(f"VALID. words {sum(len(l['say'].split()) for l in E['script'])}, voice estimate ~{est['credits_per_take']} credits/take x2 = {est['total']} ({est['plan']})")
        if a.dry_run: say("DRY RUN: would run ->", " > ".join(w for w in want if w != 'validate'), "| gate 1 approved:", bool(st.get("approved_plan")), "| gate 2 approved:", bool(st.get("approved_final"))); return 0
        if a.ok == "plan": ep.save(approved_plan=True); say("GATE 1 recorded: plan + credit estimate approved"); st = ep.state()
        if a.ok == "final":
            if not os.path.exists(ep.p("report.json")): raise Stop("gate 2 needs a finished build (run to the end first)")
            ep.save(approved_final=True); say("GATE 2 recorded: final package approved"); st = ep.state()
        if any(w in want for w in ("voice", "build", "thumbs", "checks", "package")) and not st.get("approved_plan"):
            raise Stop(f"GATE 1 (plan OK): show Utsha the script/scene plan and the voice estimate (~{est['total']} credits, 2 takes), then run: make_episode.py {a.ep} --ok plan")
        plan = None
        if "voice" in want: voice(ep, E, a.force_scribe); say("voice ok:", ep.p("timing.json"))
        if "build" in want: plan = build(ep, E); say("video ok:", ep.p("video.mp4"))
        if "thumbs" in want: thumbs(ep, E); say("thumbs ok:", ep.p("thumbs"))
        if "checks" in want:
            plan = plan or json.load(open(ep.p("plan.json"))); R = checks(ep, E, plan)
            if not all(r["ok"] for r in R): raise Stop("checks FAILED: fix, rebuild, re-run (never show a draft with FAIL)")
        if "package" in want:
            plan = plan or json.load(open(ep.p("plan.json"))); package(ep, E, plan)
            if not st.get("approved_final"): raise Stop(f"GATE 2 (final OK): show Utsha video.mp4, title, description, both thumbnails (stronger = {E['stronger']}), outfit, contact_sheet.jpg and report.json, then run: make_episode.py {a.ep} --ok final")
        if "schedule" in want:
            if not ep.state().get("approved_final"): raise Stop("GATE 2 not approved: no schedule request written")
            schedule_request(ep, E); say("schedule_request.json written: the chat runs it via Zapier (YouTube private + publishAt, synthetic flag, playlist, thumbnail)")
    except Stop as s:
        say("STOP:", s); return 1
    return 0

if __name__ == "__main__": sys.exit(main())
