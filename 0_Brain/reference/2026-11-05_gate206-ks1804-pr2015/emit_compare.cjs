const ts = require(process.argv[2]);
const fs = require('fs');
const tc = JSON.parse(fs.readFileSync(process.argv[3],'utf8')).compilerOptions;
const co = ts.convertCompilerOptionsFromJson({...tc, removeComments:true, sourceMap:false, declaration:false}, '.').options;
function stmts(f){
  const out = ts.transpileModule(fs.readFileSync(f,'utf8'), {compilerOptions: co, fileName: f}).outputText;
  const sf = ts.createSourceFile('x.js', out, ts.ScriptTarget.ES2022, true);
  return {out, s: sf.statements.map(s=>s.getText(sf))};
}
const b = stmts(process.argv[4]), h = stmts(process.argv[5]);
console.log('base stmts', b.s.length, 'head stmts', h.s.length);
const ms = a=>a.slice().sort().join('\n@@\n');
console.log('multiset equal:', ms(b.s)===ms(h.s));
console.log('sequence equal:', b.s.join('\n')===h.s.join('\n'));
b.s.forEach((x,i)=>{ if(x!==h.s[i]) console.log('DIFF at', i+1, '\n  base:', x.slice(0,100).replace(/\n/g,' '), '\n  head:', h.s[i].slice(0,100).replace(/\n/g,' ')); });
