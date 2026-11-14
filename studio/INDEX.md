# What to read (everything else is reference or archived)
Repo root `CLAUDE.md` loads automatically in Claude Code and carries the non-negotiables; this file is the full map.
Always: HARD_RULES.md, SETUP.md, CHAT_ROLES.md, inbox/<your role>.md.
By job: IDEA -> rig_v2/LIBRARY.md (pick prop/backdrop ids; only ask for a new visual when none fits), templates/ (series skeletons to copy), VOICE.md, PUBLISHING.md, EPISODE_SCHEMA.md, sources_used.md, GROWTH_NOTES.md, schedule.json, prompts/idea.md. BUILD -> EPISODE_SCHEMA.md, rig_v2/LIBRARY.md (+ library.png: every prop/backdrop/transition that already exists), rig_v2/README.md + SCENE_STYLE.md, THUMBNAIL_FORMAT_V2.md, prompts/build.md. MANAGER -> PUBLISHING.md, costs.md, schedule.json, prompts/manager.md. Long-form only -> LF_FORMAT_V2.md.
Code (not docs): rig_v2/ (renderer; props.js, backdrops.js, compose.js, thumbs.js, library_render.py), branding/rebrand-v2/ (canon Cyto), pipeline/ (voice, srt, meta check), make_episode.py.
Templates: templates/6ix-seconds-of-science.json, templates/what-happens-when.json, templates/cyto-vs-disease.json - copy one to episodes/epNN/episode.json and fill the TODOs.
Scene cache (HARD_RULES 19): renders are per scene, keyed by scene + previous scene + words/beats + plan globals + engine hash, in <episode dir>/.scene_cache. Unchanged scenes are reused; `CYTO_NOCACHE=1` forces a full render. Delete the folder to reset.
Legacy code kept only because restore.sh copies it: rig/, hf/, episodes/ep01-13 builders. Do not extend them.
Dead (moved Nov 9): /archive/ (old batch prompts, Ep14 addendum, batch-mode doc, old thumbnail screenshots, SETUP history). Do not read it.
Rule: when a doc is superseded, `git mv` it to /archive/ the same day and update this index.
