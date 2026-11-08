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
 <filter id="cut" x="-10%" y="-10%" width="130%" height="130%"><feDropShadow dx="7" dy="10" stdDeviation="0" flood-color="#000" flood-opacity=".38"/></filter>
 <filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
 <clipPath id="bodyclip"><circle r="300"/></clipPath>
 <clipPath id="hatclip"><path d="M-288 -150 C-300 -420 300 -420 288 -150Z"/></clipPath>
</defs>`;
const O='stroke="#0a1f24" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"';
function eye(x,flip){return `<g transform="translate(${x},-18)">
 <clipPath id="e${x<0?'L':'R'}"><ellipse rx="54" ry="60"/></clipPath>
 <ellipse rx="54" ry="60" fill="#fff" ${O}/>
 <circle cx="${flip*6}" cy="12" r="27" fill="#0b0b12"/><circle cx="${flip*6-9}" cy="1" r="9" fill="#fff"/>
 <g clip-path="url(#e${x<0?'L':'R'})"><rect x="-70" y="-70" width="140" height="62" fill="#34b8a4"/><rect x="-70" y="-14" width="140" height="9" fill="#0a1f24"/></g>
 <ellipse rx="54" ry="60" fill="none" ${O}/>
 <path d="M${-56} -80 Q0 ${-104+flip*-6} 56 -76" fill="none" ${O}/>
</g>`}
function cup(){return `<g transform="translate(-352,118) rotate(-7) scale(1.32)" filter="url(#cut)">
 <path d="M-72 -105 L72 -105 L54 108 Q0 122 -54 108Z" fill="url(#cupw)" ${O}/>
 <path d="M-68 -52 L68 -52 L62 34 L-62 34Z" fill="#c62828" ${O}/>
 <rect x="-64" y="-10" width="128" height="7" fill="#fff" opacity=".85"/>
 <path d="M-62 -125 L62 -125 L72 -105 L-72 -105Z" fill="#4a2c1f" ${O}/>
 <rect x="-52" y="-146" width="104" height="26" rx="10" fill="#5c3827" ${O}/>
 <g transform="translate(0,-9) scale(.78)"><circle r="62" fill="#3fc4b0" ${O}/>
  <path d="M-60 -12 C-60 -78 60 -78 60 -12Z" fill="#2c63d6" ${O}/><rect x="-62" y="-20" width="124" height="14" fill="#fff"/><circle cy="-72" r="12" fill="#fff" stroke="#0a1f24" stroke-width="6"/>
  <ellipse cx="-22" cy="14" rx="10" ry="12" fill="#fff"/><ellipse cx="22" cy="14" rx="10" ry="12" fill="#fff"/><circle cx="-20" cy="17" r="5" fill="#111"/><circle cx="24" cy="17" r="5" fill="#111"/>
  <path d="M-18 40 Q0 52 18 40" fill="none" stroke="#0a1f24" stroke-width="6" stroke-linecap="round"/></g>
 <g ${O} fill="url(#skinArm)"><ellipse cx="-70" cy="62" rx="26" ry="38"/><rect x="-74" y="46" width="112" height="30" rx="15"/><rect x="-72" y="72" width="104" height="30" rx="15"/></g>
</g>`}
function cyto(){
 let spots=''; for(let i=0;i<34;i++){const a=rnd()*6.28,r=Math.sqrt(rnd())*270;const x=Math.cos(a)*r,y=Math.sin(a)*r*0.95+20;
  if(Math.abs(x)<150&&y>-90&&y<20) continue; if(Math.abs(x)<110&&y>40&&y<170) continue; if(y<-80) continue; if(x>110&&y>90&&x<260) continue;if(x<-110&&y>95&&x>-260) continue;
  spots+=`<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(3+rnd()*6).toFixed(1)}" fill="#1f8f86" opacity=".6"/>`}
 let ribs=''; for(let i=-9;i<=9;i++) ribs+=`<path d="M${i*30} -150 L${i*34} -400" stroke="#102a74" stroke-width="5" opacity=".5"/>`;
 let pom=''; for(let i=0;i<22;i++){const a=rnd()*6.28,r=rnd()*34;pom+=`<circle cx="${(Math.cos(a)*r).toFixed(0)}" cy="${(Math.sin(a)*r).toFixed(0)}" r="5" fill="#e2dccd"/>`}
 return `<g filter="url(#cut)">
 <ellipse cx="20" cy="345" rx="250" ry="26" fill="#000" opacity=".28" filter="url(#soft)"/>
 <g><path d="M232 80 Q330 140 346 250" fill="none" stroke="#0a1f24" stroke-width="46" stroke-linecap="round"/><path d="M232 80 Q330 140 346 250" fill="none" stroke="url(#skinArm)" stroke-width="30" stroke-linecap="round"/>
 <circle cx="352" cy="262" r="52" fill="url(#skinArm)" ${O}/></g>
 <circle r="300" fill="url(#skin)" ${O}/>
 <g clip-path="url(#bodyclip)">${spots}
  <ellipse cx="-120" cy="-150" rx="120" ry="60" fill="#fff" opacity=".13" transform="rotate(-24 -120 -150)"/></g>
 <path d="M-232 70 Q-290 130 -300 170" fill="none" stroke="#0a1f24" stroke-width="46" stroke-linecap="round"/><path d="M-232 70 Q-290 130 -300 170" fill="none" stroke="url(#skinArm)" stroke-width="30" stroke-linecap="round"/>
 ${eye(-108,-1)}${eye(108,1)}
 <ellipse cx="-198" cy="62" rx="40" ry="26" fill="#9db0a6" opacity=".65"/><ellipse cx="198" cy="62" rx="40" ry="26" fill="#9db0a6" opacity=".65"/>
 <clipPath id="mo"><path d="M-78 78 Q0 100 78 78 Q66 160 0 166 Q-66 160 -78 78Z"/></clipPath>
 <path d="M-78 78 Q0 100 78 78 Q66 160 0 166 Q-66 160 -78 78Z" fill="#4a0f2b" ${O}/>
 <g clip-path="url(#mo)"><ellipse cx="0" cy="162" rx="48" ry="30" fill="#ff7f95"/></g>
 <g transform="translate(-178,150) rotate(-10)"><rect x="-58" y="-22" width="116" height="44" rx="22" fill="#ff9b3d" ${O}/><path d="M-36 8 L-22 -8 L-8 8 L6 -8 L20 8 L34 -8" fill="none" stroke="#c4541a" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>
 <g transform="translate(190,160)"><circle r="72" fill="url(#nuc)" ${O}/><circle cx="-24" cy="-26" r="15" fill="#efe6ff"/><path d="M-26 22 Q-8 38 12 18 Q24 6 36 22" fill="none" stroke="#d8c8ff" stroke-width="7" stroke-linecap="round"/></g>
 <g>
  <path d="M-288 -150 C-300 -420 300 -420 288 -150Z" fill="url(#hat)" ${O}/>
  <g clip-path="url(#hatclip)">${ribs}<ellipse cx="-150" cy="-290" rx="70" ry="90" fill="#fff" opacity=".1" transform="rotate(20 -150 -290)"/></g>
  <rect x="-300" y="-170" width="600" height="95" rx="40" fill="#142f84" ${O}/>
  <rect x="-296" y="-136" width="592" height="26" fill="#fff"/>
  <path d="M-290 -168 Q0 -190 290 -168" fill="none" stroke="#2c63d6" stroke-width="10" opacity=".55" stroke-linecap="round"/>
  <g transform="translate(0,-402)"><circle r="56" fill="#f6f3ea" ${O}/>${pom}</g>
 </g>
 </g>${cup()}`}
function skyline(w,h,base,seed){let s=seed;const r=()=>(s=(s*16807)%2147483647)/2147483647;let o='';
 o+=`<rect width="${w}" height="${h}" fill="url(#sky)"/>`;
 for(let i=0;i<130;i++) o+=`<circle cx="${(r()*w).toFixed(0)}" cy="${(r()*base*0.7).toFixed(0)}" r="${(r()*2.2+.6).toFixed(1)}" fill="#fff" opacity="${(.3+r()*.6).toFixed(2)}"/>`;
 o+=`<circle cx="${w*0.22}" cy="${base*0.2}" r="${Math.min(w,h)*0.05}" fill="#fff6d6" opacity=".9"/>`;
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
 <g transform="translate(535,520) scale(.78)">${cyto()}</g></g>
 <circle cx="500" cy="500" r="486" fill="none" stroke="#ffcf5a" stroke-width="28"/></svg>`;
fs.writeFileSync('pfp.svg',pfp);
// COVER 1640x624 (FB) — character left-center, text right, safe middle
const cover=(w,h,sc,cx,cy,tx,fs1,fs2)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${defs}
 ${skyline(w,h,h*0.8,9)}${tower(w*0.93,h*0.8,h*0.9)}<rect y="${h*0.8}" width="${w}" height="${h*0.2}" fill="#0b1430"/>
 <g transform="translate(${cx},${cy}) scale(${sc})">${cyto()}</g>
 <g font-family="Arial Black, Impact, DejaVu Sans, sans-serif" font-weight="900">
  <text x="${tx}" y="${h*0.4}" font-size="${fs1}" fill="#fff" stroke="#0a1f24" stroke-width="${fs1*0.08}" paint-order="stroke" filter="url(#cut)">THE BODY</text>
  <text x="${tx}" y="${h*0.4+fs1*0.98}" font-size="${fs1}" fill="#ffcf5a" stroke="#0a1f24" stroke-width="${fs1*0.08}" paint-order="stroke" filter="url(#cut)">IS THE 6IX</text>
  <text x="${tx+4}" y="${h*0.4+fs1*0.98+fs2*1.9}" font-size="${fs2}" fill="#8fe8d8" font-weight="700">Science in 30 seconds · live from inside your body</text>
 </g></svg>`;
fs.writeFileSync('cover.svg',cover(1640,624,.5,430,365,720,104,26));
fs.writeFileSync('banner.svg',cover(2560,1440,.62,1030,860,1290,170,46));
