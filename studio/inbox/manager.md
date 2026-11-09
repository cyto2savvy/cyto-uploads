# Manager inbox
Reports from idea/build chats go here (newest first).

## 2026-11-09 manager -> all: make_episode.py is live
1. `python3 studio/make_episode.py epNN` runs episode.json -> voice -> canon-rig render -> captions -> A/B thumbs -> checks -> package; spec in studio/EPISODE_SCHEMA.md.
2. It spends 0 credits: prints the ElevenLabs estimate and writes voice_request.json; stops at gate 1 (`--ok plan`) and gate 2 (`--ok final`, then schedule_request.json for Zapier).
3. Proven on Ep 14 data: ~2 min render, 0 layout fails, 0 FAIL check_meta, canon 29/29, rig 15/15, `test_make_episode.py` 9/9.
4. Build chat: edit episode.json, not the script; never touch tiktok/queue.json (tiktok_entry.json is for Utsha to hand over).
5. Still open (manager): IG/FB Zap + `test` row, watermark + IG profile, Nov 12 slot, LF01 time, Ep14 swiped-away after Nov 11.
