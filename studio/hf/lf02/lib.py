"""LF02 scene framework (1920x1080). One Scene = one HyperFrames composition rendered on its own, then concatenated.
Times inside a scene are LOCAL (0 = scene start); timing.json is global."""
import json, os, re, sys, subprocess, math
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/hf/lf02")
import cytohf as C, cyto3 as R, chars as K, rig2 as RG, motion as MO

W, H = 1920, 1080
P = "/home/claude/hf/lf02"
TM = json.load(open("/home/claude/lf02/timing.json"))
LINES = {l["n"]: l for l in TM["lines"]}
BEATS = TM["beats"]
DIALOGUE = "/home/claude/lf02/dialogue.wav"
SPK = {"CYTO": "#FAF4E8", "NEUTRO": "#b9d4ff", "MITO": "#ffc58a"}
SFX, MUSIC = [], []          # global (t, name, gain_db) / (t0, t1, kind) — collected from every scene build
IDS = {"CYTO": "cy", "NEUTRO": "nt", "MITO": "mt"}
JC = 0.15                    # J-cut: the picture cuts 0.15 s AFTER the next scene's first sound
OPEN_CH = {"grin": "smirk", "small": "mbp", "o": "mbp", "a": "rest", "e": "rest"}      # listener -> closed mouth
OPEN_CY = {"small", "a", "e", "o", "u", "fv"}
MOUTH_LOG = []               # (scene, who, t, shape) violations found + fixed (I12 check)


def cut_line(n): return round(LINES[n]["t0"] + JC, 3)
def cut_beat(name): return round(BEATS[name][0] + JC, 3)


def _talking(words, t, pad=.06):
    return any(w["t0"] - pad <= t <= w["t1"] + pad for w in words)


def close_listener(track, words, who, scene, t_off, mapping=None):
    """I12: only the current speaker may have an open mouth. Any open shape outside this character's own words -> closed."""
    mapping = mapping or OPEN_CH
    out = []
    for t, sh in track:
        if sh in mapping and not _talking(words, t + t_off):
            MOUTH_LOG.append((scene, who, round(t + t_off, 2), sh)); sh = mapping[sh]
        out.append([t, sh])
    return out


def gw(n, word, after=None):
    """GLOBAL time of the first word in line n starting with `word` (after= global time)."""
    for w in LINES[n]["words"]:
        if re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(re.sub(r"[^a-z0-9]", "", word.lower())) and (after is None or w["t0"] >= after):
            return w["t0"]
    raise KeyError((n, word))


# ---- CASE thread (v3): the one question + when each clue lands (global times)
CASE_FROM = round(gw(6, "plus") - .1, 3)          # the question is asked on screen ("TODAY'S CASE") then docks top-left
CLUE_T = {1: round(LINES[67]["t0"] + .25, 3), 2: round(gw(13, "cortisol") + .3, 3), 3: round(gw(41, "Case") + .25, 3)}
REVEAL_T = round(gw(47, "me") + .05, 3)


def act_js3(idp, ry, rx, mouths=(), expr=(), nods=(), pops=(), T=10.0, bob=True, shut_at=(), lid_n=-.35):
    """v3 face/body acting for the limb rigs (no pose swaps, no pupil x from expressions: pupils are procedural)."""
    J = [f'gsap.set("#{idp}Body",{{transformOrigin:"50% 100%"}});gsap.set(["#{idp}browL","#{idp}browR","#{idp}pupL","#{idp}pupR"],{{transformOrigin:"50% 50%"}});'
         f'gsap.set(["#{idp}lidL","#{idp}lidR"],{{y:{lid_n * ry:.1f}}});']
    for t, s in mouths:
        J.append("".join(f'tl.set("#{idp}m_{m}",{{opacity:{1 if m == s else 0}}},{t:.3f});' for m in K.MOUTHS))
    for a, d, k in sorted(expr):
        bl, rl, br, rr, lid, ps, pdx, _ = K.EXPR[k]
        if k == "neutral": lid = lid_n
        lid = min(lid, lid_n + .3) if k not in ("shocked", "hype", "worried") else lid
        J.append(f'tl.to("#{idp}browL",{{y:{bl},rotation:{rl},duration:.09,ease:"back.out(2)"}},{a:.3f});'
                 f'tl.to("#{idp}browR",{{y:{br},rotation:{rr},duration:.09,ease:"back.out(2)"}},{a:.3f});'
                 f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{lid * ry:.1f},duration:.09}},{a:.3f});'
                 f'tl.to(["#{idp}pupL","#{idp}pupR"],{{scale:{ps},duration:.09}},{a:.3f});')
        if k in ("shocked", "hype"):
            J.append(f'tl.fromTo("#{idp}",{{scaleX:1.12,scaleY:.86}},{{scaleX:1,scaleY:1,duration:.45,ease:"elastic.out(1.1,0.35)",immediateRender:false,svgOrigin:"300 690"}},{a:.3f});')
        e = a + d
        J.append(f'tl.to(["#{idp}browL","#{idp}browR"],{{y:0,rotation:0,duration:.14}},{e:.3f});'
                 f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{lid_n * ry:.1f},duration:.14}},{e:.3f});tl.to(["#{idp}pupL","#{idp}pupR"],{{scale:1,duration:.14}},{e:.3f});')
    for t, d in shut_at:
        J.append(f'tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{ry * 1.1:.1f},duration:.12}},{t:.3f});tl.to(["#{idp}lidL","#{idp}lidR"],{{y:{lid_n * ry:.1f},duration:.12}},{t + d:.3f});')
    for t in nods:
        J.append(f'tl.to("#{idp}Body",{{y:9,duration:.11,ease:"power2.out",yoyo:true,repeat:1}},{t:.3f});')
    for t, s in pops:      # anticipation (crouch) -> stretch -> settle
        J.append(f'tl.to("#{idp}",{{scaleX:{1 + .08 * s:.3f},scaleY:{1 - .1 * s:.3f},duration:.1,ease:"power2.in",svgOrigin:"300 690"}},{t - .12:.3f});'
                 f'tl.to("#{idp}",{{scaleX:{1 - .07 * s:.3f},scaleY:{1 + .12 * s:.3f},y:{-30 * s:.0f},duration:.12,ease:"power3.out",svgOrigin:"300 690"}},{t - .02:.3f});'
                 f'tl.to("#{idp}",{{scaleX:1,scaleY:1,y:0,duration:.35,ease:"bounce.out",svgOrigin:"300 690"}},{t + .12:.3f});')
    if bob:
        J.append(f'tl.fromTo("#{idp}Body",{{scaleY:1}},{{scaleY:1.018,duration:.95,yoyo:true,repeat:{int(T / .95) + 1},ease:"sine.inOut",immediateRender:false}},0);')
    return "\n".join(J)


class Scene:
    def __init__(self, name, t0, t1, music=None, bg="#0c1622"):
        self.name, self.t0, self.t1 = name, round(t0, 3), round(t1, 3)
        self.T = round(t1 - t0, 3)
        self.html, self.css, self.js, self.top = [], [], [], []
        self.bg = bg
        self.cap_y = 930
        self.cap_lr = (160, 160)
        self.cast = {}            # who -> dict(x, y face point, kind, idp)
        self.talk_off = set()     # line numbers with no speaker camera (VO over photos/3D)
        self.talk_scale = 1.07
        self.ambience = None
        self.cutpoints = []
        self.camk = []            # (t, scale) of the speaker camera
        self.covers = []          # intervals where world/set text (.settxt) must be hidden (cards, cutaways, zooms)
        self.tr_kind_in = None
        self.rigs, self.mouth_tracks = [], {}
        self.est = 0.0             # establishing wide: no speaker camera before this local time
        self.case = True           # CASE tracker sticker (top-left) from the moment the question is asked
        self.mv_extra = []         # callables(Motion) for scene-specific procedural channels (ball, dunk, bob)
        if music: MUSIC.append((self.t0, self.t1, music))

    # ---- time helpers (LOCAL)
    def l(self, n):  return round(LINES[n]["t0"] - self.t0, 3), round(LINES[n]["t1"] - self.t0, 3)
    def w(self, n, word, after=None):
        return round(gw(n, word, None if after is None else after + self.t0) - self.t0, 3)
    def b(self, name): return round(BEATS[name][0] - self.t0, 3), round(BEATS[name][1] - self.t0, 3)
    def words_of(self, who):
        return [w for l in TM["lines"] if l["who"] == who for w in l["words"] if self.t0 - .1 <= w["t0"] < self.t1]

    def hide_txt(self, a, b): self.covers.append((a, b))

    def settxt_rule(self):
        """World text (wall plaque, signs, lever label...) is only shown in WIDE framing and when no card / cutaway covers it.
        Replaces every hand-placed .settxt tween with one computed visibility track (layout: set text is never cropped or covered)."""
        self.js = [re.sub(r'tl\.(?:to|set)\("\.settxt",\{[^}]*\},[^)]*\);', "", x) for x in self.js]
        ks = sorted(self.camk); fps = 30; prev = None; J = []
        for f in range(int(self.T * fps) + 1):
            t = f / fps
            sc = 1.0
            for a, v in ks:
                if a - .02 <= t: sc = v
            vis = sc <= 1.03 and not any(a - .1 <= t <= b + .05 for a, b in self.covers)
            if vis != prev:
                J.append(f'tl.set(".settxt",{{opacity:{1 if vis else 0}}},{max(0, t - (.12 if not vis else 0)):.3f});'); prev = vis
        self.j("".join(J))

    def lines_in(self, who):
        """(n, (local t0, local t1)) for this speaker's lines that start inside the scene."""
        return [(l["n"], (round(l["t0"] - self.t0, 3), round(l["t1"] - self.t0, 3))) for l in TM["lines"]
                if l["who"] == who and l["words"] and self.t0 - .05 <= l["t0"] < self.t1]

    def auto_reactions(self, who, expr):
        """I7/7: every other-speaker line > 1.5 s gets ONE listener reaction at its key word, unless one is hand-placed nearby."""
        out = []; kinds = ["sideeye", "smug", "deadpan", "worried"]
        for i, l in enumerate(x for x in TM["lines"] if x["who"] != who and x["words"] and self.t0 <= x["t0"] < self.t1 - .5):
            if l["t1"] - l["t0"] < 1.5: continue
            ws = l["words"]; kw = max(ws[len(ws) // 3:], key=lambda w: len(re.sub(r"[^a-z]", "", w["w"].lower())))
            t = round(kw["t0"] - self.t0, 3)
            if any(abs(a - t) < 1.0 or a <= t <= a + d for a, d, _ in list(expr) + out): continue
            out.append((t, min(1.1, l["t1"] - kw["t0"]), kinds[(l["n"] + len(who)) % len(kinds)]))
        return out

    def sfx(self, t, name, gain=0):
        SFX.append((round(self.t0 + t, 3), name, gain))

    def add(self, h): self.html.append(h)
    def over(self, h): self.top.append(h)        # above the camera (UI: captions, pop-ups, cards)
    def j(self, s): self.js.append(s)
    def style(self, s): self.css.append(s)

    # ---- cast
    def cyto(self, x, y, s, outfit="outfit_pufferhoodie", cup="cup_red2", expr=(), x_expr=(), looks=(), blinks=None, z=20,
             toque_extra="", face_extra="", phone=False, **gest):
        """Cyto at body-centre (x,y), scale s. v3: 2-segment IK arms (procedural, follow-through), procedural eyes/blinks.
        gest: points=[(t,d)] waves=[t] shrugs=[(t,d)] raises=[(t,d)] sips=[(t,d)] tilts=[(t,d,ang)]."""
        rig = RG.cyto_rig(outfit, cup, face_extra=face_extra, toque_extra=toque_extra, phone=phone)
        self.add(f'<div id="cytoLayer" style="position:absolute;inset:0;z-index:{z}">{rig}</div>')
        ws = self.words_of("CYTO")
        mouth = R.viseme_track(DIALOGUE, ws, t_off=self.t0, t_end=self.t1) if ws else []
        if not mouth or mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
        mouth = close_listener(mouth, ws, "CYTO", self.name, self.t0, {k: "rest" for k in OPEN_CY})
        sips = list(gest.get("sips", ()))
        for a_, d_ in sips: mouth = [m for m in mouth if not (a_ <= m[0] <= a_ + d_)]
        self.mouth_tracks["CYTO"] = mouth
        self.cast["CYTO"] = dict(x=x, y=y - 40 * s / .6, kind="cyto", idp="cy", s=s)
        for n, (a, b) in self.lines_in("CYTO"):
            if a > .05:
                self.j(f'tl.to(["#browL","#browR"],{{y:-9,duration:.08,ease:"power2.out"}},{a - .12:.3f});tl.to(["#browL","#browR"],{{y:0,duration:.18}},{a + .25:.3f});'
                       f'tl.fromTo("#cytoJump",{{y:0}},{{y:-10,duration:.1,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{a - .12:.3f});')
        mute = [(a, 0) for a, d in sips]
        for a, d in sips: self.sfx(a + .18, "sip", -3)
        self.j(f'tl.set("#cytoPos",{json.dumps(C.place(x, y, s))},0);')
        self.j(R.rig3_js(mouth, self.T, blinks=(), expr=expr, looks=(), mute=mute, tilts=gest.get("tilts", ())))
        # ---- arms (rig coords). R = screen-right arm (phone / points), L = cup arm
        aR = MO.Arm("cyaR", RG.CY_SH["R"], RG.C_L1, RG.C_L2, RG.CY_REST["R"], 600)
        aL = MO.Arm("cyaL", RG.CY_SH["L"], RG.C_L1, RG.C_L2, RG.CY_REST["L"], 600)
        rR, rL = RG.CY_REST["R"], RG.CY_REST["L"]
        for t, d in gest.get("points", ()):
            aR.to(t - .1, (rR[0] - 10, rR[1] + 14), .1, "io", None, "relaxed")          # anticipation dip
            aR.to(t, (1112, 600), .24, "back", None, "point").to(t + d, rR, .3, "io", None, "relaxed")
        for t in gest.get("waves", ()):
            aR.to(t - .08, (rR[0], rR[1] + 12), .08, "io").to(t, (1030, 470), .22, "back", 185, "relaxed").to(t + .75, rR, .3, "io", None, "relaxed")
            aR.wig.append((t + .2, t + .75, 34, .28))
        for t, d in gest.get("shrugs", ()):
            aR.to(t, (1060, 770), .2, "back", -125, "relaxed").to(t + d, rR, .28, "io", None)
            aL.to(t, (228, 800), .2, "back", 0, None).to(t + d, rL, .28, "io", 0)
        for t, d in gest.get("raises", ()):
            aL.to(t, (214, 640), .22, "back", 0).to(t + d, rL, .28, "io", 0)
        for t, d in sips:          # cup to the mouth on an arc, tips, settles; eyes close contentedly
            aL.to(t, (440, 830), .24, "out", 52).to(t + .3, (448, 822), max(.1, d - .55), "io", 62).to(t + d - .24, rL, .28, "io", 0)
            self.j(f'tl.set(["#eyeL","#eyeR"],{{opacity:0}},{t + .2:.3f});tl.set(["#ecL","#ecR"],{{opacity:1}},{t + .2:.3f});tl.set(["#eyeL","#eyeR"],{{opacity:1}},{t + d - .2:.3f});tl.set(["#ecL","#ecR"],{{opacity:0}},{t + d - .2:.3f});')
        aL.hand_rest_abs = None   # cup arm: keep the cup upright unless a key sets it
        self.rigs.append(dict(who="CYTO", kind="cyto", arms=[aR, aL], cup_arm=aL, looks=list(looks), blinks=blinks,
                              exprs=[(a, d, k) for a, d, k in expr] + [(a, d, k) for a, d, k in x_expr]))
        x_expr = list(x_expr) + self.auto_reactions("CYTO", list(x_expr) + [(a, d, "neutral") for a, d, _ in expr])
        if x_expr: self.j(K.cyto_expr_js(x_expr))

    def char(self, kind, idp, x, y, s, z=20, pose=None, expr=(), poses=(), looks=(), nods=(), pops=(), blinks=None,
             who=None, flip=False, extra_html="", shut_at=(), bob=True, walks=(), ball=None, **kw):
        """kind: neutro|mito|rhino. (x,y) = top-left of the char canvas, scale s.
        v3 (neutro, mito): limb rig - poses are hand TARGETS reached on arcs (IK, follow-through), procedural eyes.
        walks: [(t0, t1, dx)] walk cycle (legs + arm swing + bob) while the wrapper travels dx px.
        ball (mito): list of (t0, t1, mode) mode in held|dribble|hidden."""
        if kind == "neutro": inner = RG.neutro_html(idp, trench=kw.get("trench", False)); rx, ry = 30, 34
        elif kind == "mito": inner = RG.mito_html(idp, gassed=kw.get("gassed", False)); rx, ry = 30, 36
        else: inner = K.rhino_html(idp, pose or "sneak"); rx, ry = 26, 28
        if kind == "mito" and ball is not None:
            inner = inner.replace("</g></g></svg>", f'</g></g><g id="{idp}bshW" opacity="0"><ellipse id="{idp}bsh" cx="0" cy="0" rx="50" ry="13" fill="#000"/></g><g id="{idp}bW" opacity="0">{RG.ball_svg(idp + "ball", 48)}</g></svg>')
        self.add(K.wrap(inner + extra_html, idp + "W", x, y, s, z=z, flip=flip))
        ws = self.words_of(who) if who else []
        expr = list(expr) + self.auto_reactions(who or kind, expr)
        mouths = K.mouth_track(DIALOGUE, ws, list(expr), self.t0, self.t1) if (ws or expr) else []
        mouths = close_listener(mouths, ws, who or kind, self.name, self.t0)
        if who: self.mouth_tracks[who] = mouths
        fx, fy = {"neutro": (300, 316), "mito": (300, 286), "rhino": (200, 220)}[kind]
        if who: self.cast[who] = dict(x=x + fx * s, y=y + fy * s, kind=kind, idp=idp, s=s)
        for n, (a, b) in (self.lines_in(who) if who else []):
            if a > .05:
                self.j(f'tl.to(["#{idp}browL","#{idp}browR"],{{y:-10,duration:.08,ease:"power2.out"}},{a - .12:.3f});tl.to(["#{idp}browL","#{idp}browR"],{{y:0,duration:.18}},{a + .25:.3f});'
                       f'tl.fromTo("#{idp}",{{scaleY:1}},{{scaleY:1.04,duration:.1,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false,svgOrigin:"300 690"}},{a - .12:.3f});')
        if kind == "rhino":
            self.j(K.act_js(idp, ry, rx, mouths=mouths, expr=expr, blinks=blinks, looks=looks, nods=nods, poses=poses,
                            pops=pops, T=self.T, seed=len(idp) + len(self.name), shut_at=shut_at, bob=bob))
            return
        lid_n = -.05 if kind == "mito" else -.35
        self.j(act_js3(idp, ry, rx, mouths=mouths, expr=expr, nods=nods, pops=pops, T=self.T, shut_at=shut_at, bob=bob, lid_n=lid_n))
        PO = RG.NPOSE if kind == "neutro" else RG.MPOSE
        SH = RG.N_SH if kind == "neutro" else RG.M_SH
        L1, L2 = (RG.N_L1, RG.N_L2) if kind == "neutro" else (RG.M_L1, RG.M_L2)
        p0 = pose or "idle"
        arms = {}
        for k in "LR":
            P, h, shp = PO[p0][k]
            a_ = MO.Arm(f"{idp}a{k}", SH[k], L1, L2, P, 300)
            a_.keys.append((0, P, 1 / 30, "lin", h, shp)); arms[k] = a_
        for t, nm in sorted(poses):
            for k in "LR":
                P, h, shp = PO[nm][k]
                arms[k].to(t, P, .26, "back", h, shp)
        props = []
        if kind == "neutro":
            seq = [(0, p0)] + sorted(poses)
            for pid, want in (("pad", "notepad"), ("pen", "notepad"), ("tkt", "ticket")):
                props.append((f"{idp}{pid}", [(t + (.12 if nm == want else 0), 1 if nm == want else 0) for t, nm in seq]))
            for t, nm in seq:
                if nm == "notepad": arms["R"].wig.append((t + .3, t + 1.6, 7, .32))      # pen scribbles
        self.rigs.append(dict(who=who or kind, kind=kind, idp=idp, arms=[arms["L"], arms["R"]], looks=list(looks), blinks=blinks,
                              exprs=list(expr), walks=list(walks), props=props, ball=ball, flip=flip, s=s, x=x, y=y, rx=rx, ry=ry))

    # ---- camera
    def punch(self, t, sc=1.14, d=.45, ox=960, oy=540):
        self.covers.append((t - .02, t + d))
        self.j(f'tl.set("#cam",{{transformOrigin:"{ox}px {oy}px"}},{t - .01:.3f});tl.fromTo("#cam",{{scale:{sc}}},{{scale:1,duration:{d},ease:"power3.out",immediateRender:false}},{t:.3f});')

    def snapzoom(self, t, sc, d, ox, oy, hold_out=.25):
        self.covers.append((t - .02, t + d + hold_out))
        self.j(f'tl.set("#cam",{{transformOrigin:"{ox}px {oy}px"}},{t - .01:.3f});tl.to("#cam",{{scale:{sc},duration:.12,ease:"power4.out"}},{t:.3f});'
               f'tl.to("#cam",{{scale:1,duration:{hold_out},ease:"power2.inOut"}},{t + d:.3f});')

    def shake(self, t, d=.5, amp=14):
        n = max(2, int(d / .05))
        self.j(f'tl.to("#shk",{{keyframes:[' + ",".join(f'{{x:{amp * ((-1) ** i) * (1 - i / n):.1f},y:{amp * .6 * ((-1) ** (i + 1)) * (1 - i / n):.1f},duration:.05}}' for i in range(n)) + f',{{x:0,y:0,duration:.05}}]}},{t:.3f});')

    def push(self, t0, t1, a=1.0, b=1.06, ox=960, oy=540):
        self.j(f'tl.set("#cam",{{transformOrigin:"{ox}px {oy}px"}},{t0:.3f});tl.fromTo("#cam",{{scale:{a}}},{{scale:{b},duration:{t1 - t0:.3f},ease:"sine.inOut",immediateRender:false}},{t0:.3f});')

    # ---- SPEAKER-DRIVEN CAMERA (#tk wrapper) + listener eyes/heads  (fix pass)
    def talk_lines(self):
        return [l for l in TM["lines"] if (self.t0 - .05 <= l["t0"] or l["t1"] > self.t0 + .5) and l["t0"] < self.t1 - .1 and l["n"] not in self.talk_off]

    def _frame(self, p, sc):
        px, py = p
        dx = max(W * (1 - sc), min(0, W / 2 - sc * px)); dy = max(H * (1 - sc), min(0, H * .46 - sc * py))
        return round(dx, 1), round(dy, 1)

    def talk_camera(self):
        if not self.talk_scale: return
        ls = [l for l in self.talk_lines() if l["who"] in self.cast]
        if not ls: return
        J = ['gsap.set("#tk",{transformOrigin:"0px 0px",x:0,y:0,scale:1});']
        # shot / reverse-shot: runs of >=3 quick alternating exchanges (each <= 2.6 s, gaps < .45 s)
        quick = set()
        for i in range(len(ls)):
            run = [ls[i]]
            for k in range(i + 1, len(ls)):
                if ls[k]["who"] != run[-1]["who"] and ls[k]["t0"] - run[-1]["t1"] < .45 and ls[k]["t1"] - ls[k]["t0"] < 2.6 and run[-1]["t1"] - run[-1]["t0"] < 2.6:
                    run.append(ls[k])
                else: break
            if len(run) >= 3 and len({r["who"] for r in run}) >= 2: quick.update(r["n"] for r in run)
        prev = None
        for i, l in enumerate(ls):
            c = self.cast[l["who"]]; p = (c["x"], c["y"])
            t0 = max(l["t0"] - self.t0, self.est + .15); t1 = l["t1"] - self.t0
            if t1 <= t0: continue
            if prev is not None and t0 - (prev["t1"] - self.t0) > 1.3:            # long action beat: back to the wide
                J.append(f'tl.to("#tk",{{x:0,y:0,scale:1,duration:.5,ease:"power2.inOut"}},{prev["t1"] - self.t0 + .15:.3f});'); self.camk.append((prev["t1"] - self.t0 + .65, 1.0))
                prev = None
            if l["n"] in quick:
                sc = 1.24; dx, dy = self._frame(p, sc)
                tc = max(0, t0 - .05)
                J.append(f'tl.set("#tk",{{x:{dx},y:{dy},scale:{sc}}},{tc:.3f});'); self.camk.append((tc, sc))
                self.cutpoints.append(tc)
            else:
                same = prev is not None and prev["who"] == l["who"]
                sc = self.talk_scale + (.02 if same else 0); dx, dy = self._frame(p, sc)
                ta = max(0, (min(t0, prev["t1"] - self.t0) if prev is not None else t0) - .15)
                J.append(f'tl.to("#tk",{{x:{dx},y:{dy},scale:{sc},duration:.25,ease:"power2.inOut"}},{ta:.3f});'); self.camk.append((ta, sc))
                # long monologue: a new framing at sentence ends every >= 2.8 s (push <-> medium), so no shot holds > ~4 s
                last, alt = t0, 0
                for w in l["words"][:-1]:
                    tw = w["t1"] - self.t0
                    if re.search(r"[.?!:…]$", w["w"]) and tw - last >= 2.8 and t1 - tw > 1.2:
                        alt ^= 1; sc2 = getattr(self, 'alt_scale', 1.16) if alt else self.talk_scale; dx2, dy2 = self._frame(p, sc2)
                        J.append(f'tl.to("#tk",{{x:{dx2},y:{dy2},scale:{sc2},duration:.3,ease:"power2.inOut"}},{tw + .02:.3f});'); self.camk.append((tw + .02, sc2))
                        last = tw
            prev = l
        self.j("\n".join(J))

    def listener_looks(self):
        J = []
        for l in self.talk_lines():
            if l["who"] not in self.cast or not l["words"]: continue
            sx = self.cast[l["who"]]["x"]; t0 = max(0, l["t0"] - self.t0 - .12); t1 = l["t1"] - self.t0
            for who, c in self.cast.items():
                if who == l["who"]: continue
                d = 1 if sx > c["x"] else -1
                if c["kind"] == "cyto":
                    J.append(f'tl.to(["#pupL","#pupR"],{{x:{6 * d},y:-1,duration:.1,ease:"power2.out"}},{t0:.3f});tl.to(["#pupL","#pupR"],{{x:0,y:0,duration:.18}},{t1 + .1:.3f});')
                else:
                    i = c["idp"]; s_ = c["s"]
                    J.append(f'tl.to(["#{i}pupL","#{i}pupR"],{{x:{7 * d},duration:.1,ease:"power2.out"}},{t0:.3f});tl.to(["#{i}pupL","#{i}pupR"],{{x:0,duration:.18}},{t1 + .1:.3f});'
                             f'tl.to("#{i}W",{{rotation:{2.5 * d},transformOrigin:"{300 * s_:.0f}px {640 * s_:.0f}px",duration:.2,ease:"power2.out"}},{t0:.3f});'
                             f'tl.to("#{i}W",{{rotation:0,duration:.25}},{t1 + .1:.3f});')
        if J: self.j("\n".join(J))

    # ---- transitions: MOTIVATED cuts only (fix pass). No colour/fade frames: the picture is always the scene.
    #   whip  = 4-frame motion-blurred pan out on the last word + 4-frame blurred pan in (characters already in frame)
    #   cut   = hard cut on the sound (with a 6-frame punch-in on the new shot)
    #   match = hard cut, the next scene starts on the matching shape (scale pop from the same spot)
    # ---- transitions (v3 flow bible): straight CUT by default; the SUBWAY DOORS only on a change of place/chapter.
    #   doors: A closes over its last 0.32 s (holds shut 0.1 s), B holds shut 0.12 s then opens -> the cut frame is
    #   identical on both sides.  The doors carry the NEXT STOP sign, so the change of place is always announced.
    def _doors(self, label, t_close=None, t_open=None):
        i = len(self.top); sign = bool(label)
        half = lambda side: (f'<div class="door{side}" style="position:absolute;top:0;{"left" if side == "L" else "right"}:0;width:964px;height:1080px;'
                              f'background:linear-gradient(90deg,#8d969e,#d9dee2 35%,#b4bcc3 70%,#8d969e);border-{"right" if side == "L" else "left"}:14px solid #1b1f24">'
                              f'<div style="position:absolute;{"right" if side == "L" else "left"}:70px;top:250px;width:330px;height:420px;border-radius:26px;background:#22303c;border:12px solid #5d6770;box-shadow:inset 0 0 0 6px #10161c"></div>'
                              f'<div style="position:absolute;left:0;right:0;top:770px;height:26px;background:#C8102E"></div>'
                              f'<div class="drsign" style="position:absolute;{"right" if side == "L" else "left"}:0;top:84px;width:640px;height:96px;background:#111;border:6px solid #333;{"" if sign else "display:none;"}'
                              f'font:54px/84px InterBlack;color:#ffb020;text-align:{"right" if side == "L" else "left"};padding:0 26px;letter-spacing:.06em;white-space:nowrap">'
                              f'{"NEXT STOP:" if side == "L" else label}</div></div>')
        h = (f'<div id="dr{i}" class="clip" data-start="{(t_close - .02 if t_close is not None else 0):.3f}" data-duration="{(self.T - t_close + .02 if t_close is not None else t_open + .45):.3f}" style="position:absolute;inset:0;z-index:96;overflow:hidden">'
             f'<div id="dr{i}L" style="position:absolute;inset:0">{half("L")}</div><div id="dr{i}R" style="position:absolute;inset:0">{half("R")}</div></div>')
        self.over(h)
        if t_close is not None:
            self.j(f'tl.fromTo("#dr{i}L",{{x:-980}},{{x:0,duration:.22,ease:"power3.in",immediateRender:true}},{t_close:.3f});'
                   f'tl.fromTo("#dr{i}R",{{x:980}},{{x:0,duration:.22,ease:"power3.in",immediateRender:true}},{t_close:.3f});'
                   f'tl.fromTo("#dr{i}",{{x:0}},{{keyframes:[{{x:-6,duration:.04}},{{x:4,duration:.04}},{{x:0,duration:.04}}],immediateRender:false}},{t_close + .22:.3f});'
                   f'gsap.set("#dr{i} .drsign",{{opacity:0}});tl.to("#dr{i} .drsign",{{opacity:1,duration:.06}},{t_close + .2:.3f});'
                   f'tl.set(UIQ(),{{opacity:0}},{t_close + .22:.3f});')
            self.sfx(t_close - .18, "doorchime", -9); self.sfx(t_close + .02, "doorslide", -10)
        else:
            self.j(f'gsap.set(".settxt",{{opacity:0}});gsap.set(UIQ(),{{opacity:0}});tl.to(UIQ(),{{opacity:1,duration:.1}},{t_open + .06:.3f});tl.to("#dr{i} .drsign",{{opacity:0,duration:.05}},{t_open:.3f});'
                   f'tl.fromTo("#dr{i}L",{{x:0}},{{x:-980,duration:.3,ease:"power3.inOut",immediateRender:false}},{t_open:.3f});'
                   f'tl.fromTo("#dr{i}R",{{x:0}},{{x:980,duration:.3,ease:"power3.inOut",immediateRender:false}},{t_open:.3f});')
            self.sfx(t_open, "doorslide", -11)
        self.covers.append((t_close if t_close is not None else 0, self.T if t_close is not None else t_open + .3))

    def tr_in(self, kind="cut", d=.13, at=(960, 540), label=""):
        kind = {"whip": "cut", "flash": "cut", "iris": "cut", "zoom": "cut", "static": "cut"}.get(kind, kind)
        self.tr_kind_in = kind
        if kind == "doors":
            self._doors(label, t_open=.12)
        elif kind == "match":
            self.j(f'tl.fromTo("#shk",{{scale:1.08,transformOrigin:"{at[0]}px {at[1]}px"}},{{scale:1,duration:.22,ease:"power3.out",immediateRender:true}},0);')

    def tr_out(self, kind="cut", d=.13, label=""):
        kind = {"whip": "cut", "flash": "cut", "iris": "cut", "zoom": "cut", "static": "cut"}.get(kind, kind)
        if kind == "doors":
            self._doors(label, t_close=self.T - .34)

    # ---- flow devices -----------------------------------------------------------------------------------------
    def location(self, title, sub, t0=.5, d=2.4):
        """small location title card (top-right), lands after the doors open, holds while the establishing wide holds."""
        self.est = max(self.est, t0 + .55)
        self.over(f'<div id="loc" class="pop clip" data-start="{t0:.3f}" data-duration="{d:.3f}" style="right:36px;top:30px;z-index:79;padding:12px 26px 14px;border-radius:18px;'
                  f'background:#0c1622;border:5px solid #FFD166;box-shadow:0 10px 0 rgba(0,0,0,.35);text-align:right">'
                  f'<div style="font:46px/1.05 InterBlack;color:#FAF4E8;letter-spacing:.02em">{title}</div><div style="font:30px/1.2 InterBlack;color:#FFD166">{sub}</div></div>')
        self.j(f'tl.fromTo("#loc",{{x:60,opacity:0}},{{x:0,opacity:1,duration:.25,ease:"back.out(1.8)"}},{t0:.3f});tl.to("#loc",{{x:50,opacity:0,duration:.2,ease:"power2.in"}},{t0 + d - .2:.3f});')
        self.sfx(t0, "blip", -14)

    def recap(self, t0, n, text, d=3.6, y=150):
        """chapter recap card (<= 4 s): the clue that just landed, in plain words."""
        d = min(d, 4.0)
        self.over(f'<div id="rc{n}" class="pop clip" data-start="{t0:.3f}" data-duration="{d:.3f}" style="left:560px;width:800px;top:{y}px;z-index:77;padding:18px 26px 20px;border-radius:22px;'
                  f'background:#FAF4E8;border:7px solid #0c1622;box-shadow:0 14px 0 rgba(0,0,0,.35);text-align:center;transform:rotate(-1.5deg)">'
                  f'<div style="font:30px InterBlack;letter-spacing:.14em;color:#e63946">CLUE {n} FOUND ✓</div>'
                  f'<div style="font:46px/1.12 InterBlack;color:#0c1622;margin-top:6px">{text}</div></div>')
        self.j(f'tl.fromTo("#rc{n}",{{y:-40,scale:.6,opacity:0}},{{y:0,scale:1,opacity:1,duration:.3,ease:"back.out(2)"}},{t0:.3f});tl.to("#rc{n}",{{y:-30,opacity:0,duration:.22,ease:"power2.in"}},{t0 + d - .22:.3f});')
        self.covers.append((t0, t0 + d)); self.sfx(t0, "coin", -9)

    def case_tracker(self):
        g0 = CASE_FROM
        if self.t1 <= g0: return
        ta = max(0, g0 - self.t0, getattr(self, 'case_from', 0))
        chips = []
        for i in (1, 2, 3):
            lit = CLUE_T[i] <= self.t0 + .01
            chips.append(f'<div id="ck{i}" style="width:66px;height:38px;border-radius:12px;border:4px solid #0c1622;background:{"#FFD166" if lit else "#c9ccd2"};'
                         f'font:24px/30px InterBlack;color:#0c1622;text-align:center">{"✓" if lit else ""}{i}</div>')
        rv = REVEAL_T <= self.t0 + .01
        chips.append(f'<div id="cks" style="width:96px;height:38px;border-radius:12px;border:4px solid #0c1622;background:{"#e63946" if rv else "#0c1622"};'
                     f'font:22px/30px InterBlack;color:#FAF4E8;text-align:center">{"CYTO" if rv else "WHO?"}</div>')
        self.over(f'<div id="case" class="clip" data-start="{ta:.3f}" data-duration="{self.T - ta:.3f}" style="position:absolute;left:24px;top:20px;z-index:78;'
                  f'padding:8px 14px 10px;border-radius:16px;background:#FAF4E8;border:5px solid #0c1622;box-shadow:0 7px 0 rgba(0,0,0,.35);transform:rotate(-1.5deg)">'
                  f'<div style="font:18px InterBlack;letter-spacing:.12em;color:#e63946">CASE FILE · CLUES</div>'
                  f'<div style="font:24px/1.05 InterBlack;color:#0c1622;width:330px">WHO KEEPS PULLING THE ALARM?</div>'
                  f'<div style="display:flex;gap:7px;margin-top:7px">{"".join(chips)}</div></div>')
        if ta > 0:
            self.j(f'tl.fromTo("#case",{{scale:1.9,x:700,y:300,opacity:0}},{{scale:1,x:0,y:0,opacity:1,duration:.45,ease:"back.out(1.4)"}},{ta:.3f});')
        for i in (1, 2, 3):
            tc = CLUE_T[i] - self.t0
            if 0 < tc < self.T:
                self.j(f'tl.set("#ck{i}",{{background:"#FFD166",innerHTML:"✓{i}"}},{tc:.3f});tl.fromTo("#ck{i}",{{scale:1.8}},{{scale:1,duration:.35,ease:"back.out(3)",immediateRender:false}},{tc:.3f});')
                self.sfx(tc, "coin", -10)
        tr = REVEAL_T - self.t0
        if 0 < tr < self.T:
            self.j(f'tl.set("#cks",{{background:"#e63946",innerHTML:"CYTO"}},{tr:.3f});tl.fromTo("#cks",{{scale:2.2,rotation:-12}},{{scale:1,rotation:0,duration:.35,ease:"back.out(3)",immediateRender:false}},{tr:.3f});')
            self.sfx(tr, "stamp", -6)

    # ---- procedural motion: arms (IK), eyes (saccades, listener holds), blinks, walks, props, ball
    def motion(self):
        mv = MO.Motion(self.T); n = mv.n
        act = []
        for f in range(n):
            tg = self.t0 + f / MO.FPS; best = None
            for l in TM["lines"]:
                if l["words"] and l["t0"] - .12 <= tg <= l["t1"] + .35 and (best is None or l["t0"] > best["t0"]): best = l
            act.append(best["who"] if best else None)
        for r in self.rigs:
            who = r["who"]
            if who not in self.cast: continue
            cx = self.cast[who]["x"]; others = {k: v for k, v in self.cast.items() if k != who}
            tg = []; cur = (0.0, -.05)
            for f in range(n):
                a = act[f]
                if a == who and others:
                    o = min(others.values(), key=lambda v: abs(v["x"] - cx)); cur = ((1 if o["x"] > cx else -1) * .55, -.05)
                elif a == who: cur = (0.0, -.05)
                elif a in self.cast: cur = ((1 if self.cast[a]["x"] > cx else -1) * .85, -.05)
                tg.append(cur)
            for lk in r["looks"][:1]:                                  # <= 1 glance away per scene
                t, dx, dy = lk[:3]; dur = lk[3] if len(lk) > 3 else .9
                nx = lambda v: max(-1, min(1, v / 10 if abs(v) > 1 else v))
                for f in range(int(t * 30), min(n, int((t + dur) * 30))): tg[f] = (nx(dx), nx(dy))
            if r.get("flip"): tg = [(-x, y) for x, y in tg]
            shock = [(a, a + d) for a, d, k in r["exprs"] if k in ("shock", "shocked")]
            bl = r["blinks"] if r["blinks"] is not None else MO.auto_blinks(self.T, len(self.name) * 7 + len(who), shock)
            bl = [b if not isinstance(b, (tuple, list)) else b[0] for b in bl]
            if r["kind"] == "cyto":
                px, py, fx, fy, lid = MO.eye_track(n, 40, tg, bl, -70, 18, 54, inner_max=6)
                mv.tr("cypgL", px, py); mv.tr("cypgR", px, py); mv.tr("cyfT", fx, fy)
                mv.tr("cybkL", 0, lid); mv.tr("cybkR", 0, lid)
            else:
                i, rx, ry = r["idp"], r["rx"], r["ry"]
                px, py, fx, fy, lid = MO.eye_track(n, rx, tg, bl, -1.4 * ry, .3 * ry, 1.1 * ry)
                mv.tr(f"{i}pgL", px, py); mv.tr(f"{i}pgR", px, py); mv.tr(f"{i}fT", fx, fy)
                mv.tr(f"{i}bkL", 0, lid); mv.tr(f"{i}bkR", 0, lid)
            # walks: legs + arm swing + bob (wrapper travel is a GSAP tween)
            ov = {"L": [None] * n, "R": [None] * n}; legL = [0.0] * n; legR = [0.0] * n; bob = [0.0] * n
            for t0, t1, dx in r.get("walks", ()):
                per = .5
                self.j(f'tl.to("#{r["idp"]}W",{{x:"+={dx}",duration:{t1 - t0:.3f},ease:"sine.inOut"}},{t0:.3f});')
                for f in range(int(t0 * 30), min(n, int(t1 * 30) + 1)):
                    t = f / 30; e = min(1, (t - t0) / .15, (t1 - t) / .15)
                    ph = math.sin(2 * math.pi * (t - t0) / (2 * per))
                    legL[f] = 20 * ph * e; legR[f] = -20 * ph * e; bob[f] = -9 * abs(ph) * e
                    for k, sg in (("L", 1), ("R", -1)):
                        a_ = [x for x in r["arms"] if x.pid.endswith("a" + k)][0]
                        P = a_.rest; ov[k][f] = ((P[0] + (30 if k == "L" else -30) * ph * e, P[1] - 8 * abs(ph) * e), None, "relaxed")
            if r["kind"] in ("neutro", "mito"):
                i = r["idp"]
                hips = RG.N_SH if False else ({"L": (232, 596), "R": (368, 596)} if r["kind"] == "neutro" else RG.M_HIP)
                if any(legL) or r.get("ball"):
                    pass
                # ball / dribble (mito)
                res = {}
                if r["kind"] == "mito" and r.get("ball"):
                    res = self._mito_ball(mv, r, ov, legL, legR, bob)
                for a_ in r["arms"]:
                    k = a_.pid[-1]
                    res[k] = mv.arm(a_, ov[k] if any(x is not None for x in ov[k]) else None)
                if r["kind"] == "mito" and r.get("ball"): self._mito_ball_place(mv, r, res)
                mv.rot(f"{i}legL", hips["L"][0], hips["L"][1], legL); mv.rot(f"{i}legR", hips["R"][0], hips["R"][1], legR)
                mv.tr(f"{i}Mv", 0, bob)
                for pid, steps in r.get("props", ()):
                    vals = []; v = 0; si = 0; st = sorted(steps)
                    for f in range(n):
                        while si < len(st) and st[si][0] <= f / 30 + 1e-6: v = st[si][1]; si += 1
                        vals.append(v)
                    mv.op(pid, vals)
            else:
                for a_ in r["arms"]: mv.arm(a_)
        for fn in self.mv_extra: fn(mv)
        self.mv = mv
        self.j(mv.js())

    def _mito_ball(self, mv, r, ov, legL, legR, bob):
        """dribble: period 0.5 s, gravity arc (ease-in down, ease-out up), squash on contact, stretch in flight,
        hand meets the ball, feet step in sync, body bob. Returns {} (ball placed after the arm solve)."""
        n = mv.n; self._ball = [None] * n
        for t0, t1, mode in r["ball"]:
            if mode != "dribble": continue
            P = .5
            for f in range(int(t0 * 30), min(n, int(t1 * 30))):
                t = f / 30; ph = ((t - t0) % P) / P; e = min(1, (t - t0) / .2, (t1 - t) / .2)
                if ph < .16: hy = 452 + 44 * MO.ease(ph / .16, "in")
                elif ph < .5: hy = 496 - 44 * MO.ease((ph - .16) / .34, "out")
                elif ph > .86: hy = 452 + 8 * math.sin(math.pi * (ph - .86) / .14)
                else: hy = 452
                ov["R"][f] = ((524, hy), None, "grip" if ph < .16 or ph > .9 else "relaxed")
                step = int((t - t0) / P) % 2
                lift = math.sin(math.pi * min(1, ph / .5)) if ph < .5 else 0
                if step: legL[f] = 9 * lift * e
                else: legR[f] = -9 * lift * e
                bob[f] = 5 * math.sin(math.pi * ph) ** 2 * e
                self._ball[f] = ("dribble", ph, hy)
        return {}

    def _mito_ball_place(self, mv, r, res):
        n = mv.n; i = r["idp"]; RB = 48; floor = RG.M_FEET_Y - 2
        bx, by, sx, sy, rot, op, shx, shs, sho = [], [], [], [], [], [], [], [], []
        mode_at = lambda f: next((m for a, b, m in r["ball"] if a <= f / 30 < b), "hidden")
        spin = 0.0
        for f in range(n):
            m = mode_at(f); hand = res["R"]["hand"][f]
            habs = res["R"]["A"][f] + res["R"]["B"][f] + res["R"]["H"][f]
            d = MO.dvec(habs)
            x = hand[0] + d[0] * (30 * .6 + RB); y = hand[1] + d[1] * (30 * .6 + RB); a = b = 1.0
            if m == "dribble" and self._ball[f]:
                _, ph, hy = self._ball[f]
                top = hand[1] + 30 * 1.5 + RB; bot = floor - RB
                if ph < .16: y = top
                elif ph < .44: y = top + (bot - top) * MO.ease((ph - .16) / .28, "in")
                elif ph < .52: y = bot + RB * .2; a, b = 1.24, .74            # contact squash (bottom stays on the floor)
                else: y = bot - (bot - top) * MO.ease((ph - .52) / .48, "out")
                if .16 <= ph < .44 or ph >= .52:
                    sp = abs(math.cos(math.pi * ((ph - .16) / .28 if ph < .44 else (ph - .52) / .48) / 2)) if ph < .44 else 1 - (ph - .52) / .48
                    b = 1 + .12 * sp; a = 1 - .08 * sp
                x = hand[0] + 4; spin += 9
            bx.append(x); by.append(y); sx.append(a); sy.append(b); rot.append(spin)
            vis = 0 if m == "hidden" else 1; op.append(vis)
            h = max(0, floor - RB - y); k = max(0, 1 - h / 260)
            shx.append(x); shs.append(.45 + .55 * k); sho.append(vis * (.12 + .25 * k))
        mv.svgm(f"{i}ball", 0, 0, bx, by, 0, sx, sy)
        mv.rot(f"{i}ballseam", 0, 0, rot)
        mv.op(f"{i}bW", op)
        mv.svgm(f"{i}bsh", 0, 0, shx, floor + 2, 0, shs, shs); mv.op(f"{i}bshW", sho)

    # ---- captions: ONE fixed centred band (y 912-1040), dark pill, max 2 lines, words pop in and stay (fix pass I5)
    def captions(self, keys=None, y=None):
        keys = keys or {}
        words = []
        for l in TM["lines"]:
            for w in l["words"]:
                if self.t0 - .05 <= w["t0"] < self.t1 - .05:
                    words.append(dict(w=w["w"], t0=round(w["t0"] - self.t0, 3), t1=round(w["t1"] - self.t0, 3), who=l["who"], n=l["n"]))
        chunks, cur = [], []
        for i, w in enumerate(words):
            cur.append(i)
            nxt = words[i + 1] if i + 1 < len(words) else None
            long_ = sum(len(words[k]["w"]) + 1 for k in cur) > 26
            if len(cur) >= 5 or long_ or re.search(r"[.?!:…]$", w["w"]) or not nxt or nxt["n"] != w["n"] or nxt["t0"] - w["t1"] > .35:
                chunks.append(cur); cur = []
        h, js = [], []
        for ci, ch in enumerate(chunks):
            a = max(0, words[ch[0]]["t0"] - .06)
            last = words[ch[-1]]["t1"]
            nx = words[chunks[ci + 1][0]]["t0"] - .06 if ci + 1 < len(chunks) else self.T
            b = min(nx, last + .45, self.T)
            col = SPK[words[ch[0]]["who"]]
            sp = []
            for i in ch:
                raw = words[i]["w"]; key = re.sub(r"[^A-Za-z0-9]", "", raw).lower()
                kc = keys.get(key)
                st = f' style="color:{kc}"' if kc else ""
                sp.append(f'<span id="{self.name}w{i}" class="w{" key" if kc else ""}"{st}>{raw.upper()}</span>')
                js.append(f'tl.fromTo("#{self.name}w{i}",{{scale:1.07,y:-3}},{{scale:1,y:0,duration:.12,ease:"power2.out",immediateRender:false}},{max(a, words[i]["t0"] - .03):.3f});')
            h.append(f'<div id="{self.name}cap{ci}" class="capband clip" data-start="{a:.3f}" data-duration="{max(.05, b - a):.3f}"><span class="cap" style="color:{col}">{" ".join(sp)}</span></div>')
            js.append(f'tl.fromTo("#{self.name}cap{ci} .cap",{{scale:.9,opacity:0}},{{scale:1,opacity:1,duration:.1,ease:"back.out(2)"}},{a:.3f});')
        self.top.append("\n".join(h)); self.js.extend(js)

    # ---- page
    def build(self):
        self.talk_camera(); self.settxt_rule(); self.motion()
        if self.case: self.case_tracker()
        # continuous slow drift so no shot is ever locked off (I1 / rule 9)
        if getattr(self, "drift", True):
            self.j(f'tl.fromTo("#drift",{{scale:1,x:0}},{{scale:1.025,x:-12,duration:{self.T:.3f},ease:"sine.inOut",immediateRender:false}},0);')
        # J-cut lines start before the scene: a negative timeline position would shift the whole GSAP timeline -> clamp to 0
        self.js = [re.sub(r"\},\s*-\d+(?:\.\d+)?\)", "},0)", x) for x in self.js]
        d = f"{P}/{self.name}"; os.makedirs(d, exist_ok=True)
        if not os.path.exists(f"{d}/assets"): os.symlink(f"{P}/assets", f"{d}/assets")
        if not os.path.exists(f"{d}/node_modules"): os.symlink("/home/claude/hf/node_modules", f"{d}/node_modules")
        for f in ("hyperframes.json", "package.json"):
            if not os.path.exists(f"{d}/{f}"): subprocess.run(["cp", f"/home/claude/hf/ep07/{f}", f"{d}/{f}"])
        html = f"""<!doctype html>
<html lang="en" data-resolution="landscape"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script>{'<script src="assets/three.min.js"></script><script src="assets/three_lf02.js"></script>' if any('C3' in x for x in self.js) else ''}
<style>{C.FONT_CSS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:{self.bg}}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:InterXB;background:{self.bg}}}
#shk,#cam,#tk,#drift,#bob{{position:absolute;inset:0;transform-origin:960px 540px}}
.fill{{position:absolute;inset:0}}
.capband{{position:absolute;left:180px;right:180px;top:{self.cap_y}px;text-align:center;z-index:80}}
.cap{{display:inline-block;max-width:1560px;padding:8px 26px 12px;border-radius:22px;background:rgba(12,22,34,.78);font:56px/1.14 InterBlack;-webkit-text-stroke:2px #0c1622;paint-order:stroke fill}}
.w{{display:inline-block}} .key{{font-size:62px}}
.static{{background-image:repeating-radial-gradient(circle at 17% 32%,#fff 0,#000 2px,#888 3px,#222 5px);background-size:120px 90px}}
.pop{{position:absolute;z-index:70}}
{R.rig3_css()}
{''.join(self.css)}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{self.T}" data-width="1920" data-height="1080">
<svg width="0" height="0" style="position:absolute"><filter id="mbf" x="-5%" y="0" width="110%" height="100%"><feGaussianBlur id="mbg" stdDeviation="0 0"/></filter></svg>
<div id="shk" class="clip" data-start="0" data-duration="{self.T}"><div id="drift"><div id="bob"><div id="tk"><div id="cam">
{chr(10).join(self.html)}
</div></div></div></div></div>
{chr(10).join(self.top)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
const UIQ = () => Array.from(document.querySelectorAll('#case,#sb,#dksb')).filter(Boolean);
const T = {self.T};
{chr(10).join(self.js)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
        open(f"{d}/index.html", "w").write(html)
        json.dump(dict(name=self.name, t0=self.t0, t1=self.t1), open(f"{d}/meta.json", "w"))
        return d


def save_audio_events():
    """Merge this run's SFX/MUSIC into /home/claude/lf02/events.json keyed by scene time range."""
    f = "/home/claude/lf02/events.json"
    ev = json.load(open(f)) if os.path.exists(f) else {"sfx": [], "music": []}
    return ev


def _three(self, var, factory, t0, t1, opts="{}", z=1, w=1920, h=1080, extra=""):
    self.add(f'<canvas id="cv{var}" width="{w}" height="{h}" class="clip" data-start="{max(0, t0 - .05):.3f}" data-duration="{t1 - max(0, t0 - .05):.3f}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:{z};{extra}"></canvas>')
    self.j(f'const {var}=C3D2.{factory}(document.getElementById("cv{var}"),{opts});const P{var}={{t:0}};{var}.render(0);'
           f'tl.fromTo(P{var},{{t:0}},{{t:{t1 - t0:.3f},duration:{t1 - t0:.3f},ease:"none",onUpdate:()=>{var}.render(P{var}.t)}},{t0:.3f});')


def _parallax(self, ids_depths, t0, t1, dx=-80, dy=0, ease="sine.inOut"):
    """Multi-plane camera move: each layer travels dx*depth."""
    for i, d in ids_depths:
        self.j(f'tl.fromTo("#{i}",{{x:0,y:0}},{{x:{dx * d:.1f},y:{dy * d:.1f},duration:{t1 - t0:.3f},ease:"{ease}",immediateRender:false}},{t0:.3f});')


def _popup(self, id_, t0, t1, title, sub="", col="#FFD166", x=960, y=300, w=980, kind="game", z=70):
    """Video-game style pop-up banner (pixel border) or stamp. Centre (x,y). Fix pass: brief pop-in, never > 3.2 s."""
    t1 = min(t1, t0 + 3.2)
    if kind == "game":
        h = (f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x - w // 2}px;top:{y}px;width:{w}px;z-index:{z};'
             f'padding:22px 30px;background:#151a24;border:8px solid {col};box-shadow:0 0 0 8px #0c1622,0 16px 0 rgba(0,0,0,.4);text-align:center">'
             f'<div style="font:30px InterBlack;letter-spacing:.18em;color:{col}">{title}</div>'
             + (f'<div style="font:52px/1.1 InterBlack;color:#FAF4E8;margin-top:8px">{sub}</div>' if sub else "") + '</div>')
    else:   # stamp
        h = (f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x - w // 2}px;top:{y}px;width:{w}px;z-index:{z};text-align:center;'
             f'font:84px InterBlack;color:{col};-webkit-text-stroke:4px #0c1622;paint-order:stroke fill;transform:rotate(-4deg)">{title}</div>')
    self.over(h)
    self.covers.append((t0, t1))
    self.j(f'tl.fromTo("#{id_}",{{scale:2.2,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:{-4 if kind != "game" else 0},duration:.28,ease:"back.out(2.2)"}},{t0:.3f});'
           f'tl.to("#{id_}",{{scale:.6,opacity:0,duration:.18,ease:"power2.in"}},{t1 - .2:.3f});')


Scene.three3d = _three
Scene.parallax = _parallax
Scene.popup = _popup


# ---------------------------------------------------------------- fix-pass helpers
RIM = "filter:drop-shadow(0 0 1.5px rgba(255,248,230,.95)) drop-shadow(0 0 1px rgba(255,248,230,.9)) drop-shadow(0 22px 16px rgba(0,0,0,.45))"


def _photo(self, id_, name, t0, t1, kb=(1.0, 1.12), z=1, ox="50%", oy="50%", over=False, extra=""):
    """Real Toronto photo plate (graded in photos.py) with a slow Ken Burns push. Plates are 2112x1188 (10% oversize)."""
    h = (f'<div id="{id_}" class="clip" data-start="{max(0, t0):.3f}" data-duration="{t1 - max(0, t0):.3f}" style="position:absolute;inset:0;z-index:{z};overflow:hidden;{extra}">'
         f'<img id="{id_}i" src="assets/ph_{name}.jpg" style="position:absolute;left:-96px;top:-54px;width:2112px;height:1188px;transform-origin:{ox} {oy}"/></div>')
    (self.over if over else self.add)(h)
    self.j(f'tl.fromTo("#{id_}i",{{scale:{kb[0]}}},{{scale:{kb[1]},duration:{t1 - t0:.3f},ease:"none",immediateRender:true}},{max(0, t0):.3f});')


def _panel(self, id_, t0, t1, title, sub="", col="#FFD166", x=60, y=60, w=760, z=72):
    """Text over a photo / 3D shot always sits on its own dark panel (clean zone)."""
    t1 = min(t1, t0 + 3.2)
    if self.case and x < 420 and y < 175 and self.t0 + t1 > CASE_FROM: y = 178          # v3: top-left corner belongs to the CASE sticker
    self.over(f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};padding:20px 28px 22px;'
              f'border-radius:20px;background:rgba(12,22,34,.86);border-left:12px solid {col};box-shadow:0 12px 0 rgba(0,0,0,.3)">'
              f'<div style="font:30px InterBlack;letter-spacing:.12em;color:{col}">{title}</div>'
              + (f'<div style="font:{50 if len(sub) <= 26 else 42}px/1.08 InterBlack;color:#FAF4E8;margin-top:6px;white-space:nowrap">{sub}</div>' if sub else "") + '</div>')
    self.j(f'tl.fromTo("#{id_}",{{x:-50,opacity:0}},{{x:0,opacity:1,duration:.22,ease:"back.out(1.8)"}},{t0:.3f});tl.to("#{id_}",{{x:-40,opacity:0,duration:.16,ease:"power2.in"}},{t1 - .16:.3f});')


def _prop_in(self, sel, t, kind="drop", origin="50% 0%", sfx="clunk", amp=1.0, svg=None):
    """F: props ACT. anticipation -> action -> settle (squash & stretch) + a sound. kind: drop (spring in from above,
    overshoot + 3 wobbles) | pop (scale up from 0) | slide (from the right)."""
    o = f'svgOrigin:"{svg}"' if svg else f'transformOrigin:"{origin}"'
    if kind == "drop":
        self.j(f'gsap.set("{sel}",{{{o}}});tl.fromTo("{sel}",{{y:-420*{amp},scaleY:1.25,scaleX:.85}},{{y:0,scaleY:1,scaleX:1,duration:.55,ease:"elastic.out(1.05,0.32)",immediateRender:true}},{t:.3f});'
               f'tl.fromTo("{sel}",{{rotation:0}},{{keyframes:[{{rotation:9,duration:.09}},{{rotation:-7,duration:.11}},{{rotation:5,duration:.11}},{{rotation:-3,duration:.1}},{{rotation:2,duration:.09}},{{rotation:0,duration:.08}}],immediateRender:false}},{t + .18:.3f});')
    elif kind == "pop":
        self.j(f'gsap.set("{sel}",{{{o}}});tl.fromTo("{sel}",{{scale:0}},{{keyframes:[{{scale:1.18,duration:.16,ease:"power3.out"}},{{scale:.94,duration:.09}},{{scale:1,duration:.12}}],immediateRender:true}},{t:.3f});')
    elif kind == "slide":
        self.j(f'gsap.set("{sel}",{{{o}}});tl.fromTo("{sel}",{{x:700,skewX:-12}},{{x:0,skewX:0,duration:.4,ease:"back.out(1.6)",immediateRender:true}},{t:.3f});')
    if sfx: self.sfx(t + (.18 if kind == "drop" else .05), sfx, -8)


Scene.photo = _photo
Scene.panel = _panel
Scene.prop_in = _prop_in
