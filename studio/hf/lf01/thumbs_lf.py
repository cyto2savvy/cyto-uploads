"""LF01 thumbnails, 1280x720 landscape. Countdown clock hero '20 MIN -> 1 YR', Cyto big + Neutro peeking. Max 3 words on image."""
import sys, os, math, subprocess
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/hf/thumbs"); sys.path.insert(0, "/home/claude/hf/lf01")
import cyto3 as R
from thumb import FACES, ARMS, stage_assets, CH
from neutro import neutro_html, neutro_js
import lfart as L
W, H = 1280, 720; INK, GOLD, CREAM, CORAL, GREEN = "#0c1622", "#FFD166", "#FAF4E8", "#FF7A59", "#5AE68C"
D = "/home/claude/hf/lf01/thumbs"; stage_assets(D, ("outfit_hoodie",))
def rays(cx, cy, c1, c2, n=24):
    o = [f'<rect width="{W}" height="{H}" fill="{c1}"/>']
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        o.append(f'<path d="M{cx} {cy} L{cx + 2000 * math.cos(a0):.0f} {cy + 2000 * math.sin(a0):.0f} L{cx + 2000 * math.cos(a1):.0f} {cy + 2000 * math.sin(a1):.0f}Z" fill="{c2}"/>')
    return "".join(o)
def page(v):
    cx, cy, s = v["cyto"]
    xf = f"translate({cx - 600 * s:.0f}px,{cy - 640 * s:.0f}px) scale({s})"
    hx, hy = v["hero_xy"]
    bg = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0"><defs><radialGradient id="gl" cx="{hx / W:.2f}" cy="{hy / H:.2f}" r=".5">'
          f'<stop offset="0" stop-color="{v["glow"]}" stop-opacity=".9"/><stop offset="1" stop-color="{v["glow"]}" stop-opacity="0"/></radialGradient>'
          f'<radialGradient id="vg" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".65"/></radialGradient></defs>'
          f'{rays(hx, hy, v["bg1"], v["bg2"])}<rect width="{W}" height="{H}" fill="url(#gl)"/><rect width="{W}" height="{H}" fill="url(#vg)"/></svg>')
    js = (FACES[v["face"]] + ARMS[v["arm"]] + f'gsap.set(["#pupL","#pupR"],{{x:{v["look"][0]},y:{v["look"][1]}}});gsap.set("#cyto",{{rotation:{v["tilt"]}}});')
    nt = (f'<div style="position:absolute;left:{v["nt"][0]}px;top:{v["nt"][1]}px;width:600px;height:720px;transform:scale({v["nt"][2]}) rotate({v["nt"][3]}deg);transform-origin:0 0;'
          f'filter:drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 -5px 0 #fff)">{neutro_html("nt", "cross")}</div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
@font-face{{font-family:IB;src:url(assets/InterDisplay-Black.otf)}}@font-face{{font-family:InterBlack;src:url(assets/InterDisplay-Black.otf)}} *{{margin:0;padding:0}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
#st{{position:relative;width:{W}px;height:{H}px;overflow:hidden}} {R.rig3_css()} #cytoPos{{transform:{xf};filter:drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff) drop-shadow(0 -6px 0 #fff) drop-shadow(0 20px 24px rgba(0,0,0,.5))}}
.hl{{position:absolute;font-family:IB;color:#fff;line-height:.9;letter-spacing:-2px;paint-order:stroke fill;-webkit-text-stroke:16px {INK};text-shadow:0 10px 0 {INK};white-space:nowrap}}
</style></head><body><div id="st">{bg}<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">{v["hero"]}</svg>{nt}{R.rig3_html("outfit_hoodie", "cup_red")}{v["text"]}</div>
<script>const VS=["rest","mbp","small","a","e","o","u","fv"];function show(k){{VS.forEach(x=>document.getElementById("v_"+x).setAttribute("opacity",x===k?1:0));}}
gsap.set("#armL",{{svgOrigin:"{R.SH_L[0]} {R.SH_L[1]}"}});gsap.set("#armR",{{svgOrigin:"{R.SH_R[0]} {R.SH_R[1]}"}});gsap.set("#cup",{{svgOrigin:"{R.HAND_L[0]} {R.HAND_L[1]}"}});
gsap.set(["#browL","#browR"],{{transformOrigin:"50% 50%"}});gsap.set("#cyto",{{transformOrigin:"600px 960px"}});{js}
{neutro_js("nt", brows=[(0, "up")], mouths=[(0, "smirk")]).replace("tl.", "gsap.timeline().")}
</script></body></html>"""
CLOCK = L.clock(0, 0, 200, "ck", "20 MIN")
V = {
 "A": dict(cyto=[285, 480, .6], face="shock", arm="point", look=[7, -4], tilt=-5, nt=[1010, 420, .45, -12], glow="#FFD166", bg1="#14233a", bg2="#1d3354", hero_xy=[820, 400],
           hero=f'<g transform="translate(820,410) rotate(-6)">{CLOCK}</g>',
           text=f'<div class="hl" style="left:500px;top:34px;font-size:100px;transform:rotate(-3deg)">20 MIN <span style="color:{GOLD}">→ 1 YR</span></div>'),
 "B": dict(cyto=[1010, 470, .6], face="hype", arm="raise", look=[-7, -4], tilt=5, nt=[-40, 440, .42, 10], glow="#5AE68C", bg1="#13262a", bg2="#1c3a3c", hero_xy=[470, 360],
           hero=(f'<g transform="translate(330,370) scale(.82)">{CLOCK}</g>'
                 f'<path d="M520 370 H640" stroke="#fff" stroke-width="22" stroke-linecap="round"/><path d="M610 330 L660 370 L610 410" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
                 + L.heart(780, 380, 1.55, "hb", "#e8455a")),
           text=f'<div class="hl" style="left:700px;top:330px;width:160px;text-align:center;font-size:84px;-webkit-text-stroke:10px {INK}">1 YR</div>'),
}
for k, v in V.items():
    p = f"{D}/thumb-lf01-{k}.html"; open(p, "w").write(page(v))
    subprocess.run([CH, "--no-sandbox", "--headless", "--hide-scrollbars", f"--screenshot={D}/thumb-lf01-{k}.png", f"--window-size={W},{H}", "--virtual-time-budget=2500", f"file://{p}"], capture_output=True)
    print(k, os.path.getsize(f"{D}/thumb-lf01-{k}.png"))
