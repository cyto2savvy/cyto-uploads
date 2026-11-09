#!/usr/bin/env python3
"""No-twitch JITTER CHECK (studio/ep14_addendum.md).
Samples hand, cup, pupils, brows and mouth every frame (rig-local coords: placement and camera removed) and FAILs a part if
  - it reverses direction more than 3 times inside any 0.3 s window, or
  - its frame-to-frame acceleration spikes above 4x its own median (a part that never moves must never jump at all).
Usage: python3 jitter.py <episode index.html> [--rig canon|old] [--fps 30] [--t0 0 --t1 T]"""
import sys, json, argparse
import numpy as np
from playwright.sync_api import sync_playwright

PARTS = {
    "canon": {"handL": "#handL", "cup": "#cup", "handR": "#handR", "pupL": "#pupL", "pupR": "#pupR", "browL": "#browL", "browR": "#browR",
              "mouth": ["#m_closed", "#m_small", "#m_wide", "#m_o"]},
    "old": {"handL": "#armL", "cup": "#cupTable", "handR": "#armR", "pupL": "#pupL", "pupR": "#pupR", "browL": "#browL", "browR": "#browR",
            "mouth": ["#v_rest", "#v_mbp", "#v_small", "#v_a", "#v_e", "#v_o", "#v_u", "#v_fv"]},
}
SAMPLE_JS = """(P)=>{const B=document.getElementById('cytoPos').getBoundingClientRect(),k=1200/B.width,out={};
 const op=e=>{let v=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){const a=n.getAttribute&&n.getAttribute('opacity');v*=parseFloat(getComputedStyle(n).opacity)*(a==null?1:parseFloat(a));if(n.id==='cytoPos')break}return v};
 for(const [name,sel] of Object.entries(P)){let el;
  if(Array.isArray(sel)){el=sel.map(s=>document.querySelector(s)).filter(Boolean).sort((a,b)=>op(b)-op(a))[0]}else el=document.querySelector(sel);
  if(!el){out[name]=null;continue}const r=el.getBoundingClientRect();out[name]=[((r.left+r.right)/2-B.left)*k,((r.top+r.bottom)/2-B.top)*k]}
 return out}"""


def sample(html, parts, fps=30, t0=0.0, t1=None):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + html, wait_until="load")
        for _ in range(100):
            if pg.evaluate("!!(window.__timelines && window.__timelines.main)"): break
            pg.wait_for_timeout(100)
        T = pg.evaluate("window.__timelines.main.duration()") if t1 is None else t1
        rows = []
        for i in range(int((T - t0) * fps)):
            t = t0 + i / fps
            pg.evaluate(f"void window.__timelines.main.seek({t:.4f},false)")
            rows.append(pg.evaluate(SAMPLE_JS, parts))
        b.close()
    return rows


def analyse(rows, fps=30, dead=0.05):
    win = max(2, round(0.3 * fps)); res = {}
    for name in rows[0]:
        if rows[0][name] is None: continue
        P = np.array([r[name] for r in rows], float)
        d = np.diff(P, axis=0)
        worst_rev = 0
        for ax in (0, 1):
            s = np.sign(np.where(np.abs(d[:, ax]) > dead, d[:, ax], 0))
            # reversal = sign flip between consecutive non-zero moves; count those inside every 0.3 s window
            idx = np.nonzero(s)[0]; flips = [idx[j] for j in range(1, len(idx)) if s[idx[j]] != s[idx[j - 1]]]
            for f in flips:
                worst_rev = max(worst_rev, sum(1 for g in flips if f <= g < f + win))
        a = np.linalg.norm(np.diff(P, 2, axis=0), axis=1)
        med = float(np.median(a)); mx = float(a.max()) if len(a) else 0.0
        if med < 1e-3: acc_ok, ratio = mx < 0.05, (float("inf") if mx >= 0.05 else 0.0)
        else: ratio = mx / med; acc_ok = ratio <= 4
        res[name] = dict(reversals_in_0_3s=worst_rev, accel_max=round(mx, 3), accel_median=round(med, 4),
                         spike_ratio=(round(ratio, 2) if ratio != float("inf") else "static-part jump"), ok=bool(worst_rev <= 3 and acc_ok))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--rig", default="canon"); ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--t0", type=float, default=0); ap.add_argument("--t1", type=float, default=None); ap.add_argument("--json")
    a = ap.parse_args()
    res = analyse(sample(a.html, PARTS[a.rig], a.fps, a.t0, a.t1), a.fps)
    fails = 0
    for k, v in res.items():
        print(("PASS " if v["ok"] else "FAIL ") + f"{k:6s} reversals/0.3s={v['reversals_in_0_3s']}  accel max={v['accel_max']} median={v['accel_median']} ratio={v['spike_ratio']}")
        fails += not v["ok"]
    print(f"JITTER CHECK: {fails} FAIL / {len(res)} parts")
    if a.json: json.dump(res, open(a.json, "w"), indent=1)
    sys.exit(1 if fails else 0)
