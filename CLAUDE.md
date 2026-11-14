# Cyto The Cell / "The Body is the 6ix" — read this first

YouTube @thebodyisthe6ix. Monetized Shorts, one episode a day, plus occasional long-form.
Owner: Utsha. Casual and direct, concise over generic. Say it in a line, not a page.

## Before doing anything
1. `bash studio/restore.sh`
2. Read `studio/INDEX.md`, then `studio/HARD_RULES.md` (26 rules — these override every older
   note in the repo), then `studio/inbox/<your role>.md`.
3. Ignore `/archive/` and the legacy `rig/`, `hf/`, `episodes/ep01-13` builders.

## Roles (see studio/CHAT_ROLES.md)
MANAGER owns rules, analytics, scheduling, costs, repo docs — never writes scripts or builds.
IDEA pitches topics, researches PubMed, writes script + scene plan + claims.
BUILD renders, checks, packages.
Chats talk to each other through files in this repo, never by pasting long prompts.

## Non-negotiables (the full versions are in HARD_RULES.md)
- **$0 by default.** Say so BEFORE anything spends credits or money. The render costs nothing;
  ElevenLabs voice does.
- **Every claim traced to PubMed** or a textbook, sources on screen + in the description + in
  the pinned comment. "Not medical advice" on health topics, plus a see-a-doctor line where
  symptoms are involved. Run `studio/check_sources.py`.
- **Cyto canon v2**: paper COFFEE cup — white body, red band, brown lid, small flat Cyto-face
  logo, steam. Never the old double-stacked party cup. Whole cup in frame, in his mitten.
  No real brands. Never show the contents, never reference drinking or getting high.
- **Answer the hook.** If the hook asks a question, a later line answers it with a mechanism.
  Minimum 3 explaining lines. Narration 24-32 s.
- **One line, one job** — never the disclaimer, the ask and the catchphrase in one breath.
- **The catchphrase gets its own beat**, after the payoff, never in the first 6 seconds.
- **One ask per episode and it is a send**, not like/subscribe.
- **It has to loop**: last frame = frame 0, nothing mid-motion at the seam, clean audio tail,
  and the last line reads into the hook.
- **No TikTok.** Dropped Nov 13, 2026. The `tiktok/` folder is gone; don't recreate it.
- Toronto is the flavour, never the reason to watch.

## Build it
```
python3 studio/make_episode.py epNN          # runs to the next gate
python3 studio/make_episode.py epNN --ok plan   # gate 1 passed (Utsha approved the plan)
python3 studio/make_episode.py epNN --ok final  # gate 2 passed (Utsha approved the draft)
```
Needs python3 + numpy, node, ffmpeg. Stages: validate -> voice -> build -> thumbs -> checks ->
package -> schedule. It stops at the two OK gates and never spends credits itself: it writes
`voice_request.json` / `schedule_request.json` for whoever can make those calls.
Scene renders are cached per scene; `CYTO_NOCACHE=1` forces a full re-render.

## Where things live
`studio/episodes/epNN/` — episode.json, claims.md, plan.md, state.json (the source of truth)
`epNN/` at repo root — the rendered mp4, thumbnails, contact sheet (what gets uploaded)
`studio/rig_v2/` — the renderer and LIBRARY.md (reuse ids before drawing anything new)
`studio/GROWTH_NOTES.md` — what the analytics actually say. Read before changing the format.
`studio/schedule.json` — what is scheduled and what is live.

## Current state (update this line when it changes)
Nov 14, 2026: Eps 1-15, 17 live; Ep 16 scheduled Nov 14. Ep 18 in redo. Library sprint
running for Eps 18-25 (2 new backdrops + 2 new props per episode). ~22 subs, Shorts cap
~1,000 views — the diagnosis and the fix list are in GROWTH_NOTES.md.
