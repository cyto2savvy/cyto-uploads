import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const svg = fs.readFileSync('ff.svg','utf8');
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1800,height:600}, deviceScaleFactor:2});
await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
const el = await p.$('svg'); await el.screenshot({path:'ff.png', omitBackground:true});
await b.close(); console.log('ok');
