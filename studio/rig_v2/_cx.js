#!/usr/bin/env node
// CANON v2 COMPOSITOR: plan.json -> 1080x1920 mp4. Every scene is a cut-out set: parallax backdrop + drawn props (props.js)
// + headline/card + word captions, with Cyto composited on top (his pose is a pure function of t, so it blends across every cut).
// usage: node compose.js plan.json out.mp4 [audio.wav] [startSec endSec]     -> also out.layout.json (layout + props + static report)
// plan: {fps,duration,fit,seed,cytoX,cytoY,cytoSize,words:[{w,start,end}],beats:[{t,emotion,gaze?}],keys:{word:color},
//        scenes:[{id,bg,start,end,headline,hot:[..],card,props:[..],transition,snow}]}
//   bg: skyline|streetcar|snow|subway|lake|plain|trail|hospital|lab
process.env.SEED = process.env.SEED || '3';
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { frameSvg } = require('./cyto_rig.js');
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
function headlineHtml(sc, lt, dur, y) {
  const m = hlMetrics(sc); if (!m.fs) return '';
  const t0 = sc.instant ? 0 : (sc.transition && sc.start > 0 ? (sc.transitionDur || 0.42) : 0);
  const hot = (sc.hot || []).map(s => s.toUpperCase()), inst = !!sc.instant;
  const p = inst ? 1 : backOut((lt - t0 - 0.1) / 0.4), fade = clamp((dur - lt) / 0.25, 0, 1) * (inst ? 1 : clamp((lt - t0 - 0.08) / 0.1, 0, 1));
  const body = m.lines.map(l => `<div>${l.split(' ').map(w => `<span style="color:${hot.includes(w.toUpperCase().replace(/[^A-Z0-9%'-]/g, '')) || hot.includes(w.toUpperCase()) ? GOLD : '#fff'}">${w}</span>`).join(' ')}</div>`).join('');
  // shrink-wrapped so the safe-zone check measures the real glyph box, not a full-width block (pop-in overshoots past 1.0)
  return `<div data-chk="headline" data-s="${p >= 0.98 ? 1 : 0}" style="position:absolute;left:50%;top:${y}px;width:max-content;max-width:880px;text-align:center;font:900 ${m.fs}px/1.04 'Arial Black','Inter',Impact,sans-serif;letter-spacing:1px;-webkit-text-stroke:${Math.round(m.fs / 9)}px ${INK};paint-order:stroke fill;text-shadow:7px 10px 0 rgba(10,31,36,.55);transform:translateX(-50%) scale(${Math.min(1, Math.max(.01, p)).toFixed(3)},${Math.max(.01, p).toFixed(3)});transform-origin:50% 0;opacity:${fade.toFixed(2)}">${body}</div>`;
}
function cardHtml(sc, lt, dur, y) {
  const m = cardMetrics(sc); if (!m.h) return '';
  const c0 = (sc.instant ? 0 : (sc.transition && sc.start > 0 ? (sc.transitionDur || 0.42) : 0)) + 0.45;
  const p = backOut((lt - c0) / 0.38), fade = clamp((dur - lt) / 0.25, 0, 1) * (lt > c0 ? 1 : 0);
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
  const lt = t - sc.start, dur = sc.end - sc.start, k = clamp(lt / dur, 0, 1);
  const L = layers(sc.bg, sc.seed || 5);
  const bg = L.map(l => `<div style="position:absolute;inset:0;transform:translateX(${(-26 * k * l.d).toFixed(2)}px) scale(${(1 + 0.085 * k * l.d).toFixed(4)});transform-origin:50% 58%">${l.s}</div>`).join('');
  const snow = (sc.snow === true || (sc.snow !== false && ['snow', 'skyline', 'streetcar', 'trail'].includes(sc.bg))) ? snowDots(t) : '';
  const st = sceneStage(sc);
  const props = (sc.props || []).map((p, i) => propHtml(p, lt, sc.id, i, (sc.props || []).length, st));
  return `<div style="position:absolute;inset:0;overflow:hidden">${bg}${snow}${props.map(r => r ? r.html : '').join('')}` +
    `${headlineHtml(sc, lt, dur, st.hy)}${cardHtml(sc, lt, dur, st.cy)}</div>`;
}

// ---------------------------------------------------------------- transitions: whole composites move, constant speed, no frozen frame
function transitionHtml(t, tl, i) {
  const S = tl.scenes, sc = S[i], lt = t - sc.start, TD = sc.transitionDur || 0.42;
  if (i === 0 || lt >= TD || lt < 0) return null;
  const x = clamp(lt / TD, 0, 1), prev = S[i - 1], kind = sc.transition || 'whip';
  const a = sceneComposite(prev, t, tl), b = sceneComposite(sc, t, tl);   // both keep animating during the cut
  if (kind === 'zoom') {
    const za = 1 + x * 1.5, zb = 1.3 - 0.3 * x;
    return `<div style="position:absolute;inset:0;transform:scale(${za.toFixed(3)});opacity:${(1 - x).toFixed(3)};filter:blur(${(x * 9).toFixed(1)}px)">${a}</div>` +
      `<div style="position:absolute;inset:0;transform:scale(${zb.toFixed(3)});opacity:${Math.min(1, x * 1.6).toFixed(3)}">${b}</div>`;
  }
  if (kind === 'membrane') {
    // circle(R%) is relative to the 1080x1920 diagonal/sqrt2 = 1558 px, and 80% already covers the frame from (50%,58%).
    // R = 80*x^0.62 reveals a near-constant slice of area per frame: no 2-frame hard cut, no stall.
    const r = 80 * Math.pow(x, 0.62), wob = 1 + Math.sin(x * 9) * 0.03, rr = (r * wob).toFixed(2);
    return `<div style="position:absolute;inset:0;transform:translateX(${(-14 * x).toFixed(1)}px) scale(${(1 + .05 * x).toFixed(4)})">${a}</div>` +
      `<div style="position:absolute;inset:0;clip-path:circle(${rr}% at 50% 58%)">${b}</div>` +
      `<div style="position:absolute;inset:0;clip-path:circle(${rr}% at 50% 58%);box-shadow:inset 0 0 0 ${(9 * (1 - x) + 3).toFixed(1)}px ${INK},inset 0 0 0 ${(15 * (1 - x) + 6).toFixed(1)}px rgba(127,227,211,.55);pointer-events:none"></div>`;
  }
  if (kind === 'doors') {      // subway doors: panels never rest — they keep sliding and a light sweep crosses them
    const close = clamp(x / 0.52, 0, 1), open = clamp((x - 0.52) / 0.48, 0, 1);
    const w = (W / 2) * (close - open * 0.999) + 2, shown = x < 0.5 ? a : b, sweep = (x * 2200 - 400).toFixed(0);
    const panel = (side) => `<div style="position:absolute;${side}:0;top:0;width:${Math.max(0, w).toFixed(1)}px;height:${H}px;background:linear-gradient(90deg,#b9c6d4,#dfe8f0 55%,#aab8c6);border-${side === 'left' ? 'right' : 'left'}:9px solid ${INK};overflow:hidden">` +
      `<div style="position:absolute;left:14px;right:14px;top:300px;height:620px;background:#2a4a6a;border:9px solid ${INK};border-radius:14px;opacity:.9"></div>` +
      `<div style="position:absolute;left:${sweep}px;top:0;width:180px;height:${H}px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-18deg)"></div></div>`;
    return `${shown}${panel('left')}${panel('right')}`;
  }
  const tr = x * W * 1.06, bl = (Math.sin(x * Math.PI) * 15).toFixed(1);   // whip: linear slide, blur eases to 0 at both ends
  return `<div style="position:absolute;inset:0;transform:translateX(${(-tr).toFixed(1)}px) scale(${(1 - .04 * x).toFixed(4)});filter:blur(${bl}px)">${a}</div>` +
    `<div style="position:absolute;inset:0;transform:translateX(${(W * 1.06 - tr).toFixed(1)}px) scale(${(0.96 + .04 * x).toFixed(4)});filter:blur(${bl}px)">${b}</div>`;
}

function frameHtml(t, tl, chunks, cyto) {
  const S = tl.scenes; let i = S.findIndex(s => t >= s.start && t < s.end); if (i < 0) i = S.length - 1;
  const sc = S[i];
  const body = transitionHtml(t, tl, i) || sceneComposite(sc, t, tl);
  const cy = `<div data-chk="cyto" style="position:absolute;left:${tl.cytoX ?? 16}px;top:${tl.cytoY ?? 1040}px;width:${tl.cytoSize ?? 820}px;height:${tl.cytoSize ?? 820}px">${cyto}</div>`;
  return `<div id="f" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#0a1330">${body}${cy}${captionsHtml(tl, t, chunks)}</div>`;
}
const inTransition = (tl, t) => tl.scenes.some((s, i) => i > 0 && t >= s.start && t < s.start + (s.transitionDur || 0.42));

// ---------------------------------------------------------------- main
module.exports={sceneStage,hlMetrics,cardMetrics};