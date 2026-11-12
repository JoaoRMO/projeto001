const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
const svg=fs.readFileSync('entregas.svg','utf8');
const mk=x=>`<html><head><style>@page{size:17cm 11.3333cm;margin:0}html,body{margin:0}svg{display:block;${x}}</style></head><body>${svg}</body></html>`;
const p=await b.newPage({viewport:{width:1536,height:1024},deviceScaleFactor:4016/1536});
await p.setContent(mk('width:1536px;height:1024px'));
await p.screenshot({path:'entregas_17cm_600dpi.png',clip:{x:0,y:0,width:1536,height:1024}});
await p.setContent(mk(''));await p.pdf({path:'entregas_17cm.pdf',width:'17cm',height:'11.3333cm',printBackground:true,pageRanges:'1'});
await b.close()})()
