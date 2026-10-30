const ts=require('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules/typescript');const fs=require('fs');
function strip(f){const src=fs.readFileSync(f,'utf8');const sc=ts.createScanner(ts.ScriptTarget.Latest,false,ts.LanguageVariant.Standard,src);let out='',pos=0,k,n=0;
while((k=sc.scan())!==ts.SyntaxKind.EndOfFileToken){ if(k===ts.SyntaxKind.SingleLineCommentTrivia||k===ts.SyntaxKind.MultiLineCommentTrivia){out+=src.slice(pos,sc.getTokenPos());pos=sc.getTextPos();n++;} }
out+=src.slice(pos);return {out,n};}
const [a,b]=[strip(process.argv[2]),strip(process.argv[3])];
const norm=s=>s.split('\n').map(l=>l.trimEnd()).filter(l=>l.trim()!=='').join('\n');
console.log('comments',a.n,b.n,'stripped-equal(ws-normalised):',norm(a.out)===norm(b.out), 'raw-equal:',a.out===b.out);
fs.writeFileSync('/tmp/g25/sa.txt',a.out);fs.writeFileSync('/tmp/g25/sb.txt',b.out);
