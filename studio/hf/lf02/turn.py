"""rig turnaround test scene (not part of the episode): Mito relaxed / grip-ball / fist-pump, Neutro poses, Cyto gestures."""
import sys; sys.path.insert(0, "/home/claude/hf/lf02")
from lib import *
S = Scene("turn", 400, 403.6, bg="#2b1640"); S.case = False
S.add('<div class="fill" style="background:linear-gradient(#3a2a5a,#1d1838)"></div><div style="position:absolute;left:0;right:0;top:860px;bottom:0;background:#2f6f8f"></div>')
S.char("mito", "mt", 60, 250, .8, pose="idle", who="MITO", poses=[(1.2, "ball"), (2.4, "hype")], ball=[(1.2, 2.4, "held")], blinks=[])
S.char("neutro", "nt", 620, 260, .8, pose="idle", who="NEUTRO", poses=[(1.2, "notepad"), (2.4, "radio")], blinks=[])
S.cyto(1560, 640, .5, phone=True, points=[(1.2, 1.0)], sips=[(2.4, 1.1)], blinks=[])
S.talk_scale = 0
S.build(); print("ok", S.mv.n)
