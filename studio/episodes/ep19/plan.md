# Ep 19 plan: "Is 'Hangry' Real? What Hunger Does to Your Mood" (IDEA chat, Nov 14, 2026)
Status: written by the IDEA chat, awaiting Utsha's OK (gate 1). Nothing rendered, 0 credits spent. Series: 6ix Seconds of Science. Slot: Tue Nov 17 6 PM ET (2026-11-17T23:00:00Z).
Claims/sources: `claims.md`. Spec: `episode.json`. Voice: 1 take (episode.json `voice.takes = 1`).

## Why this topic (rule 26)
Passes the topic gate (body fact leads; Toronto is flavour). See claims.md for the trend hook and what each claim rests on.

## Script
1. [hook] Is hangry real, or just an excuse?
2. 64 people logged their mood 9,000 times. Hungrier meant angrier and more irritable.
3. In a trial, fasted women reported more anger and tension. That's a link, styll, not the full why.
4. Yo, it's ya boy Cyto. Snack before you fight over the TTC, bro. Not medical advice. Send this to your hangriest friend.

## Scene table
| # | Backdrop / transition | Props (anchor word) | New this episode |
|---|---|---|---|
| 0 | foodcourt / zoom (instant) | crossOut "JUST AN EXCUSE" @"excuse?"; angerFace @"hangry" | foodcourt (bg), crossOut, angerFace |
| 1 | kitchen / whip | moodDial FULL to HUNGRY @"hungrier"; peopleGrid 64 @"people" | kitchen (bg), moodDial |
| 2 | lab / membrane | breakfastPlate FASTED vs ATE @"fasted"; arrowStat MORE ANGER (no number) @"anger"; stamp LINK, NOT PROOF @"link" | breakfastPlate |
| 3 | foodcourt / doors (catchphrase + payoff + send, clean) | none | loop back to scene 0 |
New-element share: 3 of 4 scenes (75%). The catchphrase scene is the last scene (clean by rule 21); it lands about 15 s in.

## New library items for the sprint (rule 25: add to backdrops.js / props.js / LIBRARY.md / library.png the same day)
- `foodcourt` (backdrop): mall food court: counters with generic blank signs, tray tables, warm lighting. No brands, no logos.
- `kitchen` (backdrop): night kitchen, fridge door open with glow, counter, clock reading late.
- `crossOut` (prop): block text slams in, then a red X/strike draws across it; param `text`.
- `angerFace` (prop): cut-out round face that flips from calm to hangry (brows down, steam puffs).
- `moodDial` (prop): semicircle dial, needle moves from smile to scowl; params `labels`.
- `breakfastPlate` (prop): two plates side by side: empty, and one with eggs and toast; param `labels`.
`make_episode.py` validates `bg` against a fixed list. The new backdrop ids above must be registered (BGS in make_episode.py + backdrops.js) before `--dry-run --stage validate` passes; with them registered the spec validates with 0 errors and 0 warnings.

## Rules checklist
- Rule 22 (22-26 s, loop): word-estimate ~22 s of speech, plus pauses and the outro ~24-25 s; last scene's backdrop = scene 0's backdrop; BUILD must make the last frame match the first (same Cyto pose).
- Rule 23 (intro + catchphrase): a wrong answer crossed out ('JUST AN EXCUSE' struck through, 'REAL.' in gold) at frame 1. Log `intro:wrong-answer-crossed-out`. Catchphrase: a beat at the Toronto payoff (about 15 s in), shortened to 'Yo, it's ya boy Cyto'. Varies from Ep 18 and 20 (stingers at the end).
- Rule 24 (one ask, a send): spoken in the last scene AND on screen (headline + 'WHO'S YOURS?' card). Pinned comment posted the hour it goes public.
- Rule 21: every prop has `shows` + `anchor`; catchphrase/outro scenes have none.
- Rule 25: new backdrops + props listed above; at least 75% of scenes carry a first-appearance element.
- Cup: canon v2 paper coffee cup with steam. Nothing about drinking. No real brands.

## Thumbnails
See episode.json: A/B, `stronger` named. Vertical 1080x1920 first.

## Costs
Idea $0. ElevenLabs: see the voice estimate in the validator output (1 take). BUILD asks before spending credits.
