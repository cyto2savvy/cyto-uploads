# Batch build mode (Nov 2-5, 2026) — one episode per cloud session

Goal: use Utsha's cloud-session credits (expire Nov 5) to build as many finished episodes as possible in parallel.
Each session = ONE episode. Flow per session:
1. Clone + restore (see SETUP.md), read SETUP.md, VOICE.md, PUBLISHING.md and the episode brief `studio/episodes/epNN/EPNN_brief.md`.
2. Voice: Utsha drags `epN/raw.mp3` (ElevenLabs "Cyto - Toronto (A)", already generated). Do NOT generate voice in the build session.
3. Build with `hf/template/build.py` (v2 layout + v3 rig), <=45s shorts. Follow the "Ep 9 lessons" in SETUP.md (zones, 1-fps frame check, eyes).
4. 2 thumbnails (say which is stronger), meta.json, `check_meta.py` 0 FAIL, captions.srt.
5. Commit episode folder + final mp4 to the repo (`studio/episodes/epNN/`), post the final package, STOP and wait for Utsha's OK. Scheduling/TikTok queue happens in the manager chat.
