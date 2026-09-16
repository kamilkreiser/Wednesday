// Drafter-side comment-only check of routes/verification.ts base 80686962 vs head a376756ab, by PARSER, with controls.
// Two instruments (the #999 gate's method): (1) ts.transpileModule removeComments:true, byte compare (blind to
// type-only edits); (2) AST leaf-token walk from ts.createSourceFile, JSDoc node kinds excluded (sees type-only edits).
// Reads only; typescript is required by absolute path from the Secuura checkout's node_modules (no write there).
// Usage: node commentonly_parser.cjs <base.ts> <head.ts>
const fs = require('fs');
const ts = require('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules/typescript');
const [baseP, headP] = process.argv.slice(2);
const base = fs.readFileSync(baseP, 'utf8');
const head = fs.readFileSync(headP, 'utf8');

function transpiled(src) {
  return ts.transpileModule(src, { compilerOptions: { removeComments: true, target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS }, reportDiagnostics: false }).outputText;
}
function leaves(src) {
  const sf = ts.createSourceFile('x.ts', src, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  const out = [];
  const isJsDoc = (n) => n.kind >= ts.SyntaxKind.FirstJSDocNode && n.kind <= ts.SyntaxKind.LastJSDocNode;
  (function walk(n) {
    if (isJsDoc(n)) return;
    const kids = n.getChildren(sf).filter((k) => !isJsDoc(k));
    if (kids.length === 0) { if (n.kind !== ts.SyntaxKind.EndOfFileToken) out.push(n.kind + ':' + n.getText(sf)); return; }
    kids.forEach(walk);
  })(sf);
  return { out, diags: sf.parseDiagnostics.length };
}
function compare(label, a, b) {
  const la = leaves(a), lb = leaves(b);
  const tIdentical = transpiled(a) === transpiled(b);
  const aIdentical = la.out.length === lb.out.length && la.out.every((x, i) => x === lb.out[i]);
  console.log(`${label.padEnd(58)} transpile_identical=${tIdentical} ast_leaf_identical=${aIdentical} (${la.out.length}/${lb.out.length}) diags=${la.diags}/${lb.diags} raw_identical=${a === b}`);
}
function mutate(label, from, to) {
  const n = head.split(from).length - 1;
  if (n !== 1) { console.log(`${label.padEnd(58)} CONTROL NOT PLACED: anchor count ${n} != 1`); return; }
  compare(label, head, head.replace(from, to));
}
compare('SUBJECT verification.ts base 80686962 vs head a376756ab', base, head);
mutate('CONTROL code edit ?? null -> || null (F3 tamper)', "const persistedStatus = (doc as any).blockchain?.status ?? null;", "const persistedStatus = (doc as any).blockchain?.status || null;");
mutate('CONTROL F2 guard dropped', ": persistedStatus == null && persistedConfidence === 'pending-onchain'", ": persistedConfidence === 'pending-onchain'");
mutate('CONTROL type-only edit (status: unknown -> any)', "  status: unknown,\n): 'on-chain'", "  status: any,\n): 'on-chain'");
mutate('CONTROL added line comment', "const persistedStatus = (doc as any).blockchain?.status ?? null;", "const persistedStatus = (doc as any).blockchain?.status ?? null; // qa");
mutate('CONTROL JSDoc-only edit', " * BACKLOG #G6 — verifier-role", " * BACKLOG #G6 (qa) — verifier-role");
mutate('CONTROL code smuggled out of a comment', "// `status` is not producible today.", "// `status` is not producible today.\nconst qaSmuggled = 1;");
mutate('CONTROL string literal in code', "return 'off-chain-only';\n  }\n}", "return 'off-chain-only ';\n  }\n}");
