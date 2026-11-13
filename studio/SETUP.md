# Cyto studio: read this first (lean version, Nov 9, 2026). Old history: archive/studio-docs/SETUP_history_to_Nov9.md (do NOT read unless Utsha asks).
**Order of authority:** studio/HARD_RULES.md > this file > the other docs listed in studio/INDEX.md. Anything in archive/ is dead.

## Restore
`git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh` (recreates /home/claude/{cyto2,hf,epN}). Pushing needs `add_repo` with access `push`.

## Make an episode (one command)
`python3 studio/make_episode.py epNN` (spec: studio/EPISODE_SCHEMA.md). IDEA chat writes studio/episodes/epNN/{episode.json,claims.md,plan.md}; BUILD chat runs it; stops at gate 1 (`--ok plan`: plan + credit estimate) and gate 2 (`--ok final`). It spends no credits; it writes voice_request.json for the chat to run. Fix problems in episode.json or the compositor, never by hand-building a one-off.
Tests: `bash studio/branding/rebrand-v2/run_tests.sh` (29/29), `python3 -I studio/rig_v2/test_rig.py` (15/15), `python3 -I studio/test_make_episode.py` (12/12).

## Look (canon v2)
Flat 2D cut-out Cyto, mitten hands, generic paper cup with steam + Cyto-face logo, gold "6" chain, toque. Built from studio/branding/rebrand-v2/cyto2d.js + rig in studio/rig_v2/ (cyto_rig.js, compose.js, thumbs.js). Style rules: HARD_RULES.md + rig_v2/SCENE_STYLE.md. Safe zone x 60-940, y 200-1480 (IG/FB: top 220 / bottom 350 clear); captions at y~900, 74 px.

## Voice
ElevenLabs Starter (30,000 credits/mo, renews Dec 2), voice "Cyto - Toronto (A)" id `MDpsT9lfiqWEMyN3A1bk`, model `eleven_v4`. `estimate_only` first, say the cost, never re-call a generation to retry. Spell for the ear in `tts` only; captions keep real spelling. Fetch audio via `audio/list.txt` + the fetch-audio GitHub workflow (sandbox cannot download from ElevenLabs/Unsplash). Word timings: Scribe (0 credits) -> words_scribe.json. Script rules: studio/VOICE.md. vidIQ credits are exhausted (1 left until Nov 30): do not use vidIQ tools.

## Publishing (Zapier YouTube, connection `02a2f56e-1e01-8a41-9364-13e401f8bd6b`)
Rules + metadata: studio/PUBLISHING.md; `python3 studio/pipeline/check_meta.py epNN/meta.json` must show 0 FAIL. Upload private + publish_at, then PUT status with `containsSyntheticMedia:true` and RESEND embeddable/publicStatsViewable/license (the PUT replaces status), add to playlist `PLIU9ZD7rP0Ss`, set thumbnail A/B (stronger first). `youtube_make_api_get_request` needs `fail_on_errors:"true"`, `method`, `querystring` as a dict. Calendar = studio/schedule.json. Credits log = studio/costs.md. No reused sources: studio/sources_used.md.
Ep 14 = Xwv_JKtNFgY (Wed Nov 11 9:00 AM ET). Ep 15 slot: Thu Nov 12 6 PM ET. LF01 MLdcV-vmyXE is set for Nov 29 9:45 AM ET (time unconfirmed).

## Platforms
YouTube Shorts 1/day. TikTok: no longer part of the plan (friend collaboration ended Nov 13, tiktok/ removed). IG/FB: social/PLAN.md (post natively, AI label on, 12:00 ET next day); Zap + watermark + IG profile still open.

## Chats
manager / idea / build, talking only through repo files: studio/CHAT_ROLES.md, studio/inbox/*.md, studio/prompts/*.md.

## Commits
End with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` + the Claude-Session line.
