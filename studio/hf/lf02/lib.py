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
        self.cap_y = 936
        self.cap_lr = (150, 150)
        if music: MUSIC.append((self.t0, self.t1, music))

    # ---- time helpers (LOCAL)
    def l(self, n):  return round(LINES[n]["t0"] - self.t0, 3), round(LINES[n]["t1"] - self.t0, 3)
    def w(self, n, word, after=None):
        return round(gw(n, word, None if after is None else after + self.t0) - self.t0, 3)
    def b(self, name): return round(BEATS[name][0] - self.t0, 3), round(BEATS[name][1] - self.t0, 3)
    def words_of(self, who):
        return [w for l in TM["lines"] if l["who"] == who for w in l["words"] if self.t0 - .1 <= w["t0"] < self.t1]

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
        if blinks is None:
            import random
            rnd = random.Random(len(self.name)); t = rnd.uniform(.5, 1.5); blinks = []
            while t < self.T - .3:
                blinks.append((round(t, 2), .1)); t += rnd.uniform(2.5, 4.5)
        mute = [(a, 0) for a, d in gest.get("sips", ())]
        for a, d in gest.get("sips", ()): self.sfx(a + .18, "sip", -3)
        self.j(f'tl.set("#cytoPos",{json.dumps(C.place(x, y, s))},0);')
        self.j(R.rig3_js(mouth, self.T, blinks=blinks, expr=expr, looks=looks, mute=mute, **gest))
        if x_expr: self.j(K.cyto_expr_js(x_expr))

    def char(self, kind, idp, x, y, s, z=20, pose=None, expr=(), poses=(), looks=(), nods=(), pops=(), blinks=None,
             who=None, flip=False, extra_html="", shut_at=(), bob=True, **kw):
        """kind: neutro|mito|rhino. (x,y) = top-left of the char canvas, scale s."""
        if kind == "neutro": inner = K.neutro_html(idp, pose or "idle", trench=kw.get("trench", False)); rx, ry = 30, 34
        elif kind == "mito": inner = K.mito_html(idp, pose or "idle", gassed=kw.get("gassed", False)); rx, ry = 34, 40
        else: inner = K.rhino_html(idp, pose or "sneak"); rx, ry = 26, 28
        self.add(K.wrap(inner + extra_html, idp + "W", x, y, s, z=z, flip=flip))
        ws = self.words_of(who) if who else []
        mouths = K.mouth_track(DIALOGUE, ws, list(expr), self.t0, self.t1) if (ws or expr) else []
        self.j(K.act_js(idp, ry, rx, mouths=mouths, expr=expr, blinks=blinks, looks=looks, nods=nods, poses=poses,
                        pops=pops, T=self.T, seed=len(idp) + len(self.name), shut_at=shut_at, bob=bob))

    # ---- camera
    def punch(self, t, sc=1.14, d=.45, ox=960, oy=540):
        self.j(f'tl.set("#cam",{{transformOrigin:"{ox}px {oy}px"}},{t - .01:.3f});tl.fromTo("#cam",{{scale:{sc}}},{{scale:1,duration:{d},ease:"power3.out",immediateRender:false}},{t:.3f});')

    def snapzoom(self, t, sc, d, ox, oy, hold_out=.25):
        self.j(f'tl.set("#cam",{{transformOrigin:"{ox}px {oy}px"}},{t - .01:.3f});tl.to("#cam",{{scale:{sc},duration:.12,ease:"power4.out"}},{t:.3f});'
               f'tl.to("#cam",{{scale:1,duration:{hold_out},ease:"power2.inOut"}},{t + d:.3f});')

    def shake(self, t, d=.5, amp=14):
        n = max(2, int(d / .05))
        self.j(f'tl.to("#shk",{{keyframes:[' + ",".join(f'{{x:{amp * ((-1) ** i) * (1 - i / n):.1f},y:{amp * .6 * ((-1) ** (i + 1)) * (1 - i / n):.1f},duration:.05}}' for i in range(n)) + f',{{x:0,y:0,duration:.05}}]}},{t:.3f});')

    def push(self, t0, t1, a=1.0, b=1.06, ox=960, oy=540):
        self.j(f'tl.set("#cam",{{transformOrigin:"{ox}px {oy}px"}},{t0:.3f});tl.fromTo("#cam",{{scale:{a}}},{{scale:{b},duration:{t1 - t0:.3f},ease:"sine.inOut",immediateRender:false}},{t0:.3f});')

    # ---- transitions (each cut = out-half at the end of scene A + matching in-half at the start of scene B)
    def tr_in(self, kind="whip", d=.3):
        self._tr("in", kind, 0, d)

    def tr_out(self, kind="whip", d=.3):
        self._tr("out", kind, self.T - d, d)

    def _tr(self, io, kind, t, d):
        i = f"tr{io}"
        if io == "out": self.j(f'tl.to(".settxt",{{opacity:0,duration:.05}},{t:.3f});')
        else: self.j(f'tl.set(".settxt",{{opacity:0}},0);tl.to(".settxt",{{opacity:1,duration:.1}},{d:.3f});')
        if kind == "whip":
            self.over(f'<div id="{i}" style="position:absolute;top:-40px;left:0;width:2600px;height:1160px;z-index:95;background:linear-gradient(90deg,rgba(255,209,102,0),#FFD166 18%,#FF7A59 50%,#3fc1b0 82%,rgba(63,193,176,0));transform:skewX(-14deg)"></div>')
            a, b = (-2700, 2100) if io == "out" else (-300, 2300)
            if io == "out": self.j(f'tl.fromTo("#{i}",{{x:-2700}},{{x:-320,duration:{d},ease:"power3.in"}},{t:.3f});tl.to("#cam",{{x:-140,duration:{d},ease:"power3.in"}},{t:.3f});')
            else: self.j(f'tl.fromTo("#{i}",{{x:-320}},{{x:2300,duration:{d},ease:"power3.out"}},0);tl.fromTo("#cam",{{x:140}},{{x:0,duration:{d + .1},ease:"power3.out",immediateRender:false}},0);')
        elif kind == "iris":
            self.over(f'<div id="{i}" style="position:absolute;left:960px;top:540px;width:10px;height:10px;z-index:95;border-radius:50%;box-shadow:0 0 0 2400px #0c1622"></div>')
            if io == "out": self.j(f'tl.set("#{i}",{{opacity:1}},0);tl.fromTo("#{i}",{{scale:260}},{{scale:0,duration:{d},ease:"power2.in",immediateRender:false}},{t:.3f});tl.set("#{i}",{{scale:260}},0);')
            else: self.j(f'tl.fromTo("#{i}",{{scale:0}},{{scale:260,duration:{d},ease:"power2.out"}},0);')
        elif kind == "flash":
            self.over(f'<div id="{i}" style="position:absolute;inset:0;z-index:95;background:#fffbe8;opacity:0"></div>')
            if io == "out": self.j(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:{d},ease:"power2.in",immediateRender:false}},{t:.3f});')
            else: self.j(f'tl.fromTo("#{i}",{{opacity:1}},{{opacity:0,duration:{d},ease:"power2.out"}},0);')
        elif kind == "static":
            self.over(f'<div id="{i}" class="static" style="position:absolute;inset:0;z-index:95;opacity:0"></div>')
            if io == "out": self.j(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:{d},immediateRender:false}},{t:.3f});')
            else: self.j(f'tl.fromTo("#{i}",{{opacity:1}},{{opacity:0,duration:{d}}},0);')
            self.j(f'tl.fromTo("#{i}",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"37px 91px",duration:.06,repeat:{int(self.T / .06)},ease:"steps(1)",immediateRender:false}},0);')
        elif kind == "zoom":
            self.over(f'<div id="{i}" style="position:absolute;inset:0;z-index:95;background:#FAF4E8;opacity:0"></div>')
            if io == "out": self.j(f'tl.to("#cam",{{scale:1.6,duration:{d},ease:"power3.in",transformOrigin:"960px 540px"}},{t:.3f});tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:{d},ease:"power3.in",immediateRender:false}},{t:.3f});')
            else: self.j(f'tl.fromTo("#cam",{{scale:.7}},{{scale:1,duration:{d + .15},ease:"power3.out",transformOrigin:"960px 540px",immediateRender:false}},0);tl.fromTo("#{i}",{{opacity:1}},{{opacity:0,duration:{d}}},0);')

    # ---- captions
    def captions(self, keys=None, y=None):
        keys = keys or {}
        y = y or self.cap_y
        words = []
        for l in TM["lines"]:
            for w in l["words"]:
                if self.t0 - .05 <= w["t0"] < self.t1 - .1:
                    words.append(dict(w=w["w"], t0=round(w["t0"] - self.t0, 3), t1=round(w["t1"] - self.t0, 3), who=l["who"], n=l["n"]))
        chunks, cur = [], []
        for i, w in enumerate(words):
            cur.append(i)
            nxt = words[i + 1] if i + 1 < len(words) else None
            long_ = sum(len(words[k]["w"]) for k in cur) > 30
            if len(cur) >= 6 or long_ or re.search(r"[.?!:…]$", w["w"]) or not nxt or nxt["n"] != w["n"] or nxt["t0"] - w["t1"] > .3:
                chunks.append(cur); cur = []
        h, js = [], []
        for ci, ch in enumerate(chunks):
            a = words[ch[0]]["t0"] - .05
            last = words[ch[-1]]["t1"]
            nx = words[chunks[ci + 1][0]]["t0"] - .05 if ci + 1 < len(chunks) else self.T
            b = min(nx, last + .9)
            col = SPK[words[ch[0]]["who"]]
            sp = []
            for i in ch:
                raw = words[i]["w"]; key = re.sub(r"[^A-Za-z0-9]", "", raw).lower()
                kc = keys.get(key)
                st = f' style="color:{kc}"' if kc else ""
                sp.append(f'<span id="{self.name}w{i}" class="w{" key" if kc else ""}"{st}>{raw.upper()}</span>')
                js.append(f'tl.fromTo("#{self.name}w{i}",{{opacity:0,y:14,scale:{1.4 if kc else 1.15}}},{{opacity:1,y:0,scale:1,duration:{.2 if kc else .12},ease:"back.out(2.4)"}},{words[i]["t0"] - .03:.3f});')
            h.append(f'<div id="{self.name}cap{ci}" class="cap clip" data-start="{max(0, a):.3f}" data-duration="{b - max(0, a):.3f}" style="top:{y}px;left:{self.cap_lr[0]}px;right:{self.cap_lr[1]}px;color:{col}">{" ".join(sp)}</div>')
        self.top.append("\n".join(h)); self.js.extend(js)

    # ---- page
    def build(self):
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
#shk,#cam{{position:absolute;inset:0;transform-origin:960px 540px}}
.fill{{position:absolute;inset:0}}
.cap{{position:absolute;left:150px;right:150px;text-align:center;font:58px/1.12 InterBlack;-webkit-text-stroke:3px #0c1622;paint-order:stroke fill;text-shadow:0 5px 0 rgba(0,0,0,.4);z-index:80}}
.w{{display:inline-block;opacity:0}} .key{{font-size:70px}}
.static{{background-image:repeating-radial-gradient(circle at 17% 32%,#fff 0,#000 2px,#888 3px,#222 5px);background-size:120px 90px}}
.pop{{position:absolute;z-index:70}}
{R.rig3_css()}
{''.join(self.css)}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{self.T}" data-width="1920" data-height="1080">
<div id="shk" class="clip" data-start="0" data-duration="{self.T}"><div id="cam">
{chr(10).join(self.html)}
</div></div>
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
    """Video-game style pop-up banner (pixel border) or stamp. Centre (x,y)."""
    if kind == "game":
        h = (f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x - w // 2}px;top:{y}px;width:{w}px;z-index:{z};'
             f'padding:22px 30px;background:#151a24;border:8px solid {col};box-shadow:0 0 0 8px #0c1622,0 16px 0 rgba(0,0,0,.4);text-align:center">'
             f'<div style="font:30px InterBlack;letter-spacing:.18em;color:{col}">{title}</div>'
             + (f'<div style="font:52px/1.1 InterBlack;color:#FAF4E8;margin-top:8px">{sub}</div>' if sub else "") + '</div>')
    else:   # stamp
        h = (f'<div id="{id_}" class="pop clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" style="left:{x - w // 2}px;top:{y}px;width:{w}px;z-index:{z};text-align:center;'
             f'font:84px InterBlack;color:{col};-webkit-text-stroke:4px #0c1622;paint-order:stroke fill;transform:rotate(-4deg)">{title}</div>')
    self.over(h)
    self.j(f'tl.to(".settxt",{{opacity:0,duration:.1}},{t0:.3f});tl.to(".settxt",{{opacity:1,duration:.15}},{t1:.3f});')
    self.j(f'tl.fromTo("#{id_}",{{scale:2.2,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:{-4 if kind != "game" else 0},duration:.28,ease:"back.out(2.2)"}},{t0:.3f});'
           f'tl.to("#{id_}",{{scale:.6,opacity:0,duration:.18,ease:"power2.in"}},{t1 - .2:.3f});')


Scene.three3d = _three
Scene.parallax = _parallax
Scene.popup = _popup
