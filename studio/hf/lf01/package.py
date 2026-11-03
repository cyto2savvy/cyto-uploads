"""LF01 package: meta.json, captions.srt, pinned_comment.txt (studio/episodes/lf01)."""
import json, re, sys
sys.path.insert(0, "/home/claude/hf/lf01")
import lf
OUT = "/home/user/cyto-uploads/studio/episodes/lf01"
def mmss(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
CH = [mmss(b) for b in lf.B[:8]]
NAMES = ["The Countdown", "What's in the smoke", "First hours", "The first week", "Weeks 2-4", "Months to years", "Cyto's tips", "The 6ix tour + sources"]
SRC = [("Jha P, et al. NEJM 2013 (21st-century hazards of smoking and benefits of cessation; Centre for Global Health Research, Toronto)", "https://doi.org/10.1056/NEJMsa1211128"),
       ("Tashkin DP. Annals of the American Thoracic Society 2013 (review)", "https://doi.org/10.1513/AnnalsATS.201212-127FR"),
       ("Bonnet U, Preuss UW. Substance Abuse and Rehabilitation 2017 (review)", "https://doi.org/10.2147/SAR.S109576"),
       ("Lapperre TS, et al. Respiratory Research 2007", "https://doi.org/10.1186/1465-9921-8-85"),
       ("Fairman BJ, et al. Drug and Alcohol Dependence 2023", "https://doi.org/10.1016/j.drugalcdep.2023.109837"),
       ("Walters KJ, et al. Addictive Behaviors 2023", "https://doi.org/10.1016/j.addbeh.2023.107902"),
       ("Hartmann-Boyce J, et al. Cochrane Database of Systematic Reviews 2021", "https://doi.org/10.1002/14651858.CD013229.pub2"),
       ("Theodoulou A, et al. Cochrane Database of Systematic Reviews 2023", "https://doi.org/10.1002/14651858.CD013308.pub2"),
       ("Livingstone-Banks J, et al. Cochrane Database of Systematic Reviews 2023", "https://doi.org/10.1002/14651858.CD006103.pub8"),
       ("CDC Office on Smoking and Health: 'Within 20 Minutes of Quitting' (2004 Surgeon General's Report)", "https://archive.cdc.gov/www_cdc_gov/tobacco/sgr/2004/posters/20mins/index.htm"),
       ("WHO: Health benefits of smoking cessation", "https://www.who.int/news-room/q-a-detail/health-benefits-of-smoking-cessation"),
       ("Health Canada: Canadian Cannabis Survey 2024 (canada.ca)", None)]
desc = f"""What happens when you quit smoking, whether it's cigarettes, weed or grabba? Cyto counts it down from the 6ix: 20 minutes, 12 hours, week four, one year and fifteen years. Plus the one trigger that makes people slip, and how many years of life you can get back.

Quick version: within 20 minutes your heart rate starts dropping. By 12 hours, carbon monoxide in your blood is back to normal. Regular weed smokers can get a real but mostly light-to-moderate withdrawal (mood and sleep), and cannabinoid receptors start resetting within about two days and are back to normal function around week four. Tobacco-leaf wraps like blunts and grabba deliver real nicotine. By one year the extra heart disease risk is about half; by fifteen years it matches someone who never smoked. A study from Toronto's Centre for Global Health Research found smokers lose about a decade of life, and quitting at 25 to 34 gets back about 10 years (35 to 44: about 9; 45 to 54: about 6).

Cyto's tips: get a squad (counselling raised the odds of quitting by about 44% across 300+ trials), ask a pharmacist (combination nicotine replacement, or varenicline by prescription), know your trigger spots, replace the ritual, and remember one slip isn't a relapse.

Free support in Canada: Smokers' Helpline, call 1-877-513-5333 or text iQuit to 123456 (free, 24/7).

Chapters:
""" + "\n".join(f"{c} {n}" for c, n in zip(CH, NAMES)) + """

Sources:
""" + "\n".join(f"{a}{(' — ' + u) if u else ''}" for a, u in SRC) + """

Not medical advice. Talk to your doctor or pharmacist about quitting.

#quitsmoking #health #science #toronto #6ix"""
meta = {"format": "long", "keyword": "what happens when you quit smoking", "title": "What Happens When You Quit Smoking Weed & Tobacco",
        "description": desc,
        "tags": ["what happens when you quit smoking", "quit smoking", "quitting weed", "cannabis withdrawal", "quit smoking timeline",
                 "what happens when you stop smoking weed", "nicotine withdrawal", "smokers helpline", "toronto", "cyto the cell", "the body is the 6ix", "6ixty seconds of science"],
        "category_id": 27, "made_for_kids": False, "synthetic": True, "health": True, "duration_s": round(lf.B[-1], 1),
        "thumbnails": ["thumb-lf01-A.png", "thumb-lf01-B.png"], "thumbnail_pick": "thumb-lf01-A.png", "captions_srt": "captions.srt",
        "playlist": "Cyto Long-Form", "related_video": "Ep 13: Meet Neutro: Your Flu Season Bouncer",
        "end_screen": "Last 20s: subscribe element + best Short (Ep 13 Meet Neutro); the final line loops visually back to the hook frame.",
        "pinned_comment": open(f"{OUT}/pinned_comment.txt").read() if False else None,
        "publish_at": "2026-11-20T23:00:00Z", "privacy": "private until publish_at (channel one-month anniversary)",
        "outfit": "blue toque + heather-grey hoodie (outfit_hoodie), red cup = ATP smoothie held in front of the hand; Neutro (neutrophil security guard) in Ch1, Ch4, thumbnails",
        "video_file": "lf01/cyto-lf01-quit-smoking.mp4", "chapters": dict(zip(CH, NAMES)), "resolution": "1920x1080"}
pinned = ("What's the hardest part, the habit or the craving? 👇 I read them all.\n\n"
          "Sources: Jha 2013 (NEJM) · Tashkin 2013 (Annals ATS) · Bonnet 2017 (Subst Abuse Rehabil) · Lapperre 2007 (Respir Res) · Fairman 2023 (Drug Alcohol Depend) · "
          "Walters 2023 (Addict Behav) · Hartmann-Boyce 2021, Theodoulou 2023, Livingstone-Banks 2023 (Cochrane) · CDC/Surgeon General 2004 · WHO · Health Canada CCS 2024. "
          "Full links in the description.\n\nFree help: Smokers' Helpline 1-877-513-5333 or text iQuit to 123456. Not medical advice.")
meta["pinned_comment"] = pinned
open(f"{OUT}/pinned_comment.txt", "w").write(pinned + "\n")
json.dump(meta, open(f"{OUT}/meta.json", "w"), indent=1, ensure_ascii=False)
# captions.srt (same chunks/spellings as on screen)
cw = lf.cap_words(lf.ALLW)
chunks, cur = [], []
for i, w in enumerate(cw):
    cur.append(w)
    if len(cur) >= 7 or sum(len(x["w"]) + 1 for x in cur) > 38 or re.search(r"[.,?!:…]$", w["w"]): chunks.append(cur); cur = []
if cur: chunks.append(cur)
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
srt = []
for i, ch in enumerate(chunks):
    a = ch[0]["t0"]; b = ch[-1]["t1"] + 0.25
    if i + 1 < len(chunks): b = min(b, chunks[i + 1][0]["t0"] - 0.02)
    srt.append(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{' '.join(x['w'] for x in ch)}\n")
open(f"{OUT}/captions.srt", "w").write("\n".join(srt))
print("chapters", CH, "srt cues", len(srt), "desc words", len(re.findall(r'\b\w+\b', desc)))
