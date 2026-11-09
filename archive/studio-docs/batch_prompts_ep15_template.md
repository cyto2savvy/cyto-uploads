# Next-episode build prompt (Ep 15 and every video after) — paste into the build chat, fill the <> parts
```
Build Ep <N> of Cyto The Cell: "<topic>" (Short, publish <date/time ET>). Follow the project workflow (pitch -> script/claims -> OK -> build -> show -> OK -> schedule). START: git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh ; git pull; read studio/SETUP.md, studio/branding/CYTO_CANON_v2.md, studio/rig_v2/README.md, studio/rig_v2/SCENE_STYLE.md, studio/GROWTH_NOTES.md, studio/THUMBNAIL_FORMAT_V2.md.

LOOK (non-negotiable, Utsha Nov 9):
1) Use the canon v2 rig: studio/rig_v2 (cyto_rig.js + render_rig.js). Build timeline.json from the ElevenLabs word timings (words) and write a BEAT for every idea/sentence change (emotion + gaze). Cyto's face MUST move all video: gaze wanders, blinks, brows/face react (shock/think/happy/laugh), mouth per syllable. Never one fixed stare.
2) The cup is ALWAYS in his hand (mitten + thumb), never set down or placed on anything, even in serious parts; steam rises, it sways a little.
3) The WHOLE video is in canon cut-out style (studio/rig_v2/SCENE_STYLE.md): backgrounds, figure cards, arrows, labels, captions, transitions. No generic stock or raw figures in the video body.
4) Run `bash studio/branding/rebrand-v2/run_tests.sh` (19/19) and `python3 -I studio/rig_v2/test_rig.py` (15/15) before showing anything; plus a 1-fps contact sheet showing face/expression changes between beats.

GROWTH: voice + huge claim + visual in frame 1; catchphrase after the hook; re-hook with an open-loop line at 4-5 s; new visual every 2 s in the first 8 s; ending loops into the hook; quiet follow chip around 40-60%; <= 34 s; universal "can you actually / is X a myth" topics with Toronto only in the payoff.

THUMBNAILS: MrBeast format v2 BOTH sizes: 1280x720 and vertical 1080x1920 (--format short), real topic background (AI scene ~820 ElevenLabs credits, say the cost first, or free Unsplash via photos/list.txt), huge expressive Cyto, <= 4 words, 2 options, say which is stronger.

COST: say before spending (voice ~14 vidIQ credits / ~1 ElevenLabs credit per char; image ~820). TikTok queue is not yours to touch. Wait for Utsha's OK before scheduling.
```
