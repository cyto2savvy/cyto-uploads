#!/usr/bin/env python3
"""Cyto v2 canon + animation tests.  Run:  python3 test_cyto.py   (needs node, xmllint, numpy, pillow, playwright)
Builds the SVGs with SEED=3 into a temp dir, renders the 8s organelle loop frame by frame, and checks it."""
import os, sys, subprocess, tempfile, shutil, io, re, statistics
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
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
