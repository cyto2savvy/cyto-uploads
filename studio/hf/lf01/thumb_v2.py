"""LF01 thumbnail v2 (viral): before/after split. DAY 1 (dark, damaged lungs) -> 1 YEAR (glowing healthy lungs), shocked Cyto bridging, Neutro peeking.
No smoking, no products, no smoke plumes. 1280x720, checked at feed sizes."""
import sys, os, math, random, subprocess
sys.path.insert(0, "/home/claude/hf"); sys.path.insert(0, "/home/claude/hf/thumbs"); sys.path.insert(0, "/home/claude/hf/lf01")
import cyto3 as R
from thumb import FACES, ARMS, stage_assets, CH
from neutro import neutro_html, neutro_js
W, H = 1280, 720; INK = "#0c1622"
D = "/home/claude/hf/lf01/thumbs"; stage_assets(D, ("outfit_hoodie",))

def lungs(cx, cy, s, fill, lobe_hi, airway, extra=""):
    Lp = "M-30 -120 Q-150 -140 -190 40 Q-210 190 -110 200 Q-40 205 -30 120Z"
    Rp = "M30 -120 Q150 -140 190 40 Q210 190 110 200 Q40 205 30 120Z"
    br = ("M0 -110 Q-20 -100 -40 -80 Q-80 -40 -100 20 M-60 -60 Q-120 -20 -150 60 M-80 0 Q-90 60 -70 130 "
          "M0 -110 Q20 -100 40 -80 Q80 -40 100 20 M60 -60 Q120 -20 150 60 M80 0 Q90 60 70 130")
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            f'<path d="M0 -235 V-110" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M0 -235 V-110" stroke="{airway}" stroke-width="24" stroke-linecap="round"/>'
            f'<path d="{Lp}" fill="{fill}" stroke="{INK}" stroke-width="10"/><path d="{Rp}" fill="{fill}" stroke="{INK}" stroke-width="10"/>'
            f'<ellipse cx="-120" cy="-30" rx="26" ry="60" fill="{lobe_hi}" opacity=".55" transform="rotate(20 -120 -30)"/>'
            f'<ellipse cx="120" cy="-30" rx="26" ry="60" fill="{lobe_hi}" opacity=".55" transform="rotate(-20 120 -30)"/>'
            f'<path d="{br}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round" opacity=".9"/>'
            f'<path d="{br}" fill="none" stroke="{airway}" stroke-width="8" stroke-linecap="round"/>{extra}</g>')

rnd = random.Random(5)
spots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#1a1416" opacity=".75"/>' for x, y, r in
                [(rnd.choice([-1, 1]) * rnd.uniform(60, 170), rnd.uniform(-90, 180), rnd.uniform(7, 18)) for _ in range(30)])
cracks = "".join(f'<path d="{d}" fill="none" stroke="#ff3b3b" stroke-width="8" stroke-linecap="round"/>' for d in
                 ("M-160 10 L-125 45 L-145 95 L-105 130", "M150 20 L118 58 L140 104 L100 134", "M-80 -60 L-62 -20 L-88 12", "M88 -50 L70 -10 L96 20"))
sick = lungs(300, 395, 1.28, "#6e6468", "#9a8f94", "#5a5055", spots + cracks)
spark = "".join(f'<g transform="translate({x},{y}) scale({s})"><path d="M0 -30 L8 -8 L30 0 L8 8 L0 30 L-8 8 L-30 0 L-8 -8Z" fill="#fff"/></g>'
                for x, y, s in ((-205, -150, 1.1), (210, -120, .9), (-230, 110, .7), (235, 150, 1.0), (0, -175, .6)))
healthy = lungs(985, 395, 1.28, "#ff8fa8", "#ffd3dc", "#ffc1cc", spark)

bg = f'''<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0"><defs>
<radialGradient id="gr" cx=".26" cy=".55" r=".6"><stop offset="0" stop-color="#5a1a1f"/><stop offset="1" stop-color="#120708"/></radialGradient>
<radialGradient id="gg" cx=".77" cy=".55" r=".55"><stop offset="0" stop-color="#7dffcf"/><stop offset=".45" stop-color="#1fb58e"/><stop offset="1" stop-color="#06352d"/></radialGradient>
<clipPath id="cl"><path d="M0 0 H690 L590 720 H0Z"/></clipPath><clipPath id="cr"><path d="M690 0 H1280 V720 H590Z"/></clipPath></defs>
<rect width="{W}" height="{H}" fill="url(#gg)"/>
<g clip-path="url(#cr)">''' + "".join(f'<path d="M985 395 L{985 + 1600 * math.cos(2 * math.pi * i / 28):.0f} {395 + 1600 * math.sin(2 * math.pi * i / 28):.0f} L{985 + 1600 * math.cos(2 * math.pi * (i + 1) / 28):.0f} {395 + 1600 * math.sin(2 * math.pi * (i + 1) / 28):.0f}Z" fill="#ffffff" opacity=".07"/>' for i in range(0, 28, 2)) + f'''</g>
<g clip-path="url(#cl)"><rect width="{W}" height="{H}" fill="url(#gr)"/></g>
<path d="M690 0 L590 720" stroke="#fff" stroke-width="14"/><path d="M690 0 L590 720" stroke="{INK}" stroke-width="5"/>
{sick}{healthy}</svg>'''

def label(x, y, txt, bgc, fg, rot):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg);background:{bgc};color:{fg};font:96px/1 IB;letter-spacing:-2px;'
            f'padding:10px 26px 14px;border:7px solid {INK};border-radius:22px;box-shadow:0 10px 0 {INK};white-space:nowrap">{txt}</div>')
text = label(70, 34, "DAY 1", "#ff3b3b", "#fff", -4) + label(860, 34, "1 YEAR", "#5AE68C", INK, 4)
arrow = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;overflow:visible">'
         f'<path d="M500 205 Q640 120 780 205" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round"/>'
         f'<path d="M500 205 Q640 120 780 205" fill="none" stroke="#FFD166" stroke-width="20" stroke-linecap="round"/>'
         f'<path d="M745 165 L800 215 L728 228Z" fill="#FFD166" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/></svg>')
cx, cy, s = 640, 545, .5
xf = f"translate({cx - 600 * s:.0f}px,{cy - 640 * s:.0f}px) scale({s})"
nt = (f'<div style="position:absolute;left:1015px;top:430px;width:600px;height:720px;transform:scale(.36) rotate(-8deg);transform-origin:0 0;'
      f'filter:drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 -5px 0 #fff)">{neutro_html("nt", "flex")}</div>')
js = (FACES["shock"] + ARMS["point"] + 'gsap.set(["#pupL","#pupR"],{x:7,y:-3});gsap.set("#cyto",{rotation:6});gsap.set("#pom",{rotation:-16});')
html = f"""<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
@font-face{{font-family:IB;src:url(assets/InterDisplay-Black.otf)}} *{{margin:0;padding:0}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
#st{{position:relative;width:{W}px;height:{H}px;overflow:hidden}} {R.rig3_css()}
#cytoPos{{transform:{xf};filter:drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 -7px 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 18px 22px rgba(0,0,0,.6))}}
</style></head><body><div id="st">{bg}{arrow}{nt}{R.rig3_html("outfit_hoodie", "cup_red")}{text}</div>
<script>const VS=["rest","mbp","small","a","e","o","u","fv"];function show(k){{VS.forEach(x=>document.getElementById("v_"+x).setAttribute("opacity",x===k?1:0));}}
gsap.set("#armL",{{svgOrigin:"{R.SH_L[0]} {R.SH_L[1]}"}});gsap.set("#armR",{{svgOrigin:"{R.SH_R[0]} {R.SH_R[1]}"}});gsap.set("#cup",{{svgOrigin:"{R.HAND_L[0]} {R.HAND_L[1]}"}});
gsap.set("#pom",{{svgOrigin:"{R.CX} {R.CY - R.R * 1.12:.0f}"}});gsap.set(["#browL","#browR"],{{transformOrigin:"50% 50%"}});gsap.set("#cyto",{{transformOrigin:"600px 960px"}});{js}
{neutro_js("nt", brows=[(0, "up")], mouths=[(0, "open")]).replace("tl.", "gsap.timeline().")}
</script></body></html>"""
p = f"{D}/thumb-lf01-v2.html"; open(p, "w").write(html)
subprocess.run([CH, "--no-sandbox", "--headless", "--hide-scrollbars", f"--screenshot={D}/thumb-lf01-v2.png", f"--window-size={W},{H}", "--virtual-time-budget=2500", f"file://{p}"], capture_output=True)
# feed check: full, home-feed (~360px), search/sidebar (~168px), with YouTube's duration badge mocked
from PIL import Image, ImageDraw
im = Image.open(f"{D}/thumb-lf01-v2.png").convert("RGB"); bd = im.copy(); d = ImageDraw.Draw(bd)
d.rounded_rectangle((1180, 668, 1268, 708), 6, fill=(0, 0, 0)); d.text((1192, 676), "5:28", fill="white")
S = Image.new("RGB", (1280 + 20, 720 + 230), "#f1f1f1"); S.paste(bd, (10, 10)); S.paste(bd.resize((360, 202)), (10, 740)); S.paste(bd.resize((168, 94)), (400, 740))
S.save(f"{D}/feed_check_v2.jpg", quality=88); print("ok")
