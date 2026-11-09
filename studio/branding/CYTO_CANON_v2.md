# Cyto CANON v2 (approved by Utsha, Nov 8, 2026) — the look every future build follows
Source of truth: `branding/rebrand-v2/cyto2d.js` (SVG generator). Final art = `SEED=3`. Tests: `bash branding/rebrand-v2/run_tests.sh` (must stay 19/19).

## Style
Flat 2D cut-out, South Park style, thick dark outline (#0a1f24, 7px), with light 3D shading (gradient skin, soft drop-shadow). NOT full 3D.

## Parts (do not change without Utsha)
- **Body**: round teal cell, big, with spots. Outfit = SpongeBob-style: clipped to the body (jersey / hoodie / puffer; `FIT=` env). No overhang.
- **Eyes**: heavy half-lids, chill. **Pupils PARALLEL** (same offset in both eyes, never cross-eyed). Smirk, cheeks.
- **Hands**: round MITTENS. **No fingers anywhere** (not on the face, not on the cup).
- **Arms**: short tube arms drawn BEHIND the body/outfit edge so they come out of the sides; raised right arm holds the cup, left arm relaxed.
- **Toque**: blue and white, "6" patch, pom-pom, tilted -7deg.
- **Chain**: gold link necklace that wraps around the body under the face (clipped to the body), "6" medallion pendant with gems. Drawn ABOVE organelles/outfit, never covered.
- **Cup**: generic Toronto-style paper COFFEE cup: white body, red band, brown lid, small flat Cyto-face logo, steam. No real brand, no wave mark, no brand text. Never show what's inside, no drinking/drug references. Replaces the old double-stacked party cup everywhere.
- **Organelles** (nucleus, 2 mitochondria, Golgi, rough ER, lysosomes, ribosomes): visible inside the body, clipped to the body ellipse so they NEVER cover or poke outside the cell, never cover the chain/face. Placement is RANDOM per build (`SEED`) with out-of-place jitter, and they IDLE-DRIFT (SMIL, 4s/8s, seamless 8s loop).
- **Toronto**: CN Tower, skyline, stadium dome, lake reflections, red streetcar (cover/banner), snow, gold ring on the profile pic.

## Build commands
`SEED=3 node cyto2d.js` -> pfp.svg, cover.svg, banner.svg, fits.svg. `SEED=3 ANIM=1 node cyto2d.js` -> pfp_anim.svg (drift loop). `FIT=jersey|hoodie|puffer`.
Rendered finals: `cyto-profile-picture-1000.png`, `cyto-facebook-cover-1640x624.png`, `cyto-youtube-banner-2560x1440.png`, `cyto-outfit-options.png`, `cyto-organelle-drift-loop.mp4`.

## Animation rules (rig)
Cut-out puppet: mouth per syllable, blink every 2–4s, idle bounce, organelle idle drift, cup+hand ONE rigid group (see ep14_addendum no-twitch rules). Animation tests (`test_cyto.py`) check: valid SVG; SEED reproducible and random per seed; pupils parallel; organelles clipped; no fingers; cup generic; chain present; 4 outfits render; nothing outside the cell changes; motion exists; no jitter spikes; seamless loop; no twitch. Any new rig code must add its own check to that file before it is shown to Utsha.

## Asset pack (`branding/rebrand-v2/assets/`, built by cyto2d.js -> cyto_<fit>.svg)
`cyto-{none,jersey,hoodie,puffer}-transparent.png` (use these for thumbnails, end cards, b-roll stickers), `video-watermark-150-canon.png` (upload in YouTube Studio > Branding > Video watermark), `thumbnail-template-example-1080x1920.png` (headline top, huge Cyto with white sticker outline bottom).
RULE: every new thumbnail, watermark, end card and banner uses these canon assets. The old PNG-layer rig (`studio/rig/*.png`, `hf/cyto3.py`) is the OLD look; porting the video rig to canon v2 is the next build task (start with Ep 14).
