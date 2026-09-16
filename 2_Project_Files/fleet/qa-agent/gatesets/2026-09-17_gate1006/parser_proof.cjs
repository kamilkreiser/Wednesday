// parser_proof.cjs — #1006 Q1: is the header commit 86fe59e6b COMMENT-ONLY over its parent e28c91f9b, and are 9 / 10 / 1 the counts
// READ FROM the exact sets? (1) transpileModule removeComments byte compare; (2) AST leaf walk (childless nodes, kind + text; JSDoc and
// EOF excluded). S0 = develop vs prev (must DIFFER: the two exact-set entries), S1 = prev vs head (must be IDENTICAL on both), S2 = develop
// vs head-with-the-2-entries-removed (must be IDENTICAL: the whole ks727 delta is 2 entries + comment). Controls on the same instrument.
// Then the counts: EXPECTED_CORPUS / EXPECTED_HANDLERS array-literal elements, distinct modules, FORWARDING_HANDLERS elements — by AST.
// Usage: node parser_proof.cjs <clone tree> <ks727_develop.ts> <ks727_prev.ts> <ks727_head.ts>
const [TREE, DP, PP, HP] = process.argv.slice(2);
const ts = require(TREE + '/Blockchain/Dev/node_modules/typescript'); const fs = require('fs');
console.log('parser_proof', new Date().toString(), 'typescript', ts.version);
const tr = s => ts.transpileModule(s, { compilerOptions: { removeComments: true, target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext }, reportDiagnostics: false }).outputText;
function leaves(s) { const sf = ts.createSourceFile('x.ts', s, ts.ScriptTarget.Latest, true); const out = [];
  (function walk(n) { const k = n.getChildren(sf); if (k.length === 0) { if (!ts.isJSDoc(n) && n.kind !== ts.SyntaxKind.EndOfFileToken) out.push(ts.SyntaxKind[n.kind] + ':' + n.getText(sf)); } else k.forEach(walk); })(sf);
  return { out, diags: sf.parseDiagnostics.length }; }
let all = true;
function cmp(label, a, b, eTr, eAst) { const la = leaves(a), lb = leaves(b); const trS = tr(a) === tr(b);
  const astS = la.out.length === lb.out.length && la.out.every((x, i) => x === lb.out[i]);
  const ok = trS === eTr && astS === eAst; all = all && ok;
  console.log(`${label} | transpile identical ${trS} | AST leaves identical ${astS} (${la.out.length}/${lb.out.length}) | parse diags ${la.diags}/${lb.diags} | raw identical ${a === b} | expected tr=${eTr} ast=${eAst} -> ${ok ? 'OK' : 'MISMATCH'}`); }
function once(s, a, b) { const n = s.split(a).length - 1; if (n !== 1) throw new Error('anchor count ' + n + ' for ' + a.slice(0, 80)); return s.replace(a, b); }
const D = fs.readFileSync(DP, 'utf8'), Pv = fs.readFileSync(PP, 'utf8'), H = fs.readFileSync(HP, 'utf8');
const E1 = "      'services/demo-service/src/middleware/errorHandler.ts',\n";
const E2 = "      'services/demo-service/src/middleware/errorHandler.ts → errorHandler',\n";
console.log('entry lines: head', H.split(E1).length - 1, H.split(E2).length - 1, '| develop', D.split(E1).length - 1, D.split(E2).length - 1);
console.log('== SUBJECTS');
cmp('S0 develop vs prev e28c91f9b (the 2 exact-set entries: must differ)', D, Pv, false, false);
cmp('S1 prev e28c91f9b vs head 86fe59e6b (the header commit: must be identical)', Pv, H, true, true);
cmp('S2 develop vs head-with-the-2-entries-removed (every other ks727 delta is comment: must be identical)', D, once(once(H, E1, ''), E2, ''), true, true);
console.log('== CONTROLS (on head)');
cmp('C1 code: an exact-set entry string edited', H, once(H, E2, "      'services/demo-service/src/middleware/errorHandler.ts → errorHandlerX',\n"), false, false);
cmp('C2 added line comment', H, once(H, "const FORWARDING_HANDLERS = new Set([\n", "// qa inert\nconst FORWARDING_HANDLERS = new Set([\n"), true, true);
cmp('C3 type-only edit (transpile blind spot): `as Handler` -> `as unknown as Handler`', H, once(H, "handler: value as Handler, module: mod", "handler: value as unknown as Handler, module: mod"), true, false);
cmp('C4 header count edited back to 8/9 (comment text)', H, once(H, "Count today: 9 modules contributing 10 handlers.", "Count today: 8 modules contributing 9 handlers."), true, true);
cmp('C5 code smuggled after a header comment line, at statement level', H, once(H, "//          answering it (`FORWARDING_HANDLERS`, also an exact set). A handler\n", "//          answering it (`FORWARDING_HANDLERS`, also an exact set). A handler\nvoid 0;\n"), false, false);
console.log('ALL CONTROLS AND SUBJECTS AS EXPECTED:', all);
console.log('== COUNTS READ FROM THE EXACT SETS (AST: the array literal initialiser of each const; no regex)');
function arrays(s, label) {
  const sf = ts.createSourceFile('x.ts', s, ts.ScriptTarget.Latest, true); const found = {};
  (function walk(n) {
    if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name) && ['EXPECTED_CORPUS', 'EXPECTED_HANDLERS', 'EXPECTED_INLINE_SITES'].includes(n.name.text) && n.initializer && ts.isArrayLiteralExpression(n.initializer)) {
      found[n.name.text] = n.initializer.elements.map(e => ts.isStringLiteral(e) ? e.text : '<non-literal:' + ts.SyntaxKind[e.kind] + '>');
    }
    if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name) && n.name.text === 'FORWARDING_HANDLERS' && n.initializer && ts.isNewExpression(n.initializer)) {
      const a = n.initializer.arguments && n.initializer.arguments[0];
      found.FORWARDING_HANDLERS = a && ts.isArrayLiteralExpression(a) ? a.elements.map(e => ts.isStringLiteral(e) ? e.text : '<non-literal>') : ['<not an array literal>'];
    }
    n.forEachChild(walk);
  })(sf);
  const C = found.EXPECTED_CORPUS || [], Hs = found.EXPECTED_HANDLERS || [], F = found.FORWARDING_HANDLERS || [];
  const mods = new Set(Hs.map(x => x.split(' → ')[0]));
  const multi = [...mods].filter(m => Hs.filter(x => x.startsWith(m + ' → ')).length > 1);
  console.log(`${label}: EXPECTED_CORPUS ${C.length} | EXPECTED_HANDLERS ${Hs.length} across ${mods.size} distinct modules (multi-handler modules: ${JSON.stringify(multi)}) | FORWARDING_HANDLERS ${F.length} | EXPECTED_INLINE_SITES ${(found.EXPECTED_INLINE_SITES || ['<absent>']).length} | corpus == handler modules: ${JSON.stringify([...mods].sort()) === JSON.stringify([...C].sort())} | non-literal elements: ${[...C, ...Hs, ...F].filter(x => x.startsWith('<')).length}`);
  const hdr = (s.match(/Count today: (\d+) modules contributing (\d+) handlers/) || []).slice(1); const nth = (s.match(/The (\d+)th handler is/) || []).slice(1); const of = (s.match(/Of those (\d+), exactly (\d+) is a FILTER/) || []).slice(1);
  console.log(`${label}: HEADER says modules=${hdr[0]} handlers=${hdr[1]} | "The Nth handler"=${nth[0]} | "Of those N, exactly M"=${of[0]}/${of[1]} | header==sets: ${Number(hdr[0]) === mods.size && Number(hdr[1]) === Hs.length && Number(nth[0]) === Hs.length && Number(of[0]) === Hs.length && Number(of[1]) === F.length}`);
}
arrays(D, 'develop 40fe4db69'); arrays(Pv, 'prev    e28c91f9b'); arrays(H, 'head    86fe59e6b');
console.log('control: the same AST reader on a fixture with a known answer');
arrays("const EXPECTED_CORPUS = ['a.ts', 'b.ts'];\nconst EXPECTED_HANDLERS = ['a.ts → x', 'a.ts → y', 'b.ts → x'];\nconst FORWARDING_HANDLERS = new Set(['a.ts → y']);\nconst EXPECTED_INLINE_SITES: string[] = [];\n// Count today: 2 modules contributing 3 handlers.\n// The 3th handler is\n// Of those 3, exactly 1 is a FILTER\n", 'fixture (expect 2 | 3 across 2 | multi [a.ts] | 1 | 0 | header==sets true)');
