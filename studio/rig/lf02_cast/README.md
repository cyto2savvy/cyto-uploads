# LF02 cast rigs (vector, flat-ink) — source: chars.py (same file as studio/hf/lf02/chars.py)
- `neutro_html(idp, pose, trench)` — Neutro v2: Toronto-police-STYLE officer (navy shirt, peaked cap with black/white checkered band, blank gold badge shapes, shoulder radio, notepad). No text, no crest. Poses idle/cross/notepad/radio/point/ticket/facepalm; `trench=True` overlay for noir. Supersedes the security-guard look in studio/rig/neutro (kept for Ep 13).
- `mito_html(idp, pose, gassed)` — Mito: bean mitochondrion, cristae "abs" in the V-neck, red #6 jersey with white/black trim, headband, high-tops, no logos. Poses idle/hype/ball/dunk/slump/point/shrug; `gassed=True` = towel + sweat.
- `rhino_html(idp, pose)` — Rhino: green spiky cold virus, sunglasses, black hoodie, never speaks. Poses sneak/wave/idle/spread/duck.
- Faces: `face_svg` + `act_js` (expressions smug/shocked/deadpan/hype/exhausted/determined/sideeye/worried, auto blinks, eye darts, nods, squash & stretch pops, pose swaps, lip sync via `mouth_track`).
- Cyto LF02 outfit: studio/rig/outfit_pufferhoodie.png (hoodie + puffer), cup: studio/rig/cup_red2.png (double-stacked face cup).
