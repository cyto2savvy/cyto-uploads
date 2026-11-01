"""Cyto thumbnail system (v1, Nov 2026). One fixed structure for every Short so the channel is recognisable
and every thumbnail reads at phone-feed size (~170 px wide).

THE STRUCTURE (1080x1920)
  y   0-180   breathing room (nothing important)
  y 225-290   SERIES PILL - small, same spot every episode (brand recognition)
  y 300-660   HEADLINE - max 4 words / 2 lines, InterDisplay Black ~170px, white + ONE gold word,
              thick ink stroke + hard drop shadow. Must ADD to the title, never repeat it.
  y 620-1400  HERO (shift with hero_dy) - one big object that asks the question (a phone at 3:00, a heart at 114 BPM...).
              Bright, glowing, the most saturated thing on the canvas.
  y 980-1625  CYTO - huge (scale ~0.88), reacting (shock / skeptic / hype), looking AT the hero,
              cup visible, white rim light so he pops off the background.
  y 1640-1920 YouTube's title/UI overlays this - background only.
  Feed crops: everything that matters sits inside the centre 1080x1350 (y 285-1635), so the 4:5 crop
  and the small grid tile still show headline + hero + face.
  Background: flat brand gradient + light rays from the hero + vignette. Never a busy photo, never a fact card.

Usage: python3 thumb.py <spec.json> <out_dir>   (spec: see ep08 spec in studio/hf/ep08/thumbs.json)
"""
import os, sys, json, shutil, subprocess, math
sys.path.insert(0, "/home/claude/hf")
import cyto3 as R

W, H = 1080, 1920
NAVY, INK, CREAM, GOLD, CORAL, TEAL = "#0c1622", "#0c1622", "#FAF4E8", "#FFD166", "#FF7A59", "#3fc1b0"
CH = subprocess.run("ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | head -1",
                    shell=True, capture_output=True, text=True).stdout.strip()

FACES = {   # static reaction faces (same element ids as the animated rig)
    "shock":   'gsap.set(["#lidL","#lidR"],{y:%d});gsap.set(["#browL","#browR"],{y:-20});gsap.set(["#pupL","#pupR"],{scale:.78,transformOrigin:"50%% 50%%"});show("o");' % R.LID_WIDE,
    "skeptic": 'gsap.set("#browL",{y:-16,rotation:-12});gsap.set("#browR",{y:8,rotation:10});gsap.set("#lidR",{y:%d});show("mbp");' % R.LID_SQUINT,
    "hype":    'gsap.set(["#browL","#browR"],{y:-14});gsap.set(["#lidL","#lidR"],{y:-30});show("a");',
    "tired":   'gsap.set(["#lidL","#lidR"],{y:22});gsap.set("#browL",{rotation:10,y:-2});gsap.set("#browR",{rotation:-10,y:-2});show("small");',
}
ARMS = {
    "point": 'gsap.set("#armR",{rotation:-124});',
    "shrug": 'gsap.set("#armR",{rotation:-62});',
    "raise": 'gsap.set("#armL",{rotation:-30});gsap.set("#cup",{rotation:30});',
    "none": "",
}


def rays(cx, cy, n=22, c1="#14233a", c2="#1b2f4c"):
    out = [f'<rect width="{W}" height="{H}" fill="{c1}"/>']
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        L = 2600
        out.append(f'<path d="M{cx} {cy} L{cx + L * math.cos(a0):.0f} {cy + L * math.sin(a0):.0f} L{cx + L * math.cos(a1):.0f} {cy + L * math.sin(a1):.0f}Z" fill="{c2}"/>')
    return "".join(out)


def page(spec, assets_rel="assets"):
    g = spec.get("glow", "#3a6fd8")
    hx, hy = spec.get("hero_xy", [640, 990])
    bg = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0"><defs>'
          f'<radialGradient id="glow" cx="{hx / W:.3f}" cy="{hy / H:.3f}" r=".55"><stop offset="0" stop-color="{g}" stop-opacity=".95"/>'
          f'<stop offset=".45" stop-color="{g}" stop-opacity=".25"/><stop offset="1" stop-color="{g}" stop-opacity="0"/></radialGradient>'
          f'<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>'
          f'<linearGradient id="foot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05090f" stop-opacity="0"/><stop offset="1" stop-color="#05090f" stop-opacity=".85"/></linearGradient></defs>'
          f'{rays(hx, hy, c1=spec.get("bg1", "#101d31"), c2=spec.get("bg2", "#172a45"))}'
          f'<rect width="{W}" height="{H}" fill="url(#glow)"/><rect width="{W}" height="{H}" fill="url(#vig)"/>'
          f'<rect y="1560" width="{W}" height="360" fill="url(#foot)"/></svg>')
    cx, cy, s = spec.get("cyto", [430, 1370, 0.88])
    xf = f"translate({cx - 600 * s:.0f}px,{cy - 640 * s:.0f}px) scale({s})"
    l1, l2 = spec["headline"]
    hot = spec.get("hot", "")
    def hl(t): return t.replace(hot, f'<span style="color:{GOLD}">{hot}</span>') if hot else t
    head = (f'<div class="pill">{spec["series"]}</div>'
            f'<div class="hl" style="font-size:{spec.get("hl_size", 172)}px"><div>{hl(l1)}</div><div>{hl(l2)}</div></div>')
    pupils = spec.get("look", [12, -10])
    js = (FACES[spec.get("face", "shock")] + ARMS[spec.get("arm", "point")] +
          f'gsap.set(["#pupL","#pupR"],{{x:{pupils[0]},y:{pupils[1]}}});gsap.set("#pom",{{rotation:{spec.get("pom", -14)}}});'
          f'gsap.set("#cyto",{{rotation:{spec.get("tilt", -4)}}});')
    return f"""<!doctype html><html><head><meta charset="utf-8"><script src="{assets_rel}/gsap.min.js"></script><style>
@font-face{{font-family:IB;src:url({assets_rel}/InterDisplay-Black.otf)}}@font-face{{font-family:IX;src:url({assets_rel}/Inter-ExtraBold.otf)}}
*{{margin:0;padding:0}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{NAVY}}}
#stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
{R.rig3_css()}
#cytoPos{{transform:{xf}}}
#cytoPos{{filter:drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 -7px 0 #fff) drop-shadow(0 28px 30px rgba(0,0,0,.55))}}
.pill{{position:absolute;top:225px;left:50%;transform:translateX(-50%);background:{GOLD};color:{INK};font:38px IB;letter-spacing:.04em;
  padding:12px 30px;border-radius:40px;white-space:nowrap;border:5px solid {INK};box-shadow:0 6px 0 {INK}}}
.hl{{position:absolute;top:305px;left:0;width:{W}px;text-align:center;font-family:IB;color:#fff;line-height:.93;letter-spacing:-2px;
  transform:rotate({spec.get("hl_rot", -3)}deg);paint-order:stroke fill;-webkit-text-stroke:22px {INK};
  text-shadow:0 14px 0 {INK},0 22px 30px rgba(0,0,0,.5)}}
.hero{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}
</style></head><body><div id="stage">{bg}<div class="hero" style="transform:translateY({spec.get("hero_dy", 60)}px)">{spec["hero_svg"]}</div>
{R.rig3_html(spec.get("outfit"), spec.get("cup", "cup_red"), spec.get("acc"))}{head}</div>
<script>
const VS=["rest","mbp","small","a","e","o","u","fv"];function show(k){{VS.forEach(v=>document.getElementById("v_"+v).setAttribute("opacity",v===k?1:0));}}
gsap.set("#armL",{{svgOrigin:"{R.SH_L[0]} {R.SH_L[1]}"}});gsap.set("#armR",{{svgOrigin:"{R.SH_R[0]} {R.SH_R[1]}"}});
gsap.set("#cup",{{svgOrigin:"{R.HAND_L[0]} {R.HAND_L[1]}"}});gsap.set("#pom",{{svgOrigin:"{R.CX} {R.CY - R.R * 1.12:.0f}"}});
gsap.set(["#browL","#browR"],{{transformOrigin:"50% 50%"}});gsap.set("#cyto",{{transformOrigin:"600px 960px"}});
{js}
</script></body></html>"""


def stage_assets(d, outfits=()):
    a = os.path.join(d, "assets"); os.makedirs(a, exist_ok=True)
    for f in ("cup_red.png", "cup_orange.png", "cup_blue.png", *[o + ".png" for o in outfits]):
        p = f"/home/claude/cyto2/rig/{f}"
        if os.path.exists(p): shutil.copy(p, a)
    for f in ("InterDisplay-Black.otf", "Inter-ExtraBold.otf", "Inter-SemiBold.otf"):
        shutil.copy(f"/usr/share/fonts/opentype/inter/{f}", a)
    shutil.copy("/home/claude/hf/node_modules/gsap/dist/gsap.min.js", a)


def shoot(html_path, png_path, w=W, h=H, transparent=False):
    args = [CH, "--no-sandbox", "--headless", "--hide-scrollbars", f"--screenshot={png_path}", f"--window-size={w},{h}", "--virtual-time-budget=2500"]
    if transparent: args.append("--default-background-color=00000000")
    subprocess.run(args + [f"file://{html_path}"], capture_output=True)


def feed_check(pngs, out):
    """How they look where people actually decide: full-size, 4:5 feed crop, and phone-grid size (~170px)."""
    from PIL import Image, ImageDraw
    cols = []
    for p in pngs:
        im = Image.open(p).convert("RGB")
        full = im.resize((360, 640))
        crop = im.crop((0, 285, 1080, 1635)).resize((360, 450))
        tiny = im.resize((170, 302))
        c = Image.new("RGB", (380, 640 + 450 + 302 + 60), "#e9e9e9"); c.paste(full, (10, 10)); c.paste(crop, (10, 670)); c.paste(tiny, (105, 1140))
        cols.append(c)
    sheet = Image.new("RGB", (380 * len(cols), cols[0].height), "#e9e9e9")
    for i, c in enumerate(cols): sheet.paste(c, (380 * i, 0))
    sheet.save(out, quality=88)


if __name__ == "__main__":
    spec_file, out = sys.argv[1], sys.argv[2]
    specs = json.load(open(spec_file)); os.makedirs(out, exist_ok=True)
    stage_assets(out, [s.get(k) for s in specs.values() for k in ("outfit", "acc") if s.get(k)])
    made = []
    for name, spec in specs.items():
        hp = os.path.join(out, f"{name}.html"); open(hp, "w").write(page(spec))
        shoot(hp, os.path.join(out, f"{name}.png")); made.append(os.path.join(out, f"{name}.png"))
    feed_check(made, os.path.join(out, "feed_check.jpg"))
    print(made)
