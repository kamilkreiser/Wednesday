// Drafter-side comment-only check of the #1003 composed ks1165 test, base 5b4f38a48 (04ab42a65) vs head c5488a689 (3c86f0c93), by PARSER, with controls.
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
compare('SUBJECT composed ks1165 test base 5b4f38a48 vs head c5488a689', base, head);
mutate('CONTROL code edit (path literal in code)', "const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');", "const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.js'), 'utf8');");
mutate('CONTROL type-only edit (status: number -> any)', "status(code: number) {", "status(code: any) {");
mutate('CONTROL added line comment', "const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');", "const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8'); // qa");
mutate('CONTROL block-comment edit', " * with `CSRF_TOKEN_MISSING`.", " * with `CSRF_TOKEN_MISSING` (qa).");
mutate('CONTROL code smuggled after a line comment', "// T3 / T4). The real-app cells are in ks1165-real-app-csrf-mount-order.test.ts.", "// T3 / T4). The real-app cells are in ks1165-real-app-csrf-mount-order.test.ts.\nconst qaSmuggled = 1;");
