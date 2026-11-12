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
