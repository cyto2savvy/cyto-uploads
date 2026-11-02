# Cyto studio: how it works (read this first in a new chat)

**Restore:** `git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh`
The scripts expect the original paths (`/home/claude/cyto2`, `/home/claude/epN`, `/home/claude/hf`), and restore.sh recreates them.

**Publishing:** read `studio/PUBLISHING.md` (separate Shorts vs long-form rules: titles ≤ 60 / hard 70 chars, keyword in first 40, no hashtags in titles, chapters for long-form…). Every episode gets `epNN/meta.json`; run `python3 /home/claude/cyto2/check_meta.py epNN/meta.json` and fix all FAILs **before** showing Utsha the final package and before uploading. Required from Nov 1, 2026.

**Scripts:** read `studio/VOICE.md` before writing any script (Toronto slang bank, references, body map, checklist). Required from Oct 30, 2026.

### Cyto's voice = Utsha, disguised (Nov 1, 2026 — replaces vidIQ Liam once approved)
- Utsha records each script on his phone and drops the file in chat → save as `/home/claude/epN/rec.m4a`.
- `python3 cyto2/cyto_voice.py epN/rec.m4a epN/raw.wav [cyto|cartoon|gruff]` (source: `studio/pipeline/cyto_voice.py`; needs `pip install --break-system-packages pyworld pedalboard`). WORLD vocoder shifts pitch AND formants so it doesn't sound like him, then a character EQ/comp/grit chain.
- Then the usual: silencedetect → segs.json → build_voice2.py → timing.json. $0, no vidIQ credits.

## Pipeline (all $0)
1. **Research:** PubMed connector for the sources, and WebSearch for Toronto events and trends.
2. **Voice:** vidIQ voiceover, voice **Liam** (`voiceId TX3LPaxmHKxFdv7VOQHJ`). **Charged 14 credits per started 1,000 characters** — a 600-char script costs the full 14. Ask Utsha before spending. Spell for the ear: "three A M", "six" (captions come from `segs.json`, so they can still say 3AM / 6ix). The cloud workspace can't download the vidIQ MP3 (S3 is blocked), so Utsha drags it into chat.
   - Neither this workspace nor Utsha's Mac (`~/Claude/cyto-voice`, connected) can reach the S3 link — send Utsha the link and he saves it to `~/Claude/cyto-voice/` or drags it into chat.
   - Save it as `/home/claude/epN/raw.mp3`.
   - Find the speech segments with ffmpeg `silencedetect`, then write `segs.json`: `{"tempo":x,"segs":[[start,end,line,"phrase"],...]}`.
   - Run `python3 cyto2/build_voice2.py /home/claude/epN`. It writes `voice.wav` and `timing.json` (per-word times).
3. **Animation (current method, from Ep 7 on): HyperFrames + puppet rig.**
   - `cyto2/rig.py` exports the layered PNG rig to `cyto2/rig/`: body, toque, 2 eyes, 4 mouths, both arms and hands, cups (red, orange-pumpkin, blue) and the jersey outfit. `rig.json` holds the pivots.
   - `hf/cytohf.py` holds the shared helpers: `place()`, `mouth_track()`, `rig_html/css/js` (blinks, waves, points, tilts, shrugs, raises, sips), `cup_down()`, `captions()` and `transition()` (whip, membrane, doors, zoom).
   - **From Ep 8 on, every episode = v2 layout + v3 rig.** Start from `hf/template/build.py` (the standard: layout, vector rig, lip sync, acting, sip sound). Use `hf/ep07/build.py` only for full-episode structure ideas (hook, outro). **Never use the old PNG rig (`C.rig_html`/`C.rig_js`) for new episodes.** Copy the template to `hf/epNN/`, edit the scenes and timings, run `python3 build.py`, then `npx hyperframes lint`, then `npx hyperframes snapshot --at ...` (look at the frames!), then `npx hyperframes render --output X.mp4 --fps 30 --workers 4`.
   - Set `HYPERFRAMES_BROWSER_PATH` to the Playwright chrome-headless-shell (see restore.sh).
   - Episode audio: reuse an existing mix, or build voice + beat + SFX the way `cyto2/engine.py make_audio` does.
   - The old method (Eps 1–6) was a PIL frame renderer: `cyto2/render.py`, `engine.py`, `epN.py`. It's kept for reference.
   - **Frame check (v2):** after `npx hyperframes snapshot --at ... -o snaps`, run `python3 -c "import sys;sys.path.insert(0,'/home/claude/hf');import cytohf as C;C.safe_sheet('snaps','safe.jpg')"` and look at `safe.jpg`. It overlays YouTube's Shorts UI (grey shapes); no caption, card, number or face may sit under them.

### v3 rig (approved Oct 30, 2026 — Ep 8 onward) — `hf/cyto3.py`
Vector Cyto on the same canvas/pivots/cup PNGs as the old rig (outfits and cup rules unchanged). Before/after: `hf/v3test/compare_v3.mp4`.
- **Lip sync:** `R.viseme_track(voice.wav, words)` → 8 mouth shapes from the sounds (rest, M/B/P, small, A, E, O, U, F/V).
- **Acting every episode:** at least one `expr` per scene (`shock` on "bro WHAT" beats, `hype` on punchlines, `skeptic` on myths/rivals, `squint`, `sad` for serious parts) and `looks` so he glances at the figure. Gestures snap in, hold, settle; the pom-pom follows through automatically.
- **Organelles** (nucleus, nucleolus, mito, ER, golgi, ribosomes, vesicles) drift the whole time and pulse on his loud words — automatic. Outfits that cover the lower body hide some of them; prefer outfits that leave the middle visible.
- **Sip sound:** every sip in `gest["sips"]` gets a slurp via `R.mix_sips(base.wav, sip_times, audio.wav)`; the music dips under it. Always run it.

### v2 rules (approved Oct 30, 2026 — Ep 8 onward)
Why: in Eps 1–7 the captions sat under YouTube's title text, fact cards ran under the like/comment buttons, Cyto shrank to a corner sticker for ~18s, and the Mermaid diagram was default white boxes clipped off the edge. Before/after: `hf/v2test/compare.mp4`.
1. **Safe zone:** everything readable inside x 60–940, y 200–1480 (`C.SAFE`). Bottom ~440px and right ~140px belong to YouTube's UI. Captions at `C.CAP_Y_V2` (880), just under the figure panel.
2. **Cyto big, always on screen:** `C.CYTO_V2` (lower-left, scale 0.56) during science scenes; fact card to his right (`.card` in `V2_CSS`). He can go bigger for hook/joke/outro scenes, but never the old 0.40 corner placement.
3. **Diagrams:** Mermaid in the Cyto theme via `C.mermaid_svg(src, out)` (navy boxes, teal borders, yellow arrows), inlined in a `.mmd` div and built box-by-box on the voice with `C.mermaid_js`. Max 3 levels / 5 boxes, short ALL-CAPS labels.
4. **Lottie:** one LottieFiles animation per science scene where it fits. Find it with the LottieFiles MCP (`searchPublicAnimations`, use `jsonUrl`), add `name url` to `lottie/list.txt` (repo root) and push; the `fetch-lottie` workflow downloads it (check `lottie/status.txt`). Drive it with `C.lottie_js` (frame-locked to the timeline). Prefer animations close to the brand palette.
5. **Length:** hard cap ~30s (`C.MAX_T_V2`). Ep 7 ran 34.9s.

4. **Photos:** Unsplash search works, but direct downloads are blocked.
   - Add a line to `photos/list.txt` (repo root) (filename + images.unsplash.com URL) and push. The GitHub Action `fetch-photos` downloads it into `photos/`.
   - Always call Unsplash `download_asset` for each photo you use, and credit the photographer in the description.
   - Blur or avoid readable real company signs.
5. **Hosting:** commit the final mp4 and thumbnails to `epNN/` in this repo. Public raw URL: `https://raw.githubusercontent.com/cyto2savvy/cyto-uploads/main/epNN/<file>`.
6. **Upload (Zapier, YouTube app `YouTubeV4CLIAPI`).** Only after `check_meta.py` passes. Title/description/tags come straight from `meta.json`.
   - Before upload: `python3 /home/claude/cyto2/make_srt.py /home/claude/epN` → `captions.srt` (exact captions from timing.json; add the intro offset if the voice doesn't start at 0s). Set `captions_srt` in meta.json. Utsha uploads it in Studio → Subtitles (the API route needs file upload, which Zapier can't do).
   - After it goes live: pinned comment + related video (Studio, manual) and reply to comments in the first hour.
   Always pass `connection_id` `02a2f56e-1e01-8a41-9364-13e401f8bd6b`.
   - `upload_video` with `privacy_status: private` and `publish_at` (UTC), `category_id: 27`, `made_for_kids: false` and PubMed links in the description.
   - Then `_zap_raw_request` (tool `youtube_make_api_mutating_request`): PUT `videos?part=status` with `containsSyntheticMedia: true`, and keep `publishAt` + `privacyStatus: private`.
   - GET requests use `execute_zapier_read_action` with tool `youtube_make_api_get_request`.
   - Uploads playlist: `UUJRfXFQKUTWj-2LfA1cAWtA`.
   - **"Throttled" errors:** check the uploads playlist before retrying, since sometimes it did succeed. Space retries about 1 hour apart.
   - **Thumbnails:** they fail with a 429 until the channel is phone-verified (youtube.com/verify). Until then Utsha sets them in Studio.
7. **TikTok:** add the approved episode to `tiktok/queue.json`. Utsha's friend's Claude posts from it (see `tiktok/INSTRUCTIONS.md`).

### Thumbnails (Nov 1, 2026 — Ep 8 onward) — `hf/thumbs/thumb.py`
Old thumbnails were paused mid-video frames (tiny Cyto, fact cards, unreadable charts). Every thumbnail now uses ONE structure:
- **Series pill** (same spot every time) → **headline** max 4 words / 2 lines, white + ONE gold word, must ADD to the title (never repeat it) → **one hero object** that asks the question (phone at 3:00, a heart at 114 BPM…) → **huge reacting Cyto** (shock/skeptic/hype/tired face, looking at the hero, cup visible, white rim light).
- Bottom ~280px is YouTube's title overlay: background only. Everything that matters sits in the centre 1080x1350 so the 4:5 feed crop still shows headline + hero + face.
- Flat brand gradient + light rays from the hero. Never a photo, never a fact card.
- Make 2 options as a JSON spec (`hf/ep08/thumbs.json` is the example) → `python3 hf/thumbs/thumb.py spec.json outdir`. It also writes `feed_check.jpg` (full / 4:5 crop / phone-grid size) — look at it before showing Utsha.

### Art library — `hf/art.py`
Flat cutout set pieces in the rig's style: `skyline()`, `city_hall()`, `night_bus()`, `phone()`, `body_clock()`, `hypnogram()`, `moon()`, `stars()`. Add new Toronto pieces here (not inside an episode) so every episode can reuse them.
Outfits/accessories: `rig3_html(outfit, cup, acc)` — `acc` is an optional layer drawn ON TOP of the toque (e.g. `acc_sleepmask`). Drawn as SVG in `hf/outfits/`, exported to `rig/*.png`.

### Build gotchas (learned on Ep 8)
- HyperFrames renders by **seeking**, and GSAP skips `tl.call()` on seek. Never swap text with callbacks: put both versions on screen and swap opacity with `tl.set`.
- Lottie files often start on blank frames: drive them from a frame offset (see Ep 8's Zzz) if they're on screen at t=0.
- Loop: the last frame should match frame 1 (same background, same Cyto pose/eyes).
- `segs.json` takes optional `line_gap` / `in_gap` (default 0.26 / 0.11) — tighten gaps before raising the tempo above ~1.2.

## Posted so far (YouTube times are Eastern)
| Ep | Topic | YouTube ID | Go-live |
|---|---|---|---|
| 1 | Goosebumps | gm4Jgs3vvT4 | live |
| 2 | Scared to death (Halloween) | qy5GwZ3PMeo | live Oct 30 |
| 4 | Clocks fall back | etwgExzRMW8 | Oct 31, 7 PM |
| 3 | Sugar rush myth | M1_ZMi-Dceg | Nov 1, 11 AM |
| 5 | Cold season | Y8pJ4GNJ60s | Nov 2, 6 PM |
| 6 | Procrastination | OO9AceZh2tc | Nov 3, 6 PM |
| 7 | Leafs overtime (first rig episode) | Sd47GFmiTFg | Nov 4, 7 PM |
| 8 | Why you wake up at 3AM | kcKDLS1b-tE | Nov 5, 6 PM |
| 8 | Why you wake up at 3am (first v2+v3 episode, new thumbnail system) | — | built, awaiting OK (Nov 5, 6 PM) |

## Next ideas already researched
- Diwali (Nov 8): mithai and the sugar crash, with Mito (Mantantzis 2019, doi 10.1016/j.neubiorev.2019.03.016)
- "Why do you wake up at 3am" (about 19.7k searches/month, still needs a source)
- Royal Winter Fair (Nov 6–15)
- Remembrance Day (Nov 11)
- First long-form (with vidIQ Boost): "Cyto vs the Flu", which debuts Neutro and Platelet Pete

## Improvement log (one change per week, check it worked in the weekly report)
| Date | Change | Expected effect | Result |
|---|---|---|---|
| Oct 30, 2026 | v2 layout from Ep 8: safe-zone captions, big Cyto, themed Mermaid, Lottie, ≤30s | Fewer swipe-aways; captions readable over YouTube's UI | check after Ep 8–10 |
| Oct 30, 2026 | Toronto voice guide (`VOICE.md`): ≥3 slang + 1 Toronto reference per script | More comments/shares from Toronto viewers | check after first episodes using it |
| Oct 30, 2026 | **v3 rig TEST** (`hf/cyto3.py`, `hf/v3test/compare_v3.mp4`): vector Cyto, brows/lids/pupils, 8 mouth shapes from sounds, moving organelles, pom-pom, snappy pose-to-pose, sip SFX | Cyto feels alive; better retention | approved Oct 30 — standard from Ep 8 |

| Nov 1, 2026 | Thumbnail system (`hf/thumbs/thumb.py`): fixed headline / hero / big reacting Cyto structure, feed-crop safe | Higher CTR from the Shorts feed | compare Ep 8+ CTR vs Eps 2–7 in the weekly report |
| Nov 1, 2026 | Publishing rules (`PUBLISHING.md`) + `check_meta.py`: titles ≤ 60 (Shorts) / 50–60 (long), keyword first, no #shorts in titles, pinned comment + related video, separate long-form rules; tag recipe; exact captions file (`make_srt.py`) | Better search reach; titles not cut off | compare search traffic share before/after in the weekly report |

## Watch: vidIQ credits
Nov 1, 2026: 26 credits left after Ep 8 (14), 0 renewable until Nov 30 → only ~1 more Liam voiceover. Boost is needed for daily episodes. Spend credits on voice only until Boost is active.
