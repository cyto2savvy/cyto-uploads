# Cyto studio: how it works (read this first in a new chat)

**Restore:** `git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh`
The scripts expect the original paths (`/home/claude/cyto2`, `/home/claude/epN`, `/home/claude/hf`), and restore.sh recreates them.

**Publishing:** read `studio/PUBLISHING.md` (separate Shorts vs long-form rules: titles ≤ 60 / hard 70 chars, keyword in first 40, no hashtags in titles, chapters for long-form…). Every episode gets `epNN/meta.json`; run `python3 /home/claude/cyto2/check_meta.py epNN/meta.json` and fix all FAILs **before** showing Utsha the final package and before uploading. Required from Nov 1, 2026.

**Scripts:** read `studio/VOICE.md` before writing any script (Toronto slang bank, references, body map, checklist). Required from Oct 30, 2026.

### CYTO'S VOICE NOW = ELEVENLABS (Nov 2, 2026, Ep 9 onward) — replaces vidIQ Liam
- Plan: ElevenLabs **Starter** (renews Dec 2; 30,000 credits/mo; commercial license, ONLY for audio generated while subscribed). Never publish audio made on the free tier.
- Voice: **"Cyto - Toronto (A)"**, voice_id `MDpsT9lfiqWEMyN3A1bk` (designed: young Toronto male, chill, slightly raspy). Model `eleven_v4` (supports tags like [pause], [laughs softly], [whispering]). Cost ~636 credits per 40s read per take; use 2 takes and pick.
- Spell for the ear in the TTS text only (captions keep the real word): "ah-lie", "stiiill", "the six". Full table: `studio/VOICE.md` > "TTS pronunciation".
- Flow: ElevenLabs connector `creative_generate_speech` (poll `creative_get_flow_run_status`) -> Utsha downloads the mp3 from the ElevenLabs link and drags it into the chat (the sandbox cannot download elevenlabsusercontent.com) -> save `epN/raw.mp3` -> silencedetect -> `segs.json` -> `build_voice2.py`. Do NOT use vidIQ voice (costs credits) and do not use `cyto_voice.py` unless Utsha records his own voice.
- Ask Utsha before spending credits; `estimate_only` first; never re-call a generation to retry (double charge).
- Length: let the idea set it, up to 60s for scripts written from Nov 2 on (Ep 9 read = ~41.5s; Eps 10-14 reads are 36-43s and stay as is).

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
5. **Length (changed Nov 2, 2026):** series is now "6ixty Seconds of Science"; Shorts may run up to 60s (`C.MAX_T_V2` = 60, ~140-165 words at ~2.8 w/s). Only fill the time with real content (a new visual every 2-3s, one idea + payoff); never pad, because completion rate is what Shorts distribution rewards. Must still loop into the start. The pill label on every frame reads `6IXTY SECONDS OF SCIENCE`. Eps 10-14 are already scripted/voiced at 36-43s and stay that way.

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

### 3D (Nov 2, 2026 — Ep 9 onward) — `hf/three3d.js` (three.js r149, `assets/three.min.js`)
Real 3D renders inside HyperFrames (WebGL via the headless shell). Style = cel-shaded ("toon") + ink outlines so it matches the cutout rig.
- Factories: `C3D.earth()` (winter-tilted Earth, sun, Toronto pin label), `C3D.bars()` (growing 3D bar chart, labels projected onto bar tops), `C3D.capsulesDna()` (vitamin capsules bounce, DNA helix rises). Each returns `render(t)`.
- Drive from the timeline with the `three()` helper in `hf/ep09/build.py` (onUpdate → render(t)) so seeks are frame-exact. Canvas needs `preserveDrawingBuffer:true` (the factories do it).
- Add new 3D pieces to `three3d.js`, not inside an episode. Keep lighting low (ambient ≤ 0.35) or toon colours wash out.
- Target mix per Short: ~3 × 3D shots, the rest 2D cutout + Lottie; max one chart, everything else is action (things moving, changing, reacting).

### Art library — `hf/art.py`
Flat cutout set pieces in the rig's style: `skyline()`, `city_hall()`, `night_bus()`, `streetcar()`, `stop_pole()`, `window()`, `lamp()`, `phone()`, `body_clock()`, `hypnogram()`, `moon()`, `stars()`. Outfits so far: jersey, PJ + sleep mask, puffer vest. Add new Toronto pieces here (not inside an episode) so every episode can reuse them.
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
| 9 | Is winter killing your vitamin D? (first 3D episode, ElevenLabs voice) | — | built, awaiting OK (Nov 6, 6 PM) |
| 8 | Why you wake up at 3am (first v2+v3 episode, new thumbnail system) | — | built, awaiting OK (Nov 5, 6 PM) |
| 11 | Diwali food coma (Scarborough-led, kurta outfit) | — | built, awaiting OK (Nov 8, 3 PM) |
| 12 | Movember: does checking yourself save lives? (first Scribe-timed + ElevenLabs-SFX episode) | — | built, awaiting OK (Nov 9, 6 PM) |

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

### Ep 9 lessons (Nov 2, 2026 — apply to every build)
- **Eyes looked "off":** glances were +-12..18px, pushing the pupils out of the eye and never recentring. Fixed in `cyto3.py` (glances are now clamped to ~+-7px / -6px and ease back to centre after ~1s). Don't pass big look values; use `looks` sparingly (1 per scene max).
- **Text and animations colliding:** give each scene three fixed zones and keep them apart: (1) top = figure/Lottie/3D, (2) middle = ONE headline or stamp at a time, (3) bottom = captions (C.CAP_Y_V2) + Cyto. Rules: max ONE big text element on screen at once (fade the previous one out before the next lands, >=0.15s gap); chips/cards must not overlap a stamp or the 3D label; Lottie sits beside text, never under it; no element within 40px of the caption band.
- **Check at 1 fps, not just key frames:** `npx hyperframes snapshot --at 0.5,1.5,2.5,...` for EVERY second (a 40s short = ~40 frames), build a contact sheet, and fix any frame where two text/graphic elements touch or Cyto's pupils leave the eye. Show Utsha only after this pass.

### SOURCE RULE (Nov 2, 2026): never reuse a PubMed source across Shorts
Each Short needs its own NEW source(s) from PubMed (ideally 2+ substantive ones). Check `studio/sources_used.md` and run `python3 studio/check_sources.py` before scripting. If a topic overlaps an earlier episode, pick a different angle with different papers. Long-form may cite earlier sources.

### TORONTO BACKGROUND RULE (Nov 2, 2026, from Utsha after Ep 10). City of Toronto only (Scarborough, Etobicoke, North York, East York, York, old Toronto all count); NO Brampton, Mississauga or other GTA cities. Ep 11 is Scarborough-led.
Every scene's background/props must be Toronto-specific or topic-specific, never random filler. Use niche local detail: TTC streetcars and Line 1 platforms (Bloor-Yonge, Union), Union Station, the CN Tower silhouette, Nathan Phillips Square rink, the Toronto Island ferry, Gerrard India Bazaar, Queen's Park, Kensington, raccoons, condo cranes, snow/slush. Use generic shapes only: no real logos, store names, brands or people. Each brief has a "Toronto background plan" section: follow it scene by scene, and add one extra small Toronto Easter egg per scene if it doesn't clutter the frame (still max ONE big text at a time).

### MANDATORY AUTOMATIC CHECK: `layout_check.py` (added Nov 2, 2026 after Ep 10's overlaps and fake score)
After `python3 epNN/build.py`, run from /home/claude/hf: `python3 layout_check.py epNN --brief <path to studio/episodes/epNN/EPNN_brief.md>`. It loads the page, seeks the timeline every 0.25s and FAILS on: text overlapping text or captions, text cut off by the screen edge, text covered by a Lottie animation, pupils off-centre (>8px), and on-screen score-like text or numbers that are not in the brief. **0 FAIL is required before you show Utsha anything**; read every WARN and fix or justify it. Fix, rebuild, re-run. It does NOT replace the 1-fps visual contact-sheet review, which is still required (it can't see graphics-vs-graphics clashes or a stat chart that looks wrong).
**Content rule:** never put an invented number, score, quote or record on screen. A scoreboard for a game that hasn't happened shows "TONIGHT 7:00", never a score. Every figure on screen must come from the brief's sources or script.

### Ep 11 lessons (Nov 2, 2026)
- **Some Lotties render blank in the final HyperFrames video** even though they show in a plain browser: `zzz-a` (PNG image layers) and the thin-stroke `fireworks-1/2`. Check the real mp4 (ffmpeg frame grabs), not just `snapshot`. For Zzz and fireworks use native SVG + GSAP instead (`zzz()` / `burst()` in `hf/ep11/build.py`); vector Lotties like `diya-1` and `rangoli-1` render fine.
- **`wt()` matches by prefix**: `wt("say")` hit "says", `wt("So")` hit "solid", `wt("Yo")` hit "you're". Always pass the `after=` time for short words.
- **GSAP x/y on an SVG `<g transform="translate(...)">` replaces the translate.** Wrap it: outer `<g transform>` for placement, inner `<g id>` for the animation.
- New art.py pieces: `scarb_skyline`, `balcony` (+raccoon), `diya`, `bluffs_view`, `platform_view`, `hallway`, `il1_cell`, `mithai_plate`, `couch`, `rangoli`, `string_lights`, `stomach`. Outfit `outfit_kurta`. `three3d.js` bars take `floorW` for 3 bars.
- Python Playwright for `layout_check.py`: `pip install --break-system-packages playwright==1.63.0` (must match the preinstalled browser build).

### Ep 11 review: rules for Eps 12+ (manager review, Nov 2, 2026)
Ep 11 passed layout_check but a human review of the 1-fps sheet still found these. They are now hard rules:
- **Nothing within 40px of any screen edge**, including meters, labels, stamps and bars (Ep 11's "TIRED" meter label sat on the left edge and looked clipped). Treat every layout_check safe-zone WARN as a FAIL unless it is a deliberate slide-in/out of a moving object (e.g. a bus entering).
- **On-screen sources card: text at least 34px tall at 1080 wide**, max 2 sources, short form ("Orr 1997 · Lehrskov 2018"). Full citations live in the description and pinned comment. Small unreadable text defeats the point of crediting.
- **Hook (0-3s): at most 3 moving things** (e.g. background, one caption, Cyto). No bus + diyas + raccoon + caption pile-up. The first caption is the hook.
- **Use the space.** Cyto sits low-left; put the science figure/card in the upper-middle (y 300-1100) at full size. Do not leave the bottom third empty AND the figure tiny. Figures should fill their card.
- Check Lotties in the REAL rendered mp4 (ffmpeg frame grabs), never just in the preview. Blank Lotties: replace with native SVG + GSAP.
- No captioning tool is available: match the audio to the script line by line using segs.json pauses, then listen once and fix drift over 0.3s.
- Say in the final post: layout_check result (FAIL/WARN counts and what each WARN is), and the three things you are least sure about.

### Ep 12 lessons (Nov 3, 2026): test upgrades that worked, roll into Eps 13+
- **No drag-and-drop needed for ElevenLabs audio.** The sandbox can't reach elevenlabsusercontent.com, but GitHub Actions can: add `name url` (the signed `full_res_url` from `creative_get_generations`) to `audio/list.txt` and push. The `fetch-audio` workflow commits it within ~1 min (check `audio/status.txt`). Find an existing read with `creative_list_flows` → `creative_get_flow` → `creative_get_flow_node` (generations).
- **Word timing = ElevenLabs Scribe, 0 credits.** `creative_add_flow_asset_node(generation_id)` returns the TTS node itself; pass it as `connect_from` to `creative_transcribe_audio` (eleven_scribe_v1). Save the words as `epN/words_scribe.json` (caption spellings: 6ix, styll, 95%) and use `epN/make_segs.py` (`segs` builds segs.json from silencedetect + words; `remap` shifts the Scribe times through build_voice2's re-spacing into timing.json). Captions and visemes then land on the real word onsets instead of syllable-split guesses.
- **SFX via `creative_generate_in_flow` node_type `sfx`, model `eleven_text_to_sound_v2`, generations_count 1.** estimate_only said 50 cr, the real bill was ~16.7 cr each. Fetch them the same way (audio/list.txt). Mix each at unit RMS × voice RMS × -18 dB (hits -15) so they sit under the voice; music bed at -24 dB. Trim the 2s pop to 0.35s.
- **rig3_html now takes `face_extra` / `toque_extra`** (inline SVG on the face/toque, moves with Cyto). Ep 12 uses `art.handlebar()` (moustache sticker) and `art.awareness_ribbon()`. `thumb.py` passes the same keys from the spec.
- New art.py pieces: `univ_ave` (hospital row + Queen's Park), `subway_platform` (Bloor-Yonge hanging sign + NEXT TRAIN board, `{idp}Train`), `clinic_street` (Danforth-style walk-in clinic), `ferry_view` (skyline from the Island ferry), `handlebar`, `awareness_ribbon`.
- layout_check gotchas: an en-dash range like "15–45" is read as a score, so write "15 TO 45". Wall text hidden behind a semi-opaque panel still counts as overlapping text; move it, don't hide it.
- Lotties that came out blank even in a plain browser: ribbon-1/2, calendar-1; stache-2 was blank in the HyperFrames frames → used SVG + GSAP. Fine in the real mp4: shield-2, steth-1, heart-beat.
- `thumb.py` needs an ABSOLUTE out_dir (a relative path gives blank white PNGs).

### Cup rule (Nov 2, 2026, from Utsha)
The red cup is ALWAYS drawn IN FRONT of Cyto's hand and body, never behind the hand. `cyto3.py` now draws the hand first and the cup on top. In every build, check frames where the cup is held, raised and tipped: the cup must be fully visible and the hand must not sit on top of it.

### Ep 13 lessons (Nov 3, 2026)
- **Neutro** (neutrophil bouncer) is a vector rig: `hf/neutro.py` (source `studio/rig/neutro/neutro.py`, design frame `neutro_design.png`). `neutro_html(idp, pose)` + `neutro_js(idp, poses, mouths, brows, nods, looks, blinks)`; poses idle/cross/flex. Wrap him in an outer div for placement (CSS scale); never `pop()` that wrapper (GSAP scale overrides the CSS scale) — tween to the wrapper's own scale instead.
- New outfit `outfit_hoodie` (hf/outfits/hoodie.svg -> studio/rig/outfit_hoodie.png). New art: `union_station`, `raccoon`, `go_train`, `queen_snow`, `pharmacy_nps(py=, shop=)`, `virus`, `lungs`.
- **Playwright gotcha:** `page.evaluate("window.__timelines.main.seek(t)")` HANGS (it tries to serialise the timeline). Use `void (...)`. In a plain browser all `.clip` scenes are visible; toggle visibility from data-start/duration for contact sheets.
- **Frame 0:** the last zoom/whip transition's fromTo rendered its from-values at t=0 (1.5x zoom) and `#cytoPos` wasn't placed until the playhead moved. Fix: `immediateRender:false` on transition fromTo + `gsap.set("#cytoPos", POS_HOOK)` at build time.
- Cards slide in from x:90 with a fade (the old x:600 slide was flagged as cut off). Big headlines: left 60 / width 880 to stay inside the safe zone (right edge 940).
- Hidden art still counts in layout_check (off-screen svg text = safe-zone WARN); use `display:none`, not a translate.

### LF02 lessons (Nov 3, 2026) — long-form FORMAT v2 build (cartoon episode, 1920x1080)
- **Build lives in `studio/hf/lf02/`** (copy to /home/claude/hf/lf02): `audio.py` (cuts every line out of the per-character takes with Scribe words + `lines.json`, sequences them with comedy gaps + silent action beats -> dialogue.wav + timing.json), `chars.py` (Neutro officer, Mito, Rhino + one shared face/expression system: smug/shocked/deadpan/hype/exhausted/determined/sideeye/worried; `cyto_expr_js` adds the same names to Cyto), `sets.py` (HQ, court, noir office, nose door...), `lib.py` (Scene class: local times, captions coloured per speaker, cast, camera punch/snapzoom/shake/parallax, transitions split across the cut, popups), `scenes.py` (s01..s17), `mix.py` (synth music beds per scene + SFX, ducked under speech), `snap.py` (fast 1-fps sheets), `lc_all.sh`, `render_all.sh`. LF01's hf build was never committed, so LF02 rebuilt the landscape template from scratch: commit the hf folder this time.
- **One HyperFrames composition per scene** (3-43s each) rendered separately and concatenated with ffmpeg; audio is mixed once for the whole episode and muxed at the end. ~7 fps at 1920x1080 with 4 workers (5:27 = ~25 min).
- **layout_check now takes `--size landscape --root <dir>`** (40px margin, no Shorts UI). Wall signs drawn as SVG `<text>` count as text: give them `class="settxt"`; `S.popup` and transitions fade `.settxt` out under pop-ups. Pop-ups that restore it at their end can re-show a sign under a later card (s17): re-hide after each pop-up.
- **gw()/S.w() prefix matching bites harder in long lines**: "The" matched "the pickup", "And" matched "and hit". Use a distinctive word ("signal", "they") or `after=`.
- GSAP `x` on a wrapper div is a RELATIVE translate: move characters with offsets (x:+560), never absolute stage coords.
- three.js shots render fine inside HyperFrames (WebGL in the headless shell): body-city fly-through, adrenal condos, beating heart, nose lasers (`assets_src/three_lf02.js`, `C3D2.*`). No pre-render step was needed.
- ElevenLabs SFX still bill ~16.7 cr each; 6 hero SFX = ~100 cr. Everything else (buzz, whoosh, coin, level-up, typewriter, rain...) is synthesized in `mix.py` for 0.

### LF02 fix lessons (Nov 3, 2026) — what made the handoffs feel like a real conversation
- **Gap rules beat "comedy timing" padding.** Cut every line at first word -0.03 s / last word +0.05 s (push the tail to the energy valley, but NEVER past the next word of the same take: the takes are read back-to-back and the old +0.14 s tail leaked the next line's first syllable). Then lay lines on ONE timeline by handoff type (`audio.py` GAP table): reply 0.14 s, fast banter 0.05 s, interruption -0.08 s (next line starts under the tail, tail ducked -6 dB), punchline setup 0.42 s, "..." hold 0.58 s, same speaker 0.30 s, list item 0.36 s. Silent action beats max 1.0 s speaker-to-speaker (dunk/heist/seccam/achoo max 2.0 s and FILLED with SFX + visible action). Result: 45 speaker changes, median 0.14 s (was ~0.5 s with eleven gaps of 1.1-4.8 s); 5:27 -> 4:42.
- **timing.json t0/t1 = speech, not the cut.** Store first-word start / last-word end so a gap is just `next.t0 - prev.t1`; the cut window lives in `cut`.
- **One room for three voices:** per-line LUFS match (pyloudnorm, -21 LUFS) instead of peak/RMS, one shared 0.25 s / 4 % wet reverb on the whole dialogue bus, and a continuous room-tone bed per scene (HQ hum, crowd babble, body rumble, noir rain, city wind) so the track never drops to digital silence. silencedetect -45 dB/0.35 s is the check.
- **J-cut every scene change:** the scene boundary = next scene's first sound + 0.15 s (`cut_line()` / `cut_beat()` in lib.py); its music bed and room tone start 0.15 s before the picture with a 0.15 s crossfade. GOTCHA: a line that starts before the scene gives NEGATIVE GSAP positions, and a negative position shifts the whole paused timeline (Cyto rendered at the rig's default 1:1 for the first 2.5 s). `Scene.build()` now clamps every `},-x)` to 0.
- **Speaker camera, generic:** `Scene.talk_camera()` (wrapper `#tk` between `#shk` and `#cam`) pushes 7 % toward whoever talks, starting 0.15 s before the previous speaker finishes (anticipation), eased 0.25 s; runs of >= 3 quick alternating lines (<= 2.6 s, gaps < 0.45 s) become hard-cut shot / reverse-shot at 1.24x; monologues re-frame (push <-> medium) at sentence ends every >= 2.8 s. Disable with `S.talk_scale = 0` for VO over photos / 3D, or per line with `S.talk_off`. A second wrapper `#drift` adds a slow push so nothing is ever locked off.
- **Listener rules:** `close_listener()` maps any open mouth (grin/o/small/a/e; Cyto: small/a/e/o/u/fv) outside the character's own words to a closed one and logs it (I12 check = mouth_log.json); `listener_looks()` turns every listener's eyes (and a 2.5 deg head lean) to the speaker for the length of the line; speakers get a brow pop + tiny inhale 0.12 s before their first word; `auto_reactions()` gives listeners one reaction at the key word of every other-speaker line > 1.5 s unless one is hand-placed within 1 s.
- **Transitions = camera moves, never colour frames.** The old whip was a full-screen gradient wipe and flash/iris/zoom faded to cream/white/navy = the "mini pause". Now: whip = 4-frame horizontal motion blur (SVG feGaussianBlur "70 0" on `#shk`) + 150 px pan at 1.13x (so no edge shows) out and in; cut = hard cut on a sound with a 6-frame punch-in. Every scene's first frame already has its cast on model.
- **Props act:** `S.prop_in(sel, t, "drop"|"pop"|"slide")` = anticipation > action (elastic overshoot) > 3 wobbles + sound. The alarm bell drops in at frame 3 and rattles for as long as the siren runs (`alarm_shake`).
- **Captions:** one fixed centred band (y 930), dark pill, whole phrase appears at once (word-by-word reveal left an empty dark pill + "one word alone" look), the spoken word does a small scale pop. Keep the per-word pop <= 1.07 or neighbours collide.
- **Real photos (photos.py):** paint out every brand (skyline: Scotiabank S, 2x BMO, TRUMP, Deloitte) with cv2.inpaint + feathered blur; Distillery: crop the right half (x >= 1290 of 2400) so the "PURE SPIRITS" sign and the person are gone. Grade 18-30 % toward the HQ night/magenta duotone, darken bright daytime plates (Queen's Park) ~0.8x, 1-2 px blur for plates, 8 px + 0.62x for backdrops. Characters over photos get `RIM` (light 1.5 px rim + soft drop shadow). Text over photos/3D always sits on `S.panel()` (dark panel).
- **3D clean-up:** max 3 heroes + a ground disc + fogged sky, one eased camera move (`sm(t/dur)`), HQ purple/magenta + one accent. The body-city fly-through was replaced by the real skyline -> Queen's Park photos. Heart: one hero, lub-dub squash & stretch on a bpm grid with a matching synth heartbeat SFX.
- **Python playwright** is not preinstalled for snap.py / layout_check.py: `pip install playwright==<node playwright version>` (1.63.0 here) — never `playwright install`.


### LF02 v3 lessons (Nov 4, 2026) — story flow + limb rigs (the new minimum standard)
- **Flow bible lives in code**: `lib.Scene.tr_out/tr_in("doors", label=...)` = the subway-doors wipe with a NEXT STOP sign, ONLY on a change of place/chapter (A closes over its last 0.34 s, B opens at 0.12 s, cut = beat start + 0.45 s). Everything else is a straight cut. `S.location(title, sub)` = location card + establishing hold (talk camera waits until `S.est`). `S.recap(t, n, text)` = <= 4 s clue card. The CASE sticker (top-left, `case_tracker`) threads the whole video; clue times live in `lib.CLUE_T / REVEAL_T`. Panels and source chips keep out of the top-left corner.
- **Rigs (`rig2.py` + `motion.py`)**: Neutro/Mito/Cyto arms are 2-segment IK limbs driven per frame (hand targets on arcs around the shoulder, elbow lags 1 f, hand/prop lags 2 f + overshoot). Poses are hand TARGETS (`rig2.NPOSE/MPOSE`), never opacity swaps. Mito = round body, arm 40 % of body height, mitten hands (relaxed/grip/fist/point), legs on hip pivots, separate ball (`ball=[(t0,t1,"dribble"|"held"|"hidden")]`). Eyes are procedural (pupil wrapper `#{idp}pg`, blink lid `#{idp}bk`, face-turn `#{idp}fT`): clamp <= 25 % eye width, 3-frame saccades, listeners look at the speaker and hold, 3-frame blinks every 2-4 s. NEVER tween those ids with GSAP (one owner per element).
- **GSAP on an SVG <g> with a transform attribute**: setting `y` replaces the translate -> the group jumps. Wrap in an inner group.
- `check.py SCENES` = mouth/collar/prop overlap, pupils-in-mask, closed-mouth-when-silent on every 2nd frame (DOM measurements). Run it before rendering.
- Python Playwright: `pip install playwright`, launch with `executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'` (never `playwright install`). Assets are NOT in git: `C.copy_assets(...)`, copy three.min.js + assets_src/three_lf02.js, run photos.py + cyto_png.py.
- Render: ~3.3x realtime per scene, 2 scenes in parallel is fine; do NOT run mix.py at the same time as encodes (OOM kill).
