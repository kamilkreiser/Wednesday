const fs=require('fs'),path=require('path');
const src=fs.readFileSync(process.argv[2],'utf8');
const body=src.slice(src.indexOf('function lexSpans'),src.indexOf('const inAny'));
const lexSpans=new Function(body+';return lexSpans;')();
let best={n:0},bigF={s:0},files=0;
const walk=(d)=>{let es;try{es=fs.readdirSync(d,{withFileTypes:true})}catch{return}
 for(const e of es){if(e.name==='node_modules'||e.name==='dist'||e.name.startsWith('.'))continue;const f=path.join(d,e.name);
  if(e.isDirectory()){walk(f);continue}
  if(!/\.(ts|tsx|mts|cts)$/.test(e.name))continue;files++;const t=fs.readFileSync(f,'utf8');const n=lexSpans(t).stringStarts.size;
  if(n>best.n)best={n,f};if(t.length>bigF.s)bigF={s:t.length,f}}};
for(const d of process.argv.slice(3))walk(d);
console.log(JSON.stringify({files,maxStringStarts:best,largestFile:bigF}));
