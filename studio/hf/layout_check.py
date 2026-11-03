#!/usr/bin/env python3
"""Automatic layout + content check for a built Cyto Short (added Nov 2, 2026 after Ep 10).

Usage (from /home/claude/hf, after `python3 epNN/build.py`):
    python3 layout_check.py ep10 [--brief /home/claude/hf/ep10/EP10_brief.md] [--step 0.25]

It loads epNN/index.html in headless Chromium, seeks the GSAP timeline (window.__timelines.main) every
`step` seconds and flags, per time:
  FAIL  two visible text blocks overlap (area > 12% of the smaller one), unless nested / same card
  FAIL  a text block touches the caption band (.cap) or is cut off by the screen edge
  FAIL  text covered >25% by a Lottie animation (WARN for Cyto's body)
  FAIL  pupils offset more than 8px (eyes look 'off')
  FAIL  an on-screen score-like pattern (3-3, 2-1 ...) or other number that is not in the brief (fabricated figure)
  WARN  overlap 3-12%; text outside the Shorts safe zone; numbers on screen not found in the brief
Exit code 1 if any FAIL. Fix every FAIL, rebuild, re-run. Then still do the 1-fps visual contact-sheet check.
"""
import sys, re, json, time, argparse, threading, http.server, socketserver, functools, os
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("ep")
ap.add_argument("--brief")
ap.add_argument("--step", type=float, default=0.25)
ap.add_argument("--root", default="/home/claude/hf")
ap.add_argument("--size", default="1080x1920", help="WxH; 1920x1080 for long-form landscape (LF01+)")
a = ap.parse_args()

# ---- serve /home/claude/hf over http (file:// breaks ES modules / fetch)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
ROOT = a.root
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), lambda *x, **k: Q(*x, directory=ROOT, **k))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS_COLLECT = r"""
(t) => {
  const tl = window.__timelines && window.__timelines.main;
  if (!tl) return {err: "no window.__timelines.main"};
  tl.seek(t, false);
  const out = [];
  const inTime = (el) => {
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const s = e.getAttribute && e.getAttribute("data-start");
      const d = e.getAttribute && e.getAttribute("data-duration");
      if (s !== null && d !== null && e.id !== "root") {
        const s0 = parseFloat(s), d0 = parseFloat(d);
        if (t < s0 - 1e-3 || t >= s0 + d0 - 1e-3) return false;
      }
    }
    return true;
  };
  const eff = (el) => {
    let o = 1;
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === "none" || cs.visibility === "hidden") return 0;
      o *= parseFloat(cs.opacity);
    }
    return o;
  };
  const all = document.querySelectorAll("body *");
  for (const el of all) {
    if (el.closest(".cap") && !el.classList.contains("cap")) continue;
    if (el.closest("#pill")) continue;
    if (el.closest("defs") || el.tagName === "STYLE" || el.tagName === "SCRIPT") continue;
    let txt = "";
    const isSvgText = el.tagName.toLowerCase() === "text";
    if (isSvgText) txt = el.textContent.trim();
    else if (el.classList.contains("cap")) txt = el.textContent.trim();
    else for (const n of el.childNodes) if (n.nodeType === 3) txt += n.textContent;
    txt = txt.replace(/\s+/g, " ").trim();
    if (!txt) continue;
    if (!inTime(el)) continue;
    const o = eff(el);
    if (o < 0.4) continue;
    let r;
    if (isSvgText) r = el.getBoundingClientRect();
    else {
      const rg = document.createRange(); rg.selectNodeContents(el);
      if (!el.classList.contains("cap")) {   // tight box around OWN text nodes only
        const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
        if (own.length) { rg.setStartBefore(own[0]); rg.setEndAfter(own[own.length - 1]); }
      }
      r = rg.getBoundingClientRect();
    }
    if (r.width < 4 || r.height < 4) continue;
    const card = el.closest(".card,.tile,.gauge,.chip,.stamp,.panel,.tip");
    out.push({id: el.id || el.className || el.tagName, txt: txt.slice(0, 40), cap: el.classList.contains("cap"),
              x: r.left, y: r.top, w: r.width, h: r.height, grp: card ? (card.id || card.className) + ":" + [...document.querySelectorAll(".card,.tile,.gauge,.chip,.stamp,.panel,.tip")].indexOf(card) : "",
              fs: parseFloat(getComputedStyle(el).fontSize)});
  }
  const gfx = [];
  document.querySelectorAll("svg").forEach(sv => {
    if (!sv.innerHTML.includes("__lottie_element")) return;
    if (!inTime(sv) || eff(sv) < 0.4) return;
    const r = sv.getBoundingClientRect(); if (r.width < 30) return;
    gfx.push({type: "lottie", id: (sv.parentElement && sv.parentElement.id) || "lottie", x: r.left, y: r.top, w: r.width, h: r.height});
  });
  // Cyto's real silhouette = body circle + toque (the outfit <image> inside #bodyG is a full 1200px transparent canvas and inflated the box)
  const parts = ["#bodyG > circle", "#toque"].map(q => document.querySelector(q)).filter(Boolean);
  const cy = parts.length ? parts[0] : (document.querySelector("#bodyG") || document.querySelector("#cyto"));
  if (cy && inTime(cy) && eff(cy) > 0.4) {
    const rs = (parts.length ? parts : [cy]).map(e => e.getBoundingClientRect());
    const x0 = Math.min(...rs.map(r => r.left)), y0 = Math.min(...rs.map(r => r.top)), x1 = Math.max(...rs.map(r => r.right)), y1 = Math.max(...rs.map(r => r.bottom));
    if (x1 - x0 > 50) gfx.push({type: "cyto", id: "cyto", x: x0, y: y0, w: x1 - x0, h: y1 - y0});
  }
  const g = (sel, p) => { try { return gsap.getProperty(sel, p) } catch (e) { return 0 } };
  return {items: out, gfx: gfx, pup: [g("#pupL", "x"), g("#pupL", "y"), g("#pupR", "x"), g("#pupR", "y")]};
}
"""

W, Hh = (int(v) for v in a.size.lower().split("x"))
if W > Hh:   # landscape long-form: no Shorts UI, so the safe zone is just "nothing within 40px of an edge" (flag fires at <40 incl. the 10px slack)
    SAFE = dict(left=50, right=W - 50, top=50, bottom=Hh - 50)
else:
    SAFE = dict(left=40, right=1010, top=120, bottom=1560)
fails, warns = {}, {}
seen_text = {}
def add(d, key, t, msg):
    d.setdefault((key, msg), []).append(t)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": Hh})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{port}/{a.ep}/index.html")
    pg.wait_for_timeout(2500)
    T = pg.evaluate("() => { const r=document.getElementById('root'); return parseFloat(r.getAttribute('data-duration')) }")
    t = 0.0
    while t <= T + 1e-6:
        res = pg.evaluate(JS_COLLECT, t)
        if "err" in res:
            print("ERROR:", res["err"]); sys.exit(2)
        items = res["items"]
        for it in items:
            seen_text.setdefault(it["txt"], t)
            # edge cut-off
            vis_w = max(0, min(it["x"] + it["w"], W) - max(it["x"], 0)); vis_h = max(0, min(it["y"] + it["h"], Hh) - max(it["y"], 0))
            frac_vis = (vis_w * vis_h) / (it["w"] * it["h"])
            if 0.05 < frac_vis < 0.94 and it["w"] < 3000:
                add(fails, "edge", t, f'text cut off by screen edge ({int((1-frac_vis)*100)}% outside): "{it["txt"]}"')
            if not it["cap"] and it["fs"] >= 14:
                if it["x"] < SAFE["left"] - 10 or it["x"] + it["w"] > SAFE["right"] + 10 or it["y"] < SAFE["top"] - 10 or it["y"] + it["h"] > SAFE["bottom"] + 10:
                    add(warns, "safe", t, f'outside Shorts safe zone: "{it["txt"]}"')
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                A, B = (dict(it, x=it["x"] + it["w"] * .03, w=it["w"] * .94, y=it["y"] + it["h"] * .15, h=it["h"] * .7) for it in (items[i], items[j]))
                if A["grp"] and A["grp"] == B["grp"]: continue
                ix = max(0, min(A["x"] + A["w"], B["x"] + B["w"]) - max(A["x"], B["x"]))
                iy = max(0, min(A["y"] + A["h"], B["y"] + B["h"]) - max(A["y"], B["y"]))
                inter = ix * iy
                if inter <= 0: continue
                frac = inter / min(A["w"] * A["h"], B["w"] * B["h"])
                kind = "caption" if (A["cap"] or B["cap"]) else "text"
                if frac > 0.12: add(fails, kind, t, f'{kind} overlap {int(frac*100)}%: "{A["txt"]}" x "{B["txt"]}"')
                elif frac > 0.03: add(warns, kind, t, f'{kind} touch {int(frac*100)}%: "{A["txt"]}" x "{B["txt"]}"')
        for it in items:
            if it["cap"]: continue
            for G in res["gfx"]:
                if it["w"] > 0.83 * W: continue
                tx, ty, tw, th = it["x"] + it["w"] * .03, it["y"] + it["h"] * .15, it["w"] * .94, it["h"] * .7
                ix = max(0, min(tx + tw, G["x"] + G["w"] * .92) - max(tx, G["x"] + G["w"] * .04)); iy = max(0, min(ty + th, G["y"] + G["h"] * .92) - max(ty, G["y"] + G["h"] * .04))
                frac = (ix * iy) / (tw * th)
                if frac > 0.25:
                    add(fails if G["type"] == "lottie" else warns, "gfx", t, f'text over {G["type"]} animation ({int(frac*100)}% covered): "{it["txt"]}"')
        px = res["pup"]
        if any(abs(float(v)) > 8 for v in px):
            add(fails, "eyes", t, f"pupils off-centre {[round(float(v),1) for v in px]}")
        t = round(t + a.step, 3)
    b.close()
srv.shutdown()

# ---- number check against the brief
W2N = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split())}
W2N.update({w: 10 * i for i, w in enumerate("x x twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "x"})
def words_to_numbers(s):
    toks = re.findall(r"[a-z]+|\d[\d,\.]*", s.lower().replace("-", " ")); nums, cur, seen = set(), 0, False
    for tk in toks:
        if tk in W2N: cur += W2N[tk]; seen = True
        elif tk == "hundred": cur = max(cur, 1) * 100; seen = True
        elif tk == "thousand": cur = max(cur, 1) * 1000; seen = True
        else:
            if seen: nums.add(cur)
            cur, seen = 0, False
            if re.fullmatch(r"\d[\d,\.]*", tk):
                try: nums.add(float(tk.replace(",", "")))
                except: pass
    if seen: nums.add(cur)
    return {float(n) for n in nums}
brief_path = a.brief or f"{a.root}/{a.ep}/EP{re.sub(r'[^0-9]', '', a.ep)}_brief.md"
brief_nums = set(); raw_brief_text = ""
for cand in (brief_path, f"/root/cyto-uploads/studio/episodes/{a.ep}/EP{re.sub(r'[^0-9]', '', a.ep)}_brief.md"):
    if os.path.exists(cand):
        raw = open(cand, encoding="utf-8").read()
        m = re.search(r"## Script.*?(?=\n## (?:Scene plan|Toronto background))", raw, re.S)   # script + TTS + claims only
        body = m.group(0) if m else raw
        body = re.sub(r"\[[^\]]*\]", " ", body)                     # drop [timing tags]
        body = re.sub(r"https?://\S+|10\.\d{4,9}/\S+", " ", body)      # drop URLs / DOIs
        body = re.sub(r"\(\d+ chars?\)|Chars: \d+.*", " ", body)
        raw_brief_text = body; brief_nums = words_to_numbers(body); brief_path = cand; break
if not brief_nums:
    print(f"WARN: brief not found for number check ({brief_path}); pass --brief")
else:
    for txt, t0 in seen_text.items():
        if re.fullmatch(r"[\d:,\.\s%+x\-–↑↓]+", txt) is None and not re.search(r"\d", txt): continue
        sc = re.search(r"\b\d+\s*[–\-]\s*\d+\b", txt)
        if sc and re.sub(r"\s", "", sc.group(0)) not in re.sub(r"\s", "", raw_brief_text):
            add(fails, "number", t0, f'score-like text not in brief (fabricated?): "{txt}"'); continue
        for m in re.finditer(r"\d+(?:[:,\.]\d+)*", txt):
            tok = m.group(0)
            vals = {float(tok.replace(",", ""))} if re.fullmatch(r"\d+(?:,\d{3})*(?:\.\d+)?", tok) else {float(x) for x in re.split(r"[:]", tok) if x.replace('.', '').isdigit()}
            if vals & brief_nums or vals <= {0.0, 1.0, 6.0, 7.0}: continue
            score = re.search(r"\b\d+\s*[–\-]\s*\d+\b", txt)
            if score: add(fails, "number", t0, f'score-like text not in brief (fabricated?): "{txt}"')
            else: add(warns, "number", t0, f'number "{tok}" on screen not found in brief: "{txt}" (check it is real)')

def persist(d, min_s=0.4):
    """keep only groups that last >= min_s (consecutive samples), so card slide-ins / crossfades don't trigger"""
    keep = {}
    for k, ts in d.items():
        ts = sorted(set(ts)); run = [ts[0]]; best = 0.0; runs = []
        for x in ts[1:]:
            if abs(x - run[-1] - a.step) < 1e-6: run.append(x)
            else: runs.append(run); run = [x]
        runs.append(run)
        good = [r for r in runs if (r[-1] - r[0] + a.step) >= min_s - 1e-6]
        if good: keep[k] = [x for r in good for x in r]
    return keep
num_f = {k: v for k, v in fails.items() if k[0] == 'number'}     # content failures never filtered by duration
fails, warns = persist({k: v for k, v in fails.items() if k[0] != 'number'}), persist(warns)
fails.update(num_f)

def fmt(ts):
    ts = sorted(set(ts)); return f"{ts[0]:.2f}s" if len(ts) == 1 else f"{ts[0]:.2f}-{ts[-1]:.2f}s ({len(ts)} samples)"
print(f"\nLayout check {a.ep}: T={T:.1f}s, step {a.step}s, brief={os.path.basename(brief_path)}")
if errs: print("page errors:", errs[:3])
for title, d in (("FAIL", fails), ("WARN", warns)):
    for (k, msg), ts in sorted(d.items(), key=lambda kv: min(kv[1])):
        print(f"  {title} @ {fmt(ts)}  {msg}")
print(f"\n{len(fails)} FAIL group(s), {len(warns)} WARN group(s)")
sys.exit(1 if fails else 0)
