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
function mouthAt(tl,t,rest){
 for(const w of tl.words||[]) if(t>=w.start&&t<=w.end){const k=Math.floor((t-w.start)/.085);return ['small','wide','o','small','wide','small'][k%6];}
 return rest;
}
function state(t,tl){
 const sc=tl._sched||(tl._sched=schedule(tl)), b=beatAt(tl,t)||{emotion:'chill'}, E=EMO[b.emotion]||EMO.chill;
 // gaze
 let gx=0,gy=0; const s=[...sc.sacc].reverse().find(k=>k.t<=t)||sc.sacc[0]; const prev=sc.sacc[Math.max(0,sc.sacc.indexOf(s)-1)]||s;
 const a=ease(clamp((t-s.t)/.12,0,1)); gx=prev.x+(s.x-prev.x)*a; gy=prev.y+(s.y-prev.y)*a;
 const tg=b.gaze||E.gaze; if(tg&&t-b.t<2.2){gx=tg[0];gy=tg[1];}   // beats can pin the gaze (reaction)
 // blink (110 ms down, 110 ms up)
 let blink=0; for(const bt of sc.blinks){const d=t-bt; if(d>=0&&d<.22) blink=d<.11?d/.11:1-(d-.11)/.11;}
 // brow pops on reaction onset
 const since=t-(b.t||0); const pop=since<.25?Math.sin(since/.25*Math.PI)*.5:0;
 return {expr:E.expr,gx,gy,blink,brow:E.brow+pop,mouth:mouthAt(tl,t,E.rest),
  tilt:E.tilt+Math.sin(t*2*Math.PI*.45)*1.4, bob:Math.sin(t*2*Math.PI*.9)*6,
  cupDy:Math.sin(t*2*Math.PI*.7+1)*5, cupRot:Math.sin(t*2*Math.PI*.55)*2.5};
}
function frameSvg(t,tl,size=1080){
 const st=state(t,tl); C.setExpr(st.expr); C.reset();
 Object.assign(G,{gx:st.gx,gy:st.gy,blink:st.blink,brow:st.brow,mouth:st.mouth,cupDy:st.cupDy,cupRot:st.cupRot,steam:true});
 const body=cyto(tl.fit||'none');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="-550 -550 1100 1100">${defs}<g transform="translate(0,${st.bob.toFixed(1)}) rotate(${st.tilt.toFixed(2)})">${body}</g></svg>`;
}
module.exports={state,frameSvg,EMO};
