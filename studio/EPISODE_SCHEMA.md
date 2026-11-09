# make_episode.py + episode.json (manager, Nov 9, 2026)
One command per stage; stops at Utsha's two OK gates. `python3 studio/make_episode.py epNN [--ok plan|final] [--dry-run] [--stage validate|voice|build|thumbs|checks|package|schedule]`
Flow: IDEA chat writes `studio/episodes/epNN/episode.json` (+ claims.md) -> `--dry-run` -> Utsha OKs plan + credit estimate -> `--ok plan` -> voice -> build -> thumbs -> checks -> package (STOP, gate 2) -> Utsha OKs -> `--ok final` -> `schedule_request.json` (the chat runs it via Zapier).
Credits: the script spends NONE. It prints the ElevenLabs estimate (chars x 2 takes) and writes `voice_request.json` / `scribe_request.json` for the chat to run (Scribe = 0 credits). Never retry a generation call (double charge).
Never touches tiktok/queue.json (writes `tiktok_entry.json` only for Utsha to hand over).

```
{ "ep":15, "slug":"short-slug", "title":"<=60 chars", "health":true, "fit":"hoodie|jersey|puffer|none", "seed":7,
  "publish_at":"2026-11-12T23:00:00Z", "keyword":"first tag (default: title lower)", "hashtags":["#topic1"],  (brand #shorts #science #toronto #6ix auto-added)
  "script":[{"say":"caption spelling, e.g. 6ix","tts":"optional ear spelling","scene":0,"emotion":"chill|happy|shock|think|solemn|laugh","emotion2":"","gaze":[x,y],"pause_after":0.5}],
  "scenes":[{"bg":"skyline|streetcar|snow|subway|lake|plain","headline":"LINE1\nLINE2","hot":["WORD"],"card":"text","transition":"whip|doors|zoom|membrane"}],
  "keys":{"word":"#hexcolor"}, "thumbnails":[{"id":"A","headline":["2 MINUTES","OF SILENCE"],"hot":["SILENCE"],"hero":"heart|clock|snow|brain|phone|sugar","emotion":"shock"},{"id":"B",...}], "stronger":"B",
  "sources":[{"short":"Author Year, Journal (on screen)","full":"citation + PubMed link (description)"}],
  "description":"must contain 'Not medical advice' if health", "tags":[...], "pinned_comment":"question + sources in description", "related_video":"Ep N (id)", "playlist":"6ixty Seconds of Science", "outfit_note":"" }
```
Rules enforced: script scenes in order, every scene has a line, <=60 s speech, 2 thumbnails + `stronger`, no real brands, no drinking refs, sources short+full, 0 FAIL in pipeline/check_meta.py.
Checks (report.json, any FAIL stops): layout safe zone/overlap, nothing static >1 s, face moves every 1 s, cup visible (frames inside transitions skipped), captions >=60 px, sources card >=34 px, canon 29/29, rig 15/15. Contact sheet = `contact_sheet.jpg` (1 fps, from the real mp4). Thumbs: A/B in 1280x720 + 1080x1920 plus `feed_check-<id>.jpg`.
Audio: voice + soft pad (ducked) + whoosh per cut, loudnorm -14. Words need Scribe timings (`words_scribe.json`, token count must equal `say` words).
Fixture proof: Ep 14 data renders in ~2 min (957 frames), 0 layout fails, 0 FAIL meta.
