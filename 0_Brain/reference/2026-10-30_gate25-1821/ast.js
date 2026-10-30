const ts=require('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules/typescript');const fs=require('fs');
const p=ts.createPrinter({removeComments:true});
const pr=f=>p.printFile(ts.createSourceFile('x.ts',fs.readFileSync(f,'utf8'),ts.ScriptTarget.Latest,true));
const [a,b]=[pr(process.argv[2]),pr(process.argv[3])];
console.log('AST-print(no comments) equal:',a===b,'len',a.length,b.length);
