// CANON v2 VIDEO RIG — drives Cyto (branding/rebrand-v2/cyto2d.js) frame by frame: gaze wander, blinks, brows, reactions,
// per-syllable mouth, head tilt/bounce, cup held + swaying with rising steam, organelle drift.  state(t, tl) is pure & testable.
const path=require('path');
const C=require(path.join(__dirname,'..','branding','rebrand-v2','cyto2d.js'));
const {cyto,defs,G}=C;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), ease=x=>x*x*(3-2*x);
function rng(seed){let s=seed%2147483647||1;return()=>(s=(s*16807)%2147483647)/2147483647;}
// emotion table: base face (EXPR), brow lift, resting mouth (null = canon), tilt degrees, default gaze
const EMO={
 chill:{expr:'chill',brow:0,rest:null,tilt:0},
 happy:{expr:'chill',brow:.5,rest:'smile',tilt:3},
 shock:{expr:'shock',brow:1,rest:null,tilt:-2},
 think:{expr:'chill',brow:.6,rest:'closed',tilt:7,gaze:[-.8,-.6]},
 solemn:{expr:'solemn',brow:-.3,rest:null,tilt:0},
 laugh:{expr:'chill',brow:.8,rest:'smile',tilt:-6},
};
function schedule(tl){ // deterministic blink + gaze-saccade schedule
 const r=rng(tl.seed||7), blinks=[], sacc=[]; let t=r()*1.5+.6;
 while(t<tl.duration){blinks.push(t);t+=2+r()*2;}                 // blink every 2-4 s
 t=.5; while(t<tl.duration){const cam=r()<.4; sacc.push({t,x:cam?0:(r()*2-1)*.9,y:cam?0:(r()*2-1)*.5});t+=1.1+r()*1.5;} // look around, back to camera 40%
 return {blinks,sacc};
}
function beatAt(tl,t){let b=null;for(const k of tl.beats||[])if(k.t<=t)b=k;return b;}
function beatPair(tl,t){let p=null,b=null;for(const k of tl.beats||[]){if(k.t<=t){p=b;b=k;}}return [p,b];}
function mouthAt(tl,t,rest){
 for(const w of tl.words||[]) if(t>=w.start&&t<=w.end){const k=Math.floor((t-w.start)/.085);return ['small','wide','o','small','wide','small'][k%6];}
 return rest;
}
function state(t,tl){
 // HARD_RULES 22 (loop): over the last 0.5 s the pose eases back to the pose of frame 0, so the last frame equals the first.
 if(tl.loop&&!tl._noLoop){const L=.5,D=tl.duration,f=1/(tl.fps||30),w=ease(clamp((t-(D-L))/(L-f-1e-6),0,1));
  if(w>0){const tl0=Object.assign({},tl,{_noLoop:true}); tl0._sched=tl._sched0||(tl._sched0=schedule(tl)); const a=state(t,tl0),z=state(0,tl0),o={};
   for(const k of ['gx','gy','blink','brow','tilt','bob','cupDy','cupRot']) o[k]=a[k]+(z[k]-a[k])*w;
   o.expr=w<.5?a.expr:z.expr; o.mouth=w<.5?a.mouth:z.mouth; return o;}}
 // rule 22b: with a loop, the idle bounce / sway / cup sway fade in over the first 0.6 s, so frame 0 is a true neutral pose (zero offset, zero speed)
 // and the restart does not jerk. (The tail above eases the pose back to exactly this.)
 const sc=tl._sched||(tl._sched=schedule(tl)); const [bp,b0]=beatPair(tl,t); const b=b0||{emotion:'chill',t:0};
 const E=EMO[b.emotion]||EMO.chill, Ep=EMO[(bp||{}).emotion]||E;
 // pose BLENDS across a beat (0.28 s): tilt used to snap up to 9 deg in one frame, which read as a pop at every cut
 const u=ease(clamp((t-(b.t||0))/.28,0,1)), lerp=(a,c)=>a+(c-a)*u;
 // gaze
 let gx=0,gy=0; const s=[...sc.sacc].reverse().find(k=>k.t<=t)||sc.sacc[0]; const prev=sc.sacc[Math.max(0,sc.sacc.indexOf(s)-1)]||s;
 const a=ease(clamp((t-s.t)/.12,0,1)); gx=prev.x+(s.x-prev.x)*a; gy=prev.y+(s.y-prev.y)*a;
 // beats pin the gaze (reaction): eased in over .28 s and eased back OUT over the last .4 s - releasing it
 // instantly at 2.2 s snapped the eyes, which landed as a pose jump whenever a cut sat near that moment
 // Gaze pins hand over between beats. Dropping the old beat's pin the instant a pin-less beat starts snapped the eyes,
 // so the outgoing pin is released on the same eased weight that fades the new pose in.
 const pinOf=bb=>{if(!bb)return null; const g=bb.gaze||(EMO[bb.emotion]||{}).gaze; if(!g)return null;
  const a2=t-(bb.t||0); return {g,w:ease(clamp(a2/.34,0,1))*ease(clamp((2.2-a2)/.5,0,1))};};
 const pPin=pinOf(bp), cPin=pinOf(b0);
 if(pPin){const w=pPin.w*(1-u); gx+=(pPin.g[0]-gx)*w; gy+=(pPin.g[1]-gy)*w;}
 if(cPin){const w=cPin.w*u;     gx+=(cPin.g[0]-gx)*w; gy+=(cPin.g[1]-gy)*w;}
 // blink (110 ms down, 110 ms up)
 let blink=0; for(const bt of sc.blinks){const d=t-bt; if(d>=0&&d<.22) blink=d<.11?d/.11:1-(d-.11)/.11;}
 // brow pops on reaction onset
 const since=t-(b.t||0); const pop=since<.25?Math.pow(Math.sin(since/.25*Math.PI),2)*.5:0;
 return {expr:u<.5?Ep.expr:E.expr,gx,gy,blink,brow:lerp(Ep.brow,E.brow)+pop,mouth:mouthAt(tl,t,u<.5?Ep.rest:E.rest),
  tilt:lerp(Ep.tilt,E.tilt)+Math.sin(t*2*Math.PI*.45)*1.4*(tl.loop?ease(clamp(t/.6,0,1)):1), bob:Math.sin(t*2*Math.PI*.9)*6*(tl.loop?ease(clamp(t/.6,0,1)):1),
  cupDy:Math.sin(t*2*Math.PI*.7+1)*5*(tl.loop?ease(clamp(t/.6,0,1)):1), cupRot:Math.sin(t*2*Math.PI*.55)*2.5*(tl.loop?ease(clamp(t/.6,0,1)):1)};
}
// SMIL clock for Cyto's own animations (steam, 2.4 s loop). With tl.loop it is warped over the last second so the steam is back at phase 0 on the last frame.
function smilTime(t,tl){ if(!tl.loop) return t; const D=tl.duration,f=1/(tl.fps||30),P=2.4,end=Math.round((D-f)/P)*P,a=D-1;
 if(t<=a) return t; const u=clamp((t-a)/(1-f),0,1); return a+(end-a)*u; }
function frameSvg(t,tl,size=1080){
 const st=state(t,tl); C.setExpr(st.expr); C.reset();
 Object.assign(G,{gx:st.gx,gy:st.gy,blink:st.blink,brow:st.brow,mouth:st.mouth,cupDy:st.cupDy,cupRot:st.cupRot,steam:true});
 const body=cyto(tl.fit||'none');
 // overflow:visible — the held cup + steam reach x -579 / y -570, outside the -550 viewBox (Utsha: "cup clipped"). Geometry is unchanged.
 return `<svg xmlns="http://www.w3.org/2000/svg" data-t="${smilTime(t,tl).toFixed(4)}" width="${size}" height="${size}" viewBox="-550 -550 1100 1100" style="overflow:visible">${defs}<g transform="translate(0,${st.bob.toFixed(1)}) rotate(${st.tilt.toFixed(2)})">${body}</g></svg>`;
}
module.exports={state,frameSvg,smilTime,EMO};
