// parser_proof.js — is every changed line of ssrf-guard.ts CODE? Parse base and head with the TypeScript compiler (the
// checkout's own typescript), print both with removeComments, and diff the comment-free texts. Also counts the comment
// ranges touched. Usage: node parser_proof.js <typescript module path> <base.ts> <head.ts>
const [tsPath, basePath, headPath] = process.argv.slice(2);
const ts = require(tsPath); const fs = require('fs');
const strip = (p) => { const sf = ts.createSourceFile(p, fs.readFileSync(p, 'utf8'), ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  return ts.createPrinter({ removeComments: true }).printFile(sf).split('\n'); };
const commentText = (p) => { const text = fs.readFileSync(p, 'utf8'); const out = []; const sc = ts.createScanner(ts.ScriptTarget.ES2022, false, ts.LanguageVariant.Standard, text);
  for (let k = sc.scan(); k !== ts.SyntaxKind.EndOfFileToken; k = sc.scan()) if (k === ts.SyntaxKind.SingleLineCommentTrivia || k === ts.SyntaxKind.MultiLineCommentTrivia) out.push(sc.getTokenText()); return out; };
const b = strip(basePath), h = strip(headPath);
const bs = new Set(b), hs = new Set(h);
const removed = b.filter((l) => !hs.has(l)), added = h.filter((l) => !bs.has(l));
const cb = commentText(basePath), ch = commentText(headPath);
console.log(JSON.stringify({ ts: ts.version, codeLinesBase: b.length, codeLinesHead: h.length, codeRemoved: removed, codeAdded: added,
  commentsBase: cb.length, commentsHead: ch.length, commentsIdentical: JSON.stringify(cb) === JSON.stringify(ch),
  headHasLiveRace: h.some((l) => l.includes('Promise.race(')), headDeadlineUsesRemaining: h.some((l) => /\}, remainingMs\);/.test(l)) }, null, 1));
