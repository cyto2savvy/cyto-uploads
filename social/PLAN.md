# Instagram + Facebook plan (Nov 8, 2026). Utsha is creating the accounts.
Goal: same Cyto Shorts, native uploads, 1 extra distribution channel each at no extra build cost.

## Account setup (Utsha, 20 min)
1. Instagram: handle as close to @thebodyisthe6ix as possible. Switch to a CREATOR account (I believe Business accounts get a more limited trending-audio library; check in-app). Bio: "Cyto the cell, live from the 6ix. Science in 30 seconds. Not medical advice." Link = YouTube channel.
2. Facebook Page "The Body is the 6ix" (same logo/banner as YouTube), linked to the Instagram account. Turn on 2-step login on both.
3. Use Meta Business Suite (free, business.facebook.com) to schedule the same Reel to Instagram + Facebook at once ("Share to Facebook" / both toggles).
4. Profile art: reuse YouTube avatar + banner (Drive /Cyto Assets).

## Specs (checked Nov 8)
- 9:16, 1080x1920, 30 fps, MP4. Instagram: crop-safe zone = keep key text/faces out of the top ~220 px and bottom ~350 px (socialcal.app). Facebook (Meta Ads Guide via postfa.st): keep ~14% top, 35% bottom, 6% sides clear of key elements; Facebook Reels now have no length limit; the feed crops Reels to 4:5.
- Instagram Reels can be up to 20 min, but recommended 30-90 s for educational; keep Shorts <= 30 s.
- ACTION for the builder: add an IG/FB safe-zone check to layout_check.py (captions and the big hook text inside the central 1080x1370 area). Our YouTube layout may put captions low; test before posting.
- Export from the ORIGINAL mp4, never the TikTok download (watermarks get down-ranked).

## Posting rules
- Turn ON Meta's AI label (AI info / "AI-generated") for every post (AI voice + animation). Same rule as TikTok/YouTube.
- Caption = hook line first (first ~125 chars show), 3-5 hashtags max (#science #toronto #6ix + 1-2 topic), sources + "Not medical advice", ends with a question people must answer. Same pinned comment as YouTube (pin up to 3 on Instagram, 1 on Facebook; manual).
- Original sound only. Optional later A/B: add a licensed in-app trending sound at ~10% under the voice on ONE Reel and compare reach; never download third-party audio.
- Reply to every comment in the first hour.

## Cadence (so each platform gets "fresh"): YouTube 6 PM -> TikTok 6 PM (friend) -> Instagram + Facebook next day 12:00 noon ET.
Launch week: post 5 best/most relevant videos 1/day (Ep 2, 3, 5 = our 3 highest-view videos, then Ep 12, 13) so the new accounts have content, then 1 per day following YouTube.

## Monetization on Meta
Facebook/Instagram have their own creator-payment programs with their own eligibility. I have NOT verified the current 2026 requirements: in Business Suite open "Monetization" and tell Claude what it says. Don't rely on it for revenue yet; treat it as audience growth (and a funnel to YouTube).

## Tracking
Weekly report adds: Instagram reach/plays + follows, Facebook reach, plus "viewed vs swiped away" on IG (Insights). Compare the same video across platforms to learn which hook works where.

## Who posts
Phase 1: Utsha posts via Business Suite (2 min per video, queue in social/queue.json). Phase 2: a posting Claude through Chrome with the same rules as tiktok/INSTRUCTIONS.md (login by Utsha only). vidIQ has an Instagram Reel publishing tool but it needs credits and a connected account: skip for now.
