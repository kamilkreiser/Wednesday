// usage: node survey.cjs <check.cjs> <root>...  : lists SPEC matches the lexer filter drops, plus counts
const fs=require('fs'),path=require('path');
const src=fs.readFileSync(process.argv[2],'utf8');
const grab=(start,end)=>{const a=src.indexOf(start);const b=src.indexOf(end,a);return src.slice(a,b);};
const code=grab('const SPEC','function sourceSpecifiers')+grab('function lexSpans','/** The nearest node_modules');
const {SPEC,lexSpans,inAny}=new Function(code+';return {SPEC,lexSpans,inAny};')();
let files=0,raw=0,kept=0;const dropped=[];
const walk=d=>{let es;try{es=fs.readdirSync(d,{withFileTypes:true})}catch{return}
 for(const e of es){if(e.name==='node_modules'||e.name==='dist'||e.name.startsWith('.'))continue;const f=path.join(d,e.name);
  if(e.isDirectory()){walk(f);continue} if(!/\.(ts|tsx|mts|cts)$/.test(e.name))continue; files++;
  const t=fs.readFileSync(f,'utf8');const {stringStarts,comments}=lexSpans(t);
  for(const m of t.matchAll(SPEC)){raw++;const q=m.index+m[0].indexOf(m[1])-1;
   if(!stringStarts.has(q)||inAny(comments,m.index)){const ln=t.slice(0,m.index).split('\n').length;dropped.push(`${f}:${ln}: ${t.split('\n')[ln-1].trim().slice(0,160)}`)} else kept++;}}};
for(const r of process.argv.slice(3))walk(r);
console.log(`files ${files} raw ${raw} kept ${kept} dropped ${dropped.length}`);dropped.forEach(x=>console.log(x));
