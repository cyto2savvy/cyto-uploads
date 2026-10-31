# Cyto studio: how it works (read this first in a new chat)

**Restore:** `git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh`
The scripts expect the original paths (`/home/claude/cyto2`, `/home/claude/epN`, `/home/claude/hf`), and restore.sh recreates them.

**Scripts:** read `studio/VOICE.md` before writing any script (Toronto slang bank, references, body map, checklist). Required from Oct 30, 2026.

## Pipeline (all $0)
1. **Research:** PubMed connector for the sources, and WebSearch for Toronto events and trends.
2. **Voice:** vidIQ voiceover, voice **Liam** (about 14 credits per 1000 characters, so ask Utsha before spending). The cloud workspace can't download the vidIQ MP3 (S3 is blocked), so Utsha drags it into chat.
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
6. **Upload (Zapier, YouTube app `YouTubeV4CLIAPI`).** Always pass `connection_id` `02a2f56e-1e01-8a41-9364-13e401f8bd6b`.
   - `upload_video` with `privacy_status: private` and `publish_at` (UTC), `category_id: 27`, `made_for_kids: false` and PubMed links in the description.
   - Then `_zap_raw_request` (tool `youtube_make_api_mutating_request`): PUT `videos?part=status` with `containsSyntheticMedia: true`, and keep `publishAt` + `privacyStatus: private`.
   - GET requests use `execute_zapier_read_action` with tool `youtube_make_api_get_request`.
   - Uploads playlist: `UUJRfXFQKUTWj-2LfA1cAWtA`.
   - **"Throttled" errors:** check the uploads playlist before retrying, since sometimes it did succeed. Space retries about 1 hour apart.
   - **Thumbnails:** they fail with a 429 until the channel is phone-verified (youtube.com/verify). Until then Utsha sets them in Studio.
7. **TikTok:** add the approved episode to `tiktok/queue.json`. Utsha's friend's Claude posts from it (see `tiktok/INSTRUCTIONS.md`).

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

## Watch: vidIQ credits
Oct 30, 2026: 40 credits left, 0 renewable until Nov 30 (~5 Liam voiceovers). Spend credits on voice only until Boost is active.
