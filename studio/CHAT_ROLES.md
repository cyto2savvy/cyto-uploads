# Three-chat setup (from Nov 9)

Every chat starts the same way: clone the repo, run `studio/restore.sh`, read `studio/SETUP.md`. Chats talk to each other ONLY through files in the repo (never by pasting long prompts).

## 1. MANAGER chat (long-lived, low-volume)
- Owns: the standing rules, analytics/weekly report, scheduling decisions, platform rollout, cost approvals, Zapier/Drive, the repo docs.
- Does NOT: write scripts or build videos.
- Reads `studio/inbox/manager.md` (reports from the other two). Writes decisions to `studio/PROJECT_INSTRUCTIONS.md` / `SETUP.md`.
- Carried-over to-dos (status Nov 9: Ep 14 DONE; vidIQ exhausted DONE/noted; rest below are open - IG/FB Zap + test row need Zapier editor access, watermark + IG profile/AI label are manual for Utsha, Nov 12 slot needs idea chat, LF01 time needs Utsha's answer, Ep 14 swiped-away after it goes live Nov 11): publish the IG/FB Zap and delete the `test` row; Ep 14 scheduled Wed Nov 11 9:00 AM ET; fill the Nov 12 slot; LF01 publish time; vidIQ credits are exhausted; upload the new watermark in YouTube Studio; manual IG profile/Business account/AI-info label; get "Viewed vs swiped away" for Ep 14. Do NOT touch `tiktok/queue.json` (friend's Claude).

## 2. IDEA chat (short, one per batch)
- Owns: Toronto events + trends search, 3 topic pitches, PubMed research, script + scene plan + claims/sources list, title/thumbnail text options.
- Output: `studio/episodes/epNN/episode.json` (script, beats, outfit, thumbnail lines, sources) + `claims.md`. Stops at Utsha's OK.
- Does NOT: render anything or spend credits.

## 3. BUILD chat (one per episode, then discard)
- Input: an approved `episodes/epNN/episode.json`. Prompt is ~5 lines: "Build epNN from its episode.json; follow the repo rules."
- Owns: voice, rig render (cup always held + steam, face always moving, whole video canon cut-out style), captions, both thumbnails (1280x720 + 1080x1920), frame check via contact sheet, tests, YouTube scheduling after Utsha's OK, TikTok queue entry.
- Says before spending credits (ElevenLabs/vidIQ voice).
- Writes a 5-line result to `studio/inbox/manager.md` when done.

## Handoff rules
- Rules live in the repo, not in prompts. If a rule changes, edit the repo doc, not the prompt.
- One chat per episode for build; start a fresh one when context gets long.
- Ep 14 stays as-is. The `ledge`/cup-down option in the Ep 14 rig must NOT be used again.

- [DONE Nov 9, manager] studio/make_episode.py built + tested on Ep 14 data (see EPISODE_SCHEMA.md). IDEA chat writes episode.json; BUILD chat runs it.
