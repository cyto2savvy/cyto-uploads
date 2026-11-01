"""Channel branding in the v3 style: profile picture, banner, watermark.
Vector Cyto (hf/cyto3.py) posed with GSAP, over a flat illustrated Toronto skyline. python3 brand.py -> out/*.png"""
import os, sys, shutil, subprocess, random, json
sys.path.insert(0, "/home/claude/hf")
import cyto3 as R

D = "/home/claude/hf/branding"; os.chdir(D)
os.makedirs("assets", exist_ok=True); os.makedirs("out", exist_ok=True)
for f in ("cup_red.png",): shutil.copy(f"/home/claude/cyto2/rig/{f}", "assets")
for f in ("InterDisplay-Black.otf", "Inter-ExtraBold.otf", "Inter-SemiBold.otf"): shutil.copy(f"/usr/share/fonts/opentype/inter/{f}", "assets")
shutil.copy("/home/claude/hf/node_modules/gsap/dist/gsap.min.js", "assets")
CH = subprocess.run("ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | head -1",
                    shell=True, capture_output=True, text=True).stdout.strip()

NAVY, NAVY2, INK, CREAM, GOLD, CORAL, TEAL = "#0c1622", "#17304d", "#0c1622", "#FAF4E8", "#FFD166", "#FF7A59", "#3fc1b0"


def skyline(W, H, base, scale=1.0, seed=4, lit=.35, cn=None):
    """Flat cutout Toronto skyline: CN Tower, the dome, condo towers with lit windows. Returns SVG markup."""
    rnd = random.Random(seed); s = scale; out = []
    cn = W * .5 if cn is None else cn
    # back row of towers
    x = -20
    while x < W:
        w = rnd.uniform(70, 150) * s; h = rnd.uniform(140, 380) * s
        out.append(f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#13263d"/>')
        x += w + rnd.uniform(4, 18) * s
    # dome
    out.append(f'<path d="M{cn + 150 * s:.0f} {base} A{150 * s:.0f} {95 * s:.0f} 0 0 1 {cn + 450 * s:.0f} {base} Z" fill="#1a3150" stroke="{INK}" stroke-width="{5 * s:.0f}"/>')
    for k in range(1, 5):
        out.append(f'<path d="M{cn + 300 * s:.0f} {base - 95 * s:.0f} L{cn + 150 * s + k * 60 * s:.0f} {base}" stroke="#2a4866" stroke-width="{4 * s:.0f}"/>')
    # CN Tower
    sh = 860 * s; pod_y = base - sh * .62
    out.append(f'<path d="M{cn - 34 * s:.0f} {base} L{cn - 12 * s:.0f} {base - sh * .9:.0f} L{cn + 12 * s:.0f} {base - sh * .9:.0f} L{cn + 34 * s:.0f} {base} Z" fill="#1c3656" stroke="{INK}" stroke-width="{6 * s:.0f}"/>')
    out.append(f'<rect x="{cn - 4 * s:.0f}" y="{base - sh:.0f}" width="{8 * s:.0f}" height="{sh * .12:.0f}" fill="#1c3656" stroke="{INK}" stroke-width="{4 * s:.0f}"/>')
    out.append(f'<ellipse cx="{cn}" cy="{pod_y:.0f}" rx="{62 * s:.0f}" ry="{30 * s:.0f}" fill="#22406a" stroke="{INK}" stroke-width="{6 * s:.0f}"/>')
    out.append(f'<rect x="{cn - 56 * s:.0f}" y="{pod_y - 6 * s:.0f}" width="{112 * s:.0f}" height="{10 * s:.0f}" fill="{GOLD}" opacity=".85"/>')
    out.append(f'<ellipse cx="{cn}" cy="{base - sh * .78:.0f}" rx="{20 * s:.0f}" ry="{11 * s:.0f}" fill="#22406a" stroke="{INK}" stroke-width="{4 * s:.0f}"/>')
    out.append(f'<circle cx="{cn}" cy="{base - sh:.0f}" r="{7 * s:.0f}" fill="{CORAL}"/>')
    # front row: condos with windows
    x = -10
    while x < W:
        w = rnd.uniform(90, 190) * s; h = rnd.uniform(90, 300) * s
        if abs(x + w / 2 - cn) < 70 * s: x += 80 * s; continue
        out.append(f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h + 4:.0f}" fill="#1a3150" stroke="{INK}" stroke-width="{5 * s:.0f}"/>')
        for wy in range(int(base - h + 18 * s), int(base - 12 * s), int(26 * s)):
            for wx in range(int(x + 14 * s), int(x + w - 18 * s), int(26 * s)):
                if rnd.random() < lit:
                    out.append(f'<rect x="{wx}" y="{wy}" width="{12 * s:.0f}" height="{14 * s:.0f}" fill="{GOLD}" opacity="{rnd.uniform(.55, .95):.2f}"/>')
        x += w + rnd.uniform(0, 10) * s
    out.append(f'<rect x="0" y="{base}" width="{W}" height="{H - base}" fill="{NAVY}"/>')
    return "".join(out)


def stars(W, H, n, seed=1):
    rnd = random.Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H * .55):.0f}" r="{rnd.choice((2, 2, 3, 4))}" fill="{CREAM}" opacity="{rnd.uniform(.25, .7):.2f}"/>' for _ in range(n))


POSES = {   # static poses applied with gsap.set (same element IDs the animation uses)
    "cheers": 'gsap.set("#armL",{rotation:-30});gsap.set("#cup",{rotation:30});gsap.set(["#browL","#browR"],{y:-10});'
              'gsap.set(["#lidL","#lidR"],{y:-20});gsap.set("#pupL",{x:4});gsap.set("#pupR",{x:4});show("e");',
    "grin":   'gsap.set(["#browL","#browR"],{y:-10});gsap.set(["#lidL","#lidR"],{y:-22});gsap.set("#pom",{rotation:10});show("a");',
    "wave":   'gsap.set("#armR",{rotation:-122});gsap.set(["#browL","#browR"],{y:-12});gsap.set(["#lidL","#lidR"],{y:-24});show("a");',
    "chill":  'gsap.set("#browL",{y:-8,rotation:-6});gsap.set("#browR",{y:2,rotation:6});gsap.set("#pom",{rotation:-8});show("rest");',
}


def page(W, H, bg, cyto_xform, pose, extra="", transparent=False):
    return f"""<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
@font-face{{font-family:IB;src:url(assets/InterDisplay-Black.otf)}}@font-face{{font-family:IX;src:url(assets/Inter-ExtraBold.otf)}}@font-face{{font-family:IS;src:url(assets/Inter-SemiBold.otf)}}
*{{margin:0;padding:0}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{'transparent' if transparent else NAVY}}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
{R.rig3_css()}
#cytoPos{{transform:{cyto_xform}}}
</style></head><body><div id="stage">{bg}{R.rig3_html(None, "cup_red")}{extra}</div>
<script>
const VS=["rest","mbp","small","a","e","o","u","fv"];function show(k){{VS.forEach(v=>document.getElementById("v_"+v).setAttribute("opacity",v===k?1:0));}}
gsap.set("#armL",{{svgOrigin:"{R.SH_L[0]} {R.SH_L[1]}"}});gsap.set("#armR",{{svgOrigin:"{R.SH_R[0]} {R.SH_R[1]}"}});
gsap.set("#cup",{{svgOrigin:"{R.HAND_L[0]} {R.HAND_L[1]}"}});gsap.set("#pom",{{svgOrigin:"{R.CX} {R.CY - R.R * 1.12:.0f}"}});
gsap.set(["#browL","#browR"],{{transformOrigin:"50% 50%"}});gsap.set(["#nuc","#mito"],{{transformOrigin:"50% 50%"}});
{POSES[pose]}
</script></body></html>"""


def shoot(name, html, W, H, transparent=False):
    open(f"{name}.html", "w").write(html)
    args = [CH, "--no-sandbox", "--headless", "--hide-scrollbars", f"--screenshot=out/{name}.png", f"--window-size={W},{H}", "--virtual-time-budget=2000"]
    if transparent: args.append("--default-background-color=00000000")
    subprocess.run(args + [f"file://{D}/{name}.html"], capture_output=True)


def cyto_at(cx, cy, s):   # put body centre (600,640) at (cx,cy)
    return f"translate({cx - 600 * s:.0f}px,{cy - 640 * s:.0f}px) scale({s})"


# ---------------- profile picture 800x800 (YouTube crops to a circle; shown as small as 24px)
W = H = 800
bg = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">'
      f'<defs><radialGradient id="g" cx=".5" cy=".38" r=".7"><stop offset="0" stop-color="#22487a"/><stop offset="1" stop-color="{NAVY}"/></radialGradient></defs>'
      f'<rect width="{W}" height="{H}" fill="url(#g)"/>{stars(W, H, 26, 2)}{skyline(W, H, 760, .62, seed=9, lit=.3)}</svg>')
ring = f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0"><circle cx="400" cy="400" r="384" fill="none" stroke="{GOLD}" stroke-width="26"/></svg>'
for name, pose in (("profile-grin", "grin"), ("profile-chill", "chill")):
    shoot(name, page(W, H, bg, cyto_at(415, 470, 0.80), pose, ring), W, H)

# ---------------- banner 2560x1440 (safe area for all devices: centred 1546x423)
W, H = 2560, 1440
sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
bg = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">'
      f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f2236"/><stop offset=".55" stop-color="#22487a"/><stop offset="1" stop-color="#2d5a8f"/></linearGradient></defs>'
      f'<rect width="{W}" height="{H}" fill="url(#g)"/>{stars(W, H, 90, 5)}{skyline(W, H, 1230, 1.0, seed=4, lit=.32, cn=sx0 + 1546 + 170)}</svg>')
text = f"""
<div style="position:absolute;left:{sx0 + 470}px;top:{sy0 + 40}px;width:1060px;font-family:IB;color:{CREAM};line-height:.95">
  <div style="font-size:104px;letter-spacing:-1px;text-shadow:0 8px 0 rgba(0,0,0,.35)">THE BODY IS THE <span style="color:{GOLD}">6IX</span></div>
  <div style="font:42px/1.25 IX;margin-top:26px;color:{CREAM}">Your body, explained by a cell from the 6ix.</div>
  <div style="margin-top:30px;display:flex;gap:18px"><span style="background:{CORAL};color:{INK};font:30px IB;letter-spacing:.03em;padding:14px 26px;border-radius:40px;white-space:nowrap">NEW SHORTS EVERY DAY</span>
  <span style="background:{TEAL};color:{INK};font:30px IB;letter-spacing:.03em;padding:14px 26px;border-radius:40px;white-space:nowrap">REAL SCIENCE · TORONTO STYLE</span></div>
</div>"""
shoot("banner", page(W, H, bg, cyto_at(sx0 + 215, sy0 + 236, 0.5), "wave", text), W, H)

# safe-area check image
from PIL import Image, ImageDraw
im = Image.open("out/banner.png").convert("RGB"); d = ImageDraw.Draw(im)
d.rectangle([sx0, sy0, sx0 + 1546, sy0 + 423], outline=(255, 0, 255), width=6)                      # all devices
d.rectangle([(W - 2560) // 2, (H - 423) // 2, W, (H + 423) // 2], outline=(0, 255, 0), width=4)    # desktop max
im.resize((1280, 720)).save("out/banner_safecheck.jpg", quality=85)

# ---------------- watermark 150x150 transparent (bottom-right of every video)
W = H = 600
shoot("watermark_big", page(W, H, "", cyto_at(310, 360, 0.72), "grin", "", transparent=True), W, H, transparent=True)
Image.open("out/watermark_big.png").resize((150, 150), Image.LANCZOS).save("out/watermark-150.png")

# final sizes
Image.open("out/profile-grin.png").save("out/channel-profile-800.png")
print(json.dumps({f: Image.open(f"out/{f}").size for f in sorted(os.listdir("out")) if f.endswith(".png")}))
