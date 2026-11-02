// QA GATE 126: the walk's own cost on bodies just under the node cap (19,999 values), and JSON.parse for comparison.
const { findStructuralBreach, STRUCTURAL_JSON_DEFAULTS: C } = require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944/repo/Blockchain/Dev/packages/shared/dist/middleware/request-limits.js');
const os = require('os');
function count(v){let n=0;const s=[v];while(s.length){const x=s.pop();n++;if(x&&typeof x==='object')for(const k of Object.keys(x))s.push(x[k]);}return n;}
const shapes = {
  arrays_19x1000: (() => { const a=[]; for(let i=0;i<19;i++) a.push(Array(1000).fill(1)); a.push(Array(977).fill(1)); return {a}; })(),
  wide_object_19998_keys: (() => { const o={}; for(let i=0;i<19998;i++) o['k'+i]=i; return o; })(),
  objects_of_strings: (() => { const a=[]; for(let i=0;i<999;i++) a.push({x:'aaaaaaaaaaaaaaaa',y:'bbbbbbbbbbbbbbbb',z:i,w:{q:i}}); return {a, b:Array(1000).fill(0).slice(0,1000)}; })(),
  nested_depth_31_x_600: (() => { const a=[]; for(let j=0;j<600;j++){ let v=1; for(let i=0;i<30;i++) v=[v]; a.push(v);} return {a}; })(),
};
console.log('node', process.version, 'load', os.loadavg().map(x=>x.toFixed(2)).join(' '), 'cpus', os.cpus().length);
for (const [name, v] of Object.entries(shapes)) {
  const n = count(v); const raw = JSON.stringify(v);
  const r = findStructuralBreach(v, C);
  for (let i=0;i<50;i++) findStructuralBreach(v, C); // warm
  const N=200; let t=process.hrtime.bigint(); for(let i=0;i<N;i++) findStructuralBreach(v, C); const walk=Number(process.hrtime.bigint()-t)/N/1e6;
  t=process.hrtime.bigint(); for(let i=0;i<N;i++) JSON.parse(raw); const parse=Number(process.hrtime.bigint()-t)/N/1e6;
  console.log(`${name}: values=${n} bytes=${raw.length} breach=${r} walk_ms=${walk.toFixed(3)} JSON.parse_ms=${parse.toFixed(3)} ratio=${(walk/parse).toFixed(2)}`);
}
// a hostile body: 1 MB flat array (refused at the first container)
const big = Array(524284).fill(0); let t=process.hrtime.bigint(); for(let i=0;i<200;i++) findStructuralBreach({a:big}, C); console.log('1MB flat array 524,284: breach', findStructuralBreach({a:big}, C), 'walk_ms', (Number(process.hrtime.bigint()-t)/200/1e6).toFixed(4));
const wide={}; for(let i=0;i<200000;i++) wide['k'+i]=i; t=process.hrtime.bigint(); for(let i=0;i<20;i++) findStructuralBreach(wide, C); console.log('200k-key object: breach', findStructuralBreach(wide, C), 'walk_ms', (Number(process.hrtime.bigint()-t)/20/1e6).toFixed(3), '(Object.keys of 200k is paid before the refusal)');
