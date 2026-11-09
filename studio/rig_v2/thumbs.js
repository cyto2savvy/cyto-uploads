#!/usr/bin/env node
// CANON v2 thumbnails: node thumbs.js thumbs.json outDir   -> thumb-<id>-1280x720.jpg + thumb-<id>-1080x1920.jpg (+ feed_check.jpg made by make_episode.py)
// spec: {fit, thumbs:[{id, headline:["YOUR HEART","SLOWS DOWN"], hot:["SLOWS"], hero:"heart|clock|snow|brain|phone|sugar" or hero_svg:"<g>..</g>", emotion:"shock|think|happy|solemn|chill", gaze:[x,y], glow:"#ff5a4d", photo:"/abs/path.jpg" (optional background), series:"6IXTY SECONDS OF SCIENCE"}]}
process.env.SEED = process.env.SEED || '3';
const fs = require('fs'), path = require('path');
const { frameSvg } = require('./cyto_rig.js'); const { chromium } = require('playwright');
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
function photoHtml(sp) { // optional free-photo background (Unsplash): sp.photo = path to a jpg; navy wash keeps the headline readable
  if (!sp.photo) return '';
  const b64 = fs.readFileSync(path.resolve(__dirname, '..', '..', sp.photo)).toString('base64');
  return `<div style="position:absolute;inset:0;background:url(data:image/jpeg;base64,${b64}) center/cover"></div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,19,48,.78) 0%,rgba(10,19,48,.35) 45%,rgba(10,19,48,.7) 100%)"></div>`;
}
function html(sp, fit, W, H) {
  const portrait = H > W, pad = portrait ? 1 : 0.62;
  const hero = sp.hero_svg || HERO[sp.hero] || HERO.heart, glow = sp.glow || '#ff5a4d';
  const tl = { fps: 30, duration: 1, fit, seed: 7, words: [], beats: [{ t: 0, emotion: sp.emotion || 'shock', gaze: sp.gaze || [-.7, -.4] }] };
  const csz = portrait ? 980 : 700, cyto = frameSvg(0.1, tl, csz);
  const hot = (sp.hot || []).map(s => s.toUpperCase());
  const hl = sp.headline.map(l => `<div>${l.split(' ').map(w => `<span style="color:${hot.includes(w.toUpperCase()) ? GOLD : '#fff'}">${w}</span>`).join(' ')}</div>`).join('');
  const mx = Math.max(...sp.headline.map(l => l.length)), avail = portrait ? 940 : 560, hs = Math.round(Math.min(portrait ? 170 : 108, Math.max(60, avail / (mx * 0.7))));
  const L = portrait
    ? { pill: 'left:60px;top:225px', hl: 'left:70px;top:300px;width:940px;text-align:center;white-space:nowrap', hero: 'left:640px;top:900px', cy: 'left:-40px;top:940px' }
    : { pill: 'left:50px;top:34px', hl: 'left:44px;top:96px;width:560px;text-align:left;white-space:nowrap', hero: 'left:210px;top:410px', cy: 'left:600px;top:-10px' };
  const hsz = portrait ? 460 : 300;
  return `<body style="margin:0"><div style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:radial-gradient(circle at ${portrait ? '60% 45%' : '30% 70%'},${sp.bg2 || '#15284a'},${sp.bg1 || '#0a1330'} 75%)">
${photoHtml(sp)}<div style="position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at ${portrait ? '60% 45%' : '30% 70%'},rgba(255,255,255,.06) 0 6deg,transparent 6deg 18deg)"></div>
<div style="position:absolute;${L.pill};background:${GOLD};color:${INK};border:6px solid ${INK};border-radius:40px;padding:6px 26px;font:900 ${portrait ? 34 : 24}px 'Arial Black',sans-serif">${sp.series || '6IXTY SECONDS OF SCIENCE'}</div>
<div style="position:absolute;${L.hl};font:900 ${hs}px/1.0 'Arial Black','Inter',Impact,sans-serif;-webkit-text-stroke:${Math.round(hs / 8)}px ${INK};paint-order:stroke fill;text-shadow:8px 11px 0 rgba(10,31,36,.6)">${hl}</div>
<div style="position:absolute;${L.hero}"><svg viewBox="-220 -220 440 440" width="${hsz}" height="${hsz}" style="overflow:visible;filter:drop-shadow(0 0 40px ${glow})"><defs></defs><g>${hero}</g></svg></div>
<div style="position:absolute;${L.cy};width:${csz}px;height:${csz}px;filter:drop-shadow(0 0 18px rgba(255,255,255,.55))">${cyto}</div></div></body>`;
}
(async () => {
  const spec = JSON.parse(fs.readFileSync(process.argv[2])), out = path.resolve(process.argv[3]); fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch();
  for (const sp of spec.thumbs) for (const [W, H] of [[1280, 720], [1080, 1920]]) {
    const pg = await br.newPage({ viewport: { width: W, height: H } });
    await pg.setContent(html(sp, spec.fit || 'none', W, H)); await pg.evaluate(() => document.querySelectorAll('svg').forEach(e => { try { e.pauseAnimations(); e.setCurrentTime(0.1); } catch (_) { } }));
    await pg.screenshot({ path: path.join(out, `thumb-${sp.id}-${W}x${H}.jpg`), type: 'jpeg', quality: 90 }); await pg.close();
  }
  await br.close(); console.log('thumbs ok');
})();
