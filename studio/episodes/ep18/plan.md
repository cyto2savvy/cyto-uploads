# Ep 18 plan: "Why Your Heart Doesn't Tire Like Your Bicep" (IDEA chat, Nov 14, 2026)
Status: written by the IDEA chat, awaiting Utsha's OK (gate 1). Nothing rendered, 0 credits spent. Series: 6ix Seconds of Science. Slot: Mon Nov 16 6 PM ET (2026-11-16T23:00:00Z). CHECK: Utsha wrote 'Sun Nov 16' but Nov 16, 2026 is a Monday..
Claims/sources: `claims.md`. Spec: `episode.json`. Voice: 1 take (episode.json `voice.takes = 1`).

## Why this topic (rule 26)
Passes the topic gate (body fact leads; Toronto is flavour). See claims.md for the trend hook and what each claim rests on.

## Script
1. [hook] Your heart works all day without a break. So why does flexing your bicep burn?
2. A third of each heart cell is mitochondria, tiny power plants running nonstop, fam.
3. Your bicep isn't built for nonstop. Heart's the 504 streetcar, bicep's a weekend closure, styll.
4. [outro] Not medical advice. Send this to the one who does the bicep heart. Yo, it's ya boy Cyto!

## Scene table
| # | Backdrop / transition | Props (anchor word) | New this episode |
|---|---|---|---|
| 0 | gym / zoom (instant) | ecgLine @"heart"; bicepHeart @"bicep" | gym (bg), ecgLine, bicepHeart |
| 1 | chestcavity / membrane | cellSlice heartCell 1/3 @"third" | chestcavity (bg), cellSlice |
| 2 | subway / whip | fatigueMeter HEART vs BICEP @"bicep's" | fatigueMeter |
| 3 | gym / doors (outro, clean) | none: headline + card + sources | loop back to scene 0 |
New-element share: 3 of 4 scenes (75%).

## New library items for the sprint (rule 25: add to backdrops.js / props.js / LIBRARY.md / library.png the same day)
- `gym` (backdrop): weight room, dumbbell rack on the far wall, mirror wall, rubber floor, bench silhouette. Mito may cameo (silent). No brands, no signage text.
- `chestcavity` (backdrop): ribcage arches in parallax, warm red-pink interior, beating heart silhouette in the far layer.
- `ecgLine` (prop): ECG trace that draws on left to right with a recurring spike and a small heart-blip.
- `bicepHeart` (prop): cut-out flexed arm (fist up); the other hand presses the inside of the bicep and the arm outline pops into a heart shape.
- `cellSlice` (prop, kind `heartCell`): big rounded muscle-cell cross-section, bean-shaped mitochondria fill in until they cover `fill_share` (0.33) of the cell; label chip.
- `fatigueMeter` (prop): two vertical gauges (HEART, BICEP). Heart stays low/steady; bicep fills red. `show_numbers: false`: no numerals.
`make_episode.py` validates `bg` against a fixed list. The new backdrop ids above must be registered (BGS in make_episode.py + backdrops.js) before `--dry-run --stage validate` passes; with them registered the spec validates with 0 errors and 0 warnings.

## Rules checklist
- Rule 22 (22-26 s, loop): word-estimate ~22 s of speech, plus pauses and the outro ~24-25 s; last scene's backdrop = scene 0's backdrop; BUILD must make the last frame match the first (same Cyto pose).
- Rule 23 (intro + catchphrase): stat stamp slams in first (the 1/3 stamp is revealed in scene 1; scene 0 opens on the ECG + hook headline at frame 1). Rule 23 asks for a pattern none of the last 3 episodes used; no `intro:` entries exist yet, so log `intro:stat-stamp`. Catchphrase: 1.3 s stinger at the very end over the outro (shortened: 'Yo, it's ya boy Cyto!'), well after 6 s.
- Rule 24 (one ask, a send): spoken in the last scene AND on screen (headline + 'WHO'S YOURS?' card). Pinned comment posted the hour it goes public.
- Rule 21: every prop has `shows` + `anchor`; catchphrase/outro scenes have none.
- Rule 25: new backdrops + props listed above; at least 75% of scenes carry a first-appearance element.
- Cup: canon v2 paper coffee cup with steam. Nothing about drinking. No real brands.

## Thumbnails
See episode.json: A/B, `stronger` named. Vertical 1080x1920 first.

## Costs
Idea $0. ElevenLabs: see the voice estimate in the validator output (1 take). BUILD asks before spending credits.
