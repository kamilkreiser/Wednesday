// tokeq_gate31.js <typescript module dir> <a.ts> <b.ts> — CODE-TOKEN EQUIVALENCE for #1303 (KS-1350), the drafter's instrument.
// Parses each file with the TypeScript PARSER (ts.createSourceFile, setParentNodes) and walks node.getChildren(sf) to the LEAVES, dropping every
// node in the JSDoc kind range (ts.SyntaxKind.FirstJSDocNode..LastJSDocNode) with its whole subtree — the parser attaches /** */ blocks to the AST
// as JSDoc nodes, so without that filter a comment edit reads as a code difference; ordinary comments are trivia and never leaves. A raw
// ts.createScanner is NOT used: without the parser driving reScanTemplateToken it mis-lexes the first backtick (Seat B 33rd's i4 finding, relayed
// by Wednesday). Prints: leaves(a) leaves(b) IDENTICAL|DIFFER and, on DIFFER, the first diverging leaf. rc 0 IDENTICAL, 1 DIFFER, 2 usage/parse.
const ts = require(process.argv[2]);
const fs = require('fs');
function leaves(file) {
  const src = fs.readFileSync(file, 'utf8');
  const sf = ts.createSourceFile(file, src, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
  const out = [];
  const jsdoc = (k) => k >= ts.SyntaxKind.FirstJSDocNode && k <= ts.SyntaxKind.LastJSDocNode;
  (function walk(n) {
    if (jsdoc(n.kind)) return;
    const ch = n.getChildren(sf);
    if (ch.length === 0) { out.push([ts.SyntaxKind[n.kind], n.getText(sf)]); return; }
    for (const c of ch) walk(c);
  })(sf);
  return { out, diag: sf.parseDiagnostics ? sf.parseDiagnostics.length : -1 };
}
if (process.argv.length < 5) { console.log('usage: tokeq_gate31.js <typescript dir> <a.ts> <b.ts>'); process.exit(2); }
const A = leaves(process.argv[3]), B = leaves(process.argv[4]);
let first = -1;
for (let i = 0; i < Math.max(A.out.length, B.out.length); i++) {
  const x = A.out[i], y = B.out[i];
  if (!x || !y || x[0] !== y[0] || x[1] !== y[1]) { first = i; break; }
}
const same = first === -1;
const eof = (L) => L.out.filter((x) => x[0] !== 'EndOfFileToken').length;
console.log(`typescript ${ts.version} | leaves ${A.out.length} vs ${B.out.length} (${eof(A)} vs ${eof(B)} without the EndOfFileToken leaf) | parse diagnostics ${A.diag} vs ${B.diag} | JSDoc kinds ${ts.SyntaxKind.FirstJSDocNode}-${ts.SyntaxKind.LastJSDocNode} excluded | ${same ? 'IDENTICAL' : 'DIFFER at leaf ' + first + ': ' + JSON.stringify(A.out[first]) + ' vs ' + JSON.stringify(B.out[first])}`);
process.exit(same ? 0 : 1);
