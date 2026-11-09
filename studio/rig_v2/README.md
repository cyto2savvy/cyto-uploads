# rig_v2 — canon v2 video rig (Nov 9, 2026)
Drives Cyto (`../branding/rebrand-v2/cyto2d.js`) with a timeline, frame by frame -> transparent PNG sequence + `cyto.webm` (VP9 alpha).
```
node studio/rig_v2/render_rig.js timeline.json outDir 1080 [startSec endSec]     # SEED=3 default
python3 -I studio/rig_v2/test_rig.py                                              # 15 checks, must pass
```
**timeline.json**: `{fps:30,duration:<s>,fit:none|jersey|hoodie|puffer,seed:7,words:[{w,start,end}],beats:[{t,emotion,gaze?:[x,y]}]}`
- `words` = ElevenLabs/Scribe word timings -> mouth shape per syllable (small/wide/o cycle every 85 ms).
- `beats` = one entry at EVERY sentence/idea change (at least every 2-3 s): `emotion` = chill | happy | shock | think | solemn | laugh. Reactions pop the brows, tilt the head and can pin the gaze (`gaze:[0,0]` = look at camera, `[-.8,-.6]` = up-left thinking).
- Automatic life: blink every 2-4 s, gaze saccade every ~1-2.5 s (40% back to camera), idle bounce, head sway, cup sways with steam rising, organelles drift.
- The cup is ALWAYS in his hand. Never set it down.
**Composite**: overlay `cyto.webm` (or the PNGs) on the scene backgrounds with ffmpeg / HyperFrames, scale ~0.6-1.0, bottom-centre or left third; add the sticker outline in the scene layer if needed. Camera moves (push-in, punch-zoom) are done on the composite, not on the rig.
`example_timeline.json` is a working 4 s sample.
