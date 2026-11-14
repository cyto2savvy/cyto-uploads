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
    else if (kind === 'prostate') {   // clinical diagram: bladder above, the gland (gold = the subject) below, urethra through it. Ep 16.
      const pp = 1 + Math.sin(lt * 3.2) * .03;
      body = O('M-96 -150 Q-128 -62 -70 -22 Q0 14 70 -22 Q128 -62 96 -150 Q0 -182 -96 -150Z', '#ffd9e3', 9) +
        `<path d="M-58 -128 Q-78 -78 -50 -44" stroke="${WHITE}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".55"/>` +
        `<path d="M0 96 L0 150" stroke="${INK}" stroke-width="30" stroke-linecap="round"/><path d="M0 96 L0 150" stroke="${PINK}" stroke-width="14" stroke-linecap="round"/>` +
        `<g transform="translate(0,52) scale(${pp.toFixed(3)})">` + sticker(O('M-74 -44 Q-104 6 -58 46 Q0 74 58 46 Q104 6 74 -44 Q0 -68 -74 -44Z', GOLD, 9)) +
        `<path d="M-44 -26 Q-60 4 -36 26" stroke="${WHITE}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".6"/><path d="M0 -40 L0 50" stroke="${INK}" stroke-width="7" stroke-linecap="round" stroke-dasharray="4 14"/></g>`;
    }
    else if (kind === 'brain') body = `<g transform="scale(.92)">` +   // same cut-out brain as the thumbnail hero (thumbs.js). Ep 17.
      O('M-20 -140 C-140 -160 -190 -40 -140 20 C-190 80 -130 160 -40 130 C0 170 70 160 90 120 C170 130 200 40 150 -10 C190 -70 130 -150 40 -120 C20 -150 0 -145 -20 -140Z', PINK, 9) +
      `<path d="M0 -130 V120 M-80 -60 Q-40 -30 0 -50 M80 -40 Q40 0 0 20 M-90 50 Q-40 70 0 40" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round"/>` +
      `<path d="M-110 -70 Q-120 -110 -70 -118" stroke="${WHITE}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".5"/></g>`;
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
        (p.plate ? `<rect x="${-W / 2 + 4}" y="${-H / 2 + 2}" width="${W - 8}" height="${H - 4}" rx="24" fill="${p.plate === true ? WHITE : p.plate}" stroke="${INK}" stroke-width="8"/>` : '') +
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

  // ---- Ep 18 (library sprint, HARD_RULES 25) ----
  // ECG trace that draws on left to right, then keeps sweeping like a monitor: a new beat (spike + heart blip) every `period` s
  ecgLine(p, lt) {
    const t0 = p.in || 0, W = 560, H = 250, mid = 150, period = p.period || 1.1, beats = 3, bw = (W - 60) / beats;
    let d = `M30 ${mid}`;
    for (let i = 0; i < beats; i++) { const x = 30 + i * bw; d += ` L${x + bw * .30} ${mid} L${x + bw * .38} ${mid - 16} L${x + bw * .46} ${mid} L${x + bw * .52} ${mid + 22} L${x + bw * .60} ${mid - 104} L${x + bw * .68} ${mid + 42} L${x + bw * .76} ${mid} L${x + bw} ${mid}`; }
    const L = 1150, a = lt - t0, first = ease(a / 0.8), col = p.color || '#ff5a5f';
    const ph = a < 0.8 ? first : ((a - 0.8) % period) / period, sweeping = a >= 0.8;       // after the first draw-on, an erase bar sweeps across and the trace redraws behind it
    const dash = sweeping ? `stroke-dasharray="${(L * ph).toFixed(0)} ${(L * .12).toFixed(0)} ${L}"` : `stroke-dasharray="${L}" stroke-dashoffset="${(L * (1 - first)).toFixed(0)}"`;
    const beat = Math.floor(Math.max(0, a) / (period / 1)) , bp = ((Math.max(0, a) % period) / period), pulse = 1 + .28 * Math.pow(Math.max(0, Math.sin(bp * Math.PI)), 6);
    const events = []; for (let e = t0; e <= t0 + 9; e += period) events.push(+e.toFixed(2));
    // `rest: true` (Ep 18 redo): shade the flat stretch after each spike = the pause between beats (diastole), one band per beat, popping in turn
    const rest = !p.rest ? '' : Array.from({ length: beats }, (_, i) => { const x0 = 30 + i * bw + bw * .78, x1 = 30 + (i + 1) * bw + bw * .28, pp = backOut((a - 0.5 - i * 0.35) / 0.3); if (pp <= 0 || i === beats - 1) return '';
      return `<g opacity="${Math.min(1, pp).toFixed(2)}"><rect x="${x0.toFixed(0)}" y="34" width="${(x1 - x0).toFixed(0)}" height="${H - 68}" rx="12" fill="${TEAL}" opacity="${(.3 + .12 * Math.sin(a * 5 + i)).toFixed(2)}"/>` +
        `<g transform="translate(${((x0 + x1) / 2).toFixed(0)},${H - 62}) scale(${Math.max(.01, pp).toFixed(3)})"><rect x="-52" y="-22" width="104" height="40" rx="14" fill="${WHITE}" stroke="${INK}" stroke-width="6"/>${txt(0, 8, p.rest === true ? 'REST' : p.rest, 26, INK, 900, 'middle', 0)}</g></g>`; }).join('');
    return {
      svg: `<rect x="6" y="20" width="${W - 12}" height="${H - 40}" rx="26" fill="#0f2238" stroke="${INK}" stroke-width="9"/>` +
        [1, 2, 3].map(i => `<path d="M24 ${20 + i * (H - 40) / 4} H${W - 24}" stroke="#27496b" stroke-width="3"/>`).join('') + [1, 2, 3, 4, 5].map(i => `<path d="M${i * W / 6} 34 V${H - 34}" stroke="#27496b" stroke-width="3"/>`).join('') +
        rest + `<path d="${d}" fill="none" stroke="${col}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round" ${dash}/>` +
        `<g transform="translate(${W - 74},66) scale(${(pulse * .2).toFixed(3)})">${O('M0 150 C-190 20 -150 -170 -45 -165 C-15 -160 0 -130 0 -110 C0 -130 15 -160 45 -165 C150 -170 190 20 0 150Z', col, 34)}</g>`,
      w: W, h: H, events
    };
  },

  // the #BicepHeart pose: a cut-out arm flexes (fist up), the other hand presses the inside of the bicep, and the shape pops into a heart
  bicepHeart(p, lt) {
    const t0 = p.in || 0, W = 420, H = 420, a = lt - t0, col = p.color || GOLD, col2 = p.color2 || '#e2a51c';
    const flex = backOut(a / 0.45), press = ease((a - 0.5) / 0.3), hp = backOut((a - 0.8) / 0.4), beat = 1 + (hp > .9 ? Math.pow(Math.max(0, Math.sin((a - 1.2) * 5.2)), 4) * .09 : 0);
    const limb = (d, w2, c = col) => `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${w2 + 18}" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="${c}" stroke-width="${w2}" stroke-linecap="round" stroke-linejoin="round"/>`;
    const heart = 'M0 150 C-190 20 -150 -170 -45 -165 C-15 -160 0 -130 0 -110 C0 -130 15 -160 45 -165 C150 -170 190 20 0 150Z';
    const fore = -90 * Math.min(1.06, flex) + 40 * (1 - Math.min(1, flex));       // forearm swings up to vertical as the arm flexes
    const events = [t0, +(t0 + .5).toFixed(2), +(t0 + .8).toFixed(2)]; for (let e = t0 + 1.7; e <= t0 + 6; e += 0.9) events.push(+e.toFixed(2));
    const bul = 36 + 14 * Math.min(1, flex);
    return {
      svg: `<g transform="translate(46,338)">` + limb('M0 0 L214 0', 86) +                                                  // upper arm, shoulder at the left
        `<g transform="translate(214,0) rotate(${fore.toFixed(1)})">` + limb('M0 0 L176 0', 70) + `<circle cx="196" cy="0" r="54" fill="${col}" stroke="${INK}" stroke-width="9"/><path d="M176 -30 Q200 -44 222 -28" stroke="${WHITE}" stroke-width="9" fill="none" stroke-linecap="round" opacity=".5"/></g>` +
        (hp < 1 ? `<ellipse cx="104" cy="-46" rx="78" ry="${bul}" fill="${col}" stroke="${INK}" stroke-width="9" opacity="${(1 - clamp(hp, 0, 1)).toFixed(2)}"/>` : '') +
        // the bicep pops into a heart
        (hp > 0 ? `<g transform="translate(104,-58) scale(${(Math.max(.01, hp) * beat * .64).toFixed(3)})"><path d="${heart}" fill="none" stroke="${WHITE}" stroke-width="44" stroke-linejoin="round"/><path d="${heart}" fill="#ff5a5f" stroke="${INK}" stroke-width="15" stroke-linejoin="round"/><path d="M-95 -105 Q-120 -50 -85 -10" stroke="${WHITE}" stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/></g>` : '') +
        `</g>` +
        // the other hand: a round mitt (no fingers) that comes down from the upper left and presses the top of the bicep
        (press > 0 ? `<g transform="translate(${(-70 + 70 * press).toFixed(1)},${(-90 + 90 * press).toFixed(1)})" opacity="${Math.min(1, press * 3).toFixed(2)}">` + limb('M16 52 L122 158', 50, col2) + `<circle cx="138" cy="172" r="38" fill="${col2}" stroke="${INK}" stroke-width="9"/></g>` : ''),
      w: W, h: H, events
    };
  },

  // big rounded muscle-cell cross-section; bean-shaped mitochondria fill in until they cover `fill_share` of the cell, then keep sparking (running nonstop)
  cellSlice(p, lt) {
    const t0 = p.in || 0, W = 640, H = 470, a = lt - t0, share = p.fill_share == null ? 0.33 : p.fill_share, spread = p.spread || 1.6;
    const cw = 560, chh = 300, cx = W / 2, cy = 176, rx = 70, cellArea = cw * chh - (4 - Math.PI) * rx * rx;
    const bw = 31, bh = 15.5, beanArea = Math.PI * bw * bh, n = Math.round(share * cellArea / beanArea);           // the beans really do cover `share` of the drawn cell
    const cols = 10, rows = 6, slots = [];
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const x = cx - cw / 2 + 50 + c * ((cw - 100) / (cols - 1)), y = cy - chh / 2 + 38 + r * ((chh - 76) / (rows - 1));
      if (Math.hypot((x - cx) / 1.25, y - cy) < 62) continue;                                                       // keep the nucleus clear
      slots.push([x, y, (r * 7 + c * 13) % 5]);
    }
    let s0 = 7; const rr = () => (s0 = (s0 * 16807) % 2147483647) / 2147483647;
    const order = slots.map((s, i) => [rr(), i]).sort((x, y) => x[0] - y[0]).slice(0, Math.min(n, slots.length)).map(x => slots[x[1]]);
    const col = p.kind === 'heartCell' || !p.kind ? '#e8627a' : '#f08fa0', mito = '#ffa93a';
    let g = `<rect x="${cx - cw / 2}" y="${cy - chh / 2}" width="${cw}" height="${chh}" rx="${rx}" fill="${col}" stroke="${INK}" stroke-width="10"/>` +
      [-2, -1, 0, 1, 2].map(i => `<path d="M${cx + i * 96} ${cy - chh / 2 + 14} V${cy + chh / 2 - 14}" stroke="#c94863" stroke-width="7" opacity=".55"/>`).join('') +            // striations: it is muscle
      `<path d="M${cx - cw / 2 + 40} ${cy - chh / 2 + 34} Q${cx - cw / 2 + 22} ${cy} ${cx - cw / 2 + 40} ${cy + 60}" stroke="${WHITE}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".4"/>` +
      `<ellipse cx="${cx}" cy="${cy}" rx="62" ry="46" fill="#7d3bb0" stroke="${INK}" stroke-width="8"/><ellipse cx="${cx - 14}" cy="${cy - 10}" rx="20" ry="13" fill="#b07fe0" opacity=".8"/>`;
    order.forEach(([x, y, k], i) => {
      const st = 0.25 + (i / order.length) * spread, pop = backOut((a - st) / 0.3); if (pop <= 0) return;
      const spark = Math.pow(Math.max(0, Math.sin((a - st) * 2.6 + i * 1.7)), 8);                                  // each plant keeps firing
      g += `<g transform="translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${k * 36 - 70}) scale(${(Math.max(.01, pop) * (1 + .1 * spark)).toFixed(3)})"><rect x="${-bw}" y="${-bh}" width="${bw * 2}" height="${bh * 2}" rx="${bh}" fill="${mito}" stroke="${INK}" stroke-width="6"/>` +
        `<path d="M-18 6 L-10 -6 L-2 6 L6 -6 L14 6" stroke="${INK}" stroke-width="4" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".75"/>` + (spark > .5 ? `<circle cx="0" cy="-22" r="${(5 + 5 * spark).toFixed(1)}" fill="${GOLD}" stroke="${INK}" stroke-width="3"/>` : '') + `</g>`;
    });
    // a three-part bar: one part fills = one third (no numerals)
    const by = H - 104, k3 = ease((a - 0.25) / spread), seg = 150;
    g += [0, 1, 2].map(i => `<rect x="${cx - 1.5 * seg - 8 + i * (seg + 8)}" y="${by}" width="${seg}" height="30" rx="12" fill="${i === 0 ? mito : '#e6ebf2'}" opacity="${i === 0 ? (0.25 + .75 * k3).toFixed(2) : 1}" stroke="${INK}" stroke-width="7"/>`).join('');
    if (p.label) g += `<g transform="translate(${cx},${H - 30})"><rect x="-150" y="-36" width="300" height="62" rx="24" fill="${WHITE}" stroke="${INK}" stroke-width="8"/>${txt(0, 10, p.label, 38, INK, 900, 'middle', 0)}</g>`;
    const events = spanEvents(t0, 0.25 + spread, 0.55); for (let e = t0 + 0.25 + spread + 0.9; e <= t0 + 9; e += 0.9) events.push(+e.toFixed(2));
    return { svg: g, w: W, h: H, events, beans: order.length, share: +(order.length * beanArea / cellArea).toFixed(3) };
  },

  // two vertical gauges: the first stays low and steady, the second fills red and "burns". No numerals unless show_numbers.
  fatigueMeter(p, lt) {
    const t0 = p.in || 0, W = 460, H = 440, a = lt - t0, labs = p.labels || ['HEART', 'BICEP'], vals = p.values || [20, 90], dur = p.dur || 1.5;
    const gw = 110, gh = 290, top = 26, xs = [W / 2 - 112, W / 2 + 112];
    let g = '';
    xs.forEach((x, i) => {
      const hot = vals[i] >= 60, k = ease((a - 0.2 - i * 0.15) / (hot ? dur : 0.5)), wob = hot ? (k > .97 ? Math.sin(a * 9) * .012 : 0) : Math.sin(a * 2 * Math.PI / 0.9) * .035;   // heart ticks along steadily; bicep trembles at the top
      const lvl = clamp(vals[i] / 100 * k + wob, 0, 1), fh = (gh - 16) * lvl, fc = hot ? (lvl > .66 ? RED : lvl > .4 ? '#ff8a3a' : GOLD) : TEAL;
      g += `<g transform="translate(${x},0)"><rect x="${-gw / 2}" y="${top}" width="${gw}" height="${gh}" rx="30" fill="#e6ebf2" stroke="${INK}" stroke-width="10"/>` +
        `<rect x="${-gw / 2 + 9}" y="${(top + gh - 8 - fh).toFixed(1)}" width="${gw - 18}" height="${fh.toFixed(1)}" rx="22" fill="${fc}"/>` +
        [1, 2, 3].map(j => `<path d="M${-gw / 2 + 8} ${top + j * gh / 4} h22" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`).join('') +
        `<rect x="${-gw / 2 + 16}" y="${top + 22}" width="14" height="${gh - 60}" rx="7" fill="${WHITE}" opacity=".45"/>` +
        (hot && k > .92 ? [-1, 0, 1].map(j => `<path d="M${j * 30} ${top - 6 - ((a * 60 + j * 17) % 26)} q-9 -12 0 -22 q9 -10 0 -22" stroke="${RED}" stroke-width="7" fill="none" stroke-linecap="round" opacity="${(.9 - ((a * 60 + j * 17) % 26) / 30).toFixed(2)}"/>`).join('') : '') +
        (p.show_numbers ? txt(0, top + gh / 2, Math.round(vals[i] * k), 46, INK, 900, 'middle', 0) : '') +
        `<g transform="translate(0,${top + gh + 50})"><rect x="-98" y="-36" width="196" height="60" rx="22" fill="${WHITE}" stroke="${INK}" stroke-width="8"/>${txt(0, 9, labs[i] || '', 36, INK, 900, 'middle', 0)}</g></g>`;
    });
    const events = spanEvents(t0, 0.35 + dur, 0.55); for (let e = t0 + 0.35 + dur + 0.9; e <= t0 + 8; e += 0.9) events.push(+e.toFixed(2));
    return { svg: g, w: W, h: H + 20, events };
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
  const OUT = 0.25, gone = p.out != null ? clamp((p.out + OUT - lt) / OUT, 0, 1) : 1;   // HARD_RULES 21: leaves <= 1.5 s after its sentence
  if (vis <= 0 || gone <= 0) return { html: '', events: r.events.map(e => e), id: `${scId}:${p.t}${i}`, visible: false };
  // props FILL the stage (scale up, not just down): `fill` = share of the stage height this prop takes.
  const stageH = stage.bottom - stage.top;
  let auto = ((p.fill == null ? 0.5 : p.fill) * stageH) / r.h;
  if (r.w * auto > 900) auto = 900 / r.w;
  const s = auto * (p.scale || 1) * (0.9 + 0.1 * pop) * (0.8 + 0.2 * gone);
  const hw = (r.w * s) / 2, hh = (r.h * s) / 2;
  const x = clamp(p.at[0], 70 + hw, 1010 - hw), y = clamp(stage.top + stageH * p.at[1], stage.top + hh, stage.bottom - hh);
  const dy = Math.sin(lt * 1.5 + i) * 5;
  return {
    id: `${scId}:${p.t}${i}`, visible: true, events: r.events,
    html: `<div data-prop="${scId}:${p.t}${i}" style="position:absolute;left:${x.toFixed(1)}px;top:${(y + dy).toFixed(1)}px;width:${r.w}px;height:${r.h}px;margin-left:${(-r.w / 2).toFixed(1)}px;margin-top:${(-r.h / 2).toFixed(1)}px;transform:scale(${s.toFixed(4)});opacity:${(vis * gone).toFixed(2)};filter:drop-shadow(7px 10px 0 rgba(10,31,36,.38))">` +
      `<svg width="${r.w}" height="${r.h}" viewBox="0 0 ${r.w} ${r.h}" style="overflow:visible">${r.svg}</svg></div>`
  };
}
module.exports = { propHtml, normalize, PROPS, GLYPH };
