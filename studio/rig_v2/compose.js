#!/usr/bin/env node
// CANON v2 COMPOSITOR: plan.json -> 1080x1920 mp4. Every scene is a cut-out set: parallax backdrop + drawn props (props.js)
// + headline/card + word captions, with Cyto composited on top (his pose is a pure function of t, so it blends across every cut).
// usage: node compose.js plan.json out.mp4 [audio.wav] [startSec endSec]     -> also out.layout.json (layout + props + static report)
// plan: {fps,duration,fit,seed,cytoX,cytoY,cytoSize,words:[{w,start,end}],beats:[{t,emotion,gaze?}],keys:{word:color},
//        scenes:[{id,bg,start,end,headline,hot:[..],card,props:[..],transition,snow}]}
//   bg: skyline|streetcar|snow|subway|lake|plain|trail|hospital|lab
process.env.SEED = process.env.SEED || '3';
const fs = require('fs'), path = require('path'), crypto = require('crypto'), { spawn } = require('child_process');
const { frameSvg, state } = require('./cyto_rig.js');
const { propHtml, normalize, PROPS } = require('./props.js');
const C = require('../branding/rebrand-v2/cyto2d.js');
const { chromium } = require('playwright');
const W = 1080, H = 1920, INK = '#0a1f24', GOLD = '#ffc83a';
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), ease = x => x * x * (3 - 2 * x);
const backOut = x => { x = clamp(x, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const TOP = 206, STAGE_BOT = 915, CAP_Y = 930;   // headline band / prop stage / captions; Cyto's head starts ~1095 so nothing sits on him

const { layers, snowDots } = require('./backdrops.js');

// ---------------------------------------------------------------- text blocks (sized in JS so the prop stage can start below them)
function hlMetrics(sc) {
  if (!sc.headline) return { fs: 0, h: 0, lines: [] };
  const lines = sc.headline.split('\n'), mx = Math.max(...lines.map(l => l.length));
  const fs = Math.round(clamp(780 / (mx * 0.76), 56, 118));   // 780, not 820: real Arial Black advance is wider than 0.76 em and the box must stay inside x60-940
  return { fs, lines, h: Math.round(lines.length * fs * 1.04) + 10 };
}
function cardMetrics(sc) {
  if (!sc.card) return { h: 0, lines: [] };
  const lines = String(sc.card).split('\n'), size = sc.cardSize || 46;
  return { size, lines, h: Math.round(lines.length * size * 1.16) + 46 };
}
function headlineHtml(sc, lt, dur, y, hasNext) {
  const m = hlMetrics(sc); if (!m.fs) return '';
  // (b) the headline lands WITH the cut (0.6 of the way through) instead of half a second after it, so the new scene is never wordless
  const t0 = sc.instant ? 0 : (sc.transition && sc.start > 0 ? (sc.transitionDur || 0.42) * 0.6 : 0);
  const hot = (sc.hot || []).map(s => s.toUpperCase()), inst = !!sc.instant;
  const p = inst ? 1 : backOut((lt - t0 - 0.1) / 0.4), fade = (hasNext ? 1 : clamp((dur - lt) / 0.25, 0, 1)) * (inst ? 1 : clamp((lt - t0 - 0.08) / 0.1, 0, 1));
  const body = m.lines.map(l => `<div>${l.split(' ').map(w => `<span style="color:${hot.includes(w.toUpperCase().replace(/[^A-Z0-9%'-]/g, '')) || hot.includes(w.toUpperCase()) ? GOLD : '#fff'}">${w}</span>`).join(' ')}</div>`).join('');
  // shrink-wrapped so the safe-zone check measures the real glyph box, not a full-width block (pop-in overshoots past 1.0)
  return `<div data-chk="headline" data-s="${p >= 0.98 ? 1 : 0}" style="position:absolute;left:50%;top:${y}px;width:max-content;max-width:880px;text-align:center;font:900 ${m.fs}px/1.04 'Arial Black','Inter',Impact,sans-serif;letter-spacing:1px;-webkit-text-stroke:${Math.round(m.fs / 9)}px ${INK};paint-order:stroke fill;text-shadow:7px 10px 0 rgba(10,31,36,.55);transform:translateX(-50%) scale(${Math.min(1, Math.max(.01, p)).toFixed(3)},${Math.max(.01, p).toFixed(3)});transform-origin:50% 0;opacity:${fade.toFixed(2)}">${body}</div>`;
}
function cardHtml(sc, lt, dur, y, hasNext) {
  const m = cardMetrics(sc); if (!m.h) return '';
  const c0 = (sc.instant ? 0 : (sc.transition && sc.start > 0 ? (sc.transitionDur || 0.42) * 0.6 : 0)) + 0.45;
  const p = backOut((lt - c0) / 0.38), fade = (hasNext ? 1 : clamp((dur - lt) / 0.25, 0, 1)) * (lt > c0 ? 1 : 0);
  return `<div data-chk="card" data-s="${p >= 0.98 ? 1 : 0}" style="position:absolute;left:50%;top:${y}px;transform:translateX(-50%) scale(${Math.min(1, Math.max(.01, p)).toFixed(3)},${Math.max(.01, p).toFixed(3)});transform-origin:50% 0;box-sizing:border-box;width:max-content;max-width:800px;background:#fff;color:${INK};border:7px solid ${INK};border-radius:30px;padding:16px 30px;font:800 ${m.size}px/1.16 'Arial','Inter',sans-serif;text-align:center;box-shadow:8px 11px 0 rgba(10,31,36,.45);opacity:${fade.toFixed(2)}">${String(sc.card).replace(/\n/g, '<br>')}</div>`;
}
function chunkWords(words) {
  const out = []; let cur = [];
  words.forEach((w, i) => { cur.push(i); const nx = words[i + 1]; if (cur.length >= 4 || /[.!?…]$/.test(w.w) || (nx && nx.start - w.end > 0.45) || !nx) { out.push(cur); cur = []; } });
  return out;
}
function captionsHtml(tl, t, chunks) {
  const W_ = tl.words; const ck = chunks.find(c => t >= W_[c[0]].start - 0.02 && t <= W_[c[c.length - 1]].end + 0.22);
  if (!ck) return '';
  const keys = tl.keys || {}, size = 74;
  const spans = ck.filter(i => t >= W_[i].start - 0.02).map(i => {
    const w = W_[i], bare = w.w.toLowerCase().replace(/[^a-z0-9%']/g, ''), col = keys[bare], big = !!col;
    const age = t - w.start, pop = backOut(age / 0.14);
    return `<span style="display:inline-block;margin:0 9px;color:${col || '#fff'};font-size:${big ? size * 1.22 : size}px;transform:scale(${(.6 + .4 * pop).toFixed(3)})">${w.w.toUpperCase()}</span>`;
  }).join('');
  return `<div data-chk="caption" style="position:absolute;left:60px;top:${CAP_Y}px;width:880px;text-align:center;font:900 ${size}px/1.05 'Arial Black','Inter',Impact,sans-serif;-webkit-text-stroke:9px ${INK};paint-order:stroke fill;text-shadow:5px 7px 0 rgba(10,31,36,.6)">${spans}</div>`;
}

// ---------------------------------------------------------------- one scene = backdrop layers + props + headline + card
function sceneStage(sc) {
  const hy = TOP, hh = hlMetrics(sc).h, cy = hy + Math.round(hh * 1.13) + 16, ch = cardMetrics(sc).h;   // *1.13 = room for the vertical overshoot of the headline
  return { hy, cy, top: (ch ? cy + Math.round(ch * 1.13) + 22 : hy + Math.round(hh * 1.04) + 18), bottom: STAGE_BOT };
}
function sceneComposite(sc, t, tl) {
  const hasNext = tl.scenes.indexOf(sc) < tl.scenes.length - 1;
  const lt = t - sc.start, dur = sc.end - sc.start, k = clamp(lt / dur, 0, 1);
  const L = layers(sc.bg, sc.seed || 5);
  const bg = L.map(l => `<div style="position:absolute;inset:0;transform:translateX(${(-26 * k * l.d).toFixed(2)}px) scale(${(1 + 0.085 * k * l.d).toFixed(4)});transform-origin:50% 58%">${l.s}</div>`).join('');
  const snow = (sc.snow === true || (sc.snow !== false && sc.bg === 'snow')) ? snowDots(t) : '';
  const st = sceneStage(sc);
  const props = (sc.props || []).map((p, i) => propHtml(p, lt, sc.id, i, (sc.props || []).length, st));
  return `<div style="position:absolute;inset:0;overflow:hidden">${bg}${snow}${sc.dim ? `<div style="position:absolute;inset:0;background:rgba(10,19,48,${+sc.dim})"></div>` : ''}${props.map(r => r ? r.html : '').join('')}` +
    `${headlineHtml(sc, lt, dur, st.hy, hasNext)}${cardHtml(sc, lt, dur, st.cy, hasNext)}</div>`;
}

const BL = b => b > 0.25 ? `filter:blur(${b.toFixed(2)}px);` : '';                       // below this, the blur is invisible but still forces a resample
const TF = (dx, k) => (Math.abs(dx) > 0.3 || Math.abs(k - 1) > 0.0015) ? `transform:translateX(${dx.toFixed(1)}px) scale(${k.toFixed(4)});` : '';
const TS = k => Math.abs(k - 1) > 0.0015 ? `transform:scale(${k.toFixed(4)});` : '';
// ---------------------------------------------------------------- transitions: whole composites move, constant speed, no frozen frame
function transitionHtml(t, tl, i) {
  const S = tl.scenes, sc = S[i], lt = t - sc.start, TD = sc.transitionDur || 0.42;
  if (i === 0 || lt >= TD || lt < 0) return null;
  // HARD_RULES 18: eased progress (smoothstep) so the cut accelerates out of the old scene and decelerates into the new one.
  // Linear progress made the motion stop dead on the last frame - that is the 'first cut is off' Utsha flagged.
  const xr = clamp(lt / TD, 0, 1), x = ease(xr), prev = S[i - 1], kind = sc.transition || 'whip';
  const a = sceneComposite(prev, t, tl), b = sceneComposite(sc, t, tl);   // both keep animating during the cut
  if (kind === 'zoom') {
    const za = 1 + x * 1.5, zb = 1.3 - 0.3 * x;
    return `<div style="position:absolute;inset:0;${TS(za)}opacity:${(1 - x).toFixed(3)};${BL(x * 9)}">${a}</div>` +
      `<div style="position:absolute;inset:0;${TS(zb)}opacity:${Math.min(1, x * 1.6).toFixed(3)}">${b}</div>`;
  }
  if (kind === 'membrane') {
    // circle(R%) is relative to the 1080x1920 diagonal/sqrt2 = 1558 px, and 80% already covers the frame from (50%,58%).
    // R = 80*x^0.62 reveals a near-constant slice of area per frame: no 2-frame hard cut, no stall.
    const r = 80 * Math.pow(x, 0.62), wob = 1 + Math.sin(x * 9) * 0.03, rr = (r * wob).toFixed(2);
    const full = r >= 79.5;   // once the circle covers the frame, drop the clip + ring so the last frame equals the plain scene
    return (x < 0.995 ? `<div style="position:absolute;inset:0;${TF(-14 * x, 1 + .05 * x)}">${a}</div>` : '') +
      `<div style="position:absolute;inset:0;${full ? '' : `clip-path:circle(${rr}% at 50% 58%)`}">${b}</div>` +
      (full ? '' : `<div style="position:absolute;inset:0;clip-path:circle(${rr}% at 50% 58%);box-shadow:inset 0 0 0 ${(9 * (1 - x) + 3).toFixed(1)}px ${INK},inset 0 0 0 ${(15 * (1 - x) + 6).toFixed(1)}px rgba(127,227,211,.55);pointer-events:none"></div>`);
  }
  if (kind === 'doors') {      // subway doors: panels never rest — they keep sliding and a light sweep crosses them
    const close = clamp(x / 0.52, 0, 1), open = clamp((x - 0.52) / 0.48, 0, 1);
    const w = (W / 2) * (close - open), shown = x < 0.5 ? a : b, sweep = (x * 2200 - 400).toFixed(0);
    const panel = (side) => `<div style="position:absolute;${side}:0;top:0;width:${Math.max(0, w).toFixed(1)}px;height:${H}px;background:linear-gradient(90deg,#b9c6d4,#dfe8f0 55%,#aab8c6);border-${side === 'left' ? 'right' : 'left'}:9px solid ${INK};overflow:hidden">` +
      `<div style="position:absolute;left:14px;right:14px;top:300px;height:620px;background:#2a4a6a;border:9px solid ${INK};border-radius:14px;opacity:.9"></div>` +
      `<div style="position:absolute;left:${sweep}px;top:0;width:180px;height:${H}px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-18deg)"></div></div>`;
    return w <= 1 ? shown : `${shown}${panel('left')}${panel('right')}`;
  }
  const tr = x * W * 1.06, bl = Math.sin(x * Math.PI) * 15;   // whip: eased slide, motion blur peaks mid-cut and clears at both ends
  return (x < 0.995 ? `<div style="position:absolute;inset:0;${TF(-tr, 1 - .04 * x)}${BL(bl)}">${a}</div>` : '') +
    `<div style="position:absolute;inset:0;${TF(W * 1.06 - tr, 0.96 + .04 * x)}${BL(bl)}">${b}</div>`;
}

function frameHtml(t, tl, chunks, cyto) {
  const S = tl.scenes; let i = S.findIndex(s => t >= s.start && t < s.end); if (i < 0) i = S.length - 1;
  const sc = S[i];
  const body = transitionHtml(t, tl, i) || sceneComposite(sc, t, tl);
  const cs = tl.cytoSize ?? 840, cxp = tl.cytoX ?? 64, cyp = tl.cytoY ?? 1110, k = cs / 1100;
  let lean = 0;                                    // smooth bump across each cut: he moves with the whip, then settles
  for (let j = 1; j < S.length; j++) { const TD = S[j].transitionDur || 0.42, u = (t - (S[j].start - 0.1)) / (TD + 0.22);
    if (u > 0 && u < 1) lean = Math.sin(u * Math.PI) * (S[j].transition === 'whip' ? 1 : 0.55); }
  // invisible markers so the overlap check (rule 17) can measure Cyto's face and his cup like any other item
  const mark = (name, x0, y0, x1, y1) => `<div data-chk="${name}" style="position:absolute;left:${(x0 + 550) * k}px;top:${(y0 + 550) * k}px;width:${(x1 - x0) * k}px;height:${(y1 - y0) * k}px;pointer-events:none"></div>`;
  const lt2 = lean > 0.004 ? `transform:translateX(${(-26 * lean).toFixed(1)}px) rotate(${(-2.2 * lean).toFixed(2)}deg);transform-origin:50% 80%;` : '';
  const cy = `<div style="position:absolute;left:${cxp}px;top:${cyp}px;width:${cs}px;height:${cs}px;${lt2}">${cyto}` +
    mark('face', -230, -160, 230, 60) + mark('cup', -500, -200, -150, 260) + `</div>`;
  return `<div id="f" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#0a1330">${body}${cy}${captionsHtml(tl, t, chunks)}</div>`;
}
const inTransition = (tl, t) => tl.scenes.some((s, i) => i > 0 && t >= s.start && t < s.start + (s.transitionDur || 0.42));

// ---------------------------------------------------------------- main
// Rendering is per SCENE segment, cached by a hash of everything that can change the picture (HARD_RULES 19):
// the scene, the previous scene (its composite is on screen during the incoming cut), the words/beats in range,
// the plan globals and the engine source. Unchanged scenes are copied from the cache, so a one-scene fix costs seconds.
const ENGINE = crypto.createHash('sha1').update(['cyto_rig.js', 'props.js', 'backdrops.js', 'compose.js', '../branding/rebrand-v2/cyto2d.js']
  .map(f => { try { return fs.readFileSync(path.join(__dirname, f)); } catch (_) { return ''; } }).join('|')).digest('hex').slice(0, 10);

function segKey(tl, i, i0, i1) {
  const S = tl.scenes, win = [S[i].start - 0.7, S[i].end + 0.7];
  const inWin = a => (a || []).filter(w => (w.end ?? w.t) >= win[0] && (w.start ?? w.t) <= win[1]);
  return crypto.createHash('sha1').update(JSON.stringify({
    v: 3, engine: ENGINE, scene: S[i], prev: i ? S[i - 1] : null, i0, i1, fps: tl.fps || 30,
    g: { fit: tl.fit, seed: tl.seed, dur: tl.duration, cx: tl.cytoX, cy: tl.cytoY, cs: tl.cytoSize, keys: tl.keys },
    words: inWin(tl.words), beats: inWin(tl.beats),
  })).digest('hex').slice(0, 16);
}

async function renderSegment(pg, tl, chunks, i0, i1, outFile) {
  const fps = tl.fps || 30;
  const part = { fails: [], overlaps: [], census: [], seen: {}, concurrent: {}, poseCut: {}, poseJerks: [], poseSpeed: 0, maxRun: 0, frames: i1 - i0 };
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', '-g', '30', outFile], { stdio: ['pipe', 'inherit', 'inherit'] });
  let pPose = null, pStep = null, prev = null, run = 0; const open = {};
  for (let i = i0; i < i1; i++) {
    const t = i / fps;
    const sc = tl.scenes.find(s => t >= s.start && t < s.end) || tl.scenes[tl.scenes.length - 1];
    const html = frameHtml(t, tl, chunks, frameSvg(t, tl, tl.cytoSize ?? 840));
    await pg.evaluate(([h, tt]) => { document.body.innerHTML = h; document.querySelectorAll('svg').forEach(e => { try { e.pauseAnimations(); e.setCurrentTime(tt); } catch (_) { } }); }, [html, t]);
    const ps = state(t, tl);                               // pose continuity across cuts (HARD_RULES 9/18)
    // head pose + brow only: eye saccades are meant to be fast, so they are not a "pose jump"
    if (pPose) {
      const d = Math.abs(ps.tilt - pPose.tilt) + 8 * Math.abs(ps.brow - pPose.brow);
      part.poseSpeed = Math.max(part.poseSpeed, d); const jk = pStep == null ? 0 : Math.abs(d - pStep); pStep = d;
      const cut = tl.scenes.find((s2, j) => j > 0 && t >= s2.start - 0.1 && t < s2.start + (s2.transitionDur || 0.42) + 0.1);
      if (cut) part.poseCut[cut.id] = Math.max(part.poseCut[cut.id] ?? 0, jk); part.poseJerks.push(jk);
    }
    pPose = ps;
    if (i % 3 === 0) {                                     // layout + prop + overlap census every 0.1 s
      const rs = await pg.evaluate(() => [...document.querySelectorAll('[data-chk],[data-prop]')].map(e => { const r = e.getBoundingClientRect(); return { k: e.dataset.chk || null, p: e.dataset.prop || null, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom, a: r.width * r.height, vis: +(getComputedStyle(e).opacity) > 0.3 && r.width > 4 && e.dataset.s !== '0' }; }));
      const props = rs.filter(r => r.p && r.vis && r.a > 400);
      if (!inTransition(tl, t)) {   // during a cut both scenes' props are on screen; counting them would inflate the census
        (part.seen[sc.id] = part.seen[sc.id] || []); props.forEach(r => { if (!part.seen[sc.id].includes(r.p)) part.seen[sc.id].push(r.p); });
      }
      if (t - sc.start > 0.5 && !inTransition(tl, t)) { part.concurrent[sc.id] = Math.min(part.concurrent[sc.id] ?? 99, props.length); part.census.push({ t: +t.toFixed(2), s: sc.id, n: props.length, ids: props.map(q => q.p) }); }
      if (inTransition(tl, t)) { for (const k2 of Object.keys(open)) delete open[k2]; }   // two composites are on screen mid-cut; both rules are static-layout rules
      else {
        // HARD_RULES 17: nothing covers anything else for more than 0.3 s
        const items = rs.filter(r => r.vis && r.a > 400 && (r.p || ['headline', 'card', 'caption', 'face', 'cup'].includes(r.k))).map(r => ({ n: r.p || r.k, ...r }));
        const now = new Set();
        for (let a = 0; a < items.length; a++) for (let b2 = a + 1; b2 < items.length; b2++) {
          const A = items[a], B = items[b2]; if (A.n === B.n || (A.n === 'face' && B.n === 'cup') || (A.n === 'cup' && B.n === 'face')) continue;
          const ov = Math.max(0, Math.min(A.x1, B.x1) - Math.max(A.x0, B.x0)) * Math.max(0, Math.min(A.y1, B.y1) - Math.max(A.y0, B.y0));
          if (ov > 0.02 * Math.min(A.a, B.a)) { const key = [A.n, B.n].sort().join(' x '); now.add(key); open[key] = open[key] || { t0: +t.toFixed(2), scene: sc.id }; }
        }
        for (const key of Object.keys(open)) if (!now.has(key)) { const d = +(t - open[key].t0).toFixed(2); if (d > 0.3) part.overlaps.push({ pair: key, scene: open[key].scene, t0: open[key].t0, dur: d }); delete open[key]; }
        const txt = rs.filter(r => r.vis && r.k && !['cyto', 'face', 'cup'].includes(r.k));
        for (const r of txt) if (r.x0 < 59 || r.x1 > 941 || r.y0 < 199 || r.y1 > 1481) part.fails.push({ t: +t.toFixed(2), what: `${r.k} outside safe zone`, box: [r.x0, r.y0, r.x1, r.y1].map(Math.round) });
        for (let a = 0; a < txt.length; a++) for (let b = a + 1; b < txt.length; b++) { const A = txt[a], B = txt[b]; if (A.x0 < B.x1 && B.x0 < A.x1 && A.y0 < B.y1 && B.y0 < A.y1) part.fails.push({ t: +t.toFixed(2), what: `${A.k} overlaps ${B.k}`, a: [A.x0, A.y0, A.x1, A.y1].map(Math.round), b: [B.x0, B.y0, B.x1, B.y1].map(Math.round) }); }
      }
    }
    const buf = await pg.screenshot({ type: 'jpeg', quality: 92 });
    if (prev && Buffer.compare(prev, buf) === 0) { run++; part.maxRun = Math.max(part.maxRun, run); } else run = 0; prev = buf;
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  const endT = i1 / fps;
  for (const key of Object.keys(open)) { const d = +(endT - open[key].t0).toFixed(2); if (d > 0.3) part.overlaps.push({ pair: key, scene: open[key].scene, t0: open[key].t0, dur: d }); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  return part;
}

(async () => {
  const [, , planF, outF, audio, a0, a1] = process.argv;
  const tl = JSON.parse(fs.readFileSync(planF)); const fps = tl.fps || 30;
  tl.words = tl.words || []; const chunks = chunkWords(tl.words);
  const preview = a0 != null;                                   // ad-hoc range preview: single pass, never cached
  const total = Math.round(tl.duration * fps);
  const segs = preview
    ? [{ i: -1, i0: Math.round(+a0 * fps), i1: Math.round(+(a1 || tl.duration) * fps) }]
    : tl.scenes.map((sc, i) => ({ i, i0: Math.round(sc.start * fps), i1: i === tl.scenes.length - 1 ? total : Math.round(tl.scenes[i + 1].start * fps) }));
  const cacheDir = path.join(path.dirname(path.resolve(outF)), '.scene_cache');
  if (!preview) fs.mkdirSync(cacheDir, { recursive: true });
  const useCache = !preview && process.env.CYTO_NOCACHE !== '1';

  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: W, height: H } });
  await pg.setContent('<body style="margin:0;background:#0a1330"></body>');
  const parts = [], files = []; let hits = 0;
  for (const sg of segs) {
    const key = preview ? null : segKey(tl, sg.i, sg.i0, sg.i1);
    const mp4 = preview ? outF + '.seg.mp4' : path.join(cacheDir, key + '.mp4'), meta = preview ? null : path.join(cacheDir, key + '.json');
    if (useCache && fs.existsSync(mp4) && fs.existsSync(meta)) {
      parts.push(JSON.parse(fs.readFileSync(meta))); files.push(mp4); hits++;
      console.log(`scene ${tl.scenes[sg.i].id}: cached (${key.slice(0, 8)})`);
    } else {
      console.log(`scene ${preview ? 'preview' : tl.scenes[sg.i].id}: rendering ${sg.i1 - sg.i0} frames`);
      const part = await renderSegment(pg, tl, chunks, sg.i0, sg.i1, mp4);
      if (!preview) fs.writeFileSync(meta, JSON.stringify(part));
      parts.push(part); files.push(mp4);
    }
  }
  await br.close();

  const list = (preview ? outF : path.join(cacheDir, 'list')) + '.txt';
  fs.writeFileSync(list, files.map(f => `file '${f.replace(/'/g, "'\\''")}'`).join('\n') + '\n');
  await new Promise((res, rej) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list,
    ...(audio && audio !== '-' ? ['-i', audio, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '160k', '-shortest'] : []),
    '-c:v', 'copy', '-movflags', '+faststart', outF], { stdio: 'inherit' }).on('close', c => c ? rej(new Error('concat failed')) : res()));
  fs.unlinkSync(list); if (preview) fs.existsSync(outF + '.seg.mp4') && fs.unlinkSync(outF + '.seg.mp4');

  // merge the per-segment layout data
  const layout = { fails: [], overlaps: [], census: [], samples: 0 };
  const seen = {}, concurrent = {}, poseCut = {}; let jerks = [], poseSpeed = 0, maxRun = 0, frames = 0;
  for (const p of parts) {
    layout.fails.push(...p.fails); layout.overlaps.push(...p.overlaps); layout.census.push(...p.census);
    for (const [k, v] of Object.entries(p.seen)) { seen[k] = seen[k] || new Set(); v.forEach(x => seen[k].add(x)); }
    for (const [k, v] of Object.entries(p.concurrent)) concurrent[k] = Math.min(concurrent[k] ?? 99, v);
    for (const [k, v] of Object.entries(p.poseCut)) poseCut[k] = Math.max(poseCut[k] ?? 0, v);
    jerks = jerks.concat(p.poseJerks || []); poseSpeed = Math.max(poseSpeed, p.poseSpeed || 0);
    maxRun = Math.max(maxRun, p.maxRun || 0); frames += p.frames || 0;
  }
  const gaps = {};
  for (const sc of tl.scenes) {
    const P_ = sc.props || []; if (!P_.length) { gaps[sc.id] = 0; continue; }   // rule 21: clean scenes carry no props
    const dur = Math.min(sc.end - sc.start, Math.max(...P_.map(p => (p && p.out != null) ? p.out : 1e9))), ev = [0];
    (sc.props || []).forEach((p, i) => { const q = normalize(p, i, (sc.props || []).length); const r = PROPS[q.t]; if (r) r(q, 0).events.forEach(e => ev.push(e)); });
    if (sc.card) ev.push(0.45);
    const u = [...new Set(ev.filter(e => e >= 0 && e <= dur).map(e => +e.toFixed(2)))].sort((a, b) => a - b);
    gaps[sc.id] = +Math.max(...u.map((e, i) => (i ? e - u[i - 1] : e)), dur - (u[u.length - 1] ?? 0)).toFixed(2);
  }
  const med = jerks.slice().sort((a, b) => a - b)[Math.floor(jerks.length / 2)] || 0;
  layout.samples = layout.census.length;
  layout.longest_static_run_frames = maxRun; layout.frames = frames;
  layout.pose_speed_max = +poseSpeed.toFixed(3); layout.pose_jerk_median = +med.toFixed(3);
  layout.pose_jerk_in_cut = Object.fromEntries(Object.entries(poseCut).map(([k, v]) => [k, +v.toFixed(3)]));
  layout.props_by_scene = Object.fromEntries(Object.entries(seen).map(([k, v]) => [k, v.size]));
  layout.props_concurrent_min = concurrent;
  layout.props_rendered = Object.values(layout.props_by_scene).reduce((a, b) => a + b, 0);
  layout.new_element_gap_s = gaps;
  layout.cache = { dir: cacheDir, segments: segs.length, reused: hits, rendered: segs.length - hits, engine: ENGINE };
  fs.writeFileSync(outF.replace(/\.mp4$/, '') + '.layout.json', JSON.stringify(layout, null, 1));
  console.log('done', frames, 'frames;', hits, '/', segs.length, 'scenes from cache; layout fails', layout.fails.length,
    '; overlaps', layout.overlaps.length, '; static run', maxRun, '; props', layout.props_rendered, JSON.stringify(layout.props_concurrent_min));
})();
