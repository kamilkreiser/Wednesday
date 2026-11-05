const path=require('path');
const {ESLint}=require(path.join(process.argv[2],'node_modules','eslint'));
(async()=>{const e=new ESLint({cwd:process.argv[2]});const r=await e.lintFiles(process.argv.slice(3));
let err=0,warn=0;for(const f of r){err+=f.errorCount;warn+=f.warningCount;for(const m of f.messages)console.log(path.basename(f.filePath),m.line,m.ruleId,m.message)}
console.log(`files=${r.length} errors=${err} warnings=${warn}`);process.exit(err?1:0)})();
