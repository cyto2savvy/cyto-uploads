#!/usr/bin/env node
// CANON v2 BACKDROPS: topic cut-out sets as parallax layers (far .15 -> near 1), shared by compose.js (video) and thumbs.js (drawn
// thumbnail scenes). HARD_RULES 6: backdrops come from the topic (trail, hospital row, lab bench, TTC), not always the skyline.
const C = require('../branding/rebrand-v2/cyto2d.js');
const W = 1080, H = 1920, INK = '#0a1f24', GOLD = '#ffc83a', C_RED = '#c62828';
const KINDS = ['skyline', 'streetcar', 'snow', 'subway', 'lake', 'plain', 'trail', 'hospital', 'lab', 'gym', 'chestcavity'];
// ---------------------------------------------------------------- backdrops: parallax layers (far .25 -> near 1)
function rnd(seed) { let s = seed % 2147483647 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
const svg = (inner, defs = '') => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${defs}${inner}</svg>`;
const GR = `<defs><linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#15224d"/><stop offset=".55" stop-color="#3a3f7a"/><stop offset="1" stop-color="#c9707a"/></linearGradient>
<linearGradient id="dayb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1a40"/><stop offset="1" stop-color="#2b4180"/></linearGradient>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b3358"/><stop offset="1" stop-color="#132444"/></linearGradient></defs>`;
function stars(seed, n = 90) { const r = rnd(seed); let o = ''; for (let i = 0; i < n; i++) o += `<circle cx="${(r() * W).toFixed(0)}" cy="${(r() * H * .62).toFixed(0)}" r="${(1 + r() * 2.6).toFixed(1)}" fill="#fff" opacity="${(.3 + r() * .6).toFixed(2)}"/>`; return o; }
function trees(seed, y, h, fill, n) { const r = rnd(seed); let o = ''; for (let i = 0; i < n; i++) { const x = (i + r() * .6) * (W / n), s = .7 + r() * .6; o += `<g transform="translate(${x.toFixed(0)},${y}) scale(${s.toFixed(2)})"><rect x="-13" y="-${h * .3}" width="26" height="${h * .3}" fill="#3c2b22" stroke="${INK}" stroke-width="7"/><path d="M0 -${h} L${h * .42} -${h * .25} L-${h * .42} -${h * .25}Z" fill="${fill}" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/><path d="M0 -${h * .78} L${h * .34} -${h * .1} L-${h * .34} -${h * .1}Z" fill="${fill}" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/></g>`; } return o; }
function bgLayers(kind, seed = 5) {
  const base = 1280;
  if (kind === 'skyline' || kind === 'streetcar') return [
    { d: .2, s: svg(`<rect width="${W}" height="${H}" fill="url(#dayb)"/>${stars(seed)}`, GR) },
    { d: .55, s: svg(`<g transform="translate(0,-250)">${C.skyline(W, H, base, seed) + C.tower(820, base, 1000)}</g>`, C.defs) },
    { d: 1, s: svg(C.extras(W, H, base, kind === 'streetcar', seed + 6), C.defs) }];
  if (kind === 'lake') return [
    { d: .2, s: svg(`<rect width="${W}" height="${H}" fill="url(#sky)"/><circle cx="780" cy="520" r="150" fill="#ffe9a8" opacity=".9"/>${stars(seed, 50)}`, C.defs) },
    { d: .8, s: svg(C.extras(W, H, base, false, seed + 3), C.defs) }];
  if (kind === 'subway') return [
    { d: .25, s: svg(`<rect width="${W}" height="${H}" fill="#143a52"/>` + Array.from({ length: 10 }, (_, i) => `<rect x="${i * 120}" y="260" width="116" height="760" fill="${i % 2 ? '#1c5873' : '#18506a'}" stroke="${INK}" stroke-width="5"/>`).join('')) },
    {
      d: .7, s: svg([[96, '#f2f5f8', '#2c63d6'], [628, '#fff3d6', C_RED]].map(([x, bg, bar], i) =>
        `<g transform="translate(${x},430)"><rect width="356" height="470" rx="18" fill="${bg}" stroke="${INK}" stroke-width="9"/><rect y="0" width="356" height="92" fill="${bar}" stroke="${INK}" stroke-width="9"/>` +
        [0, 1, 2].map(j => `<rect x="34" y="${150 + j * 86}" width="${288 - j * 64}" height="40" rx="12" fill="#c3cedb" stroke="${INK}" stroke-width="6"/>`).join('') + `</g>`).join(''))
    },
    { d: 1, s: svg(`<rect y="1020" width="${W}" height="900" fill="#26323f"/><rect y="1020" width="${W}" height="16" fill="${INK}"/><rect y="1210" width="${W}" height="34" fill="${GOLD}" stroke="${INK}" stroke-width="5"/>`) }];
  if (kind === 'trail') return [   // waterfront trail at dawn: sky, lake + far shore, treeline, path
    { d: .15, s: svg(`<rect width="${W}" height="${H}" fill="url(#dawn)"/><circle cx="300" cy="640" r="96" fill="#ffd9a0" opacity=".95"/>${stars(seed, 40)}`, GR) },
    { d: .45, s: svg(`<rect y="760" width="${W}" height="180" fill="#2a4a86"/>` + Array.from({ length: 7 }, (_, i) => `<rect x="${i * 170 - 40}" y="${680 - (i % 3) * 70}" width="110" height="${100 + (i % 3) * 70}" fill="#1b2d55" stroke="${INK}" stroke-width="6"/>`).join('') +
      [[180, 560], [300, 505], [430, 575]].map(([x, y]) => `<path d="M${x} ${y} q18 -16 34 0 q16 -16 34 0" stroke="${INK}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join('')) },
    { d: .75, s: svg(trees(seed + 2, 1010, 300, '#1f6f5c', 6)) },
    { d: 1, s: svg(`<path d="M0 1320 Q540 1250 ${W} 1330 L${W} ${H} L0 ${H}Z" fill="#6a5b4a" stroke="${INK}" stroke-width="9"/><path d="M0 1420 Q540 1352 ${W} 1430" stroke="#f2e4c9" stroke-width="12" fill="none" stroke-dasharray="70 56"/>`) }];
  if (kind === 'hospital') return [  // hospital row on University Ave
    { d: .2, s: svg(`<rect width="${W}" height="${H}" fill="url(#dayb)"/>${stars(seed, 60)}`, GR) },
    {
      d: .6, s: svg(Array.from({ length: 4 }, (_, i) => { const x = i * 300 - 120, h = 760 + (i % 2) * 140;
        return `<rect x="${x}" y="${1180 - h}" width="268" height="${h}" fill="url(#wall)" stroke="${INK}" stroke-width="8"/>` +
          Array.from({ length: 24 }, (_, j) => `<rect x="${x + 22 + (j % 4) * 60}" y="${1210 - h + Math.floor(j / 4) * 96}" width="40" height="52" fill="${(i + j) % 3 ? '#cfe6ff' : GOLD}" opacity=".9"/>`).join('');
      }).join(''), GR)
    },
    {
      d: 1, s: svg(`<rect y="1180" width="${W}" height="${H - 1180}" fill="#2a3242"/><rect y="1180" width="${W}" height="14" fill="${INK}"/>` +
        `<g transform="translate(176,1092)"><rect x="-86" y="-86" width="172" height="172" rx="20" fill="#fff" stroke="${INK}" stroke-width="9"/><rect x="-20" y="-56" width="40" height="112" fill="${C_RED}"/><rect x="-56" y="-20" width="112" height="40" fill="${C_RED}"/></g>` +
        `<g transform="translate(830,1104)"><rect x="-150" y="-92" width="300" height="130" rx="18" fill="#fff" stroke="${INK}" stroke-width="9"/><rect x="-150" y="-30" width="300" height="12" fill="${C_RED}"/><circle cx="-86" cy="52" r="34" fill="#2b3340" stroke="${INK}" stroke-width="9"/><circle cx="86" cy="52" r="34" fill="#2b3340" stroke="${INK}" stroke-width="9"/></g>`)
    }];
  if (kind === 'lab') return [   // clinic / lab bench
    { d: .2, s: svg(`<rect width="${W}" height="${H}" fill="#16304a"/><rect y="0" width="${W}" height="${H}" fill="url(#glow)" opacity=".5"/>`, C.defs) },
    {
      d: .6, s: svg(`<rect x="60" y="560" width="960" height="26" rx="10" fill="#8a9bb0" stroke="${INK}" stroke-width="8"/>` +
        [0, 1, 2, 3].map(i => `<rect x="${140 + i * 210}" y="430" width="92" height="130" rx="12" fill="${i % 2 ? '#7fe3d3' : '#ffd0d8'}" stroke="${INK}" stroke-width="8"/>`).join(''))
    },
    {
      d: 1, s: svg(`<rect y="1240" width="${W}" height="${H - 1240}" fill="#20394f"/><rect y="1240" width="${W}" height="18" fill="${INK}"/>` +
        `<g transform="translate(210,1240)"><path d="M-54 0 L-54 -96 L-74 -150 L74 -150 L54 -96 L54 0Z" fill="#9fe8db" stroke="${INK}" stroke-width="9"/><rect x="-54" y="-70" width="108" height="70" fill="#3fd0bb"/></g>` +
        `<g transform="translate(880,1240)"><rect x="-70" y="-168" width="140" height="168" rx="14" fill="#fff" stroke="${INK}" stroke-width="9"/><path d="M-70 -110 H70" stroke="${INK}" stroke-width="7"/><rect x="-44" y="-86" width="88" height="54" fill="#cfe6ff"/></g>`)
    }];
  if (kind === 'gym') {   // Ep 18: weight room. Mirror wall, dumbbell rack on the far wall, bench silhouette, rubber floor. No brands, no signage text.
    const r = rnd(seed + 11);
    const bell = (x, y, s, col) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-34" y="-9" width="68" height="18" rx="6" fill="#9fb0c0" stroke="${INK}" stroke-width="6"/>` +
      [-1, 1].map(k => `<path d="M${k * 30} -30 L${k * 58} -30 L${k * 66} -15 L${k * 66} 15 L${k * 58} 30 L${k * 30} 30Z" fill="${col}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>`).join('') + `</g>`;
    const cols = ['#2b3340', '#3a4656', '#c62828', '#2c63d6', '#2fae9b'];
    const shelf = (y, n, s) => `<rect x="110" y="${y}" width="860" height="24" rx="8" fill="#8a9bb0" stroke="${INK}" stroke-width="8"/>` +
      Array.from({ length: n }, (_, i) => bell(110 + 860 * (i + .5) / n, y - 30 * s - 4, s, cols[Math.floor(r() * cols.length)])).join('');
    return [
      { d: .15, s: svg(`<rect width="${W}" height="${H}" fill="#18304e"/><rect y="0" width="${W}" height="250" fill="#122640"/>` +
        Array.from({ length: 4 }, (_, i) => `<g transform="translate(${30 + i * 262},270)"><rect width="236" height="690" rx="10" fill="#2a5078" stroke="${INK}" stroke-width="8"/>` +
          `<path d="M${30 + (i % 2) * 40} 690 L${130 + (i % 2) * 40} 0 h46 L${76 + (i % 2) * 40} 690Z" fill="#fff" opacity=".13"/><path d="M${150 - (i % 2) * 60} 690 L${205 - (i % 2) * 60} 300 h18 L${168 - (i % 2) * 60} 690Z" fill="#fff" opacity=".09"/></g>`).join('')) },
      { d: .55, s: svg([[-1, 300], [1, 780]].map(([k, x]) => `<rect x="${x - 14}" y="560" width="28" height="470" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/>`).join('') +
        `<rect x="${140 - 14}" y="560" width="28" height="470" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/><rect x="${940 - 14}" y="560" width="28" height="470" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/>` +
        shelf(650, 6, .92) + shelf(800, 5, 1.12) + shelf(960, 4, 1.34)) },
      { d: 1, s: svg(`<rect y="1030" width="${W}" height="${H - 1030}" fill="#232a33"/><rect y="1030" width="${W}" height="16" fill="${INK}"/>` +
        Array.from({ length: 70 }, () => `<circle cx="${(r() * W).toFixed(0)}" cy="${(1060 + r() * 840).toFixed(0)}" r="${(3 + r() * 4).toFixed(1)}" fill="${r() < .5 ? '#3d4855' : '#56c9b8'}" opacity=".7"/>`).join('') +
        Array.from({ length: 5 }, (_, i) => `<path d="M${i * 270 - 20} 1046 V${H}" stroke="${INK}" stroke-width="5" opacity=".5"/>`).join('') +
        // flat bench silhouette, far right, behind where Cyto stands
        `<g transform="translate(905,1120)"><rect x="-150" y="-34" width="300" height="40" rx="16" fill="#c62828" stroke="${INK}" stroke-width="9"/><rect x="-128" y="6" width="22" height="92" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/><rect x="106" y="6" width="22" height="92" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/><rect x="-150" y="92" width="66" height="18" rx="8" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/><rect x="84" y="92" width="66" height="18" rx="8" fill="#5d6c7c" stroke="${INK}" stroke-width="8"/></g>`) }];
  }
  if (kind === 'chestcavity') {   // Ep 18: inside the chest. Warm interior, heart silhouette beating in the far layer (SMIL, 0.9 s), rib arches in parallax.
    const CG = `<defs><radialGradient id="chest" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="#e2566a"/><stop offset=".55" stop-color="#a52b46"/><stop offset="1" stop-color="#5a1430"/></radialGradient></defs>`;
    const heart = 'M0 150 C-190 20 -150 -170 -45 -165 C-15 -160 0 -130 0 -110 C0 -130 15 -160 45 -165 C150 -170 190 20 0 150Z';
    const rib = (y, sw, col, k, reach) => [-1, 1].map(sd => { const d = `M${540 + sd * 620} ${y - 130 * k} Q${540 + sd * (reach + 90)} ${y - 50 * k} ${540 + sd * reach} ${y + 70 * k}`;
      return `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${sw + 16}" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${col}" stroke-width="${sw}" stroke-linecap="round"/>` +
        `<path d="${d}" fill="none" stroke="#fff" stroke-width="${Math.round(sw * .2)}" stroke-linecap="round" opacity=".4" transform="translate(0,${-Math.round(sw * .22)})"/>`; }).join('');
    return [
      { d: .15, s: svg(`<rect width="${W}" height="${H}" fill="url(#chest)"/>` +
        `<g transform="translate(540,700)"><g><animateTransform attributeName="transform" type="scale" values="1;1.07;1;1.035;1;1" keyTimes="0;.12;.3;.42;.6;1" dur="0.9s" repeatCount="indefinite"/>` +
        `<path d="${heart}" transform="scale(2.5)" fill="#7a1c38" stroke="#4a0f26" stroke-width="5"/><path d="M-95 -105 Q-120 -50 -85 -10" transform="scale(2.5)" stroke="#c2506a" stroke-width="9" fill="none" stroke-linecap="round" opacity=".6"/></g></g>`, CG) },
      { d: .5, s: svg([330, 560, 790, 1020].map(y => rib(y, 30, '#b98f92', .8, 400)).join('')) },
      { d: 1, s: svg([200, 470, 740, 1010, 1280].map(y => rib(y, 54, '#ecdccb', 1.1, 455)).join('') +
        `<path d="M0 1470 Q540 1330 ${W} 1470 L${W} ${H} L0 ${H}Z" fill="#8f2440" stroke="${INK}" stroke-width="9"/><path d="M120 1486 Q540 1380 960 1486" stroke="#c2506a" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/>`) }];
  }
  if (kind === 'plain') return [
    { d: .2, s: svg(`<rect width="${W}" height="${H}" fill="url(#sky)"/><circle cx="540" cy="760" r="640" fill="url(#glow)"/>`, C.defs) } ];   // decorative rings removed (HARD_RULES 21: no ambient floaters)
  return [{ d: .2, s: svg(`<rect width="${W}" height="${H}" fill="url(#sky)"/>`, C.defs) },
  { d: .9, s: svg(C.extras(W, H, 1500, false, seed + 9).replace(/<rect y="[^"]*" width="[^"]*" height="[^"]*" fill="#0d1a40"\/>/, ''), C.defs) }];
}
function snowDots(t, n = 46, seed = 4) {
  const r = rnd(seed); let o = '';
  for (let i = 0; i < n; i++) { const x = r() * W, y0 = r() * H, v = 70 + r() * 130, rad = 2 + r() * 4.5; const y = (y0 + t * v) % H; o += `<circle cx="${(x + Math.sin(t + i) * 14).toFixed(0)}" cy="${y.toFixed(0)}" r="${rad.toFixed(1)}" fill="#fff" opacity="${(.4 + r() * .45).toFixed(2)}"/>`; }
  return `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0">${o}</svg>`;
}


const BG = {}; const layers = (k, s) => BG[k + s] || (BG[k + s] = bgLayers(k, s));
module.exports = { bgLayers, layers, snowDots, KINDS, W, H };
