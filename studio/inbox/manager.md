# Manager inbox
Reports from idea/build chats go here (newest first).

## Nov 9 (IDEA chat): Ep 15 scripted
Ep 15 "Can exercise actually lower your cancer risk?" scripted, awaiting Utsha OK (studio/episodes/ep15/). Suggested slot Thu Nov 12 6 PM ET. Sources logged in sources_used.md. Nothing built, no credits spent. Note: SETUP.md / project brief still say double-stacked party cup; Canon v2 coffee cup used.

## 2026-11-09 manager -> all: make_episode.py is live
1. `python3 studio/make_episode.py epNN` runs episode.json -> voice -> canon-rig render -> captions -> A/B thumbs -> checks -> package; spec in studio/EPISODE_SCHEMA.md.
2. It spends 0 credits: prints the ElevenLabs estimate and writes voice_request.json; stops at gate 1 (`--ok plan`) and gate 2 (`--ok final`, then schedule_request.json for Zapier).
3. Proven on Ep 14 data: ~2 min render, 0 layout fails, 0 FAIL check_meta, canon 29/29, rig 15/15, `test_make_episode.py` 9/9.
4. Build chat: edit episode.json, not the script; never touch tiktok/queue.json (tiktok_entry.json is for Utsha to hand over).
5. Still open (manager): IG/FB Zap + `test` row, watermark + IG profile, Nov 12 slot, LF01 time, Ep14 swiped-away after Nov 11.

## 2026-11-09 manager -> idea + build: HARD RULES after Ep 15 (studio/HARD_RULES.md, INDEX.md added)
1. Ep 15 as rendered FAILS the new rules: topic-less skyline thumbnail, text-only scenes with empty middle, stalled/popping transitions (s1 pop, s2 stall), cup clipped at the left edge. make_episode.py now fails these automatically.
2. IDEA: episode.json needs per scene `props` (>=2 drawn visuals), <=8 words text, no repeated backdrop in a row; per thumbnail `photo` + `bg_subject` ("cancer + Sunnybrook Odette Cancer Centre"). ep15/episode.json has 12 validation errors to fix; fetch a Sunnybrook/Princess Margaret photo via photos/list.txt.
3. BUILD: compose.js has NO prop renderer yet (layout.props_rendered = 0, TODO in file): add scene.props (organ, bars, counter, drawn arrow, icon row, hospital/TTC/trail backdrops), make transitions continuous (the membrane stalls, whip pops), blend Cyto's pose across cuts, and redo the cup hold (whole cup in frame, mitten wrapped, chest height). Default cytoX is now 0 so the cup is no longer clipped.
4. Repo cleaned: old batch prompts, Ep14 addendum, batch doc, old thumb screenshots and SETUP history moved to /archive/; SETUP.md is now 28 lines; read INDEX.md.
5. Utsha: add one line to the Project instructions: "Read studio/HARD_RULES.md and studio/INDEX.md first; ignore /archive/."

## 2026-11-11 manager -> BUILD: Ep 15 gate checklist (Utsha asked for all post-Ep15 feedback to be enforced; Ep 15 may not be shown until every line passes)
Cup is now explicitly the canon v2 COFFEE cup with steam (HARD_RULES 10); the old double-stacked party cup is retired.
1. PROPS (feedback 2+3): compose.js must render `scene.props` (organ, bars/chart, counter, drawn-on arrow, icon row, hospital/TTC/trail backdrops) and set `layout.props_rendered` to the real count. PASS = `props_rendered >= 2 x scenes`, every scene has >= 2 distinct props on screen between 0.5 s and the end, `make_episode` check "scene props rendered" = PASS.
2. NO BLANK SPACE (3): add a check that the middle band of the frame (y 25-65%) is never > 85% flat backdrop for more than 1 s. PASS on contact sheet at 2 fps: no frame with only text or only background in the middle.
3. TRANSITIONS (4): rebuild the membrane wipe so it does not stall and the whip so it has no single-frame pop; blend Cyto's pose across the cut. PASS = `transitions smooth` check PASS on every cut, no frame-diff of 0 inside a transition, no diff spike > 3x neighbours.
4. CUP HOLD (5): cup rides ONE rigid group with the mitten wrapped around it, rests at chest height beside the body, slight sway, steam rises, never floats or leaves the frame. PASS = `cup + Cyto fully inside the frame` PASS on all frames and a 2 fps contact sheet shows the cup attached to the mitten in every scene.
5. SCENE STYLE (2): every scene (not just the hook) uses SCENE_STYLE.md: parallax layers, pop-in with overshoot. PASS = no scene is text on a flat backdrop.
6. IDEA chat: fix ep15/episode.json (12 errors), add a Sunnybrook/Princess Margaret photo + `bg_subject` for both thumbnails, make A/B vertical-first (HARD_RULES 3b).
7. Then run `python3 studio/make_episode.py ep15`, look at the contact sheet, transition plot and 160 px thumbnail yourself, and only then hand the draft to Utsha.

## 2026-11-11 manager -> IDEA: queue is empty after Ep 14
Ep 9 (id UEAjo09k7WI) and Ep 14 (Xwv_JKtNFgY) are live/scheduled. Nothing is scheduled for Nov 12 or later (HARD_RULES 14: keep >= 3 ahead). Pitch 3 topics now (check Toronto events this week), and finish Ep 15's spec in parallel.

## 2026-11-11 manager -> BUILD: Ep 15 v2 feedback + speed (Utsha: "much better", but)
Feedback: (a) the transition into the intro (first cut) is off; (b) some animations sit in each other's way (overlaps). Rules 17-19 added to HARD_RULES.
Tasks, in order, no extra credits:
1. Fix the first-cut transition and add it to the `transitions smooth` check (rule 18).
2. Add an overlap check to make_episode/compose (rule 17): per-frame bounding boxes for props, headline, card, captions, Cyto face, cup; FAIL on > 0.3 s overlap; print which two items collided and in which scene. (Utsha, Nov 11: Ep 15 is NOT being rebuilt; the checks apply from the next episode on.)
3. Write studio/rig_v2/LIBRARY.md from props.js + backdrops.js: every id (organ kinds, bars, counter, runner, icons, peopleGrid, arrowStat, stamp, stopSign, backdrops, transitions) with params and a tiny example JSON. Add a `library_render.py` that renders a contact sheet of every item (one PNG) so Utsha and the idea chat can see what exists.
4. Add per-series scene templates (6ix Seconds of Science, What happens to your body when..., Cyto vs Disease) as episode.json skeletons: hook / explain x3 / stat / Toronto payoff / outro, each pre-filled with library ids, so a new episode = fill text + pick ids.
5. Scene cache (rule 19): hash each scene's JSON + rig version, skip re-render when unchanged, so fixes cost seconds not a full render. Voice stays gated (voice_request.json), no credits.
6. Target: a new Short from approved script to checked draft in ~15 min of work. Do not rebuild Ep 15. Time the next episode instead.
IDEA chat: use LIBRARY.md ids in episode.json; only request a new visual when none fits.

## 2026-11-11 BUILD -> manager: tasks 1-6 done (Ep 15 NOT rebuilt, 0 credits)
1. **First cut fixed + checked.** Three real causes, all in the engine: cuts used linear progress so the motion stopped
   dead on the last frame; the outgoing headline dissolved *before* the cut while everything else slid; and the incoming
   headline waited until 0.5 s *after* the cut, so the new scene arrived wordless. Now every cut eases in and out, the
   outgoing text rides off with the cut, the incoming text lands at 60% through it, and Cyto leans into the whip instead
   of sitting frozen. Two rig bugs behind the "pose jumps": the gaze pin was released instantly at 2.2 s, and it was
   dropped outright when the next beat had no pin. Both now ease. The check (`transitions smooth, every cut incl. the
   first`) covers scenes[1..n] — the first cut was always in that list — and now also fails on a pose break: it measures
   per-frame pose *jerk*, so a fast-but-smooth head turn passes and a one-frame snap does not. Ep 15 measures 1.0–1.7
   against a limit of 3.0.
2. **Overlap check added (rule 17).** compose.js measures bounding boxes every 0.1 s for props, headline, card, captions,
   Cyto's face and his cup, tracks how long each pair overlaps, and fails on > 0.3 s, naming both items and the scene.
   Frames inside a cut are skipped (both scenes are on screen by design). On a layout.json from before this change the
   check reports "not measured" rather than passing silently. **Ep 15 has 6 real overlaps** (it is not being rebuilt):
   s0 arrowStat×icons 1.97 s, s0 organ×runner 0.37 s, s1 organ×peopleGrid 0.4 s, s3 card×organ 3.33 s,
   s3 card×peopleGrid 1.93 s, s5 counter×icons 5.33 s. That is what Utsha saw. LIBRARY.md documents how to stack props
   so it does not happen again.
3. **LIBRARY.md + library_render.py.** Every id with parameters and copy-paste JSON: 11 prop types (17 variants),
   9 backdrops, 4 transitions, plus the placement/timing rules and the checks each one can fail.
   `python3 studio/rig_v2/library_render.py` → `studio/rig_v2/library.png`, one sheet of everything that exists.
4. **Series templates** in `studio/templates/`: 6ix-seconds-of-science, what-happens-when, cyto-vs-disease. Seven scenes
   each (hook / explain ×3 / stat / Toronto payoff / outro), pre-filled with library ids, backdrops that never repeat
   back to back, and props already spaced so the ≤ 2 s and no-overlap rules hold. Copy one, fill the TODOs. A template
   passes `--stage validate` as-is, so the structure is never the thing that breaks.
5. **Scene cache (rule 19).** Rendering is per scene, keyed by the scene + the previous scene (its composite shows during
   the incoming cut) + the words/beats in range + plan globals + a hash of the engine source, cached in
   `<episode dir>/.scene_cache`. Measured on Ep 15's plan: **cold 2m31s, unchanged re-render 1.3 s, one-scene edit 46 s**
   (that scene plus the next, whose cut shows it). `CYTO_NOCACHE=1` forces a full render.
6. **~15 min target.** Not claimed yet — it needs a real episode and I was told not to rebuild Ep 15. The build steps now
   cost: validate ~1 s, render 2m30s cold (seconds for a fix), thumbnails ~25 s, checks ~70 s, package ~15 s. The gap is
   the voice gate, which still waits for Utsha. I will time the next episode end to end and report the real number.

Also fixed: `props_rendered` counted props on transition frames, where both scenes are on screen, so it over-reported
(50 vs the true 26 for Ep 15). Tests: 18/18 offline (adds overlap, pose and cache-key cases), rig 15/15, canon 29/29.

## IDEA chat, Nov 11 (late)
- Ep 16 "No Nut November vs Your Prostate: Science" scripted: episodes/ep16/{episode.json,claims.md,plan.md}. Validates (80 words, ~491 credits/take). Suggested slot Fri Nov 13 6 PM ET. Waiting for Utsha OK. Not monetized yet, so reach over ad-safety.
- Pitches 1-3 (knees/weather, cold pee, therapy dog) still open; Ep 15 not rebuilt, still with BUILD chat. Buffer rule needs more eps.
- Ep 17 "Why Quitting Smoking Is So Hard" scripted (Addictions Awareness Week), slot Fri Nov 13 6 PM ET. Ep 16 moved to Sat Nov 14. Smokers Helpline number NOT verified, left out.

## 2026-11-12 manager -> BUILD + IDEA: variety system (Utsha: "every ep should be somewhat unique, but the bot mixes and chooses from a select variety created from different episodes")
Rule 20 added to HARD_RULES. Ep 17 reused too much of the previous episode's look. Do NOT rebuild Ep 15/17 for this; apply from Ep 18 on (Ep 17 only if Utsha asks).
BUILD:
1. Tag every library item (backdrops, props, organ kinds, transitions) in LIBRARY.md with topic tags (heart, brain, cancer, sleep, food, sport, city...), mood, and a "last used in epNN" field filled from a new studio/rig_v2/library_usage.json (written by make_episode when an episode is packaged; backfill from Ep 1-17).
2. Add `suggest_scenes.py <topic tags>`: prints, per scene role (hook, explain, stat, payoff), 3 candidate backdrop+prop sets that fit the tags, least-recently-used first, none identical to the last 3 episodes. The idea chat uses it instead of reusing the last episode's scenes.
3. Add the check "variety vs last 3 episodes" to make_episode (rule 20): FAIL if > 50% of scenes repeat a backdrop+prop combo from the last 3 episodes, or the backdrop order matches the previous episode. Also require >= 1 least-recently-used or new item.
4. Make library items parametric so reuse still looks different (position, colour, scale, count, timing); document the knobs in LIBRARY.md.
5. When an episode needs a visual the library lacks, draw it once, add it to the library with tags the same day. Target: library grows by 1-3 items per episode, build time stays ~15 min.
IDEA: pick scenes via suggest_scenes.py and the tags; say in plan.md which items are reused and which are new.

## 2026-11-12 manager -> BUILD + IDEA: no floaters (Utsha, after watching Ep 15: "stuff floating around in random scenes, not necessary")
What I saw on Ep 15's contact sheet: the jogger runs through the hook, the "LIVE FROM THE 6IX" catchphrase scene and the outro with no link to the line; stray pink boxes/tabs and circles hang in the 5-year and colon scenes; dot rows and bubbles that mean nothing. Rule 21 added; rule 5 loosened (props only when they show what is said; catchphrase/outro have none).
BUILD: (1) remove ambient/decorative layers from the default scene render (keep backdrop elements that are part of the place, e.g. snow in a snow scene); (2) require `shows` + word anchor on every prop in episode.json and validate it; (3) auto-hide a prop 1.5 s after its anchor sentence; (4) add check "no floaters" to make_episode; (5) strip the jogger/shoe/etc. from the series templates unless the topic is exercise; catchphrase and outro templates get no props; (6) clean Ep 17 with these before it is scheduled (cache makes it cheap). Do not rebuild Ep 15 (already scheduled).
IDEA: every prop in plan.md gets a one-line "shows" tied to the exact words; no prop without a line it illustrates.

## 2026-11-12 BUILD -> manager + IDEA: rules 20 + 21 tooling is in; Ep 16 plan rebuilt (0 credits)
- Done: `suggest_scenes.py` (+ `rig_v2/library_tags.json`, `rig_v2/library_usage.json`), make_episode checks "variety vs last 3 episodes", "no floaters", "every declared prop was drawn"; props take `shows` + `anchor` (+ `lead`, `hold`) and leave 1.5 s after their sentence; templates stripped (no runner/shoe filler, catchphrase + outro clean); `plain` rings and non-snow snow particles removed. Rules apply from Ep 16 (`RULE21_FROM`). Tests: test_make_episode 28/28, rig 19/19.
- New library items: organ kind `prostate`, stamp `plate`, scene `dim`. LIBRARY.md §6 documents all of it.
- Ep 16: episode.json/plan.md/claims.md rewritten; a silent preview with synthetic timing passes every check. Blocked only on Utsha's OK for 1 voice take (~524 ElevenLabs credits).
- NOT done: Ep 17 clean-up for rule 21 (task 6). Its episode.json still has the runner/shoe props and no anchors; it publishes Nov 13. Needs Utsha's call (rebuild costs 0 credits, the voice exists).
- "No blank middle" and "new thing every 2 s" are now measured only while a prop is up (rule 21 allows empty beats). Flagging so nobody thinks they got stricter.

## 2026-11-13 BUILD -> manager: Ep 16 FINAL approved by Utsha, in the repo, NOT yet scheduled
- Files: `ep16/` (video, vertical + 16:9 thumbnails A/B, contact sheet), `studio/episodes/ep16/` (episode.json, plan.md, claims.md, state.json, schedule_request.json, meta). Stronger thumbnail = A.
- Still to do (not done by BUILD): YouTube schedule via Zapier for Sat Nov 14, 6 PM ET (private + publishAt, altered/synthetic = YES, playlist Cyto vs Disease, thumbnail A), then the IG+FB Sheet row (rule 15). tiktok/queue.json untouched by BUILD.
- Cost: 524 ElevenLabs credits (1 take). Ep 17 rule 21 clean-up still open.

## 2026-11-13 BUILD -> manager: Ep 17 rebuilt for rules 20/21 (task 6 done), draft in the repo, awaiting Utsha's final OK
- Files: `ep17/` (video, vertical + 16:9 thumbnails A/B, contact sheet), `studio/episodes/ep17/` (episode.json, plan.md, state.json). Stronger thumbnail = B. Checks 0 FAIL / 0 WARN.
- Every prop has `shows` + anchor; catchphrase + outro clean; runner/shoe gone. New library item: organ kind `brain` (rig tests 20/20).
- Cost: 550 ElevenLabs credits (1 take, Nov 12); the rebuild cost 0.
- NOT done: gate 2 `--ok final`, YouTube schedule (slot Fri Nov 13, 6 PM ET; the Zapier connector was down in the build session), IG+FB Sheet row. tiktok/queue.json untouched by BUILD.

## Views push + library sprint (Nov 14, from the 16-Short analytics pull)
Read studio/GROWTH_NOTES.md (Nov 14 section) and HARD_RULES 22-26 before building Ep 18.
Why: 85% of views come from the Shorts feed; we hold ~15 s whatever the length; seeded episodes
stall at ~1,000 because shares/comments are ~zero.

BUILD tasks, starting Ep 18:
1. Length: target 24 s, hard fail over 28 s. Cut a beat rather than speeding up the read.
   Make the last frame match the first so the loop is seamless.
2. Intro: a different opening pattern from the last 3 episodes, logged as `intro:<pattern>` in
   library_usage.json. First 2 spoken words = the question or claim. Catchphrase out of the
   first 6 s — make it a 1-1.5 s stinger over the outro or a beat at the Toronto payoff, and
   alternate which one.
3. One ask, and it's a send ("send this to the one who always..."), spoken AND on screen.
   Closing question on screen too.
4. Library sprint, Eps 18-25: ~75% of scenes contain a first-appearance element, and at least
   2 new backdrops + 2 new props per episode, added to backdrops.js/props.js + LIBRARY.md +
   library.png the same day. New = different silhouette, not a recolour. Expect build time to
   rise during the sprint; that is accepted.
5. New make_episode checks to add: `duration <= 28 s`, `loop frame match`, `intro pattern differs
   from last 3`, `catchphrase start >= 6.0 s`, `send-ask present (spoken + on screen)`,
   `new-element share >= 75% (Eps 18-25)`.
6. Report per episode: duration, catchphrase start time, intro pattern used, and the list of new
   library ids added.

IDEA chat: HARD_RULES 26 topic gate. "Why does your body do X" / "is X real" / "what happens to
your body when X". No local-sports-only or "does this practice work" openers; Toronto is the
flavour, not the reason to watch.

## IDEA chat, Nov 14 (Eps 18-20 written, awaiting Utsha's OK)
- Ep 18 "Why Your Heart Doesn't Tire Like Your Bicep" (#BicepHeart hook), Ep 19 "Is 'Hangry' Real?", Ep 20 "Why Do Freezing Fingers Suddenly Warm Up?" are in studio/episodes/ep18-20 (episode.json, claims.md, plan.md). All three validate with 0 errors once their new backdrop ids are registered (gym, chestcavity, foodcourt, kitchen, windowfrost, ttcshelter).
- Slots written as Mon Nov 16 / Tue Nov 17 / Wed Nov 18, 6 PM ET (23:00Z). Utsha said "Sun Nov 16" but Nov 16, 2026 is a Monday: manager to confirm.
- Each ep is 60-63 words (~22 s of speech, ~24-25 s with pauses), 1 voice take: 348 / 352 / 385 ElevenLabs credits (about 1,085 total). BUILD asks before spending.
- Sources: Ep 18 has ONE PubMed source (Hinton Circ Res 2024: mitochondria = one third of cardiomyocyte volume); the heart-vs-bicep contrast is textbook and the page is unconfirmed. Ep 20 angle changed from rewarming pain to cold-induced vasodilation (no source for the pain mechanism).
- check_make_episode gaps: BGS in make_episode.py has a fixed backdrop list, so new ids fail validation until registered. Intro patterns to log: `intro:stat-stamp` (18), `intro:wrong-answer-crossed-out` (19), `intro:pov-push-in` (20). Catchphrase: stinger at the end (18, 20), payoff beat ~15 s (19).

## 2026-11-14 BUILD -> manager: Ep 18 draft built, awaiting Utsha's final OK (gate 2)
- Ep 18 "Why Your Heart Doesn't Tire Like Your Bicep": 23.1 s, all checks PASS incl. the new rule 22-25 checks; catchphrase starts 21.0 s; intro logged `intro:stat-stamp`; loop: last frame = first.
- New library ids: backdrops `gym`, `chestcavity`; props `ecgLine`, `bicepHeart`, `cellSlice:heartCell`, `fatigueMeter` (LIBRARY.md, library.png, tags updated; rig tests 27/27, make_episode tests 34/34).
- Changed vs the idea chat's spec (Utsha OK'd at gate 1): scene 2 props (meter on "bicep" + stop sign "504 / ALL DAY" + "CLOSED" stamp, dim .45) because one late prop failed the 2 s rule; thumbnail B scene lab -> hospital; `tts` ear-spelling for 504/styll; `voice.lead` 0.12; `intro` field added to Eps 18-20.
- Credits: ElevenLabs 359 (1 take; 348 approved + 11 for the ear-spelling). Scribe 0. vidIQ 0.
- NOT done: gate 2, YouTube schedule (Mon Nov 16 6 PM ET), IG+FB Sheet row. Open: textbook edition/page for the heart-vs-bicep contrast is still a placeholder in the description. Eps 19-20 still need their backdrops registered (foodcourt, kitchen, windowfrost, ttcshelter).

## Ep 18 redo (Nov 14) — my rules were wrong, not your build
Utsha on the Ep 18 draft: "it barely explained the topic and in the end it just blurted out
'yo it's ya boy Cyto'". You followed rules 22-24 exactly; the rules fought each other. Both are
rewritten — re-read HARD_RULES 22, 23 and the new 23b before redoing this.

What changed:
- Rule 22: narration is now 24-32 s (fail over 34), with a MINIMUM of 3 explaining lines, and a
  new check — if the hook asks a question, a later line must answer it with a mechanism. Ep 18's
  hook asked "why does flexing your bicep burn?" and claims.md line 5 admits the video never
  answers it. The outro's seconds no longer count against the body budget.
- Rule 23: the catchphrase gets its own 1.5-2 s beat with a visual, after the payoff. Never
  stapled to another line. Cut it entirely if there's no room.
- Rule 23b: one line, one job. Never disclaimer + ask + catchphrase in one breath.

Ep 18 redo, same slot (Mon Nov 16, 6 PM ET — Utsha said Sun, the date is a Monday, keep Nov 16):
1. Answer the hook. The payoff is that the heart DOES rest — it rests between every beat
   (diastole is roughly two thirds of the cardiac cycle at rest), it is almost entirely
   oxidative and densely capillarised, so it never runs the deficit a bicep does. The bicep
   burn is metabolite build-up in fast-twitch glycolytic fibres (H+, inorganic phosphate, ADP)
   — NOT "lactic acid", do not say lactic acid. Source these properly; claims.md currently has
   one PubMed-verified line (Hinton, Circ Res 2024, mitochondria = 1/3 of cardiomyocyte volume)
   and the rest is textbook. Get a real source for the diastole and the metabolite lines, or
   phrase them as the textbook physiology they are.
2. Structure: hook (the trend + the question) -> 1/3 mitochondria -> it rests between beats ->
   bicep is built for bursts and accumulates metabolites -> Toronto payoff -> catchphrase beat
   -> send-ask. That is ~30 s, which is now allowed.
3. Keep: the #BicepHeart hook, the new library items (gym, chestcavity, ecgLine, bicepHeart,
   cellSlice, fatigueMeter), the loop, the vertical thumbnails, the no-numbers fatigue meter,
   and the chest-pain line in the description.
4. Add the make_episode checks for the rewritten rules: `hook answered`, `>= 3 explaining
   lines`, `narration <= 34 s`, `catchphrase has its own scene`, `one line one job`.

### Ep 18 redo: the loop and the flow are the part not to break
Utsha: "make sure the loop and everything is intact cus remember it has to flow good and loop
properly." Rule 22's loop spec is tightened — the check was pixel-only. Four things now:
- Frame: last frame = frame 0 (backdrop, Cyto pose, camera position and zoom). Already checked.
- Motion: nothing mid-arc at the seam. Cyto's idle bounce and any camera push sit at a neutral
  point at BOTH ends so the restart doesn't jerk or run backwards.
- Audio: last word finishes with >= 0.25 s of clean tail, no click, no clipped syllable, bed
  continuous across the seam. Look at the waveform at both ends, not just the picture.
- Sense: the last line reads into the hook. Catchphrase beat last is good — "Yo, it's ya boy
  Cyto" into the hook is the natural order on a replay.
Run the frame-diff transition check across the seam as well, treating end -> start as a cut.

Scene order for the redo (keeps gym at both ends so the loop holds):
  0 gym (hook: trend + the question, `instant`)
  1 chestcavity (1/3 mitochondria)
  2 chestcavity or cellSlice variant (it rests between beats - diastole)
  3 gym or new bg (bicep is built for bursts, metabolites build up)
  4 subway (Toronto payoff: 504 always running vs weekend closure)
  5 short beat (catchphrase, own 1.5-2 s scene, with a visual)
  6 gym (send-ask + sources on screen; disclaimer is ON-SCREEN text, not spoken)
Scene 6 backdrop MUST equal scene 0's, and rule 6 still bans two consecutive scenes sharing a
backdrop — so scene 5 cannot be gym. ~30 s total, which rule 22 now allows.
Report the seam evidence with the draft: first and last frame side by side, the waveform at
both ends, and the transition plot including the seam.

## 2026-11-14 BUILD -> manager: Ep 18 REDO built, awaiting Utsha's final OK (gate 2 NOT run)
- 28.5 s (hook-to-payoff narration 24.1 s, outro 4.4 s), 7 scenes, 3 explaining lines; hook answered in line 4 (metabolites build up = the burn, Pollak 2014). All checks PASS incl. the new ones: hook answered, >= 3 explaining lines, narration <= 34 s, catchphrase own scene (s5 streetcar, 1.61 s, starts 24.5 s), one line one job, loop frame / motion / audio / sense.
- Seam evidence in ep18/: seam_frames.jpg, seam_waveform.png, transition_plot.png (SEAM panel). Frame diff across the seam 0.22 (in-scene median 0.77); 0.59 s tail after the last word; bed continuous.
- Science: diastole spoken as "more than half of each cycle" (Friedberg 2006 measured ~0.58 in healthy controls; "two thirds at rest" was not found in a PubMed abstract, textbook only). No "lactic acid", no "fast-twitch", no capillaries (unsourced). Sources: Hinton 2024, Pollak 2014, Karwi 2019, Friedberg 2006.
- Credits: ElevenLabs 456 (1 take). The Scribe call quoted 165 cr at start (first time non-zero): confirm on the usage page. Ep 18 total voice: 359 (superseded take) + 456.
- Open: sources card is on screen only ~1.3 s in the 2.5 s outro; description is 337 words (check_meta WARN, aim <= 220). Intro logged `intro:cold-open-question`. Not scheduled; IG+FB row not added.
