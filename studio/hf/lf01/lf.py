"""LF01 long-form (1920x1080 LANDSCAPE) framework. One composition per chapter: lf01/chK/index.html.
Layout: Cyto big in the left third (x 60-600), content panel on the right two-thirds (x 660-1860, y 60-850),
captions under the panel (y 875+). Nothing within 40px of any edge (designed to 60px).
Each chapter covers [B[k], B[k+1]) of the global voice (frame-aligned), so the renders concat cleanly.
Retention: every helper that makes a visible change registers a beat; build() fills any gap > 2.9 s with a
small panel push-in so something changes at least every 3 s. Ken Burns runs on every slide (.kb) and background."""
import json, os, re, sys, shutil, subprocess
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/cyto2")
import cytohf as C, cyto3 as R, art as A
from neutro import neutro_html, neutro_js

W, H, FPS = 1920, 1080, 30
P = "/home/claude/hf/lf01"; V = "/home/claude/lf01"
TM = json.load(open(f"{V}/timing.json"))
ALLW = TM["words"]; CHAP = TM["chapters"]
import math
B = [math.floor(c["t0"] * FPS) / FPS for c in CHAP] + [round((TM["total"] + 0.6) * FPS) / FPS]
INK, CREAM, GOLD, CORAL, TEAL, BLUE, PINK, GREEN, SKY = "#0c1622", "#FAF4E8", "#FFD166", "#FF7A59", "#3fc1b0", "#4f86ff", "#f6a6c8", "#5AE68C", "#9fc3e8"
PX, PY, PW, PH = 660, 60, 1200, 790          # panel
CAP_Y = 878
POS = C.place(350, 640, 0.70)                # Cyto body centre (stage), scale
TITLES = ["THE COUNTDOWN", "WHAT'S IN THE SMOKE", "THE FIRST HOURS", "THE FIRST WEEK", "WEEKS 2 TO 4", "MONTHS TO YEARS", "CYTO'S TIPS", "THE 6IX TOUR"]

# caption display fixes (real spellings / digits); merges are (first_word_regex, n_words, text)
MERGES = [(r"^one,$", 11, "1-877-513-5333,"), (r"^one$", 6, "123456."), (r"^twenty-five$", 3, "25 TO 34,"), (r"^Thirty-five$", 3, "35 TO 44,"),
          (r"^Forty-five$", 3, "45 TO 54,"), (r"^forty-four$", 2, "44%."), (r"^ninety$", 2, "90%."), (r"^three$", 2, "300")]
MERGE_OK = {"1-877-513-5333,": "three", "123456.": "six", "25 TO 34,": "thirty", "35 TO 44,": "forty", "45 TO 54,": "fifty", "44%.": "percent", "90%.": "percent", "300": "hundred"}
SUBS = {"forty,": "40,", "ten": "10", "nine.": "9.", "six.": "6."}


def cap_words(words):
    out = []; i = 0
    while i < len(words):
        w = words[i]; done = False
        for rx, n, txt in MERGES:
            if re.match(rx, w["w"]) and i + n <= len(words) and MERGE_OK[txt] in words[i + n - 1]["w"].lower():
                out.append(dict(w, w=txt, t1=words[i + n - 1]["t1"])); i += n; done = True; break
        if done: continue
        out.append(dict(w, w=SUBS.get(w["w"], w["w"]) if w["ch"] == 5 or w["w"] not in ("ten", "nine.", "six.") else w["w"])); i += 1
    return out


class Ch:
    def __init__(self, k):
        self.k = k; self.b0, self.b1 = B[k], B[k + 1]; self.T = round(self.b1 - self.b0, 4)
        self.dir = f"{P}/ch{k}"; os.makedirs(f"{self.dir}/assets", exist_ok=True)
        self.words = [dict(w, t0=round(w["t0"] - self.b0, 3), t1=round(w["t1"] - self.b0, 3)) for w in ALLW if self.b0 - 0.01 <= w["t0"] < self.b1]
        self.J, self.beats, self.sfx, self.slides, self.bgs, self.over = [], [], [], [], [], []
        self.nslide = 0; self.css = ""; self.hidden = []

    # ---------------- timing
    def wt(self, word, after=0.0, end=False):
        key = re.sub(r"[^a-z0-9%'/-]", "", word.lower())
        for w in self.words:
            if w["t0"] >= after - 1e-6 and re.sub(r"[^a-z0-9%'/-]", "", w["w"].lower()) == key:
                return round(w["t1"] if end else w["t0"], 3)
        raise KeyError(f"ch{self.k}: {word} after {after}")

    def j(self, s): self.J.append(s)
    def beat(self, t): self.beats.append(t)
    def fx(self, kind, t): self.sfx.append((kind, round(self.b0 + t, 3)))

    # ---------------- animation helpers (all register beats)
    def pop(self, sel, t, s="pop", hide=True):
        if hide: self.hidden.append(sel); self.j(f'tl.set("{sel}",{{opacity:0}},0);')
        self.j(f'tl.fromTo("{sel}",{{scale:0.2,opacity:0}},{{scale:1,opacity:1,duration:0.34,ease:"back.out(2.6)",immediateRender:false}},{t:.3f});')
        self.beat(t); s and self.fx(s, t)

    def out(self, sel, t):
        self.j(f'tl.to("{sel}",{{opacity:0,scale:0.8,duration:0.18,ease:"power2.in"}},{t:.3f});'); self.beat(t)

    def stamp(self, sel, t, r=-6, s="hit"):
        self.hidden.append(sel); self.j(f'tl.set("{sel}",{{opacity:0}},0);tl.fromTo("{sel}",{{scale:2.6,opacity:0,rotation:{r - 6}}},{{scale:1,opacity:1,rotation:{r},duration:0.26,ease:"back.out(1.6)",immediateRender:false}},{t:.3f});')
        self.beat(t); s and self.fx(s, t); self.punch(t + 0.05)

    def slide_in(self, sel, t, dx=90, s="pop"):
        self.hidden.append(sel); self.j(f'tl.set("{sel}",{{opacity:0}},0);tl.fromTo("{sel}",{{x:{dx},opacity:0}},{{x:0,opacity:1,duration:0.36,ease:"back.out(1.8)",immediateRender:false}},{t:.3f});')
        self.beat(t); s and self.fx(s, t)

    def rise(self, sel, t, dy=60, s=None):
        self.hidden.append(sel); self.j(f'tl.set("{sel}",{{opacity:0}},0);tl.fromTo("{sel}",{{y:{dy},opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"power3.out",immediateRender:false}},{t:.3f});')
        self.beat(t); s and self.fx(s, t)

    def draw(self, sel, t, dur=0.7, s=None):
        """stroke draw-on: element needs pathLength=1 + stroke-dasharray=1 + stroke-dashoffset=1 (see DRAW attr)."""
        self.j(f'tl.fromTo("{sel}",{{strokeDashoffset:100}},{{strokeDashoffset:0,duration:{dur},ease:"power2.out",immediateRender:false}},{t:.3f});')
        self.beat(t); s and self.fx(s, t)

    def punch(self, t, s=1.035):
        self.j(f'tl.to("#punch",{{scale:{s},duration:0.08,ease:"power2.out"}},{t:.3f});tl.to("#punch",{{scale:1,duration:0.35,ease:"back.out(2)"}},{t + 0.08:.3f});')

    def nudge(self, t):
        """filler beat: small push-in on the panel content (used by build() for gaps > 2.9 s)"""
        self.j(f'tl.to("#pnudge",{{scale:1.03,duration:0.25,ease:"power2.out"}},{t:.3f});tl.to("#pnudge",{{scale:1,duration:0.6,ease:"sine.inOut"}},{t + 0.25:.3f});')
        self.beats.append(t)

    # ---------------- structure
    def bg(self, id_, t0, t1, inner, kb=(1.0, 1.06), dim=0.0):
        """full-bleed Toronto background (svg inner), Ken Burns over its life."""
        self.bgs.append((id_, t0, t1, inner, kb, dim))

    def slide(self, id_, t0, t1, inner, title=None, panel=True, s="whoosh"):
        """panel slide; cut = transition (whip-in of the new slide, old one out)."""
        self.slides.append((id_, t0, t1, inner, title, panel)); self.nslide += 1
        if t0 > 0.05: self.fx(s, t0 - 0.15) if s else None
        self.beat(t0)

    def overlay(self, html): self.over.append(html)

    # ---------------- build
    def build(self, cyto_js_kw=None, neutro=(), extra_css="", cap_keys=None, cyto_pos=None, cap_hide=()):
        T = self.T
        # backgrounds
        bg_html = []
        for id_, t0, t1, inner, kb, dim in self.bgs:
            bg_html.append(f'<div id="{id_}" class="bg clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}"><div id="{id_}K" class="bgk">'
                           f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">{inner}</svg></div>'
                           + (f'<div class="bgdim" style="opacity:{dim}"></div>' if dim else "") + '</div>')
            self.j(f'tl.fromTo("#{id_}K",{{scale:{kb[0]}}},{{scale:{kb[1]},duration:{t1 - t0:.3f},ease:"none",immediateRender:false}},{t0:.3f});')
            if t0 > 0.05:
                self.j(f'tl.fromTo("#{id_}",{{opacity:0}},{{opacity:1,duration:0.35,ease:"power1.out",immediateRender:false}},{t0:.3f});'); self.beat(t0)
        # slides
        sl_html = []
        for id_, t0, t1, inner, title, panel in self.slides:
            ttl = f'<div class="ptitle">{title}</div>' if title else ""
            sl_html.append(f'<div id="{id_}" class="slide clip{" panel" if panel else ""}" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}">{ttl}<div id="{id_}K" class="kb">{inner}</div></div>')
            self.j(f'tl.fromTo("#{id_}K",{{scale:1}},{{scale:1.045,duration:{t1 - t0:.3f},ease:"none",immediateRender:false}},{t0:.3f});')
            if t0 > 0.05:
                self.j(f'tl.fromTo("#{id_}",{{x:160,opacity:0}},{{x:0,opacity:1,duration:0.32,ease:"power3.out",immediateRender:false}},{t0:.3f});')
            if t1 < T - 0.05:
                self.j(f'tl.to("#{id_}",{{x:-160,opacity:0,duration:0.22,ease:"power2.in"}},{t1 - 0.22:.3f});')
        # chapter title card (1.5 s) + chapter-edge whip
        title_html = ""
        if self.k > 0:
            title_html = (f'<div id="ttl" class="clip ttl" data-start="0.1" data-duration="1.55"><div class="ttln">CHAPTER {self.k}</div><div class="ttlt">{TITLES[self.k]}</div></div>')
            self.j('tl.fromTo("#ttl",{scaleY:0,opacity:1},{scaleY:1,duration:0.22,ease:"back.out(1.6)"},0.1);'
                   'tl.fromTo("#ttl .ttlt",{scale:1.6,opacity:0},{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"},0.2);'
                   'tl.to("#ttl",{scaleY:0,opacity:0,duration:0.2,ease:"power2.in"},1.45);')
            self.fx("hit", 0.15); self.beat(0.1)
        tr_html = ""
        if self.k > 0:   # uncover from previous chapter's whip
            tr_html += '<div id="whipIn" class="clip whip" data-start="0" data-duration="0.25"></div>'
            self.j('tl.fromTo("#whipIn",{x:-200},{x:2300,duration:0.25,ease:"power2.out"},0);')
        if self.k < 7:
            tr_html += f'<div id="whipOut" class="clip whip" data-start="{T - 0.25:.3f}" data-duration="0.25"></div>'
            self.j(f'tl.fromTo("#whipOut",{{x:-2600}},{{x:-200,duration:0.25,ease:"power2.in"}},{T - 0.25:.3f});')
            self.fx("whoosh", T - 0.3)
        # retention filler: any visual gap > 2.9 s gets a nudge
        bs = sorted(set(round(b, 2) for b in self.beats + [0.0, T]))
        fill = []
        for a, b in zip(bs, bs[1:]):
            n = int((b - a) / 2.6)
            for i in range(1, n + 1): fill.append(round(a + (b - a) * i / (n + 1), 2))
        for t in fill: self.nudge(t)
        self.max_gap = max(b - a for a, b in zip(*(lambda s: (s, s[1:]))(sorted(set(round(b, 2) for b in self.beats + [0.0, T])))))
        # captions
        cw = cap_words(self.words)
        cw = [w for w in cw if not any(a <= w["t0"] < b for a, b in cap_hide)]
        cap_html, cap_js = captions(cw, cap_keys or {})
        # Cyto
        vw = f"{self.dir}/assets/voice.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{V}/voice.wav", "-ss", f"{self.b0:.4f}", "-t", f"{T:.4f}", "-ar", "48000", vw], check=True)
        mouth = R.viseme_track(vw, self.words)
        if not mouth or mouth[0][0] > 0: mouth.insert(0, [0, "rest"])
        kw = dict(cyto_js_kw or {})
        kw.setdefault("blinks", [(round(1.3 + i * 3.1, 2), 0.1) for i in range(int(T / 3.1))])
        rig_js = R.rig3_js(mouth, T, **kw)
        pos = cyto_pos or POS
        # assets
        C.copy_assets_v2(self.dir)
        html = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
<head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="assets/gsap.min.js"></script><script src="assets/lottie_svg.min.js"></script>
<style>{CSS}{extra_css}{self.css}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
<audio id="mix" class="clip" src="assets/voice.wav" data-start="0" data-duration="{T}" data-has-audio="true"></audio>
<div id="punch" class="clip" data-start="0" data-duration="{T}">
{chr(10).join(bg_html)}
<div id="pnudge">{chr(10).join(sl_html)}</div>
{chr(10).join(self.over)}
<div id="cytoLayer">{R.rig3_html("outfit_hoodie", "cup_red")}</div>
</div>
{title_html}
{cap_html}
{tr_html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{rig_js}
gsap.set("#cytoPos",{json.dumps(pos)});tl.set("#cytoPos",{json.dumps(pos)},0);
{"".join(f"gsap.set({json.dumps(h)},{{opacity:0}});" for h in self.hidden)}
{chr(10).join(self.J)}
{cap_js}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>"""
        open(f"{self.dir}/index.html", "w").write(html)
        for f in ("hyperframes.json", "package.json"):
            if not os.path.exists(f"{self.dir}/{f}"): shutil.copy(f"/home/claude/hf/ep13/{f}", f"{self.dir}/{f}")
        if not os.path.exists(f"{self.dir}/node_modules"): os.symlink("/home/claude/hf/node_modules", f"{self.dir}/node_modules")
        json.dump(self.sfx, open(f"{V}/sfx_ch{self.k}.json", "w"))
        print(f"ch{self.k}: T={T:.2f}s slides={self.nslide} beats={len(self.beats)} fillers={len(fill)} sfx={len(self.sfx)} bytes={len(html)}")


def captions(words, keys, max_chars=30, max_words=6):
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        long_ = sum(len(words[j]["w"]) + 1 for j in cur) > max_chars
        if len(cur) >= max_words or long_ or re.search(r"[.,?!:…]$", w["w"]) or (i + 1 < len(words) and words[i + 1]["t0"] - w["t1"] > 0.3):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    html, js = [], []
    for ci, ch in enumerate(chunks):
        a = max(0, words[ch[0]]["t0"] - 0.05)
        b = words[chunks[ci + 1][0]]["t0"] - 0.05 if ci + 1 < len(chunks) else words[ch[-1]]["t1"] + 0.8
        b = min(b, words[ch[-1]]["t1"] + 1.4)
        spans = []
        for i in ch:
            raw = words[i]["w"]; key = re.sub(r"[^A-Za-z0-9%]", "", raw).lower(); col = keys.get(key)
            st = f' style="color:{col}"' if col else ""
            spans.append(f'<span id="w{ci}_{i}" class="w{" key" if col else ""}"{st}>{raw.upper()}</span>')
            js.append(f'tl.fromTo("#w{ci}_{i}",{{opacity:0,scale:{1.5 if col else 1.2},y:14}},{{opacity:1,scale:1,y:0,duration:{0.2 if col else 0.13},ease:"back.out(2.4)"}},{max(0, words[i]["t0"] - 0.03):.3f});')
        html.append(f'<div id="cap{ci}" class="cap clip" data-start="{a:.3f}" data-duration="{max(0.1, b - a):.3f}">{" ".join(spans)}</div>')
    return "\n".join(html), "\n".join(js)


DRAW = 'pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"'


def NT(idp, left, top, s, pose="cross"):
    return f'<div id="{idp}W" class="ntw" style="left:{left}px;top:{top}px;transform:scale({s})"><div id="{idp}M">{neutro_html(idp, pose)}</div></div>'


def svg(inner, w=PW, h=PH, style="position:absolute;left:0;top:0;overflow:visible"):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="{style}">{inner}</svg>'


def src_card(id_, head, body, color=BLUE, left=None, top=640, width=560):
    """in-panel source tag (34px+). Panel-local coords."""
    left = PW - width - 30 if left is None else left
    return (f'<div id="{id_}" class="card" style="left:{left}px;top:{top}px;width:{width}px;border-left-color:{color}">'
            f'<h3 style="color:{color}">{head}</h3>' + (f'<p>{body}</p>' if body else "") + '</div>')


CSS = f"""
{C.FONT_CSS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0c1622; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:InterXB; }}
#punch {{ position:absolute; inset:0; transform-origin:960px 540px; }}
#pnudge {{ position:absolute; inset:0; transform-origin:{PX + PW / 2}px {PY + PH / 2}px; }}
.bg {{ position:absolute; inset:0; overflow:hidden; }}
.bgk {{ position:absolute; inset:0; transform-origin:30% 60%; }}
.bgdim {{ position:absolute; inset:0; background:#0c1622; }}
.slide {{ position:absolute; left:{PX}px; top:{PY}px; width:{PW}px; height:{PH}px; }}
.slide.panel {{ border-radius:36px; background:rgba(15,34,54,.96); border:3px solid #2c4d6e; box-shadow:0 20px 50px rgba(0,0,0,.45); overflow:hidden; }}
.kb {{ position:absolute; inset:0; transform-origin:50% 45%; }}
.ptitle {{ position:absolute; left:40px; top:28px; font:34px InterBlack; color:#96b0c4; letter-spacing:.05em; z-index:5; }}
.big {{ position:absolute; text-align:center; font-family:InterBlack; line-height:.98; letter-spacing:-1px;
  paint-order:stroke fill; -webkit-text-stroke:12px #0c1622; z-index:30; white-space:nowrap; }}
.chip {{ position:absolute; font-family:InterBlack; letter-spacing:.03em; padding:10px 24px; border-radius:30px; border:5px solid #0c1622;
  box-shadow:0 6px 0 #0c1622; white-space:nowrap; color:#0c1622; z-index:30; font-size:42px; }}
.stamp {{ position:absolute; font:92px InterBlack; color:#FF7A59; padding:6px 30px; border:10px solid #FF7A59; border-radius:24px;
  background:rgba(12,22,34,.92); z-index:40; letter-spacing:.02em; white-space:nowrap; }}
.card {{ position:absolute; padding:18px 26px 18px 30px; border-radius:24px; background:#FAF4E8; border-left:14px solid #FF7A59; box-shadow:0 12px 26px rgba(0,0,0,.35); z-index:30; }}
.card h3 {{ font:34px InterBlack; letter-spacing:.02em; white-space:nowrap; }}
.card p {{ font:34px/1.2 InterSB; color:#0c1622; margin-top:6px; }}
.lbl {{ position:absolute; font:40px InterBlack; color:#FAF4E8; white-space:nowrap; paint-order:stroke fill; -webkit-text-stroke:8px #0c1622; z-index:20; }}
.ntw {{ position:absolute; width:600px; height:720px; transform-origin:0 0; z-index:25; }}
.cap {{ position:absolute; left:{PX}px; width:{PW}px; top:{CAP_Y}px; text-align:center; font:58px/1.08 InterBlack; color:#FAF4E8; -webkit-text-stroke:3px #0c1622;
  paint-order:stroke fill; text-shadow:0 5px 0 rgba(0,0,0,.4); z-index:50; }}
.w {{ display:inline-block; opacity:0; }}
.key {{ font-size:68px; }}
.ttl {{ position:absolute; left:{PX - 20}px; top:280px; width:{PW + 40}px; height:280px; border-radius:30px; border-left:10px solid #0c1622; border-right:10px solid #0c1622; background:linear-gradient(90deg,#FF7A59,#FFD166); z-index:80;
  border-top:10px solid #0c1622; border-bottom:10px solid #0c1622; transform-origin:50% 50%; opacity:0; }}
.ttln {{ position:absolute; left:0; width:100%; top:36px; text-align:center; font:44px InterBlack; color:#0c1622; letter-spacing:.2em; }}
.ttlt {{ position:absolute; left:0; width:100%; top:100px; text-align:center; font:104px InterBlack; white-space:nowrap; color:#0c1622; letter-spacing:-2px; }}
.whip {{ position:absolute; top:0; left:0; width:2400px; height:{H}px; z-index:95;
  background:linear-gradient(90deg, rgba(255,122,89,0) 0%, #FF7A59 22%, #FFD166 50%, #FF7A59 78%, rgba(255,122,89,0) 100%); }}
#cytoLayer {{ position:absolute; inset:0; z-index:20; pointer-events:none; }}
{R.rig3_css()}
"""
