import sys; sys.path.insert(0, "/home/claude/hf/lf02")
from lib import *
S = Scene("lineup", 0, 4.0)
S.add('<div class="fill" style="background:radial-gradient(ellipse at 50% 40%,#24406a,#0c1622 75%)"></div>'
      '<div style="position:absolute;left:0;right:0;top:860px;height:220px;background:#132238"></div>')
S.cyto(330, 600, .5, expr=[], x_expr=[(0, 1, "smug"), (1, 1, "shocked"), (2, 1, "deadpan"), (3, 1, "hype")])
ex = [(0, 1, "deadpan"), (1, 1, "shocked"), (2, 1, "sideeye"), (3, 1, "determined")]
S.char("neutro", "nt", 560, 300, .82, pose="notepad", expr=ex, blinks=[], bob=False)
S.char("mito", "mt", 1060, 280, .78, pose="hype", expr=[(0, 1, "hype"), (1, 1, "shocked"), (2, 1, "exhausted"), (3, 1, "smug")], blinks=[], bob=False)
S.char("rhino", "rh", 1530, 520, .9, pose="sneak", expr=[(0, 1, "smug"), (1, 1, "shocked"), (2, 1, "sideeye"), (3, 1, "determined")], blinks=[], bob=False)
S.over('<div style="position:absolute;left:0;right:0;top:40px;text-align:center;font:54px InterBlack;color:#FFD166">LF02 CAST</div>')
for x, n in ((330, "CYTO"), (820, "NEUTRO"), (1300, "MITO"), (1700, "RHINO")):
    S.over(f'<div style="position:absolute;left:{x - 150}px;width:300px;top:960px;text-align:center;font:40px InterBlack;color:#FAF4E8">{n}</div>')
S.build()
