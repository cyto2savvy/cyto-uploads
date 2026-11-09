#!/usr/bin/env python3
"""Cyto v2 canon + animation tests.  Run:  python3 test_cyto.py   (needs node, xmllint, numpy, pillow, playwright)
Builds the SVGs with SEED=3 into a temp dir, renders the 8s organelle loop frame by frame, and checks it."""
import os, sys, subprocess, tempfile, shutil, io, re, statistics, math
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES, DUR = 96, 8.0
BODY = dict(cx=512, cy=505, rx=308*.86, ry=292*.86)   # pfp placement of the cell body
MARGIN = 20                                             # px beyond the body ellipse: outline stroke + soft drop-shadow halo (<=5% faint, measured to 14px)
results = []

def check(name, ok, detail=""):
    results.append(ok); print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))

def build(d, seed, anim=True):
    env = dict(os.environ, SEED=str(seed), ANIM="1" if anim else "0")
    subprocess.run(["node", os.path.join(HERE, "cyto2d.js")], cwd=d, env=env, check=True, capture_output=True)

tmp = tempfile.mkdtemp(prefix="cyto_test_")
try:
    a, b, c = (os.path.join(tmp, n) for n in "abc")
    for p in (a, b, c): os.makedirs(p)
    build(a, 3); build(b, 3); build(c, 4)

    # 1 valid XML
    for f in ("pfp.svg", "cover.svg", "banner.svg", "fits.svg", "pfp_anim.svg"):
        r = subprocess.run(["xmllint", "--noout", os.path.join(a, f)], capture_output=True, text=True)
        check(f"valid SVG: {f}", r.returncode == 0, r.stderr.strip()[:80])

    svg = open(os.path.join(a, "pfp_anim.svg")).read()
    # 2 determinism + randomness
    check("SEED=3 is reproducible", open(os.path.join(a, "pfp.svg")).read() == open(os.path.join(b, "pfp.svg")).read())
    check("different SEED moves organelles", open(os.path.join(a, "pfp.svg")).read() != open(os.path.join(c, "pfp.svg")).read())

    # 3 design canon
    pupils = re.findall(r'<circle cx="(-?[\d.]+)" cy="[\d.]+" r="25" fill="#0b0b12"/>', svg)
    check("pupils parallel (both eyes same offset)", len(pupils) == 2 and pupils[0] == pupils[1], str(pupils))
    check("organelles clipped to cell body", 'clip-path="url(#bodyclip2)"' in svg and svg.count("animateTransform") >= 4,
          f"{svg.count('animateTransform')} drift anims")
    check("no fingers anywhere", "finger" not in svg.lower())
    check("generic cup has Cyto-face logo, no real brand", "cupw" in svg and not re.search(r"\b(tim|tims|timmy|horton|hortons|starbucks|dunkin|mcdonald)\b", svg, re.I))
    check("gold chain + 6 medallion present", "gold" in svg and ">6<" in svg.replace(" ", ""))
    check("outfit variants render", all(subprocess.run(["node", os.path.join(HERE, "cyto2d.js")], cwd=a, env=dict(os.environ, SEED="3", FIT=f), capture_output=True).returncode == 0 for f in ("none", "jersey", "hoodie", "puffer")))
    build(a, 3)   # restore anim svg after the FIT loop

    # 4 render the loop
    imgs = []
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1000, "height": 1000})
        pg.goto("file://" + os.path.join(a, "pfp_anim.svg")); pg.wait_for_timeout(300)
        for i in range(FRAMES):
            pg.evaluate("t=>{const s=document.documentElement;s.pauseAnimations();s.setCurrentTime(t)}", i * DUR / FRAMES)
            imgs.append(np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("RGB")).astype(np.int16))
        br.close()
    A = np.stack(imgs)

    yy, xx = np.mgrid[0:1000, 0:1000]
    outside = (((xx-BODY["cx"])/(BODY["rx"]+MARGIN))**2 + ((yy-BODY["cy"])/(BODY["ry"]+MARGIN))**2) > 1
    inside = (((xx-BODY["cx"])/(BODY["rx"]-12))**2 + ((yy-BODY["cy"])/(BODY["ry"]-12))**2) < 1

    # organelles never leak outside the cell: pixels outside the body are identical in every frame
    dev_out = np.abs(A - A[0]).max(axis=(0, 3))[outside].max()
    check("nothing outside the cell changes (organelles can't cover or leave)", dev_out == 0, f"max pixel change outside = {dev_out}")

    motion = np.abs(A - A[0]).sum(axis=3)[:, inside].sum(axis=1)
    check("organelles actually move inside the cell", motion.max() > 5000, f"peak changed-pixel energy {int(motion.max())}")

    step = np.array([np.abs(A[(i+1) % FRAMES] - A[i]).sum() for i in range(FRAMES)], dtype=float)  # includes seam (last->first)
    med = statistics.median(step)
    check("smooth: no jitter spikes (max step < 3x median)", step.max() < 3*med, f"max {step.max():.0f}, median {med:.0f}")
    check("never frozen: every step moves", step.min() > 0, f"min {step.min():.0f}")
    check("seamless loop (last->first step like any other)", step[-1] < 2*med, f"seam {step[-1]:.0f} vs median {med:.0f}")
    # direction reversals of a motion signal (centroid x of changed pixels) - no twitch
    sig = motion - motion.mean()
    rev = int(((np.diff(np.sign(np.diff(motion))) != 0)).sum())
    check("no twitch: motion energy reverses direction <= 12 times per loop", rev <= 12, f"{rev} reversals")

    # 5 ANIMATABLE RIG (RIG=1): layers, talking mouths, blink, rigid cup+hand group, no jitter, flush outfit
    r = os.path.join(tmp, "r"); os.makedirs(r)
    subprocess.run(["node", os.path.join(HERE, "cyto2d.js")], cwd=r, env=dict(os.environ, SEED="3", RIG="1", EXPR="solemn"), check=True, capture_output=True)
    rsvg = open(os.path.join(r, "cyto_rig_hoodie_solemn.svg")).read()
    check("rig SVG valid", subprocess.run(["xmllint", "--noout", os.path.join(r, "cyto_rig_hoodie_solemn.svg")]).returncode == 0)
    need = ["cyto", "armCup", "handL", "cup", "bob", "armR", "handR", "body", "orgs", "outfit", "eyeL", "eyeR", "pupL", "pupR", "lidL", "lidR",
            "browL", "browR", "mouth", "m_closed", "m_small", "m_wide", "m_o", "chain", "toque", "pom"]
    miss = [i for i in need if f'id="{i}"' not in rsvg]
    check("rig layers have ids (body, eyes, brows, mouth, arm+hand+cup, hat, chain, organelles)", not miss, f"missing {miss}")
    check("rig organelles drift via runtime (>=8 .org groups, no SMIL)", rsvg.count('class="org"') >= 8 and "animateTransform" not in rsvg, f"{rsvg.count('class=\"org\"')} org")
    check("rig: no ids collide with gradient/clip ids", len(re.findall(r'id="([^"]+)"', rsvg)) == len(set(re.findall(r'id="([^"]+)"', rsvg))))
    RT = open(os.path.join(HERE, "cyto_rig_runtime.js")).read()
    page = os.path.join(r, "rig.html")
    open(page, "w").write(f'<html><body style="margin:0;background:#1a2d5e">{rsvg}<script>{RT}</script></body></html>')
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1100, "height": 1100}); pg.goto("file://" + page)
        shot = lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("RGB")).astype(np.int16)
        pose = lambda mouth, blink=None, closed=None, t=0: pg.evaluate("""([m,b,c,t])=>{const R=CytoRig(document.querySelector('svg'),{mouth:[[0,m]],blinks:b!=null?[b]:[],closed:c?[c]:[],bob:{amp:0},armR:{deg:0}});return R.update(t)}""", [mouth, blink, closed, t])
        imgs = {}
        for m in ("closed", "small", "wide", "o"):
            pose(m); imgs[m] = shot()
        mouth_box = (slice(550 + 80, 550 + 165), slice(550 - 70, 550 + 90))
        diffs = {f"{a}-{b}": int(np.abs(imgs[a][mouth_box] - imgs[b][mouth_box]).sum() // 1000) for a in imgs for b in imgs if a < b}
        check("talking mouth set: closed/small/wide/o all exist and look different", min(diffs.values()) > 50, str(diffs))
        # geometry, not pixels: the root drop-shadow filter re-rasterises a few anti-aliased edge pixels on any repaint
        geo = "()=>[...document.querySelectorAll('[id]')].filter(e=>!/^m_|^mouth$/.test(e.id)&&e.getBoundingClientRect).map(e=>{const r=e.getBoundingClientRect();return e.id+':'+[r.x,r.y,r.width,r.height].map(v=>v.toFixed(2))}).join('|')"
        moved = []
        for m in ("closed", "small", "wide", "o"):
            pose(m); moved.append(pg.evaluate(geo))
        check("mouth swaps move nothing outside the mouth (all other layer boxes identical)", len(set(moved)) == 1, f"{len(set(moved))} distinct layouts")
        eye_box = (slice(550 - 70, 550 + 50), slice(550 - 160, 550 - 40))
        white = lambda im: int(((im[eye_box] > 235).all(axis=2)).sum())
        pose("closed"); w_open = white(shot())
        pose("closed", blink=0.0, t=0.08); w_shut = white(shot())
        pose("closed", blink=0.0, t=0.30); w_back = white(shot())
        check("blink closes the eye and reopens it", w_shut < 0.1 * w_open and abs(w_back - w_open) < 0.02 * w_open, f"white px open {w_open} shut {w_shut} after {w_back}")
        rigid = pg.evaluate("""()=>{const g=document.getElementById('armCup'),c=document.getElementById('cup'),h=document.getElementById('handL');
            const ctr=e=>{const r=e.getBoundingClientRect();return [(r.left+r.right)/2,(r.top+r.bottom)/2]};
            const a=[ctr(c),ctr(h)]; g.setAttribute('transform','translate(40 -25) rotate(6 -330 180)'); const b=[ctr(c),ctr(h)]; g.removeAttribute('transform');
            return {same_parent: c.parentNode===g && h.parentNode===g, dc:[b[0][0]-a[0][0],b[0][1]-a[0][1]], dh:[b[1][0]-a[1][0],b[1][1]-a[1][1]]}}""")
        check("cup + hand are ONE rigid group (move together)", rigid["same_parent"] and math.dist(rigid["dc"], rigid["dh"]) < 30 and math.dist(rigid["dc"], [0, 0]) > 20, str(rigid))
        # no jitter: idle 8 s with talking + blinks, sampled at 30 fps in rig coordinates
        sys.path.insert(0, HERE); import jitter as JT
        rows = pg.evaluate("""()=>{const R=CytoRig(document.querySelector('svg'),{mouth:[[0,'closed'],[0.5,'small'],[0.6,'wide'],[0.7,'o'],[0.8,'small'],[1.2,'closed'],[3,'wide'],[3.2,'closed']],blinks:[1.5,4.2,6.9]});
            const S=['handL','cup','handR','pupL','pupR','browL','browR'],out=[],M=['m_closed','m_small','m_wide','m_o'];
            for(let i=0;i<240;i++){const s=R.update(i/30);const o={};for(const k of S){const r=document.getElementById(k).getBoundingClientRect();o[k]=[(r.left+r.right)/2,(r.top+r.bottom)/2]}
             const r=document.getElementById('m_'+s).getBoundingClientRect();o.mouth=[(r.left+r.right)/2,(r.top+r.bottom)/2];out.push(o)}return out}""")
        jr = JT.analyse(rows, 30)
        bad = {k: v for k, v in jr.items() if not v["ok"]}
        check("rig idle has no jitter (<=3 reversals/0.3s, accel spikes <=4x median)", not bad, str(bad) if bad else f"{len(jr)} parts ok")
        # outfit flush with the body (addendum: silhouette width within 4% of base Cyto)
        def width(fit):
            s = open(os.path.join(r, f"cyto_rig_{fit}_solemn.svg")).read()
            pg.set_content(f'<html><body style="margin:0;background:#000">{s}</body></html>')
            pg.evaluate("()=>{for(const id of ['armCup','ledge','shadow','armR','toque','chain']){const e=document.getElementById(id);if(e)e.setAttribute('opacity',0)}}")
            im = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("L")); cols = np.nonzero((im > 12).any(axis=0))[0]
            return int(cols.max() - cols.min())
        w0 = width("none"); ws = {f: width(f) for f in ("hoodie", "puffer", "jersey")}
        check("outfits flush with the body (silhouette width within 4%)", all(abs(v - w0) <= 0.04 * w0 for v in ws.values()), f"base {w0} {ws}")
        br.close()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
