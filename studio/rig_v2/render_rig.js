#!/usr/bin/env node
// usage: node render_rig.js timeline.json outDir [size=1080] [startSec] [endSec]   -> outDir/f00000.png (transparent) + cyto.webm (alpha) if libvpx exists
const fs=require('fs'),path=require('path'),{execSync}=require('child_process');
const {frameSvg}=require('./cyto_rig.js'); const {chromium}=require('playwright');
(async()=>{
 const tl=JSON.parse(fs.readFileSync(process.argv[2])); const out=process.argv[3]; const size=+(process.argv[4]||1080);
 const t0=+(process.argv[5]||0), t1=+(process.argv[6]||tl.duration), fps=tl.fps||30;
 process.env.SEED=process.env.SEED||'3';
 fs.mkdirSync(out,{recursive:true});
 const br=await chromium.launch(); const pg=await br.newPage({viewport:{width:size,height:size}});
 await pg.setContent('<body style="margin:0;background:transparent"></body>');
 const n=Math.round((t1-t0)*fps);
 for(let i=0;i<n;i++){ const t=t0+i/fps;
  await pg.evaluate(([s,t])=>{document.body.innerHTML=s;const e=document.querySelector('svg');e.pauseAnimations();e.setCurrentTime(t);},[frameSvg(t,tl,size),t]);
  await pg.screenshot({path:path.join(out,'f'+String(i).padStart(5,'0')+'.png'),omitBackground:true});
  if(i%60===0) console.log('frame',i,'/',n);
 }
 await br.close();
 try{ execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${out}/f%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 28 ${out}/cyto.webm`); console.log('webm ok'); }catch(e){ console.log('no vp9 alpha encoder; use the PNG sequence'); }
 console.log('done',n,'frames');
})();
