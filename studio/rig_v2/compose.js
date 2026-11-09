#!/usr/bin/env node
// CANON v2 COMPOSITOR: plan.json -> 1080x1920 mp4 (all scenes in canon cut-out style, Cyto from cyto_rig.js, word captions, transitions).
// usage: node compose.js plan.json out.mp4 [audio.wav] [startSec endSec]     -> also out.layout.json (layout + static-run report)
// plan: {fps,duration,fit,seed,words:[{w,start,end}],beats:[{t,emotion,gaze?}],keys:{word:color},
//        scenes:[{id,bg,start,end,headline,hot:[..],card,transition,snow}]}   (bg: skyline|streetcar|snow|subway|lake|plain)
process.env.SEED = process.env.SEED || '3';
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { frameSvg } = require('./cyto_rig.js');
const C = require('../branding/rebrand-v2/cyto2d.js');
const { chromium } = require('playwright');
const W = 1080, H = 1920, INK = '#0a1f24', GOLD = '#ffc83a';
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), ease = x => x * x * (3 - 2 * x);
const backOut = x => { x = clamp(x, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

// ---------------------------------------------------------------- backgrounds (flat canon cut-outs)
function rnd(seed) { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
function bgSvg(kind, seed = 5) {
  const base = 1280, r = rnd(seed + 11);
  let inner = '';
  if (kind === 'skyline' || kind === 'streetcar') {
    inner = C.skyline(W, H, base, seed) + C.extras(W, H, base, kind === 'streetcar', seed + 6) + C.tower(820, base, 1000);
  } else if (kind === 'lake') {
    inner = `<rect width="${W}" height="${H}" fill="url(#sky)"/><circle cx="780" cy="520" r="150" fill="#ffe9a8" opacity=".9"/>` + C.extras(W, H, base, false, seed + 3);
  } else if (kind === 'subway') {
    inner = `<rect width="${W}" height="${H}" fill="#143a52"/>` +
      Array.from({ length: 10 }, (_, i) => `<rect x="${i * 120}" y="260" width="116" height="760" fill="${i % 2 ? '#1c5873' : '#18506a'}" stroke="${INK}" stroke-width="5"/>`).join('') +
      `<rect y="1020" width="${W}" height="900" fill="#26323f"/><rect y="1020" width="${W}" height="16" fill="${INK}"/><rect y="1210" width="${W}" height="34" fill="${GOLD}" stroke="${INK}" stroke-width="5"/>` +
      `<g><rect x="90" y="880" width="520" height="110" rx="14" fill="#fff" stroke="${INK}" stroke-width="7"/><rect x="110" y="900" width="480" height="70" rx="8" fill="#c62828"/></g>`;
  } else if (kind === 'plain') {
    inner = `<rect width="${W}" height="${H}" fill="url(#sky)"/><circle cx="540" cy="720" r="620" fill="url(#glow)"/>`;
  } else { // snow
    inner = `<rect width="${W}" height="${H}" fill="url(#sky)"/>` + C.extras(W, H, 1500, false, seed + 9).replace(/<rect y="[^"]*" width="[^"]*" height="[^"]*" fill="#0d1a40"\/>/, '');
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${C.defs}${inner}</svg>`;
}
function snowDots(t, n = 46, seed = 4) {
  const r = rnd(seed); let o = '';
  for (let i = 0; i < n; i++) { const x = r() * W, y0 = r() * H, v = 70 + r() * 130, rad = 2 + r() * 4.5; const y = (y0 + t * v) % H; o += `<circle cx="${(x + Math.sin(t + i) * 14).toFixed(0)}" cy="${y.toFixed(0)}" r="${rad.toFixed(1)}" fill="#fff" opacity="${(.4 + r() * .45).toFixed(2)}"/>`; }
  return `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0">${o}</svg>`;
}
const BG = {}; const getBg = (k, s) => BG[k + s] || (BG[k + s] = bgSvg(k, s));

// ---------------------------------------------------------------- text blocks
function headlineHtml(sc, lt, dur) {
  if (!sc.headline) return '';
  const lines = sc.headline.split('\n'), mx = Math.max(...lines.map(l => l.length));
  const fs_ = Math.round(clamp(820 / (mx * 0.76), 56, 150)), hot = (sc.hot || []).map(s => s.toUpperCase());
  const inst = !!sc.instant; // hook-first: scene 0 headline is fully on screen at frame 0 (no pop, no fade-in)
  const p = inst ? 1 : backOut((lt - 0.12) / 0.38), fade = clamp((dur - lt) / 0.25, 0, 1) * (inst ? 1 : clamp((lt - 0.1) / 0.1, 0, 1));
  const body = lines.map(l => `<div>${l.split(' ').map(w => `<span style="color:${hot.includes(w.toUpperCase().replace(/[^A-Z0-9%']/g, '')) || hot.includes(w.toUpperCase()) ? GOLD : '#fff'}">${w}</span>`).join(' ')}</div>`).join('');
  return `<div data-chk="headline" data-s="${p >= 0.98 ? 1 : 0}" style="font:900 ${fs_}px/1.02 'Arial Black','Inter',Impact,sans-serif;text-align:center;letter-spacing:1px;-webkit-text-stroke:${Math.round(fs_ / 9)}px ${INK};paint-order:stroke fill;text-shadow:7px 10px 0 rgba(10,31,36,.55);transform:scale(${Math.max(.01, p).toFixed(3)});opacity:${fade.toFixed(2)}">${body}</div>`;
}
function cardHtml(sc, lt, dur) {
  if (!sc.card) return '';
  const p = backOut((lt - 0.5) / 0.35), fade = clamp((dur - lt) / 0.25, 0, 1) * (lt > 0.5 ? 1 : 0);
  return `<div data-chk="card" data-s="${p >= 0.98 ? 1 : 0}" style="max-width:820px;background:#fff;color:${INK};border:7px solid ${INK};border-radius:30px;padding:16px 30px;font:800 ${sc.cardSize || 46}px/1.15 'Arial','Inter',sans-serif;text-align:center;box-shadow:8px 11px 0 rgba(10,31,36,.45);transform:scale(${Math.max(.01, p).toFixed(3)});opacity:${fade.toFixed(2)}">${String(sc.card).replace(/\n/g, '<br>')}</div>`;
}
function chunkWords(words) { // caption chunks: <=4 words, break after sentence punctuation or long gaps
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
  return `<div data-chk="caption" style="position:absolute;left:60px;top:900px;width:880px;text-align:center;font:900 ${size}px/1.05 'Arial Black','Inter',Impact,sans-serif;-webkit-text-stroke:9px ${INK};paint-order:stroke fill;text-shadow:5px 7px 0 rgba(10,31,36,.6)">${spans}</div>`;
}

// ---------------------------------------------------------------- frame
function sceneLayer(sc, t, tl) {
  const lt = t - sc.start, dur = sc.end - sc.start, k = clamp(lt / dur, 0, 1);
  const push = 1 + 0.07 * k, dx = -22 * k;
  const snow = (sc.snow !== false && ['snow', 'skyline', 'streetcar', 'lake', 'plain'].includes(sc.bg)) ? snowDots(t) : '';
  return `<div style="position:absolute;inset:0;transform:translateX(${dx.toFixed(1)}px) scale(${push.toFixed(4)});transform-origin:50% 55%">${getBg(sc.bg, sc.seed || 5)}${snow}</div>`;
}
function transitionHtml(t, tl, i) {
  const S = tl.scenes, sc = S[i], lt = t - sc.start, TD = sc.transitionDur || 0.35;
  if (i === 0 || lt >= TD) return null;
  const p = ease(lt / TD), prev = S[i - 1], kind = sc.transition || 'whip';
  const a = sceneLayer({ ...prev }, Math.min(t, prev.end - 0.001), tl), b = sceneLayer(sc, t, tl);
  if (kind === 'zoom') return `<div style="position:absolute;inset:0;transform:scale(${(1 + p * 1.6).toFixed(3)});opacity:${(1 - p).toFixed(2)};z-index:2">${a}</div>${b}`;
  if (kind === 'membrane') return `${a}<div style="position:absolute;inset:0;clip-path:circle(${(p * 150).toFixed(1)}% at 50% 62%);z-index:2">${b}</div><div style="position:absolute;inset:0;z-index:3;border-radius:50%;box-shadow:0 0 0 ${(14 * (1 - p)).toFixed(1)}px ${INK};clip-path:circle(${(p * 150).toFixed(1)}% at 50% 62%);pointer-events:none"></div>`;
  if (kind === 'doors') {
    const open = p < .5 ? 1 - p * 2 : (p - .5) * 2, shown = p < .5 ? a : b, w = (W / 2) * (p < .5 ? p * 2 : 1 - (p - .5) * 2);
    return `${shown}<div style="position:absolute;left:0;top:0;width:${w}px;height:${H}px;background:#c7d3de;border-right:8px solid ${INK};z-index:3"></div><div style="position:absolute;right:0;top:0;width:${w}px;height:${H}px;background:#c7d3de;border-left:8px solid ${INK};z-index:3"></div>`;
  }
  // whip (default): outgoing slides left, incoming slides in, blur peaks mid-move
  const bl = (Math.sin(p * Math.PI) * 14).toFixed(1);
  return `<div style="position:absolute;inset:0;transform:translateX(${(-p * W).toFixed(0)}px);filter:blur(${bl}px)">${a}</div><div style="position:absolute;inset:0;transform:translateX(${((1 - p) * W).toFixed(0)}px);filter:blur(${bl}px)">${b}</div>`;
}
function frameHtml(t, tl, chunks, cyto) {
  const S = tl.scenes; let i = S.findIndex(s => t >= s.start && t < s.end); if (i < 0) i = S.length - 1;
  const sc = S[i], lt = t - sc.start, dur = sc.end - sc.start;
  const bg = transitionHtml(t, tl, i) || sceneLayer(sc, t, tl);
  const stack = `<div style="position:absolute;left:60px;top:240px;width:880px;display:flex;flex-direction:column;align-items:center;gap:34px">${headlineHtml(sc, lt, dur)}${cardHtml(sc, lt, dur)}</div>`;
  const cy = `<div data-chk="cyto" style="position:absolute;left:${tl.cytoX ?? -80}px;top:${tl.cytoY ?? 990}px;width:${tl.cytoSize ?? 800}px;height:${tl.cytoSize ?? 800}px">${cyto}</div>`;
  return `<div id="f" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#0a1330">${bg}${stack}${cy}${captionsHtml(tl, t, chunks)}</div>`;
}

// ---------------------------------------------------------------- main
(async () => {
  const [, , planF, outF, audio, a0, a1] = process.argv;
  const tl = JSON.parse(fs.readFileSync(planF)); const fps = tl.fps || 30;
  tl.words = tl.words || []; const chunks = chunkWords(tl.words);
  const t0 = +(a0 || 0), t1 = +(a1 || tl.duration), n = Math.round((t1 - t0) * fps);
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: W, height: H } });
  await pg.setContent('<body style="margin:0;background:#0a1330"></body>');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    ...(audio && audio !== '-' ? ['-i', audio, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '160k', '-shortest'] : []),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', '-movflags', '+faststart', outF], { stdio: ['pipe', 'inherit', 'inherit'] });
  const layout = { fails: [], samples: 0 }; let prev = null, run = 0, maxRun = 0;
  for (let i = 0; i < n; i++) {
    const t = t0 + i / fps;
    const html = frameHtml(t, tl, chunks, frameSvg(t, tl, tl.cytoSize ?? 800));
    await pg.evaluate(([h, t]) => { document.body.innerHTML = h; document.querySelectorAll('svg').forEach(e => { try { e.pauseAnimations(); e.setCurrentTime(t); } catch (_) { } }); }, [html, t]);
    if (i % Math.max(1, Math.round(fps / 4)) === 0) { // layout check every 0.25 s
      const rs = await pg.evaluate(() => [...document.querySelectorAll('[data-chk]')].map(e => { const r = e.getBoundingClientRect(); return { k: e.dataset.chk, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom, vis: +(getComputedStyle(e).opacity) > 0.3 && r.width > 4 && e.dataset.s !== '0' }; }));
      layout.samples++;
      const txt = rs.filter(r => r.vis && r.k !== 'cyto');
      for (const r of txt) { if (r.x0 < 59 || r.x1 > 941 || r.y0 < 199 || r.y1 > 1481) layout.fails.push({ t: +t.toFixed(2), what: `${r.k} outside safe zone`, box: [r.x0, r.y0, r.x1, r.y1].map(Math.round) }); }
      for (let a = 0; a < txt.length; a++) for (let b = a + 1; b < txt.length; b++) { const A = txt[a], B = txt[b]; if (A.x0 < B.x1 && B.x0 < A.x1 && A.y0 < B.y1 && B.y0 < A.y1) layout.fails.push({ t: +t.toFixed(2), what: `${A.k} overlaps ${B.k}` }); }
    }
    const buf = await pg.screenshot({ type: 'jpeg', quality: 92 });
    if (prev && Buffer.compare(prev, buf) === 0) { run++; maxRun = Math.max(maxRun, run); } else run = 0; prev = buf;
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 90 === 0) console.log('frame', i, '/', n);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close();
  layout.longest_static_run_frames = maxRun; layout.frames = n;
  fs.writeFileSync(outF.replace(/\.mp4$/, '') + '.layout.json', JSON.stringify(layout, null, 1));
  console.log('done', n, 'frames; layout fails', layout.fails.length, '; longest static run', maxRun);
})();
