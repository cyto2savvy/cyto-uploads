#!/usr/bin/env node
// CANON v2 SCENE PROPS (HARD_RULES 5): drawn cut-out visuals that fill the middle of the frame in every scene.
// Same drawing language as Cyto: thick #0a1f24 outline, flat fill + one highlight, hard drop shadow, white sticker edge on heroes.
// Every prop pops in with overshoot and keeps moving (grow / count / draw-on / stagger / sway) so nothing is static > 1 s.
//
// A scene declares:  "props":[{"t":"bars","at":[540,0.52],"in":0.4,...}, ...]        (>= 2 per scene)
//   t   = prop type (see PROPS below)           at = [frame x px, y as 0..1 of the prop stage]   in = seconds into the scene
//   scale, w/h overrides optional. A bare string ("bars") is shorthand for {t:"bars"}.
// propHtml() returns the positioned HTML plus `events` = times a NEW thing appears (compose.js checks the <= 2 s rule).
const INK = '#0a1f24', GOLD = '#ffc83a', TEAL = '#3fd0bb', TEAL2 = '#2fae9b', RED = '#c62828', WHITE = '#fff', NAVY = '#16254f', PINK = '#ff9db8';
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), ease = x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
const backOut = x => { x = clamp(x, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const O = (d, f, sw = 9, extra = '') => `<path d="${d}" fill="${f}" stroke="${INK}" stroke-width="${sw}" stroke-linejoin="round" stroke-linecap="round" ${extra}/>`;
const txt = (x, y, s, size, fill = WHITE, w = 900, anchor = 'middle', stroke = 10) =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Arial Black,Inter,Impact,sans-serif" font-weight="${w}" font-size="${size}" fill="${fill}" stroke="${INK}" stroke-width="${stroke}" paint-order="stroke" stroke-linejoin="round">${s}</text>`;
const spanEvents = (t0, span, step = 0.6) => { const o = []; for (let e = t0; e <= t0 + span + 1e-6; e += step) o.push(+e.toFixed(2)); if (o[o.length-1] < t0 + span) o.push(+(t0 + span).toFixed(2)); return o; };
const sticker = (inner) => `<g>${inner.replace(/stroke-width="(\d+)"/g, (m, n) => `stroke-width="${+n + 16}"`).replace(/stroke="#0a1f24"/g, `stroke="${WHITE}"`)}</g>${inner}`;

// ---------------------------------------------------------------- glyphs reused by icons / grids
const GLYPH = {
  person: (f = TEAL) => `<circle cx="0" cy="-30" r="17" fill="${f}" stroke="${INK}" stroke-width="7"/>` + O('M-22 34 Q-22 -6 0 -6 Q22 -6 22 34Z', f, 7),
  organ: (f = PINK) => O('M-24 -30 Q-40 0 -24 30 Q0 44 24 30 Q40 0 24 -30 Q0 -44 -24 -30Z', f, 7) + `<path d="M-10 -14 Q0 0 10 14" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round"/>`,
  shoe: (f = WHITE) => O('M-38 18 L-38 -8 Q-20 -14 -6 -2 Q10 12 38 12 L38 22 Q0 30 -38 18Z', f, 7) + `<path d="M-24 -4 L-18 10 M-8 2 L-2 16" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`,
  cell: (f = TEAL) => `<circle r="26" fill="${f}" stroke="${INK}" stroke-width="7"/><circle cx="-7" cy="-6" r="8" fill="${TEAL2}"/><circle cx="10" cy="8" r="5" fill="${TEAL2}"/>`,
  check: () => `<circle r="26" fill="${TEAL}" stroke="${INK}" stroke-width="7"/><path d="M-12 1 L-3 11 L13 -9" stroke="${INK}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
};

// ---------------------------------------------------------------- props.  each: (p, lt) -> {svg, w, h, events}
const PROPS = {
  // two growing bars with counting values — the trial result
  bars(p, lt) {
    const vals = p.values || [80, 74], labs = p.labels || [], unit = p.unit == null ? '%' : p.unit, t0 = p.in || 0;
    const W = 640, H = 430, base = H - 96, top = 84, bw = 168, gap = 96;
    const x0 = (W - (vals.length * bw + (vals.length - 1) * gap)) / 2, mx = Math.max(...vals) * 1.1, hi = vals.indexOf(Math.max(...vals));
    let g = `<path d="M${x0 - 46} ${base + 7} H${W - x0 + 46}" stroke="${INK}" stroke-width="11" stroke-linecap="round"/>`;
    const events = spanEvents(t0, 0.3 + (vals.length - 1) * 0.55 + 0.85, 0.55);
    vals.forEach((v, i) => {
      const st = t0 + 0.3 + i * 0.55;
      const gr = ease((lt - st) / 0.85), h = (base - top) * (v / mx) * gr, x = x0 + i * (bw + gap), y = base - h;
      const wob = Math.sin((lt - st) * 3.1 + i) * (gr > .95 ? 3 : 0);
      if (gr <= 0) return;
      g += `<g transform="translate(0,${wob.toFixed(1)})">${O(`M${x} ${base} L${x} ${y + 16} Q${x} ${y} ${x + 16} ${y} L${x + bw - 16} ${y} Q${x + bw} ${y} ${x + bw} ${y + 16} L${x + bw} ${base}Z`, i === hi ? GOLD : '#cfd8e3', 9)}` +
        `<rect x="${x + 16}" y="${y + 18}" width="26" height="${Math.max(0, h - 40)}" fill="${WHITE}" opacity=".45" rx="12"/>` +
        txt(x + bw / 2, y - 26, Math.round(v * gr) + unit, 68, i === hi ? GOLD : WHITE) +
        (labs[i] ? txt(x + bw / 2, base + 62, labs[i], 34, WHITE, 900, 'middle', 9) : '') + `</g>`;
    });
    return { svg: g, w: W, h: H, events };
  },

  // a number that rolls up while a crowd of dots fills in behind it
  counter(p, lt) {
    const to = p.to == null ? 100 : p.to, t0 = p.in || 0, W = 620, H = 330, dur = p.dur || 1.3;
    const k = ease((lt - t0 - 0.2) / dur), val = to * k, events = spanEvents(t0, 0.2 + dur, 0.55);
    const fmt = v => p.suffix ? v.toFixed(p.decimals == null ? 2 : p.decimals) + p.suffix : Math.round(v).toLocaleString('en-US');
    let dots = '';
    const cols = 18, rows = 6, N = cols * rows;
    for (let i = 0; i < N; i++) {
      const on = i / N < k; if (!on) continue;
      const cx = 44 + (i % cols) * ((W - 88) / (cols - 1)), cy = 44 + Math.floor(i / cols) * 46;
      const a = clamp((k - i / N) * 14, 0, 1);
      dots += `<circle cx="${cx.toFixed(1)}" cy="${(cy + Math.sin(lt * 2 + i) * 2).toFixed(1)}" r="${(9 * a).toFixed(1)}" fill="${TEAL}" stroke="${INK}" stroke-width="4" opacity="${(a * .9).toFixed(2)}"/>`;
    }
    const pulse = 1 + (k > .99 ? Math.sin(lt * 4) * .012 : 0);
    return {
      svg: dots + `<g transform="translate(${W / 2},${H - 74}) scale(${pulse.toFixed(3)})">` +
        `<rect x="-250" y="-74" width="500" height="118" rx="28" fill="${NAVY}" stroke="${INK}" stroke-width="9"/>` +
        txt(0, 16, fmt(val), 86, GOLD, 900, 'middle', 11) + `</g>` +
        (p.label ? txt(W / 2, H - 6, p.label, 36, WHITE) : ''), w: W, h: H, events
    };
  },

  // big arrow that DRAWS ON, with the headline number in a stamp at its head
  arrowStat(p, lt) {
    const t0 = p.in || 0, W = 470, H = 470, down = p.dir !== 'up';
    const d = down ? `M80 40 Q60 210 220 258` : `M80 430 Q60 260 220 212`;
    const L = 400, dash = L * ease((lt - t0) / 0.7), events = spanEvents(t0, 1.2, 0.55);
    const head = down ? `M258 278 L169 295 L193 215Z` : `M258 192 L169 175 L193 255Z`;
    const hp = backOut((lt - t0 - 0.5) / 0.4), lp = backOut((lt - t0 - 0.72) / 0.45);
    const sway = Math.sin(lt * 1.9) * 4, hx = 258, hy = down ? 278 : 192;
    const stroke = (col, wid) => `<path d="${d}" fill="none" stroke="${col}" stroke-width="${wid}" stroke-linecap="round" stroke-dasharray="${L}" stroke-dashoffset="${(L - dash).toFixed(1)}"/>`;
    return {
      svg: `<g transform="translate(0,${sway.toFixed(1)})">` + stroke(WHITE, 48) + stroke(INK, 32) + stroke(RED, 17) +
        (hp > 0 ? `<g transform="translate(${hx},${hy}) scale(${Math.max(.01, hp).toFixed(3)}) translate(${-hx},${-hy})">${sticker(O(head, RED, 9))}</g>` : '') +
        (lp > 0 ? `<g transform="translate(${W / 2},${H - 76}) rotate(${(-7 + Math.sin(lt * 2) * 2).toFixed(1)}) scale(${Math.max(.01, lp).toFixed(3)})">` +
          `<rect x="-134" y="-58" width="268" height="116" rx="26" fill="${GOLD}" stroke="${INK}" stroke-width="10"/>` + txt(0, 22, p.label || '-28%', 72, INK, 900, 'middle', 0) + `</g>` : '') + `</g>`,
      w: W, h: H, events
    };
  },

  // a row/grid of glyphs that pop in one after another
  icons(p, lt) {
    const n = p.n || 8, g = p.glyph || 'organ', cols = p.cols || Math.min(n, 7), t0 = p.in || 0;
    const step = p.spread != null ? p.spread / Math.max(1, n - 1) : (p.step || 0.1);
    const cw = 92, ch = 96, rows = Math.ceil(n / cols), W = cols * cw, H = rows * ch + (p.label ? 58 : 0);
    const events = spanEvents(t0, (n - 1) * step + 0.38, 0.55);
    let s = '';
    for (let i = 0; i < n; i++) {
      const st = t0 + i * step;
      const pop = backOut((lt - st) / 0.38); if (pop <= 0) continue;
      const x = (i % cols) * cw + cw / 2, y = Math.floor(i / cols) * ch + ch / 2;
      const bob = Math.sin(lt * 2.2 + i * .7) * 4;
      const col = p.hi != null && i < p.hi ? GOLD : undefined;
      s += `<g transform="translate(${x},${(y + bob).toFixed(1)}) scale(${Math.max(.01, pop).toFixed(3)})">${GLYPH[g] ? GLYPH[g](col || (g === 'organ' ? PINK : g === 'shoe' ? WHITE : TEAL)) : GLYPH.cell(col)}</g>`;
    }
    if (p.label) s += txt(W / 2, H - 8, p.label, 46, WHITE);
    return { svg: s, w: W, h: H, events };
  },

  // drawn organ cut-out (tube-style colon, lungs, stomach) with a pulse and a label chip
  organ(p, lt) {
    const t0 = p.in || 0, W = 420, H = 400, kind = p.kind || 'colon';
    const pulse = 1 + Math.sin(lt * 2.6) * .022, events = [t0];
    const tube = (d, f) => `<path d="${d}" fill="none" stroke="${INK}" stroke-width="66" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="${d}" fill="none" stroke="${f}" stroke-width="48" stroke-linecap="round" stroke-linejoin="round"/>` +
      `<path d="${d}" fill="none" stroke="${WHITE}" stroke-width="12" stroke-linecap="round" opacity=".35" transform="translate(-9,-11)"/>`;
    let body;
    if (kind === 'lungs') body = O('M-14 -120 L14 -120 L14 -30 L-14 -30Z', PINK, 9) + O('M-20 -70 Q-150 -40 -140 90 Q-134 160 -70 150 Q-20 142 -20 60Z', PINK, 9) + O('M20 -70 Q150 -40 140 90 Q134 160 70 150 Q20 142 20 60Z', PINK, 9);
    else body = tube('M-130 150 L-130 -40 Q-130 -118 -52 -118 L52 -118 Q130 -118 130 -40 L130 92 Q130 140 76 140 L40 140', PINK);
    return {
      svg: `<g transform="translate(${W / 2},${H / 2 - (p.label ? 24 : 0)}) scale(${pulse.toFixed(3)})">${body}</g>` +
        (p.label ? `<g transform="translate(${W / 2},${H - 30})"><rect x="-140" y="-40" width="280" height="68" rx="24" fill="${WHITE}" stroke="${INK}" stroke-width="8"/>${txt(0, 10, p.label, 40, INK, 900, 'middle', 0)}</g>` : ''),
      w: W, h: H, events
    };
  },

  // rubber stamp that slams in and settles (caveats, labels)
  stamp(p, lt) {
    const t0 = p.in || 0, lines = (p.text || 'LINKED, NOT PROVEN').split('\n');
    const mx = Math.max(...lines.map(l => l.length)), W = Math.max(320, mx * 30 + 112), H = lines.length * 62 + 60;
    const k = clamp((lt - t0) / 0.42, 0, 1), sc = k <= 0 ? 0 : 1 + 0.55 * Math.pow(1 - k, 2.2) * Math.cos(k * 7);
    const rot = (p.rot == null ? -7 : p.rot) + Math.sin(lt * 1.6) * 1.2, col = p.color || RED;
    return {
      svg: `<g transform="translate(${W / 2},${H / 2}) rotate(${rot.toFixed(2)}) scale(${Math.max(.01, sc).toFixed(3)})">` +
        `<rect x="${-W / 2 + 10}" y="${-H / 2 + 8}" width="${W - 20}" height="${H - 16}" rx="20" fill="none" stroke="${col}" stroke-width="12"/>` +
        `<rect x="${-W / 2 + 24}" y="${-H / 2 + 20}" width="${W - 48}" height="${H - 40}" rx="12" fill="none" stroke="${col}" stroke-width="5" opacity=".7"/>` +
        lines.map((l, i) => txt(0, -H / 2 + 60 + i * 62, l, 46, col, 900, 'middle', 0)).join('') + `</g>`,
      w: W, h: H, events: [t0]
    };
  },

  // titled cut-out card with a tick grid that fills (e.g. 36 months of a 3-year plan)
  card(p, lt) {
    const t0 = p.in || 0, n = p.ticks || 36, cols = p.cols || 12, W = 520, H = 272 + (p.foot ? 56 : 0);
    const k = ease((lt - t0 - 0.25) / (p.dur || 1.1)), rows = Math.ceil(n / cols), events = spanEvents(t0, 0.25 + (p.dur || 1.1), 0.55);
    let g = `<rect x="10" y="10" width="${W - 20}" height="${H - 20}" rx="26" fill="${WHITE}" stroke="${INK}" stroke-width="9"/>` + txt(W / 2, 84, p.title || '3-YEAR PLAN', 46, INK, 900, 'middle', 0);
    const gw = (W - 120) / cols;
    for (let i = 0; i < n; i++) {
      const on = i / n < k; const x = 60 + (i % cols) * gw, y = 130 + Math.floor(i / cols) * 44;
      g += `<rect x="${x.toFixed(1)}" y="${y}" width="${(gw - 8).toFixed(1)}" height="30" rx="8" fill="${on ? TEAL : '#e6ebf2'}" stroke="${INK}" stroke-width="5"/>`;
    }
    if (p.foot) g += txt(W / 2, H - 26, p.foot, 32, INK, 900, 'middle', 0);
    return { svg: g, w: W, h: H, events };
  },

  // running shoe with motion lines (exercise hero)
  shoe(p, lt) {
    const t0 = p.in || 0, W = 420, H = 260, bob = Math.sin(lt * 3.4) * 7, sl = (lt * 220) % 150;
    const body = O('M-170 60 L-170 -20 Q-96 -46 -40 -2 Q24 50 170 44 L170 74 Q0 104 -170 60Z', WHITE, 9) +
      O('M-170 60 Q0 104 170 74 L170 92 Q0 122 -170 80Z', RED, 9) +
      `<path d="M-108 -12 L-88 44 M-62 6 L-40 60 M-18 30 L2 74" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`;
    const trail = [0, 1, 2].map(i => `<path d="M${(14 + sl * .4 - i * 18).toFixed(0)} ${86 + i * 46} h${72 - i * 16}" stroke="${WHITE}" stroke-width="13" stroke-linecap="round" opacity="${(.65 - i * .17).toFixed(2)}"/>`).join('');
    return { svg: trail + `<g transform="translate(${W / 2 + 22},${(H / 2 + bob).toFixed(1)})">${sticker(body)}</g>`, w: W, h: H, events: [t0] };
  },

  // cut-out runner, legs and arms cycling, drifts across the stage
  runner(p, lt) {
    const t0 = p.in || 0, W = 320, H = 380, ph = lt * 6.2, sw = Math.sin(ph), col = p.color || GOLD;
    const hop = Math.abs(Math.sin(ph)) * 9, cx = W / 2, cy = H / 2 + 30;
    const limb = (d, x, y, a, wid) => `<g transform="translate(${x},${y}) rotate(${a.toFixed(1)})"><path d="${d}" fill="none" stroke="${INK}" stroke-width="${wid + 14}" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="${col}" stroke-width="${wid}" stroke-linecap="round" stroke-linejoin="round"/></g>`;
    const legD = 'M0 0 L14 56 L-14 104', armD = 'M0 0 L30 38 L6 66';
    return {
      svg: `<g transform="translate(${cx},${(cy - hop).toFixed(1)})">` +
        limb(legD, 0, 10, 24 + sw * 34, 26) + limb(armD, 6, -64, -34 - sw * 46, 22) +
        O('M-38 14 Q-44 -78 4 -82 Q48 -78 42 14 Q0 26 -38 14Z', col, 9) +
        limb(legD, 0, 10, -22 - sw * 34, 26) + limb(armD, 6, -64, 30 + sw * 46, 22) +
        `<circle cx="14" cy="-116" r="38" fill="${col}" stroke="${INK}" stroke-width="9"/>` +
        `<path d="M-22 -128 Q14 -164 52 -126 Z" fill="#2c63d6" stroke="${INK}" stroke-width="9" stroke-linejoin="round"/>` +
        `<circle cx="30" cy="-112" r="5" fill="${INK}"/>` + `</g>`,
      w: W, h: H, events: [t0]
    };
  },

  // TTC stop pole + sign (Toronto payoff)
  stopSign(p, lt) {
    const t0 = p.in || 0, W = 300, H = 400, sway = Math.sin(lt * 1.4) * 1.6;
    return {
      svg: `<g transform="translate(${W / 2},${H}) rotate(${sway.toFixed(2)})">` +
        `<rect x="-12" y="-340" width="24" height="340" fill="#9fb0c0" stroke="${INK}" stroke-width="8"/>` +
        `<g transform="translate(0,-300)"><rect x="-108" y="-78" width="216" height="150" rx="18" fill="${WHITE}" stroke="${INK}" stroke-width="9"/>` +
        `<rect x="-108" y="-78" width="216" height="46" rx="18" fill="${RED}" stroke="${INK}" stroke-width="9"/>` +
        txt(0, -42, p.title || 'STOP', 36, WHITE, 900, 'middle', 0) + txt(0, 22, p.text || 'WALK IT', 44, INK, 900, 'middle', 0) + `</g></g>`,
      w: W, h: H, events: [t0]
    };
  },

  // crowd of people icons; `hi` of them highlighted (trial participants)
  peopleGrid(p, lt) {
    const n = p.n || 48, cols = p.cols || 12, t0 = p.in || 0, cw = 52, ch = 60, spread = p.spread || 0.9;
    const rows = Math.ceil(n / cols), W = cols * cw, H = rows * ch + (p.label ? 54 : 0);
    const events = spanEvents(t0, 0.2 + spread, 0.55);
    let s = '';
    for (let i = 0; i < n; i++) {
      const st = t0 + 0.2 + (i / n) * spread;
      const pop = backOut((lt - st) / 0.3); if (pop <= 0) continue;
      const x = (i % cols) * cw + cw / 2, y = Math.floor(i / cols) * ch + ch / 2;
      s += `<g transform="translate(${x},${(y + Math.sin(lt * 2 + i) * 2).toFixed(1)}) scale(${(0.72 * Math.max(.01, pop)).toFixed(3)})">${GLYPH.person(p.hi != null && i < p.hi ? GOLD : TEAL)}</g>`;
    }
    if (p.label) s += txt(W / 2, H - 8, p.label, 36, WHITE);
    return { svg: s, w: W, h: H, events };
  },
};

// ---------------------------------------------------------------- layout + html
function normalize(p, i, n) {
  if (typeof p === 'string') p = { t: p };
  p = Object.assign({}, p);
  if (p.in == null) p.in = 0.25 + i * 0.85;
  if (!p.at) p.at = n === 1 ? [540, .5] : [i % 2 ? 736 : 344, i < 2 ? .42 : .74];
  return p;
}
// stage = {top, bottom} in frame px. Returns {html, events, id} or null before the prop appears.
function propHtml(prop, lt, scId, i, n, stage) {
  const p = normalize(prop, i, n), fn = PROPS[p.t];
  if (!fn) return null;
  const r = fn(p, lt);
  const vis = clamp((lt - p.in) / 0.14, 0, 1), pop = backOut((lt - p.in) / 0.44);
  if (vis <= 0) return { html: '', events: r.events.map(e => e), id: `${scId}:${p.t}${i}`, visible: false };
  // props FILL the stage (scale up, not just down): `fill` = share of the stage height this prop takes.
  const stageH = stage.bottom - stage.top;
  let auto = ((p.fill == null ? 0.5 : p.fill) * stageH) / r.h;
  if (r.w * auto > 900) auto = 900 / r.w;
  const s = auto * (p.scale || 1) * (0.9 + 0.1 * pop);
  const hw = (r.w * s) / 2, hh = (r.h * s) / 2;
  const x = clamp(p.at[0], 70 + hw, 1010 - hw), y = clamp(stage.top + stageH * p.at[1], stage.top + hh, stage.bottom - hh);
  const dy = Math.sin(lt * 1.5 + i) * 5;
  return {
    id: `${scId}:${p.t}${i}`, visible: true, events: r.events,
    html: `<div data-prop="${scId}:${p.t}${i}" style="position:absolute;left:${x.toFixed(1)}px;top:${(y + dy).toFixed(1)}px;width:${r.w}px;height:${r.h}px;margin-left:${(-r.w / 2).toFixed(1)}px;margin-top:${(-r.h / 2).toFixed(1)}px;transform:scale(${s.toFixed(4)});opacity:${vis.toFixed(2)};filter:drop-shadow(7px 10px 0 rgba(10,31,36,.38))">` +
      `<svg width="${r.w}" height="${r.h}" viewBox="0 0 ${r.w} ${r.h}" style="overflow:visible">${r.svg}</svg></div>`
  };
}
module.exports = { propHtml, normalize, PROPS, GLYPH };
