# Ep 20 plan: "Why Do Freezing Fingers Suddenly Warm Up?" (IDEA chat, Nov 14, 2026)
Status: written by the IDEA chat, awaiting Utsha's OK (gate 1). Nothing rendered, 0 credits spent. Series: What happens to your body when.... Slot: Wed Nov 18 6 PM ET (2026-11-18T23:00:00Z).
Claims/sources: `claims.md`. Spec: `episode.json`. Voice: 1 take (episode.json `voice.takes = 1`).

## Why this topic (rule 26)
Passes the topic gate (body fact leads; Toronto is flavour). See claims.md for the trend hook and what each claim rests on.

## Script
1. [hook] Your fingers are freezing. So why do they start warming up?
2. Cold squeezes finger blood vessels, so skin chills and hands get clumsy. Then they reopen: cold-induced vasodilation, fam.
3. Ten people held a hand in ice-cold water. Fingers rebounded.
4. Still, gloves at the Bathurst stop beat hoping, styll.
5. [outro] Not medical advice. Send this to whoever won't wear gloves. Yo, it's ya boy Cyto!

## Scene table
| # | Backdrop / transition | Props (anchor word) | New this episode |
|---|---|---|---|
| 0 | windowfrost / zoom (instant) | vesselHand cross-section @"fingers" | windowfrost (bg), vesselHand |
| 1 | ttcshelter / membrane | vesselHand narrow-to-wide (morph on "reopen") @"squeezes"; tempDial dip then rebound (no numbers) @"chills" | ttcshelter (bg), tempDial |
| 2 | lab / doors | peopleGrid 10 @"ten"; tempCurve dip and rebound (no numbers) @"rebounded" | tempCurve |
| 3 | subway / whip | mitten (glove) @"gloves" | mitten |
| 4 | windowfrost / membrane (outro, clean) | none | loop back to scene 0 |
New-element share: 4 of 5 scenes (80%).

## New library items for the sprint (rule 25: add to backdrops.js / props.js / LIBRARY.md / library.png the same day)
- `windowfrost` (backdrop): frosted window with ice-crystal edges, cold blue night glow, breath fog.
- `ttcshelter` (backdrop): bus/streetcar shelter, glass panels, heater glow strip, snow blowing past. No route numbers or brand ads.
- `vesselHand` (prop): fingertip cross-section: skin layers over blood vessels; params `from_state`/`to_state` (`narrow`, `wide`), `morph_on` (anchor word where it flips), `label`. In scene 0 it is the POV push-in through the skin.
- `tempDial` (prop): round dial blue to red; `shape: dip-rebound`; `show_numbers: false`.
- `tempCurve` (prop): drawn-on line that dips then rebounds; no axis numerals.
- `mitten` (prop): cut-out glove/mitten with a small warm glow.
`make_episode.py` validates `bg` against a fixed list. The new backdrop ids above must be registered (BGS in make_episode.py + backdrops.js) before `--dry-run --stage validate` passes; with them registered the spec validates with 0 errors and 0 warnings.

## Rules checklist
- Rule 22 (22-26 s, loop): word-estimate ~22 s of speech, plus pauses and the outro ~24-25 s; last scene's backdrop = scene 0's backdrop; BUILD must make the last frame match the first (same Cyto pose).
- Rule 23 (intro + catchphrase): POV push-in through the skin (vesselHand cross-section at frame 1). Log `intro:pov-push-in`. Catchphrase: 1.3 s stinger at the very end over the outro ('Yo, it's ya boy Cyto!'), well after 6 s.
- Rule 24 (one ask, a send): spoken in the last scene AND on screen (headline + 'WHO'S YOURS?' card). Pinned comment posted the hour it goes public.
- Rule 21: every prop has `shows` + `anchor`; catchphrase/outro scenes have none.
- Rule 25: new backdrops + props listed above; at least 75% of scenes carry a first-appearance element.
- Cup: canon v2 paper coffee cup with steam. Nothing about drinking. No real brands.

## Thumbnails
See episode.json: A/B, `stronger` named. Vertical 1080x1920 first.

## Costs
Idea $0. ElevenLabs: see the voice estimate in the validator output (1 take). BUILD asks before spending credits.
