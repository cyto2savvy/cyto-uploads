# Ep 18 plan (REDO, BUILD chat, Nov 14): "Why Your Heart Doesn't Tire Like Your Bicep"
Status: gate 1 REOPENED (new script, new voice take needed). Slot Mon Nov 16, 6 PM ET (2026-11-16T23:00:00Z). Rules: HARD_RULES 22 (rewritten), 23, 23b. Old 23 s cut is superseded.

## Script (83 words, ~30 s; roles in episode.json)
1. [hook] Your heart works all day. So why does flexing your bicep burn?
2. [explain] A third of each heart cell is mitochondria, power plants running on oxygen.
3. [explain] And it does rest: between every beat, for more than half of each cycle, fam.
4. [explain, answers the hook] Your bicep's built for bursts: hold a flex and metabolites pile up. That's the burn.
5. [payoff] Heart's the 504, a quick stop every beat. Bicep's a weekend closure, styll.
6. [catchphrase, own beat] Yo, it's ya boy Cyto!
7. [ask] Send this to the one who does the bicep heart.
"Not medical advice" is on-screen text in the outro card, not spoken.

## Scene table
| # | Backdrop / transition | Props (anchor word) | Headline |
|---|---|---|---|
| 0 | gym / (instant) | ecgLine @heart; bicepHeart @bicep | HEART: NONSTOP / BICEP: BURNS? |
| 1 | chestcavity / membrane | cellSlice heartCell 1/3 @third | 1/3 MITOCHONDRIA |
| 2 | plain / zoom | ecgLine rest bands @rest | IT RESTS EVERY BEAT |
| 3 | gym (dim .4) / whip | fatigueMeter HEART vs BICEP, no numbers @bicep's | METABOLITES = THE BURN |
| 4 | subway (dim .45) / doors | stopSign 504 ALL DAY @504; ecgLine STOP bands @stop; stamp CLOSED @closure | HEART = THE 504 |
| 5 | streetcar / whip | none (clean, rule 21): backdrop + headline are the visual | LIVE FROM THE 6IX |
| 6 | gym / zoom | none: headline + WHO'S YOURS? + sources + Not medical advice | SEND IT TO THE HEART-POSE FRIEND |
Scene 2 is `plain`, not chestcavity: rule 6 bans the same backdrop twice in a row. New-element share 6/7 scenes.

## Loop (rule 22 a-d)
a) frame: scene 6 = scene 0's gym, seed and camera; hook headline fades back in; Cyto eases to his frame-0 pose.
b) motion: scene 6 holds the frame-0 camera (no drift), scene 0's push eases in from rest, Cyto's bounce/sway are at zero offset and zero speed on both sides of the seam.
c) audio: 0.5 s tail after the last word; the pad's frequencies are snapped to whole cycles of the runtime; one static gain instead of dynamic loudnorm.
d) sense: the last spoken line is the send-ask (scene order from the manager inbox), which reads into "Your heart works all day".
Evidence shipped with the draft: seam_frames.jpg, seam_waveform.png, transition_plot.png (with a SEAM panel).

## Costs
ElevenLabs: 1 take, 456 characters = ~456 credits (the first 359-credit take cannot be reused: different script). Scribe 0.
