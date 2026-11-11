#!/usr/bin/env node
// CANON v2 thumbnails (VERTICAL FIRST — Shorts use 1080x1920; 1280x720 is the long-form/YouTube-API copy).
//   node thumbs.js thumbs.json outDir   -> thumb-<id>-1080x1920.jpg + thumb-<id>-1280x720.jpg
// spec: {fit, thumbs:[{id, headline:["CANCER'S","COMEBACK"], hot:["COMEBACK"], hero:"heart|clock|snow|brain|phone|sugar" or hero_svg:"<g>..</g>",
//        emotion, gaze:[x,y], glow:"#ff5a4d", photo:"photos/x.jpg" OR scene:"hospital|trail|lab|..." (drawn canon backdrop, backdrops.js),
//        bg_subject:"cancer + Sunnybrook Odette Cancer Centre", cscale, cx, cy, series}]}
// HARD_RULES 3b: the WHOLE Cyto and the WHOLE cup sit inside the frame with >= 40 px margin and the headline never crosses his face.
process.env.SEED = process.env.SEED || '3';
const fs = require('fs'), path = require('path');
const { frameSvg } = require('./cyto_rig.js'); const { layers } = require('./backdrops.js'); const { chromium } = require('playwright');
const INK = '#0a1f24', GOLD = '#ffc83a';
const O = (d, f, extra = '') => `<path d="${d}" fill="${f}" stroke="${INK}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" ${extra}/>`;
const HERO = { // ~400x400 canon cut-outs centred on 0,0
  heart: O('M0 150 C-190 20 -150 -170 -45 -165 C-15 -160 0 -130 0 -110 C0 -130 15 -160 45 -165 C150 -170 190 20 0 150Z', '#ff5a4d') + `<path d="M-95 -105 Q-120 -50 -85 -10" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".7"/>`,
  clock: `<circle r="170" fill="#fff" stroke="${INK}" stroke-width="12"/><circle r="140" fill="#eaf6ff" stroke="${INK}" stroke-width="6"/>` + [0, 90, 180, 270].map(a => `<rect x="-6" y="-132" width="12" height="30" fill="${INK}" transform="rotate(${a})"/>`).join('') + `<path d="M0 0 L0 -105" stroke="${INK}" stroke-width="14" stroke-linecap="round"/><path d="M0 0 L78 40" stroke="#c62828" stroke-width="14" stroke-linecap="round"/><circle r="14" fill="${INK}"/>`,
  snow: [0, 60, 120].map(a => `<path d="M0 -165 V165" stroke="#fff" stroke-width="20" stroke-linecap="round" transform="rotate(${a})"/><path d="M0 -165 V165" stroke="${INK}" stroke-width="34" stroke-linecap="round" opacity=".35" transform="rotate(${a})"/>`).join('') + [0, 60, 120].map(a => `<path d="M0 -165 V165" stroke="#dff3ff" stroke-width="20" stroke-linecap="round" transform="rotate(${a})"/>`).join(''),
  brain: O('M-20 -140 C-140 -160 -190 -40 -140 20 C-190 80 -130 160 -40 130 C0 170 70 160 90 120 C170 130 200 40 150 -10 C190 -70 130 -150 40 -120 C20 -150 0 -145 -20 -140Z', '#ff9db8') + `<path d="M0 -130 V120 M-80 -60 Q-40 -30 0 -50 M80 -40 Q40 0 0 20 M-90 50 Q-40 70 0 40" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round"/>`,
  phone: `<rect x="-100" y="-175" width="200" height="350" rx="34" fill="#16254f" stroke="${INK}" stroke-width="10"/><rect x="-80" y="-145" width="160" height="270" rx="12" fill="#7fe3d3"/><text x="0" y="-5" text-anchor="middle" font-family="Arial Black" font-size="64" fill="${INK}">3:00</text>`,
  sugar: O('M-120 -40 L0 -110 L120 -40 L120 80 L0 150 L-120 80Z', '#fff') + `<path d="M-120 -40 L0 30 L120 -40 M0 30 V150" stroke="${INK}" stroke-width="9" fill="none"/>`,
};
function bgHtml(sp) {
  if (sp.photo) {   // free photo (Unsplash) + navy wash so the headline stays readable
    const b64 = fs.readFileSync(path.resolve(__dirname, '..', '..', sp.photo)).toString('base64');
    return `<div style="position:absolute;inset:0;background:url(data:image/jpeg;base64,${b64}) center/cover"></div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,19,48,.78) 0%,rgba(10,19,48,.35) 45%,rgba(10,19,48,.7) 100%)"></div>`;
  }
  if (sp.scene) {   // drawn canon scene of the topic (HARD_RULES 1 fallback when no honest photo of the place exists)
    return layers(sp.scene, sp.sceneSeed || 5).map(l => `<div style="position:absolute;inset:0;transform:scale(1.02)">${l.s}</div>`).join('') +
      `<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,19,48,.55) 0%,rgba(10,19,48,.12) 40%,rgba(10,19,48,.6) 100%)"></div>`;
  }
  return '';
}
function html(sp, fit, W, H) {
  const portrait = H > W;
  const hero = sp.hero_svg || HERO[sp.hero] || HERO.heart, glow = sp.glow || '#ff5a4d';
  const tl = { fps: 30, duration: 1, fit, seed: 7, words: [], beats: [{ t: 0, emotion: sp.emotion || 'shock', gaze: sp.gaze || [-.7, -.4] }] };
  const csz = Math.round((portrait ? 820 : 620) * (sp.cscale || 1)), cyto = frameSvg(0.1, tl, csz);
  const hot = (sp.hot || []).map(s => s.toUpperCase());
  const hl = sp.headline.map(l => `<div>${l.split(' ').map(w => `<span style="color:${hot.includes(w.toUpperCase()) ? GOLD : '#fff'}">${w}</span>`).join(' ')}</div>`).join('');
  const mx = Math.max(...sp.headline.map(l => l.length)), avail = portrait ? 940 : 560, hs = Math.round(Math.min(portrait ? 150 : 104, Math.max(60, avail / (mx * 0.72))));
  // Cyto's drawn content runs x -29..1032 and y -20..960 of a 1100 box (cup + steam + raised arm) -> keep that inside with >= 40 px.
  const L = portrait
    ? { pill: 'left:60px;top:150px', hl: 'left:70px;top:236px;width:940px;text-align:center', hero: 'left:84px;top:548px', heroSz: 440, cx: 270, cy: 1030 }
    : { pill: 'left:50px;top:34px', hl: 'left:44px;top:104px;width:560px;text-align:left', hero: 'left:170px;top:400px', heroSz: 270, cx: 566, cy: 58 };
  const cx = sp.cx != null ? sp.cx : L.cx, cy = sp.cy != null ? sp.cy : L.cy;
  return `<body style="margin:0"><div style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:radial-gradient(circle at ${portrait ? '60% 40%' : '30% 70%'},${sp.bg2 || '#15284a'},${sp.bg1 || '#0a1330'} 75%)">
${bgHtml(sp)}<div style="position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at ${portrait ? '60% 40%' : '30% 70%'},rgba(255,255,255,.06) 0 6deg,transparent 6deg 18deg)"></div>
<div style="position:absolute;${L.pill};background:${GOLD};color:${INK};border:6px solid ${INK};border-radius:40px;padding:6px 26px;font:900 ${portrait ? 34 : 24}px 'Arial Black',sans-serif">${sp.series || '6IXTY SECONDS OF SCIENCE'}</div>
<div data-chk="hl" style="position:absolute;${L.hl};font:900 ${hs}px/1.02 'Arial Black','Inter',Impact,sans-serif;-webkit-text-stroke:${Math.round(hs / 8)}px ${INK};paint-order:stroke fill;text-shadow:8px 11px 0 rgba(10,31,36,.6)">${hl}</div>
<div data-chk="hero" style="position:absolute;${L.hero}"><svg viewBox="-220 -220 440 440" width="${L.heroSz}" height="${L.heroSz}" style="overflow:visible;filter:drop-shadow(0 0 40px ${glow})"><g>${hero}</g></svg></div>
<div data-chk="cyto" style="position:absolute;left:${cx}px;top:${cy}px;width:${csz}px;height:${csz}px;filter:drop-shadow(0 0 18px rgba(255,255,255,.55))">${cyto}</div></div></body>`;
}
(async () => {
  const spec = JSON.parse(fs.readFileSync(process.argv[2])), out = path.resolve(process.argv[3]); fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch(); const report = [];
  for (const sp of spec.thumbs) for (const [W, H] of [[1080, 1920], [1280, 720]]) {   // vertical first
    const pg = await br.newPage({ viewport: { width: W, height: H } });
    await pg.setContent(html(sp, spec.fit || 'none', W, H)); await pg.evaluate(() => document.querySelectorAll('svg').forEach(e => { try { e.pauseAnimations(); e.setCurrentTime(0.1); } catch (_) { } }));
    const boxes = await pg.evaluate(() => Object.fromEntries([...document.querySelectorAll('[data-chk]')].map(e => {
      const r = e.getBoundingClientRect(); let b = r;
      if (e.dataset.chk === 'cyto') { const s = e.querySelector('svg'), g = s.getBBox(), k = r.width / 1100; b = { left: r.left + (g.x + 550) * k, top: r.top + (g.y + 550) * k, right: r.left + (g.x + g.width + 550) * k, bottom: r.top + (g.y + g.height + 550) * k }; }
      return [e.dataset.chk, { x0: Math.round(b.left), y0: Math.round(b.top), x1: Math.round(b.right), y1: Math.round(b.bottom) }];
    })));
    await pg.screenshot({ path: path.join(out, `thumb-${sp.id}-${W}x${H}.jpg`), type: 'jpeg', quality: 90 }); await pg.close();
    const c = boxes.cyto, h = boxes.hl, margin = Math.min(c.x0, c.y0, W - c.x1, H - c.y1);
    report.push({ id: sp.id, size: `${W}x${H}`, cyto: c, cyto_margin_px: margin, cyto_frac_width: +((c.x1 - c.x0) / W).toFixed(3), headline: h,
      headline_over_face: !(h.y1 < c.y0 || h.y0 > c.y1 || h.x1 < c.x0 || h.x0 > c.x1) });
  }
  fs.writeFileSync(path.join(out, 'thumb_report.json'), JSON.stringify(report, null, 1));
  await br.close(); console.log('thumbs ok', JSON.stringify(report.filter(r => r.size === '1080x1920').map(r => [r.id, r.cyto_margin_px, r.cyto_frac_width, r.headline_over_face])));
})();
