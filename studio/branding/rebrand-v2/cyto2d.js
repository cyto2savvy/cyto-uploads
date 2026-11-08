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
 return `<g transform="translate(${x},-14)">
 <clipPath id="${id}"><ellipse rx="58" ry="64"/></clipPath>
 <ellipse rx="58" ry="64" fill="#fff"/>
 <g clip-path="url(#${id})">
  <circle cx="${side*9}" cy="14" r="31" fill="#0b0b12"/><circle cx="${side*9-11}" cy="1" r="11" fill="#fff"/><circle cx="${side*9+10}" cy="26" r="5" fill="#fff" opacity=".8"/>
  <path d="M-70 -80 L70 -80 L70 -6 Q0 -${14+side*4} -70 -6Z" fill="#2fae9b"/>
  <path d="M-70 -8 Q0 ${-18-side*4} 70 -8" fill="none" stroke="#0a1f24" stroke-width="8"/>
 </g>
 <ellipse rx="58" ry="64" fill="none" ${O}/>
 <path d="M-60 -78 Q0 ${side<0?-112:-96} 62 ${side<0?-84:-72}" fill="none" stroke="#0a1f24" stroke-width="9" stroke-linecap="round"/>
</g>`}
function cup(){return `<g transform="translate(-362,92) rotate(-9) scale(1.38)" filter="url(#cut)">
 <path d="M-72 -105 L72 -105 L54 108 Q0 122 -54 108Z" fill="url(#cupw)" ${O}/>
 <path d="M-68 -54 L68 -54 L62 36 L-62 36Z" fill="#c62828" ${O}/>
 <path d="M-68 -54 L68 -54 L66 -36 L-66 -36Z" fill="#e24a4a" opacity=".55"/>
 <rect x="-64" y="-12" width="128" height="7" fill="#fff" opacity=".85"/>
 <path d="M-62 -125 L62 -125 L72 -105 L-72 -105Z" fill="#4a2c1f" ${O}/>
 <rect x="-52" y="-146" width="104" height="26" rx="10" fill="#5c3827" ${O}/>
 <path d="M-14 -166 Q-30 -190 -14 -210 M14 -166 Q30 -190 14 -214" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".55"/>
 <g transform="translate(0,-10) scale(.8)"><circle r="62" fill="#3fc4b0" ${O}/>
  <path d="M-60 -12 C-60 -78 60 -78 60 -12Z" fill="#2c63d6" ${O}/><rect x="-62" y="-20" width="124" height="14" fill="#fff"/><circle cy="-72" r="12" fill="#fff" stroke="#0a1f24" stroke-width="6"/>
  <ellipse cx="-22" cy="14" rx="10" ry="12" fill="#fff"/><ellipse cx="22" cy="14" rx="10" ry="12" fill="#fff"/><circle cx="-20" cy="17" r="5" fill="#111"/><circle cx="24" cy="17" r="5" fill="#111"/>
  <path d="M-18 40 Q0 52 18 40" fill="none" stroke="#0a1f24" stroke-width="6" stroke-linecap="round"/></g>
 <g ${O} fill="url(#skinArm)"><ellipse cx="-70" cy="62" rx="26" ry="38"/><rect x="-74" y="44" width="112" height="30" rx="15"/><rect x="-72" y="70" width="104" height="30" rx="15"/></g>
 <path d="M-58 -96 L-52 90" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".6"/>
</g>`}
function cyto(){
 let spots=''; for(let i=0;i<22;i++){const a=rnd()*6.28,r=Math.sqrt(rnd())*260;const x=Math.cos(a)*r,y=Math.sin(a)*r*0.95+20;
  if(Math.abs(x)<190&&y>-100&&y<30) continue; if(Math.abs(x)<130&&y>40&&y<170) continue; if(y<-60) continue; if(x>100&&y>80) continue;if(x<-110&&y>70&&x>-270) continue; if(y>150) continue;
  spots+=`<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(3+rnd()*5).toFixed(1)}" fill="#25a090" opacity=".55"/>`}
 let ribs=''; for(let i=-10;i<=10;i++) ribs+=`<path d="M${i*28} -140 L${i*32} -400" stroke="#102a74" stroke-width="5" opacity=".45"/>`;
 let cuffr=''; for(let i=-9;i<=9;i++) cuffr+=`<path d="M${i*32} -176 L${i*32} -82" stroke="#0e2468" stroke-width="5" opacity=".55"/>`;
 let pom=''; for(let i=0;i<24;i++){const a=rnd()*6.28,r=rnd()*34;pom+=`<circle cx="${(Math.cos(a)*r).toFixed(0)}" cy="${(Math.sin(a)*r).toFixed(0)}" r="5" fill="#dcd5c4"/>`}
 return `<g filter="url(#cut)">
 <ellipse cx="10" cy="338" rx="230" ry="24" fill="#000" opacity=".3" filter="url(#soft)"/>
 <!-- raised peace-sign arm (viewer right) -->
 <path d="M236 70 Q330 40 352 -40" fill="none" stroke="#0a1f24" stroke-width="48" stroke-linecap="round"/><path d="M236 70 Q330 40 352 -40" fill="none" stroke="url(#skinArm)" stroke-width="34" stroke-linecap="round"/>
 <g transform="translate(356,-62) rotate(12)"><rect x="-34" y="-112" width="26" height="86" rx="13" fill="url(#skinArm)" ${O}/><rect x="6" y="-112" width="26" height="86" rx="13" fill="url(#skinArm)" ${O} transform="rotate(10 19 -26)"/><circle r="46" fill="url(#skinArm)" ${O}/><rect x="-46" y="-8" width="30" height="46" rx="15" fill="url(#skinArm)" ${O} transform="rotate(-30)"/></g>
 <!-- body -->
 <ellipse rx="308" ry="292" fill="#3fd0bb" ${O}/>
 <g clip-path="url(#bodyclip2)">
  <ellipse cx="60" cy="70" rx="320" ry="300" fill="#2aa896" transform="translate(54 60)" opacity="0"/>
  <path d="M-310 0 A310 295 0 0 0 310 0 Q300 150 150 260 Q-40 330 -200 230 Q-300 150 -310 0Z" fill="#27a593" opacity=".0"/>
  <ellipse cx="86" cy="76" rx="300" ry="285" fill="#2aa896"/>
  <ellipse cx="-10" cy="-8" rx="296" ry="282" fill="#3fd0bb"/>
  <path d="M-250 -150 Q-170 -250 -40 -250" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" opacity=".38"/>
  <circle cx="-218" cy="-95" r="13" fill="#fff" opacity=".4"/>
  <path d="M300 -60 Q330 60 250 200" fill="none" stroke="#9dfbe9" stroke-width="12" stroke-linecap="round" opacity=".55"/>
  ${spots}
 </g>
 <ellipse rx="308" ry="292" fill="none" ${O}/>
 <!-- left arm (to cup) -->
 <path d="M-226 90 Q-282 130 -296 170" fill="none" stroke="#0a1f24" stroke-width="48" stroke-linecap="round"/><path d="M-226 90 Q-282 130 -296 170" fill="none" stroke="url(#skinArm)" stroke-width="34" stroke-linecap="round"/>
 ${eye(-110,-1)}${eye(110,1)}
 <ellipse cx="-196" cy="70" rx="30" ry="18" fill="#ff9aa8" opacity=".55"/><ellipse cx="196" cy="70" rx="30" ry="18" fill="#ff9aa8" opacity=".55"/>
 <!-- smirk -->
 <clipPath id="mo"><path d="M-66 96 Q4 126 82 82 Q80 150 8 160 Q-52 160 -66 96Z"/></clipPath>
 <path d="M-66 96 Q4 126 82 82 Q80 150 8 160 Q-52 160 -66 96Z" fill="#4a0f2b" ${O}/>
 <g clip-path="url(#mo)"><ellipse cx="8" cy="160" rx="46" ry="28" fill="#ff7f95"/><path d="M-60 98 Q4 124 78 84 L78 100 Q4 140 -60 114Z" fill="#fff"/></g>
 <path d="M84 78 Q98 70 104 84" fill="none" stroke="#0a1f24" stroke-width="7" stroke-linecap="round"/>
 <!-- bandage -->
 <g transform="translate(-170,150) rotate(-12)"><rect x="-56" y="-22" width="112" height="44" rx="22" fill="#ff9b3d" ${O}/><rect x="-52" y="-18" width="104" height="14" rx="7" fill="#ffc07a" opacity=".8"/><path d="M-34 8 L-20 -6 L-6 8 L8 -6 L22 8 L34 -4" fill="none" stroke="#c4541a" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>
 <!-- nucleus -->
 <g transform="translate(188,158)"><circle r="68" fill="url(#nuc)" ${O}/><circle cx="-24" cy="-26" r="14" fill="#efe6ff"/><path d="M-26 20 Q-8 36 12 16 Q24 4 36 20" fill="none" stroke="#d8c8ff" stroke-width="7" stroke-linecap="round"/></g>
 <!-- gold chain + 6 pendant -->
 <path d="M-150 214 Q0 330 150 214" fill="none" stroke="#0a1f24" stroke-width="16" stroke-linecap="round"/>
 <path d="M-150 214 Q0 330 150 214" fill="none" stroke="url(#gold)" stroke-width="9" stroke-linecap="round" stroke-dasharray="14 4"/>
 <g transform="translate(0,300)"><circle r="40" fill="url(#gold)" ${O}/><circle r="30" fill="none" stroke="#fff6c8" stroke-width="3" opacity=".8"/><text y="15" text-anchor="middle" font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900" font-size="42" fill="#7a4a00">6</text></g>
 <!-- toque (tilted) -->
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
function skyline(w,h,base,seed){let s=seed;const r=()=>(s=(s*16807)%2147483647)/2147483647;let o='';
 o+=`<rect width="${w}" height="${h}" fill="url(#sky)"/>`;
 for(let i=0;i<130;i++) o+=`<circle cx="${(r()*w).toFixed(0)}" cy="${(r()*base*0.7).toFixed(0)}" r="${(r()*2.2+.6).toFixed(1)}" fill="#fff" opacity="${(.3+r()*.6).toFixed(2)}"/>`;
 if(w>1200) o+=`<circle cx="${w*0.7}" cy="${base*0.13}" r="${Math.min(w,h)*0.05}" fill="#fff6d6" opacity=".9"/>`;
 for(let layer=0;layer<2;layer++){let x=-20;while(x<w){const bw=w*(0.04+r()*0.05),bh=h*(0.1+r()*0.25)*(layer?.7:1);
  o+=`<rect x="${x.toFixed(0)}" y="${(base-bh).toFixed(0)}" width="${bw.toFixed(0)}" height="${(h-base+bh).toFixed(0)}" fill="${layer?'#17275a':'#0e1a3e'}"/>`;
  for(let wy=base-bh+16;wy<base;wy+=24)for(let wx=x+8;wx<x+bw-8;wx+=20)if(r()>.6)o+=`<rect x="${wx.toFixed(0)}" y="${wy.toFixed(0)}" width="7" height="10" fill="#ffd27a" opacity=".8"/>`;
  x+=bw+2}}
 return o}
function tower(x,base,h){return `<path d="M${x-9} ${base} L${x-3} ${base-h*0.86} L${x+3} ${base-h*0.86} L${x+9} ${base}Z" fill="#0a1230"/><ellipse cx="${x}" cy="${base-h*0.62}" rx="${h*0.07}" ry="${h*0.022}" fill="#0a1230"/><path d="M${x} ${base-h*0.86} L${x} ${base-h}" stroke="#0a1230" stroke-width="3"/><circle cx="${x}" cy="${base-h}" r="3" fill="#ff4a4a"/>`}
// PFP 1000x1000
const pfp=`<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">${defs}
 <clipPath id="circ"><circle cx="500" cy="500" r="486"/></clipPath>
 <g clip-path="url(#circ)">${skyline(1000,1000,780,3)}${tower(840,780,540)}
 <rect y="760" width="1000" height="240" fill="#0b1430"/>
 <circle cx="520" cy="500" r="470" fill="url(#glow)"/><g transform="translate(512,505) scale(.86)">${cyto()}</g></g>
 <circle cx="500" cy="500" r="486" fill="none" stroke="#ffcf5a" stroke-width="28"/></svg>`;
fs.writeFileSync('pfp.svg',pfp);
// COVER 1640x624 (FB) — character left-center, text right, safe middle
const cover=(w,h,sc,cx,cy,tx,fs1,fs2)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${defs}
 ${skyline(w,h,h*0.8,9)}${tower(w*0.93,h*0.8,h*0.9)}<rect y="${h*0.8}" width="${w}" height="${h*0.2}" fill="#0b1430"/>
 <circle cx="${cx}" cy="${cy-40}" r="${h*0.62}" fill="url(#glow)"/><g transform="translate(${cx},${cy}) scale(${sc})">${cyto()}</g>
 <g font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900">
  <text x="${tx}" y="${h*0.4}" font-size="${fs1}" fill="#fff" stroke="#0a1f24" stroke-width="${fs1*0.08}" paint-order="stroke" filter="url(#cut)">THE BODY</text>
  <text x="${tx}" y="${h*0.4+fs1*0.98}" font-size="${fs1}" fill="#ffcf5a" stroke="#0a1f24" stroke-width="${fs1*0.08}" paint-order="stroke" filter="url(#cut)">IS THE 6IX</text>
  <text x="${tx+4}" y="${h*0.4+fs1*0.98+fs2*1.9}" font-size="${fs2}" fill="#8fe8d8" font-weight="700">Science in 30 seconds · live from inside your body</text>
 </g></svg>`;
fs.writeFileSync('cover.svg',cover(1640,624,.5,430,365,720,104,26));
fs.writeFileSync('banner.svg',cover(2560,1440,.62,1030,860,1290,170,46));
