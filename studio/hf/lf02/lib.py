"""LF02 scene framework (1920x1080). One Scene = one HyperFrames composition rendered on its own, then concatenated.
Times inside a scene are LOCAL (0 = scene start); timing.json is global."""
import json, os, re, sys, subprocess
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/hf/lf02")
import cytohf as C, cyto3 as R, chars as K

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
        """Cyto at body-centre (x,y), scale s. expr: cyto3 kinds; x_expr: chars.EXPR kinds (smug/deadpan/...)."""
        rig = R.rig3_html(outfit, cup, face_extra=face_extra, toque_extra=toque_extra)
        if phone:   # phone in the right hand (inside #armR so it follows points/waves)
            hx, hy = R.HAND_R
            ph = (f'<g transform="translate({hx - 20} {hy - 150})"><g id="cyPhone"><rect x="0" y="0" width="92" height="160" rx="16" fill="#1b1f2a" stroke="#0c1622" stroke-width="7"/>'
                  f'<rect id="cyScreen" x="9" y="14" width="74" height="126" rx="6" fill="#8ce2d6"/>'
                  f'<rect id="cyNotif" x="14" y="24" width="64" height="30" rx="7" fill="#fff"/><circle cx="26" cy="39" r="7" fill="#3fc1b0"/><rect x="38" y="33" width="34" height="5" fill="#9aa"/><rect x="38" y="43" width="24" height="5" fill="#9aa"/></g></g>')
            rig = rig.replace('<circle id="handR"', ph + '<circle id="handR"')
        self.add(f'<div id="cytoLayer" style="position:absolute;inset:0;z-index:{z}">{rig}</div>')
        ws = self.words_of("CYTO")
        mouth = R.viseme_track(DIALOGUE, ws, t_off=self.t0, t_end=self.t1) if ws else []
        if not mouth or mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
        mouth = close_listener(mouth, ws, "CYTO", self.name, self.t0, {k: "rest" for k in OPEN_CY})
        self.cast["CYTO"] = dict(x=x, y=y - 40 * s / .6, kind="cyto", idp="cy", s=s)
        # speaker cue: brows pop on the first word of each of his lines (+ anticipation inhale 0.12 s before)
        for n, (a, b) in self.lines_in("CYTO"):
            if a > .05:
                self.j(f'tl.to(["#browL","#browR"],{{y:-9,duration:.08,ease:"power2.out"}},{a - .12:.3f});tl.to(["#browL","#browR"],{{y:0,duration:.18}},{a + .25:.3f});'
                       f'tl.fromTo("#cytoJump",{{y:0}},{{y:-10,duration:.1,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{a - .12:.3f});')
        if blinks is None:
            import random
            rnd = random.Random(len(self.name)); t = rnd.uniform(.5, 1.5); blinks = []
            while t < self.T - .3:
                blinks.append((round(t, 2), .1)); t += rnd.uniform(2.5, 4.5)
        mute = [(a, 0) for a, d in gest.get("sips", ())]
        for a, d in gest.get("sips", ()): self.sfx(a + .18, "sip", -3)
        self.j(f'tl.set("#cytoPos",{json.dumps(C.place(x, y, s))},0);')
        self.j(R.rig3_js(mouth, self.T, blinks=blinks, expr=expr, looks=looks, mute=mute, **gest))
        x_expr = list(x_expr) + self.auto_reactions("CYTO", list(x_expr) + [(a, d, "neutral") for a, d, _ in expr])
        if x_expr: self.j(K.cyto_expr_js(x_expr))

    def char(self, kind, idp, x, y, s, z=20, pose=None, expr=(), poses=(), looks=(), nods=(), pops=(), blinks=None,
             who=None, flip=False, extra_html="", shut_at=(), bob=True, **kw):
        """kind: neutro|mito|rhino. (x,y) = top-left of the char canvas, scale s."""
        if kind == "neutro": inner = K.neutro_html(idp, pose or "idle", trench=kw.get("trench", False)); rx, ry = 30, 34
        elif kind == "mito": inner = K.mito_html(idp, pose or "idle", gassed=kw.get("gassed", False)); rx, ry = 34, 40
        else: inner = K.rhino_html(idp, pose or "sneak"); rx, ry = 26, 28
        self.add(K.wrap(inner + extra_html, idp + "W", x, y, s, z=z, flip=flip))
        ws = self.words_of(who) if who else []
        expr = list(expr) + self.auto_reactions(who or kind, expr)
        nods = list(nods)
        mouths = K.mouth_track(DIALOGUE, ws, list(expr), self.t0, self.t1) if (ws or expr) else []
        mouths = close_listener(mouths, ws, who or kind, self.name, self.t0)
        fx, fy = {"neutro": (300, 330), "mito": (300, 300), "rhino": (200, 220)}[kind]
        if who: self.cast[who] = dict(x=x + fx * s, y=y + fy * s, kind=kind, idp=idp, s=s)
        for n, (a, b) in (self.lines_in(who) if who else []):
            if a > .05:
                self.j(f'tl.to(["#{idp}browL","#{idp}browR"],{{y:-10,duration:.08,ease:"power2.out"}},{a - .12:.3f});tl.to(["#{idp}browL","#{idp}browR"],{{y:0,duration:.18}},{a + .25:.3f});'
                       f'tl.fromTo("#{idp}",{{scaleY:1}},{{scaleY:1.04,duration:.1,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{a - .12:.3f});')
        self.j(K.act_js(idp, ry, rx, mouths=mouths, expr=expr, blinks=blinks, looks=looks, nods=nods, poses=poses,
                        pops=pops, T=self.T, seed=len(idp) + len(self.name), shut_at=shut_at, bob=bob))

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
            t0 = l["t0"] - self.t0; t1 = l["t1"] - self.t0
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
    def tr_in(self, kind="whip", d=.13, at=(960, 540)):
        kind = {"flash": "cut", "iris": "cut", "zoom": "whip", "static": "cut"}.get(kind, kind)
        self.tr_kind_in = kind
        if kind == "whip":
            self.j(f'tl.set("#shk",{{filter:"url(#mbf)"}},0);tl.fromTo("#mbg",{{attr:{{stdDeviation:"70 0"}}}},{{attr:{{stdDeviation:"0 0"}},duration:{d},ease:"power2.out",immediateRender:true}},0);'
                   f'tl.fromTo("#shk",{{x:150,scale:1.13}},{{x:0,scale:1,duration:{d},ease:"power3.out",immediateRender:true}},0);tl.set("#shk",{{filter:"none"}},{d + .01:.3f});')
        elif kind in ("cut", "match"):
            self.j(f'tl.fromTo("#shk",{{scale:{1.12 if kind == "match" else 1.05},transformOrigin:"{at[0]}px {at[1]}px"}},{{scale:1,duration:.22,ease:"power3.out",immediateRender:true}},0);')

    def tr_out(self, kind="whip", d=.13):
        kind = {"flash": "cut", "iris": "cut", "zoom": "whip", "static": "cut"}.get(kind, kind)
        t = self.T - d
        if kind == "whip":
            self.j(f'tl.set("#shk",{{filter:"url(#mbf)"}},{t:.3f});tl.fromTo("#mbg",{{attr:{{stdDeviation:"0 0"}}}},{{attr:{{stdDeviation:"70 0"}},duration:{d},ease:"power2.in",immediateRender:false}},{t:.3f});'
                   f'tl.to("#shk",{{x:-150,scale:1.13,duration:{d},ease:"power3.in"}},{t:.3f});')
            self.sfx(self.T - .06, "whoosh", -5)
        else:
            self.sfx(self.T - .01, "hit", -9)

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
        self.talk_camera(); self.listener_looks(); self.settxt_rule()
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
#shk,#cam,#tk,#drift{{position:absolute;inset:0;transform-origin:960px 540px}}
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
<div id="shk" class="clip" data-start="0" data-duration="{self.T}"><div id="drift"><div id="tk"><div id="cam">
{chr(10).join(self.html)}
</div></div></div></div>
{chr(10).join(self.top)}
</div>
<script>
const tl = gsap.timeline({{paused:true}});
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
