# TikTok posting: instructions for Claude

You're helping post **"The Body is the 6ix"** (Cyto the Cell) Shorts to TikTok from this Mac. Utsha makes and approves every episode. Your job is only to post approved episodes to the TikTok account the person you're working with is already logged in to.

## Source of truth
- Queue: https://raw.githubusercontent.com/cyto2savvy/cyto-uploads/main/tiktok/queue.json
  Re-read it at the start of every session, because new episodes get added daily.
- Repo (public, read-only for you): https://github.com/cyto2savvy/cyto-uploads

## Rules
1. **Only post entries with `"status": "approved"`.** Never post anything else from the repo, and never edit the video.
2. **Use the caption exactly as written** in `caption`. Don't add, remove or change hashtags or text.
3. **Turn ON TikTok's "AI-generated content" label** for every post (More options → AI-generated content). The voice and character are AI-made. TikTok requires this label, and the channel's rules do too.
4. **Use the video's original sound.** Don't add TikTok music, filters, stickers or effects.
5. **Post time:** `post_at_toronto_time` is Toronto (Eastern) time. Convert it to this Mac's local time zone before scheduling. If that time has already passed, post right away, but space posts at least 2 hours apart.
6. **Scheduling:** use TikTok Studio's web scheduler (tiktok.com/tiktokstudio/upload). It only allows scheduling about 10 days ahead, so schedule anything inside that window.
7. **Never post twice.** Keep a log at `~/Cyto/tiktok-posted.json`, a list of `{episode, posted_or_scheduled_at, tiktok_url_if_known}`. Check it before each post and update it right after. If you're unsure whether something already went up, check the account's TikTok Studio content list before posting.
8. **Don't handle the login.** The person logs in to TikTok themselves. Never ask for or type their password or 2FA codes.
9. Comments, DMs, account settings and the bio are out of scope. Stop and ask before doing anything outside posting.

## How to post one episode
1. Download the video to `~/Cyto/videos/` (make the folder if it doesn't exist):
   `curl -L -o ~/Cyto/videos/<episode>.mp4 "<video_url>"`
   Check the file is over 1 MB and plays (`ffprobe` or open it). It should be a 1080×1920 video of about 30–35 seconds.
2. In Chrome (Claude in Chrome), open https://www.tiktok.com/tiktokstudio/upload. If it's not logged in, stop and ask the person to log in.
3. Upload the file from `~/Cyto/videos/`, then paste the caption exactly.
4. Set **Who can watch: Everyone**. Allow comments, Duet and Stitch.
5. Open More options and turn on **AI-generated content**.
6. Pick **Schedule** with the converted local time, or **Post** if the time has already passed.
7. Wait for the confirmation, then write the entry to `~/Cyto/tiktok-posted.json`.
8. Report back in one line: episode, posted or scheduled, and the time in both Toronto time and local time.

## If something goes wrong
- If TikTok shows an error or a copyright or "content check" warning, stop that post and report the exact message. Don't retry more than once.
- If the download fails, report the URL and the error. The file may not be pushed yet.
- If the upload page layout looks different from these steps, take a screenshot, describe it and ask before guessing.
