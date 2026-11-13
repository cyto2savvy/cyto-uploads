# Ep 17 plan: "Why Quitting Smoking Is So Hard (And What Helps)" (IDEA chat, Nov 11, 2026)
Status: REBUILT for HARD_RULES 20/21 on Nov 13 (0 FAIL / 0 WARN), awaiting Utsha's new gate-2 OK. The Nov 12 approval covered the pre-rule-21 cut.
Voice = 1 take, 550 ElevenLabs credits, already generated — the rule-21 rebuild costs 0 extra credits. Claims: `claims.md`. Spec: `episode.json`.

## Why
- Public-health tie: National Addictions Awareness Week (Nov 15-21) and Lung Cancer Awareness Month (Nov). Utsha asked for it this Friday: publish_at 2026-11-13T23:00:00Z (Fri 6 PM ET).
- Honest framing: the Italian RISP data is non-randomized, so the script says "not a fair race, linked, not proven".
- Slot note: Ep 16 (NNN) moved to Sat Nov 14 to avoid a clash. Manager can swap.

## Script (~85 words)
1. [hook] Quitting smoking is hard, and your brain's the reason, fam.
2. Nicotine locks onto brain receptors, so cravings hit louder than a TTC delay.
3. Yo, it's ya boy Cyto, live from the 6ix... inside your body.
4. In an Italian lung screening program, half of smokers who chose the plant-based medicine cytisine quit. Counselling alone: 8 percent.
5. But they picked it themselves, so it's not a fair race. Linked, not proven, styll.
6. So ask your doctor or pharmacist what fits. Every try counts, bro.
7. Not medical advice. Know someone quitting? Send this, because

## Scene table
| # | Backdrop / transition | Props |
|---|---|---|
| 0 | hospital / zoom (instant) | organ lungs @"smoking"; organ brain (NEW) @"brain's" |
| 1 | streetcar / whip | stamp NICOTINE @"Nicotine"; icons cell RECEPTORS @"receptors"; stopSign TTC/DELAY @"TTC" |
| 2 | hospital / membrane | none (catchphrase, clean) |
| 3 | lab / whip | card ITALY 2026 @"Italian"; peopleGrid HALF QUIT (5 of 10) @"half"; bars 50.1 vs 8.1 @"Counselling" |
| 4 | plain / zoom | peopleGrid CHOSE IT @"picked"; stamp LINKED @"Linked"; stamp NOT PROVEN @"proven" |
| 5 | snow / doors | icons person ASK THEM @"doctor"; icons check EVERY TRY @"try" |
| 6 | hospital / whip | none (outro, clean; sources card only) |

### Rule 20/21 rebuild (BUILD chat, Nov 13) — supersedes the Nov 12 notes below
Every prop now has `shows` + a word `anchor` and leaves with its sentence; catchphrase and outro are prop-free. Reused: lungs, stamps, icons, peopleGrid, bars, card, stopSign (all with new params). New: organ kind `brain` (added to props.js, LIBRARY.md, library_tags.json, test_rig). Backdrop order hospital/streetcar/hospital/lab/plain/snow/hospital. 0 extra credits (same voice take).

### BUILD chat prop changes (Nov 12, Ep 17 draft 1 -> final)
Props are all existing LIBRARY.md ids; only parameters changed, so nothing new to add to the library.
- s1: lungs labelled "RECEPTORS" contradicted the line — nicotinic receptors are in the brain, not the lungs. Swapped to a cell grid labelled RECEPTORS + a NICOTINE stamp.
- s5/s6: `shoe` / `runner` were exercise-episode template leftovers with no link to quitting. Replaced with check/person icons and a SEND IT people grid.
- s5: stopSign text "ASK FOR HELP" overflowed the sign's 216 px box; shortened to "ASK".
- s0: icon row re-laid out as 3x2 (it was clamped wide and covering the lungs, HARD_RULES 17).
- s1-s4: prop `in`/`spread` re-timed for the <= 2 s arrival rule without leaving the middle of the frame flat.
- Description: dropped a duplicated sources block and hashtag line (make_episode appends both).

## Look
Toque + puffer, canon coffee cup with steam. No smoking props.

## Title / thumbs
- Title (48): Why Quitting Smoking Is So Hard (And What Helps)
- A: QUITTING / IS HARD. B (STRONGER): 50% VS 8% / QUIT. Number plus curiosity gap.

## Costs
Idea $0. ElevenLabs about 500-600 credits/take (build chat asks first).
