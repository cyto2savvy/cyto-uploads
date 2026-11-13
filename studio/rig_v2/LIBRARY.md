# rig_v2 LIBRARY — reuse these ids, don't draw new things (HARD_RULES 19)

Everything an `episode.json` scene can use, with its parameters and a copy-paste example.
Render the picture of all of it: `python3 studio/rig_v2/library_render.py` → `studio/rig_v2/library.png`.

**Rule:** the idea chat picks ids from this file. Only ask for a NEW visual when nothing here fits; whoever draws it adds
it to props.js/backdrops.js **and to this file plus library.png the same day**, so the next episode can reuse it.

---

## 1. Scene shape

```json
{ "bg": "hospital", "transition": "whip", "headline": "NOT JUST\nPATIENTS?", "hot": ["PATIENTS?"], "card": "",
  "props": [ {"t": "peopleGrid", "n": 36, "cols": 12, "hi": 9, "label": "889 PATIENTS", "at": [540, 0.34], "fill": 0.62, "in": 0.0} ] }
```

| key | meaning |
|---|---|
| `bg` | backdrop id (§3). Two scenes in a row may not share one (HARD_RULES 6). |
| `transition` | `whip` \| `zoom` \| `membrane` \| `doors` (§4). Ignored on the first scene. |
| `transitionDur` | optional, 0.35–0.5 s. Default 0.42. |
| `headline` / `card` | text, `\n` for a line break. headline + card ≤ 8 words for the whole scene. |
| `hot` | words in the headline painted gold. |
| `instant` | `true` on scene 0 only: the headline is fully on screen at frame 1 (hook-first). |
| `props` | 0+ entries (§2). From Ep 16 every prop needs `shows` + `anchor` (HARD_RULES 21); catchphrase and outro scenes have none. |
| `dim` | optional 0..1 navy wash over the backdrop so props/headline read on a busy one (hospital, subway). |

### Every prop takes these
| key | meaning |
|---|---|
| `t` | prop id (§2) |
| `at` | `[x px, y as 0..1 of the prop stage]`. The stage is the band between the headline/card and Cyto's head. |
| `fill` | share of the stage **height** this prop takes. Hero ≈ 0.6–0.9, mid ≈ 0.3–0.5, accent row ≈ 0.15–0.26. Props scale **up** to this. |
| `scale` | optional extra multiplier on top of `fill`. |
| `shows` | REQUIRED: one line saying what the prop illustrates ("about 17 percent lower odds"). |
| `anchor` | REQUIRED: the spoken word (in that scene's script) the prop appears on. make_episode turns it into `in`, and into `out` = end of that sentence + 1.5 s. |
| `lead` | optional, ≤ 1.0 s: arrive this long before the anchor word (e.g. the hook's first prop at frame 1). |
| `hold` | optional, ≤ 1.5 s: leave sooner after the sentence (use it to clear the stage for the next hero prop). |
| `in` | set by make_episode from `anchor` (Ep 16+). Only hand-written in pre-Ep 16 episodes. |

**Placing props so they don't collide** (HARD_RULES 17 fails the build on > 0.3 s of overlap): stack them down the stage,
`at[1]` ≈ `fill/2`, then `fill1 + gap + fill2/2`, etc. Two props side by side need their widths to fit 70–1010 px.

**Timing** (HARD_RULES 5): two props must be fully on screen by 0.5 s, and something new has to arrive every ≤ 2 s.
Props with `spread` keep producing new elements for that long, which is the cheap way to cover a long scene.
A scene's first prop should be readable within ~0.2 s of the cut — a grid with a long `spread` looks empty if it is the only thing there.

---

## 2. Props

| id | what it is | parameters |
|---|---|---|
| `organ` | drawn organ with a label chip, pulses | `kind`: `colon` \| `lungs` \| `prostate` (Ep 16: bladder + gold gland diagram) \| `brain` (Ep 17: the thumbnail-hero brain as a scene prop); `label` |
| `bars` | bars that grow with counting values | `values`: `[80,74]`; `labels`: `["EXERCISE","PAMPHLETS"]`; `unit` (default `%`). Tallest bar goes gold. |
| `counter` | number rolling up over a crowd of dots that fills in | `to`; `suffix` (e.g. `M`); `decimals`; `label`; `dur` (default 1.3) |
| `arrowStat` | big arrow that draws on, number in a gold stamp at the head | `dir`: `down` \| `up`; `label` |
| `icons` | row/grid of glyphs popping in one after another | `glyph`: `person` \| `organ` \| `shoe` \| `cell` \| `check`; `n`; `cols`; `spread` (seconds to place them all) or `step`; `label`; `hi` (first N go gold) |
| `peopleGrid` | crowd of person icons filling in | `n`; `cols`; `hi`; `label`; `spread` |
| `card` | titled white card with a tick grid that fills | `title`; `ticks`; `cols`; `foot`; `dur` |
| `stamp` | rubber stamp that slams in and settles | `text` (`\n` ok); `color` (default red); `rot`; `plate` (`true` = white, or a colour: backing plate so it reads on a busy backdrop) |
| `shoe` | running shoe with motion lines | — |
| `runner` | cut-out jogger, limbs cycling | `color` (default gold — deliberately not Cyto's teal) |
| `stopSign` | TTC-style stop sign on a pole | `title`; `text` |

```json
{"t":"bars","values":[80,74],"labels":["EXERCISE","PAMPHLETS"],"at":[540,0.56],"fill":0.72,"in":0.3}
{"t":"counter","to":1.44,"suffix":"M","decimals":2,"label":"ADULTS","at":[540,0.28],"fill":0.54,"in":0.0}
{"t":"arrowStat","label":"-28%","dir":"down","at":[730,0.50],"fill":0.86,"in":0.2}
{"t":"icons","glyph":"organ","n":13,"cols":7,"label":"13 CANCERS","spread":4.4,"at":[540,0.80],"fill":0.40,"in":0.3}
{"t":"organ","kind":"colon","label":"COLON","at":[270,0.50],"fill":0.76,"in":0.0}
{"t":"peopleGrid","n":36,"cols":12,"hi":9,"label":"889 PATIENTS","spread":1.2,"at":[540,0.34],"fill":0.62,"in":0.0}
{"t":"card","title":"36 MONTHS","ticks":36,"cols":12,"foot":"AFTER CHEMO","at":[540,0.30],"fill":0.56,"in":0.0}
{"t":"stamp","text":"LINKED, NOT PROVEN","at":[750,0.28],"fill":0.26,"in":0.3}
{"t":"shoe","at":[760,0.34],"fill":0.40,"in":0.3}
{"t":"runner","at":[225,0.52],"fill":0.72,"in":0.0}
{"t":"stopSign","title":"TTC","text":"WALK IT","at":[238,0.52],"fill":0.88,"in":0.0}
```

---

## 3. Backdrops

Parallax layer sets (far → near) in `backdrops.js`. All take an optional `seed` via the scene's `seed`.

| id | what it shows | use it for |
|---|---|---|
| `trail` | dawn sky, lake, far shore, treeline, path | exercise, outdoors, movement |
| `hospital` | University Ave hospital row, red cross, ambulance | patients, trials, diagnosis |
| `lab` | bench, flasks, microscope, screen | studies, mechanism, "what researchers did" |
| `subway` | TTC platform, tiles, posters | the Toronto payoff, commuting |
| `streetcar` | night skyline + red streetcar | the city, going out |
| `skyline` | Toronto towers and CN Tower | only when the topic IS the city (HARD_RULES 1) |
| `lake` | waterfront at night, moon | calm, sleep, reflection |
| `snow` | winter sky and drifts | winter, cold, seasonal |
| `plain` | glow + rings, neutral stage | a big stat that should carry the frame alone |

---

## 4. Transitions

Every cut is 0.35–0.5 s, eases in and out, and keeps moving (HARD_RULES 8, 18).

| id | what it does | good for |
|---|---|---|
| `whip` | both scenes slide sideways with motion blur; Cyto leans into it | the default, high energy |
| `zoom` | old scene pushes past the camera, new one settles back | entering a detail or a figure |
| `membrane` | circular cell-wall reveal with an ink + teal ring | going inside the body |
| `doors` | subway doors close over the swap and open again | anything arriving at the TTC payoff |

---

## 5. What the checks will fail you on

| check | rule |
|---|---|
| `every declared prop was drawn` | each prop in episode.json shows up in the render |
| `no floaters` | a prop is on screen only from its anchor word to its sentence end + 1.5 s; catchphrase + outro have none |
| `variety vs last 3 episodes` | rule 20, see §6 |
| `a new thing moves in every <= 2 s` | gaps between prop arrivals |
| `no blank middle` | while a prop is up, y 25–65 % is never > 85 % flat backdrop for > 1 s |
| `no overlaps` | nothing covers anything else for > 0.3 s |
| `transitions smooth` | every cut including the first: no stall, no pop, Cyto's pose blends |
| `layout` | all text inside x 60–940, y 200–1480, nothing overlapping |
| `cup + Cyto fully inside the frame` | ≥ 40 px margin on the whole rig including the cup and steam |

---

## 6. Variety (HARD_RULES 20) and tags

- Tags + scene roles per item: `rig_v2/library_tags.json`. Last use per item: `rig_v2/library_usage.json` (rewritten by make_episode at package time and by `suggest_scenes.py --usage`; never edit by hand).
- Pick scenes: `python3 studio/suggest_scenes.py --for=epNN <topic tags>` prints 3 backdrop + prop sets per role (hook, explain, stat, limits, payoff, clean), topic fit first, then least recently used, none a combo from the 3 episodes before epNN.
- make_episode fails the episode before any credits are spent if: more than half the scenes repeat a backdrop+prop combo from the last 3 episodes, the backdrop order equals the previous episode's, there is no new or least-recently-used item, or a prop is reused with identical params.
- Vary reused items: `at`, `fill`, counts (`n`, `ticks`, `cols`), `color`/`plate`, `rot`, labels, `dur`/`spread`.
- Ep 17 added: organ kind `brain`.
- Ep 16 added: organ kind `prostate`, stamp `plate`, scene `dim`, prop `hold`/`lead`. Removed: decorative rings on `plain`, snow particles on non-snow backdrops (rule 21).
