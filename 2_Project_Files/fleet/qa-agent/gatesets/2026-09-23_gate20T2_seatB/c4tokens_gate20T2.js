// c4tokens_gate20T2.js — the gate20T2 drafter's re-derivation of the comment_patch (C4) TOKEN-EQUIVALENCE instrument, BOTH tokenisations:
//   SCANNER  — every non-trivia token (kind, text) from ts.createScanner(skipTrivia=true), the seat's raise/c4tokens.js instrument (it reported 17731);
//   LEAVES   — every leaf node (kind, text) of ts.createSourceFile's AST, the checker's "parser leaves" wording (it reported 17679).
// A sha256 over each JSON stream. Usage: node c4tokens_gate20T2.js <typescript module dir> <file> [<file> ...]
// -> one JSON line per file: {"file":…, "scanner_n":…, "scanner_sha256":…, "leaves_n":…, "leaves_sha256":…, "ts":"<version>"}
// READ-ONLY: typescript is loaded by absolute path (argv[2]); the files are read; nothing is written. Not the seat's file — written from its description.
const ts = require(process.argv[2]);
const fs = require('fs'), crypto = require('crypto');
const H = (x) => crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
for (const file of process.argv.slice(3)) {
  const src = fs.readFileSync(file, 'utf8');
  const sc = ts.createScanner(ts.ScriptTarget.Latest, true, ts.LanguageVariant.Standard, src);
  const toks = []; let k;
  while ((k = sc.scan()) !== ts.SyntaxKind.EndOfFileToken) {
    if (k === ts.SyntaxKind.SingleLineCommentTrivia || k === ts.SyntaxKind.MultiLineCommentTrivia || k === ts.SyntaxKind.WhitespaceTrivia || k === ts.SyntaxKind.NewLineTrivia) continue;
    toks.push([ts.SyntaxKind[k], sc.getTokenText()]);
  }
  const sf = ts.createSourceFile(file, src, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
  const leaves = [];
  const walk = (n) => { const kids = n.getChildren(sf); if (kids.length === 0) { if (n.kind !== ts.SyntaxKind.EndOfFileToken) leaves.push([ts.SyntaxKind[n.kind], n.getText(sf)]); } else kids.forEach(walk); };
  walk(sf);
  console.log(JSON.stringify({ file, scanner_n: toks.length, scanner_sha256: H(toks), leaves_n: leaves.length, leaves_sha256: H(leaves), ts: ts.version }));
}
