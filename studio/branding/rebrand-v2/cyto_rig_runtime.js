/* Cyto canon-v2 rig runtime.  CytoRig(rootEl, opts).update(t) poses the rig for time t (seconds).
   Pure function of t -> safe for seek-based renderers (HyperFrames).  One idle loop per part, no stacked yoyos.
   opts.mouth  : [[t,"closed"|"small"|"wide"|"o"], ...] sorted
   opts.blinks : [t, ...]   each blink: close .07s, hold .03s, open .08s
   opts.bob    : {amp:3, period:4}   idle bounce of everything except the set-down cup group
   opts.armR   : {deg:2, period:6.4} slow calm sway of the free arm (around the shoulder)
   opts.closed : [[a,b], ...]  eyes gently closed from a to b (0.2s sine blend in and out)           */
(function(g){
 g.CytoRig=function(root,o){
  o=o||{};
  const q=s=>root.querySelector(s);
  const bob=q('#bob'), armR=q('#armR'), orgs=[...root.querySelectorAll('.org')], lids=[q('#lidL'),q('#lidR')];
  const M={closed:q('#m_closed'),small:q('#m_small'),wide:q('#m_wide'),o:q('#m_o')};
  const mouth=o.mouth||[[0,'closed']], blinks=o.blinks||[], closed=o.closed||[];
  const A=(o.bob&&o.bob.amp!=null)?o.bob.amp:3, P=(o.bob&&o.bob.period)||4;
  const AD=(o.armR&&o.armR.deg!=null)?o.armR.deg:2, AP=(o.armR&&o.armR.period)||6.4;
  function shapeAt(t){let s='closed';for(let i=0;i<mouth.length;i++){if(mouth[i][0]<=t+2e-3)s=mouth[i][1];else break}return s}
  function hold(t){for(const [a,b] of closed){const u=Math.min(1,Math.max(0,(t-a)/0.2)),v=Math.min(1,Math.max(0,(b-t)/0.2));const k=Math.min(u,v);if(k>0)return 0.5-0.5*Math.cos(Math.PI*k)}return 0}
  function lidAt(t){const h=hold(t);if(h>0)return h;for(const b of blinks){const d=t-b;if(d>=0&&d<0.18)return d<0.07?d/0.07:d<0.10?1:1-(d-0.10)/0.08}return 0}
  return {update(t){
    bob.setAttribute('transform',`translate(0 ${(-A*Math.sin(2*Math.PI*t/P)).toFixed(3)})`);
    armR.setAttribute('transform',`rotate(${(AD*Math.sin(2*Math.PI*t/AP)).toFixed(3)} 268 82)`);
    for(const e of orgs){const d=+e.dataset.d,w=2*Math.PI*(t+(+e.dataset.ph))/d;
      e.setAttribute('transform',`translate(${(+e.dataset.dx*Math.sin(w)).toFixed(2)} ${(+e.dataset.dy*Math.sin(w+1.3)).toFixed(2)}) rotate(${(+e.dataset.rot*Math.sin(w)).toFixed(2)})`)}
    const L=(lidAt(t)*64).toFixed(2); for(const l of lids) l.setAttribute('transform',`translate(0 ${L})`);
    const s=shapeAt(t); for(const k in M) M[k].setAttribute('opacity',k===s?1:0);
    return s;
  }};
 };
})(typeof window!=='undefined'?window:globalThis);
