import fs from 'node:fs';
const [,, d] = process.argv;
let parse;
try { ({ parseAccessLine: parse } = await import(d + '/repo/systemTest/akto/src/scan/gatewayTimeline.ts')); console.log('imported real parseAccessLine'); }
catch (e) { console.log('real import failed:', String(e.message).slice(0,120)); }
if (!parse) {
  const src = fs.readFileSync(d + '/repo/systemTest/akto/src/scan/gatewayTimeline.ts','utf8');
  const m = /const LINE =\s*\n?\s*(\/.*\/);/.exec(src);
  const LINE = eval(m[1]); console.log('using extracted regex', String(LINE).length);
  parse = (l) => { const x = LINE.exec(l); return x ? { s: x[10], ua: x[11], t: x.slice(1,7).join('|') } : null; };
}
const b = fs.readFileSync(d + '/evidence/log_base.txt','utf8').trim().split('\n');
const h = fs.readFileSync(d + '/evidence/log_head.txt','utf8').trim().split('\n');
console.log('node', process.version);
b.forEach((l,i) => console.log(i, JSON.stringify(parse(l)), JSON.stringify(parse(h[i]))));
// control: garbage must be null
console.log('control null:', parse('not a log line'));
