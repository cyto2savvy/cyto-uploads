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
