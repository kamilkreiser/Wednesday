// Gate 140 (B): regenerate EVERY golden-g135.json entry myself from the head's cases-g135.ts with REAL zod 3.25.76
// (my develop worktree), and compare byte-for-byte. Also golden.json from cases.ts if it shares the contract.
// usage: node golden_regen.cjs <headDev> <baseDev> <out>
const path=require('path'), fs=require('fs'), {createRequire}=require('module');
const [H,B,OUT]=process.argv.slice(2);
const ts=createRequire(path.join(H,'package.json'))('typescript');
const zmod=createRequire(path.join(B,'package.json'))('zod'); const z3=zmod.z||zmod;
const ver=JSON.parse(fs.readFileSync(path.join(B,'node_modules/zod/package.json'),'utf8')).version;
const FX=path.join(H,'packages/shared/src/__tests__/fixtures/ks1725-zod3-golden');
const load=(f)=>{const js=ts.transpileModule(fs.readFileSync(path.join(FX,f),'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText; const m={exports:{}}; new Function('module','exports','require',js)(m,m.exports,require); return m.exports;};
const res={zod:ver}; const lines=[];
for (const [cf,gf] of [['cases-g135.ts','golden-g135.json'],['cases.ts','golden.json']]) {
  const mod=load(cf); const arr=Object.values(mod).find((v)=>Array.isArray(v)&&v.length&&v[0].build);
  const gold=JSON.parse(fs.readFileSync(path.join(FX,gf),'utf8')); const gc=gold.cases||gold;
  let eq=0, ne=0, missing=0;
  for (const c of arr) {
    let got; try { const r=c.build(z3,3).safeParse(c.input); got=r.success?'__SUCCESS__':JSON.stringify(r.error.issues); } catch(e){ got='THROW '+e.message; }
    if (!(c.name in gc)) { missing++; lines.push(gf+' MISSING '+c.name); continue; }
    if (gc[c.name]===got) eq++; else { ne++; lines.push(gf+' NE '+c.name+'\n   gold '+gc[c.name].slice(0,300)+'\n   z3   '+got.slice(0,300)); }
  }
  res[gf]={cases:arr.length, goldKeys:Object.keys(gc).length, goldZod:gold.zod, equal:eq, notEqual:ne, missing};
}
fs.writeFileSync(OUT, JSON.stringify(res,null,1)+'\n'+lines.join('\n')+'\n'); console.log(JSON.stringify(res));
