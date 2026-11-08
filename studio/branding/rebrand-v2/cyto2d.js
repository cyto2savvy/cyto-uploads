const fs=require('fs');
let rs=5; const rnd=()=>(rs=(rs*16807)%2147483647)/2147483647;
const defs=`
<defs>
 <radialGradient id="skin" cx=".36" cy=".3" r=".85"><stop offset="0" stop-color="#7be6d2"/><stop offset=".5" stop-color="#3fc4b0"/><stop offset="1" stop-color="#238f86"/></radialGradient>
 <radialGradient id="skinArm" cx=".4" cy=".3" r=".9"><stop offset="0" stop-color="#4fd0bc"/><stop offset="1" stop-color="#1f8a82"/></radialGradient>
 <linearGradient id="hat" x1="0" x2="1"><stop offset="0" stop-color="#1e4fc0"/><stop offset=".45" stop-color="#2c63d6"/><stop offset="1" stop-color="#142f84"/></linearGradient>
 <radialGradient id="nuc" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#b79cff"/><stop offset=".55" stop-color="#7b4fd0"/><stop offset="1" stop-color="#4b2b94"/></radialGradient>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1330"/><stop offset=".65" stop-color="#1a2d5e"/><stop offset="1" stop-color="#2b4180"/></linearGradient>
 <linearGradient id="cupw" x1="0" x2="1"><stop offset="0" stop-color="#e9e6df"/><stop offset=".35" stop-color="#ffffff"/><stop offset="1" stop-color="#cfcac0"/></linearGradient>
 <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#6ff0dc" stop-opacity=".75"/><stop offset=".55" stop-color="#3a6be0" stop-opacity=".32"/><stop offset="1" stop-color="#1a2d5e" stop-opacity="0"/></radialGradient>
 <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0a0"/><stop offset=".5" stop-color="#ffc83a"/><stop offset="1" stop-color="#d08a10"/></linearGradient>
 <clipPath id="bodyclip2"><ellipse rx="308" ry="292"/></clipPath>
 <filter id="cut" x="-10%" y="-10%" width="130%" height="130%"><feDropShadow dx="7" dy="10" stdDeviation="0" flood-color="#000" flood-opacity=".38"/></filter>
 <filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
 <clipPath id="bodyclip"><circle r="300"/></clipPath>
 <clipPath id="hatclip"><path d="M-288 -150 C-300 -420 300 -420 288 -150Z"/></clipPath>
</defs>`;
const O='stroke="#0a1f24" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"';

function sparkle(x,y,r,c='#fff'){return `<path d="M${x} ${y-r} Q${x+r*.15} ${y-r*.15} ${x+r} ${y} Q${x+r*.15} ${y+r*.15} ${x} ${y+r} Q${x-r*.15} ${y+r*.15} ${x-r} ${y} Q${x-r*.15} ${y-r*.15} ${x} ${y-r}Z" fill="${c}"/>`}
function eye(x,side){ // side -1 left, 1 right
 const id='e'+(side<0?'L':'R');
 return `<g transform="translate(${x},-8)">
 <clipPath id="${id}"><ellipse rx="50" ry="55"/></clipPath>
 <ellipse rx="50" ry="55" fill="#fff"/>
 <g clip-path="url(#${id})">
  <circle cx="5" cy="14" r="25" fill="#0b0b12"/><circle cx="-4" cy="2" r="9" fill="#fff"/><circle cx="14" cy="22" r="4" fill="#fff" opacity=".8"/>
  <path d="M-70 -80 L70 -80 L70 2 Q0 ${-8-side*5} -70 2Z" fill="#2fae9b"/>
  <path d="M-70 0 Q0 ${-10-side*5} 70 0" fill="none" stroke="#0a1f24" stroke-width="8"/>
 </g>
 <ellipse rx="50" ry="55" fill="none" ${O}/>
 <path d="M-56 -66 Q0 ${side<0?-98:-86} 58 ${side<0?-72:-62}" fill="none" stroke="#0a1f24" stroke-width="9" stroke-linecap="round"/>
</g>`}
function cup(){return `<g transform="translate(-362,92) rotate(-9) scale(1.38)" filter="url(#cut)">
 <path d="M-72 -105 L72 -105 L54 108 Q0 122 -54 108Z" fill="url(#cupw)" ${O}/>
 <path d="M-68 -54 L68 -54 L62 36 L-62 36Z" fill="#c62828" ${O}/>
 <path d="M-68 -54 L68 -54 L66 -36 L-66 -36Z" fill="#e24a4a" opacity=".55"/>
 <rect x="-64" y="-12" width="128" height="7" fill="#fff" opacity=".85"/>
 <path d="M-62 -125 L62 -125 L72 -105 L-72 -105Z" fill="#4a2c1f" ${O}/>
 <rect x="-52" y="-146" width="104" height="26" rx="10" fill="#5c3827" ${O}/>
 <path d="M-16 -160 q-16 -18 0 -34 q16 -16 0 -34 M16 -160 q16 -18 0 -34 q-16 -16 0 -34" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".55"/>
 <g transform="translate(0,-10) scale(.8)"><circle r="62" fill="#3fc4b0" ${O}/>
  <path d="M-60 -12 C-60 -78 60 -78 60 -12Z" fill="#2c63d6" ${O}/><rect x="-62" y="-20" width="124" height="14" fill="#fff"/><circle cy="-72" r="12" fill="#fff" stroke="#0a1f24" stroke-width="6"/>
  <ellipse cx="-22" cy="14" rx="10" ry="12" fill="#fff"/><ellipse cx="22" cy="14" rx="10" ry="12" fill="#fff"/><circle cx="-20" cy="17" r="5" fill="#111"/><circle cx="24" cy="17" r="5" fill="#111"/>
  <path d="M-18 40 Q0 52 18 40" fill="none" stroke="#0a1f24" stroke-width="6" stroke-linecap="round"/></g>
 <g ${O} fill="url(#skinArm)"><ellipse cx="-70" cy="62" rx="26" ry="38"/><ellipse cx="-14" cy="64" rx="62" ry="36"/></g>
 <path d="M-58 -96 L-52 90" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".6"/>
</g>`}

function chain(){ // necklace wrapping around the body, pendant hanging at centre
 const P0=[-300,128],C=[0,300],P1=[300,128]; let links='';
 const N=40;
 const link=(x,y,ang,i)=>{const rot=ang+(i%2?90:0), rx=i%2?8.5:14, ry=i%2?14:9;
  return `<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="${rx}" ry="${ry}" transform="rotate(${rot.toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})" fill="url(#gold)" stroke="#6b4100" stroke-width="3.5"/>`+(i%2===0?`<circle cx="${(x-3).toFixed(1)}" cy="${(y-3).toFixed(1)}" r="2.4" fill="#fffbe0" opacity=".9"/>`:'')};
 for(let i=0;i<=N;i++){const t=i/N; const x=(1-t)*(1-t)*P0[0]+2*(1-t)*t*C[0]+t*t*P1[0]; const y=(1-t)*(1-t)*P0[1]+2*(1-t)*t*C[1]+t*t*P1[1];
  const dx=2*(1-t)*(C[0]-P0[0])+2*t*(P1[0]-C[0]), dy=2*(1-t)*(C[1]-P0[1])+2*t*(P1[1]-C[1]); links+=link(x,y,Math.atan2(dy,dx)*180/Math.PI,i)}
 let drop=''; for(let k=0;k<3;k++) drop+=link(0,222+k*13,90,k+1);
 let gems=''; for(let i=0;i<12;i++){const a=i/12*6.283; gems+=`<circle cx="${(Math.cos(a)*40).toFixed(1)}" cy="${(Math.sin(a)*40).toFixed(1)}" r="4" fill="#e8fbff" stroke="#6b4100" stroke-width="1.6"/>`}
 return `<g clip-path="url(#bodyclip2)"><path d="M-300 128 Q0 300 300 128" fill="none" stroke="#0a1f24" stroke-width="22" stroke-linecap="round" opacity=".3" transform="translate(4 9)"/>${links}</g>
 ${drop}
 <g transform="translate(0,298)"><ellipse cx="0" cy="-48" rx="10" ry="13" fill="none" stroke="#6b4100" stroke-width="6"/><ellipse cx="0" cy="-48" rx="10" ry="13" fill="none" stroke="#ffd95a" stroke-width="2.5"/>
  <circle r="50" fill="url(#gold)" ${O}/><circle r="41" fill="none" stroke="#fff3b0" stroke-width="3"/>${gems}
  <text y="17" text-anchor="middle" font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900" font-size="46" fill="#7a4a00" stroke="#fff3b0" stroke-width="1.5" paint-order="stroke">6</text>
  <path d="M-30 -26 Q-14 -40 4 -36" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".8"/></g>
 ${sparkle(34,262,14,'#fff')}`}
function arm(d,w=42){return `<path d="${d}" fill="none" stroke="#0a1f24" stroke-width="${w+14}" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="#2fb5a1" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="#4fd8c3" stroke-width="${w*0.45}" stroke-linecap="round" stroke-linejoin="round" opacity=".55" transform="translate(-4 -5)"/>`}
function garment(fit){
 if(fit==='none') return '';
 const hem='M-330 104 Q0 236 330 104 L330 340 L-330 340Z';
 let g=`<g clip-path="url(#bodyclip2)">`;
 if(fit==='jersey'){
  g+=`<path d="${hem}" fill="#1f4fc0"/><path d="M-330 214 Q0 292 330 214 L330 236 Q0 314 -330 236Z" fill="#fff"/><path d="M-330 252 Q0 330 330 252 L330 270 Q0 348 -330 270Z" fill="#fff"/>
   <path d="M-330 104 Q0 236 330 104" fill="none" stroke="#fff" stroke-width="12"/><path d="M-330 104 Q0 236 330 104" fill="none" stroke="#0a1f24" stroke-width="7" transform="translate(0 -9)" opacity=".0"/>
   <text x="0" y="248" text-anchor="middle" transform="scale(1,.92)" font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900" font-size="54" fill="#fff" stroke="#0e2468" stroke-width="5" paint-order="stroke" opacity="0">6IX</text>
   <path d="M-330 104 Q0 236 330 104 L330 340 L-330 340Z" fill="none" stroke="#0a1f24" stroke-width="7"/>`;
 } else if(fit==='hoodie'){
  g+=`<path d="${hem}" fill="#2a2d36"/><path d="M-330 104 Q0 236 330 104" fill="none" stroke="#3b3f4b" stroke-width="16"/>
   <path d="M-130 206 Q0 262 130 206 L156 306 Q0 338 -156 306Z" fill="#23262e" stroke="#0a1f24" stroke-width="5"/>
   <path d="M-34 170 L-40 222" stroke="#f4f1e8" stroke-width="7" stroke-linecap="round"/><path d="M34 170 L40 222" stroke="#f4f1e8" stroke-width="7" stroke-linecap="round"/>
   <circle cx="-40" cy="230" r="6" fill="#f4f1e8"/><circle cx="40" cy="230" r="6" fill="#f4f1e8"/>
   <path d="M-330 296 Q0 390 330 296 L330 340 L-330 340Z" fill="#171920"/>
   <path d="M-330 104 Q0 236 330 104 L330 340 L-330 340Z" fill="none" stroke="#0a1f24" stroke-width="7"/>`;
 } else if(fit==='puffer'){
  g+=`<path d="${hem}" fill="#f0a722"/>`;
  for(const y of [150,196,242]) g+=`<path d="M-330 ${y} Q0 ${y+88} 330 ${y}" fill="none" stroke="#b86d0a" stroke-width="7"/>`;
  g+=`<path d="M-330 104 Q0 236 330 104" fill="none" stroke="#ffd36a" stroke-width="12"/><path d="M0 170 L0 340" stroke="#b86d0a" stroke-width="7"/><path d="M-330 104 Q0 236 330 104 L330 340 L-330 340Z" fill="none" stroke="#0a1f24" stroke-width="7"/>
   <path d="M-210 215 Q-130 235 -60 222" fill="none" stroke="#ffe39a" stroke-width="8" stroke-linecap="round" opacity=".6"/>`;
 }
 return g+`</g>`}
function cyto(fit='none'){
 let spots=''; for(let i=0;i<22;i++){const a=rnd()*6.28,r=Math.sqrt(rnd())*260;const x=Math.cos(a)*r,y=Math.sin(a)*r*0.95+20;
  if(Math.abs(x)<190&&y>-100&&y<30) continue; if(Math.abs(x)<130&&y>40&&y<170) continue; if(y<-60) continue; if(x>100&&y>80) continue;if(x<-110&&y>70&&x>-270) continue; if(y>130) continue;
  spots+=`<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(3+rnd()*5).toFixed(1)}" fill="#25a090" opacity=".55"/>`}
 let ribs=''; for(let i=-10;i<=10;i++) ribs+=`<path d="M${i*28} -140 L${i*32} -400" stroke="#102a74" stroke-width="5" opacity=".45"/>`;
 let cuffr=''; for(let i=-9;i<=9;i++) cuffr+=`<path d="M${i*32} -176 L${i*32} -82" stroke="#0e2468" stroke-width="5" opacity=".55"/>`;
 let pom=''; for(let i=0;i<24;i++){const a=rnd()*6.28,r=rnd()*34;pom+=`<circle cx="${(Math.cos(a)*r).toFixed(0)}" cy="${(Math.sin(a)*r).toFixed(0)}" r="5" fill="#dcd5c4"/>`}
 const hand=(x,y)=>`<g transform="translate(${x},${y})"><circle r="52" fill="#2fb5a1" ${O}/><circle r="52" fill="url(#skinArm)" opacity=".7"/><ellipse cx="-16" cy="-20" rx="16" ry="10" fill="#fff" opacity=".4" transform="rotate(-30 -16 -20)"/></g>`;
 return `<g filter="url(#cut)">
 <ellipse cx="10" cy="338" rx="230" ry="24" fill="#000" opacity=".3" filter="url(#soft)"/>
 <!-- arms emerge from behind the body edge -->
 ${arm("M268 60 Q372 70 366 -34",44)}${hand(366,-62)}
 ${arm("M-268 82 Q-318 112 -322 164",44)}
 <!-- body -->
 <ellipse rx="308" ry="292" fill="#3fd0bb" ${O}/>
 <g clip-path="url(#bodyclip2)">
  <ellipse cx="86" cy="76" rx="300" ry="285" fill="#2aa896"/>
  <ellipse cx="-10" cy="-8" rx="296" ry="282" fill="#3fd0bb"/>
  <path d="M-250 -150 Q-170 -250 -40 -250" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" opacity=".38"/>
  <circle cx="-218" cy="-95" r="13" fill="#fff" opacity=".4"/>
  <path d="M300 -60 Q330 60 250 200" fill="none" stroke="#9dfbe9" stroke-width="12" stroke-linecap="round" opacity=".55"/>
  ${spots}
  ${organelles()}
 </g>
 ${garment(fit)}
 <ellipse rx="308" ry="292" fill="none" ${O}/>
 ${eye(-100,-1)}${eye(100,1)}
 <ellipse cx="-196" cy="70" rx="30" ry="18" fill="#ff9aa8" opacity=".55"/><ellipse cx="196" cy="70" rx="30" ry="18" fill="#ff9aa8" opacity=".55"/>
 <path d="M-62 112 Q0 138 84 92" fill="none" stroke="#0a1f24" stroke-width="11" stroke-linecap="round"/>
 <path d="M84 92 Q100 82 106 98" fill="none" stroke="#0a1f24" stroke-width="8" stroke-linecap="round"/>
 <path d="M-40 126 Q10 146 60 118" fill="none" stroke="#1f8f86" stroke-width="7" stroke-linecap="round" opacity=".55"/>
 <g transform="translate(-176,124) rotate(-12)"><rect x="-56" y="-22" width="112" height="44" rx="22" fill="#ff9b3d" ${O}/><rect x="-52" y="-18" width="104" height="14" rx="7" fill="#ffc07a" opacity=".8"/><path d="M-34 8 L-20 -6 L-6 8 L8 -6 L22 8 L34 -4" fill="none" stroke="#c4541a" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>
 ${chain()}
 <g transform="rotate(-7 0 -150)">
  <path d="M-292 -150 C-312 -410 312 -410 292 -150Z" fill="url(#hat)" ${O}/>
  <g clip-path="url(#hatclip)">${ribs}<ellipse cx="-150" cy="-300" rx="70" ry="90" fill="#fff" opacity=".13" transform="rotate(20 -150 -290)"/></g>
  <rect x="-304" y="-176" width="608" height="98" rx="42" fill="#142f84" ${O}/>
  ${cuffr}
  <rect x="-300" y="-140" width="600" height="24" fill="#fff"/>
  <path d="M-296 -172 Q0 -196 296 -172" fill="none" stroke="#3a78ec" stroke-width="10" opacity=".6" stroke-linecap="round"/>
  <g transform="translate(0,-128)"><circle r="30" fill="url(#gold)" stroke="#0a1f24" stroke-width="6"/><text y="14" text-anchor="middle" font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900" font-size="38" fill="#7a4a00">6</text></g>
  <g transform="translate(0,-404)"><circle r="56" fill="#f6f3ea" ${O}/>${pom}</g>
 </g>
 ${sparkle(-300,-240,30)}${sparkle(330,-210,24,'#ffe27a')}${sparkle(300,260,20)}${sparkle(-380,-60,18,'#ffe27a')}
 </g>${cup()}`}


const ANIM=process.env.ANIM==='1';
let _os=+(process.env.SEED||Date.now()%100000)+1;
const orand=()=>(_os=(_os*16807)%2147483647)/2147483647;
const OJ=(amt)=>(orand()-0.5)*2*amt;   // random out-of-place jitter
let _ai=0;
function wob(inner,dx,dy,rot=0){ // drift animation (SMIL), loops every 8s
 if(!ANIM) return inner;
 const d=[4,8,8,4][_ai++%4], ph=(orand()*d).toFixed(2);
 return `<g>${inner}<animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;${dx} ${dy};${(-dx*.6).toFixed(1)} ${(dy*.8).toFixed(1)};0 0" keyTimes="0;.33;.66;1" dur="${d}s" begin="-${ph}s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/>${rot?`<animateTransform attributeName="transform" type="rotate" additive="sum" values="0;${rot};${-rot};0" dur="${d}s" begin="-${ph}s" repeatCount="indefinite"/>`:''}</g>`}
function organelles(){ // all drawn inside the cell body clip; nothing can extend outside the cell
 const T='stroke="#0a1f24" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"';
 let o='';
 // nucleus
 o+=wob(`<g transform="translate(${205+OJ(12)},${128+OJ(10)}) rotate(${OJ(20)})"><circle r="54" fill="url(#nuc)" ${T}/><circle r="54" fill="none" stroke="#d8c8ff" stroke-width="3" stroke-dasharray="3 9" opacity=".7" transform="scale(.82)"/><circle cx="8" cy="6" r="16" fill="#4b2b94" stroke="#0a1f24" stroke-width="4"/><circle cx="-20" cy="-22" r="11" fill="#efe6ff"/></g>`,9,-7);
 // mitochondria
 const mito=(x,y,r,sc=1)=>wob(`<g transform="translate(${x+OJ(14)},${y+OJ(10)}) rotate(${r+OJ(28)}) scale(${sc})"><rect x="-46" y="-22" width="92" height="44" rx="22" fill="#ffa93a" ${T}/><rect x="-40" y="-16" width="80" height="14" rx="7" fill="#ffd089" opacity=".7"/><path d="M-30 14 L-22 -8 L-14 14 L-6 -8 L2 14 L10 -8 L18 14 L26 -8 L32 8" fill="none" stroke="#c4541a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>`,12,6,4);
 o+=mito(-84,248,-8,.78)+mito(236,-62,62,.72);
 // golgi stack
 o+=wob(`<g transform="translate(${96+OJ(12)},${252+OJ(8)}) rotate(${-8+OJ(14)})">${[0,1,2,3].map(i=>`<path d="M${-44+i*3} ${-24+i*14} Q0 ${-38+i*14} ${44-i*3} ${-24+i*14}" fill="none" stroke="#0a1f24" stroke-width="14" stroke-linecap="round"/><path d="M${-44+i*3} ${-24+i*14} Q0 ${-38+i*14} ${44-i*3} ${-24+i*14}" fill="none" stroke="${['#ff9ac0','#ff7fae','#f56a9d','#e85a8e'][i]}" stroke-width="8" stroke-linecap="round"/>`).join('')}<circle cx="58" cy="-26" r="8" fill="#ffd0e2" ${T}/><circle cx="-56" cy="26" r="7" fill="#ffd0e2" ${T}/></g>`,-8,-5,3);
 // rough ER
 o+=wob(`<g transform="translate(${-246+OJ(8)},${-6+OJ(18)})"><path d="M0 -70 Q-26 -50 0 -32 Q26 -14 0 4 Q-26 22 0 40 Q22 54 0 70" fill="none" stroke="#0a1f24" stroke-width="17" stroke-linecap="round"/><path d="M0 -70 Q-26 -50 0 -32 Q26 -14 0 4 Q-26 22 0 40 Q22 54 0 70" fill="none" stroke="#9be7f2" stroke-width="10" stroke-linecap="round"/>${[[-14,-52],[14,-20],[-14,12],[10,50],[-6,-34],[8,-2]].map(p=>`<circle cx="${p[0]}" cy="${p[1]}" r="4.5" fill="#3b2a66" stroke="#0a1f24" stroke-width="1.5"/>`).join('')}</g>`,5,10);
 // lysosomes / vesicles
 const lys=(x,y,r,c)=>wob(`<g transform="translate(${x+OJ(16)},${y+OJ(14)})"><circle r="${r}" fill="${c}" ${T}/><circle cx="${-r*.3}" cy="${-r*.3}" r="${r*.28}" fill="#fff" opacity=".7"/><circle cx="${r*.25}" cy="${r*.2}" r="${r*.16}" fill="#0a1f24" opacity=".35"/></g>`,10,-9);
 o+=lys(-30,236,17,'#c8f06a')+lys(236,40,15,'#c8f06a')+lys(-262,92,13,'#ffe27a')+lys(-212,-92,12,'#c8f06a');
 // ribosome dots
 for(let i=0;i<14;i++){const a=orand()*6.28,rad=60+orand()*220,x=Math.cos(a)*rad,y=Math.sin(a)*rad*0.9+30; if(y<-60||Math.abs(x)<150&&y>-70&&y<150) continue; o+=wob(`<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="4.5" fill="#3b2a66" opacity=".8"/>`,8,8)}
 return o}
function skyline(w,h,base,seed){let s=seed;const r=()=>(s=(s*16807)%2147483647)/2147483647;let o='';
 o+=`<rect width="${w}" height="${h}" fill="url(#sky)"/>`;
 for(let i=0;i<130;i++) o+=`<circle cx="${(r()*w).toFixed(0)}" cy="${(r()*base*0.7).toFixed(0)}" r="${(r()*2.2+.6).toFixed(1)}" fill="#fff" opacity="${(.3+r()*.6).toFixed(2)}"/>`;
 
 for(let layer=0;layer<2;layer++){let x=-20;while(x<w){const bw=w*(0.04+r()*0.05),bh=h*(0.1+r()*0.25)*(layer?.7:1);
  o+=`<rect x="${x.toFixed(0)}" y="${(base-bh).toFixed(0)}" width="${bw.toFixed(0)}" height="${(h-base+bh).toFixed(0)}" fill="${layer?'#17275a':'#0e1a3e'}"/>`;
  for(let wy=base-bh+16;wy<base;wy+=24)for(let wx=x+8;wx<x+bw-8;wx+=20)if(r()>.6)o+=`<rect x="${wx.toFixed(0)}" y="${wy.toFixed(0)}" width="7" height="10" fill="#ffd27a" opacity=".8"/>`;
  x+=bw+2}}
 return o}
function tower_old(x,base,h){return `<path d="M${x-9} ${base} L${x-3} ${base-h*0.86} L${x+3} ${base-h*0.86} L${x+9} ${base}Z" fill="#0a1230"/><ellipse cx="${x}" cy="${base-h*0.62}" rx="${h*0.07}" ry="${h*0.022}" fill="#0a1230"/><path d="M${x} ${base-h*0.86} L${x} ${base-h}" stroke="#0a1230" stroke-width="3"/><circle cx="${x}" cy="${base-h}" r="3" fill="#ff4a4a"/>`}

function tower(x,base,h){return `<path d="M${x-12} ${base} L${x-4} ${base-h*0.62} L${x+4} ${base-h*0.62} L${x+12} ${base}Z" fill="#0a1230"/>
 <path d="M${x-4} ${base-h*0.62} L${x-2} ${base-h*0.95} L${x+2} ${base-h*0.95} L${x+4} ${base-h*0.62}Z" fill="#0a1230"/>
 <ellipse cx="${x}" cy="${base-h*0.6}" rx="${h*0.085}" ry="${h*0.026}" fill="#0a1230"/><ellipse cx="${x}" cy="${base-h*0.628}" rx="${h*0.06}" ry="${h*0.02}" fill="#16254f"/>
 <ellipse cx="${x}" cy="${base-h*0.74}" rx="${h*0.026}" ry="${h*0.016}" fill="#0a1230"/>
 <path d="M${x} ${base-h*0.95} L${x} ${base-h}" stroke="#0a1230" stroke-width="3"/><circle cx="${x}" cy="${base-h}" r="3.5" fill="#ff4a4a"/>
 <ellipse cx="${x}" cy="${base-h*0.6}" rx="${h*0.12}" ry="${h*0.06}" fill="#ffcf5a" opacity=".05" filter="url(#soft)"/>`}
function extras(w,h,base,withCar,snowSeed){let s=snowSeed;const r=()=>(s=(s*16807)%2147483647)/2147483647;let o='';
 // horizon glow
 o+=`<rect y="${base-h*0.18}" width="${w}" height="${h*0.18}" fill="#ff7a59" opacity=".10"/>`;
 // stadium dome
 const dx=w*(withCar?0.55:0.2), dr=w*(withCar?0.075:0.09);
 o+=`<path d="M${dx-dr} ${base} Q${dx} ${base-dr*1.3} ${dx+dr} ${base}Z" fill="#1b2d66"/><path d="M${dx-dr*.5} ${base} Q${dx} ${base-dr*1.2} ${dx+dr*.5} ${base}" fill="none" stroke="#2b4590" stroke-width="3"/>`;
 // lake
 o+=`<rect y="${base}" width="${w}" height="${h-base}" fill="#0d1a40"/>`;
 for(let i=0;i<46;i++){const x=r()*w,y=base+6+r()*(h-base-12),l=8+r()*40;o+=`<rect x="${x.toFixed(0)}" y="${y.toFixed(0)}" width="${l.toFixed(0)}" height="2.5" rx="1.2" fill="${r()>.5?'#ffd27a':'#7fb0ff'}" opacity="${(.12+r()*.28).toFixed(2)}"/>`}
 if(withCar){const cx=w*0.74,cy=base-h*0.012,cw=w*0.17,ch=h*0.085;
  o+=`<g><rect x="${cx}" y="${cy-ch}" width="${cw}" height="${ch}" rx="10" fill="#c62828" stroke="#0a1f24" stroke-width="5"/><rect x="${cx}" y="${cy-ch*0.42}" width="${cw}" height="${ch*0.1}" fill="#fff"/>`;
  for(let i=0;i<5;i++) o+=`<rect x="${cx+cw*0.06+i*cw*0.18}" y="${cy-ch*0.85}" width="${cw*0.13}" height="${ch*0.32}" rx="4" fill="#ffe9a8"/>`;
  o+=`<path d="M${cx+cw*0.5} ${cy-ch} L${cx+cw*0.42} ${cy-ch*1.35} L${cx+cw*0.6} ${cy-ch*1.35}" stroke="#0a1f24" stroke-width="4" fill="none"/><path d="M${cx-40} ${cy-ch*1.42} H${cx+cw+60}" stroke="#0a1f24" stroke-width="3"/><circle cx="${cx+cw*0.2}" cy="${cy+4}" r="9" fill="#0a1f24"/><circle cx="${cx+cw*0.8}" cy="${cy+4}" r="9" fill="#0a1f24"/></g>`}
 // snow
 for(let i=0;i<90;i++) o+=`<circle cx="${(r()*w).toFixed(0)}" cy="${(r()*h).toFixed(0)}" r="${(1.6+r()*3.4).toFixed(1)}" fill="#fff" opacity="${(.35+r()*.5).toFixed(2)}"/>`;
 return o}
// PFP 1000x1000
const pfp=`<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">${defs}
 <clipPath id="circ"><circle cx="500" cy="500" r="486"/></clipPath>
 <g clip-path="url(#circ)">${skyline(1000,1000,780,3)}${extras(1000,1000,780,false,17)}${tower(850,780,700)}
 <circle cx="520" cy="500" r="470" fill="url(#glow)"/><g transform="translate(512,505) scale(.86)">${cyto(process.env.FIT||'none')}</g></g>
 <circle cx="500" cy="500" r="486" fill="none" stroke="#ffcf5a" stroke-width="28"/></svg>`;
fs.writeFileSync('pfp.svg',pfp);
// COVER 1640x624 (FB) — character left-center, text right, safe middle
const cover=(w,h,sc,cx,cy,tx,fs1,fs2,ty=h*0.4)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${defs}
 ${skyline(w,h,h*0.8,9)}${extras(w,h,h*0.8,true,23)}${tower(w*0.93,h*0.8,h*0.98)}
 <circle cx="${cx}" cy="${cy-40}" r="${h*0.62}" fill="url(#glow)"/><g transform="translate(${cx},${cy}) scale(${sc})">${cyto(process.env.FIT||'none')}</g>
 <g font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900">
  <text x="${tx}" y="${ty}" font-size="${fs1}" fill="#fff" stroke="#0a1f24" stroke-width="${fs1*0.08}" paint-order="stroke" filter="url(#cut)">THE BODY</text>
  <text x="${tx}" y="${ty+fs1*0.98}" font-size="${fs1}" fill="#ffcf5a" stroke="#0a1f24" stroke-width="${fs1*0.08}" paint-order="stroke" filter="url(#cut)">IS THE 6IX</text>
  <text x="${tx+4}" y="${ty+fs1*0.98+fs2*1.9}" font-size="${fs2}" fill="#8fe8d8" font-weight="700">Science in 30 seconds · live from inside your body</text>
 </g></svg>`;
fs.writeFileSync('cover.svg',cover(1640,624,.5,430,365,720,104,26));
fs.writeFileSync('banner.svg',cover(2560,1440,.41,905,745,1105,84,27,640)  /* YT safe area x662-1897 y551-889 */);


// OUTFIT SHEET
const fits=[['none','BASE'],['jersey','HOCKEY JERSEY'],['hoodie','BLACK HOODIE'],['puffer','PUFFER']];
const sheet=`<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1100" viewBox="0 0 2400 1100">${defs}
 <rect width="2400" height="1100" fill="url(#sky)"/>
 ${fits.map((f,i)=>`<g transform="translate(${i*600},0)"><circle cx="300" cy="520" r="290" fill="url(#glow)"/><g transform="translate(300,560) scale(.5)">${cyto(f[0])}</g>
  <text x="300" y="1010" text-anchor="middle" font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900" font-size="44" fill="#ffcf5a" stroke="#0a1f24" stroke-width="6" paint-order="stroke">${f[1]}</text></g>`).join('')}
</svg>`;
fs.writeFileSync('fits.svg',sheet);

if(ANIM){ fs.writeFileSync('pfp_anim.svg', pfp); }
