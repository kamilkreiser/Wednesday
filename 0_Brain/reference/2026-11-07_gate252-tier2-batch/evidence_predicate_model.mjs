const real=(s,c)=>(s!==undefined&&typeof s!=='string')||(c!==undefined&&typeof c!=='string');
const G4=(s,c)=>(s!==undefined&&typeof s==='object')||(c!==undefined&&typeof c==='object');
const G3=(s,c)=>(s!=null&&typeof s!=='string')||(c!=null&&typeof c!=='string');
const TR=(s,c)=>(s&&typeof s!=='string')||(c&&typeof c!=='string');
const vals=[null,0,false,123,true,['a'],{},'',  'x'];
const cells={P8:['state',[null,0,false]],P9:['state',[123,true]],P10:['code_challenge',[null,0,false]],P11:['code_challenge',[123,true]]};
const mk=(f,v)=>f==='state'?[v,undefined]:['xyz',v];
const ok=(fn)=>Object.entries(cells).map(([k,[f,vs]])=>[k,vs.every(v=>fn(...mk(f,v)))?'green':'RED']);
for(const [n,fn] of Object.entries({real,G4,G3,TR})) console.log(n,JSON.stringify(ok(fn)));
// tamper: null removed from P8
console.log('tamper P8 w/o null, G3:', [0,false].every(v=>G3(v,undefined))?'green':'RED','| real:',[0,false].every(v=>real(v,undefined))?'green':'RED');
console.log('control: real admits string/empty/undefined:', !real('x'),!real(''),!real(undefined,undefined));
